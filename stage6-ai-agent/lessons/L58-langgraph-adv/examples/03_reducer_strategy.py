"""
示例 3: Reducer 策略与状态合并

展示如何使用不同的 Reducer 策略合并节点返回的状态。
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add


def max_reducer(current: int, update: int) -> int:
    """取最大值的 Reducer"""
    return max(current, update)


class ReducerState(TypedDict):
    """
    使用多种 Reducer 策略的状态

    - messages: 使用 add（追加到列表）
    - counter: 使用自定义 max（取最大值）
    - last_update: 无 Reducer（默认覆盖）
    """

    messages: Annotated[list[str], add]  # 追加
    counter: Annotated[int, max_reducer]  # 最大值
    last_update: str  # 覆盖


def node_a(state: ReducerState) -> ReducerState:
    """节点 A：返回部分状态"""
    return {
        "messages": ["消息 A"],
        "counter": 10,
        "last_update": "A",
    }


def node_b(state: ReducerState) -> ReducerState:
    """节点 B：返回部分状态"""
    return {
        "messages": ["消息 B"],
        "counter": 20,
        "last_update": "B",
    }


def node_c(state: ReducerState) -> ReducerState:
    """节点 C：返回部分状态"""
    return {
        "messages": ["消息 C"],
        "counter": 15,
        "last_update": "C",
    }


def main() -> None:
    """主函数"""
    # 构建图：顺序执行三个节点
    builder = StateGraph(ReducerState)

    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)

    # START -> a -> b -> c -> END (顺序执行)
    builder.add_edge(START, "a")
    builder.add_edge("a", "b")
    builder.add_edge("b", "c")
    builder.add_edge("c", END)

    graph = builder.compile()

    # 执行
    initial_state: ReducerState = {
        "messages": ["初始消息"],
        "counter": 5,
        "last_update": "initial",
    }

    result = graph.invoke(initial_state)

    print("=" * 60)
    print("Reducer 测试结果")
    print("=" * 60)
    print(f"\nmessages (追加): {result['messages']}")
    print("  预期: ['初始消息', '消息 A', '消息 B', '消息 C']")

    print(f"\ncounter (最大值): {result['counter']}")
    print("  预期: 20 (max(5, 10, 20, 15))")

    print(f"\nlast_update (覆盖): {result['last_update']}")
    print("  预期: 'C' (最后执行的节点)")

    # 验证结果
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert len(result["messages"]) == 4, "messages 应该包含 4 条"
    assert result["counter"] == 20, f"counter 应该是 20, 实际: {result['counter']}"
    assert result["last_update"] == "C", f"last_update 应该是 'C', 实际: {result['last_update']}"
    print("✅ 所有验证通过!")


if __name__ == "__main__":
    main()
