"""

from __future__ import annotations

测试异步装饰器与现代并发模式

验证 asyncio.TaskGroup 和异步装饰器的正确性
"""

import asyncio
import time

from examples.async_decorators_modern import (
    async_cache,
    async_retry,
    async_timer,
    concurrent_map,
    expensive_calculation,
    fetch_data,
    process_item,
)
import pytest


class TestAsyncTimer:
    """测试异步计时装饰器"""

    @pytest.mark.asyncio
    async def test_async_timer_basic(self, capsys):
        """测试基本异步计时功能"""

        @async_timer
        async def async_func():
            await asyncio.sleep(0.01)
            return "done"

        result = await async_func()
        assert result == "done"

        captured = capsys.readouterr()
        assert "async_func" in captured.out
        assert "⏱️" in captured.out

    @pytest.mark.asyncio
    async def test_async_timer_with_args(self):
        """测试带参数的异步函数计时"""

        @async_timer
        async def add_async(a: int, b: int) -> int:
            await asyncio.sleep(0.01)
            return a + b

        result = await add_async(2, 3)
        assert result == 5

    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试预定义的 fetch_data 函数"""
        result = await fetch_data("https://test.com")
        assert isinstance(result, dict)
        assert result["url"] == "https://test.com"
        assert result["status"] == "ok"


class TestAsyncRetry:
    """测试异步重试装饰器"""

    @pytest.mark.asyncio
    async def test_async_retry_success(self):
        """测试重试成功的情况"""
        call_count = 0

        @async_retry(max_attempts=3, delay=0.01, backoff=2.0)
        async def sometimes_fails():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Failed")
            return "Success"

        result = await sometimes_fails()
        assert result == "Success"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_async_retry_all_fail(self):
        """测试所有重试都失败的情况"""

        @async_retry(max_attempts=3, delay=0.01)
        async def always_fails():
            raise ConnectionError("Always fails")

        with pytest.raises(ConnectionError, match="Always fails"):
            await always_fails()

    @pytest.mark.asyncio
    async def test_async_retry_immediate_success(self):
        """测试第一次就成功的情况"""

        @async_retry(max_attempts=3, delay=0.01)
        async def immediate_success():
            return "OK"

        result = await immediate_success()
        assert result == "OK"


class TestConcurrentMap:
    """测试并发映射装饰器（使用 TaskGroup）"""

    @pytest.mark.asyncio
    async def test_concurrent_map_basic(self):
        """测试基本并发处理"""

        @concurrent_map(max_concurrent=3)
        async def double(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 2

        items = [1, 2, 3, 4, 5]
        results = await double(items)

        assert results == [2, 4, 6, 8, 10]

    @pytest.mark.asyncio
    async def test_concurrent_map_timing(self):
        """测试并发处理的性能"""

        @concurrent_map(max_concurrent=5)
        async def slow_process(x: int) -> int:
            await asyncio.sleep(0.1)
            return x

        items = list(range(10))

        start = time.perf_counter()
        results = await slow_process(items)
        elapsed = time.perf_counter() - start

        assert results == items
        # 10 个任务，最多 5 个并发，每个 0.1s
        # 应该在约 0.2s 内完成（而非 1.0s 串行）
        assert elapsed < 0.3

    @pytest.mark.asyncio
    async def test_concurrent_map_order_preserved(self):
        """测试结果顺序是否保持"""

        @concurrent_map(max_concurrent=3)
        async def process_with_delay(x: int) -> int:
            # 延迟时间与值成反比，测试顺序保持
            await asyncio.sleep(0.01 * (10 - x))
            return x * 10

        items = [1, 2, 3, 4, 5]
        results = await process_with_delay(items)

        assert results == [10, 20, 30, 40, 50]

    @pytest.mark.asyncio
    async def test_process_item_function(self):
        """测试预定义的 process_item 函数"""
        items = [1, 2, 3]
        results = await process_item(items)
        assert results == [2, 4, 6]


class TestAsyncCache:
    """测试异步缓存装饰器"""

    @pytest.mark.asyncio
    async def test_async_cache_basic(self):
        """测试基本缓存功能"""
        call_count = 0

        @async_cache(ttl=1.0)
        async def cached_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)
            return x * 2

        # 第一次调用
        result1 = await cached_func(5)
        assert result1 == 10
        assert call_count == 1

        # 第二次调用（缓存命中）
        result2 = await cached_func(5)
        assert result2 == 10
        assert call_count == 1  # 没有增加

    @pytest.mark.asyncio
    async def test_async_cache_ttl_expiration(self):
        """测试缓存过期"""
        call_count = 0

        @async_cache(ttl=0.1)
        async def cached_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        await cached_func(5)
        assert call_count == 1

        # 等待缓存过期
        await asyncio.sleep(0.15)

        await cached_func(5)
        assert call_count == 2  # 重新计算

    @pytest.mark.asyncio
    async def test_async_cache_no_ttl(self):
        """测试无 TTL 限制的缓存"""

        @async_cache(ttl=None)
        async def cached_func(x: int) -> int:
            await asyncio.sleep(0.01)
            return x**2

        result1 = await cached_func(3)
        assert result1 == 9

        result2 = await cached_func(3)
        assert result2 == 9

    @pytest.mark.asyncio
    async def test_async_cache_clear(self):
        """测试缓存清除"""
        call_count = 0

        @async_cache(ttl=10.0)
        async def cached_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x + 1

        await cached_func(1)
        assert call_count == 1

        cached_func.cache_clear()

        await cached_func(1)
        assert call_count == 2  # 缓存已清除

    @pytest.mark.asyncio
    async def test_expensive_calculation_function(self):
        """测试预定义的 expensive_calculation 函数"""
        result = await expensive_calculation(4)
        assert result == 16


class TestTaskGroupErrorHandling:
    """测试 TaskGroup 的错误处理"""

    @pytest.mark.asyncio
    async def test_taskgroup_single_failure(self):
        """测试单个任务失败的情况"""

        async def success_task():
            await asyncio.sleep(0.1)
            return "success"

        async def failure_task():
            await asyncio.sleep(0.05)
            raise ValueError("Task failed")

        with pytest.raises(ExceptionGroup) as exc_info:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(success_task())
                tg.create_task(failure_task())

        # 验证捕获到异常组
        eg = exc_info.value
        assert len(eg.exceptions) == 1
        assert isinstance(eg.exceptions[0], ValueError)

    @pytest.mark.asyncio
    async def test_taskgroup_all_success(self):
        """测试所有任务都成功的情况"""

        async def task(n: int) -> int:
            await asyncio.sleep(0.01)
            return n * 2

        results = []

        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(task(i)) for i in range(5)]

        # 收集结果
        for t in tasks:
            results.append(t.result())

        assert results == [0, 2, 4, 6, 8]


class TestIntegration:
    """集成测试"""

    @pytest.mark.asyncio
    async def test_decorator_composition(self):
        """测试装饰器组合"""

        @async_timer
        @async_cache(ttl=1.0)
        async def composed_func(x: int) -> int:
            await asyncio.sleep(0.05)
            return x * 3

        result1 = await composed_func(7)
        assert result1 == 21

        result2 = await composed_func(7)
        assert result2 == 21

    @pytest.mark.asyncio
    async def test_concurrent_cached_processing(self):
        """测试并发 + 缓存的组合"""
        call_count = 0

        @concurrent_map(max_concurrent=3)
        async def process(x: int) -> int:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)
            return x * 2

        items = [1, 2, 3, 4, 5]
        results = await process(items)

        assert results == [2, 4, 6, 8, 10]
        assert call_count == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
