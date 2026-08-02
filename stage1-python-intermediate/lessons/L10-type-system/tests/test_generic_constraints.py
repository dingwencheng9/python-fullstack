"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L10: 类型系统 - 泛型约束测试
"""

import pytest



def test_container_basic():
    """测试泛型容器基本功能"""
    container = generic_constraints.Container(value=42)
    assert container.get() == 42
    container.set(100)
    assert container.get() == 100


def test_container_with_string():
    """测试字符串容器"""
    container = generic_constraints.Container(value="hello")
    assert container.get() == "hello"


def test_number_box_int():
    """测试整数容器"""
    box = generic_constraints.NumberBox(value=10)
    assert box.get() == 10
    result = box.add(5)
    assert result.get() == 15


def test_number_box_float():
    """测试浮点数容器"""
    box = generic_constraints.NumberBox(value=3.14)
    assert box.get() == pytest.approx(3.14)
    result = box.multiply(2)
    assert result.get() == pytest.approx(6.28)


def test_number_box_invalid_type():
    """测试无效类型"""
    with pytest.raises(TypeError):
        generic_constraints.NumberBox(value="not a number")


def test_merge_containers():
    """测试合并同类型容器"""
    a = generic_constraints.Container(value=1)
    b = generic_constraints.Container(value=2)
    result = generic_constraints.merge_containers(a, b)
    assert result == [1, 2]
