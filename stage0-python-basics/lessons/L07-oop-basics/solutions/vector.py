"""Vector 类参考答案"""


class Vector:
    """二维向量类"""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def length(self) -> float:
        """计算向量长度（勾股定理）"""
        return (self.x**2 + self.y**2) ** 0.5

    def dot(self, other: "Vector") -> float:
        """计算点积"""
        return self.x * other.x + self.y * other.y

    def scale(self, factor: float) -> "Vector":
        """缩放向量"""
        return Vector(self.x * factor, self.y * factor)
