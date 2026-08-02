"""

from __future__ import annotations

装饰器详细基础示例

补充 L20 核心内容，提供更详细的装饰器基础讲解。

本文件涵盖：
- 闭包回顾（装饰器的基础）
- 装饰器的本质和执行时机
- 参数传递的深入讲解
- 装饰器叠加的原理

作者: Python 3.13 全栈课程
日期: 2026-06-04
Python版本: 3.12+
"""

from collections.abc import Callable
from functools import wraps
import time
from typing import Any

# ============================================
# 第一部分：闭包回顾
# ============================================


def demonstrate_closure() -> None:
    """
    回顾闭包的概念。

    装饰器的本质是闭包，理解闭包是理解装饰器的前提。
    """
    print("=" * 50)
    print("1. 闭包回顾")
    print("=" * 50)

    def outer(x: int) -> Callable[[], int]:
        """外层函数"""

        def inner() -> int:
            """内层函数，可以访问外层函数的变量"""
            return x * 2

        return inner

    # 创建闭包
    closure = outer(10)
    print(f"闭包结果: {closure()}")  # 20
    print(f"闭包捕获的变量: {closure.__closure__}")
    print()


# ============================================
# 第二部分：装饰器的本质
# ============================================


def simple_decorator(func: Callable) -> Callable:
    """
    最简单的装饰器。

    装饰器是一个函数，它接受一个函数作为参数，返回一个新的函数。

    Args:
        func: 被装饰的函数

    Returns:
        包装后的函数
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"调用函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数返回: {result}")
        return result

    return wrapper


@simple_decorator
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"


def demonstrate_decorator_essence() -> None:
    """
    演示装饰器的本质。

    @decorator 语法糖等价于: func = decorator(func)
    """
    print("=" * 50)
    print("2. 装饰器的本质")
    print("=" * 50)

    # 使用 @ 语法
    result1 = greet("张三")
    print(f"最终结果: {result1}")

    # 等价的手动装饰
    def manual_greet(name: str) -> str:
        return f"Hello, {name}!"

    decorated_greet = simple_decorator(manual_greet)
    result2 = decorated_greet("李四")
    print(f"手动装饰结果: {result2}")
    print()


# ============================================
# 第三部分：装饰器的执行时机
# ============================================


def decorator_with_print(func: Callable) -> Callable:
    """
    带打印的装饰器，用于演示执行时机。
    """
    print(f"[装饰时] 正在装饰函数: {func.__name__}")

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"[调用时] 执行 {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


def demonstrate_execution_timing() -> None:
    """
    演示装饰器的执行时机。

    关键点：
    - 装饰器在函数定义时执行（模块导入时）
    - wrapper 在函数调用时执行
    """
    print("=" * 50)
    print("3. 装饰器的执行时机")
    print("=" * 50)

    print("定义函数时:")

    @decorator_with_print
    def example_func() -> str:
        return "done"

    print("\n调用函数时:")
    example_func()
    print()


# ============================================
# 第四部分：参数传递深入讲解
# ============================================


def timing_decorator(func: Callable) -> Callable:
    """
    计时装饰器。

    演示如何正确传递参数。

    Args:
        func: 被装饰的函数

    Returns:
        包装后的函数
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # *args 捕获位置参数
        # **kwargs 捕获关键字参数
        start = time.perf_counter()
        result = func(*args, **kwargs)  # 传递给原函数
        end = time.perf_counter()
        print(f"{func.__name__} 执行时间: {end - start:.4f}秒")
        return result

    return wrapper


@timing_decorator
def slow_function(duration: float = 0.1) -> int:
    """模拟耗时操作"""
    time.sleep(duration)
    return 42


@timing_decorator
def add(a: int, b: int) -> int:
    """加法函数"""
    return a + b


def demonstrate_parameter_passing() -> None:
    """
    演示参数传递。
    """
    print("=" * 50)
    print("4. 参数传递深入讲解")
    print("=" * 50)

    # 无参数
    result1 = slow_function()
    print(f"结果: {result1}")

    # 位置参数
    result2 = add(10, 20)
    print(f"结果: {result2}")

    # 关键字参数
    result3 = add(a=5, b=15)
    print(f"结果: {result3}")

    # 混合参数
    result4 = add(5, b=10)
    print(f"结果: {result4}")
    print()


# ============================================
# 第五部分：带参数的装饰器（装饰器工厂）
# ============================================


def repeat(times: int) -> Callable:
    """
    重复执行装饰器。

    这是一个装饰器工厂，返回一个装饰器。

    Args:
        times: 重复次数

    Returns:
        装饰器函数
    """
    print(f"[工厂] 创建装饰器，重复次数: {times}")

    def decorator(func: Callable) -> Callable:
        print(f"[装饰器] 装饰函数: {func.__name__}")

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> list[Any]:
            print(f"[执行] 重复执行 {times} 次")
            results = []
            for _i in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results

        return wrapper

    return decorator


@repeat(3)
def roll_dice() -> int:
    """掷骰子"""
    import random

    return random.randint(1, 6)


def demonstrate_parameterized_decorator() -> None:
    """
    演示带参数的装饰器。

    @repeat(3) 等价于:
    1. decorator = repeat(3)        # 调用工厂
    2. roll_dice = decorator(roll_dice)  # 应用装饰器
    """
    print("=" * 50)
    print("5. 带参数的装饰器")
    print("=" * 50)

    results = roll_dice()
    print(f"掷骰子3次: {results}")
    print()


# ============================================
# 第六部分：装饰器叠加（装饰器链）
# ============================================


def decorator_a(func: Callable) -> Callable:
    """装饰器A"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("→ 装饰器A: 前")
        result = func(*args, **kwargs)
        print("← 装饰器A: 后")
        return result

    return wrapper


def decorator_b(func: Callable) -> Callable:
    """装饰器B"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("  → 装饰器B: 前")
        result = func(*args, **kwargs)
        print("  ← 装饰器B: 后")
        return result

    return wrapper


@decorator_a
@decorator_b
def complex_function(x: int) -> int:
    """被多个装饰器装饰的函数"""
    print(f"    · 原函数执行: {x}")
    return x * 2


def demonstrate_decorator_stacking() -> None:
    """
    演示装饰器叠加。

    装饰器的执行顺序：
    - 装饰时：从下到上（先B后A）
    - 执行时：从上到下（先A后B）

    @decorator_a
    @decorator_b
    def func():
        pass

    等价于: func = decorator_a(decorator_b(func))
    """
    print("=" * 50)
    print("6. 装饰器叠加")
    print("=" * 50)

    print("调用 complex_function(21):")
    result = complex_function(21)
    print(f"最终结果: {result}")
    print()


# ============================================
# 主函数
# ============================================


def main() -> None:
    """主函数"""
    demonstrate_closure()
    demonstrate_decorator_essence()
    demonstrate_execution_timing()
    demonstrate_parameter_passing()
    demonstrate_parameterized_decorator()
    demonstrate_decorator_stacking()

    print("=" * 50)
    print("演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
