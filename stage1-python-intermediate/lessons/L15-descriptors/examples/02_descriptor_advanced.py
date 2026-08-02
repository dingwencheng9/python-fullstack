"""L13: 描述符 - 高级示例"""

# === Part 1: 函数作为非数据描述符 ===


class Property:
    """手写 Property 描述符"""

    def __init__(self, getter=None, setter=None, deleter=None):
        self.getter = getter
        self.setter = setter
        self.deleter = deleter
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.getter is None:
            raise AttributeError(f"未定义 getter for {self.name}")
        return self.getter(obj)

    def __set__(self, obj, value):
        if self.setter is None:
            raise AttributeError(f"未定义 setter for {self.name}")
        self.setter(obj, value)

    def setter_method(self, setter):
        self.setter = setter
        return self

    def deleter_method(self, deleter):
        self.deleter = deleter
        return self


# 使用示例
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    def _get_celsius(self) -> float:
        return self._celsius

    def _set_celsius(self, value: float) -> None:
        self._celsius = value

    def _get_fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    def _set_fahrenheit(self, value: float) -> None:
        self._celsius = (value - 32) * 5 / 9

    celsius = Property(_get_celsius, _set_celsius)
    fahrenheit = Property(_get_fahrenheit, _set_fahrenheit)


t = Temperature(25)
print(f"摄氏: {t.celsius}°C = 华氏: {t.fahrenheit}°F")

t.fahrenheit = 100
print(f"华氏 100°F = 摄氏 {t.celsius}°C")

# === Part 2: 描述符与类属性交互 ===


class RevealAccess:
    """揭示访问模式的描述符"""

    def __init__(self, init_val=None, name=None):
        self.name = name
        self.default = init_val
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name, self.default)

    def __set__(self, obj, value):
        print(f"[设置 {self.name} = {value}]")
        setattr(obj, self.storage_name, value)


class Point:
    x = RevealAccess(0, "x")
    y = RevealAccess(0, "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


p = Point(1, 2)
print(f"\n创建点: {p}")
p.x = 10
print(f"修改后: {p}")
print(f"访问 x: {p.x}")

# === Part 3: __getattribute__ 与描述符 ===


class AutomaticLog:
    """自动日志描述符"""

    def __init__(self):
        self.storage = {}

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.name not in obj.__dict__:
            raise AttributeError(f"属性 '{self.name}' 未初始化")
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        print(f"[日志] 设置 {self.name} = {value!r}")
        obj.__dict__[self.name] = value


class User:
    name = AutomaticLog()
    email = AutomaticLog()

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


u = User("Alice", "alice@example.com")
print("\n初始化后:")
u.email = "new_email@example.com"
print(f"获取: {u.name}")

# === Part 4: 描述符优先级链 ===


class Upper:
    """字符串大写描述符"""

    def __set_name__(self, owner, name):
        self.storage = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.storage, "").upper()

    def __set__(self, obj, value):
        setattr(obj, self.storage, str(value))


class FormField:
    """表单字段"""

    name = Upper()
    email = Upper()

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


form = FormField("john doe", "JOHN@EXAMPLE.COM")
print(f"\n表单名: {form.name}")
print(f"表单邮箱: {form.email}")

# 设置小写，自动转大写
form.name = "jane doe"
print(f"更新后: {form.name}")

# === Part 5: 描述符与元类 ===


class ValidatedDescriptor:
    """带验证的描述符"""

    def __init__(self, validator):
        self.validator = validator
        self.name = None
        self.storage = None

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        validated = self.validator(value)
        setattr(obj, self.storage, validated)


def positive_int(value):
    """验证正整数"""
    if not isinstance(value, int):
        raise TypeError("必须为整数")
    if value <= 0:
        raise ValueError("必须为正数")
    return value


def email_format(value):
    """验证邮箱格式"""
    if "@" not in value:
        raise ValueError("邮箱格式无效")
    return value.lower()


class Product:
    quantity = ValidatedDescriptor(positive_int)
    sku = ValidatedDescriptor(email_format)  # 复用验证器

    def __init__(self, quantity: int, sku: str):
        self.quantity = quantity
        self.sku = sku


p = Product(10, "ABC@EXAMPLE.COM")
print(f"\n产品: qty={p.quantity}, sku={p.sku}")

try:
    p.quantity = -5
except ValueError as e:
    print(f"错误: {e}")

print("\n=== 描述符高级示例完成 ===")
