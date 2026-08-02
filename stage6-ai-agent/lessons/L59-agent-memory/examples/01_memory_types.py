"""
L56 示例: 记忆类型与选择

学习目标:
- Buffer Memory / Summary Memory / Vector Memory 的 API 差异
- Token 计数与滑动窗口裁剪
- 层级记忆架构（短期/中期/长期）
"""

from __future__ import annotations


# --- 记忆存储 ---
class InMemoryHistory:
    """简化版对话历史存储（模拟 Buffer Memory）。"""

    def __init__(self, max_messages: int | None = None) -> None:
        self._history: list[str] = []
        self._max = max_messages

    def add(self, role: str, content: str) -> None:
        self._history.append(f"{role}: {content}")
        if self._max and len(self._history) > self._max:
            self._history.pop(0)

    def load(self) -> list[str]:
        return list(self._history)

    def clear(self) -> None:
        self._history.clear()


class SlidingWindowHistory:
    """滑动窗口历史（自动裁剪旧消息）。"""

    def __init__(self, max_messages: int = 20) -> None:
        self._window: list[str] = []
        self._max = max_messages

    def add(self, role: str, content: str) -> None:
        self._window.append(f"{role}: {content}")
        if len(self._window) > self._max:
            self._window.pop(0)

    def load(self) -> list[str]:
        return list(self._window)


class SummarizedHistory:
    """摘要历史（模拟 ConversationSummaryMemory）。"""

    def __init__(self) -> None:
        self._history: list[str] = []
        self._summary: str = ""

    def add(self, role: str, content: str) -> None:
        self._history.append(f"{role}: {content}")
        if len(self._history) > 10:
            # 简化摘要：将最近 3 条压缩为 1 条
            recent = self._history[-3:]
            self._summary = f"[摘要] {' '.join(r.split(': ', 1)[1] for r in recent if ': ' in r)}"
            self._history = self._history[:-3]

    def load(self) -> list[str]:
        result = list(self._history)
        if self._summary:
            result.append(f"system: {self._summary}")
        return result


# --- Token 计数（简化版） ---
def count_tokens(text: str) -> int:
    """简化版 Token 计数（按空格 + 标点分词）。"""
    words = text.split()
    return len(words)


def trim_to_token_limit(messages: list[str], max_tokens: int = 50) -> list[str]:
    """保留消息直到 Token 数不超过限制。"""
    result = []
    total = 0
    for msg in messages:
        tokens = count_tokens(msg)
        if total + tokens <= max_tokens:
            result.append(msg)
            total += tokens
        else:
            break
    return result


# --- 多级记忆 ---
class MultiLevelMemory:
    """层级记忆：每个用户独立存储短期/中期/长期记忆。"""

    def __init__(self) -> None:
        self._short: dict[str, InMemoryHistory] = {}
        self._mid: dict[str, SummarizedHistory] = {}
        self._long: dict[str, list[str]] = {}

    def _short_term(self, user_id: str) -> InMemoryHistory:
        if user_id not in self._short:
            self._short[user_id] = InMemoryHistory(max_messages=10)
        return self._short[user_id]

    def _mid_term(self, user_id: str) -> SummarizedHistory:
        if user_id not in self._mid:
            self._mid[user_id] = SummarizedHistory()
        return self._mid[user_id]

    def save_context(self, user_input: str, agent_output: str, user_id: str = "default") -> None:
        self._short_term(user_id).add("user", user_input)
        self._short_term(user_id).add("assistant", agent_output)
        self._mid_term(user_id).add("user", user_input)
        self._mid_term(user_id).add("assistant", agent_output)
        if len(user_input) > 30:
            self._long.setdefault(user_id, []).append(user_input)

    def load_relevant(self, query: str, user_id: str = "default") -> dict[str, list[str]]:
        short = self._short_term(user_id).load()
        mid = self._mid_term(user_id).load()
        long = self._long.get(user_id, [])
        return {"short": short, "mid": mid, "long": long}


# --- 演示 ---
if __name__ == "__main__":
    print("=== 1. Buffer Memory ===")
    history = InMemoryHistory()
    history.add("user", "我叫小明")
    history.add("assistant", "你好小明！")
    history.add("user", "我最喜欢的颜色是蓝色")
    history.add("assistant", "记住了，你喜欢蓝色")
    print(f"历史: {history.load()}")

    print("\n=== 2. Token 裁剪 ===")
    messages = [f"msg{i}" for i in range(20)]
    trimmed = trim_to_token_limit(messages, max_tokens=6)
    print(f"原始: {len(messages)} 条 → 裁剪后: {len(trimmed)} 条")

    print("\n=== 3. 多级记忆 ===")
    memory = MultiLevelMemory()
    memory.save_context("我叫小明，我喜欢蓝色和编程", "好的小明，已记住", "user-1")
    memory.save_context("我的邮箱是 xiaoming@example.com", "邮箱已记录", "user-1")
    memory.save_context("请总结一下关于我的信息", "总结中...", "user-1")

    relevant = memory.load_relevant("小明的信息", "user-1")
    for level, items in relevant.items():
        print(f"  {level}: {len(items)} 条")
