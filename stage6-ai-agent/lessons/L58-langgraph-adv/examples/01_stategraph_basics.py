"""
示例 1: LangGraph StateGraph 基础

本示例展示如何创建一个最简单的 LangGraph 应用。
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class AgentState(TypedDict):
    """Agent 的共享状态 - 消息列表和下一步动作"""

    messages: list[str]
    next_action: str | None


def process_node(state: AgentState) -> AgentState:
    """
    处理节点：添加新消息

    Args:
        state: 当前状态

    Returns:
        更新后的状态
    """
    new_message = f"处理步骤 {len(state['messages']) + 1}"
    return {
        "messages": state["messages"] + [new_message],
        "next_action": None,
    }


def should_continue(state: AgentState) -> str:
    """
    决定是否继续执行

    Args:
        state: 当前状态

    Returns:
        "process" 继续处理，或 END 结束
    """
    if len(state["messages"]) < 3:
        return "process"
    return END


def main() -> None:
    """主函数：构建并执行图"""
    # 1. 创建状态图构建器
    builder = StateGraph(AgentState)

    # 2. 添加节点
    builder.add_node("process", process_node)

    # 3. 添加边
    builder.add_edge(START, "process")

    # 4. 添加条件边（循环）
    builder.add_conditional_edges(
        "process",
        should_continue,
        {
            "process": "process",  # 继续循环
            END: END,  # 结束
        },
    )

    # 5. 编译图
    graph = builder.compile()

    # 6. 执行
    result = graph.invoke(
        {
            "messages": [],
            "next_action": None,
        }
    )

    print("=" * 50)
    print("执行结果:")
    print("=" * 50)
    print(f"消息列表: {result['messages']}")
    print(f"共执行 {len(result['messages'])} 步")


if __name__ == "__main__":
    main()
