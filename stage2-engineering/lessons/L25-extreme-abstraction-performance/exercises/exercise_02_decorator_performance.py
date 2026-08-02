"""
练习 2: 装饰器性能优化

任务：
实现缓存装饰器并测量性能提升

要求：
1. 使用 PEP 695 泛型语法实现通用缓存装饰器
2. 支持过期时间 (TTL)
3. 测量缓存命中率和性能提升
4. 使用 functools.wraps 保留元数据
5. 通过 mypy --strict 检查

Python 3.14 线程安全考量：
- 缓存字典需要线程安全保护（使用 threading.Lock）
- time.time() 是线程安全的
- 在无 GIL 环境下，多线程同时访问缓存字典会导致竞态条件
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

# PEP 612: ParamSpec 用于保留函数签名
P = ParamSpec("P")
R = TypeVar("R")


# ============================================================================
# 原始版本（无缓存）
# ============================================================================


def fibonacci_slow(n: int) -> int:
    """慢速斐波那契（无缓存）"""
    if n <= 1:
        return n
    return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)


# ============================================================================
# TODO: 学生需要实现的部分
# ============================================================================


def simple_cache[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """
    简单缓存装饰器

    TODO: 实现以下功能
    1. 创建缓存字典 cache: dict[tuple, R] = {}
    2. 实现 wrapper 函数，检查缓存，命中则返回，否则计算并存储
    3. 使用 functools.wraps(func) 保留原函数元数据
    4. 支持可变参数 (*args, **kwargs)

    Python 3.14 注意：
        当前实现不是线程安全的！
        在无 GIL 环境下，需要使用 threading.Lock 保护 cache 字典
    """
    # TODO: 实现
    raise NotImplementedError("请实现 simple_cache 装饰器")


def ttl_cache[**P, R](ttl_seconds: float) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    带 TTL 的缓存装饰器

    TODO: 实现以下功能
    1. 创建缓存字典和过期时间字典
    2. 检查缓存是否过期
    3. 过期则重新计算并更新缓存
    4. 使用 functools.wraps 保留元数据

    参数:
        ttl_seconds: 缓存过期时间（秒）

    Python 3.14 注意：
        time.time() 是线程安全的
        但 cache 和 expiry 字典需要使用 threading.Lock 保护
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # TODO: 实现
        _ = (ttl_seconds, func)  # 使用参数避免 ruff 警告
        raise NotImplementedError("请实现 ttl_cache 装饰器")

    return decorator


# ============================================================================
# PEP 695 泛型版本
# ============================================================================


class CacheStats:
    """缓存统计"""

    def __init__(self) -> None:
        self.hits: int = 0
        self.misses: int = 0

    @property
    def hit_rate(self) -> float:
        """缓存命中率"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


def cache_with_stats[**P, R](func: Callable[P, R]) -> tuple[Callable[P, R], CacheStats]:
    """
    带统计的缓存装饰器（PEP 695 泛型语法）

    TODO: 实现以下功能
    1. 创建 CacheStats 实例
    2. 在 wrapper 中更新命中/未命中统计
    3. 返回 (wrapped_func, stats)

    Python 3.14 注意：
        stats.hits 和 stats.misses 的更新不是原子操作
        如果多线程同时调用，需要使用 threading.Lock 保护
    """
    # TODO: 实现
    raise NotImplementedError("请实现 cache_with_stats 装饰器")


# ============================================================================
# 测试代码
# ============================================================================


def test_simple_cache() -> None:
    """测试简单缓存"""
    print("测试简单缓存装饰器:\n")

    try:

        @simple_cache
        def fibonacci(n: int) -> int:
            if n <= 1:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        # 测试性能
        start = time.time()
        result1 = fibonacci(30)
        time1 = time.time() - start

        start = time.time()
        result2 = fibonacci(30)  # 第二次应该命中缓存
        time2 = time.time() - start

        print(f"第一次计算: fibonacci(30) = {result1}, 耗时: {time1:.4f}s")
        print(f"第二次计算: fibonacci(30) = {result2}, 耗时: {time2:.4f}s")
        print(f"性能提升: {time1 / time2:.0f}x")

        if time2 < 0.001:  # 缓存应该几乎瞬时返回
            print("✓ 缓存生效")
        else:
            print("✗ 缓存可能未生效")

    except NotImplementedError as e:
        print(f"✗ {e}")


def test_ttl_cache() -> None:
    """测试 TTL 缓存"""
    print("\n" + "=" * 60)
    print("测试 TTL 缓存装饰器")
    print("=" * 60)

    try:

        @ttl_cache(ttl_seconds=1.0)
        def get_timestamp() -> float:
            return time.time()

        # 第一次调用
        ts1 = get_timestamp()
        print(f"第一次调用: {ts1}")

        # 立即第二次调用（应该命中缓存）
        ts2 = get_timestamp()
        print(f"第二次调用: {ts2}")

        if ts1 == ts2:
            print("✓ 缓存命中（时间戳相同）")
        else:
            print("✗ 缓存未命中")

        # 等待过期
        print("等待 1.5 秒...")
        time.sleep(1.5)

        # 第三次调用（应该重新计算）
        ts3 = get_timestamp()
        print(f"第三次调用: {ts3}")

        if ts3 > ts1:
            print("✓ 缓存过期后重新计算")
        else:
            print("✗ 缓存未正确过期")

    except NotImplementedError as e:
        print(f"✗ {e}")


def test_cache_with_stats() -> None:
    """测试带统计的缓存"""
    print("\n" + "=" * 60)
    print("测试 PEP 695 泛型缓存（带统计）")
    print("=" * 60)

    try:

        def slow_function(n: int) -> int:
            time.sleep(0.1)
            return n * 2

        cached_func, stats = cache_with_stats(slow_function)

        # 调用 10 次，前 5 次不同参数，后 5 次重复
        for i in range(5):
            cached_func(i)

        for i in range(5):
            cached_func(i)  # 重复调用

        print("总调用: 10 次")
        print(f"缓存命中: {stats.hits} 次")
        print(f"缓存未命中: {stats.misses} 次")
        print(f"命中率: {stats.hit_rate:.1%}")

        if stats.hits == 5 and stats.misses == 5:
            print("✓ 统计正确")
        else:
            print("✗ 统计不正确")

    except NotImplementedError as e:
        print(f"✗ {e}")


if __name__ == "__main__":
    test_simple_cache()
    test_ttl_cache()
    test_cache_with_stats()
