# L15: 描述符与属性

> **课程编号**: L15  
> **所属阶段**: Stage 1 - Python 进阶  
> **预计时长**: 5 小时  
> **难度**: ⭐⭐⭐⭐☆（中高级）  
> **前置课程**: L13 Python 高级特性（入门）  
> **版本**: v1.0
> **最后更新**: 2026-08-07
> **学习目标**: 掌握描述符协议、property 装饰器、自定义属性访问控制

---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ 理解 Python 描述符协议（`__get__`、`__set__`、`__delete__`）
2. ✅ 掌握 `property` 装饰器的实现原理
3. ✅ 创建自定义描述符实现数据验证、转换、懒加载
4. ✅ 理解 `__getattr__` 和 `__getattribute__` 的区别
5. ✅ 设计安全的属性访问模式

---

## 📚 核心内容

### Part 1: 描述符协议简介

#### 1.1 什么是描述符？

描述符是**实现了描述符协议的对象**，可以控制对另一个对象属性的访问。

```python
class Descriptor:
    """描述符基类"""
    def __get__(self, obj, objtype=None):
        ...

    def __set__(self, obj, value):
        ...

    def __delete__(self, obj):
        ...
```

**描述符协议方法：**
| 方法 | 调用时机 | 作用 |
|------|----------|------|
| `__get__` | 读取属性 | 返回属性值 |
| `__set__` | 赋值属性 | 设置属性值 |
| `__delete__` | 删除属性 | 删除属性 |
| `__set_name__` | 类创建时 | 获取属性名（Python 3.6+） |

---

#### 1.2 数据描述符 vs 非数据描述符

**数据描述符（Data Descriptor）**：实现了 `__set__` 和/或 `__delete__`
- 优先级最高，总是覆盖实例字典

**非数据描述符（Non-data Descriptor）**：只实现了 `__get__`
- 如函数、方法、`classmethod`、`staticmethod`
- 优先级低于实例字典

```python
# 数据描述符：实现 __set__
class DataDescriptor:
    def __get__(self, obj, objtype=None):
        print("__get__ called")
        return getattr(obj, '_value', None)

    def __set__(self, obj, value):
        print(f"__set__ called with {value}")
        obj._value = value

# 非数据描述符：只实现 __get__
class NonDataDescriptor:
    def __get__(self, obj, objtype=None):
        print("__get__ called")
        return getattr(obj, '_cached', None)

# 优先级：数据描述符 > 实例字典 > 非数据描述符
```

---

### Part 2: property 装饰器

#### 2.1 property 的本质

`property` 是 Python 内置的数据描述符：

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    @property
    def radius(self) -> float:
        """半径（只读）"""
        return self._radius

    @property
    def diameter(self) -> float:
        """直径（自动计算）"""
        return self._radius * 2

    @property
    def area(self) -> float:
        """面积（自动计算）"""
        import math
        return math.pi * self._radius ** 2

circle = Circle(5)
print(circle.radius)    # 5
print(circle.diameter)  # 10
print(circle.area)      # 78.54
```

---

#### 2.2 setter 和 deleter

```python
class Temperature:
    def __init__(self, celsius: float = 0) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value

    @celsius.deleter
    def celsius(self) -> None:
        print("删除温度值")
        self._celsius = 0

temp = Temperature(25)
print(temp.celsius)  # 25

temp.celsius = 30
print(temp.celsius)  # 30

temp.celsius = -300  # ValueError!

del temp.celsius     # 删除温度值
```

---

#### 2.3 property 工厂函数

```python
def validate_range(min_val: float, max_val: float):
    """创建带验证的范围属性"""
    def decorator(func):
        private_name = f"__{func.__name__}"

        @property
        def prop(self) -> float:
            return getattr(self, private_name, min_val)

        @prop.setter
        def prop(self, value: float) -> None:
            if not (min_val <= value <= max_val):
                raise ValueError(f"值必须在 {min_val} 到 {max_val} 之间")
            setattr(self, private_name, value)

        return prop

    return decorator

class Slider:
    @validate_range(0, 100)
    def value(self) -> float:
        pass

slider = Slider()
slider.value = 50   # ✅
slider.value = 150  # ValueError!
```

---

### Part 3: 自定义描述符实战

#### 3.1 验证描述符

```python
class Validated(Descriptor):
    """验证描述符基类"""

    def __init__(self, name: str | None = None) -> None:
        self.name = name
        self.private_name = f"__{name}" if name else None

    def __set_name__(self, owner, name):
        """Python 3.6+ 自动获取属性名"""
        self.name = name
        self.private_name = f"_{owner.__name__}__{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    def validate(self, value):
        """子类实现验证逻辑"""
        raise NotImplementedError

class Integer(Validated):
    """整数验证描述符"""

    def __init__(self, min_val: int | None = None, max_val: int | None = None, **kwargs):
        super().__init__(**kwargs)
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"需要整数，得到 {type(value).__name__}")
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"值不能小于 {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"值不能大于 {self.max_val}")

class String(Validated):
    """字符串验证描述符"""

    def __init__(self, min_len: int = 0, max_len: int = 255, pattern: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.min_len = min_len
        self.max_len = max_len
        self.pattern = pattern

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"需要字符串，得到 {type(value).__name__}")
        if len(value) < self.min_len:
            raise ValueError(f"长度不能小于 {self.min_len}")
        if len(value) > self.max_len:
            raise ValueError(f"长度不能大于 {self.max_len}")
        if self.pattern:
            # 简化验证：仅检查基本结构（完整正则支持见 L16）
            # pattern 示例: "email" → 检查包含 @ 和 .
            if self.pattern == "email":
                if "@" not in value or "." not in value.split("@")[-1]:
                    raise ValueError(f"不符合 email 格式")

# 使用示例
class User:
    age = Integer(min_val=0, max_val=150)
    name = String(min_len=2, max_len=50)
    email = String(min_len=5, max_len=100, pattern="email")

    def __init__(self, name: str, age: int, email: str) -> None:
        self.name = name
        self.age = age
        self.email = email

user = User("Alice", 25, "alice@example.com")
print(user.name, user.age, user.email)

user.age = -5   # ValueError!
user.name = "A" # ValueError!
```

---

#### 3.2 懒加载描述符

```python
class Lazy:
    """懒加载描述符 - 首次访问时才初始化"""

    def __init__(self, init_func):
        self.init_func = init_func
        self.private_name = None
        self.attr_name = None

    def __set_name__(self, owner, name):
        self.attr_name = name
        self.private_name = f"_{name}_lazy"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        if not hasattr(obj, self.private_name):
            # 首次访问，执行初始化
            value = self.init_func(obj)
            setattr(obj, self.private_name, value)

        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        raise AttributeError(f"{self.attr_name} 是只读的")

class DatabaseConnection:
    """数据库连接类"""
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def _connect(self):
        """模拟连接数据库"""
        print(f"连接数据库: {self.dsn}")
        return {"connected": True, "dsn": self.dsn}

    connection = Lazy(_connect)  # 首次访问时才连接

db = DatabaseConnection("postgresql://localhost/mydb")
print("对象已创建，但尚未连接")

conn = db.connection  # 触发连接
print(f"连接状态: {conn}")

conn2 = db.connection  # 使用缓存的连接
```

---

#### 3.3 日志描述符

```python
import logging
from functools import cached_property

class Logged:
    """日志记录描述符"""

    def __init__(self, name: str | None = None) -> None:
        self.name = name
        self.private_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"__{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        value = getattr(obj, self.private_name, None)
        logger = logging.getLogger(obj.__class__.__name__)
        logger.debug(f"读取 {self.name} = {value}")
        return value

    def __set__(self, obj, value):
        logger = logging.getLogger(obj.__class__.__name__)
        logger.debug(f"设置 {self.name} = {value}")
        setattr(obj, self.private_name, value)

class User:
    name = Logged()
    email = Logged()

    def __init__(self, name: str, email: str) -> None:
        self.name = name  # 日志: 设置 name = Alice
        self.email = email

    def __repr__(self) -> str:
        return f"User(name={self.name!r}, email={self.email!r})"

# 配置日志
logging.basicConfig(level=logging.DEBUG)
user = User("Alice", "alice@example.com")
print(user.name)  # 日志: 读取 name = Alice
```

---

### Part 4: `__getattr__` vs `__getattribute__`

#### 4.1 区别对比

| 方法 | 调用时机 | 行为 |
|------|----------|------|
| `__getattribute__` | 访问任何属性 | 拦截所有属性访问 |
| `__getattr__` | 属性不存在时 | 仅拦截不存在的属性 |

```python
class Example:
    def __init__(self):
        self.regular_attr = "regular"

    def __getattr__(self, name):
        """仅当属性不存在时调用"""
        print(f"__getattr__ called for: {name}")
        raise AttributeError(f"属性 {name} 不存在")

    def __getattribute__(self, name):
        """拦截所有属性访问"""
        print(f"__getattribute__ called for: {name}")
        return super().__getattribute__(name)

obj = Example()
print(obj.regular_attr)  # __getattribute__ called
print(obj.missing)       # __getattribute__ then __getattr__ called
```

---

#### 4.2 组合使用

```python
class DynamicAttributes:
    """动态属性类"""

    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, name: str):
        """访问不存在的属性时，从 _data 中查找"""
        if name.startswith('_'):
            raise AttributeError(name)
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"属性 {name} 不存在")

    def __setattr__(self, name: str, value) -> None:
        """支持动态设置属性"""
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

# 使用
obj = DynamicAttributes({"name": "Alice", "age": 25})
print(obj.name)  # Alice
print(obj.age)   # 25

obj.city = "Beijing"  # 动态添加
print(obj.city)      # Beijing
```

---

#### 4.3 `__getattribute__` 的陷阱

```python
class Broken:
    def __getattribute__(self, name: str):
        # ❌ 错误：直接访问 self.name 会递归调用 __getattribute__
        return self.name + "!"  # 无限递归！

    def __getattribute__(self, name: str):
        # ✅ 正确：使用 super() 绕过描述符协议
        return super().__getattribute__(name) + "!"

class Safe:
    def __getattribute__(self, name: str):
        # 使用 super() 安全地访问属性
        value = super().__getattribute__(name)
        # 可以对值进行转换
        if isinstance(value, str):
            return value.upper()
        return value
```

---

### Part 5: 描述符与装饰器的结合

#### 5.1 组合 property 和验证

```python
class ValidatedProperty:
    """验证属性组合器"""

    def __init__(self, validator):
        self.validator = validator
        self.func = None

    def __call__(self, func):
        self.func = func
        return self

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func(obj)

    def __set__(self, obj, value):
        self.validator(value)
        if self.func:
            self.func.__set__(obj, value)

def validate_positive(value):
    if value <= 0:
        raise ValueError("值必须为正数")

class Counter:
    @ValidatedProperty(validate_positive)
    def count(self):
        return getattr(self, '__count', 0)

    @count.setter
    def count(self, value):
        self.__count = value

counter = Counter()
counter.count = 5
print(counter.count)  # 5

counter.count = -1  # ValueError!
```

---

#### 5.2 观察者模式

```python
class Observable:
    """可观察属性"""

    def __init__(self):
        self.observers: list[callable] = []

    def add_observer(self, callback: callable) -> None:
        self.observers.append(callback)

    def notify(self, obj, old_value, new_value) -> None:
        for observer in self.observers:
            observer(obj, old_value, new_value)

class ObservableDescriptor:
    """可观察描述符"""

    def __init__(self, observable: Observable):
        self.observable = observable
        self.name = None
        self.private_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        old_value = getattr(obj, self.private_name, None)
        setattr(obj, self.private_name, value)
        self.observable.notify(obj, old_value, value)

# 观察者回调
def on_value_change(obj, old, new):
    print(f"值从 {old} 变为 {new}")

observable = Observable()
observable.add_observer(on_value_change)

class Product:
    price = ObservableDescriptor(observable)

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

product = Product("iPhone", 9999)
product.price = 8999  # 输出: 值从 9999 变为 8999
```

---

### Part 6: 描述符高级应用（进阶）

> ⚠️ **进阶内容**：本节属于高级应用，初学者可先完成练习后再深入学习。

#### 6.1 数据库字段映射

```python
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

T = TypeVar("T")

class Field(ABC):
    """数据库字段基类"""

    def __init__(self, column_name: str, nullable: bool = True, default: Any = None):
        self.column_name = column_name
        self.nullable = nullable
        self.default = default

    @abstractmethod
    def validate(self, value: Any) -> Any:
        """验证并转换值"""
        ...

    @abstractmethod
    def to_sql(self) -> str:
        """生成 SQL 定义"""
        ...

class StringField(Field):
    """字符串字段"""

    def __init__(self, column_name: str, max_length: int = 255, **kwargs):
        super().__init__(column_name, **kwargs)
        self.max_length = max_length

    def validate(self, value: Any) -> str | None:
        if value is None:
            if not self.nullable:
                raise ValueError(f"字段 {self.column_name} 不能为空")
            return None
        return str(value)[:self.max_length]

    def to_sql(self) -> str:
        nullable = "" if self.nullable else " NOT NULL"
        default = f" DEFAULT '{self.default}'" if self.default else ""
        return f"{self.column_name} VARCHAR({self.max_length}){nullable}{default}"

class IntField(Field):
    """整数字段"""

    def __init__(self, column_name: str, auto_increment: bool = False, **kwargs):
        super().__init__(column_name, **kwargs)
        self.auto_increment = auto_increment

    def validate(self, value: Any) -> int | None:
        if value is None:
            if not self.nullable:
                raise ValueError(f"字段 {self.column_name} 不能为空")
            return None
        return int(value)

    def to_sql(self) -> str:
        nullable = "" if self.nullable else " NOT NULL"
        auto = " AUTO_INCREMENT" if self.auto_increment else ""
        return f"{self.column_name} INT{auto}{nullable}"

class ModelMeta(type):
    """模型元类：收集字段定义"""

    def __new__(mcs, name: bases, attrs):
        cls = super().__new__(mcs, name, attrs)
        cls._fields = {}

        # 收集所有 Field 描述符
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                attr_value.name = attr_name
                cls._fields[attr_name] = attr_value

        return cls

class Model(metaclass=ModelMeta):
    """模型基类"""

    _fields: dict[str, Field]

    def __init__(self, **kwargs):
        for field_name, field in self._fields.items():
            value = kwargs.get(field_name, field.default)
            setattr(self, field_name, field.validate(value))

    @classmethod
    def create_table_sql(cls) -> str:
        """生成建表 SQL"""
        columns = [field.to_sql() for field in cls._fields.values()]
        return f"CREATE TABLE {cls.__name__} (\n  " + ",\n  ".join(columns) + "\n)"

class User(Model):
    """用户模型"""
    id = IntField("id", auto_increment=True, nullable=False)
    name = StringField("name", max_length=100, nullable=False)
    email = StringField("email", max_length=255)
    age = IntField("age", default=0)

# 使用示例
user = User(name="Alice", email="alice@example.com", age=25)
print(f"用户: {user.name}, {user.email}, {user.age}")
print(User.create_table_sql())
```

#### 6.2 依赖注入容器

```python
from typing import Callable, Any, get_type_hints

class Inject:
    """依赖注入描述符"""

    def __init__(self, factory: Callable[[], Any]):
        self.factory = factory
        self._instance = None

    def __get__(self, obj, objtype=None):
        if self._instance is None:
            self._instance = self.factory()
        return self._instance

    def __set__(self, obj, value):
        raise AttributeError("依赖项不能直接赋值")

class Container:
    """依赖注入容器"""

    def __init__(self) -> None:
        self._factories: dict[str, Callable] = {}
        self._singletons: dict[str, Any] = {}

    def register(self, interface: type, factory: Callable, singleton: bool = True):
        """注册依赖"""
        self._factories[interface.__name__] = (factory, singleton)

    def resolve(self, interface: type) -> Any:
        """解析依赖"""
        name = interface.__name__
        if name not in self._factories:
            raise ValueError(f"未注册的依赖: {name}")

        factory, singleton = self._factories[name]

        if singleton:
            if name not in self._singletons:
                self._singletons[name] = factory()
            return self._singletons[name]
        else:
            return factory()

# 使用示例
container = Container()

# 注册服务
class DatabaseService:
    def query(self, sql: str):
        print(f"执行 SQL: {sql}")

class CacheService:
    def get(self, key: str):
        return None

    def set(self, key: str, value):
        print(f"缓存: {key} = {value}")

container.register(DatabaseService, lambda: DatabaseService())
container.register(CacheService, lambda: CacheService())

class UserService:
    db: Inject = Inject(lambda: container.resolve(DatabaseService))
    cache: Inject = Inject(lambda: container.resolve(CacheService))

    def get_user(self, user_id: int):
        # 使用注入的依赖
        cached = self.cache.get(f"user:{user_id}")
        if cached:
            return cached

        user = self.db.query(f"SELECT * FROM users WHERE id={user_id}")
        self.cache.set(f"user:{user_id}", user)
        return user

user_service = UserService()
user_service.get_user(1)
```

#### 6.3 特性测试框架

```python
import time
from functools import wraps

class timed_property:
    """计时属性描述符"""

    def __init__(self, func):
        self.func = func
        self.cache_name = f"_cached_{func.__name__}"
        self.time_name = f"_time_{func.__name__}"

    def __get__(self, obj, objtype=None):
        if not hasattr(obj, self.cache_name):
            # 首次访问，计算并缓存
            start = time.perf_counter()
            result = self.func(obj)
            elapsed = time.perf_counter() - start

            setattr(obj, self.cache_name, result)
            setattr(obj, self.time_name, elapsed)
            print(f"[计时] {self.func.__name__}: {elapsed*1000:.2f}ms")

        return getattr(obj, self.cache_name)

    def __set__(self, obj, value):
        # 清除缓存
        if hasattr(obj, self.cache_name):
            delattr(obj, self.cache_name)
        if hasattr(obj, self.time_name):
            delattr(obj, self.time_name)

    @property
    def last_execution_time(self):
        """获取上次执行时间（需要在实例上访问）"""
        return getattr(obj := None, self.time_name, 0) if False else None

class DataProcessor:
    """数据处理器"""

    @timed_property
    def expensive_calculation(self) -> int:
        """耗时的计算（只执行一次）"""
        time.sleep(0.1)  # 模拟耗时操作
        return 42

    @timed_property
    def sorted_data(self) -> list[int]:
        """排序数据（只执行一次）"""
        import random
        data = [random.randint(0, 100) for _ in range(1000)]
        return sorted(data)

# 使用示例
processor = DataProcessor()

print("第一次访问:")
print(f"结果: {processor.expensive_calculation}")  # 计算并计时

print("\n第二次访问（使用缓存）:")
print(f"结果: {processor.expensive_calculation}")  # 直接返回缓存

print("\n排序数据:")
print(f"前10个: {processor.sorted_data[:10]}")
```

#### 6.4 验证框架

```python
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

T = TypeVar("T")

class Validator(ABC, Generic[T]):
    """验证器基类"""

    @abstractmethod
    def validate(self, value: T) -> tuple[bool, str | None]:
        """返回 (是否有效, 错误信息)"""
        ...

class RangeValidator(Validator[int]):
    def __init__(self, min_val: int, max_val: int):
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value: int) -> tuple[bool, str | None]:
        if not (self.min_val <= value <= self.max_val):
            return False, f"值必须在 {self.min_val} 到 {self.max_val} 之间"
        return True, None

class RegexValidator(Validator[str]):
    def __init__(self, pattern: str):
        import re
        self.pattern = re.compile(pattern)

    def validate(self, value: str) -> tuple[bool, str | None]:
        if not self.pattern.match(value):
            return False, f"值不符合模式: {self.pattern.pattern}"
        return True, None

class ValidatedField:
    """验证字段描述符"""

    def __init__(self, validators: list[Validator]):
        self.validators = validators
        self.name = ""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f"_{self.name}", None)

    def __set__(self, obj, value):
        # 验证所有规则
        for validator in self.validators:
            valid, error = validator.validate(value)
            if not valid:
                raise ValueError(f"字段 {self.name} 验证失败: {error}")

        setattr(obj, f"_{self.name}", value)

class Person:
    """人物模型"""

    age = ValidatedField([
        RangeValidator(0, 150),
    ])

    email = ValidatedField([
        RegexValidator(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
    ])

    name = ValidatedField([])  # 无验证

    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

# 使用示例
try:
    person = Person("Alice", 25, "alice@example.com")
    print(f"创建成功: {person.name}, {person.age}岁, {person.email}")

    person.age = -5  # ValueError!
except ValueError as e:
    print(f"验证错误: {e}")
```

### Part 7: 描述符最佳实践与性能（进阶）

> **📌 提示**：本节介绍描述符的性能优化和最佳实践，适合进阶学习。

#### 7.1 描述符 vs __getattr__

```python
class DescriptorExample:
    """描述符方式"""

    class AgeField:
        def __get__(self, obj, objtype=None):
            return obj.__dict__.get("_age", 0)

        def __set__(self, obj, value):
            if not (0 <= value <= 150):
                raise ValueError("年龄必须在 0-150 之间")
            obj.__dict__["_age"] = value

    age = AgeField()

class GetAttrExample:
    """__getattr__ 方式"""

    def __init__(self):
        self.__dict__["_age"] = 0

    def __getattr__(self, name):
        if name == "age":
            return self.__dict__.get("_age", 0)
        raise AttributeError(f"'{type(self).__name__}' 没有属性 '{name}'")

    def __setattr__(self, name, value):
        if name == "age":
            if not (0 <= value <= 150):
                raise ValueError("年龄必须在 0-150 之间")
            self.__dict__["_age"] = value
        else:
            self.__dict__[name] = value

# 选择指南
print("""
描述符适用场景:
- 需要在多个类/属性间复用逻辑
- 需要精细控制属性访问（get/set/delete）
- 需要类型检查或验证

__getattr__ 适用场景:
- 处理任意数量的动态属性
- 实现代理或延迟加载
- 简单的属性转发
""")
```

#### 7.2 描述符性能优化

```python
# 避免在 __get__ 中创建新对象
class BadDescriptor:
    """低效：每次访问都创建新对象"""
    def __get__(self, obj, objtype=None):
        return {"value": obj.__dict__.get("_value")}  # 每次创建新字典

class GoodDescriptor:
    """高效：使用 __dict__ 直接存储"""
    def __get__(self, obj, objtype=None):
        return obj.__dict__.get("_value")

    def __set__(self, obj, value):
        obj.__dict__["_value"] = value

# 使用 __slots__ 优化
class OptimizedModel:
    """使用 slots 减少内存占用"""
    __slots__ = ("_name", "_age", "_email")

    name = GoodDescriptor()
    age = GoodDescriptor()
    email = GoodDescriptor()

    def __init__(self, name: str, age: int, email: str):
        self._name = name
        self._age = age
        self._email = email
```

#### 7.3 描述符与 dataclasses

```python
from dataclasses import dataclass, field
from typing import Any

# 在 dataclass 中使用描述符
class ValidatedField:
    """可验证字段"""
    def __init__(self, validator=None):
        self.validator = validator

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f"_{self.name}", None)

    def __set__(self, obj, value):
        if self.validator:
            self.validator(value)
        setattr(obj, f"_{self.name}", value)

def positive_validator(value):
    if value < 0:
        raise ValueError("值必须为正数")

@dataclass
class Account:
    """账户（结合 dataclass 和描述符）"""
    name: str = field(default="")
    balance: float = field(default=0.0)

    # 使用描述符覆盖字段行为
    _balance = ValidatedField(positive_validator)

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float):
        if self._balance is None:
            object.__setattr__(self, "_balance", value)
        else:
            positive_validator(value)
            object.__setattr__(self, "_balance", value)

# 使用示例
account = Account(name="Alice", balance=1000)
print(f"账户余额: {account.balance}")

account.balance = 2000
print(f"新余额: {account.balance}")

try:
    account.balance = -100
except ValueError as e:
    print(f"错误: {e}")
```

### Part 8: 面试题精选

#### 8.1 描述符的优先级

```python
"""
描述符优先级（从高到低）:
1. 数据描述符（定义了 __get__ 和 __set__）
2. 实例 __dict__
3. 非数据描述符（只定义了 __get__）
4. 类属性

这意味着:
- 数据描述符总是优先于实例 __dict__
- 实例 __dict__ 优先于非数据描述符
"""

class DataDescriptor:
    """数据描述符"""
    def __get__(self, obj, objtype=None):
        return f"DataDescriptor.get()"

    def __set__(self, obj, value):
        print(f"DataDescriptor.set({value})")

class NonDataDescriptor:
    """非数据描述符"""
    def __get__(self, obj, objtype=None):
        return f"NonDataDescriptor.get()"

class MyClass:
    data = DataDescriptor()
    non_data = NonDataDescriptor()

obj = MyClass()

# 访问优先级测试
print(obj.data)  # DataDescriptor.get()
obj.data = "value"  # DataDescriptor.set(value)

print(obj.non_data)  # NonDataDescriptor.get()

# 如果实例有同名属性
obj.__dict__["data"] = "instance_value"
print(obj.data)  # 仍然是 DataDescriptor.get()（数据描述符优先）

obj.__dict__["non_data"] = "instance_value"
print(obj.non_data)  # instance_value（实例 __dict__ 优先）
```

#### 8.2 property vs 描述符

```python
"""
Q: property 和描述符有什么区别？

A: property 是描述符的一种特例。
   - property: 非数据描述符，绑定到类属性
   - 描述符: 更通用的协议，可以创建数据描述符
"""

# property 的实现原理
class property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.doc = doc or fget.__doc__ if fget else None

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)

    def __set__(self, obj, value):
        self.fset(obj, value)

    def __delete__(self, obj):
        self.fdel(obj)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.doc)

# 实际上 property 就是用描述符实现的！
```

#### 8.3 描述符在实际框架中的应用

```python
"""
Django ORM 中的描述符:
- CharField, IntegerField 等都是描述符
- 负责数据验证、类型转换、数据库交互

SQLAlchemy 中的描述符:
- Column 对象是描述符
- 负责懒加载、关系映射、变更追踪

FastAPI/Pydantic 中的描述符:
- Field 是描述符
- 负责验证、序列化、JSON Schema 生成
"""

# 示例：Django 风格的字段
class CharField:
    """简化版 Django CharField"""
    def __init__(self, max_length=255, null=False, default=""):
        self.max_length = max_length
        self.null = null
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name
        self.attname = f"{name}_id"  # 数据库列名

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        if value is None and not self.null:
            raise ValueError(f"{self.name} 不能为空")
        if value and len(value) > self.max_length:
            raise ValueError(f"{self.name} 长度不能超过 {self.max_length}")
        obj.__dict__[self.name] = value

    def to_db(self, value):
        """转换为数据库格式"""
        return value or ""

    def from_db(self, value):
        """从数据库读取"""
        return value

class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        cls._meta = {"fields": {}, "table_name": name.lower()}
        return cls

class Model(metaclass=ModelMeta):
    pass

class User(Model):
    name = CharField(max_length=100)
    email = CharField(max_length=255)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# 使用示例
user = User(name="Alice", email="alice@example.com")
print(f"{user.name}: {user.email}")

try:
    user.name = "A" * 200  # 超过最大长度
except ValueError as e:
    print(f"验证错误: {e}")
```

## 🚀 快速开始

从仓库根目录进入本课：

```bash
cd stage1-python-intermediate/lessons/L15-descriptors
```

### 1. 运行示例代码

```bash
# 描述符协议、property、验证和懒加载
python examples/01_descriptor_basics.py

# 自定义 property、访问日志、优先级和验证器组合
python examples/02_descriptor_advanced.py
```

### 2. 完成练习题

```bash
python exercises/01_descriptors.py
```

### 3. 运行自动化测试

```bash
uv run pytest tests -q
```

---

## 📝 练习题

当前练习集中在 `exercises/01_descriptors.py`，一次性实现 3 类常用描述符：

### 练习 1: 验证描述符基类与正数验证

补齐 `Validator.__set__()`，让它在赋值前调用 `validate()`；再实现 `Positive.validate()`，拒绝负数：

```python
class Product:
    price = Positive()

product = Product()
product.price = 100   # ✅
product.price = -10   # ❌ ValueError
```

### 练习 2: 范围验证描述符

实现 `Range(min_val, max_val)`，验证数值落在闭区间内：

```python
class Product:
    rating = Range(0, 5)

product = Product()
product.rating = 4.5  # ✅
product.rating = 6    # ❌ ValueError
```

### 练习 3: 延迟加载描述符

实现 `Lazy`，第一次访问时调用实例上的 `_load_<属性名>()`，并缓存结果：

```python
class DataService:
    data = Lazy()

    def _load_data(self):
        return {"loaded": True}

service = DataService()
service.data  # 第一次访问触发加载
service.data  # 第二次访问直接返回缓存
```

## 🔗 下一步

完成本课程后，继续学习：

- [L16: 并发编程入门](../L16-concurrency-intro/lesson.md)

> 📖 **学习路径提示**：L16 将学习线程、进程和协程的并发基础。

---

**课程说明**: 本课程专注于 Python 描述符与属性访问机制，是理解 Python 面向对象高级特性的重要一环。
