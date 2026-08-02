"""
解答 2: 装饰器性能优化

完整实现所有练习要求
"""

from __future__ import annotations

import functools
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
# 解答：简单缓存装饰器
# ============================================================================


def simple_cache[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """
    简单缓存装饰器

    实现要点：
    1. 使用字典存储缓存
    2. 将参数转换为可哈希的 key
    3. 使用 functools.wraps 保留元数据

    Python 3.14 线程安全分析：
        cache 字典在多线程环境下不安全
        多个线程同时调用会导致竞态条件
        生产环境需要使用 threading.Lock 保护
    """
    cache: dict[tuple[object, ...], R] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # 将参数转换为可哈希的 key
        key = (args, tuple(sorted(kwargs.items())))

        if key in cache:
            return cache[key]

        # 计算结果并缓存
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


# ============================================================================
# 解答：带 TTL 的缓存装饰器
# ============================================================================


def ttl_cache(ttl_seconds: float) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    带 TTL 的缓存装饰器

    实现要点：
    1. 存储缓存值和过期时间
    2. 检查缓存是否过期
    3. 过期则重新计算

    Python 3.14 线程安全分析：
        time.time() 是线程安全的
        但 cache 和 expiry 字典需要使用 threading.Lock 保护
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache: dict[tuple[object, ...], R] = {}
        expiry: dict[tuple[object, ...], float] = {}

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = (args, tuple(sorted(kwargs.items())))
            current_time = time.time()

            # 检查缓存是否存在且未过期
            if key in cache and key in expiry and current_time < expiry[key]:
                return cache[key]

            # 计算结果并缓存
            result = func(*args, **kwargs)
            cache[key] = result
            expiry[key] = current_time + ttl_seconds
            return result

        return wrapper

    return decorator


# ============================================================================
# 解答：PEP 695 泛型版本（带统计）
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

    def __repr__(self) -> str:
        return f"CacheStats(hits={self.hits}, misses={self.misses}, hit_rate={self.hit_rate:.1%})"


def cache_with_stats[**P, R](
    func: Callable[P, R],
) -> tuple[Callable[P, R], CacheStats]:
    """
    带统计的缓存装饰器（PEP 695 泛型语法）

    展示特性：
    1. PEP 695: [**P, R] 声明泛型参数
    2. 返回 (wrapped_func, stats) 元组
    3. 统计缓存命中率

    Python 3.14 线程安全分析：
        stats.hits 和 stats.misses 的更新不是原子操作
        多线程同时调用时需要使用 threading.Lock 保护
    """
    cache: dict[tuple[object, ...], R] = {}
    stats = CacheStats()

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = (args, tuple(sorted(kwargs.items())))

        if key in cache:
            stats.hits += 1
            return cache[key]

        stats.misses += 1
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper, stats


# ============================================================================
# 高级：LRU 缓存（限制大小）
# ============================================================================


def lru_cache_custom(maxsize: int = 128) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    LRU 缓存装饰器（最近最少使用）

    实现要点：
    1. 限制缓存大小
    2. 淘汰最久未使用的条目
    3. 使用 OrderedDict 维护访问顺序

    注意：生产环境建议使用 functools.lru_cache
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        from collections import OrderedDict

        cache: OrderedDict[tuple[object, ...], R] = OrderedDict()

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = (args, tuple(sorted(kwargs.items())))

            if key in cache:
                # 移动到末尾（标记为最近使用）
                cache.move_to_end(key)
                return cache[key]

            # 计算结果
            result = func(*args, **kwargs)

            # 添加到缓存
            cache[key] = result
            cache.move_to_end(key)

            # 检查大小限制
            if len(cache) > maxsize:
                cache.popitem(last=False)  # 移除最旧的

            return result

        return wrapper

    return decorator


# ============================================================================
# 测试代码
# ============================================================================


def test_simple_cache() -> None:
    """测试简单缓存"""
    print("测试简单缓存装饰器:\n")

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
    speedup = time1 / max(time2, 1e-12)
    print(f"性能提升: {speedup:.0f}x")

    if time2 < 0.001:  # 缓存应该几乎瞬时返回
        print("✓ 缓存生效")
    else:
        print("⚠️ 缓存可能未生效")


def test_ttl_cache() -> None:
    """测试 TTL 缓存"""
    print("\n" + "=" * 60)
    print("测试 TTL 缓存装饰器")
    print("=" * 60)

    @ttl_cache(ttl_seconds=1.0)
    def get_timestamp() -> float:
        return time.time()

    # 第一次调用
    ts1 = get_timestamp()
    print(f"第一次调用: {ts1}")

    # 立即第二次调用（应该命中缓存）
    time.sleep(0.1)
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


def test_cache_with_stats() -> None:
    """测试带统计的缓存"""
    print("\n" + "=" * 60)
    print("测试 PEP 695 泛型缓存（带统计）")
    print("=" * 60)

    def slow_function(n: int) -> int:
        time.sleep(0.01)  # 模拟慢操作
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


def test_lru_cache() -> None:
    """测试 LRU 缓存"""
    print("\n" + "=" * 60)
    print("测试 LRU 缓存（限制大小）")
    print("=" * 60)

    @lru_cache_custom(maxsize=3)
    def compute(n: int) -> int:
        print(f"  计算 compute({n})")
        return n * 2

    # 添加 4 个不同的值（超过 maxsize）
    results = [compute(i) for i in range(4)]
    print(f"结果: {results}")

    # 再次访问第一个值（应该被淘汰了）
    print("\n再次访问 compute(0):")
    result = compute(0)
    print(f"结果: {result}")

    print("\n✓ LRU 缓存测试完成")


if __name__ == "__main__":
    test_simple_cache()
    test_ttl_cache()
    test_cache_with_stats()
    test_lru_cache()
