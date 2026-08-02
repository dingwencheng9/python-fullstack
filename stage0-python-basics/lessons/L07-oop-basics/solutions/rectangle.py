"""Rectangle 类参考答案"""


class Rectangle:
    """矩形类"""

    def __init__(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("宽和高必须为正数")
        self.width = width
        self.height = height

    def area(self) -> float:
        """计算面积"""
        return self.width * self.height

    def perimeter(self) -> float:
        """计算周长"""
        return 2 * (self.width + self.height)
