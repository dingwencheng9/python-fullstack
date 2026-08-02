"""
L10: 类型系统 - 泛型约束练习

使用泛型约束实现类型安全的函数。
"""

from typing import TypeVar

T = TypeVar("T", int, float)


def add[T: (int, float)](a: T, b: T) -> T:
    """加法"""
    return a + b


def multiply[T: (int, float)](a: T, b: T) -> T:
    """乘法"""
    return a * b


def max_of_two[T: (int, float)](a: T, b: T) -> T:
    """返回较大值"""
    return a if a > b else b


# === 验证 ===

if __name__ == "__main__":
    assert add(1, 2) == 3
    assert add(1.5, 2.5) == 4.0
    assert multiply(3, 4) == 12
    assert max_of_two(10, 20) == 20

    print("✅ 所有测试通过！")
