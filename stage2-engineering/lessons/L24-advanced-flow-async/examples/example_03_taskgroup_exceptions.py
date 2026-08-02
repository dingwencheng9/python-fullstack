"""示例 3: TaskGroup 和异常处理

展示：
- TaskGroup vs gather 对比
- except* 异常组处理
- 结构化并发
- 错误恢复策略
"""

from __future__ import annotations

import asyncio
import random
from collections.abc import AsyncGenerator
from dataclasses import dataclass

# ============================================================================
# gather vs TaskGroup 对比
# ============================================================================


async def task_success(task_id: int) -> str:
    """成功的任务"""
    await asyncio.sleep(0.1)
    return f"Task-{task_id} 成功"


async def task_failure(task_id: int) -> str:
    """失败的任务"""
    await asyncio.sleep(0.1)
    raise ValueError(f"Task-{task_id} 失败")


async def demo_gather_vs_taskgroup() -> None:
    """对比 gather 和 TaskGroup"""
    print("=== gather vs TaskGroup 对比 ===\n")

    # 1. gather - 只捕获第一个异常
    print("1. gather (旧模式):")
    try:
        results = await asyncio.gather(
            task_success(1),
            task_failure(2),
            task_failure(3),
            task_success(4),
        )
        print(f"   结果: {results}")
    except ValueError as e:
        print(f"   ✗ 捕获到异常: {e}")
        print("   ⚠️ 只能捕获第一个异常，其他异常丢失")

    print()

    # 2. TaskGroup - 捕获所有异常
    print("2. TaskGroup (现代模式):")
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task_success(1))
            tg.create_task(task_failure(2))
            tg.create_task(task_failure(3))
            tg.create_task(task_success(4))
    except* ValueError as eg:
        print(f"   ✗ 捕获到 {len(eg.exceptions)} 个 ValueError:")
        for exc in eg.exceptions:
            print(f"      - {exc}")

    print()


# ============================================================================
# 异常组处理 (except*)
# ============================================================================


async def risky_task(task_id: int) -> str:
    """可能失败的任务"""
    await asyncio.sleep(0.1)

    if task_id % 3 == 0:
        raise ValueError(f"Task-{task_id}: 值错误")
    elif task_id % 5 == 0:
        raise TypeError(f"Task-{task_id}: 类型错误")
    elif task_id % 7 == 0:
        raise RuntimeError(f"Task-{task_id}: 运行时错误")

    return f"Task-{task_id} 成功"


@dataclass
class TaskResult:
    """任务结果"""

    task_id: int
    success: bool
    data: str | None = None
    error: str | None = None


async def demo_exception_groups() -> None:
    """演示异常组处理"""
    print("=== 异常组处理 (except*) ===\n")

    results: list[TaskResult] = []
    task_ids = list(range(1, 16))  # 1-15

    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(risky_task(i)) for i in task_ids]

        # 所有任务成功
        for i, task in enumerate(tasks):
            results.append(
                TaskResult(
                    task_id=task_ids[i],
                    success=True,
                    data=task.result(),
                )
            )

    except* ValueError as eg:
        print(f"捕获 {len(eg.exceptions)} 个 ValueError:")
        for exc in eg.exceptions:
            task_id = int(str(exc).split("-")[1].split(":")[0])
            results.append(TaskResult(task_id, False, error=str(exc)))
            print(f"  - {exc}")

    except* TypeError as eg:
        print(f"\n捕获 {len(eg.exceptions)} 个 TypeError:")
        for exc in eg.exceptions:
            task_id = int(str(exc).split("-")[1].split(":")[0])
            results.append(TaskResult(task_id, False, error=str(exc)))
            print(f"  - {exc}")

    except* RuntimeError as eg:
        print(f"\n捕获 {len(eg.exceptions)} 个 RuntimeError:")
        for exc in eg.exceptions:
            task_id = int(str(exc).split("-")[1].split(":")[0])
            results.append(TaskResult(task_id, False, error=str(exc)))
            print(f"  - {exc}")

    # 统计
    success_count = sum(1 for r in results if r.success)
    print("\n统计:")
    print(f"  成功: {success_count}/{len(task_ids)}")
    print(f"  失败: {len(results) - success_count}/{len(task_ids)}")

    print()


# ============================================================================
# 限流 + TaskGroup
# ============================================================================


async def fetch_url(url: str, semaphore: asyncio.Semaphore) -> dict[str, object]:
    """限流的 URL 请求"""
    async with semaphore:
        print(f"  → 请求: {url}")
        await asyncio.sleep(random.uniform(0.1, 0.3))
        return {"url": url, "status": 200}


async def demo_semaphore_taskgroup() -> None:
    """演示 Semaphore + TaskGroup"""
    print("=== Semaphore + TaskGroup ===\n")

    urls = [f"https://example.com/page{i}" for i in range(10)]
    max_concurrent = 3

    print(f"请求 {len(urls)} 个 URL，最大并发: {max_concurrent}\n")

    semaphore = asyncio.Semaphore(max_concurrent)

    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_url(url, semaphore)) for url in urls]

        # 收集结果
        results = [task.result() for task in tasks]
        print(f"\n✓ 成功: {len(results)}/{len(urls)}")

    except* Exception as eg:
        print(f"\n✗ 错误: {len(eg.exceptions)} 个")

    print()


# ============================================================================
# 动态任务创建
# ============================================================================


async def worker(
    task_id: int,
    queue: asyncio.Queue[int],
) -> None:
    """工作任务"""
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=1.0)
            print(f"  Worker-{task_id} 处理: {item}")
            await asyncio.sleep(0.1)
            queue.task_done()
        except TimeoutError:
            break


async def demo_dynamic_tasks() -> None:
    """演示动态任务创建"""
    print("=== 动态任务创建 ===\n")

    queue: asyncio.Queue[int] = asyncio.Queue()

    # 添加任务
    for i in range(10):
        await queue.put(i)

    print("启动 3 个工作线程:\n")

    try:
        async with asyncio.TaskGroup() as tg:
            # 动态创建工作任务
            for i in range(3):
                tg.create_task(worker(i, queue))

        print("\n✓ 所有任务完成")

    except* TimeoutError:
        print("\n✓ 工作线程超时退出")

    print()


# ============================================================================
# 级联取消
# ============================================================================


async def long_running_task(task_id: int) -> str:
    """长时间运行的任务"""
    try:
        print(f"  Task-{task_id} 开始")
        await asyncio.sleep(10)
        print(f"  Task-{task_id} 完成")
        return f"Task-{task_id} 结果"
    except asyncio.CancelledError:
        print(f"  Task-{task_id} 被取消")
        raise


async def trigger_failure(delay: float) -> None:
    """触发失败的任务"""
    await asyncio.sleep(delay)
    raise ValueError("触发失败")


async def demo_cascading_cancel() -> None:
    """演示级联取消"""
    print("=== 级联取消 ===\n")

    print("启动 3 个长时间任务，0.5s 后触发失败:\n")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(long_running_task(1))
            tg.create_task(long_running_task(2))
            tg.create_task(long_running_task(3))
            tg.create_task(trigger_failure(0.5))

    except* ValueError as eg:
        print(f"\n✗ 捕获 ValueError: {eg.exceptions[0]}")
        print("✓ TaskGroup 自动取消了所有其他任务")

    print()


# ============================================================================
# 实战：批量处理管道
# ============================================================================


async def process_item(item: int) -> int:
    """处理单个项目"""
    await asyncio.sleep(0.1)
    if item % 10 == 0:
        raise ValueError(f"Item {item} 处理失败")
    return item * 2


async def batch_pipeline(
    items: list[int],
    batch_size: int = 5,
) -> AsyncGenerator[list[int]]:
    """批量处理管道"""
    for i in range(0, len(items), batch_size):
        batch = items[i : i + batch_size]
        results: list[int] = []

        try:
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(process_item(item)) for item in batch]

            # 批量成功
            results = [task.result() for task in tasks]

        except* ValueError as eg:
            print(f"  ⚠️ 批次 {i // batch_size + 1} 有 {len(eg.exceptions)} 个错误")
            # 继续处理（容错）

        if results:
            yield results


async def demo_batch_pipeline() -> None:
    """演示批量处理管道"""
    print("=== 批量处理管道 ===\n")

    items = list(range(1, 26))  # 1-25
    total = 0

    print(f"处理 {len(items)} 个项目，批量大小: 5\n")

    async for batch_results in batch_pipeline(items, batch_size=5):
        total += len(batch_results)
        print(f"  ✓ 批次完成: {len(batch_results)} 个结果")

    print(f"\n总计处理: {total}/{len(items)}")

    print()


# ============================================================================
# 主程序
# ============================================================================


async def main() -> None:
    """运行所有示例"""
    await demo_gather_vs_taskgroup()
    await demo_exception_groups()
    await demo_semaphore_taskgroup()
    await demo_dynamic_tasks()
    await demo_cascading_cancel()
    await demo_batch_pipeline()


if __name__ == "__main__":
    asyncio.run(main())
