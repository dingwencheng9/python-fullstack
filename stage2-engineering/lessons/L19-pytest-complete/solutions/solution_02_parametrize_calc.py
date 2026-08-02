"""练习 2 参考答案: 参数化计算器"""

from __future__ import annotations

import pytest


class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    def power(self, base: float, exp: float) -> float:
        return base**exp


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (100, -50, 50),
        (2.5, 3.5, 6.0),
    ],
)
def test_add(a, b, expected):
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
def test_divide(a, b, expected):
    assert Calculator().divide(a, b) == expected


def test_divide_by_zero():
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
def test_power(base, exp, expected):
    assert Calculator().power(base, exp) == expected
