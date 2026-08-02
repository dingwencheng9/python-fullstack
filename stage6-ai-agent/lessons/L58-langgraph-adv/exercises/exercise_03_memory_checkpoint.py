"""
练习题 3: 检查点与记忆系统

请实现一个支持多轮对话的聊天机器人，使用检查点持久化状态：

1. 定义 ChatState:
   - messages: list[str] (对话历史)
   - turn: int (对话轮数)

2. 实现 chat_node:
   - 接收用户最后一条消息
   - 生成简单的机器人回复
   - 记录到 messages 历史
   - turn 加 1

3. 使用 MemorySaver 实现检查点:
   - 使用 thread_id 隔离不同用户会话
   - 支持多轮对话状态累积

4. 实现功能:
   - 对话历史自动累积
   - 不同 thread_id 的对话互不影响
   - 可以从指定检查点恢复

5. 测试场景:
   - 用户 A 进行 3 轮对话
   - 用户 B 进行 1 轮对话
   - 验证两者的对话历史独立
"""

from typing import TypedDict


class ChatState(TypedDict):
    """聊天状态"""

    messages: list[str]
    turn: int


def chat_node(state: ChatState) -> ChatState:
    """
    聊天节点：处理用户输入并生成回复

    Args:
        state: 当前状态

    Returns:
        更新后的状态
    """
    # TODO: 实现聊天逻辑
    # 1. 获取最后一条用户消息
    # 2. 生成简单回复（可以使用规则或模拟）
    # 3. 更新 messages 和 turn
    pass


def main() -> None:
    """主函数"""
    # TODO: 创建 MemorySaver 检查点
    pass

    # TODO: 构建图并编译
    pass

    # TODO: 测试多轮对话
    # 1. 用户 A 对话 3 轮
    # 2. 用户 B 对话 1 轮
    # 3. 验证状态隔离
    pass


if __name__ == "__main__":
    main()
