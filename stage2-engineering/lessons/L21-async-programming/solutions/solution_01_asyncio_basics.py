"""

from __future__ import annotations

练习 1: asyncio 基础 - 参考答案

===============================================================================
解题思路 (Solution Strategy)
===============================================================================

本练习涵盖 Python 异步编程的核心概念，从协程创建到并发执行。

核心知识点：
1. 协程定义与执行 (async def, await)
2. asyncio.sleep() vs time.sleep()
3. asyncio.gather() 并发执行
4. asyncio.create_task() 创建后台任务
5. 事件循环的调度机制

实现要点：
- async def 声明协程函数
- await 关键字等待异步操作
- asyncio.gather() 收集多个协程的结果
- asyncio.create_task() 立即启动协程
- time.time() 测量性能差异

为什么使用异步？
- I/O 密集型任务：网络请求、文件读写、数据库查询
- 并发非并行：单线程中交替执行多个任务
- 避免阻塞：当一个任务等待时，其他任务可继续执行

【解题思路】
本练习的完整实现展示了以下核心概念和技术要点：

1. **问题分析**：
   - 理解练习要求和核心目标
   - 识别关键技术点和实现难点
   - 确定合适的数据结构和算法

2. **实现策略**：
   - 采用模块化设计，每个函数/类职责单一
   - 使用 Python 3.13 类型提示增强代码可读性
   - 遵循 PEP 8 编码规范和最佳实践

3. **关键技术点**：
   - 正确使用语言特性（类型系统/异步/装饰器等）
   - 处理边界条件和异常情况
   - 编写清晰的文档字符串和注释

4. **测试验证**：
   - 覆盖正常流程和异常情况
   - 使用 pytest 进行单元测试
   - 确保代码质量和可维护性

【学习建议】：
- 先理解问题需求，再查看实现代码
- 对比自己的实现，找出差距和改进点
- 运行代码并修改参数，观察行为变化
- 尝试扩展功能，加深理解

===============================================================================
"""

import asyncio
import time

# ============================================================================
# 任务 1: 创建和执行协程
# ============================================================================


async def greet(name: str) -> str:
    """
    简单的异步问候函数

    关键点：
    - async def 声明协程函数
    - await asyncio.sleep() 非阻塞等待
    - 协程必须用 await 或 asyncio.run() 调用

    为什么用 asyncio.sleep 而非 time.sleep？
    - time.sleep 会阻塞整个线程
    - asyncio.sleep 只挂起当前协程，允许其他协程运行
    """
    await asyncio.sleep(0.5)  # 模拟异步 I/O 操作
    return f"Hello, {name}!"


# ============================================================================
# 任务 2: 并发执行多个协程
# ============================================================================


async def fetch_data(source: str, delay: float) -> dict[str, object]:
    """
    模拟从数据源获取数据

    设计模式：
    - 打印开始/完成消息，观察并发行为
    - 返回字典而非简单字符串，模拟真实 API 响应

    注意事项：
    - 多个 fetch_data 协程会交错执行
    - 不是按调用顺序完成，而是按 delay 时间
    """
    print(f"开始获取 {source}")
    await asyncio.sleep(delay)  # 模拟网络延迟
    print(f"完成获取 {source}")
    return {"source": source, "data": f"Data from {source}"}


async def fetch_all_parallel() -> list[dict[str, object]]:
    """
    并发获取多个数据源的数据

    asyncio.gather() 的工作原理：
    1. 立即启动所有协程
    2. 等待所有协程完成
    3. 返回结果列表（按传入顺序）

    性能分析：
    - 串行执行：1.0 + 0.5 + 1.5 = 3.0 秒
    - 并发执行：max(1.0, 0.5, 1.5) = 1.5 秒
    - 加速比：2x

    为什么不用 asyncio.create_task？
    - gather 更简洁，适合"全部完成后继续"的场景
    - create_task 更灵活，适合需要单独控制任务的场景
    """
    results = await asyncio.gather(
        fetch_data("API-1", 1.0),
        fetch_data("API-2", 0.5),
        fetch_data("API-3", 1.5),
    )
    return results


# ============================================================================
# 任务 3: 使用 Task 对象
# ============================================================================


async def background_counter(name: str, count: int) -> int:
    """
    后台计数器

    用途：
    - 模拟长时间运行的后台任务
    - 展示任务的独立执行

    观察点：
    - 两个计数器会交错打印
    - 不是 Counter-1 全部完成后才执行 Counter-2
    """
    for i in range(count):
        print(f"{name}: {i}")
        await asyncio.sleep(0.1)
    return count


async def create_tasks_example() -> tuple[int, int]:
    """
    创建并管理多个后台任务

    asyncio.create_task() vs await 直接调用：

    错误示例（串行执行）：
        result1 = await background_counter("Counter-1", 5)
        result2 = await background_counter("Counter-2", 3)
        # Counter-2 要等 Counter-1 完成后才开始

    正确示例（并发执行）：
        task1 = asyncio.create_task(background_counter("Counter-1", 5))
        task2 = asyncio.create_task(background_counter("Counter-2", 3))
        result1 = await task1
        result2 = await task2
        # 两个计数器同时运行

    关键点：
    - create_task 立即启动协程，不等待完成
    - 可以在等待任务前做其他工作
    - 必须 await task 来获取结果
    """
    # 创建任务（立即开始执行）
    task1 = asyncio.create_task(background_counter("Counter-1", 5))
    task2 = asyncio.create_task(background_counter("Counter-2", 3))

    # 主任务可以继续执行其他工作
    print("主任务继续执行")
    await asyncio.sleep(0.2)

    # 等待所有任务完成
    result1 = await task1
    result2 = await task2

    return result1, result2


# ============================================================================
# 任务 4: 测量性能对比
# ============================================================================


def sync_sleep(n: int) -> None:
    """
    同步版本 - 串行执行

    问题：
    - time.sleep 阻塞整个线程
    - 无法利用等待时间做其他工作
    - 总耗时 = n * 0.5 秒
    """
    for i in range(n):
        time.sleep(0.5)


async def async_sleep(n: int) -> None:
    """
    异步版本 - 并发执行

    优势：
    - 所有 sleep 同时开始
    - 事件循环在等待期间可处理其他任务
    - 总耗时 ≈ 0.5 秒（无论 n 多大）

    实现技巧：
    - 列表推导式创建多个协程
    - *tasks 展开列表传给 gather
    """
    tasks = [asyncio.sleep(0.5) for _ in range(n)]
    await asyncio.gather(*tasks)


async def performance_comparison() -> tuple[float, float]:
    """
    对比同步和异步的性能

    测量方法：
    - time.time() 获取当前时间戳
    - 执行操作前后相减得到耗时

    预期结果：
    - 同步耗时：约 2.5 秒（5 * 0.5）
    - 异步耗时：约 0.5 秒（max(0.5, 0.5, ...））
    - 加速比：5x

    注意事项：
    - 在异步函数中调用同步阻塞函数
    - 会阻塞整个事件循环
    - 这里仅用于演示对比
    """
    # 测量同步版本
    start = time.time()
    sync_sleep(5)
    sync_time = time.time() - start

    # 测量异步版本
    start = time.time()
    await async_sleep(5)
    async_time = time.time() - start

    return sync_time, async_time


# ============================================================================
# 测试代码
# ============================================================================


async def test_greet() -> None:
    """测试问候函数"""
    result = await greet("World")
    assert result == "Hello, World!", f"期望 'Hello, World!'，得到 '{result}'"
    print("✅ greet 测试通过")


async def test_fetch_all_parallel() -> None:
    """测试并发获取数据"""
    start = time.time()
    results = await fetch_all_parallel()
    elapsed = time.time() - start

    assert len(results) == 3, f"期望 3 个结果，得到 {len(results)}"
    assert elapsed < 2.0, f"并发执行应该在 2 秒内完成，实际耗时 {elapsed:.2f}秒"
    print(f"✅ fetch_all_parallel 测试通过 (耗时: {elapsed:.2f}秒)")


async def test_create_tasks() -> None:
    """测试创建任务"""
    result1, result2 = await create_tasks_example()
    assert result1 == 5, f"期望 Counter-1 返回 5，得到 {result1}"
    assert result2 == 3, f"期望 Counter-2 返回 3，得到 {result2}"
    print("✅ create_tasks 测试通过")


async def test_performance() -> None:
    """测试性能对比"""
    sync_time, async_time = await performance_comparison()
    print(f"   同步耗时: {sync_time:.2f}秒")
    print(f"   异步耗时: {async_time:.2f}秒")
    print(f"   加速比: {sync_time / async_time:.2f}x")

    assert async_time < sync_time * 0.5, "异步版本应该快得多"
    print("✅ performance 测试通过")


async def main() -> None:
    """运行所有测试"""
    print("=" * 60)
    print("练习 1: asyncio 基础 - 参考答案")
    print("=" * 60)
    print()

    try:
        await test_greet()
        print()

        await test_fetch_all_parallel()
        print()

        await test_create_tasks()
        print()

        await test_performance()
        print()

        print("=" * 60)
        print("🎉 所有测试通过！")
        print("=" * 60)
        print()
        print("知识回顾：")
        print("1. async def 声明协程函数")
        print("2. await 等待异步操作完成")
        print("3. asyncio.gather() 并发执行多个协程")
        print("4. asyncio.create_task() 立即启动后台任务")
        print("5. asyncio.sleep() vs time.sleep()")
        print()
        print("下一步：")
        print("1. 理解事件循环如何调度协程")
        print(
            "2. 继续练习 2: uv run python stage2-engineering/lessons/L19-async-programming/exercises/exercise_02_async_await.py"
        )

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())
