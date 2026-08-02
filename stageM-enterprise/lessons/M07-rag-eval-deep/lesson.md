# M07: RAG 评估深度

> **课程编号**: M07
> **所属阶段**: Stage M - 企业级 AI 应用
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐ (中高级)
> **前置课程**: M02 (LlamaIndex 高级 RAG)、M05 (向量库深入)
> **状态**: 🟡 完善中
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **评估体系**：构建完整的 RAG 系统评估框架
2. **指标定义**：理解并实现 RAGAs、Trulens 等评估标准
3. **自动化测试**：实现持续评估和回归测试
4. **优化迭代**：基于评估结果优化 RAG 系统

---

## 📚 课程内容

### 第一部分：RAG 评估概述

#### 1.1 为什么需要评估 RAG

```
RAG 系统评估的重要性：

1. 多组件复杂系统
   - 检索组件：向量匹配、关键词匹配
   - 生成组件：LLM 理解、答案生成
   - 编排组件：流程控制、上下文构建

2. 质量维度多样
   - 准确性（是否正确回答）
   - 相关性（是否相关回答）
   - 完整性（是否回答完整）
   - 安全性（是否有害内容）

3. 难以人工评估
   - 成本高
   - 一致性差
   - 扩展性差
```

#### 1.2 评估维度

```
┌─────────────────────────────────────────────────────────┐
│                  RAG 评估维度                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  上下文相关  │    │   答案相关   │    │   答案忠实   │ │
│  │ (Context    │    │ (Answer     │    │ (Faithful-  │ │
│  │  Relevance) │    │  Relevance) │    │   ness)     │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│         ↓                 ↓                 ↓           │
│  上下文是否包含         答案是否         答案是否       │
│  回答问题所需信息       针对问题         忠实于上下文   │
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   答案正确   │    │   答案流利   │    │   毒性检测   │ │
│  │ (Correctness│    │ (Fluency)   │    │  (Toxicity) │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│         ↓                 ↓                 ↓           │
│  答案与真实           答案是否         答案是否         │
│  答案的匹配度         语法正确         包含有害内容     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### 1.3 评估框架对比

| 框架 | 特点 | 适用场景 | 评估方式 |
|------|------|----------|----------|
| **RAGAs** | 简单、主流 | 快速评估 | LLM 作为评判 |
| **Trulens** | 全面、可视化 | 生产监控 | 多种指标组合 |
| **ARES** | 自动化、统计 | 大规模评估 | 少样本学习 |
| **G-eval** | 灵活、可定制 | 研究场景 | Chain-of-Thought |

---

### 第二部分：RAGAs 评估框架

#### 2.1 RAGAs 核心指标

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class MetricType(Enum):
    """RAGAs 指标类型"""
    # 检索指标
    CONTEXT_PRECISION = "context_precision"
    CONTEXT_RECALL = "context_recall"
    CONTEXT_RELEVANCE = "context_relevance"

    # 生成指标
    ANSWER_RELEVANCE = "answer_relevance"
    FAITHFULNESS = "faithfulness"
    ANSWER_CORRECTNESS = "answer_correctness"

@dataclass
class RAGAsMetrics:
    """RAGAs 评估指标"""
    # 检索指标
    context_precision: float      # 上下文精确度
    context_recall: float         # 上下文召回率
    context_relevance: float      # 上下文相关性

    # 生成指标
    answer_relevance: float       # 答案相关性
    faithfulness: float           # 答案忠实度
    answer_correctness: float     # 答案正确性

    def overall_score(self) -> float:
        """综合得分"""
        return (
            self.context_precision * 0.15 +
            self.context_recall * 0.15 +
            self.context_relevance * 0.15 +
            self.answer_relevance * 0.2 +
            self.faithfulness * 0.2 +
            self.answer_correctness * 0.15
        )
```

#### 2.2 指标计算实现

```python
from typing import List, Dict, Any
import asyncio

class RAGAsEvaluator:
    """RAGAs 评估器实现"""

    def __init__(self, llm):
        self.llm = llm

    async def evaluate_context_relevance(
        self,
        question: str,
        contexts: List[str]
    ) -> float:
        """
        评估上下文相关性

        计算公式：相关句子数 / 总句子数
        """
        prompt = f"""You are a helpful assistant. Your task is to evaluate the context relevance.

Consider the following question and context. Determine which sentences in the context
are relevant to answering the question. Output a JSON with:
- "relevant_sentences": list of relevant sentence indices
- "total_sentences": total number of sentences
- "reasoning": explanation

Question: {question}

Context:
{chr(10).join([f"[{i}] {ctx}" for i, ctx in enumerate(contexts)])}

Output JSON:"""

        response = await self.llm.acomplete(prompt)
        import json
        result = json.loads(str(response))

        relevance = len(result["relevant_sentences"]) / result["total_sentences"]
        return min(1.0, relevance)

    async def evaluate_faithfulness(
        self,
        question: str,
        contexts: List[str],
        answer: str
    ) -> float:
        """
        评估答案忠实度

        计算公式：答案中由上下文支持的主张数 / 答案总主张数
        """
        prompt = f"""You are a helpful assistant. Your task is to evaluate answer faithfulness.

Given a question, context, and answer, determine how faithful the answer is to the context.
Identify all claims in the answer and check if each claim is supported by the context.

Question: {question}

Context:
{chr(10).join([f"[{i}] {ctx}" for i, ctx in enumerate(contexts)])}

Answer: {answer}

Output JSON with:
- "claims": list of claims in the answer
- "supported_claims": list of supported claim indices
- "faithfulness_score": supported / total
- "reasoning": explanation

Output JSON:"""

        response = await self.llm.acomplete(prompt)
        import json
        result = json.loads(str(response))

        total_claims = len(result["claims"])
        supported_claims = len(result["supported_claims"])

        if total_claims == 0:
            return 1.0  # 无主张默认为忠实

        return supported_claims / total_claims

    async def evaluate_answer_relevance(
        self,
        question: str,
        answer: str
    ) -> float:
        """
        评估答案相关性

        方法：生成多个反向问题，计算与原问题的相似度
        """
        # 生成反向问题
        prompt = f"""Generate 3 different variations of the following question that
capture the same intent but use different wording. Output as JSON list.

Original question: {question}

Output: ["question1", "question2", "question3"]"""

        response = await self.llm.acomplete(prompt)
        import json
        variations = json.loads(str(response))

        # 计算相似度
        from .embedder import EmbeddingGenerator
        embedder = EmbeddingGenerator()

        question_vec = embedder.encode([question])[0]
        variation_vecs = embedder.encode(variations)

        similarities = [
            embedder.similarity(question, v)
            for v in variations
        ]

        return sum(similarities) / len(similarities)

    async def evaluate_context_precision(
        self,
        contexts: List[str],
        ground_truth_contexts: List[str]
    ) -> float:
        """
        评估上下文精确度

        计算公式：相关上下文数 / 总上下文数
        """
        # 使用 LLM 判断每个上下文是否与真实上下文相关
        scores = []

        for ctx in contexts:
            is_relevant = await self._is_context_relevant(ctx, ground_truth_contexts)
            scores.append(1.0 if is_relevant else 0.0)

        return sum(scores) / len(scores) if scores else 0.0

    async def _is_context_relevant(
        self,
        context: str,
        ground_truth: List[str]
    ) -> bool:
        """判断上下文是否相关"""
        prompt = f"""Is the following context relevant to the ground truth contexts?

Context: {context}

Ground Truth:
{chr(10).join([f"- {gt}" for gt in ground_truth])}

Answer: yes or no"""

        response = await self.llm.acomplete(prompt)
        return "yes" in str(response).lower()
```

#### 2.3 完整评估流程

```python
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime

@dataclass
class EvaluationResult:
    """评估结果"""
    question: str
    ground_truth_answer: str
    predicted_answer: str
    contexts: List[str]
    metrics: RAGAsMetrics
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "ground_truth_answer": self.ground_truth_answer,
            "predicted_answer": self.predicted_answer,
            "context_precision": self.metrics.context_precision,
            "context_recall": self.metrics.context_recall,
            "context_relevance": self.metrics.context_relevance,
            "answer_relevance": self.metrics.answer_relevance,
            "faithfulness": self.metrics.faithfulness,
            "answer_correctness": self.metrics.answer_correctness,
            "overall_score": self.metrics.overall_score(),
            "timestamp": self.timestamp.isoformat()
        }

class RAGEvaluator:
    """RAG 完整评估器"""

    def __init__(self, llm, embedder):
        self.llm = llm
        self.ragas = RAGAsEvaluator(llm)
        self.embedder = embedder

    async def evaluate_single(
        self,
        question: str,
        predicted_answer: str,
        contexts: List[str],
        ground_truth_answer: Optional[str] = None,
        ground_truth_contexts: Optional[List[str]] = None
    ) -> EvaluationResult:
        """评估单个样本"""
        # 计算各项指标
        context_relevance = await self.ragas.evaluate_context_relevance(
            question, contexts
        )

        faithfulness = await self.ragas.evaluate_faithfulness(
            question, contexts, predicted_answer
        )

        answer_relevance = await self.ragas.evaluate_answer_relevance(
            question, predicted_answer
        )

        # 上下文精确度和召回率（如果有 ground truth）
        context_precision = 0.0
        context_recall = 0.0

        if ground_truth_contexts:
            context_precision = await self.ragas.evaluate_context_precision(
                contexts, ground_truth_contexts
            )
            context_recall = await self.ragas.evaluate_context_precision(
                ground_truth_contexts, contexts
            )

        # 答案正确性（如果有 ground truth）
        answer_correctness = 0.0
        if ground_truth_answer:
            answer_correctness = await self._evaluate_answer_correctness(
                predicted_answer, ground_truth_answer
            )

        metrics = RAGAsMetrics(
            context_precision=context_precision,
            context_recall=context_recall,
            context_relevance=context_relevance,
            answer_relevance=answer_relevance,
            faithfulness=faithfulness,
            answer_correctness=answer_correctness
        )

        return EvaluationResult(
            question=question,
            ground_truth_answer=ground_truth_answer or "",
            predicted_answer=predicted_answer,
            contexts=contexts,
            metrics=metrics
        )

    async def evaluate_batch(
        self,
        test_cases: List[Dict[str, Any]],
        show_progress: bool = True
    ) -> List[EvaluationResult]:
        """批量评估"""
        results = []

        for i, case in enumerate(test_cases):
            if show_progress:
                print(f"Evaluating {i+1}/{len(test_cases)}...")

            result = await self.evaluate_single(
                question=case["question"],
                predicted_answer=case["predicted_answer"],
                contexts=case["contexts"],
                ground_truth_answer=case.get("ground_truth_answer"),
                ground_truth_contexts=case.get("ground_truth_contexts")
            )
            results.append(result)

        return results

    async def _evaluate_answer_correctness(
        self,
        predicted: str,
        ground_truth: str
    ) -> float:
        """评估答案正确性（使用 embedding 相似度）"""
        pred_vec = self.embedder.encode([predicted])[0]
        gt_vec = self.embedder.encode([ground_truth])[0]

        similarity = self.embedder.similarity(predicted, ground_truth)
        return similarity
```

---

### 第三部分：Trulens 评估

#### 3.1 Trulens 核心组件

```python
# Trulens 评估框架
from trulens.core import Feedback
from trulens.feedback import Groundedness, Relevance
from trulens.providers.litellm import LiteLLM

class TrulensEvaluator:
    """Trulens 评估器"""

    def __init__(self, llm):
        self.llm = llm
        self.provider = LiteLLM(model="gpt-4")

    def setup_feedback(self) -> list[Feedback]:
        """设置反馈函数"""
        # 接地性评估
        groundedness = Feedback(
            self.provider.groundedness_measure,
            name="Groundedness"
        ).on(
            context=self._select_context,
            response=self._select_response
        )

        # 答案相关性
        answer_relevance = Feedback(
            self.provider.relevance,
            name="Answer Relevance"
        ).on(
            prompt=self._select_prompt,
            response=self._select_response
        )

        # 上下文相关性
        context_relevance = Feedback(
            self.provider.relevance,
            name="Context Relevance"
        ).on(
            prompt=self._select_prompt,
            context=self._select_context
        ).aggregate(self._mean)

        return [groundedness, answer_relevance, context_relevance]

    def _select_context(self, record) -> str:
        """选择上下文"""
        return "\n".join([
            ctx.get("text", "")
            for ctx in record.main_output.get("contexts", [])
        ])

    def _select_response(self, record) -> str:
        """选择响应"""
        return record.main_output.get("response", "")

    def _select_prompt(self, record) -> str:
        """选择提示"""
        return record.main_input

    def _mean(self, scores: list[float]) -> float:
        """计算平均值"""
        return sum(scores) / len(scores) if scores else 0.0
```

#### 3.2 与 RAG 集成

```python
from trulens.apps.langchain import LangChainInstrument
from trulens.core import TruSession
from trulens.apps.custom import instrument

class TrulensRAGEvaluator:
    """Trulens RAG 评估"""

    def __init__(self, rag_pipeline, llm):
        self.rag = rag_pipeline
        self.llm = llm
        self.tru = TruSession()

    @instrument
    def retrieve(self, query: str) -> list:
        """检索方法（被 Trulens 追踪）"""
        return self.rag.retrieve(query)

    @instrument
    def generate(self, query: str, context: str) -> str:
        """生成方法（被 Trulens 追踪）"""
        return self.rag.generate(query, context)

    def run_evaluation(self, test_queries: list[str]) -> dict:
        """运行评估"""
        results = []

        for query in test_queries:
            # 使用 Trulens 追踪执行
            with self.tru as recording:
                context = self.retrieve(query)
                response = self.generate(query, context)

            # 获取评估结果
            record = self.tru.get_record(query)
            results.append({
                "query": query,
                "response": response,
                "metrics": record.feedback_results
            })

        return results
```

---

### 第四部分：评估数据集

#### 4.1 测试集构建

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class TestCase:
    """测试用例"""
    question: str
    ground_truth_answer: str
    ground_truth_contexts: List[str] = field(default_factory=list)
    metadata: Dict[str, any] = field(default_factory=dict)

class TestDatasetBuilder:
    """测试数据集构建器"""

    def __init__(self, llm):
        self.llm = llm

    async def generate_synthetic(
        self,
        documents: List[dict],
        num_questions_per_doc: int = 5
    ) -> List[TestCase]:
        """从文档生成合成测试集"""
        test_cases = []

        for doc in documents:
            prompt = f"""Based on the following document, generate {num_questions_per_doc}
diverse questions and their answers.

Document: {doc['content']}

Output JSON format:
{{
    "questions": [
        {{
            "question": "question text",
            "ground_truth_answer": "answer text",
            "difficulty": "easy/medium/hard",
            "type": "factual/analytical/summary"
        }}
    ]
}}"""

            response = await self.llm.acomplete(prompt)
            import json
            result = json.loads(str(response))

            for qa in result["questions"]:
                test_cases.append(TestCase(
                    question=qa["question"],
                    ground_truth_answer=qa["ground_truth_answer"],
                    ground_truth_contexts=[doc["content"]],
                    metadata={
                        "source": doc.get("title", "unknown"),
                        "difficulty": qa["difficulty"],
                        "type": qa["type"]
                    }
                ))

        return test_cases

    async def generate_adversarial(
        self,
        documents: List[dict]
    ) -> List[TestCase]:
        """生成对抗性测试用例"""
        test_cases = []

        prompt = """Generate adversarial test cases that challenge a RAG system.
Consider these types of challenges:
1. Ambiguous questions
2. Questions requiring multi-hop reasoning
3. Questions outside the document scope
4. Questions with partial context

Documents:
{chr(10).join([f"- {doc['title']}: {doc['content'][:500]}" for doc in documents[:5]])}

Output JSON:
{{
    "adversarial_cases": [
        {{
            "question": "...",
            "expected_challenge": "...",
            "ground_truth_answer": "..." or "unanswerable"
        }}
    ]
}}"""

        response = await self.llm.acomplete(prompt)
        import json
        result = json.loads(str(response))

        for case in result["adversarial_cases"]:
            test_cases.append(TestCase(
                question=case["question"],
                ground_truth_answer=case["ground_truth_answer"],
                metadata={
                    "challenge_type": case["expected_challenge"],
                    "is_adversarial": True
                }
            ))

        return test_cases
```

#### 4.2 公开数据集

| 数据集 | 来源 | 规模 | 特点 |
|--------|------|------|------|
| **HotpotQA** | DeepMind | 113k | 多跳问答 |
| **Natural Questions** | Google | 323k | 真实用户问题 |
| **MS MARCO** | Microsoft | 1M | 搜索引擎点击 |
| **TriviaQA** | UW NLP | 95k | 知识问答 |
| **PopQA** | ASU NLP | 15k | 长尾实体 |

---

### 第五部分：持续评估

#### 5.1 CI/CD 集成

```yaml
# .github/workflows/rag-eval.yml
name: RAG Evaluation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          pip install uv
          uv sync

      - name: Run evaluation
        run: |
          uv run python scripts/evaluate.py \
            --test-set data/eval/test_set.json \
            --output results/eval_results.json

      - name: Check threshold
        run: |
          uv run python scripts/check_threshold.py \
            --results results/eval_results.json \
            --threshold 0.75

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: eval-results
          path: results/

  regression-check:
    needs: evaluate
    runs-on: ubuntu-latest
    steps:
      - name: Compare with baseline
        run: |
          uv run python scripts/regression_check.py \
            --current results/eval_results.json \
            --baseline data/eval/baseline.json
```

#### 5.2 监控仪表板

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd

@dataclass
class MonitoringSnapshot:
    """监控快照"""
    timestamp: datetime
    metrics: Dict[str, float]
    num_requests: int
    avg_latency: float
    error_rate: float

class EvaluationMonitor:
    """评估监控系统"""

    def __init__(self, db_path: str = "eval_monitor.db"):
        self.db_path = db_path
        self.snapshots: List[MonitoringSnapshot] = []

    def record_snapshot(
        self,
        metrics: RAGAsMetrics,
        num_requests: int,
        latency: float,
        errors: int
    ) -> None:
        """记录监控快照"""
        snapshot = MonitoringSnapshot(
            timestamp=datetime.now(),
            metrics={
                "context_precision": metrics.context_precision,
                "context_recall": metrics.context_recall,
                "answer_relevance": metrics.answer_relevance,
                "faithfulness": metrics.faithfulness,
                "overall": metrics.overall_score()
            },
            num_requests=num_requests,
            avg_latency=latency,
            error_rate=errors / num_requests if num_requests > 0 else 0
        )
        self.snapshots.append(snapshot)

        # 持久化
        self._persist(snapshot)

    def get_trend(
        self,
        metric_name: str,
        days: int = 7
    ) -> pd.DataFrame:
        """获取指标趋势"""
        cutoff = datetime.now() - timedelta(days=days)
        relevant = [
            s for s in self.snapshots
            if s.timestamp >= cutoff
        ]

        return pd.DataFrame([
            {
                "timestamp": s.timestamp,
                "value": s.metrics.get(metric_name, 0)
            }
            for s in relevant
        ])

    def check_anomalies(
        self,
        metric_name: str,
        threshold: float = 0.05
    ) -> List[Dict]:
        """检测异常"""
        if len(self.snapshots) < 2:
            return []

        # 计算滚动平均
        recent = self.snapshots[-10:]
        avg = sum(
            s.metrics.get(metric_name, 0) for s in recent
        ) / len(recent)

        # 检测下降
        current = self.snapshots[-1]
        current_val = current.metrics.get(metric_name, 0)

        if avg - current_val > threshold:
            return [{
                "metric": metric_name,
                "current": current_val,
                "average": avg,
                "drop": avg - current_val,
                "timestamp": current.timestamp.isoformat()
            }]

        return []

    def _persist(self, snapshot: MonitoringSnapshot) -> None:
        """持久化到数据库"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO snapshots (timestamp, metrics, num_requests, avg_latency, error_rate)
            VALUES (?, ?, ?, ?, ?)
        """, (
            snapshot.timestamp.isoformat(),
            str(snapshot.metrics),
            snapshot.num_requests,
            snapshot.avg_latency,
            snapshot.error_rate
        ))

        conn.commit()
        conn.close()
```

---

## 🚀 实战案例

### 案例：RAG 系统评估平台

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import json

@dataclass
class EvalConfig:
    """评估配置"""
    rag_pipeline: any
    test_dataset_path: str
    output_path: str
    thresholds: dict

class EvalPlatform:
    """RAG 评估平台"""

    def __init__(self, config: EvalConfig):
        self.config = config
        self.rag = config.rag_pipeline

    async def run_full_evaluation(self) -> dict:
        """运行完整评估"""
        # 1. 加载测试集
        test_cases = self._load_test_cases()

        # 2. 执行 RAG 并收集结果
        predictions = []
        for case in test_cases:
            result = await self.rag.query(case["question"])
            predictions.append({
                **case,
                "predicted_answer": result["answer"],
                "contexts": [s["content"] for s in result["sources"]]
            })

        # 3. 评估
        evaluator = RAGEvaluator(self.rag.llm, self.rag.embedder)
        results = await evaluator.evaluate_batch(predictions)

        # 4. 汇总
        summary = self._summarize_results(results)

        # 5. 检查阈值
        passed = self._check_thresholds(summary)

        # 6. 生成报告
        report = self._generate_report(results, summary, passed)

        # 7. 保存
        self._save_report(report)

        return {
            "summary": summary,
            "passed": passed,
            "report": report
        }

    def _load_test_cases(self) -> List[dict]:
        """加载测试用例"""
        with open(self.config.test_dataset_path) as f:
            return json.load(f)

    def _summarize_results(self, results: List[EvaluationResult]) -> dict:
        """汇总结果"""
        metrics = {
            "context_precision": [],
            "context_recall": [],
            "context_relevance": [],
            "answer_relevance": [],
            "faithfulness": [],
            "answer_correctness": [],
            "overall": []
        }

        for r in results:
            metrics["context_precision"].append(r.metrics.context_precision)
            metrics["context_recall"].append(r.metrics.context_recall)
            metrics["context_relevance"].append(r.metrics.context_relevance)
            metrics["answer_relevance"].append(r.metrics.answer_relevance)
            metrics["faithfulness"].append(r.metrics.faithfulness)
            metrics["answer_correctness"].append(r.metrics.answer_correctness)
            metrics["overall"].append(r.metrics.overall_score())

        summary = {
            metric: {
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "std": self._std(values)
            }
            for metric, values in metrics.items()
        }

        summary["total_samples"] = len(results)
        return summary

    def _std(self, values: List[float]) -> float:
        """计算标准差"""
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5

    def _check_thresholds(self, summary: dict) -> bool:
        """检查阈值"""
        passed = True
        for metric, threshold in self.config.thresholds.items():
            if metric in summary:
                actual = summary[metric]["mean"]
                if actual < threshold:
                    passed = False
                    print(f"❌ {metric}: {actual:.3f} < {threshold}")
                else:
                    print(f"✅ {metric}: {actual:.3f} >= {threshold}")
        return passed

    def _generate_report(
        self,
        results: List[EvaluationResult],
        summary: dict,
        passed: bool
    ) -> dict:
        """生成报告"""
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "passed" if passed else "failed",
            "summary": summary,
            "thresholds": self.config.thresholds,
            "sample_results": [r.to_dict() for r in results[:10]]
        }

    def _save_report(self, report: dict) -> None:
        """保存报告"""
        with open(self.config.output_path, "w") as f:
            json.dump(report, f, indent=2)
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解 RAG 评估的各个维度
- [ ] 实现 RAGAs 评估指标
- [ ] 使用 Trulens 进行系统评估
- [ ] 构建评估测试数据集
- [ ] 集成评估到 CI/CD 流程
- [ ] 建立持续监控和告警系统

---

## 🔗 相关资源

- [RAGAs GitHub](https://github.com/explodinggradients/ragas)
- [Trulens GitHub](https://github.com/truera/trulens)
- [RAG 评估论文](https://arxiv.org/abs/2310.15216)

---

## 🔗 下一步

完成本课程后，你可以：

- 完成 M08: AI 产品发布与运营
- 进入 Stage R: 前沿探索实验室
- 开始最终项目实战

---

**最后更新**: 2026-07-18
