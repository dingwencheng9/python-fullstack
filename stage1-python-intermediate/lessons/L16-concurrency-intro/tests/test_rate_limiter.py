"""
L16: 练习 3 测试 - 异步限流器
"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
import asyncio
import time

import pytest


@pytest.mark.asyncio
async def test_rate_limiter_basic():
    """测试限流器基本功能。"""
    limiter = rate_limiter.AsyncRateLimiter(max_concurrent=2)

    async def task(n):
        async with limiter:
            await asyncio.sleep(0.01)
            return n

    results = await asyncio.gather(*[task(i) for i in range(4)])
    assert sorted(results) == [0, 1, 2, 3]


@pytest.mark.asyncio
async def test_rate_limiter_timing():
    """测试限流器确实限制了并发数。"""
    limiter = rate_limiter.AsyncRateLimiter(max_concurrent=1)

    async def task(n):
        async with limiter:
            await asyncio.sleep(0.05)
            return n

    start = time.time()
    await asyncio.gather(*[task(i) for i in range(3)])
    elapsed = time.time() - start

    # 1 个并发，每批 0.05s，3 个任务至少需要 0.15s
    assert elapsed >= 0.14, f"应该至少 0.14s，实际 {elapsed:.2f}s"


@pytest.mark.asyncio
async def test_batch_requests():
    """测试批量请求。"""
    urls = [f"http://example.com/{i}" for i in range(5)]

    # 使用较高的限流以便测试通过
    results = await rate_limiter.batch_requests(urls, max_concurrent=5)

    assert len(results) == 5
    for r in results:
        assert r["status"] == "success"
        assert "url" in r


@pytest.mark.asyncio
async def test_throttled_iterator():
    """测试节流迭代器。"""
    items = list(range(5))
    throttler = rate_limiter.AsyncThrottledIterator(items, rate=20)  # 每秒 20 项 = 每项 0.05s

    results = []
    start = time.time()

    async for item in throttler:
        results.append(item)

    elapsed = time.time() - start

    assert results == items
    # 5 项，每项间隔 0.05s，最少需要 0.20s
    assert elapsed >= 0.18, f"应该至少 0.18s，实际 {elapsed:.2f}s"
