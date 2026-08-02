"""
L57 示例: 规划模式与推理技术

学习目标:
- Plan-and-Execute 模式的状态机实现
- ReWOO / Reflexion 等自我修正模式
- Chain-of-Thought / Tree-of-Thoughts 推理策略
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


# --- 规划状态 ---
@dataclass
class PlanState:
    input: str
    plan: list[str] = field(default_factory=list)
    past_steps: list[str] = field(default_factory=list)
    result: str = ""


@dataclass
class ReflexionState:
    task: str
    trajectory: list[str] = field(default_factory=list)
    score: int = 0
    reflection: str = ""
    answer: str = ""


# --- Plan-and-Execute ---
def planner_node(state: PlanState) -> PlanState:
    """简化版规划器：按换行拆分用户输入为步骤列表。"""
    lines = [line.strip() for line in state.input.strip().split("\n") if line.strip()]
    steps = []
    for line in lines:
        # 移除常见前缀
        cleaned = line.lstrip("0123456789.-) ")
        if cleaned:
            steps.append(cleaned)
    if not steps:
        steps = [f"处理: {state.input}"]
    return PlanState(input=state.input, plan=steps, past_steps=[], result="")


def executor_node(state: PlanState) -> PlanState:
    """执行当前第一个步骤。"""
    if not state.plan:
        return state
    current = state.plan[0]
    result = f"[执行] {current}"
    return PlanState(
        input=state.input,
        plan=state.plan[1:],
        past_steps=state.past_steps + [result],
        result="",
    )


def should_continue(state: PlanState) -> Literal["execute", "summarize"]:
    return "execute" if state.plan else "summarize"


def summarize_node(state: PlanState) -> PlanState:
    """汇总执行结果。"""
    lines = "\n".join(f"  ✓ {s}" for s in state.past_steps)
    summary = f"任务完成，共 {len(state.past_steps)} 步:\n{lines}"
    return PlanState(input=state.input, plan=[], past_steps=state.past_steps, result=summary)


def run_plan_and_execute(task: str) -> str:
    """完整执行流程。"""
    state = planner_node(PlanState(input=task))
    while True:
        route = should_continue(state)
        if route == "summarize":
            break
        state = executor_node(state)
    return summarize_node(state).result


# --- Reflexion 自我修正 ---
def actor_node(state: ReflexionState) -> ReflexionState:
    """执行任务。"""
    trajectory = state.trajectory + [f"[Actor] 处理: {state.task}"]
    return ReflexionState(
        task=state.task,
        trajectory=trajectory,
        score=state.score,
        reflection=state.reflection,
        answer=state.answer,
    )


def evaluator_node(state: ReflexionState) -> ReflexionState:
    """评估结果（简化：随机评分）。"""
    import random

    score = random.randint(5, 10)  # 简化：模拟评分 5-10
    return ReflexionState(
        task=state.task,
        trajectory=state.trajectory,
        score=score,
        reflection=state.reflection,
        answer=state.answer,
    )


def reflector_node(state: ReflexionState) -> ReflexionState:
    """生成反思。"""
    reflection = f"[Reflector] 评分 {state.score}/10，{'继续改进' if state.score < 8 else '质量可接受'}"
    return ReflexionState(
        task=state.task,
        trajectory=state.trajectory,
        score=state.score,
        reflection=reflection,
        answer=state.answer,
    )


def should_retry(state: ReflexionState) -> Literal["actor", "end"]:
    return "actor" if state.score < 8 and len(state.trajectory) < 3 else "end"


def run_reflexion(task: str) -> dict:
    """完整 Reflexion 流程。"""
    state = ReflexionState(task=task)
    for _ in range(5):
        state = actor_node(state)
        state = evaluator_node(state)
        state = reflector_node(state)
        if should_retry(state) == "end":
            break
    return {"score": state.score, "reflection": state.reflection, "trajectory": state.trajectory}


# --- Chain-of-Thought ---
def chain_of_thought(question: str) -> dict:
    """简化版 Chain-of-Thought：按步骤分析。"""
    steps = []
    # 步骤 1: 理解问题
    steps.append(f"[理解] 问题：{question[:50]}")
    # 步骤 2: 分析要素
    steps.append("[分析] 提取关键要素")
    # 步骤 3: 推导
    steps.append("[推导] 逻辑推理中")
    # 步骤 4: 结论
    answer = f"基于以上分析回答：{question[:20]}..."
    return {"steps": steps, "answer": answer}


# --- Tree-of-Thoughts ---
@dataclass
class ThoughtNode:
    content: str
    score: float
    children: list[ThoughtNode] = field(default_factory=list)


def tree_of_thoughts(question: str, n_branches: int = 3, depth: int = 2) -> list[str]:
    """简化版 Tree-of-Thoughts：生成多条推理路径。"""
    paths = []
    for branch in range(n_branches):
        branch_steps = [f"[分支{branch + 1}] {question}"]
        for d in range(depth):
            branch_steps.append(f"  [深度{d + 1}] 推理步骤 {d + 1}")
        paths.append("\n".join(branch_steps))
    return paths


# --- 演示 ---
if __name__ == "__main__":
    print("=== 1. Plan-and-Execute ===")
    task = "1. 煮水\n2. 下面条\n3. 加调料"
    print(run_plan_and_execute(task))

    print("\n=== 2. Chain-of-Thought ===")
    result = chain_of_thought("小明有3个苹果，小红比他多2个，一共多少个？")
    for step in result["steps"]:
        print(f"  {step}")

    print("\n=== 3. Tree-of-Thoughts ===")
    paths = tree_of_thoughts("如何优化 Python 性能", n_branches=2)
    for path in paths:
        print(f"  {path[:60]}")

    print("\n=== 4. Reflexion ===")
    result = run_reflexion("写一个排序算法")
    print(f"  最终评分: {result['score']}/10")
    print(f"  反思: {result['reflection']}")
    print(f"  轨迹步数: {len(result['trajectory'])}")


# =============================================================================
# 第五章：MCP 协议与工具集成
# =============================================================================
# 参见 examples/02_mcp_server.py     — MCP Server（官方 mcp SDK，stdio 模式）
# 参见 examples/03_langgraph_mcp_integration.py — LangGraph ToolNode + MCP 集成演示
# 参见 exercises/01_mcp_planning_exercise.py   — 练习题
# 参见 solutions/01_mcp_planning_solution.py    — 参考答案

"""
核心架构回顾（Plan-and-Execute + MCP）：

    ┌──────────────────────────────────────────────────────┐
    │  LangGraph StateGraph                                │
    │  ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
    │  │ planner  │───→│ executor │───→│ summarize    │  │
    │  │  (LLM)   │    │ (MCP)    │    │  (LLM)       │  │
    │  └──────────┘    └──────────┘    └──────────────┘  │
    └──────────────────────────────────────────────────────┘
                        │
                        ▼ MCP stdio（JSON-RPC）
                   ┌─────────────┐
                   │ MCP Server  │  ← 02_mcp_server.py
                   │ (文件系统)   │
                   └─────────────┘
"""
