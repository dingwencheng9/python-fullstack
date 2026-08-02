"""计算器模块"""


def add(a: float, b: float) -> float:
    """加法"""
    return a + b


def subtract(a: float, b: float) -> float:
    """减法"""
    return a - b


def multiply(a: float, b: float) -> float:
    """乘法"""
    return a * b


def divide(a: float, b: float) -> float | None:
    """除法（除数为0时返回None）"""
    if b == 0:
        return None
    return a / b
