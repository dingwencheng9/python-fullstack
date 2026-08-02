"""L19 异步核心进阶 - 演示：Queue 生产者/消费者"""

from __future__ import annotations

import asyncio


async def demo_producer_consumer():
    """演示生产者-消费者模式（asyncio.Queue）"""
    print("\n" + "=" * 60)
    print("生产者-消费者模式（asyncio.Queue）")
    print("=" * 60)

    queue: asyncio.Queue[int | None] = asyncio.Queue(maxsize=3)

    async def producer(n: int) -> None:
        for i in range(n):
            await asyncio.sleep(0.1)
            await queue.put(i)
            print(f"  生产: {i}")
        # 两个消费者，需要两个停止信号
        await queue.put(None)
        await queue.put(None)

    async def consumer(name: str) -> None:
        while True:
            item = await queue.get()
            if item is None:
                queue.task_done()
                break
            await asyncio.sleep(0.2)
            print(f"  消费者 {name} 处理: {item}")
            queue.task_done()

    await asyncio.gather(
        producer(5),
        consumer("A"),
        consumer("B"),
    )
    print()


async def main() -> None:
    print("\n" + "=" * 60)
    print("L19: 异步核心进阶 - 演示")
    print("=" * 60)

    await demo_producer_consumer()

    print("=" * 60)
    print("演示完成")
    print("=" * 60)
    print()
    print("关键 API：")
    print("  asyncio.Queue.put()  - 放入数据")
    print("  asyncio.Queue.get()  - 取出数据")
    print("  asyncio.Queue.task_done()  - 通知完成")
    print("  asyncio.Queue.join()  - 等待清空")


if __name__ == "__main__":
    asyncio.run(main())
