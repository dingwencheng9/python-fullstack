"""
L16: 练习 3 参考答案 - 异步限流器
"""

import asyncio
import time as time_module
from collections.abc import AsyncIterator


async def simulate_request(url: str, delay: float = 0.1) -> dict:
    """模拟异步请求。"""
    await asyncio.sleep(delay)
    return {"url": url, "status": "success", "timestamp": time_module.time()}


class AsyncRateLimiter:
    """异步限流器。"""

    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.max_concurrent = max_concurrent

    async def acquire(self):
        await self.semaphore.acquire()

    def release(self):
        self.semaphore.release()

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()

    async def run_task(self, coro):
        async with self:
            return await coro


async def batch_requests(urls: list[str], max_concurrent: int = 3) -> list[dict]:
    """批量发送请求，使用限流器控制并发。"""
    limiter = AsyncRateLimiter(max_concurrent)

    # 创建任务
    tasks = [
        limiter.run_task(simulate_request(url))
        for url in urls
    ]

    # 并发执行
    return await asyncio.gather(*tasks)


class AsyncThrottledIterator:
    """节流迭代器，限制迭代速率。"""

    def __init__(self, items: list, rate: float):
        self.items = items
        self.rate = rate
        self.interval = 1.0 / rate
        self._index = 0
        self._last_yield_time = 0.0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index >= len(self.items):
            raise StopAsyncIteration

        # 节流：如果距离上次太快，等待
        now = time_module.monotonic()
        elapsed = now - self._last_yield_time
        if elapsed < self.interval and self._last_yield_time > 0:
            await asyncio.sleep(self.interval - elapsed)

        # 更新状态并返回
        self._last_yield_time = time_module.monotonic()
        item = self.items[self._index]
        self._index += 1
        return item
