"""
L10: 类型系统 - Protocol 结构化类型测试
"""

import pytest

protocol = None  # type: ignore[assignment]


@pytest.fixture(autouse=True)
def _inject_protocol(solutions, request) -> None:
    """注入 protocol 模块（solution_02_protocol）到测试命名空间。"""
    try:
        request.module.__dict__["protocol"] = getattr(solutions, "solution_02_protocol")
    except (AttributeError, ImportError) as e:
        pytest.fail(f"无法导入 solution_02_protocol: {e}")


def test_circle_is_drawable():
    """测试 Circle 实现了 Drawable 协议"""
    circle = protocol.Circle(radius=5)
    assert isinstance(circle, protocol.Drawable)


def test_circle_is_resizable():
    """测试 Circle 实现了 Resizable 协议"""
    circle = protocol.Circle(radius=5)
    assert isinstance(circle, protocol.Resizable)


def test_square_is_drawable():
    """测试 Square 实现了 Drawable 协议"""
    square = protocol.Square(side=10)
    assert isinstance(square, protocol.Drawable)


def test_square_not_resizable():
    """测试 Square 没有实现 Resizable 协议"""
    square = protocol.Square(side=10)
    assert not isinstance(square, protocol.Resizable)


def test_render_shapes():
    """测试渲染多个形状"""
    shapes = [
        protocol.Circle(radius=5),
        protocol.Square(side=10),
    ]
    # 不应抛出异常
    protocol.render_shapes(shapes)


def test_process_resizable_only_circle():
    """测试只处理可调整大小的对象"""
    shapes = [protocol.Circle(radius=5)]
    # 不应抛出异常
    protocol.process_resizable(shapes)


def test_process_resizable_raises():
    """测试处理包含不可调整大小的对象时正确跳过"""
    shapes = [
        protocol.Circle(radius=5),
        protocol.Square(side=10),  # Square 没有 resize 方法，isinstance 返回 False
    ]
    # process_resizable 使用 isinstance 检查，不会抛 AttributeError
    protocol.process_resizable(shapes)
