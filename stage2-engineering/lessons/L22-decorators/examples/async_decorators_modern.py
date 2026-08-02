"""

from __future__ import annotations

异步装饰器与现代并发模式（Python 3.13）

展示 Python 3.11+ asyncio.TaskGroup 在装饰器中的应用
以及 Python 3.13 对异步代码的优化

Python 3.13 异步特性：
1. asyncio.TaskGroup (Python 3.11+) - 结构化并发
2. 改进的异步错误处理和堆栈跟踪
3. 更好的 asyncio 性能

作者: Python 3.13 全栈课程
日期: 2026-06-08
Python版本: 3.11+ (推荐 3.13)
"""

import asyncio
from collections.abc import Awaitable, Callable
import functools
import time

# ============================================
# 1. 异步计时装饰器
# ============================================


def async_timer(func: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
    """
    异步计时装饰器

    Python 3.13 优化：
    - 使用 time.perf_counter() 高精度计时
    - 保留异步函数的类型提示
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱️  {func.__name__} 耗时: {elapsed:.4f}s")
        return result

    return wrapper


# ============================================
# 2. 异步重试装饰器（使用 TaskGroup）
# ============================================


def async_retry(
    max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0
) -> Callable:
    """
    异步重试装饰器

    Python 3.11+ 特性：
    - 使用结构化的异步错误处理
    - 配合 TaskGroup 实现优雅的重试逻辑
    """

    def decorator(func: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️  尝试 {attempt}/{max_attempts} 失败: {e}")

                    if attempt < max_attempts:
                        print(f"⏳ {current_delay:.1f}秒后重试...")
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        print("❌ 所有重试均失败")
                        raise
            return None

        return wrapper

    return decorator


# ============================================
# 3. 使用 TaskGroup 的并发装饰器
# ============================================


def concurrent_map(max_concurrent: int = 5) -> Callable:
    """
    并发映射装饰器

    Python 3.11+ asyncio.TaskGroup 特性：
    - 结构化并发：所有任务在 TaskGroup 上下文中管理
    - 自动取消：任何任务失败会自动取消其他任务
    - 更好的错误处理：收集所有异常
    """

    def decorator(func: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
        @functools.wraps(func)
        async def wrapper(items: list):
            """
            并发处理列表中的所有项目

            Args:
                items: 要处理的项目列表

            Returns:
                处理结果列表
            """
            results = [None] * len(items)
            semaphore = asyncio.Semaphore(max_concurrent)

            async def process_item(index: int, item):
                async with semaphore:
                    results[index] = await func(item)

            # Python 3.11+ TaskGroup: 结构化并发
            async with asyncio.TaskGroup() as tg:
                for i, item in enumerate(items):
                    tg.create_task(process_item(i, item))

            return results

        return wrapper

    return decorator


# ============================================
# 4. 异步缓存装饰器
# ============================================


def async_cache(ttl: float | None = None) -> Callable:
    """
    异步缓存装饰器

    Python 3.13 现代类型提示：
    - 使用 float | None 而非 Optional[float]
    - 使用内置 dict 而非 typing.Dict
    """

    def decorator(func: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
        cache: dict[tuple, tuple[object, float]] = {}

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            # 检查缓存
            if key in cache:
                value, expire_time = cache[key]
                if ttl is None or now < expire_time:
                    print(f"💾 缓存命中: {func.__name__}{args}")
                    return value
                del cache[key]

            # 计算并缓存
            result = await func(*args, **kwargs)
            expire = now + ttl if ttl is not None else float("inf")
            cache[key] = (result, expire)
            return result

        wrapper.cache_clear = cache.clear
        return wrapper

    return decorator


# ============================================
# 示例函数
# ============================================


@async_timer
async def fetch_data(url: str) -> dict[str, str]:
    """模拟异步数据获取"""
    await asyncio.sleep(0.1)
    return {"url": url, "status": "ok"}


@async_retry(max_attempts=3, delay=0.5)
async def unreliable_api_call(success_rate: float) -> str:
    """模拟不稳定的 API 调用"""
    import random

    await asyncio.sleep(0.05)

    if random.random() > success_rate:
        raise ConnectionError("API 请求失败")

    return "Success"


@concurrent_map(max_concurrent=3)
async def process_item(item: int) -> int:
    """处理单个项目（模拟耗时操作）"""
    await asyncio.sleep(0.1)
    print(f"  处理项目: {item}")
    return item * 2


@async_cache(ttl=2.0)
async def expensive_calculation(x: int) -> int:
    """模拟昂贵的异步计算"""
    print(f"  🔄 执行计算: {x}")
    await asyncio.sleep(0.2)
    return x**2


# ============================================
# 演示：使用 TaskGroup 进行结构化并发
# ============================================


async def demo_basic_async_decorators():
    """演示基础异步装饰器"""
    print("\n" + "=" * 60)
    print("1. 异步计时装饰器")
    print("=" * 60)

    result = await fetch_data("https://api.example.com/data")
    print(f"结果: {result}\n")


async def demo_async_retry():
    """演示异步重试装饰器"""
    print("=" * 60)
    print("2. 异步重试装饰器")
    print("=" * 60)

    try:
        result = await unreliable_api_call(success_rate=0.3)
        print(f"✅ API 调用成功: {result}\n")
    except ConnectionError as e:
        print(f"❌ API 调用最终失败: {e}\n")


async def demo_concurrent_processing():
    """演示使用 TaskGroup 的并发处理"""
    print("=" * 60)
    print("3. TaskGroup 并发处理 (Python 3.11+)")
    print("=" * 60)

    items = list(range(1, 11))
    print(f"处理 {len(items)} 个项目（最多 3 个并发）...")

    start = time.perf_counter()
    results = await process_item(items)
    elapsed = time.perf_counter() - start

    print(f"结果: {results}")
    print(f"总耗时: {elapsed:.2f}s")
    print(f"平均每项: {elapsed / len(items):.3f}s\n")


async def demo_async_cache():
    """演示异步缓存装饰器"""
    print("=" * 60)
    print("4. 异步缓存装饰器")
    print("=" * 60)

    # 第一次调用（计算）
    result1 = await expensive_calculation(5)
    print(f"第一次结果: {result1}")

    # 第二次调用（缓存命中）
    result2 = await expensive_calculation(5)
    print(f"第二次结果: {result2}")

    # 等待缓存过期
    print("⏳ 等待 2.5 秒（缓存将过期）...")
    await asyncio.sleep(2.5)

    # 第三次调用（缓存过期，重新计算）
    result3 = await expensive_calculation(5)
    print(f"第三次结果: {result3}\n")


async def demo_taskgroup_error_handling():
    """演示 TaskGroup 的错误处理"""
    print("=" * 60)
    print("5. TaskGroup 错误处理与自动取消")
    print("=" * 60)

    async def task_success(n: int) -> str:
        await asyncio.sleep(0.5)
        return f"Task {n} 成功"

    async def task_failure(n: int) -> str:
        await asyncio.sleep(0.2)
        raise ValueError(f"Task {n} 失败")

    try:
        async with asyncio.TaskGroup() as tg:
            # 创建多个任务
            tg.create_task(task_success(1))
            tg.create_task(task_failure(2))  # 这个会失败
            tg.create_task(task_success(3))

        print("所有任务完成")
    except* ValueError as eg:
        print(f"⚠️  捕获到异常组: {len(eg.exceptions)} 个异常")
        for e in eg.exceptions:
            print(f"  - {e}")
    print()


# ============================================
# 主函数
# ============================================


async def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  Python 3.13 异步装饰器与现代并发")
    print("=" * 60)
    print("\n🚀 使用 asyncio.TaskGroup 实现结构化并发")
    print("   运行环境: Python 3.11+ (推荐 3.13)\n")

    await demo_basic_async_decorators()
    await demo_async_retry()
    await demo_concurrent_processing()
    await demo_async_cache()
    await demo_taskgroup_error_handling()

    print("=" * 60)
    print("  演示完成")
    print("=" * 60)
    print("\n💡 Python 3.11+ asyncio.TaskGroup 优势:")
    print("  1. 结构化并发：所有任务在上下文中管理")
    print("  2. 自动取消：一个任务失败会取消其他任务")
    print("  3. 异常组：使用 except* 捕获多个异常")
    print("  4. 更好的资源清理和错误跟踪")
    print()


if __name__ == "__main__":
    asyncio.run(main())
