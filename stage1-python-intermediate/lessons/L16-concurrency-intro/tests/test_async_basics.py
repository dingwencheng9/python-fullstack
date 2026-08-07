"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L16: 并发编程 - async/await 测试
"""

import pytest


@pytest.mark.asyncio
async def test_gather_results():
    """测试并发获取多个结果"""
    results = await async_basics.gather_results()
    assert results == ["A", "B", "C"]


@pytest.mark.asyncio
async def test_sequential_results():
    """测试顺序获取多个结果"""
    results = await async_basics.sequential_results()
    assert results == ["A", "B", "C"]


@pytest.mark.asyncio
async def test_with_timeout_coro_success():
    """测试超时处理成功情况"""
    result = await async_basics.with_timeout_coro()
    assert result == "超时"  # 因为默认延迟是 5 秒，超时 0.1 秒


@pytest.mark.asyncio
async def test_concurrent_tasks():
    """测试并发任务"""

    async def task(i):
        return i * 2

    tasks = [task(1), task(2), task(3)]
    results = await async_basics.concurrent_tasks(tasks)
    assert sorted(results) == [2, 4, 6]


@pytest.mark.asyncio
async def test_create_tasks():
    """测试创建任务"""
    results = await async_basics.create_tasks()
    assert len(results) == 3
    for r in results:
        assert "完成" in r
