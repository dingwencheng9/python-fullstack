"""

from __future__ import annotations

Python 3.13 vs 3.12 性能对比基准测试

运行方式:
  python3.12 examples/benchmark_313_vs_312.py > results/python312_results.txt
  python3.13 examples/benchmark_313_vs_312.py > results/python313_results.txt

然后对比两个结果文件。
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
    # 预热
    func(*args, **kwargs)

    # 测试
    start = time.perf_counter()
    for _ in range(iterations):
        func(*args, **kwargs)
    end = time.perf_counter()

    return (end - start) / iterations


# === 测试函数集 ===


def test_list_comprehension_small():
    """小列表推导（100 个元素）"""
    return [i**2 for i in range(100)]


def test_list_comprehension_medium():
    """中等列表推导（1000 个元素）"""
    return [i**2 for i in range(1000)]


def test_list_comprehension_large():
    """大列表推导（10000 个元素）"""
    return [i**2 for i in range(10000)]


def test_dict_operations():
    """字典操作"""
    d = {}
    for i in range(1000):
        d[i] = i**2
    return d


def test_dict_comprehension():
    """字典推导"""
    return {i: i**2 for i in range(1000)}


def test_set_operations():
    """集合操作"""
    s1 = set(range(1000))
    s2 = set(range(500, 1500))
    return s1 & s2


def fibonacci(n: int) -> int:
    """递归斐波那契"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def test_recursive_calls():
    """递归调用"""
    return fibonacci(20)


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


def test_math_operations():
    """数学运算（JIT 可能加速）"""
    result = 0.0
    for i in range(10000):
        result += math.sqrt(i) * math.sin(i) + math.cos(i)
    return result


def test_string_concat():
    """字符串拼接"""
    result = ""
    for i in range(1000):
        result += str(i)
    return result


def test_string_join():
    """字符串 join"""
    return "".join(str(i) for i in range(1000))


def test_string_format():
    """字符串格式化"""
    return [f"Item {i}: value={i**2}" for i in range(1000)]


class Point:
    """简单的点类"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other: "Point") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def test_class_instantiation():
    """类实例化"""
    return [Point(i, i * 2) for i in range(1000)]


def test_method_calls():
    """方法调用"""
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    total = 0.0
    for _ in range(1000):
        total += p1.distance(p2)
    return total


def test_list_operations():
    """列表操作"""
    data = list(range(1000))
    data.append(1000)
    data.sort(reverse=True)
    data.reverse()
    return data[:100]


def test_nested_loops():
    """嵌套循环"""
    result = 0
    for i in range(100):
        for j in range(100):
            result += i * j
    return result


def test_generator_expression():
    """生成器表达式"""
    return sum(i**2 for i in range(10000))


def test_filter_map():
    """filter 和 map"""
    data = range(10000)
    filtered = filter(lambda x: x % 2 == 0, data)
    mapped = map(lambda x: x**2, filtered)
    return list(mapped)


# === 测试配置 ===

TEST_SUITE = [
    # (名称, 函数, 迭代次数)
    ("小列表推导 (100)", test_list_comprehension_small, 10000),
    ("中等列表推导 (1000)", test_list_comprehension_medium, 1000),
    ("大列表推导 (10000)", test_list_comprehension_large, 100),
    ("字典操作", test_dict_operations, 1000),
    ("字典推导", test_dict_comprehension, 1000),
    ("集合操作", test_set_operations, 1000),
    ("递归调用 (fibonacci 20)", test_recursive_calls, 10),
    ("for 循环 (100k)", test_for_loop, 100),
    ("while 循环 (100k)", test_while_loop, 100),
    ("数学运算 (10k)", test_math_operations, 10),
    ("字符串拼接 (1k)", test_string_concat, 100),
    ("字符串 join (1k)", test_string_join, 1000),
    ("字符串格式化 (1k)", test_string_format, 1000),
    ("类实例化 (1k)", test_class_instantiation, 100),
    ("方法调用 (1k)", test_method_calls, 100),
    ("列表操作", test_list_operations, 1000),
    ("嵌套循环 (100x100)", test_nested_loops, 100),
    ("生成器表达式 (10k)", test_generator_expression, 100),
    ("filter + map (10k)", test_filter_map, 100),
]


def run_benchmarks():
    """运行所有基准测试"""
    print("=" * 80)
    print("Python 性能基准测试")
    print("=" * 80)
    print(f"Python 版本: {sys.version}")
    print(f"平台: {sys.platform}")
    print(f"测试数量: {len(TEST_SUITE)}")
    print()

    results = []

    for name, func, iterations in TEST_SUITE:
        print(f"测试: {name:<40} ", end="", flush=True)

        try:
            avg_time = benchmark(func, iterations=iterations)
            ms = avg_time * 1000
            results.append((name, ms))
            print(f"{ms:>10.4f} ms")
        except Exception as e:
            print(f"❌ 错误: {e}")
            results.append((name, float("inf")))

    return results


def print_summary(results: list[tuple[str, float]]):
    """打印测试汇总"""
    print("\n" + "=" * 80)
    print("测试汇总")
    print("=" * 80)
    print(f"{'测试名称':<50} {'时间 (ms)':>15}")
    print("-" * 80)

    for name, ms in results:
        if ms == float("inf"):
            print(f"{name:<50} {'ERROR':>15}")
        else:
            print(f"{name:<50} {ms:>15.4f}")

    # 计算总时间
    valid_results = [ms for _, ms in results if ms != float("inf")]
    if valid_results:
        total_ms = sum(valid_results)
        avg_ms = total_ms / len(valid_results)
        print("-" * 80)
        print(f"{'总时间':<50} {total_ms:>15.4f}")
        print(f"{'平均时间':<50} {avg_ms:>15.4f}")

    print("=" * 80)


def save_results(results: list[tuple[str, float]]):
    """保存结果到文件"""
    import os

    os.makedirs("results", exist_ok=True)

    version = f"python{sys.version_info.major}{sys.version_info.minor}"
    filename = f"results/{version}_results.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Python Version: {sys.version}\n")
        f.write(f"Platform: {sys.platform}\n")
        f.write("\n")
        f.write(f"{'Test Name':<50} {'Time (ms)':>15}\n")
        f.write("-" * 80 + "\n")

        for name, ms in results:
            if ms == float("inf"):
                f.write(f"{name:<50} {'ERROR':>15}\n")
            else:
                f.write(f"{name:<50} {ms:>15.4f}\n")

    print(f"\n结果已保存到: {filename}")


if __name__ == "__main__":
    # 运行基准测试
    results = run_benchmarks()

    # 打印汇总
    print_summary(results)

    # 保存结果
    save_results(results)

    print("\n提示:")
    print("  1. 在 Python 3.12 中运行:")
    print("     python3.12 examples/benchmark_313_vs_312.py")
    print("  2. 在 Python 3.13 中运行:")
    print("     python3.13 examples/benchmark_313_vs_312.py")
    print("  3. 对比 results/ 目录下的结果文件")
    print("\n预期改进:")
    print("  - 小列表推导: 10-20% 提升 🚀")
    print("  - 数学运算: 5-15% 提升")
    print("  - 整体性能: 5-15% 提升")
