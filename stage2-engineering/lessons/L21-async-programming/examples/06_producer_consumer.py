"""

from __future__ import annotations

异步生产者-消费者模式

演示使用 asyncio.Queue 实现生产者-消费者模式。
这是异步编程中最常见的协作模式之一。

应用场景：
- 任务队列
- 数据流处理
- 限流和缓冲

作者: Python 3.13 全栈课程
日期: 2026-06-04
Python版本: 3.13+
"""

import asyncio
import random
import time

# ============================================
# 示例1: 基础生产者-消费者
# ============================================


async def basic_producer(queue: asyncio.Queue[int], n: int) -> None:
    """
    生产者：生成数据并放入队列

    Args:
        queue: 异步队列
        n: 生产的数据数量
    """
    for i in range(n):
        await asyncio.sleep(0.1)  # 模拟生产时间
        await queue.put(i)
        print(f"[生产] 生产数据: {i}")

    # 发送结束信号
    await queue.put(None)


async def basic_consumer(queue: asyncio.Queue[int | None]) -> None:
    """
    消费者：从队列取数据并处理

    Args:
        queue: 异步队列
    """
    while True:
        item = await queue.get()

        # 检查结束信号
        if item is None:
            break

        # 处理数据
        await asyncio.sleep(0.2)  # 模拟处理时间
        print(f"[消费] 处理数据: {item}")


async def demonstrate_basic_pattern() -> None:
    """演示基础模式"""
    print("=" * 60)
    print("1. 基础生产者-消费者模式")
    print("=" * 60)

    # 创建队列（最大容量5）
    queue: asyncio.Queue[int | None] = asyncio.Queue(maxsize=5)

    # 并发运行生产者和消费者
    await asyncio.gather(
        basic_producer(queue, 5),
        basic_consumer(queue),
    )

    print()


# ============================================
# 示例2: 多生产者-多消费者
# ============================================


async def multi_producer(
    queue: asyncio.Queue[int | None], producer_id: int, n: int
) -> None:
    """多个生产者之一"""
    for i in range(n):
        await asyncio.sleep(random.uniform(0.05, 0.15))
        item = producer_id * 100 + i
        await queue.put(item)
        print(f"[生产者{producer_id}] 生产: {item}")


async def multi_consumer(queue: asyncio.Queue[int | None], consumer_id: int) -> None:
    """多个消费者之一"""
    while True:
        item = await queue.get()

        if item is None:
            break

        await asyncio.sleep(random.uniform(0.1, 0.3))
        print(f"[消费者{consumer_id}] 处理: {item}")


async def demonstrate_multiple_workers() -> None:
    """演示多生产者-多消费者"""
    print("=" * 60)
    print("2. 多生产者-多消费者模式")
    print("=" * 60)

    queue: asyncio.Queue[int | None] = asyncio.Queue(maxsize=10)

    # 启动2个生产者和3个消费者
    producers = [
        multi_producer(queue, producer_id=1, n=3),
        multi_producer(queue, producer_id=2, n=3),
    ]

    consumers = [
        multi_consumer(queue, consumer_id=1),
        multi_consumer(queue, consumer_id=2),
        multi_consumer(queue, consumer_id=3),
    ]

    # 先启动生产者；生产完成后，为每个消费者发送一个结束信号。
    consumer_tasks = [asyncio.create_task(consumer) for consumer in consumers]
    await asyncio.gather(*producers)
    for _ in consumer_tasks:
        await queue.put(None)
    await asyncio.gather(*consumer_tasks)

    print()


# ============================================
# 示例3: 带优先级的队列
# ============================================


async def priority_producer(queue: asyncio.PriorityQueue[tuple[int, str]]) -> None:
    """生产者（带优先级）"""
    tasks = [
        (5, "低优先级任务1"),
        (1, "高优先级任务"),
        (3, "中优先级任务"),
        (5, "低优先级任务2"),
    ]

    for priority, task in tasks:
        await asyncio.sleep(0.1)
        await queue.put((priority, task))
        print(f"[生产] {task} (优先级={priority})")

    await queue.put((0, "END"))  # 结束信号


async def priority_consumer(queue: asyncio.PriorityQueue[tuple[int, str]]) -> None:
    """消费者（按优先级处理）"""
    while True:
        priority, task = await queue.get()

        if task == "END":
            break

        await asyncio.sleep(0.2)
        print(f"[处理] {task} (优先级={priority})")


async def demonstrate_priority_queue() -> None:
    """演示优先级队列"""
    print("=" * 60)
    print("3. 优先级队列")
    print("=" * 60)

    queue: asyncio.PriorityQueue[tuple[int, str]] = asyncio.PriorityQueue()

    await asyncio.gather(
        priority_producer(queue),
        priority_consumer(queue),
    )

    print()


# ============================================
# 示例4: 实战应用 - 任务处理器
# ============================================


class Task:
    """任务对象"""

    def __init__(self, task_id: int, data: str) -> None:
        self.task_id = task_id
        self.data = data

    def __repr__(self) -> str:
        return f"Task({self.task_id}, {self.data!r})"


async def task_generator(queue: asyncio.Queue[Task | None], count: int) -> None:
    """任务生成器"""
    print(f"[生成器] 开始生成 {count} 个任务")

    for i in range(count):
        await asyncio.sleep(0.05)
        task = Task(i, f"数据-{i}")
        await queue.put(task)
        print(f"[生成器] 生成任务: {task}")

    # 发送结束信号
    await queue.put(None)
    print("[生成器] 完成")


async def task_processor(queue: asyncio.Queue[Task | None], processor_id: int) -> None:
    """任务处理器"""
    processed = 0

    while True:
        task = await queue.get()

        if task is None:
            break

        # 处理任务
        await asyncio.sleep(0.2)
        processed += 1
        print(f"[处理器{processor_id}] 处理任务: {task}")

    print(f"[处理器{processor_id}] 完成，共处理 {processed} 个任务")


async def demonstrate_task_processor() -> None:
    """演示任务处理器"""
    print("=" * 60)
    print("4. 实战应用 - 任务处理器")
    print("=" * 60)

    queue: asyncio.Queue[Task | None] = asyncio.Queue(maxsize=5)

    start = time.time()

    # 1 个生成器 + 3 个处理器。生成器结束后补足每个处理器的停止信号。
    processor_tasks = [
        asyncio.create_task(task_processor(queue, processor_id=1)),
        asyncio.create_task(task_processor(queue, processor_id=2)),
        asyncio.create_task(task_processor(queue, processor_id=3)),
    ]
    await task_generator(queue, count=10)
    for _ in processor_tasks:
        await queue.put(None)
    await asyncio.gather(*processor_tasks)

    elapsed = time.time() - start
    print(f"\n总耗时: {elapsed:.2f}秒")
    print()


# ============================================
# 主函数
# ============================================


async def main() -> None:
    """主函数"""
    print("\n" + "=" * 60)
    print("异步生产者-消费者模式")
    print("=" * 60 + "\n")

    await demonstrate_basic_pattern()
    await demonstrate_multiple_workers()
    await demonstrate_priority_queue()
    await demonstrate_task_processor()

    print("=" * 60)
    print("演示完成！")
    print("=" * 60)
    print()
    print("💡 要点总结：")
    print("1. asyncio.Queue 用于异步任务的生产-消费")
    print("2. 可以有多个生产者和多个消费者")
    print("3. PriorityQueue 支持按优先级处理")
    print("4. 使用 None 或特殊值作为结束信号")
    print("5. 适用于任务队列、数据流处理等场景")
    print()
    print("🚀 实战建议：")
    print("- 根据任务特点调整队列大小（maxsize）")
    print("- 使用多个消费者提高处理速度")
    print("- 妥善处理结束信号，避免死锁")


if __name__ == "__main__":
    asyncio.run(main())
