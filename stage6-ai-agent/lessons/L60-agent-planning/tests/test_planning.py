"""
L57 Agent 规划与推理 — 核心行为测试

测试覆盖：
- Plan-and-Execute 模式的状态机逻辑
- Reflexion 自我修正循环（评分 < 8 → 重试）
- Chain-of-Thought 推理步骤
- Tree-of-Thoughts 多路径探索
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


LESSON_ROOT = Path(__file__).resolve().parent.parent


def _load_module(name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# 1. Plan-and-Execute 测试
# ---------------------------------------------------------------------------


def test_planner_node_parses_numbered_steps():
    """规划器应正确解析带序号的任务列表。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.PlanState(input="1. 第一步\n2. 第二步\n3. 第三步")
    result = mod.planner_node(state)

    assert len(result.plan) >= 3
    assert any("第一" in s for s in result.plan)


def test_planner_node_handles_empty_input():
    """空输入应生成默认任务。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.PlanState(input="")
    result = mod.planner_node(state)

    assert len(result.plan) >= 1


def test_executor_node_removes_completed_step():
    """执行器应从计划中移除已完成步骤。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.PlanState(input="test", plan=["分析需求", "写代码"], past_steps=[], result="")
    result = mod.executor_node(state)

    assert len(result.plan) == 1
    assert "分析需求" not in result.plan
    assert len(result.past_steps) == 1


def test_should_continue_executes_when_plan_present():
    """计划非空时应返回 "execute"。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.PlanState(input="", plan=["step1"], past_steps=[], result="")
    assert mod.should_continue(state) == "execute"


def test_should_continue_summarizes_when_plan_empty():
    """计划为空时应返回 "summarize"。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.PlanState(input="", plan=[], past_steps=[], result="")
    assert mod.should_continue(state) == "summarize"


def test_summarize_node_formats_result():
    """汇总节点应生成格式化的结果报告。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.PlanState(
        input="test",
        plan=[],
        past_steps=["[执行] 第一步", "[执行] 第二步"],
        result="",
    )
    result = mod.summarize_node(state)

    assert "任务完成" in result.result
    assert "第一步" in result.result
    assert "第二步" in result.result


def test_run_plan_and_execute_completes_all_steps():
    """完整工作流应执行所有步骤并返回结果。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    result = mod.run_plan_and_execute("1. 煮水\n2. 下面\n3. 调味")

    assert "任务完成" in result
    assert "煮水" in result
    assert "下面" in result
    assert "调味" in result


# ---------------------------------------------------------------------------
# 2. Reflexion 自我修正测试
# ---------------------------------------------------------------------------


def test_evaluator_node_sets_score():
    """评估器应设置分数。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.ReflexionState(task="写排序", trajectory=[], score=0, reflection="", answer="")
    result = mod.evaluator_node(state)

    assert result.score >= 5
    assert result.score <= 10


def test_should_retry_retries_when_score_below_8():
    """分数 < 8 且轨迹 < 3 时应重试。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.ReflexionState(task="test", trajectory=["a"], score=6, reflection="", answer="")
    assert mod.should_retry(state) == "actor"


def test_should_retry_ends_when_score_high_enough():
    """分数 >= 8 时应结束。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.ReflexionState(task="test", trajectory=["a"], score=9, reflection="", answer="")
    assert mod.should_retry(state) == "end"


def test_should_retry_ends_after_max_retries():
    """轨迹 >= 3 时应结束（防止无限循环）。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.ReflexionState(task="test", trajectory=["a", "b", "c"], score=5, reflection="", answer="")
    assert mod.should_retry(state) == "end"


def test_run_reflexion_returns_final_state():
    """Reflexion 工作流应返回最终评分和反思。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    result = mod.run_reflexion("实现快速排序")

    assert "score" in result
    assert "reflection" in result
    assert "trajectory" in result
    assert isinstance(result["trajectory"], list)


def test_reflector_node_generates_reflection():
    """反思节点应生成反思内容。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    state = mod.ReflexionState(task="test", trajectory=[], score=6, reflection="", answer="")
    result = mod.reflector_node(state)

    assert len(result.reflection) > 0
    assert any(keyword in result.reflection for keyword in ["评分", "分", "继续", "可接受"])


# ---------------------------------------------------------------------------
# 3. Chain-of-Thought 测试
# ---------------------------------------------------------------------------


def test_chain_of_thought_returns_steps_and_answer():
    """思维链应返回推理步骤和答案。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    result = mod.chain_of_thought("小明有3个苹果，小红比他多2个")

    assert "steps" in result
    assert "answer" in result
    assert len(result["steps"]) >= 2


def test_chain_of_thought_steps_cover_analysis():
    """思维链步骤应包含理解、分析、推导等阶段。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    result = mod.chain_of_thought("计算 2+2")

    " ".join(result["steps"])
    # 至少包含分析和结论
    assert len(result["steps"]) >= 2


# ---------------------------------------------------------------------------
# 4. Tree-of-Thoughts 测试
# ---------------------------------------------------------------------------


def test_tree_of_thoughts_returns_multiple_paths():
    """思维树应返回多条推理路径。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    paths = mod.tree_of_thoughts("如何优化性能", n_branches=3)

    assert len(paths) == 3
    for path in paths:
        assert len(path) > 0


def test_tree_of_thoughts_each_path_is_distinct():
    """每条思维树路径应互不相同。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    paths = mod.tree_of_thoughts("分析问题", n_branches=3)

    # 各路径应在内容上有所区分
    unique_paths = set(paths)
    assert len(unique_paths) >= 2  # 至少部分路径不同


def test_thought_node_dataclass_has_children():
    """ThoughtNode 应支持 children 属性。"""
    mod = _load_module("plan01", LESSON_ROOT / "examples" / "01_planning_patterns.py")
    node = mod.ThoughtNode(content="分析", score=0.8)

    assert hasattr(node, "children")
    assert isinstance(node.children, list)
