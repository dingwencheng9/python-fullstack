"""Fraction 类参考答案 - 对应 exercises/01_fraction.py。"""

from __future__ import annotations

from math import gcd
from typing import override


class Fraction:
    """分数类，演示表示、比较和加法魔术方法。"""

    def __init__(self, numerator: int, denominator: int) -> None:
        if denominator == 0:
            raise ValueError("分母不能为零")

        common = gcd(abs(numerator), abs(denominator))
        sign = -1 if numerator * denominator < 0 else 1
        self.numerator = sign * abs(numerator) // common
        self.denominator = abs(denominator) // common

    @override
    def __repr__(self) -> str:
        return f"Fraction({self.numerator}, {self.denominator})"

    @override
    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return False
        return self.numerator == other.numerator and self.denominator == other.denominator

    @override
    def __hash__(self) -> int:
        return hash((self.numerator, self.denominator))

    def __add__(self, other: Fraction) -> Fraction:
        numerator = self.numerator * other.denominator + other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)
