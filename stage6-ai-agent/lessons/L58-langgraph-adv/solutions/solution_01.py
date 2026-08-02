"""
练习题 1 参考解答: 构建基础 StateGraph
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal


class CounterState(TypedDict):
    """计数器状态"""

    count: int
    history: list[str]


def increment(state: CounterState) -> CounterState:
    """增加计数器"""
    return {
        "count": state["count"] + 1,
        "history": state["history"] + ["incremented"],
    }


def decrement(state: CounterState) -> CounterState:
    """减少计数器"""
    return {
        "count": state["count"] - 1,
        "history": state["history"] + ["decremented"],
    }


def multiply(state: CounterState) -> CounterState:
    """乘以 2"""
    return {
        "count": state["count"] * 2,
        "history": state["history"] + [f"multiplied by 2 (was {state['count']})"],
    }


def should_multiply_or_end(state: CounterState) -> Literal["multiply", "__end__"]:
    """决定下一步: count < 5 时继续，否则结束"""
    return "multiply" if state["count"] < 5 else "__end__"


def main() -> None:
    """主函数"""
    builder = StateGraph(CounterState)

    # 添加节点
    builder.add_node("increment", increment)
    builder.add_node("multiply", multiply)

    # 添加边
    builder.add_edge(START, "increment")

    # 添加条件边
    builder.add_conditional_edges(
        "increment",
        should_multiply_or_end,
        {
            "multiply": "multiply",
            "__end__": END,
        },
    )

    # multiply 后继续判断
    builder.add_conditional_edges(
        "multiply",
        should_multiply_or_end,
        {
            "multiply": "multiply",
            "__end__": END,
        },
    )

    graph = builder.compile()

    # 执行
    result = graph.invoke(
        {
            "count": 0,
            "history": [],
        }
    )

    print("=" * 50)
    print("执行结果:")
    print("=" * 50)
    print(f"最终 count: {result['count']}")
    print(f"操作历史: {result['history']}")
    print(f"执行步骤数: {len(result['history'])}")

    # 验证
    assert result["count"] >= 5, f"count 应该 >= 5, 实际: {result['count']}"
    print("\n✅ 验证通过!")


if __name__ == "__main__":
    main()
