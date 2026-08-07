"""
L15: 描述符 - 练习2: Property 描述符与类级访问 - 参考答案
"""

from __future__ import annotations


# === 练习1: SimpleProperty 描述符实现 ===


class SimpleProperty:
    """简易 property 描述符实现。

    等价于内建 @property，但完整展示了描述符协议的工作原理。

    用法示例:
        class Circle:
            radius = SimpleProperty(lambda self: self._radius,
                                    lambda self, v: setattr(self, '_radius', v))
    """

    def __init__(self, getter, setter=None):
        self.getter = getter
        self.setter = setter

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.getter(obj)

    def __set__(self, obj, value):
        if self.setter is None:
            raise AttributeError(f"属性 '{self.name}' 是只读的")
        self.setter(obj, value)


class Circle:
    """圆形类，使用 SimpleProperty 描述符实现 radius 属性。"""

    def __init__(self, radius: float):
        self._radius = radius

    radius = SimpleProperty(
        getter=lambda self: self._radius,
        setter=lambda self, v: setattr(self, "_radius", v),
    )

    @property
    def diameter(self):
        return self._radius * 2


# === 练习2: 类级访问 vs 实例级访问 ===


class _AccessDemoDescriptor:
    """AccessDemo 的 value 描述符。单独定义以避免实例混淆。"""

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            # 类级访问：返回描述符对象本身
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        setattr(obj, self.storage, value)


class AccessDemo:
    """演示描述符的类级访问与实例级访问行为差异。"""

    # 类体内定义：Python 会自动调用 __set_name__(AccessDemo, "value")
    value = _AccessDemoDescriptor()

    def __init__(self, value: int):
        self.value = value


def demonstrate_access_patterns():
    """演示类级访问与实例级访问的行为差异。"""
    demo = AccessDemo(42)

    # 类级访问：返回描述符对象本身
    class_access = AccessDemo.value
    print(f"类级访问: {class_access}")
    # 输出: <_AccessDemoDescriptor object at 0x...>

    # 实例级访问：返回实例的实际值
    instance_access = demo.value
    print(f"实例级访问: {instance_access}")
    # 输出: 42

    # 验证类型差异
    assert isinstance(AccessDemo.value, _AccessDemoDescriptor)
    assert demo.value == 42


# === 练习3: 描述符优先级与继承 ===


class BaseDescriptor:
    """数据描述符基类。"""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f"_{self.name}", None)

    def __set__(self, obj, value):
        setattr(obj, f"_{self.name}", value)


class ValidatorDescriptor(BaseDescriptor):
    """带验证的描述符。"""

    def __init__(self, validate_fn=None):
        self.validate_fn = validate_fn or (lambda x: x)

    def __set__(self, obj, value):
        validated = self.validate_fn(value)
        super().__set__(obj, validated)


def _validate_non_negative(value):
    """验证值必须 >= 0。"""
    if value < 0:
        raise ValueError("price 必须 >= 0")
    return value


class Product:
    """商品类，演示描述符优先级规则。

    Python 属性查找顺序（优先级从高到低）：
    1. 数据描述符（__get__ + __set__）← 最高
    2. 实例 __dict__
    3. 非数据描述符（只有 __get__）
    4. 类属性 / 父类属性
    """

    price = ValidatorDescriptor(validate_fn=_validate_non_negative)
    category = "General"

    def __init__(self, price: float):
        self.price = price


if __name__ == "__main__":
    # 验证练习1
    c = Circle(5)
    assert c.radius == 5
    c.radius = 10
    assert c.radius == 10
    assert c.diameter == 20
    try:
        c.diameter = 30  # property 只读
        assert False
    except AttributeError:
        pass
    print("✅ Circle 练习通过！")

    # 验证练习2
    demonstrate_access_patterns()
    print("✅ 类级/实例级访问练习通过！")

    # 验证练习3
    p = Product(99.9)
    assert p.price == 99.9
    try:
        Product(price=-10)
        assert False
    except ValueError as e:
        assert ">= 0" in str(e)
    print("✅ 描述符优先级练习通过！")
