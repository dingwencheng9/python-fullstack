"""示例2: 算术运算符魔法方法"""

from __future__ import annotations


class Point:
    """演示 + - * / 运算符"""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Point) -> Point:
        """p1 + p2"""
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        """p1 - p2"""
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Point:
        """p * 2"""
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Point:
        """2 * p"""
        return self * scalar

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


# 演示
p1 = Point(1, 2)
p2 = Point(3, 4)

print(f"p1 + p2 = {p1 + p2}")  # Point(4.0, 6.0)
print(f"p2 - p1 = {p2 - p1}")  # Point(2.0, 2.0)
print(f"p1 * 3 = {p1 * 3}")  # Point(3.0, 6.0)
print(f"2 * p1 = {2 * p1}")  # Point(2.0, 4.0)
