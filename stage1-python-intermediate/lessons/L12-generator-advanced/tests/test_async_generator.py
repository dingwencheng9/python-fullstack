"""L12 生成器进阶 - 异步生成器测试

使用根 conftest.py 提供的 solutions fixture，避免 sys.path 污染。
"""

import pytest


@pytest.mark.asyncio
async def test_async_count(solutions):
    async_count = getattr(solutions, "async_count")
    result = [x async for x in async_count(5)]
    assert result == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_async_filter(solutions):
    async_filter = getattr(solutions, "async_filter")
    async_count = getattr(solutions, "async_count")

    async def is_even(x):
        return x % 2 == 0
    result = [x async for x in async_filter(is_even, async_count(6))]
    assert result == [0, 2, 4]


@pytest.mark.asyncio
async def test_async_map(solutions):
    async_map = getattr(solutions, "async_map")
    async_count = getattr(solutions, "async_count")
    result = [x async for x in async_map(lambda x: x * 2, async_count(5))]
    assert result == [0, 2, 4, 6, 8]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-asyncio-mode=auto"])
