"""
L56 Agent 记忆管理 — 核心行为测试

测试覆盖：
- InMemoryHistory 的添加与上限裁剪
- SlidingWindowHistory 的消息保留
- SummarizedHistory 的自动摘要
- 多级记忆的层级隔离
- Token 计数与裁剪
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


LESSON_ROOT = Path(__file__).resolve().parent.parent


def _load_module(name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# 1. 记忆类型测试
# ---------------------------------------------------------------------------


def test_in_memory_history_add_and_load():
    """InMemoryHistory 应正确存储和加载消息。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    history = mod.InMemoryHistory()
    history.add("user", "你好")
    history.add("assistant", "你好！")

    loaded = history.load()
    assert len(loaded) == 2
    assert "user: 你好" in loaded
    assert "assistant: 你好！" in loaded


def test_in_memory_history_max_messages_trim():
    """InMemoryHistory 超出上限时应自动裁剪最旧消息。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    history = mod.InMemoryHistory(max_messages=3)

    for i in range(5):
        history.add("user", f"msg_{i}")

    loaded = history.load()
    assert len(loaded) == 3
    assert "user: msg_4" in loaded
    assert "user: msg_0" not in loaded


def test_sliding_window_trim_messages():
    """滑动窗口应保留最近 N 条消息。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    history = mod.SlidingWindowHistory(max_messages=5)

    for i in range(10):
        history.add("user", f"msg_{i}")

    loaded = history.load()
    assert len(loaded) == 5
    assert "user: msg_9" in loaded


def test_summarized_history_reduces_old_messages():
    """SummarizedHistory 应在消息超过阈值时自动生成摘要。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    history = mod.SummarizedHistory()

    for i in range(12):
        history.add("user", f"这是第 {i} 条消息内容")

    loaded = history.load()
    # 应包含摘要消息
    summary_messages = [m for m in loaded if "摘要" in m]
    assert len(summary_messages) >= 1


# ---------------------------------------------------------------------------
# 2. Token 计数与裁剪测试
# ---------------------------------------------------------------------------


def test_count_tokens_returns_positive():
    """Token 计数应返回正数。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    assert mod.count_tokens("hello world") > 0


def test_count_tokens_consistent():
    """Token 计数应具有一致性（相同输入返回相同输出）。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    text = "Python is a great language"
    assert mod.count_tokens(text) == mod.count_tokens(text)


def test_trim_to_token_limit_keeps_under_limit():
    """Token 裁剪后消息总 Token 数应不超过限制。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    messages = [f"message number {i} with some content" for i in range(10)]
    trimmed = mod.trim_to_token_limit(messages, max_tokens=15)

    total = sum(mod.count_tokens(m) for m in trimmed)
    assert total <= 15


def test_trim_to_token_limit_preserves_recent_messages():
    """Token 裁剪应从后向前保留最新消息。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    messages = [f"old {i}" for i in range(5)] + [f"RECENT {i}" for i in range(5)]
    trimmed = mod.trim_to_token_limit(messages, max_tokens=50)

    # 最近消息应在结果中
    recent_in_result = any("RECENT" in m for m in trimmed)
    assert recent_in_result


# ---------------------------------------------------------------------------
# 3. 多级记忆测试
# ---------------------------------------------------------------------------


def test_multi_level_memory_save_and_retrieve():
    """多级记忆应正确存储和检索不同层级信息。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    memory = mod.MultiLevelMemory()

    memory.save_context("我叫小明", "你好小明", "user-1")
    memory.save_context("我喜欢 Python", "Python 很棒", "user-1")

    relevant = memory.load_relevant("小明", "user-1")
    assert "short" in relevant
    assert "mid" in relevant
    assert len(relevant["short"]) >= 2


def test_multi_level_memory_user_isolation():
    """不同用户的长记忆应完全隔离。"""
    mod = _load_module("mem01", LESSON_ROOT / "examples" / "01_memory_types.py")
    memory = mod.MultiLevelMemory()

    memory.save_context("我叫小明", "你好", "user-1")
    memory.save_context("我叫小红", "你好", "user-2")

    user1 = memory.load_relevant("用户", "user-1")
    user2 = memory.load_relevant("用户", "user-2")

    # 短期记忆中各用户数据应隔离
    user1_short = " ".join(user1.get("short", []))
    user2_short = " ".join(user2.get("short", []))
    assert "小明" in user1_short
    assert "小明" not in user2_short
    assert "小红" in user2_short


# ---------------------------------------------------------------------------
# 4. 检查点与恢复测试
# ---------------------------------------------------------------------------


def test_memory_checkpointer_put_and_get():
    """MemoryCheckpointer 应正确保存和恢复检查点。"""
    mod = _load_module("mem02", LESSON_ROOT / "examples" / "02_checkpoint_memory.py")
    checker = mod.MemoryCheckpointer()

    checkpoint = mod.ThreadCheckpoint(thread_id="session-1", step=0, values={"messages": ["hello"]})
    checker.put("session-1", checkpoint)

    restored = checker.get("session-1")
    assert restored is not None
    assert restored.step == 0
    assert restored.values["messages"] == ["hello"]


def test_memory_checkpointer_isolates_threads():
    """不同线程 ID 的检查点应完全隔离。"""
    mod = _load_module("mem02", LESSON_ROOT / "examples" / "02_checkpoint_memory.py")
    checker = mod.MemoryCheckpointer()

    for uid, step in [("thread-a", 1), ("thread-a", 2), ("thread-b", 1)]:
        checker.put(uid, mod.ThreadCheckpoint(thread_id=uid, step=step, values={}))

    # thread-a 最新是 step=2，thread-b 最新是 step=1
    assert checker.get("thread-a").step == 2
    assert checker.get("thread-b").step == 1


def test_sliding_window_merge_trims_old_messages():
    """滑动窗口合并应裁剪超出上限的旧消息。"""
    mod = _load_module("mem02", LESSON_ROOT / "examples" / "02_checkpoint_memory.py")

    old_msgs = [f"old_{i}" for i in range(25)]
    new_msgs = ["new_1", "new_2"]
    merged = mod.merge_with_sliding_window(old_msgs, new_msgs, max_messages=20)

    assert len(merged) == 20
    # 新消息应保留
    assert "new_1" in merged
    assert "new_2" in merged
    # 旧消息应被裁剪（25+2 → 20）
    assert "old_0" not in merged


def test_simulate_multi_session_memory_returns_isolated_data():
    """多会话模拟应返回完全隔离的数据。"""
    mod = _load_module("mem02", LESSON_ROOT / "examples" / "02_checkpoint_memory.py")
    result = mod.simulate_multi_session_memory()

    assert result["sessions_isolated"] is True
    assert result["user-1_latest"] == "小明"
    assert result["user-2_latest"] == "小红"
    assert result["user-1_history_len"] == 3
