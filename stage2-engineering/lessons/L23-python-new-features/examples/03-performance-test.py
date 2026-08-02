"""

from __future__ import annotations

Python 3.13 性能测试演示

本脚本演示如何测试 Python 3.13 的性能改进。
"""

import math
import sys
import time
from collections.abc import Callable


def benchmark(func: Callable, *args, iterations: int = 1000, **kwargs) -> float:
    """
    简单的基准测试函数

    Args:
        func: 要测试的函数
        *args: 函数参数
        iterations: 迭代次数
        **kwargs: 函数关键字参数

    Returns:
        平均执行时间（秒）
    """
    start = time.perf_counter()
    for _ in range(iterations):
        func(*args, **kwargs)
    end = time.perf_counter()
    return (end - start) / iterations


# === 测试 1: 列表推导 ===
def test_list_comprehension_small():
    """小列表推导（Python 3.13 优化明显）"""
    return [i**2 for i in range(100)]


def test_list_comprehension_large():
    """大列表推导"""
    return [i**2 for i in range(10000)]


# === 测试 2: 字典操作 ===
def test_dict_operations():
    """字典操作"""
    d = {}
    for i in range(1000):
        d[i] = i**2
    return d


def test_dict_comprehension():
    """字典推导"""
    return {i: i**2 for i in range(1000)}


# === 测试 3: 函数调用 ===
def fibonacci(n: int) -> int:
    """递归斐波那契（测试函数调用开销）"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def test_recursive_calls():
    """测试递归调用"""
    return fibonacci(20)


# === 测试 4: 循环操作 ===
def test_for_loop():
    """for 循环"""
    result = 0
    for i in range(100000):
        result += i
    return result


def test_while_loop():
    """while 循环"""
    result = 0
    i = 0
    while i < 100000:
        result += i
        i += 1
    return result


# === 测试 5: 数学计算 ===
def test_math_operations():
    """数学运算（JIT 可能加速）"""
    result = 0.0
    for i in range(10000):
        result += math.sqrt(i) * math.sin(i) + math.cos(i)
    return result


# === 测试 6: 字符串操作 ===
def test_string_concat():
    """字符串拼接"""
    result = ""
    for i in range(1000):
        result += str(i)
    return result


def test_string_join():
    """字符串 join"""
    return "".join(str(i) for i in range(1000))


# === 测试 7: 类实例化 ===
class Point:
    """简单的点类"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other: "Point") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def test_class_instantiation():
    """类实例化"""
    points = [Point(i, i * 2) for i in range(1000)]
    return len(points)


def test_method_calls():
    """方法调用"""
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    total = 0.0
    for _ in range(1000):
        total += p1.distance(p2)
    return total


# === 主测试函数 ===
def run_benchmarks():
    """运行所有基准测试"""
    print("=" * 70)
    print("Python 3.13 性能基准测试")
    print("=" * 70)
    print(f"Python 版本: {sys.version}")
    print(f"平台: {sys.platform}")
    print()

    tests = [
        ("小列表推导 (100)", test_list_comprehension_small, 10000),
        ("大列表推导 (10000)", test_list_comprehension_large, 100),
        ("字典操作", test_dict_operations, 1000),
        ("字典推导", test_dict_comprehension, 1000),
        ("递归调用 (fibonacci 20)", test_recursive_calls, 10),
        ("for 循环", test_for_loop, 100),
        ("while 循环", test_while_loop, 100),
        ("数学运算", test_math_operations, 10),
        ("字符串拼接", test_string_concat, 100),
        ("字符串 join", test_string_join, 1000),
        ("类实例化", test_class_instantiation, 100),
        ("方法调用", test_method_calls, 100),
    ]

    results = []

    for name, func, iterations in tests:
        print(f"测试: {name} ({iterations} 次迭代)")
        avg_time = benchmark(func, iterations=iterations)
        ms = avg_time * 1000
        results.append((name, ms))
        print(f"  平均时间: {ms:.4f} ms")
        print()

    # 打印汇总
    print("=" * 70)
    print("测试汇总")
    print("=" * 70)
    print(f"{'测试名称':<40} {'时间 (ms)':<15}")
    print("-" * 70)
    for name, ms in results:
        print(f"{name:<40} {ms:>10.4f}")
    print("=" * 70)

    return results


def compare_with_baseline(baseline_results: list[tuple[str, float]]):
    """
    与基线结果对比

    Args:
        baseline_results: 基线测试结果（来自 Python 3.13）
    """
    print("\n" + "=" * 70)
    print("性能对比 (vs 基线)")
    print("=" * 70)
    print(f"{'测试名称':<30} {'当前 (ms)':<12} {'基线 (ms)':<12} {'提升':<10}")
    print("-" * 70)

    current_results = run_benchmarks()

    if len(current_results) != len(baseline_results):
        print("警告: 测试数量不匹配！")
        return

    for (name, current_ms), (_, baseline_ms) in zip(current_results, baseline_results):
        improvement = ((baseline_ms - current_ms) / baseline_ms) * 100
        symbol = "🚀" if improvement > 0 else "⚠️"
        print(f"{name:<30} {current_ms:>10.4f} {baseline_ms:>10.4f} {symbol} {improvement:>6.1f}%")

    print("=" * 70)


def save_results(results: list[tuple[str, float]], filename: str = "results/benchmark_results.txt"):
    """保存测试结果"""
    import os

    os.makedirs("results", exist_ok=True)

    with open(filename, "w") as f:
        f.write(f"Python Version: {sys.version}\n")
        f.write(f"Platform: {sys.platform}\n")
        f.write("\n")
        f.write(f"{'Test Name':<40} {'Time (ms)':<15}\n")
        f.write("-" * 70 + "\n")
        for name, ms in results:
            f.write(f"{name:<40} {ms:>10.4f}\n")

    print(f"\n结果已保存到: {filename}")


if __name__ == "__main__":
    # 运行基准测试
    results = run_benchmarks()

    # 保存结果
    version = f"python{sys.version_info.major}{sys.version_info.minor}"
    save_results(results, f"results/{version}_results.txt")

    print("\n提示:")
    print("  1. 在 Python 3.13 中运行: python3.12 examples/03-performance-test.py")
    print("  2. 在 Python 3.13 中运行: python3.13 examples/03-performance-test.py")
    print("  3. 对比结果文件进行分析")
    print()
    print("  预期改进:")
    print("    - 小列表推导: 10-20% 提升")
    print("    - 数学运算: 5-15% 提升（JIT 启用时更高）")
    print("    - 整体性能: 5-15% 提升")
