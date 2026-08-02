"""
L55 示例: LangGraph 基础状态机

学习目标:
- StateGraph 构造与节点注册
- 条件边与路由函数
- 状态注解 (Annotated) 的合并策略
"""

from __future__ import annotations

from typing import Annotated, Literal
from operator import add


# --- 1. 定义状态 ---
class AgentState(dict):
    """LangGraph 状态必须是一个 dict（兼容 TypedDict）。"""

    messages: list[str]
    iteration: int


def agent_node(state: AgentState) -> AgentState:
    """模拟 Agent 处理节点，返回更新后的状态。"""
    return {
        "messages": state["messages"] + [f"[iter {state['iteration']}] agent 处理中"],
        "iteration": state["iteration"] + 1,
    }


def should_continue(state: AgentState) -> Literal["agent", "end"]:
    """路由函数：迭代 < 3 时继续，否则结束。"""
    return "agent" if state["iteration"] < 3 else "end"


# --- 2. 构建图（延迟执行，用于展示结构） ---
def build_graph() -> dict:
    """展示 LangGraph 的构建过程（不实际调用 API）。"""
    # 节点名称列表（模拟 add_node）
    nodes = ["agent"]
    # 入口点
    entry_point = "agent"
    # 条件边映射（模拟 add_conditional_edges）
    conditional_edges = {
        "agent": {
            "agent": should_continue,
            "end": None,
        }
    }
    return {
        "nodes": nodes,
        "entry_point": entry_point,
        "conditional_edges": conditional_edges,
    }


# --- 3. 状态注解演示 ---
class AnnotatedState(dict):
    """Annotated 演示：多节点并发写入同一字段时的合并策略。"""

    buffer: Annotated[list[str], add]  # add = 追加模式
    counter: int  # 默认覆盖模式


def merge_state_demo() -> dict:
    """演示 add 注解的合并行为。"""
    return {
        "node_a_result": {"buffer": ["A wrote this"], "counter": 1},
        "node_b_result": {"buffer": ["B wrote this"], "counter": 2},
        # add 注解会合并 buffer: ["A wrote this", "B wrote this"]
        # 普通字段以后写入的为准: counter=2
    }


# --- 演示运行 ---
if __name__ == "__main__":
    print("=== 1. LangGraph 结构 ===")
    graph_def = build_graph()
    print(f"节点: {graph_def['nodes']}")
    print(f"入口: {graph_def['entry_point']}")
    print(f"条件边: {graph_def['conditional_edges']}")

    print("\n=== 2. 状态注解 ===")
    merged = merge_state_demo()
    print(f"节点A buffer: {merged['node_a_result']['buffer']}")
    print(f"节点B buffer（追加后）: {merged['buffer']}")
    print(f"counter（覆盖）: {merged['counter']}")

    print("\n=== 3. 路由逻辑 ===")
    for i in range(5):
        result = should_continue({"messages": [], "iteration": i})
        print(f"  iteration={i} → {result}")
