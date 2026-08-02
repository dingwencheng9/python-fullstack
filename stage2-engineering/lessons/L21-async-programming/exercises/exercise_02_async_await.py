"""练习 2: asyncio.Event + asyncio.Condition.

学习目标：
- 使用 Event 实现协程间的信号通知
- 使用 Condition 实现条件变量（等待条件满足后再继续）
- 实现优雅关闭模式
"""

from __future__ import annotations

import asyncio


# ============================================================
# Event：一次性信号通知
# ============================================================


class DownloadManager:
    """使用 Event 管理下载完成信号。"""

    def __init__(self) -> None:
        self.all_done = asyncio.Event()

    async def downloader(self, task_id: int) -> None:
        """模拟下载任务。"""
        await asyncio.sleep(0.5)
        print(f"  [D{task_id}] 下载完成")
        self.all_done.set()  # 任意一个完成后触发

    async def monitor(self) -> None:
        """等待所有下载完成。"""
        print("  监控器：等待完成信号...")
        await self.all_done.wait()
        print("  监控器：收到完成信号！")


async def test_event() -> None:
    """测试 Event 信号通知。"""
    print("=" * 60)
    print("练习 2: asyncio.Event + asyncio.Condition")
    print("=" * 60)
    print()

    manager = DownloadManager()
    await asyncio.gather(
        manager.downloader(1),
        manager.downloader(2),
        manager.monitor(),
    )
    print()
    print("✅ Event 信号通知测试通过")


# ============================================================
# Condition：条件变量
# ============================================================


class BoundedBuffer:
    """使用 Condition 实现有界缓冲区。"""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._items: list[int] = []
        self._condition = asyncio.Condition()

    async def put(self, item: int) -> None:
        async with self._condition:
            while len(self._items) >= self.capacity:
                await self._condition.wait()
            self._items.append(item)
            print(f"  put({item}), buffer size: {len(self._items)}")
            self._condition.notify()

    async def get(self) -> int:
        async with self._condition:
            while not self._items:
                await self._condition.wait()
            item = self._items.pop(0)
            print(f"  get() -> {item}, buffer size: {len(self._items)}")
            self._condition.notify()
            return item

    async def size(self) -> int:
        async with self._condition:
            return len(self._items)


async def test_condition() -> None:
    """测试 Condition 条件变量。"""
    buffer = BoundedBuffer(capacity=3)

    async def producer():
        for i in range(5):
            await buffer.put(i)
            await asyncio.sleep(0.1)

    async def consumer():
        await asyncio.sleep(0.15)  # 稍晚启动
        for _ in range(5):
            await buffer.get()
            await asyncio.sleep(0.2)

    await asyncio.gather(producer(), consumer())
    print()
    print("✅ Condition 条件变量测试通过")


# ============================================================
# 自检入口
# ============================================================


async def main() -> None:
    try:
        await test_event()
        await test_condition()
    except Exception as exc:
        print(f"❌ 错误: {exc}")
        raise SystemExit(1) from exc

    print()
    print("🎉 练习 2 完成！")
    print("下一步: exercise_03_as_completed_wait.py")


if __name__ == "__main__":
    asyncio.run(main())
