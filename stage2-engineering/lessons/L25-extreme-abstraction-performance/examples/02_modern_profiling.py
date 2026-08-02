"""
现代内存剖析实战 - 隐蔽性能陷阱诊断
====================================

本模块故意构造 2 个典型的隐蔽性能/内存陷阱，用于演示现代性能分析工具的使用。

陷阱 1: 高频生成的局部大对象（内存抖动）
陷阱 2: 无界缓存导致的内存泄漏（OOM 风险）

使用 Scalene 分析本文件：
--------------------------
# 安装
uv add scalene

# 终端运行（推荐 Web UI）
scalene --web 02_modern_profiling.py

# 或终端输出
scalene 02_modern_profiling.py

# 指定 CPU 采样率（提高精度）
scalene --cpu-sampling-rate 0.01 02_modern_profiling.py

# 包含内存分析
scalene --profile-all 02_modern_profiling.py


使用 Memray 生成火焰图：
-----------------------
# 安装
uv add memray

# 运行并记录
memray run 02_modern_profiling.py

# 生成火焰图
memray flamegraph memray-02_modern_profiling.py.*.bin

# 生成表格报告
memray table memray-02_modern_profiling.py.*.bin

# 生成树状报告
memray tree memray-02_modern_profiling.py.*.bin


预期诊断结果：
-------------
Scalene 会精准指出：
- trap_1_memory_churn() 中的 line 76: 高频内存分配（每次 80MB）
- trap_2_unbounded_cache() 中的 line 134: 无界字典持续增长

Memray 火焰图会显示：
- trap_1 占用内存峰值：8GB+
- trap_2 缓存泄漏：持续增长，最终 OOM

作者：Python 3.13 全栈课程
"""

from __future__ import annotations

import sys
import time
from typing import Any, ClassVar

# ============================================================
# 陷阱 1: 高频生成的局部大对象（内存抖动）
# ============================================================


def create_large_object() -> list[int]:
    """
    创建一个占用 ~80MB 的大对象

    问题：如果在循环中高频调用，会导致内存抖动（Memory Churn）
    影响：频繁的内存分配/回收触发 GC，降低性能
    """
    # 1000 万个整数 × 8 bytes = 80MB
    return list(range(10_000_000))


def trap_1_memory_churn() -> None:
    """
    ❌ 陷阱 1: 高频生成局部大对象

    问题分析：
    - 每次循环创建 80MB 对象
    - 100 次循环 = 8GB 内存分配
    - Python GC 频繁触发
    - 性能下降 10-50%

    Scalene 会精确标记这一行为热点
    """
    print("\n" + "=" * 80)
    print("陷阱 1: 高频生成局部大对象（内存抖动）")
    print("=" * 80 + "\n")

    start = time.perf_counter()
    results: list[int] = []

    for i in range(100):
        # ❌ 问题代码：每次循环创建 80MB 大对象
        large_data = create_large_object()

        # 仅使用一个值，但整个大对象仍在内存中
        results.append(large_data[0])

        # 大对象离开作用域，等待 GC 回收
        # 但 GC 可能延迟触发，导致内存峰值飙升

        if (i + 1) % 20 == 0:
            print(f"  进度: {i + 1}/100 (内存抖动中...)")

    duration = time.perf_counter() - start

    print(f"\n✓ 完成，耗时 {duration:.2f}s")
    print(f"✓ 结果: {len(results)} 个值")
    print("\n💡 Scalene 分析提示:")
    print("   - 运行: scalene --web 02_modern_profiling.py")
    print("   - 查看: 第 76 行会标记为内存热点（红色）")
    print("   - AI 建议: 避免在循环中创建大对象\n")


def trap_1_fixed() -> None:
    """
    ✅ 修复方案: 复用对象或使用生成器

    改进：
    - 在循环外创建一次
    - 或使用生成器（按需生成）
    - 减少内存分配次数
    """
    print("\n" + "=" * 80)
    print("修复方案: 复用大对象")
    print("=" * 80 + "\n")

    start = time.perf_counter()

    # ✅ 在循环外创建一次
    large_data = create_large_object()
    results: list[int] = []

    for i in range(100):
        # 直接复用，无需重复创建
        results.append(large_data[0])

        if (i + 1) % 20 == 0:
            print(f"  进度: {i + 1}/100 (内存稳定)")

    duration = time.perf_counter() - start

    print(f"\n✓ 完成，耗时 {duration:.2f}s")
    print("✓ 内存占用: 仅 80MB（复用对象）")
    print("✓ 性能提升: 约 10-50% 更快\n")


# ============================================================
# 陷阱 2: 无界缓存导致的内存泄漏（OOM 风险）
# ============================================================


class UnboundedCache:
    """
    ❌ 陷阱 2: 无界缓存

    问题：
    - 缓存无容量限制
    - 持续增长直到 OOM
    - 常见于长期运行的服务
    """

    _cache: ClassVar[dict[str, Any]] = {}

    @classmethod
    def get_or_compute(cls, key: str, value: Any) -> Any:
        """
        获取或计算缓存值

        问题：_cache 永远不会清理，持续增长
        """
        if key not in cls._cache:
            cls._cache[key] = value
        return cls._cache[key]

    @classmethod
    def cache_size(cls) -> int:
        """返回缓存条目数"""
        return len(cls._cache)

    @classmethod
    def cache_memory(cls) -> int:
        """估算缓存占用的内存（字节）"""
        total = 0
        for value in cls._cache.values():
            total += sys.getsizeof(value)
        return total


def trap_2_unbounded_cache() -> None:
    """
    ❌ 陷阱 2: 无界缓存导致内存泄漏

    场景：
    - 长期运行的 Web 服务
    - 缓存用户请求结果
    - 缓存永不过期
    - 最终导致 OOM

    Memray 会显示持续增长的内存曲线
    """
    print("\n" + "=" * 80)
    print("陷阱 2: 无界缓存导致的内存泄漏")
    print("=" * 80 + "\n")

    start = time.perf_counter()

    # 模拟 10000 个不同的缓存键
    for i in range(10_000):
        key = f"user_{i}_data"

        # ❌ 问题代码：无界缓存，持续增长
        # 每个值占用 ~40KB，10000 个 = 400MB
        large_value = list(range(5000))  # ~40KB
        UnboundedCache.get_or_compute(key, large_value)

        if (i + 1) % 2000 == 0:
            size = UnboundedCache.cache_size()
            memory_mb = UnboundedCache.cache_memory() / (1024 * 1024)
            print(f"  进度: {i + 1}/10000 | 缓存条目: {size} | 内存: {memory_mb:.1f}MB")

    duration = time.perf_counter() - start
    final_memory_mb = UnboundedCache.cache_memory() / (1024 * 1024)

    print(f"\n✓ 完成，耗时 {duration:.2f}s")
    print(f"✓ 缓存条目: {UnboundedCache.cache_size()}")
    print(f"❌ 内存占用: {final_memory_mb:.1f}MB（持续增长！）")
    print("\n⚠️  风险:")
    print("   - 长期运行后会 OOM")
    print("   - 缓存命中率可能很低（冷数据占用内存）")
    print("\n💡 Memray 分析提示:")
    print("   - 运行: memray run 02_modern_profiling.py")
    print("   - 生成火焰图: memray flamegraph memray-*.bin")
    print("   - 查看: 会显示 _cache 字典持续增长\n")


def trap_2_fixed() -> None:
    """
    ✅ 修复方案: 使用 LRU 缓存

    改进：
    - 使用 functools.lru_cache
    - 或手动实现 LRU（最近最少使用淘汰）
    - 设置最大缓存条目数
    """
    from functools import lru_cache

    print("\n" + "=" * 80)
    print("修复方案: LRU 缓存（最大 128 条目）")
    print("=" * 80 + "\n")

    @lru_cache(maxsize=128)
    def cached_compute(_key: str) -> list[int]:
        """
        ✅ 使用 LRU 缓存，自动淘汰

        特性：
        - 最大 128 个条目
        - 自动淘汰最少使用的
        - 内存可控
        """
        return list(range(5000))

    start = time.perf_counter()

    for i in range(10_000):
        key = f"user_{i}_data"
        _ = cached_compute(key)

        if (i + 1) % 2000 == 0:
            cache_info = cached_compute.cache_info()
            progress = f"  进度: {i + 1}/10000"
            hits = f"缓存命中: {cache_info.hits}"
            misses = f"缓存未命中: {cache_info.misses}"
            print(f"  {progress} | {hits} | {misses}")

    duration = time.perf_counter() - start
    cache_info = cached_compute.cache_info()

    print(f"\n✓ 完成，耗时 {duration:.2f}s")
    print("✓ 缓存条目: 最多 128 个（自动淘汰）")
    print("✓ 内存占用: 固定 ~5MB")
    print(f"✓ 缓存命中率: {cache_info.hits / (cache_info.hits + cache_info.misses):.1%}\n")


# ============================================================
# 主函数：运行所有陷阱演示
# ============================================================


def main() -> None:
    """
    主函数：依次演示两个陷阱及其修复方案

    运行方式：
    1. 直接运行：python 02_modern_profiling.py
    2. Scalene 分析：scalene --web 02_modern_profiling.py
    3. Memray 分析：memray run 02_modern_profiling.py
    """
    print("\n" + "=" * 80)
    print("现代内存剖析实战 - 隐蔽性能陷阱诊断")
    print("=" * 80)
    print(f"\nPython 版本: {sys.version.split()[0]}")
    print("\n提示：使用 Scalene 或 Memray 分析本文件可获得更详细的性能数据")
    print("     scalene --web 02_modern_profiling.py")
    print("     memray run 02_modern_profiling.py\n")

    # 陷阱 1：内存抖动
    trap_1_memory_churn()
    trap_1_fixed()

    # 陷阱 2：无界缓存
    trap_2_unbounded_cache()
    trap_2_fixed()

    print("=" * 80)
    print("所有演示完成")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
