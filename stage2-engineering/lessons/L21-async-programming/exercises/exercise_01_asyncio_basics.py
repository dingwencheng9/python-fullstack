"""练习 1: asyncio.Queue — 生产者/消费者模式.

学习目标：
- 掌握 asyncio.Queue 的 put/get/task_done/join 用法
- 实现多生产者、多消费者的任务分发
"""

from __future__ import annotations

import asyncio


async def producer(queue: asyncio.Queue[int], producer_id: int, count: int) -> None:
    """生产者：将数据放入队列。"""
    for i in range(count):
        await asyncio.sleep(0.1)
        item = producer_id * 100 + i
        await queue.put(item)
        print(f"  [P{producer_id}] 生产: {item}")


async def consumer(queue: asyncio.Queue[int | None], consumer_id: int) -> None:
    """消费者：从队列取数据并处理。"""
    processed = 0
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        await asyncio.sleep(0.2)
        print(f"  [C{consumer_id}] 处理: {item}")
        processed += 1
        queue.task_done()
    print(f"  [C{consumer_id}] 完成，共处理 {processed} 个")


async def run_producer_consumer(
    num_producers: int,
    num_consumers: int,
    items_per_producer: int,
) -> int:
    """运行多生产者/多消费者。返回总处理数量。"""
    queue: asyncio.Queue[int | None] = asyncio.Queue(maxsize=5)

    # 启动消费者（先启动，确保它们在等待）
    consumer_tasks = [
        asyncio.create_task(consumer(queue, i)) for i in range(num_consumers)
    ]

    # 启动生产者
    producer_tasks = [
        asyncio.create_task(producer(queue, i, items_per_producer))
        for i in range(num_producers)
    ]

    # 等待所有生产者完成
    await asyncio.gather(*producer_tasks)

    # 发送结束信号（每个消费者一个）
    for _ in range(num_consumers):
        await queue.put(None)

    # 等待所有消费者完成
    await asyncio.gather(*consumer_tasks)

    return num_producers * items_per_producer


# ============================================================
# 自检测试
# ============================================================


async def test_producer_consumer() -> None:
    """测试生产者/消费者模式。"""
    print("=" * 60)
    print("练习 1: asyncio.Queue 生产者/消费者")
    print("=" * 60)
    print()

    total = await run_producer_consumer(
        num_producers=2,
        num_consumers=3,
        items_per_producer=5,
    )

    print()
    print(f"✅ 总生产数量: {total}")
    print("   关键 API: put / get / task_done / join")


async def main() -> None:
    try:
        await test_producer_consumer()
    except Exception as exc:
        print(f"❌ 错误: {exc}")
        raise SystemExit(1) from exc

    print()
    print("🎉 练习 1 完成！")
    print("下一步: exercise_02_event_condition.py")


if __name__ == "__main__":
    asyncio.run(main())
