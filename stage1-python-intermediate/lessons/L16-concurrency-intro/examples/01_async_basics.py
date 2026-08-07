"""L16: 并发编程 - async/await 基础"""

import asyncio
import time

# === Part 1: 协程基础 ===


async def say_hello():
    """异步问候函数"""
    print("Hello!")
    await asyncio.sleep(0.1)  # 模拟异步操作
    print("World!")


# 运行协程
async def main():
    await say_hello()


asyncio.run(main())

# === Part 2: asyncio.gather 并发执行 ===


async def fetch_data(name: str, delay: float) -> str:
    """模拟数据获取"""
    print(f"[{name}] 开始获取数据...")
    await asyncio.sleep(delay)
    print(f"[{name}] 完成")
    return f"数据 from {name}"


async def main_gather():
    """并发获取多个数据源"""
    start = time.perf_counter()

    # 并发执行三个任务
    results = await asyncio.gather(
        fetch_data("API", 0.5),
        fetch_data("数据库", 0.3),
        fetch_data("缓存", 0.2),
    )

    elapsed = time.perf_counter() - start
    print(f"\n全部完成，耗时: {elapsed:.2f}秒")
    print(f"结果: {results}")


asyncio.run(main_gather())

# === Part 3: Task 创建与取消 ===


async def long_task(n: int) -> str:
    """长时间运行的任务"""
    for i in range(n):
        print(f"任务 {n}: 第 {i + 1} 步")
        await asyncio.sleep(0.1)
    return f"任务 {n} 完成"


async def task_demo():
    """任务管理示例"""
    # 创建任务
    task1 = asyncio.create_task(long_task(3))
    task2 = asyncio.create_task(long_task(5))

    print("任务已创建，等待完成...")

    # 等待所有任务
    results = await asyncio.gather(task1, task2)
    print(f"结果: {results}")


asyncio.run(task_demo())

# === Part 4: 超时处理 ===


async def with_timeout():
    """超时处理示例"""
    try:
        await asyncio.wait_for(asyncio.sleep(2), timeout=0.5)
    except TimeoutError:
        print("操作超时!")


asyncio.run(with_timeout())

# === Part 5: 串行 vs 并发对比 ===


async def sequential():
    """串行执行"""
    start = time.perf_counter()
    await fetch_data("A", 0.5)
    await fetch_data("B", 0.5)
    await fetch_data("C", 0.5)
    return time.perf_counter() - start


async def concurrent():
    """并发执行"""
    start = time.perf_counter()
    await asyncio.gather(
        fetch_data("A", 0.5),
        fetch_data("B", 0.5),
        fetch_data("C", 0.5),
    )
    return time.perf_counter() - start


async def compare():
    """对比串行和并发"""
    seq_time = await sequential()
    print(f"\n串行耗时: {seq_time:.2f}秒")

    con_time = await concurrent()
    print(f"并发耗时: {con_time:.2f}秒")
    print(f"加速比: {seq_time / con_time:.1f}x")


asyncio.run(compare())

# === Part 6: 错误处理 ===


async def might_fail(task_id: int) -> str:
    """可能失败的任务"""
    await asyncio.sleep(0.1)
    if task_id == 2:
        raise ValueError(f"任务 {task_id} 失败!")
    return f"任务 {task_id} 成功"


async def error_handling():
    """错误处理示例"""
    results = await asyncio.gather(
        might_fail(1),
        might_fail(2),
        might_fail(3),
        return_exceptions=True,  # 捕获异常而不中断
    )

    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"任务 {i}: 错误 - {result}")
        else:
            print(f"任务 {i}: {result}")


asyncio.run(error_handling())

print("\n=== async/await 基础示例完成 ===")
