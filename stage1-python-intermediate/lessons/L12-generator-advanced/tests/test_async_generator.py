"""L12 生成器进阶 - 异步生成器测试"""

import pytest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "solutions"))

from solution_03_async_generator import async_count, async_filter, async_map


@pytest.mark.asyncio
async def test_async_count():
    result = [x async for x in async_count(5)]
    assert result == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_async_filter():
    async def is_even(x):
        return x % 2 == 0
    result = [x async for x in async_filter(is_even, async_count(6))]
    assert result == [0, 2, 4]


@pytest.mark.asyncio
async def test_async_map():
    result = [x async for x in async_map(lambda x: x * 2, async_count(5))]
    assert result == [0, 2, 4, 6, 8]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-asyncio-mode=auto"])
