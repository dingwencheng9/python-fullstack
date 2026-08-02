"""
L56 示例: 状态检查点与记忆恢复

学习目标:
- MemorySaver 与 PostgreSQL Checkpointer API 模拟
- 带 thread_id 的多会话状态隔离
- 滑动窗口注解（Annotated + 自定义合并）
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated


# --- 检查点存储 ---
@dataclass
class ThreadCheckpoint:
    """简化版检查点。"""

    thread_id: str
    step: int
    values: dict
    next_node: str | None = None


class MemoryCheckpointer:
    """简化版 MemoryCheckpointer。"""

    def __init__(self) -> None:
        self._store: dict[str, list[ThreadCheckpoint]] = {}

    def put(self, thread_id: str, checkpoint: ThreadCheckpoint) -> None:
        self._store.setdefault(thread_id, []).append(checkpoint)

    def get(self, thread_id: str) -> ThreadCheckpoint | None:
        history = self._store.get(thread_id, [])
        return history[-1] if history else None

    def get_history(self, thread_id: str) -> list[ThreadCheckpoint]:
        return list(self._store.get(thread_id, []))


# --- 带滑动窗口的状态更新 ---
def merge_with_sliding_window(left: list[str], right: list[str], max_messages: int = 20) -> list[str]:
    """滑动窗口合并：追加新消息，超出上限时移除最旧的。"""
    combined = left + right
    return combined[-max_messages:]


@dataclass
class ChatState(dict):
    """带滑动窗口的对话状态。"""

    messages: Annotated[list[str], merge_with_sliding_window]
    thread_id: str


# --- 演示：多会话记忆隔离 ---
def simulate_multi_session_memory() -> dict:
    """模拟两个用户会话的完全隔离。"""
    checker = MemoryCheckpointer()

    # 会话 1: user-1
    for i in range(3):
        checker.put(
            "user-1",
            ThreadCheckpoint(
                thread_id="user-1",
                step=i,
                values={"messages": [f"[user-1] msg {i}"], "user": "小明"},
            ),
        )

    # 会话 2: user-2
    checker.put(
        "user-2",
        ThreadCheckpoint(
            thread_id="user-2",
            step=0,
            values={"messages": ["[user-2] 你好，我是小红"], "user": "小红"},
        ),
    )

    u1_latest = checker.get("user-1")
    u2_latest = checker.get("user-2")

    return {
        "user-1_latest": u1_latest.values.get("user", "未知"),
        "user-2_latest": u2_latest.values.get("user", "未知"),
        "user-1_history_len": len(checker.get_history("user-1")),
        "sessions_isolated": u1_latest.values["user"] != u2_latest.values["user"],
    }


# --- 演示运行 ---
if __name__ == "__main__":
    print("=== 1. 多会话记忆隔离 ===")
    result = simulate_multi_session_memory()
    print(f"  user-1 最新消息: {result['user-1_latest']}")
    print(f"  user-2 最新消息: {result['user-2_latest']}")
    print(f"  user-1 历史长度: {result['user-1_history_len']}")
    print(f"  会话隔离: {result['sessions_isolated']}")

    print("\n=== 2. 滑动窗口合并 ===")
    old = [f"old_{i}" for i in range(25)]
    new = ["new_1", "new_2"]
    merged = merge_with_sliding_window(old, new, max_messages=20)
    print(f"  原始 {len(old)} 条 + 新增 {len(new)} 条 → 合并后 {len(merged)} 条")
    print(f"  最早: {merged[0]}, 最新: {merged[-1]}")
