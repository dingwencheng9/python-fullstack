"""Vector 类参考答案 - 演示常用魔法方法"""

from typing import override


class Vector:
    """二维向量类"""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        """向量加法：v1 + v2"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        """向量减法：v1 - v2"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        """标量乘法：v * 3"""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        """标量乘法（右侧）：3 * v"""
        return self * scalar

    @override
    def __eq__(self, other: object) -> bool:
        """相等比较：v1 == v2"""
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    @override
    def __hash__(self) -> int:
        """使对象可哈希"""
        return hash((self.x, self.y))

    @override
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    @override
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def magnitude(self) -> float:
        """向量长度"""
        result: float = (self.x**2 + self.y**2) ** 0.5
        return result
