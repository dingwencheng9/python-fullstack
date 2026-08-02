"""练习 2: 参数化计算器测试。

目标：实现 Calculator 类，并用 @pytest.mark.parametrize 覆盖多组输入。
参考答案见 solutions/solution_02_parametrize_calc.py。
"""

from __future__ import annotations

import pytest


class Calculator:
    """一个用于演示参数化测试的小型计算器。"""

    def add(self, a: float, b: float) -> float:
        """返回 a + b。"""
        return a + b

    def divide(self, a: float, b: float) -> float:
        """返回 a / b，除零时抛出 ZeroDivisionError。"""
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    def power(self, base: float, exp: float) -> float:
        """返回 base 的 exp 次幂。"""
        return base**exp


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (2.5, 3.5, 6.0),
    ],
)
def test_add(a: float, b: float, expected: float) -> None:
    assert Calculator().add(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 2, 5.0),
        (7, 2, 3.5),
        (0, 5, 0.0),
        (-6, 2, -3.0),
    ],
)
def test_divide(a: float, b: float, expected: float) -> None:
    assert Calculator().divide(a, b) == expected


def test_divide_by_zero() -> None:
    with pytest.raises(ZeroDivisionError):
        Calculator().divide(1, 0)


@pytest.mark.parametrize(
    "base,exp,expected",
    [
        (2, 3, 8),
        (5, 0, 1),
        (2, -1, 0.5),
        (10, 2, 100),
    ],
)
def test_power(base: float, exp: float, expected: float) -> None:
    assert Calculator().power(base, exp) == expected
