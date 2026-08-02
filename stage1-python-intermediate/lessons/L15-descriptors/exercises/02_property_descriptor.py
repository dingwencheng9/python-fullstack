"""
L13: 描述符 - 练习2: Property 描述符与类级访问

难度: ⭐⭐⭐ (较难)
预计时间: 35 分钟
知识点: property 描述符、类级访问、实例属性 vs 类属性

任务描述:
使用描述符实现一个类似 @property 的属性装饰器，并对比类级访问行为。
"""

from __future__ import annotations


# === 练习1: 实现 SimpleProperty 描述符 ===


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
            # 类级访问：Circle.radius 返回描述符对象本身
            return self
        return self.getter(obj)

    def __set__(self, obj, value):
        if self.setter is None:
            raise AttributeError(f"属性 '{self.name}' 是只读的")
        self.setter(obj, value)


# ========================================
# 👉 TODO 1: 使用 SimpleProperty 实现 Circle 类
# ========================================


class Circle:
    """圆形类，使用 SimpleProperty 描述符实现 radius 和 diameter 属性。"""

    def __init__(self, radius: float):
        # 👉 实现: 设置 _radius 属性
        self._radius = radius

    # 👉 实现: 使用 SimpleProperty 定义 radius 属性
    radius = SimpleProperty(lambda self: self._radius, lambda self, v: setattr(self, '_radius', v))

    # 👉 实现: 使用 SimpleProperty 定义 diameter 属性（只读，diameter = 2 * radius）
    diameter = SimpleProperty(lambda self: self._radius * 2)


# 验证区域
if __name__ == "__main__":
    c = Circle(5)
    assert c.radius == 5, f"radius 应为 5，实际为 {c.radius}"
    c.radius = 10
    assert c.radius == 10, f"radius 应为 10，实际为 {c.radius}"

    # diameter 是只读属性
    assert c.diameter == 20, f"diameter 应为 20，实际为 {c.diameter}"
    try:
        c.diameter = 30
        assert False, "diameter 应该只读"
    except AttributeError:
        pass

    print("✅ Circle 练习通过！")


# === 练习2: 类级访问 vs 实例级访问 ===


class AccessDemo:
    """演示描述符的类级访问与实例级访问行为差异。"""

    def __init__(self, value: int):
        self._value = value

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            # 类级访问：返回描述符对象（可用于元编程）
            return f"<ClassAccess: {self.name} (类级) = {self._value if hasattr(self, '_value') else '未绑定'}>"
        return f"<InstanceAccess: {self.name} (实例级) = {obj._value}>"

    def __set__(self, obj, value):
        obj._value = value


# ========================================
# 👉 TODO 2: 验证类级访问 vs 实例级访问行为
# ========================================

if __name__ == "__main__":
    # 👉 实现: 对比类级访问和实例级访问的返回值差异
    demo = AccessDemo(42)
    # 为了对比类级访问与实例级访问，把 descriptor 绑定到一个类属性上
    class Holder:
        value = demo

    # 类级访问（通过类名）
    class_access = Holder.value
    print("class_access:", class_access)

    # 实例级访问（通过实例）
    h = Holder()
    # 先给实例设置一个值（触发 __set__），以便实例级访问有可读值
    h.value = 100
    instance_access = h.value
    print("instance_access:", instance_access)

    # 观察：类级访问返回描述符提供的信息（obj 为 None），实例级访问返回绑定到实例的数据


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


# ========================================
# 👉 TODO 3: 实现带验证的描述符并理解优先级
# ========================================


class Product:
    """商品类，演示描述符优先级规则。

    Python 属性查找顺序（优先级从高到低）：
    1. 数据描述符（__get__ + __set__）← 最高
    2. 实例 __dict__
    3. 非数据描述符（只有 __get__）
    4. 类属性 / 父类属性
    """

    def __init__(self, price: float):
        # 👉 实现: 初始化价格（使用描述符进行验证）
        self.price = price


    # 实现 price 描述符（价格必须为非负数）
    @staticmethod
    def _validate_price(v):
        if not isinstance(v, (int, float)):
            raise ValueError("price 必须是数字")
        if v < 0:
            raise ValueError("price 不能为负数")
        return float(v)

    price = ValidatorDescriptor(validate_fn=_validate_price)
    # 类属性
    category = "General"


if __name__ == "__main__":
    # 测试验证功能
    # 创建 Product，验证正向用例
    p = Product(10.0)
    assert p.price == 10.0

    # 负数价格应被拒绝
    try:
        Product(-5)
        assert False, "负数价格应抛出异常"
    except ValueError:
        pass

    # 类属性与实例属性覆盖示例
    p2 = Product(20)
    assert p2.category == "General"
    # 覆盖实例属性
    p2.category = "Special"
    assert p2.category == "Special"

    print("✅ Product 验证与优先级实验通过！")
