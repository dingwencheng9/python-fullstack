"""
L13: 描述符 - 描述符练习解答

实现各种描述符。
"""

from typing import Any


class Validator:
    """值验证描述符基类"""

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

    def validate(self, value: Any) -> None:
        """子类重写此方法实现验证逻辑"""


class Positive(Validator):
    """正数验证"""

    def validate(self, value: Any) -> None:
        if value < 0:
            raise ValueError(f"{self.name} 必须为正数")


class Range:
    """范围验证描述符"""

    def __init__(self, min_val: float, max_val: float):
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
        # 触发延迟加载：调用 owner 的 _load_<name> 方法
        load_method = f"_load_{self.name}"
        if hasattr(obj, load_method):
            value = getattr(obj, load_method)()
            setattr(obj, self.cache_attr, value)
            return value
        raise AttributeError(f"对象 {obj.__class__.__name__} 没有 {load_method} 方法")

    def __set__(self, obj, value):
        setattr(obj, self.cache_attr, value)


class Upper:
    """大写字符串描述符"""

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, "").upper()

    def __set__(self, obj, value):
        setattr(obj, self.storage, str(value).upper())
