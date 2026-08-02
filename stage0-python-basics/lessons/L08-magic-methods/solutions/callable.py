"""Multiplier 类参考答案 - 对应 exercises/03_callable.py。"""

from typing import override


class Multiplier:
    """可调用乘法器，演示 __call__。"""

    def __init__(self, factor: float) -> None:
        self.factor = factor

    def __call__(self, x: float) -> float:
        return x * self.factor

    @override
    def __repr__(self) -> str:
        return f"Multiplier({self.factor})"
