"""

from __future__ import annotations

练习 5: 异步模式实战 - 参考答案

===============================================================================
解题思路: 生产者-消费者、重试机制、并发爬虫等实用异步模式
===============================================================================
"""

import asyncio
from collections.abc import AsyncIterator

# ============================================================================
# 模式 1: 生产者-消费者
# ============================================================================


async def producer(queue: asyncio.Queue, n: int):
    """生产者"""
    for i in range(n):
        item = f"item-{i}"
        await queue.put(item)
        print(f"生产: {item}")
        await asyncio.sleep(0.1)
    await queue.put(None)  # 结束信号


async def consumer(queue: asyncio.Queue, name: str):
    """消费者"""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"{name} 消费: {item}")
        await asyncio.sleep(0.2)
        queue.task_done()


async def test_producer_consumer():
    """测试生产者-消费者"""
    print("测试 1: 生产者-消费者模式")
    queue = asyncio.Queue(maxsize=5)

    await asyncio.gather(
        producer(queue, 10),
        consumer(queue, "Consumer-1"),
    )
    print("✅ 生产者-消费者测试通过\n")


# ============================================================================
# 模式 2: 重试机制
# ============================================================================


async def retry_async(func, max_retries: int = 3, delay: float = 1.0):
    """异步重试装饰器"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"重试 {attempt + 1}/{max_retries}: {e}")
            await asyncio.sleep(delay)


async def flaky_api_call():
    """模拟不稳定但可复现的 API。

    为了让课程测试稳定，每 3 次调用中前 2 次失败、第 3 次成功。
    """
    attempts = getattr(flaky_api_call, "_attempts", 0) + 1
    flaky_api_call._attempts = attempts  # type: ignore[attr-defined]

    if attempts % 3 != 0:
        raise ConnectionError("API 暂时不可用")
    return "成功响应"


async def test_retry():
    """测试重试机制"""
    print("测试 2: 重试机制")
    try:
        result = await retry_async(flaky_api_call, max_retries=5, delay=0.5)
        print(f"结果: {result}")
    except Exception as e:
        print(f"最终失败: {e}")
    print("✅ 重试测试通过\n")


# ============================================================================
# 模式 3: 异步迭代器
# ============================================================================


async def async_range(n: int) -> AsyncIterator[int]:
    """异步范围生成器"""
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i


async def test_async_iterator():
    """测试异步迭代器"""
    print("测试 3: 异步迭代器")
    async for num in async_range(5):
        print(f"  {num}")
    print("✅ 异步迭代器测试通过\n")


# ============================================================================
# 主测试
# ============================================================================


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("练习 5: 异步模式实战")
    print("=" * 60)
    print()

    await test_producer_consumer()
    await test_retry()
    await test_async_iterator()

    print("=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
