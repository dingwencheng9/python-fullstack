"""
L56 练习: Token 管理策略

练习目标:
- 实现基于 Token 数量的滑动窗口裁剪
- 实现自动摘要触发逻辑
- 支持系统消息保留

TODO 模板 — 请补全函数逻辑。
"""

from __future__ import annotations


# --- Token 计数 ---
def count_tokens(text: str) -> int:
    """简化 Token 计数（按空格分词）。

    TODO: 实现 Token 计数逻辑
    提示：简单实现可以按空格/标点分词，统计词数
    """
    raise NotImplementedError("请实现 count_tokens 函数")


def count_messages_tokens(messages: list[str]) -> int:
    """计算消息列表的总 Token 数。

    TODO: 实现消息列表 Token 计数
    """
    raise NotImplementedError("请实现 count_messages_tokens 函数")


# --- 滑动窗口 ---
def sliding_window_trim(messages: list[str], max_messages: int = 20) -> list[str]:
    """保留最近 N 条消息，自动移除最旧的。

    TODO: 实现滑动窗口裁剪
    提示：直接返回 messages[-max_messages:]
    """
    raise NotImplementedError("请实现 sliding_window_trim 函数")


# --- Token 限制裁剪 ---
def token_budget_trim(messages: list[str], max_tokens: int = 4000) -> list[str]:
    """保留消息直到总 Token 数不超过限制。

    TODO: 实现 Token 预算裁剪
    提示：从后向前保留，当总 Token 数超过限制时停止
    """
    raise NotImplementedError("请实现 token_budget_trim 函数")


# --- 自动摘要（带系统消息保留） ---
def extract_system_message(messages: list[str]) -> tuple[str | None, list[str]]:
    """提取系统消息（如果有）。

    TODO: 识别并分离系统消息
    提示：系统消息通常以 "system: " 开头
    """
    raise NotImplementedError("请实现 extract_system_message 函数")


def auto_summarize(messages: list[str], max_tokens: int = 4000, system_prompt: str | None = None) -> list[str]:
    """自动摘要：Token 超限时将早期消息压缩为摘要，保留系统和最近消息。

    TODO: 实现自动摘要逻辑
    提示：
    1. 提取系统消息
    2. 如果总 Token <= max_tokens，直接返回
    3. 否则将早期消息替换为 "[历史摘要] ..." 字符串
    """
    raise NotImplementedError("请实现 auto_summarize 函数")
