"""
L14: 并发编程 - async/await 练习解答

实现异步函数和并发任务。
"""

import asyncio


async def delay(seconds: float, value: str) -> str:
    """模拟异步延迟"""
    await asyncio.sleep(seconds)
    return value


async def gather_results() -> list[str]:
    """并发获取多个结果"""
    results = await asyncio.gather(
        delay(0.3, "A"),
        delay(0.2, "B"),
        delay(0.1, "C"),
    )
    return list(results)


async def sequential_results() -> list[str]:
    """顺序获取多个结果"""
    results = []
    for label in ["A", "B", "C"]:
        result = await delay(0.1, label)
        results.append(result)
    return results


async def with_timeout_coro() -> str:
    """超时处理练习"""
    try:
        result = await asyncio.wait_for(delay(5.0, "完成"), timeout=0.1)
        return result
    except TimeoutError:
        return "超时"


async def concurrent_tasks(tasks: list) -> list:
    """并发执行多个任务"""
    return await asyncio.gather(*tasks)


async def create_tasks() -> list[str]:
    """创建并等待多个任务"""

    async def task(name: str) -> str:
        await asyncio.sleep(0.1)
        return f"任务 {name} 完成"

    # 创建任务
    task1 = asyncio.create_task(task("A"))
    task2 = asyncio.create_task(task("B"))
    task3 = asyncio.create_task(task("C"))

    # 等待所有任务
    results = await asyncio.gather(task1, task2, task3)
    return list(results)
