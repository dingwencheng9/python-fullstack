"""
L56 练习参考答案: Token 管理策略

参考实现：
- Token 计数（按空格分词）
- 滑动窗口裁剪（保留最近 N 条）
- Token 预算裁剪（从后向前）
- 自动摘要（含系统消息保留）
"""

from __future__ import annotations

import re


def count_tokens(text: str) -> int:
    """按空格/标点分词。"""
    words = re.findall(r"\b\w+\b", text)
    return len(words)


def count_messages_tokens(messages: list[str]) -> int:
    """计算消息列表的总 Token 数。"""
    return sum(count_tokens(msg) for msg in messages)


def sliding_window_trim(messages: list[str], max_messages: int = 20) -> list[str]:
    """保留最近 N 条消息。"""
    return list(messages[-max_messages:]) if messages else []


def token_budget_trim(messages: list[str], max_tokens: int = 4000) -> list[str]:
    """从后向前保留消息，直到总 Token 数不超过限制。"""
    result = []
    total = 0
    for msg in reversed(messages):
        msg_tokens = count_tokens(msg)
        if total + msg_tokens <= max_tokens:
            result.insert(0, msg)
            total += msg_tokens
        else:
            break
    return result


def extract_system_message(messages: list[str]) -> tuple[str | None, list[str]]:
    """提取并分离系统消息。"""
    non_system = []
    system = None
    for msg in messages:
        if msg.lower().startswith("system:"):
            system = msg
        else:
            non_system.append(msg)
    return system, non_system


def auto_summarize(messages: list[str], max_tokens: int = 4000, system_prompt: str | None = None) -> list[str]:
    """自动摘要：Token 超限时压缩早期消息为摘要。"""
    # 分离系统消息
    system_msg, non_system = extract_system_message(messages)
    effective_system = system_prompt or system_msg

    # 如果总 Token 不超限，直接返回
    total = count_messages_tokens(messages)
    if total <= max_tokens:
        return list(messages)

    # 将早期消息压缩为摘要
    summary_text = f"[历史摘要] {count_messages_tokens(non_system[:-5])} 轮对话已省略"
    result = [summary_text] + non_system[-5:]

    # 加上系统消息（如果有）
    if effective_system:
        result = [effective_system] + result

    return result


if __name__ == "__main__":
    # 测试
    messages = [f"user: message {i} with some content" for i in range(20)]
    print(f"原始: {count_messages_tokens(messages)} tokens, {len(messages)} 条")

    trimmed = sliding_window_trim(messages, 10)
    print(f"滑动窗口(10): {len(trimmed)} 条")

    token_trimmed = token_budget_trim(messages, max_tokens=50)
    print(f"Token限制(50): {count_messages_tokens(token_trimmed)} tokens, {len(token_trimmed)} 条")

    summarized = auto_summarize(messages, max_tokens=30)
    print(f"自动摘要: {count_messages_tokens(summarized)} tokens, {len(summarized)} 条")
    for m in summarized:
        print(f"  {m[:60]}")
