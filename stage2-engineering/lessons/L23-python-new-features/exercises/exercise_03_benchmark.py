"""

from __future__ import annotations

练习 3: 性能基准测试

目标：
  - 创建自己的基准测试
  - 对比 Python 3.13 和 3.13 性能
  - 理解 JIT 编译器的影响

完成标准：
  - 实现基准测试装饰器
  - 创建至少 3 个测试函数
  - 运行测试并分析结果
"""

import sys
from collections.abc import Callable
from functools import wraps


# TODO: 实现基准测试装饰器
def benchmark_decorator(iterations: int = 1000):
    """
    性能测试装饰器

    参数:
        iterations: 迭代次数

    使用示例:
        @benchmark_decorator(iterations=10000)
        def my_function():
            # 你的代码
            pass
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 实现基准测试逻辑
            # 提示:
            #   1. 使用 time.perf_counter() 测量时间
            #   2. 运行函数 iterations 次
            #   3. 计算平均时间
            #   4. 打印结果
            #   5. 返回函数结果

            # 开始实现
            print(f"\n测试函数: {func.__name__}")
            print(f"迭代次数: {iterations}")

            # TODO: 你的代码
            raise NotImplementedError("请实现 benchmark_decorator")

        return wrapper

    return decorator


# TODO: 实现测试函数


@benchmark_decorator(iterations=10000)
def test_list_operations():
    """
    测试列表操作

    提示: 创建、修改、排序列表
    """
    # TODO: 实现


@benchmark_decorator(iterations=1000)
def test_string_operations():
    """
    测试字符串操作

    提示: 拼接、分割、格式化字符串
    """
    # TODO: 实现


@benchmark_decorator(iterations=100)
def test_math_operations():
    """
    测试数学运算

    提示: 使用 math 模块进行密集计算
    """
    # TODO: 实现


@benchmark_decorator(iterations=1000)
def test_dict_operations():
    """
    测试字典操作

    提示: 创建、查询、更新字典
    """
    # TODO: 实现


@benchmark_decorator(iterations=100)
def test_class_operations():
    """
    测试类操作

    提示: 创建类实例并调用方法
    """
    # TODO: 实现


# === 参考实现 ===
# 完成练习后可以取消注释查看

"""
def benchmark_decorator(iterations: int = 1000):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"\\n测试函数: {func.__name__}")
            print(f"迭代次数: {iterations}")

            # 预热
            func(*args, **kwargs)

            # 测试
            start = time.perf_counter()
            for _ in range(iterations):
                result = func(*args, **kwargs)
            end = time.perf_counter()

            # 计算并打印结果
            total_time = end - start
            avg_time = total_time / iterations
            print(f"总时间: {total_time:.4f}s")
            print(f"平均时间: {avg_time*1000:.4f}ms")
            print(f"吞吐量: {iterations/total_time:.2f} ops/s")

            return result
        return wrapper
    return decorator


# 示例测试函数
@benchmark_decorator(iterations=10000)
def test_list_operations():
    data = list(range(100))
    data.append(100)
    data.sort(reverse=True)
    return data[:10]


@benchmark_decorator(iterations=1000)
def test_string_operations():
    text = "hello"
    result = " ".join([text.upper(), text.lower(), text.capitalize()])
    return result.split()


@benchmark_decorator(iterations=100)
def test_math_operations():
    import math
    result = 0.0
    for i in range(1000):
        result += math.sqrt(i) * math.sin(i)
    return result
"""


# === 测试运行器 ===
def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("练习 3: 性能基准测试")
    print("=" * 70)
    print(f"Python 版本: {sys.version}")
    print(f"平台: {sys.platform}")

    tests = [
        test_list_operations,
        test_string_operations,
        test_math_operations,
        test_dict_operations,
        test_class_operations,
    ]

    print("\n开始测试...")

    for test in tests:
        try:
            test()
        except NotImplementedError as e:
            print(f"  ⚠️  {e}")
        except Exception as e:
            print(f"  ✗ 错误: {e}")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("\n任务:")
    print("  1. 实现 benchmark_decorator 装饰器")
    print("  2. 实现所有测试函数")
    print("  3. 在 Python 3.12 中运行: python3.12 stage2-engineering/lessons/L21-python313-experience/exercises/exercise_03_benchmark.py")
    print("  4. 在 Python 3.13 中运行: python3.13 stage2-engineering/lessons/L21-python313-experience/exercises/exercise_03_benchmark.py")
    print("  5. 对比性能差异")
    print("\n提示:")
    print("  - 小列表操作预期有 10-20% 提升")
    print("  - 数学运算预期有 5-15% 提升")
    print("  - 整体性能预期有 5-15% 提升")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
