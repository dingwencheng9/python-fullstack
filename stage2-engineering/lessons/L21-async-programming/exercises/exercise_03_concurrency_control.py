"""练习 3: as_completed / wait / TaskGroup.

学习目标：
- 使用 asyncio.as_completed 按完成顺序处理结果
- 使用 asyncio.wait 等待任务子集
- 使用 asyncio.TaskGroup 实现结构化并发
"""

from __future__ import annotations

import asyncio


# ============================================================
# as_completed：按完成顺序返回结果
# ============================================================


async def task(name: str, delay: float) -> str:
    """模拟任务。"""
    await asyncio.sleep(delay)
    return f"{name}-完成"


async def test_as_completed() -> None:
    """测试 as_completed 按完成顺序处理。"""
    print("=" * 60)
    print("练习 3: as_completed / wait / TaskGroup")
    print("=" * 60)
    print()

    tasks = [
        asyncio.create_task(task("慢", 2.0)),
        asyncio.create_task(task("快", 0.5)),
        asyncio.create_task(task("中", 1.0)),
    ]

    print("按完成顺序收集结果（as_completed）:")
    completion_order: list[str] = []
    for coro in asyncio.as_completed(tasks):
        result = await coro
        completion_order.append(result)
        print(f"  收到: {result}")

    # 快 -> 中 -> 慢
    expected = ["快-完成", "中-完成", "慢-完成"]
    assert completion_order == expected, f"期望 {expected}，得到 {completion_order}"
    print()
    print("✅ as_completed 测试通过")


# ============================================================
# wait：等待任务子集
# ============================================================


async def test_wait() -> None:
    """测试 wait 的超时行为。"""
    task_obj = asyncio.create_task(task("任务", 3.0))

    done, pending = await asyncio.wait([task_obj], timeout=1.0)

    assert task_obj in pending, "1秒后任务应仍在进行中"
    task_obj.cancel()
    await asyncio.gather(task_obj, return_exceptions=True)
    print("✅ wait 超时测试通过")


# ============================================================
# TaskGroup：结构化并发
# ============================================================


async def failing_task() -> None:
    """会抛出异常的任务。"""
    await asyncio.sleep(0.3)
    raise ValueError("模拟失败")


async def worker(n: int) -> str:
    """普通工作协程。"""
    await asyncio.sleep(0.5)
    return f"Worker-{n}"


async def test_taskgroup() -> None:
    """测试 TaskGroup 自动取消和异常收集。"""
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(failing_task())
            tg.create_task(worker(1))
            tg.create_task(worker(2))
    except* ValueError as eg:
        print(f"  捕获 ExceptionGroup：{len(eg.exceptions)} 个异常")
        for exc in eg.exceptions:
            print(f"    - {exc}")

    print("✅ TaskGroup 异常收集测试通过")


# ============================================================
# asyncio.timeout：超时上下文管理器
# ============================================================


async def slow_op() -> str:
    await asyncio.sleep(3.0)
    return "完成"


async def test_timeout() -> None:
    """测试 asyncio.timeout。"""
    try:
        async with asyncio.timeout(1.0):
            await slow_op()
    except asyncio.TimeoutError:
        print("✅ asyncio.timeout 超时测试通过")


# ============================================================
# 自检入口
# ============================================================


async def main() -> None:
    try:
        await test_as_completed()
        await test_wait()
        await test_taskgroup()
        await test_timeout()
    except Exception as exc:
        print(f"❌ 错误: {exc}")
        raise SystemExit(1) from exc

    print()
    print("🎉 练习 3 完成！")
    print("下一步: exercise_04_graceful_shutdown.py")


if __name__ == "__main__":
    asyncio.run(main())
