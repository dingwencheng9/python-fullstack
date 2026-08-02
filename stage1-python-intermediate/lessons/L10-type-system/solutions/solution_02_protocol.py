"""
L10: 类型系统 - Protocol 练习解答

使用 Protocol 实现结构化类型检查。
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    """可绘制对象协议"""

    def draw(self) -> None: ...


@runtime_checkable
class Resizable(Protocol):
    """可调整大小对象协议"""

    def resize(self, width: int, height: int) -> None: ...


class Circle:
    """圆形"""

    def __init__(self, radius: int):
        self.radius = radius

    def draw(self) -> None:
        print(f"绘制圆形，半径: {self.radius}")

    def resize(self, width: int, height: int) -> None:
        # 忽略 width，只用 height 作为新半径
        self.radius = height


class Square:
    """正方形"""

    def __init__(self, side: int):
        self.side = side

    def draw(self) -> None:
        print(f"绘制正方形，边长: {self.side}")

    # 注意：Square 没有 resize 方法


def render_shapes(shapes: list[Drawable]) -> None:
    """渲染所有可绘制形状"""
    for shape in shapes:
        shape.draw()


def process_resizable(items: list[Resizable]) -> None:
    """处理所有可调整大小的对象"""
    for item in items:
        if isinstance(item, Resizable):
            item.resize(100, 100)
