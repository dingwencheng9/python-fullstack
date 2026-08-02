"""Semaphore 限流示例"""

import asyncio


async def bounded_worker(semaphore: asyncio.Semaphore, task_id: int):
    """带 Semaphore 限制的并发工作"""
    async with semaphore:
        print(f"任务 {task_id} 开始")
        await asyncio.sleep(0.5)
        print(f"任务 {task_id} 完成")
        return task_id


async def main():
    # 限制最多 3 个并发
    semaphore = asyncio.Semaphore(3)

    async with asyncio.TaskGroup() as tg:
        for i in range(10):
            tg.create_task(bounded_worker(semaphore, i))


if __name__ == "__main__":
    asyncio.run(main())
