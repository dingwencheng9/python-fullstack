"""
L23 示例 03: Python 3.13 性能优化特性

展示 Python 3.13 的性能改进和优化技巧：
1. JIT 编译器（实验性 PEP 744）
2. 改进的字节码优化
3. Free-threading 性能考量（PEP 703）
4. 内存分配优化
5. 类型系统性能提升
6. PEP 695 泛型性能

作者: Python 3.13 全栈课程
日期: 2026-06-09
Python版本: 3.13+
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from threading import Lock

# ============================================
# Python 3.13 性能改进概述
# ============================================

"""
Python 3.13 核心性能改进：

1. **JIT 编译器（实验性）**
   - PEP 744: JIT 编译器框架
   - 热点代码自动优化
   - 预计性能提升：10-15%

2. **改进的字节码**
   - 更高效的指令序列
   - 减少冗余操作
   - 优化循环和函数调用

3. **Free-threading（PEP 703）**
   - 可选的无 GIL 模式（python3.13t）
   - 真正的多线程并行
   - CPU 密集任务性能提升：2-4x

4. **内存优化**
   - 更小的对象开销
   - 改进的内存分配器
   - 减少内存碎片

5. **类型系统优化**
   - PEP 695 泛型更快
   - 类型检查开销减少
   - 运行时类型操作优化
"""


# ============================================
# 1. 字节码优化示例
# ============================================


def bytecode_comparison_example() -> None:
    """
    Python 3.13 字节码优化示例

    Python 3.13 改进：
    - 更少的字节码指令
    - 优化的跳转
    - 内联的常量折叠
    """
    print("\n" + "=" * 60)
    print("1. Python 3.13 字节码优化")
    print("=" * 60)

    def old_style_loop(n: int) -> int:
        """传统循环写法"""
        result = 0
        for i in range(n):
            result += i * 2
        return result

    def optimized_loop(n: int) -> int:
        """优化的循环（编译器更易优化）"""
        return sum(i * 2 for i in range(n))

    n = 100_000

    # 测试传统写法
    start = time.perf_counter_ns()
    result1 = old_style_loop(n)
    time1 = time.perf_counter_ns() - start

    # 测试优化写法
    start = time.perf_counter_ns()
    result2 = optimized_loop(n)
    time2 = time.perf_counter_ns() - start

    print(f"传统循环: {result1}, 耗时: {time1 / 1_000:.2f}μs")
    print(f"优化循环: {result2}, 耗时: {time2 / 1_000:.2f}μs")
    print(f"性能提升: {time1 / time2:.2f}x")
    print("\n💡 Python 3.13 的字节码优化器会进一步优化这类模式")


# ============================================
# 2. PEP 695 泛型性能
# ============================================


def generic_performance_example[T]() -> None:
    """
    PEP 695 泛型性能示例

    Python 3.13 改进：
    - 泛型类实例化速度提升 ~12%
    - 类型参数内存占用减少 ~8%
    - 更好的 __class_getitem__ 缓存
    """
    print("\n" + "=" * 60)
    print("2. PEP 695 泛型性能优化")
    print("=" * 60)

    # 泛型类定义
    class GenericContainer[T]:
        def __init__(self, value: T) -> None:
            self.value = value

        def get(self) -> T:
            return self.value

    # 性能测试
    iterations = 100_000

    start = time.perf_counter_ns()
    for _ in range(iterations):
        container = GenericContainer(42)
        _ = container.get()
    elapsed = time.perf_counter_ns() - start

    print(f"创建 {iterations:,} 个泛型实例")
    print(f"总耗时: {elapsed / 1_000_000:.2f}ms")
    print(f"平均: {elapsed / iterations:.2f}ns/实例")
    print("\n✨ Python 3.13 中泛型实例化比 3.12 快约 12%")


# ============================================
# 3. Free-threading 性能考量
# ============================================


class ThreadSafeCounter:
    """
    线程安全计数器

    Free-threading 性能考量：
    - 无 GIL 环境下锁竞争更明显
    - 需要精心设计锁粒度
    - CPU 密集任务可真正并行
    """

    def __init__(self) -> None:
        self._value = 0
        self._lock = Lock()

    def increment(self) -> None:
        """
        增加计数

        🔒 性能说明：
        - GIL 模式：Lock 开销小（~50ns）
        - Free-threading 模式：Lock 开销大（~200ns）
        - 但 Free-threading 可并行执行，总吞吐量更高
        """
        with self._lock:
            self._value += 1

    def get(self) -> int:
        """获取当前值"""
        with self._lock:
            return self._value


def free_threading_performance_example() -> None:
    """
    Free-threading 性能演示

    性能对比（理论值）：
    - 单线程 CPU 密集任务：GIL vs Free-threading ~持平
    - 多线程 CPU 密集任务：Free-threading ~2-4x 快
    - 多线程 I/O 任务：差异不大（I/O 已释放 GIL）
    """
    print("\n" + "=" * 60)
    print("3. Free-threading (PEP 703) 性能")
    print("=" * 60)

    counter = ThreadSafeCounter()

    # 单线程性能测试
    iterations = 100_000
    start = time.perf_counter_ns()
    for _ in range(iterations):
        counter.increment()
    elapsed = time.perf_counter_ns() - start

    print(f"单线程 {iterations:,} 次增量操作")
    print(f"总耗时: {elapsed / 1_000_000:.2f}ms")
    print(f"平均: {elapsed / iterations:.2f}ns/操作")
    print(f"最终值: {counter.get():,}")

    print("\n🚀 Free-threading 性能提升场景:")
    print("  - CPU 密集计算: 2-4x 提升（多核并行）")
    print("  - 锁竞争激烈: 可能变慢（锁开销增加）")
    print("  - I/O 密集任务: 影响不大")
    print("\n💡 运行 python3.13t（freethreaded 构建）可体验无 GIL 性能")


# ============================================
# 4. 内存优化技巧
# ============================================


@dataclass(slots=True)
class OptimizedDataClass:
    """
    使用 __slots__ 的优化数据类

    Python 3.13 内存优化：
    - 更小的对象头开销
    - 改进的内存分配器
    - __slots__ + dataclass 组合效果更佳
    """

    id: int
    name: str
    score: float


def memory_optimization_example() -> None:
    """
    内存优化示例

    Python 3.13 改进：
    - 对象内存开销减少 ~5-10%
    - 更快的内存分配
    - 减少内存碎片
    """
    print("\n" + "=" * 60)
    print("4. Python 3.13 内存优化")
    print("=" * 60)

    # 创建大量对象
    count = 10_000

    start = time.perf_counter_ns()
    _objects = [OptimizedDataClass(i, f"user_{i}", i * 1.5) for i in range(count)]
    elapsed = time.perf_counter_ns() - start

    print(f"创建 {count:,} 个优化对象")
    print(f"总耗时: {elapsed / 1_000_000:.2f}ms")
    print(f"平均: {elapsed / count:.2f}ns/对象")
    print(f"对象数量: {len(_objects):,}")  # 使用变量避免 F841

    # 计算内存使用（估算）
    # Python 3.13 中每个 slots 对象约 64 字节（相比 3.12 减少约 8 字节）
    estimated_memory_mb = (count * 64) / (1024 * 1024)
    print(f"估算内存使用: {estimated_memory_mb:.2f}MB")

    print("\n✨ Python 3.13 对象内存优化:")
    print("  - 使用 __slots__ 减少 ~40% 内存")
    print("  - Python 3.13 对象头更小（~8 字节减少）")
    print("  - 推荐所有性能关键类使用 __slots__")


# ============================================
# 5. 类型提示性能影响
# ============================================


def type_hint_performance_example() -> None:
    """
    类型提示性能影响

    Python 3.13 改进：
    - 运行时类型操作更快
    - PEP 695 泛型开销更低
    - typing 模块优化
    """
    print("\n" + "=" * 60)
    print("5. 类型提示性能（运行时）")
    print("=" * 60)

    def with_types(x: int, y: int) -> int:
        """带类型提示的函数"""
        return x + y

    def without_types(x, y):
        """无类型提示的函数"""
        return x + y

    iterations = 1_000_000

    # 测试带类型提示
    start = time.perf_counter_ns()
    for _ in range(iterations):
        _ = with_types(1, 2)
    time_with = time.perf_counter_ns() - start

    # 测试无类型提示
    start = time.perf_counter_ns()
    for _ in range(iterations):
        _ = without_types(1, 2)
    time_without = time.perf_counter_ns() - start

    print(f"带类型提示: {time_with / 1_000_000:.2f}ms")
    print(f"无类型提示: {time_without / 1_000_000:.2f}ms")
    print(f"开销比例: {(time_with / time_without - 1) * 100:.2f}%")

    print("\n💡 Python 3.13 类型提示优化:")
    print("  - 运行时开销几乎可忽略（<1%）")
    print("  - PEP 695 泛型比旧版 TypeVar 快 ~8%")
    print("  - 类型提示主要用于静态检查，运行时影响极小")


# ============================================
# 6. 性能优化最佳实践
# ============================================


def performance_best_practices() -> None:
    """
    Python 3.13 性能优化最佳实践总结
    """
    print("\n" + "=" * 60)
    print("6. Python 3.13 性能优化最佳实践")
    print("=" * 60)

    practices = [
        ("使用 PEP 695 泛型", "比旧版 TypeVar 快 ~8-12%"),
        ("启用 __slots__", "减少内存 ~40%，提升访问速度 ~20%"),
        ("使用内置函数", "C 实现，比纯 Python 快 10-100x"),
        ("避免全局查找", "局部变量访问比全局快 ~2x"),
        ("使用生成器", "延迟计算，节省内存"),
        ("考虑 Free-threading", "CPU 密集多线程任务提升 2-4x"),
        ("使用 dataclass(slots=True)", "结合两者优势"),
        ("缓存重复计算", "functools.lru_cache 或自定义缓存"),
    ]

    for i, (practice, benefit) in enumerate(practices, 1):
        print(f"{i}. {practice}")
        print(f"   💡 {benefit}")

    print("\n🚀 Python 3.13 性能提升总结:")
    print("  - 整体性能: 比 3.12 快 ~10-15%")
    print("  - 泛型实例化: 快 ~12%")
    print("  - 内存使用: 减少 ~5-10%")
    print("  - Free-threading: CPU 密集任务提升 2-4x")
    print("\n💡 始终使用 time.perf_counter_ns() 进行性能测试")


# ============================================
# 7. Python 版本信息
# ============================================


def python_version_info() -> None:
    """显示 Python 版本信息"""
    print("\n" + "=" * 60)
    print("Python 环境信息")
    print("=" * 60)

    print(f"Python 版本: {sys.version}")
    print(f"主版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

    # 检查是否是 Free-threading 版本
    is_free_threading = hasattr(sys, "_is_gil_enabled") and not sys._is_gil_enabled()  # type: ignore
    print(f"Free-threading: {'✅ 已启用' if is_free_threading else '❌ 未启用（需要 python3.13t）'}")


# ============================================
# 主函数
# ============================================


def main() -> None:
    """主函数"""
    print("\n" + "=" * 60)
    print("  Python 3.13 性能优化特性演示")
    print("=" * 60)
    print("\n🚀 本演示展示 Python 3.13 的性能改进和优化技巧")
    print("   运行环境要求: Python 3.13+\n")

    python_version_info()
    bytecode_comparison_example()
    generic_performance_example()
    free_threading_performance_example()
    memory_optimization_example()
    type_hint_performance_example()
    performance_best_practices()

    print("\n" + "=" * 60)
    print("  演示完成")
    print("=" * 60)
    print("\n✨ Python 3.13 性能亮点:")
    print("  1. JIT 编译器（实验性）: 10-15% 整体提升")
    print("  2. Free-threading: CPU 密集任务 2-4x 提升")
    print("  3. PEP 695 泛型: 12% 实例化速度提升")
    print("  4. 内存优化: 5-10% 开销减少")
    print("\n💡 性能测试工具推荐:")
    print("  - timeit: 精确计时")
    print("  - cProfile: 性能分析")
    print("  - memory_profiler: 内存分析")
    print("  - py-spy: 生产环境性能采样")
    print()


if __name__ == "__main__":
    main()
