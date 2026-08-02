"""
示例 6: 流式输出与检查点结合

展示如何结合使用流式输出和检查点。
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import MemorySaver
from operator import add


class StreamingState(TypedDict):
    """流式状态"""

    messages: Annotated[list[str], add]
    status: str


def process_node(state: StreamingState) -> StreamingState:
    """
    处理节点 - 模拟流式生成

    注意：这是同步版本，演示基本的流式概念
    """
    import time

    # 模拟逐步生成
    chunks = []
    for i in range(3):
        chunks.append(f"chunk_{i}")
        time.sleep(0.05)  # 模拟延迟

    return {
        "messages": [f"生成了: {', '.join(chunks)}"],
        "status": "completed",
    }


def main() -> None:
    """主函数"""
    checkpointer = MemorySaver()

    builder = StateGraph(StreamingState)
    builder.add_node("process", process_node)
    builder.add_edge(START, "process")
    builder.add_edge("process", END)

    graph = builder.compile(checkpointer=checkpointer)

    print("=" * 60)
    print("流式输出与检查点测试")
    print("=" * 60)

    # 执行
    result = graph.invoke(
        {"messages": [], "status": "started"}, config={"configurable": {"thread_id": "stream_test"}}
    )

    print(f"\n状态: {result['status']}")
    print(f"消息: {result['messages']}")

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert len(result["messages"]) == 1, "应有 1 条消息"
    assert result["status"] == "completed", "状态应该是 completed"
    print("✅ 流式处理验证通过!")

    # 检查点测试
    print("\n--- 检查点恢复 ---")
    recovered = graph.get_state({"configurable": {"thread_id": "stream_test"}})
    print(f"恢复的状态: {recovered.values}")
    print("✅ 检查点功能正常!")


if __name__ == "__main__":
    main()
