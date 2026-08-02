"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L15: 描述符 - 描述符测试
"""

import pytest


def test_positive_descriptor():
    """测试正数验证描述符"""

    class Product:
        price = descriptors.Positive()

        def __init__(self):
            self.price = 100

    p = Product()
    assert p.price == 100


def test_positive_descriptor_negative():
    """测试正数描述符拒绝负数"""

    class Product:
        price = descriptors.Positive()

        def __init__(self):
            pass

    p = Product()
    with pytest.raises(ValueError, match="price 必须为正数"):
        p.price = -10


def test_range_descriptor():
    """测试范围描述符"""

    class Product:
        rating = descriptors.Range(0, 5)

        def __init__(self):
            self.rating = 4.5

    p = Product()
    assert p.rating == 4.5


def test_range_descriptor_out_of_bounds():
    """测试范围描述符越界"""

    class Product:
        rating = descriptors.Range(0, 5)

        def __init__(self):
            pass

    p = Product()
    with pytest.raises(ValueError, match="必须在 0 和 5 之间"):
        p.rating = 10


def test_lazy_descriptor():
    """测试延迟加载描述符"""
    call_count = 0

    class DataService:
        data = descriptors.Lazy()

        def _load_data(self):
            nonlocal call_count
            call_count += 1
            return {"loaded": True}

    service = DataService()
    # 第一次访问触发加载
    result1 = service.data
    assert result1 == {"loaded": True}
    assert call_count == 1

    # 第二次访问使用缓存
    result2 = service.data
    assert result2 == {"loaded": True}
    assert call_count == 1  # 不再调用加载方法


def test_upper_descriptor():
    """测试大写描述符"""

    class User:
        name = descriptors.Upper()

        def __init__(self):
            self.name = "john doe"

    user = User()
    assert user.name == "JOHN DOE"
    user.name = "jane doe"
    assert user.name == "JANE DOE"


def test_descriptor_class_access():
    """测试类级别访问描述符"""

    class Product:
        price = descriptors.Positive()

    # 通过类访问描述符对象本身
    assert isinstance(Product.price, descriptors.Positive)


def test_simple_property_descriptor():
    """测试 SimpleProperty 描述符（练习2）"""
    if property_desc is None:
        pytest.skip("solution_02_property 未实现")

    SimpleProperty = property_desc.SimpleProperty

    class Circle:
        def __init__(self, radius):
            self._radius = radius

        radius = SimpleProperty(
            getter=lambda self: self._radius,
            setter=lambda self, v: setattr(self, "_radius", v),
        )

        @property
        def diameter(self):
            return self._radius * 2

    c = Circle(5)
    assert c.radius == 5
    c.radius = 10
    assert c.radius == 10
    assert c.diameter == 20


def test_class_vs_instance_access():
    """测试类级访问与实例级访问的差异"""
    if property_desc is None:
        pytest.skip("solution_02_property 未实现")

    AccessDemo = property_desc.AccessDemo

    demo = AccessDemo(42)
    class_result = AccessDemo.value
    instance_result = demo.value

    # 类级访问返回描述符对象（字符串形式）
    assert hasattr(class_result, "name") and class_result.name == "value"
    # 实例级访问返回实际值
    assert instance_result == 42
