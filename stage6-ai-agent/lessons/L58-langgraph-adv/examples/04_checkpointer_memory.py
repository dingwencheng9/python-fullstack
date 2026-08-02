"""
示例 4: 检查点与记忆持久化

展示如何使用 MemorySaver 实现多轮对话状态持久化。
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import MemorySaver
from operator import add


class ConversationState(TypedDict):
    """对话状态 - 使用 Annotated 实现消息自动追加"""

    messages: Annotated[list[str], add]  # 消息历史，自动追加


def chat_node(state: ConversationState) -> ConversationState:
    """
    聊天节点

    关键点：
    - messages 是 Annotated 类型，使用 add reducer 自动累积历史
    - 每次调用只需要返回新的 Bot 消息，reducer 会自动追加到历史
    """
    # 获取最后一条用户消息
    user_msg = state["messages"][-1] if state["messages"] else ""

    # 简单的响应规则
    responses = {
        "你好": "你好！有什么可以帮助你的吗？",
        "再见": "再见！祝你有美好的一天！",
    }

    bot_msg = responses.get(user_msg, f"你说了: {user_msg}")

    # 返回新消息，reducer 会自动追加
    return {"messages": [bot_msg]}


def main() -> None:
    """主函数"""
    # 创建内存检查点
    checkpointer = MemorySaver()

    # 构建图
    builder = StateGraph(ConversationState)
    builder.add_node("chat", chat_node)
    builder.add_edge(START, "chat")
    builder.add_edge("chat", END)
    graph = builder.compile(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "user_123"}}

    print("=" * 60)
    print("检查点与记忆测试")
    print("=" * 60)

    # === 第一轮 ===
    print("\n--- 第一轮 ---")
    r1 = graph.invoke(
        {"messages": ["你好"]},  # 用户消息
        config=thread_config,
    )
    print("输入: 你好")
    print(f"Bot: {r1['messages'][-1]}")
    print(f"消息数: {len(r1['messages'])}")

    # === 第二轮 ===
    print("\n--- 第二轮 ---")
    r2 = graph.invoke({"messages": ["Python 是什么？"]}, config=thread_config)
    print("输入: Python 是什么？")
    print(f"Bot: {r2['messages'][-1]}")
    print(f"消息数: {len(r2['messages'])}")

    # === 第三轮 ===
    print("\n--- 第三轮 ---")
    r3 = graph.invoke({"messages": ["再见"]}, config=thread_config)
    print("输入: 再见")
    print(f"Bot: {r3['messages'][-1]}")
    print(f"消息数: {len(r3['messages'])}")

    # 完整历史
    print("\n--- 完整对话历史 ---")
    for i, msg in enumerate(r3["messages"], 1):
        prefix = "用户" if i % 2 == 1 else "Bot"
        print(f"  {i}. [{prefix}] {msg}")

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)

    # 1. 消息累积：Annotated + add reducer 自动合并
    assert len(r3["messages"]) == 6, f"应有 6 条消息，实际 {len(r3['messages'])}"
    print("✅ 消息历史自动累积 (Annotated + add reducer)")

    # 2. 会话隔离
    other_config = {"configurable": {"thread_id": "user_456"}}
    r4 = graph.invoke({"messages": ["你好"]}, config=other_config)
    assert len(r4["messages"]) == 2, "新会话应有 2 条消息"
    print("✅ 不同 thread_id 会话隔离")

    # 3. 恢复测试
    print("\n--- 恢复测试 ---")
    # 在新 thread_id 上恢复之前的会话
    recovered_config = {"configurable": {"thread_id": "user_789"}}
    # 先创建一些历史
    graph.invoke({"messages": ["你好"]}, config=recovered_config)
    graph.invoke({"messages": ["再见"]}, config=recovered_config)
    # 获取当前状态
    recovered_state = graph.get_state({"configurable": {"thread_id": "user_789"}})
    print(f"恢复的消息数: {len(recovered_state.values.get('messages', []))}")
    print("✅ 可从检查点恢复状态")


if __name__ == "__main__":
    main()
