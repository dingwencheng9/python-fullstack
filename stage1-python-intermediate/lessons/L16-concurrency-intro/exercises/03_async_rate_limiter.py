"""
L14: 练习 3 - 异步限流器

实现一个异步限流器，限制并发请求数。
"""

import asyncio
import time
from collections.abc import AsyncIterator


class AsyncRateLimiter:
    """异步限流器。

    使用信号量限制同时执行的任务数量。
    """

    def __init__(self, max_concurrent: int = 5):
        """初始化限流器。

        Args:
            max_concurrent: 最大并发数
        """
        # 初始化信号量
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.max_concurrent = max_concurrent
        # 追踪当前并发数（用于调试/测试场景，可选）
        self._current = 0

    async def acquire(self):
        """获取执行许可。

        如果当前并发数达到上限，会等待直到有任务完成。
        """
        await self.semaphore.acquire()
        # 可选地更新计数
        self._current += 1

    async def release(self):
        """释放执行许可。"""
        try:
            self.semaphore.release()
        finally:
            # 确保计数不会小于 0
            if self._current > 0:
                self._current -= 1

    async def __aenter__(self):
        """进入上下文管理器。"""
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器。"""
        await self.release()

    async def run_task(self, coro):
        """运行单个任务，自动获取和释放许可。

        Args:
            coro: 协程函数

        Returns:
            协程的执行结果
        """
        # 使用上下文管理器自动获取/释放许可，确保在任务内执行协程并返回结果
        async with self:
            return await coro


async def simulate_request(url: str, delay: float = 0.1) -> dict:
    """模拟异步请求。

    Args:
        url: 请求 URL
        delay: 模拟延迟（秒）

    Returns:
        响应结果字典
    """
    await asyncio.sleep(delay)
    return {"url": url, "status": "success", "timestamp": time.time()}


async def batch_requests(urls: list[str], max_concurrent: int = 3) -> list[dict]:
    """批量发送请求，使用限流器控制并发。

    Args:
        urls: URL 列表
        max_concurrent: 最大并发数

    Returns:
        响应结果列表
    """
    limiter = AsyncRateLimiter(max_concurrent=max_concurrent)
    tasks = [asyncio.create_task(limiter.run_task(simulate_request(url))) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


class AsyncThrottledIterator:
    """节流迭代器，限制迭代速率。

    用于限制 API 调用频率（如每分钟 60 次）。
    """

    def __init__(self, items: list, rate: float):
        """初始化节流迭代器。

        Args:
            items: 要迭代的项目列表
            rate: 每秒处理的项数
        """
        self.items = items
        self.rate = rate
        self.interval = 1.0 / rate
        self._last_yield_time = 0.0

    def __aiter__(self):
        return self

    async def __anext__(self):
        """异步获取下一项。"""
        if not hasattr(self, "_index"):
            self._index = 0

        if self._index >= len(self.items):
            raise StopAsyncIteration

        now = time.time()

        # 首次 yield 不等待
        if self._last_yield_time != 0.0:
            elapsed = now - self._last_yield_time
            if elapsed < self.interval:
                await asyncio.sleep(self.interval - elapsed)

        item = self.items[self._index]
        self._index += 1
        self._last_yield_time = time.time()
        return item


# === 验证 ===

if __name__ == "__main__":

    async def main():
        # 测试限流器
        limiter = AsyncRateLimiter(max_concurrent=2)

        async def task(n):
            async with limiter:
                await asyncio.sleep(0.05)
                return n

        start = time.time()
        results = await asyncio.gather(*[task(i) for i in range(4)])
        elapsed = time.time() - start

        # 2 个并发，每批需要 0.05*2=0.1 秒，4 个任务需要 2 批
        assert elapsed >= 0.1, f"应该至少 0.1 秒，实际 {elapsed}"
        assert sorted(results) == [0, 1, 2, 3]
        print(f"✅ AsyncRateLimiter 测试通过 (耗时: {elapsed:.2f}s)")

        # 测试批量请求
        urls = [f"http://example.com/{i}" for i in range(6)]
        results = await batch_requests(urls, max_concurrent=2)
        assert len(results) == 6
        assert all(r["status"] == "success" for r in results)
        print("✅ batch_requests 测试通过")

        print("\n✅ 所有测试通过！")

    asyncio.run(main())
