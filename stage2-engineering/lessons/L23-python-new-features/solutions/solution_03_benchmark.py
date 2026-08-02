"""

from __future__ import annotations

练习 3: 性能基准测试 - 参考答案

===============================================================================
解题思路: 使用 timeit 和 perf_counter 对比 Python 3.13 性能提升
===============================================================================
"""

import time
import timeit
from collections.abc import Callable


def fibonacci_recursive(n: int) -> int:
    """递归实现 Fibonacci"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n: int) -> int:
    """迭代实现 Fibonacci"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def benchmark_function(func: Callable, *args, **kwargs) -> float:
    """测量函数执行时间"""
    start = time.perf_counter()
    func(*args, **kwargs)
    return time.perf_counter() - start


def run_benchmarks():
    """运行性能测试"""
    print("=" * 70)
    print("Python 3.13 性能基准测试")
    print("=" * 70)
    print()

    # 测试 1: Fibonacci 递归 vs 迭代
    print("测试 1: Fibonacci(20)")
    n = 20

    time_recursive = benchmark_function(fibonacci_recursive, n)
    time_iterative = benchmark_function(fibonacci_iterative, n)

    print(f"  递归实现: {time_recursive:.6f} 秒")
    print(f"  迭代实现: {time_iterative:.6f} 秒")
    print(f"  加速比: {time_recursive / time_iterative:.2f}x")
    print()

    # 测试 2: 列表推导 vs for 循环
    print("测试 2: 创建 100,000 个元素的列表")

    def list_comprehension():
        return [i * 2 for i in range(100000)]

    def for_loop():
        result = []
        for i in range(100000):
            result.append(i * 2)
        return result

    time_comp = timeit.timeit(list_comprehension, number=100) / 100
    time_loop = timeit.timeit(for_loop, number=100) / 100

    print(f"  列表推导: {time_comp:.6f} 秒")
    print(f"  for 循环: {time_loop:.6f} 秒")
    print(f"  加速比: {time_loop / time_comp:.2f}x")
    print()

    # 测试 3: 字典查找 vs 列表查找
    print("测试 3: 查找 1,000 次")

    data_list = list(range(10000))
    data_dict = {i: i for i in range(10000)}
    target = 9999

    def list_lookup():
        for _ in range(1000):
            _ = target in data_list

    def dict_lookup():
        for _ in range(1000):
            _ = target in data_dict

    time_list = timeit.timeit(list_lookup, number=10) / 10
    time_dict = timeit.timeit(dict_lookup, number=10) / 10

    print(f"  列表查找: {time_list:.6f} 秒")
    print(f"  字典查找: {time_dict:.6f} 秒")
    print(f"  加速比: {time_list / time_dict:.2f}x")
    print()

    print("=" * 70)
    print("测试完成！")
    print("\nPython 3.13 性能优化:")
    print("  - JIT 编译器改进")
    print("  - 内存管理优化")
    print("  - 内置函数加速")
    print("=" * 70)


if __name__ == "__main__":
    run_benchmarks()
