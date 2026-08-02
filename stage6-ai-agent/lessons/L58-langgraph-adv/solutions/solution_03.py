"""
练习题 3 参考解答: 检查点与记忆系统
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import MemorySaver
from operator import add


class ChatState(TypedDict):
    """聊天状态 - 使用 Annotated 实现消息自动追加"""

    messages: Annotated[list[str], add]


def chat_node(state: ChatState) -> ChatState:
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
        "你叫什么": "我是 AI 助手！",
    }

    bot_msg = responses.get(user_msg, f"你说了: '{user_msg}'")

    # 返回新消息，reducer 会自动追加
    return {"messages": [bot_msg]}


def main() -> None:
    """主函数"""
    # 创建内存检查点
    checkpointer = MemorySaver()

    # 构建图
    builder = StateGraph(ChatState)
    builder.add_node("chat", chat_node)
    builder.add_edge(START, "chat")
    builder.add_edge("chat", END)
    graph = builder.compile(checkpointer=checkpointer)

    print("=" * 60)
    print("多轮对话测试")
    print("=" * 60)

    # 用户 A 进行 3 轮对话
    config_a = {"configurable": {"thread_id": "user_a"}}
    print("\n--- 用户 A 对话 ---")

    r1 = graph.invoke({"messages": ["你好"]}, config=config_a)
    print(f"轮次 1: {r1['messages'][-1]}")
    print(f"  消息数: {len(r1['messages'])}")

    r2 = graph.invoke({"messages": ["你叫什么"]}, config=config_a)
    print(f"轮次 2: {r2['messages'][-1]}")
    print(f"  消息数: {len(r2['messages'])}")

    r3 = graph.invoke({"messages": ["再见"]}, config=config_a)
    print(f"轮次 3: {r3['messages'][-1]}")
    print(f"  消息数: {len(r3['messages'])}")

    # 用户 B 进行 1 轮对话
    config_b = {"configurable": {"thread_id": "user_b"}}
    print("\n--- 用户 B 对话 ---")

    r4 = graph.invoke({"messages": ["你好"]}, config=config_b)
    print(f"轮次 1: {r4['messages'][-1]}")
    print(f"  消息数: {len(r4['messages'])}")

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)

    # 用户 A 应该累积了 3 轮对话（6 条消息）
    assert len(r3["messages"]) == 6, f"用户 A 应该有 6 条消息，实际 {len(r3['messages'])}"
    print("✅ 用户 A 消息累积正确")

    # 用户 B 只有 1 轮对话（2 条消息）
    assert len(r4["messages"]) == 2, f"用户 B 应该有 2 条消息，实际 {len(r4['messages'])}"
    print("✅ 用户 B 消息累积正确")

    print("✅ 多轮对话验证通过!")
    print("✅ 会话隔离验证通过!")

    # 检查点恢复测试
    print("\n--- 检查点恢复测试 ---")
    recovered = graph.get_state({"configurable": {"thread_id": "user_a"}})
    print(f"用户 A 恢复的消息数: {len(recovered.values.get('messages', []))}")
    print("✅ 可从检查点恢复状态")


if __name__ == "__main__":
    main()
