"""L58 示例 2: 离线批量评估与对照报告

from __future__ import annotations

学习目标：
- 构造离线评估数据集（任务 + 期望输出）
- 用规则匹配、LLM-as-Judge 与人工标注三路评分
- 输出成本/质量对照报告，做候选模型决策

本示例不依赖 LLM 服务，使用注入策略让评估流程可在本地纯函数模式下跑通；
真实场景把 `JudgeFn` 和 `ModelFn` 替换为 OpenAI/Anthropic 客户端调用即可。

运行方式：
    python 02_offline_batch_eval.py
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
import statistics
import time

# ============================================================
# 第一部分：评估数据集与样本结构
# ============================================================

ModelFn = Callable[[str], str]
JudgeFn = Callable[[str, str, str], float]  # task, prediction, reference -> [0, 1]


@dataclass(frozen=True)
class EvalCase:
    """单条评估用例。

    教学设计：使用 frozen dataclass 防止评估过程中误改用例字段，保证可复现。
    """

    task_id: str
    task: str
    reference: str  # 期望输出（可来自人工标注或权威答案）
    tags: tuple[str, ...] = ()  # 用于按维度切片统计，例如 ("math", "easy")


@dataclass
class CaseResult:
    """单条用例的评分结果。"""

    case: EvalCase
    prediction: str
    rule_score: float  # 规则匹配 [0, 1]
    judge_score: float  # LLM-as-Judge [0, 1]
    latency_ms: float
    tokens: int
    error: str | None = None


# ============================================================
# 第二部分：三路评分函数（规则 / Judge / 人工标注）
# ============================================================


def score_by_rule(prediction: str, reference: str) -> float:
    """规则评分：基于子串包含与长度比例的轻量打分。

    教学说明：规则评分快、无副作用，适合"答案是否包含关键事实"等场景。
    缺点：忽略语义等价（如同义词替换）。
    """
    pred = prediction.strip().lower()
    ref = reference.strip().lower()
    if not ref:
        return 0.0
    if pred == ref:
        return 1.0
    # 子串包含 + 长度相近度（防止预测过短）
    contains = 1.0 if ref in pred else 0.0
    length_ratio = min(len(pred), len(ref)) / max(len(pred), len(ref))
    return round(0.7 * contains + 0.3 * length_ratio, 4)


def score_by_judge(judge_fn: JudgeFn, task: str, prediction: str, reference: str) -> float:
    """LLM-as-Judge 评分：把 task/prediction/reference 交给评审 LLM。

    教学说明：判官 LLM 通常用强模型（GPT-4 / Claude Opus），
    成本高但能识别语义等价。本示例用注入函数模拟，便于离线测试。
    """
    raw = judge_fn(task, prediction, reference)
    return max(0.0, min(1.0, float(raw)))


def score_by_human(annotations: dict[str, float], task_id: str) -> float | None:
    """人工标注评分：从已有标注表查询。

    教学说明：人工标注是黄金标准，但贵且慢。
    实践中只标注一小部分用例，作为 Judge 校准基准。
    """
    return annotations.get(task_id)


# ============================================================
# 第三部分：批量评估器
# ============================================================


@dataclass
class BatchEvaluator:
    """批量评估器。

    使用方式：
        evaluator = BatchEvaluator(model_fn=my_model, judge_fn=my_judge)
        report = evaluator.run(cases, human_annotations={...})
    """

    model_fn: ModelFn
    judge_fn: JudgeFn
    results: list[CaseResult] = field(default_factory=list)

    def run(
        self,
        cases: list[EvalCase],
        human_annotations: dict[str, float] | None = None,
    ) -> BatchReport:
        """跑完整批量评估，返回报告。"""
        annotations = human_annotations or {}
        self.results = []
        for case in cases:
            result = self._evaluate_one(case)
            self.results.append(result)

        return BatchReport.from_results(self.results, annotations)

    def _evaluate_one(self, case: EvalCase) -> CaseResult:
        """评估单条用例，捕获异常以避免单点失败拖垮全批。"""
        start = time.perf_counter()
        try:
            prediction = self.model_fn(case.task)
            error: str | None = None
        except (ValueError, RuntimeError, TimeoutError) as exc:
            # 教学说明：捕获预期异常，让可疑模型不会让整批 abort
            prediction = ""
            error = f"{type(exc).__name__}: {exc}"
        latency_ms = (time.perf_counter() - start) * 1000.0

        rule = score_by_rule(prediction, case.reference)
        if error:
            judge = 0.0
        else:
            judge = score_by_judge(self.judge_fn, case.task, prediction, case.reference)

        # tokens 教学性估算：按字符数 / 4，真实场景用 tiktoken 等工具
        tokens = (len(case.task) + len(prediction)) // 4

        return CaseResult(
            case=case,
            prediction=prediction,
            rule_score=rule,
            judge_score=judge,
            latency_ms=latency_ms,
            tokens=tokens,
            error=error,
        )


# ============================================================
# 第四部分：评估报告
# ============================================================


@dataclass
class BatchReport:
    """批量评估报告，可直接 print 到终端或序列化为 JSON。"""

    total: int
    rule_mean: float
    judge_mean: float
    human_mean: float | None
    judge_human_gap: float | None  # 用于校准 Judge 与人工标注的偏差
    error_rate: float
    avg_latency_ms: float
    total_tokens: int
    by_tag: dict[str, dict[str, float]]
    results: list[CaseResult]

    @classmethod
    def from_results(
        cls,
        results: list[CaseResult],
        annotations: dict[str, float],
    ) -> BatchReport:
        """从 results 聚合出报告。"""
        if not results:
            return cls(0, 0.0, 0.0, None, None, 0.0, 0.0, 0, {}, [])

        rule_scores = [r.rule_score for r in results]
        judge_scores = [r.judge_score for r in results]
        latencies = [r.latency_ms for r in results]
        errors = sum(1 for r in results if r.error is not None)
        tokens = sum(r.tokens for r in results)

        # 人工标注覆盖率与差距
        human_pairs = [
            (annotations[r.case.task_id], r.judge_score)
            for r in results
            if r.case.task_id in annotations
        ]
        if human_pairs:
            human_mean = statistics.fmean(h for h, _ in human_pairs)
            judge_human_gap = statistics.fmean(j - h for h, j in human_pairs)
        else:
            human_mean = None
            judge_human_gap = None

        # 按 tag 切片
        by_tag: dict[str, dict[str, float]] = {}
        for result in results:
            for tag in result.case.tags:
                slot = by_tag.setdefault(tag, {"count": 0.0, "rule": 0.0, "judge": 0.0})
                slot["count"] += 1
                slot["rule"] += result.rule_score
                slot["judge"] += result.judge_score
        for slot in by_tag.values():
            count = slot["count"]
            slot["rule"] = round(slot["rule"] / count, 4)
            slot["judge"] = round(slot["judge"] / count, 4)

        return cls(
            total=len(results),
            rule_mean=round(statistics.fmean(rule_scores), 4),
            judge_mean=round(statistics.fmean(judge_scores), 4),
            human_mean=round(human_mean, 4) if human_mean is not None else None,
            judge_human_gap=(round(judge_human_gap, 4) if judge_human_gap is not None else None),
            error_rate=round(errors / len(results), 4),
            avg_latency_ms=round(statistics.fmean(latencies), 2),
            total_tokens=tokens,
            by_tag=by_tag,
            results=results,
        )

    def render(self) -> str:
        """生成人类可读的对照报告字符串。"""
        lines = [
            "=" * 60,
            "Agent 离线批量评估报告",
            "=" * 60,
            f"用例总数: {self.total}",
            f"规则均分: {self.rule_mean:.4f}",
            f"Judge均分: {self.judge_mean:.4f}",
        ]
        if self.human_mean is not None:
            lines.append(f"人工均分: {self.human_mean:.4f}")
            lines.append(
                f"Judge 与人工偏差: {self.judge_human_gap:+.4f}  (>0 表示 Judge 偏松，<0 表示偏严)"
            )
        lines.extend(
            [
                f"错误率: {self.error_rate:.2%}",
                f"平均延迟: {self.avg_latency_ms:.2f} ms",
                f"Token 总数: {self.total_tokens}",
                "-" * 60,
                "按标签切片:",
            ]
        )
        for tag, stats in sorted(self.by_tag.items()):
            count = int(stats["count"])
            lines.append(
                f"  [{tag}] count={count} rule={stats['rule']:.4f} judge={stats['judge']:.4f}"
            )
        return "\n".join(lines)


# ============================================================
# 第五部分：演示主函数
# ============================================================


def _demo_model(task: str) -> str:
    """演示用模型：按规则生成回答（真实场景接 LLM 客户端）。"""
    if "1+1" in task:
        return "答案是 2"
    if "首都" in task:
        return "中国的首都是北京"
    if "raise" in task.lower():
        msg = "demo 模型故意抛错以演示异常路径"
        raise ValueError(msg)
    return "（无法回答）"


def _demo_judge(task: str, prediction: str, reference: str) -> float:
    """演示用 Judge：基于关键字匹配（真实场景换为 LLM 调用）。"""
    if not prediction:
        return 0.0
    keys = [token for token in reference.split() if len(token) > 1]
    if not keys:
        return 1.0 if prediction.strip() == reference.strip() else 0.0
    hits = sum(1 for key in keys if key in prediction)
    return round(hits / len(keys), 4)


def main() -> None:
    """运行演示批量评估并打印对照报告。"""
    cases = [
        EvalCase(
            task_id="case-001",
            task="1+1 等于多少？",
            reference="答案是 2",
            tags=("math", "easy"),
        ),
        EvalCase(
            task_id="case-002",
            task="中国的首都是哪里？",
            reference="中国的首都是北京",
            tags=("geo", "easy"),
        ),
        EvalCase(
            task_id="case-003",
            task="请回答一个无法处理的问题：raise",
            reference="不应到达此处",
            tags=("error_path",),
        ),
        EvalCase(
            task_id="case-004",
            task="解释 Python 装饰器原理",
            reference="装饰器是高阶函数，接受函数并返回函数",
            tags=("python", "hard"),
        ),
    ]
    annotations = {
        "case-001": 1.0,
        "case-002": 1.0,
        "case-004": 0.4,  # 人工认为 demo 模型回答不充分
    }

    evaluator = BatchEvaluator(model_fn=_demo_model, judge_fn=_demo_judge)
    report = evaluator.run(cases, human_annotations=annotations)
    print(report.render())


if __name__ == "__main__":
    main()
