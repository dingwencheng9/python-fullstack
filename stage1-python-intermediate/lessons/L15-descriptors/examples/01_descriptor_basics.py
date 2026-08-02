"""L13: 描述符 - 基础示例"""

# === Part 1: 描述符协议 ===


class Descriptor:
    """描述符基类"""

    def __set_name__(self, owner, name):
        """自动设置属性名"""
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f"_{self.name}", None)

    def __set__(self, obj, value):
        setattr(obj, f"_{self.name}", value)


class Person:
    name = Descriptor()
    age = Descriptor()

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


p = Person("Alice", 30)
print(f"姓名: {p.name}")
print(f"年龄: {p.age}")

# === Part 2: 数据描述符 vs 非数据描述符 ===


class DataDescriptor:
    """数据描述符 - __get__ + __set__"""

    def __init__(self):
        self._value = None

    def __get__(self, obj, objtype=None):
        print(f"[DataDescriptor.__get__] {self._value}")
        return self._value

    def __set__(self, obj, value):
        print(f"[DataDescriptor.__set__] {value}")
        self._value = value


class NonDataDescriptor:
    """非数据描述符 - 只有 __get__"""

    def __init__(self):
        self._value = None

    def __get__(self, obj, objtype=None):
        print(f"[NonDataDescriptor.__get__] {self._value}")
        return self._value


class Example:
    data = DataDescriptor()
    non_data = NonDataDescriptor()


e = Example()
print("设置前:")
print(f"  data = {e.data}")
print(f"  non_data = {e.non_data}")

print("\n设置属性值:")
e.data = "Hello"
e.non_data = "World"

print("\n设置后:")
print(f"  data = {e.data}")
print(f"  non_data = {e.non_data}")

# === Part 3: Property 描述符 ===


class Circle:
    """使用 @property 实现描述符"""

    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        """获取半径"""
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("半径不能为负数")
        self._radius = value

    @property
    def area(self) -> float:
        """计算面积"""
        import math

        return math.pi * self._radius**2

    @property
    def circumference(self) -> float:
        """计算周长"""
        import math

        return 2 * math.pi * self._radius


circle = Circle(5)
print(f"半径: {circle.radius}")
print(f"面积: {circle.area:.2f}")
print(f"周长: {circle.circumference:.2f}")

circle.radius = 10
print("\n半径改为 10 后:")
print(f"面积: {circle.area:.2f}")

try:
    circle.radius = -5
except ValueError as e:
    print(f"\n错误: {e}")

# === Part 4: 验证描述符 ===


class Range:
    """范围验证描述符"""

    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return getattr(obj, f"_{self.name}", None)

    def __set__(self, obj, value: float) -> None:
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"{self.name} 必须在 {self.min_val} 和 {self.max_val} 之间，得到 {value}")
        setattr(obj, f"_{self.name}", value)


class Student:
    score = Range(0, 100)
    attendance = Range(0, 100)

    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.attendance = 0


s = Student("Bob")
print(f"学生: {s.name}, 分数: {s.score}")

s.score = 95
print(f"更新分数: {s.score}")

try:
    s.score = 150
except ValueError as e:
    print(f"错误: {e}")

# === Part 5: Lazy Loading 描述符 ===


class Lazy:
    """延迟加载描述符"""

    def __init__(self, func):
        self.func = func
        self.attr_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.cache_attr = f"_lazy_{name}_cache"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        # 检查缓存
        if hasattr(obj, self.cache_attr):
            return getattr(obj, self.cache_attr)

        # 计算并缓存
        value = self.func(obj)
        setattr(obj, self.cache_attr, value)
        return value


class Config:
    def __init__(self):
        self._data = {"db_host": "localhost", "db_port": 5432}

    @Lazy
    def connection_string(self) -> str:
        """延迟计算的属性"""
        print("[计算 connection_string...]")
        return f"postgresql://{self._data['db_host']}:{self._data['db_port']}"

    @Lazy
    def max_connections(self) -> int:
        """另一个延迟属性"""
        print("[计算 max_connections...]")
        return 100


config = Config()
print("Config 创建完成")

print("\n第一次访问:")
print(f"连接字符串: {config.connection_string}")

print("\n第二次访问（使用缓存）:")
print(f"连接字符串: {config.connection_string}")

print("\n访问另一个延迟属性:")
print(f"最大连接数: {config.max_connections}")

print("\n=== 描述符基础示例完成 ===")
