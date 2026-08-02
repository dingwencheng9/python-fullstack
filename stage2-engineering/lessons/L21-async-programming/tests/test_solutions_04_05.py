"""测试文件 - 自动重构

from __future__ import annotations

移除 sys.path 污染，使用 importlib 动态加载
"""

from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path

import pytest


@pytest.fixture
def solution_04():
    """加载 solution_04 模块"""
    file_path = (
        Path(__file__).parent.parent / "solutions" / "solution_04_async_context.py"
    )
    spec = importlib.util.spec_from_file_location("solution_04", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def solution_05():
    """加载 solution_05 模块"""
    file_path = (
        Path(__file__).parent.parent / "solutions" / "solution_05_async_patterns.py"
    )
    spec = importlib.util.spec_from_file_location("solution_05", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestAsyncDatabase:
    """测试 AsyncDatabase 异步上下文管理器"""

    @pytest.mark.asyncio
    async def test_async_database_basic(self, solution_04, solution_05):
        """测试基本数据库操作"""
        async with solution_04.AsyncDatabase("localhost") as db:
            result = await db.query("SELECT * FROM users")
            assert isinstance(result, list)


class TestProducer:
    """测试 producer 异步函数"""

    @pytest.mark.asyncio
    async def test_producer_basic(self, solution_04, solution_05):
        """测试基本生产"""
        queue = asyncio.Queue()
        await solution_05.producer(queue, 3)

        # 队列中应该有 3 个元素 + 1 个 None 停止信号
        assert queue.qsize() == 4

    @pytest.mark.asyncio
    async def test_producer_zero(self, solution_04, solution_05):
        """测试零生产"""
        queue = asyncio.Queue()
        await solution_05.producer(queue, 0)

        # 应该只有停止信号
        assert queue.qsize() == 1


class TestConsumer:
    """测试 consumer 异步函数"""

    @pytest.mark.asyncio
    async def test_consumer_basic(self, solution_04, solution_05):
        """测试基本消费"""
        queue = asyncio.Queue()
        await queue.put(1)
        await queue.put(2)
        await queue.put(None)  # 停止信号

        # 创建消费者任务
        task = asyncio.create_task(solution_05.consumer(queue, "test"))

        # 等待消费完成
        await asyncio.wait_for(task, timeout=1.0)


class TestRetry:
    """测试 retry_async 重试机制"""

    @pytest.mark.asyncio
    async def test_retry_async_basic(self, solution_04, solution_05):
        """测试基本重试机制"""
        result = await solution_05.retry_async(
            solution_05.flaky_api_call, max_retries=3
        )
        # flaky_api_call 在成功时返回 None 或其他值
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
