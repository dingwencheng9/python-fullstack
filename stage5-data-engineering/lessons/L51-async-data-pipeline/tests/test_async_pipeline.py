"""

from __future__ import annotations

L52 异步数据管道 基准测试

测试维度:
1. 模块导入健康测试
2. 核心异步管道逻辑测试
3. 异常边界测试
"""

import asyncio
from asyncio import Queue, Semaphore

import pytest

# ============================================================================
# 测试维度 1: 模块导入健康测试
# ============================================================================


def test_import_asyncio():
    """测试 asyncio 依赖导入"""
    try:
        import asyncio
        from asyncio import Lock, Queue, Semaphore

        assert asyncio is not None
        assert Queue is not None
        assert Semaphore is not None
        assert Lock is not None
    except ImportError as e:
        pytest.fail(f"asyncio 导入失败: {e}")


def test_import_typing():
    """测试 typing 依赖导入"""
    try:
        from collections.abc import AsyncGenerator, AsyncIterator

        assert AsyncGenerator is not None
        assert AsyncIterator is not None
    except ImportError as e:
        pytest.fail(f"typing 导入失败: {e}")


def test_import_dataclasses():
    """测试 dataclasses 依赖导入"""
    try:
        from dataclasses import dataclass, field

        assert dataclass is not None
        assert field is not None
    except ImportError as e:
        pytest.fail(f"dataclasses 导入失败: {e}")


# ============================================================================
# 测试维度 2: 核心异步管道逻辑测试
# ============================================================================


@pytest.mark.asyncio
async def test_queue_basic_operations():
    """测试队列基础操作"""
    queue = Queue(maxsize=10)

    # 放入数据
    await queue.put(1)
    await queue.put(2)
    await queue.put(3)

    # 取出数据
    assert await queue.get() == 1
    assert await queue.get() == 2
    assert await queue.get() == 3


@pytest.mark.asyncio
async def test_producer_consumer():
    """测试生产者-消费者模式"""
    queue = Queue(maxsize=5)
    produced_items = []
    consumed_items = []

    async def producer(n: int):
        """生产者"""
        for i in range(n):
            await queue.put(i)
            produced_items.append(i)
            await asyncio.sleep(0.01)
        await queue.put(None)  # 结束信号

    async def consumer():
        """消费者"""
        while True:
            item = await queue.get()
            if item is None:
                break
            consumed_items.append(item)
            await asyncio.sleep(0.01)

    # 并发执行
    await asyncio.gather(producer(10), consumer())

    assert len(produced_items) == 10
    assert len(consumed_items) == 10
    assert produced_items == consumed_items


@pytest.mark.asyncio
async def test_multiple_consumers():
    """测试多消费者并发"""
    queue = Queue(maxsize=10)
    consumed_items = []

    async def producer(n: int):
        """生产者"""
        for i in range(n):
            await queue.put(i)
        # 为每个消费者发送结束信号
        for _ in range(3):
            await queue.put(None)

    async def consumer(consumer_id: int):
        """消费者"""
        while True:
            item = await queue.get()
            if item is None:
                break
            consumed_items.append((consumer_id, item))
            await asyncio.sleep(0.01)

    # 1 个生产者，3 个消费者
    await asyncio.gather(producer(15), consumer(1), consumer(2), consumer(3))

    assert len(consumed_items) == 15


@pytest.mark.asyncio
async def test_semaphore_concurrency_control():
    """测试信号量并发控制"""
    semaphore = Semaphore(3)  # 最多 3 个并发
    concurrent_count = {"max": 0, "current": 0}

    async def worker(worker_id: int):
        """工作者"""
        async with semaphore:
            concurrent_count["current"] += 1
            concurrent_count["max"] = max(concurrent_count["max"], concurrent_count["current"])
            await asyncio.sleep(0.1)
            concurrent_count["current"] -= 1

    # 启动 10 个工作者
    await asyncio.gather(*[worker(i) for i in range(10)])

    # 最大并发数不应超过 3
    assert concurrent_count["max"] <= 3


@pytest.mark.asyncio
async def test_async_pipeline():
    """测试异步管道"""

    async def stage1(data: int) -> int:
        """阶段 1: 加倍"""
        await asyncio.sleep(0.01)
        return data * 2

    async def stage2(data: int) -> int:
        """阶段 2: 加 10"""
        await asyncio.sleep(0.01)
        return data + 10

    async def pipeline(data: int) -> int:
        """管道"""
        result = await stage1(data)
        return await stage2(result)

    # 测试单个数据流
    result = await pipeline(5)
    assert result == 20  # 5 * 2 + 10

    # 测试批量数据流
    results = await asyncio.gather(*[pipeline(i) for i in range(5)])
    assert results == [10, 12, 14, 16, 18]


# ============================================================================
# 测试维度 3: 异常边界测试
# ============================================================================


@pytest.mark.asyncio
async def test_queue_full():
    """测试队列满时的行为"""
    queue = Queue(maxsize=2)

    # 填满队列
    await queue.put(1)
    await queue.put(2)

    # 使用 wait_for 避免永久阻塞
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(queue.put(3), timeout=0.1)


@pytest.mark.asyncio
async def test_queue_empty():
    """测试队列空时的行为"""
    queue = Queue()

    # 尝试从空队列获取
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(queue.get(), timeout=0.1)


@pytest.mark.asyncio
async def test_task_cancellation():
    """测试任务取消"""
    cancelled_flag = {"value": False}

    async def long_running_task():
        """长时间运行的任务"""
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            cancelled_flag["value"] = True
            raise

    # 创建任务
    task = asyncio.create_task(long_running_task())

    # 等待一小段时间后取消
    await asyncio.sleep(0.1)
    task.cancel()

    # 等待任务完成
    with pytest.raises(asyncio.CancelledError):
        await task

    assert cancelled_flag["value"] is True


@pytest.mark.asyncio
async def test_producer_failure():
    """测试生产者失败"""
    queue = Queue()
    error_occurred = {"value": False}

    async def failing_producer():
        """会失败的生产者"""
        await queue.put(1)
        raise ValueError("Producer failed")

    async def consumer():
        """消费者"""
        try:
            item = await asyncio.wait_for(queue.get(), timeout=0.5)
            assert item == 1
        except TimeoutError:
            error_occurred["value"] = True

    with pytest.raises(ValueError, match="Producer failed"):
        await asyncio.gather(failing_producer(), consumer())


@pytest.mark.asyncio
async def test_deadlock_prevention():
    """测试死锁预防"""

    async def task_with_timeout():
        """带超时的任务"""
        queue = Queue(maxsize=1)

        async def producer():
            await queue.put(1)
            # 尝试再放入一个，会阻塞
            await asyncio.wait_for(queue.put(2), timeout=0.1)

        with pytest.raises(asyncio.TimeoutError):
            await producer()

    await task_with_timeout()


@pytest.mark.asyncio
async def test_backpressure():
    """测试背压处理"""
    queue = Queue(maxsize=3)
    produced = []
    consumed = []

    async def producer():
        """快速生产者"""
        for i in range(10):
            await queue.put(i)
            produced.append(i)

    async def slow_consumer():
        """慢速消费者"""
        while len(consumed) < 10:
            item = await queue.get()
            consumed.append(item)
            await asyncio.sleep(0.05)  # 慢速处理

    await asyncio.gather(producer(), slow_consumer())

    assert len(produced) == 10
    assert len(consumed) == 10


# ============================================================================
# 集成测试
# ============================================================================


@pytest.mark.asyncio
async def test_multi_stage_pipeline():
    """测试多阶段管道"""
    queue1 = Queue(maxsize=5)
    queue2 = Queue(maxsize=5)
    results = []

    async def stage1_producer():
        """阶段 1: 生产者"""
        for i in range(10):
            await queue1.put(i)
        await queue1.put(None)

    async def stage2_transformer():
        """阶段 2: 转换器"""
        while True:
            item = await queue1.get()
            if item is None:
                await queue2.put(None)
                break
            transformed = item * 2
            await queue2.put(transformed)

    async def stage3_consumer():
        """阶段 3: 消费者"""
        while True:
            item = await queue2.get()
            if item is None:
                break
            results.append(item)

    await asyncio.gather(stage1_producer(), stage2_transformer(), stage3_consumer())

    assert len(results) == 10
    assert results[0] == 0  # 0 * 2
    assert results[5] == 10  # 5 * 2


@pytest.mark.asyncio
async def test_pipeline_with_error_handling():
    """测试带错误处理的管道"""
    queue = Queue()
    successful = []
    failed = []

    async def producer():
        """生产者"""
        for i in range(10):
            await queue.put(i)
        await queue.put(None)

    async def consumer():
        """带错误处理的消费者"""
        while True:
            item = await queue.get()
            if item is None:
                break

            try:
                if item % 3 == 0:
                    raise ValueError(f"Cannot process {item}")
                successful.append(item)
            except ValueError:
                failed.append(item)

    await asyncio.gather(producer(), consumer())

    assert len(successful) + len(failed) == 10
    assert 0 in failed  # 0 % 3 == 0
    assert 3 in failed  # 3 % 3 == 0


# ============================================================================
# 性能测试
# ============================================================================


@pytest.mark.asyncio
async def test_pipeline_throughput():
    """测试管道吞吐量"""
    import time

    queue = Queue(maxsize=100)
    n_items = 1000

    async def producer():
        for i in range(n_items):
            await queue.put(i)
        await queue.put(None)

    async def consumer():
        count = 0
        while True:
            item = await queue.get()
            if item is None:
                break
            count += 1
        return count

    start = time.time()
    _, consumed = await asyncio.gather(producer(), consumer())
    elapsed = time.time() - start

    assert consumed == n_items
    # 吞吐量应该很高
    throughput = n_items / elapsed
    assert throughput > 1000  # 每秒至少 1000 项


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
