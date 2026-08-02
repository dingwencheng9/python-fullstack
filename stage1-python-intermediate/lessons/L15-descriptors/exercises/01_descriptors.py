"""
L13: 描述符 - 描述符练习

实现各种类型的描述符。
"""


class Validator:
    """值验证描述符。

    子类通过重写 ``validate()`` 实现具体校验逻辑，基类负责
    描述符协议和实例属性存储。
    """

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.storage, value)

    def validate(self, value):
        """验证 value。默认不做限制，由子类按需重写。"""


class Positive(Validator):
    """正数验证"""

    def validate(self, value):
        if value < 0:
            raise ValueError(f"{self.name} 必须为正数")


class Range:
    """范围验证描述符"""

    def __init__(self, min_val, max_val):
        if min_val > max_val:
            raise ValueError("min_val 不能大于 max_val")
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        if value < self.min_val or value > self.max_val:
            raise ValueError(f"{self.name} 必须在 {self.min_val} 和 {self.max_val} 之间")
        setattr(obj, self.storage, value)


class Lazy:
    """延迟加载描述符"""

    def __set_name__(self, owner, name):
        self.name = name
        self.cache_attr = f"_lazy_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if hasattr(obj, self.cache_attr):
            return getattr(obj, self.cache_attr)

        load_method_name = f"_load_{self.name}"
        if not hasattr(obj, load_method_name):
            raise AttributeError(f"对象 {obj.__class__.__name__} 没有 {load_method_name} 方法")

        value = getattr(obj, load_method_name)()
        setattr(obj, self.cache_attr, value)
        return value

    def __set__(self, obj, value):
        setattr(obj, self.cache_attr, value)


# === 验证 ===

if __name__ == "__main__":

    class Product:
        price = Positive()
        quantity = Positive()
        rating = Range(0, 5)

        def __init__(self):
            self.price = 100
            self.quantity = 10
            self.rating = 4.5

    p = Product()
    assert p.price == 100
    assert p.quantity == 10
    assert p.rating == 4.5

    # 测试验证
    try:
        p.price = -10
        assert False, "应该抛出异常"
    except ValueError:
        pass

    try:
        p.rating = 6
        assert False, "应该抛出异常"
    except ValueError:
        pass

    class DataService:
        data = Lazy()

        def __init__(self):
            self.load_count = 0

        def _load_data(self):
            self.load_count += 1
            return {"loaded": True}

    service = DataService()
    assert service.data == {"loaded": True}
    assert service.data == {"loaded": True}
    assert service.load_count == 1

    print("✅ 所有测试通过！")
