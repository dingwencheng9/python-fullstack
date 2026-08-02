"""

from __future__ import annotations

Python 3.11+ TaskGroup 现代异步模式

本示例展示 Python 3.11 引入的 asyncio.TaskGroup 特性，
以及 Python 3.13 的改进和 Free-threading 考量。

Python 3.13+ 特性说明：
1. 改进的 REPL：更好的多行编辑和语法高亮
2. 更快的解释器：性能提升约 10-15%
3. PEP 703 Free-threading (3.13t)：可选的无 GIL 模式

作者: Python 3.13 全栈课程
日期: 2026-06-08
Python版本: 3.13+
"""

import asyncio
from collections.abc import Awaitable, Callable
import time

# ============================================
# 示例1: TaskGroup vs gather 对比
# ============================================


async def fetch_data_may_fail(
    url: str, should_fail: bool = False
) -> dict[str, str | int]:
    """
    模拟可能失败的数据获取

    Args:
        url: 数据源URL
        should_fail: 是否模拟失败

    Returns:
        响应数据字典
    """
    await asyncio.sleep(0.5)

    if should_fail:
        raise ValueError(f"获取失败: {url}")

    return {"url": url, "status": 200, "data": f"Data from {url}"}


async def demo_gather_error_handling() -> None:
    """演示 gather 的错误处理（传统方式）"""
    print("=" * 60)
    print("1. gather 错误处理（传统方式）")
    print("=" * 60)

    try:
        results = await asyncio.gather(
            fetch_data_may_fail("api-1", False),
            fetch_data_may_fail("api-2", True),  # 这个会失败
            fetch_data_may_fail("api-3", False),
        )
        print(f"成功: {len(results)} 个任务")
    except ValueError as e:
        print(f"❌ 捕获异常: {e}")
        print("⚠️  gather 默认：一个任务失败，整个 gather 抛出异常")

    print()


async def demo_taskgroup_error_handling() -> None:
    """演示 TaskGroup 的错误处理（Python 3.11+）"""
    print("=" * 60)
    print("2. TaskGroup 错误处理（Python 3.11+）")
    print("=" * 60)

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch_data_may_fail("api-1", False))
            tg.create_task(fetch_data_may_fail("api-2", True))  # 这个会失败
            tg.create_task(fetch_data_may_fail("api-3", False))
    except* ValueError as eg:
        print(f"❌ 捕获 ExceptionGroup: {len(eg.exceptions)} 个异常")
        for exc in eg.exceptions:
            print(f"   - {exc}")
        print("✅ TaskGroup: 使用 ExceptionGroup 收集所有异常")

    print()


# ============================================
# 示例2: TaskGroup 优雅的资源管理
# ============================================


async def process_item(item_id: int) -> int:
    """处理单个项目"""
    await asyncio.sleep(0.1)
    print(f"处理项目 {item_id}")
    return item_id * 2


async def demo_taskgroup_modern() -> list[int]:
    """
    使用 TaskGroup 并发处理（Python 3.11+）

    优势：
    1. 自动等待所有任务完成
    2. 自动取消未完成的任务（如果有异常）
    3. 使用 ExceptionGroup 收集所有异常
    4. 更符合结构化并发原则

    Free-threading（PEP 703/779）考量：
    由于 asyncio 基于单线程事件循环，即使在 3.13t 无 GIL 模式下，
    单个事件循环内的协程仍然是协作式调度，不会真正并行。
    若需真正并行，应考虑多个事件循环 + 多线程/多进程。
    """
    print("=" * 60)
    print("3. TaskGroup 现代并发模式")
    print("=" * 60)

    results: list[int] = []

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process_item(i)) for i in range(5)]

    # TaskGroup 退出时，所有任务已完成
    results = [task.result() for task in tasks]

    print(f"✅ 完成: {results}")
    print()

    return results


# ============================================
# 示例3: 使用 PEP 695 泛型语法
# ============================================


async def parallel_map[T, R](
    func: Callable[[T], R | Awaitable[R]],
    items: list[T],
) -> list[R]:
    """
    并发映射函数（使用 PEP 695 泛型语法）

    Python 3.13 特性：
    - 使用 [T, R] 语法声明泛型类型参数
    - 更简洁，无需 TypeVar

    Args:
        func: 映射函数（可以是同步或异步）
        items: 输入列表

    Returns:
        映射结果列表

    Free-threading（PEP 703/779）考量：
    如果 func 是 CPU 密集型纯同步函数，在 3.13t 下可能造成事件循环阻塞。
    建议使用 loop.run_in_executor() 将 CPU 密集型任务放到线程池。
    """
    async with asyncio.TaskGroup() as tg:
        tasks: list[asyncio.Task[R]] = []

        for item in items:
            if asyncio.iscoroutinefunction(func):
                task = tg.create_task(func(item))  # type: ignore
            else:
                # 同步函数包装为协程，使用闭包捕获 item
                async def _wrapper(captured_item: T = item) -> R:
                    return func(captured_item)  # type: ignore

                task = tg.create_task(_wrapper())

            tasks.append(task)

    return [task.result() for task in tasks]


async def demo_generic_parallel_map() -> None:
    """演示泛型并发映射"""
    print("=" * 60)
    print("4. PEP 695 泛型 + TaskGroup")
    print("=" * 60)

    async def square_async(x: int) -> int:
        await asyncio.sleep(0.05)
        return x * x

    numbers = [1, 2, 3, 4, 5]
    results = await parallel_map(square_async, numbers)

    print(f"输入: {numbers}")
    print(f"输出: {results}")
    print()


# ============================================
# 示例4: 超时和取消（现代方式）
# ============================================


async def long_running_task(task_id: int) -> int:
    """模拟长时间运行的任务"""
    print(f"任务 {task_id} 开始")
    try:
        await asyncio.sleep(10)  # 很长的延迟
    except asyncio.CancelledError:
        print(f"任务 {task_id} 被取消")
        raise
    else:
        print(f"任务 {task_id} 完成")
        return task_id


async def demo_timeout_modern() -> None:
    """
    使用 TaskGroup + asyncio.timeout 实现超时

    Python 3.11+ 特性：
    - asyncio.timeout() 上下文管理器
    - TaskGroup 自动取消未完成的任务
    """
    print("=" * 60)
    print("5. 现代超时控制")
    print("=" * 60)

    try:
        async with asyncio.timeout(2.0):
            async with asyncio.TaskGroup() as tg:
                tg.create_task(long_running_task(1))
                tg.create_task(long_running_task(2))
    except TimeoutError:
        print("❌ 超时：所有任务已自动取消")

    print()


# ============================================
# 示例5: 性能对比
# ============================================


async def benchmark_gather_vs_taskgroup() -> None:
    """对比 gather 和 TaskGroup 的性能"""
    print("=" * 60)
    print("6. 性能对比：gather vs TaskGroup")
    print("=" * 60)

    async def dummy_task() -> int:
        await asyncio.sleep(0.01)
        return 1

    n = 100

    # 测试 gather
    start = time.perf_counter()
    await asyncio.gather(*[dummy_task() for _ in range(n)])
    gather_time = time.perf_counter() - start

    # 测试 TaskGroup
    start = time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        for _ in range(n):
            tg.create_task(dummy_task())
    taskgroup_time = time.perf_counter() - start

    print(f"gather 耗时: {gather_time:.4f}秒")
    print(f"TaskGroup 耗时: {taskgroup_time:.4f}秒")
    print(f"性能差异: {abs(gather_time - taskgroup_time) / gather_time * 100:.1f}%")
    print()
    print("💡 结论：性能相近，但 TaskGroup 提供更好的错误处理和结构化并发")
    print()


# ============================================
# 主函数
# ============================================


async def main() -> None:
    """主函数"""
    print("\n" + "=" * 60)
    print("Python 3.11+ TaskGroup 现代异步模式")
    print("=" * 60 + "\n")

    await demo_gather_error_handling()
    await demo_taskgroup_error_handling()
    await demo_taskgroup_modern()
    await demo_generic_parallel_map()
    await demo_timeout_modern()
    await benchmark_gather_vs_taskgroup()

    print("=" * 60)
    print("演示完成！")
    print("=" * 60)
    print()
    print("💡 要点总结：")
    print("1. TaskGroup 提供结构化并发，自动管理任务生命周期")
    print("2. 使用 ExceptionGroup 收集所有异常，而非第一个异常")
    print("3. PEP 695 泛型语法更简洁（无需 TypeVar）")
    print("4. Python 3.11+ asyncio.timeout() 替代 wait_for")
    print("5. Python 3.14 无 GIL 模式下，asyncio 仍是协作式调度")
    print()
    print("🚀 Python 3.13+ 特性：")
    print("- 改进的 REPL：更好的多行编辑和语法高亮")
    print("- 更快的解释器：性能提升约 10-15%")
    print("- Free-threading (3.13t)：可选的无 GIL 模式")
    print("  注意：asyncio 事件循环仍在单线程运行，不会自动并行")


if __name__ == "__main__":
    asyncio.run(main())
