# L10: Python 类型系统完整指南

> **课程编号**: L10  
> **所属阶段**: Stage 1 - Python 进阶  
> **预计时长**: 6 小时  
> **难度**: ⭐⭐⭐☆☆（中级）  
> **前置课程**: L04 函数与模块  
> **学习目标**: 掌握 PEP 484 类型注解、PEP 695 类型参数语法、Protocol 协议、类型 narrowing 与泛型

---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ 理解 Python 类型系统的演进（PEP 484 → PEP 695）
2. ✅ 掌握现代类型注解语法（Python 3.13）
3. ✅ 熟练使用 Union、Optional、Callable 等高级类型
4. ✅ 使用 Protocol 定义结构化子类型
5. ✅ 使用 PEP 695 `type` 关键字定义泛型
6. ✅ 配置 mypy 进行静态类型检查

---

## 📚 核心内容

### Part 1: 类型注解基础

#### 1.1 为什么需要类型注解？

类型注解（Type Hints）是一种声明变量、函数参数和返回值预期类型的语法：

```python
# 无注解
def add(a, b):
    return a + b

# 有注解
def add(a: int, b: int) -> int:
    return a + b
```

**类型注解的好处：**

| 场景 | 无注解 | 有注解 |
|------|--------|--------|
| IDE 补全 | 基础 | 精准 |
| 代码审查 | 依赖阅读 | 类型推导 |
| 重构安全 | 风险高 | 风险低 |
| 文档价值 | 需读源码 | 自文档化 |

> ⚠️ **重要**：Python 类型注解是**可选的**，运行时不会强制检查。它们主要用于：
> - IDE 提供智能补全和错误提示
> - mypy 等工具进行静态检查
> - 生成文档

#### 1.2 变量类型注解

```python
# 基本类型
name: str = "Alice"
age: int = 25
height: float = 1.75
is_student: bool = True

# 复杂类型
scores: list[int] = [90, 85, 92]
person: dict[str, str] = {"name": "Bob", "city": "Beijing"}
coordinates: tuple[float, float] = (39.9, 116.4)

# 类型别名
Vector = list[float]
matrix: list[Vector] = [[1.0, 2.0], [3.0, 4.0]]
```

#### 1.3 函数类型注解

```python
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def process_items(items: list[str]) -> dict[str, int]:
    """统计每个字符串出现的次数"""
    return {item: items.count(item) for item in set(items)}

# 可选参数
def create_user(
    name: str,
    age: int = 18,
    email: str | None = None
) -> dict[str, str | int | None]:
    return {"name": name, "age": age, "email": email}
```

#### 1.4 类的类型注解

```python
class User:
    def __init__(self, name: str, email: str) -> None:
        self.name: str = name
        self.email: str = email

    def introduce(self) -> str:
        return f"I'm {self.name}"

# 类型注解存储在 __annotations__
print(User.__init__.__annotations__)
# {'name': <class 'str'>, 'email': <class 'str'>, 'return': <class 'NoneType'>}
```

---

### Part 2: 联合类型与可选类型

#### 2.1 Union 类型

使用 `|` 操作符（Python 3.10+）或 `Union` 表示"可以是多种类型之一"：

```python
# Python 3.10+ 语法（推荐）
def process(value: int | float | str) -> str:
    return str(value)

# 传统 Union 语法
from typing import Union

def process(value: Union[int, float, str]) -> str:
    return str(value)
```

#### 2.2 Optional 类型

`Optional[X]` 等价于 `X | None`，表示值可以是 X 也可以是 None：

```python
# Python 3.10+ 语法（推荐）
def find_user(user_id: int) -> dict[str, str] | None:
    if user_id in users:
        return users[user_id]
    return None

# 传统 Optional 语法
from typing import Optional

def find_user(user_id: int) -> Optional[dict[str, str]]:
    if user_id in users:
        return users[user_id]
    return None
```

#### 2.3 类型守卫（Type Narrowing）

Python 运行时不会自动收窄类型，但可以通过 `isinstance` 检查实现类型守卫：

```python
def describe(value: int | str | float) -> str:
    if isinstance(value, int):
        # 在这个分支中，value 被收窄为 int
        return f"整数: {value * 2}"
    elif isinstance(value, str):
        # 在这个分支中，value 被收窄为 str
        return f"字符串: {value.upper()}"
    else:
        # 在这个分支中，value 被收窄为 float
        return f"浮点数: {value:.2f}"
```

**类型守卫模式：**

```python
# 防御性检查
def safe_divide(a: int | float, b: int | float) -> float:
    if not isinstance(b, (int, float)):
        raise TypeError("b 必须是数字")
    if b == 0:
        raise ZeroDivisionError("不能除以零")
    return a / b

# None 检查
def greet(name: str | None) -> str:
    if name is None:
        name = "Guest"
    return f"Hello, {name}!"

# 属性检查
class Animal:
    legs: int | None = None

def walk(animal: Animal) -> str:
    if animal.legs is not None:
        return f"用 {animal.legs} 条腿走路"
    return "腿数未知"
```

#### 2.4 TypeGuard 与自定义类型守卫

`typing.TypeGuard` 允许你定义自定义类型守卫函数，帮助类型检查器更精确地收窄类型：

```python
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    """判断列表是否全是字符串"""
    return all(isinstance(x, str) for x in val)

def process(items: list[object]) -> int:
    if is_string_list(items):
        # 在此分支中，items 被收窄为 list[str]
        return len(items[0])  # str 有 __len__
    return len(items)  # 在此分支中，items 仍是 list[object]
```

#### 2.5 字面量类型收窄

使用 `Literal` 类型可以收窄到具体的字面量值：

```python
from typing import Literal

def handle_mode(mode: Literal["read", "write", "append"]) -> None:
    if mode == "read":
        print("打开文件用于读取")
    elif mode == "write":
        print("打开文件用于写入")
    elif mode == "append":
        print("打开文件用于追加")
    # 类型检查器确保覆盖了所有情况
```

#### 2.6 assert 后的类型收窄

`assert` 语句也可以帮助类型收窄：

```python
def process(data: str | int | None) -> str:
    assert data is not None, "data 不能为 None"
    # 断言后，data 被收窄为 str | int

    if isinstance(data, str):
        return data.upper()
    return str(data)  # 这里是 int
```

---

### Part 3: 容器类型注解

#### 3.1 泛型容器类型

```python
from typing import TypeAlias

# 列表
numbers: list[int] = [1, 2, 3]
matrix: list[list[float]] = [[1.0, 2.0], [3.0, 4.0]]

# 字典
name_to_age: dict[str, int] = {"Alice": 25, "Bob": 30}
nested: dict[str, list[int]] = {"scores": [90, 85]}

# 集合
unique_ids: set[int] = {1, 2, 3}
string_set: set[str] = {"a", "b", "c"}

# 元组（固定长度）
point: tuple[float, float] = (3.14, 2.71)
rgb: tuple[int, int, int] = (255, 128, 0)

# 元组（可变长度）
flexible: tuple[int, ...] = (1, 2, 3, 4, 5)  # 任意数量的 int
```

#### 3.2 类型别名

使用类型别名可以让复杂的类型声明更易读：

```python
from typing import TypeAlias

# 简单别名
UserId: TypeAlias = int
ProductId: TypeAlias = int

# 复杂别名
Coordinates: TypeAlias = tuple[float, float]
RGB: TypeAlias = tuple[int, int, int]
Vector: TypeAlias = list[float]
SparseVector: TypeAlias = dict[int, float]

# 使用别名
def distance(p1: Coordinates, p2: Coordinates) -> float:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return (dx**2 + dy**2) ** 0.5
```

---

### Part 4: Callable 类型

#### 4.1 函数作为参数

使用 `Callable` 表示"可调用的"：

```python
from collections.abc import Callable

# Callable[[参数类型...], 返回类型]
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

def add(x: int, y: int) -> int:
    return x + y

def multiply(x: int, y: int) -> int:
    return x * y

print(apply(add, 3, 4))      # 7
print(apply(multiply, 3, 4)) # 12
```

#### 4.2 可调用对象

```python
from collections.abc import Callable

# 接受任意可调用对象
def call_twice(func: Callable[[], None]) -> None:
    func()
    func()

# 使用 lambda
call_twice(lambda: print("Hello!"))
```

#### 4.3 高阶函数类型

```python
from collections.abc import Callable

# 返回函数的高阶函数
def make_multiplier(factor: int) -> Callable[[int], int]:
    def multiply(x: int) -> int:
        return x * factor
    return multiply

double = make_multiplier(2)
print(double(5))  # 10

# 带上下界的变换器
from typing import TypeAlias

Transform: TypeAlias = Callable[[int], int]

def compose(f: Transform, g: Transform) -> Transform:
    """组合两个变换器"""
    def composed(x: int) -> int:
        return g(f(x))
    return composed

add_one = lambda x: x + 1
double = lambda x: x * 2
add_then_double = compose(add_one, double)
print(add_then_double(3))  # (3 + 1) * 2 = 8
```

---

### Part 5: Protocol - 结构化子类型

#### 5.1 什么是 Protocol？

Protocol（PEP 544）定义了一组方法签名，任何实现了这些方法的类都"结构性地"属于该 Protocol：

```python
from typing import Protocol

class Closeable(Protocol):
    def close(self) -> None: ...

# 实现了 close() 的类自动满足 Closeable
class File:
    def __init__(self, path: str) -> None:
        self._file = open(path)

    def close(self) -> None:
        self._file.close()

# File 自动满足 Closeable
def close_all(resource: Closeable) -> None:
    resource.close()

f = File("test.txt")
close_all(f)  # ✅ 可以工作！
```

#### 5.2 Protocol 与继承的区别

| 特性 | Protocol | ABC 继承 |
|------|----------|----------|
| 实现方式 | 结构性（duck typing） | 名义性 |
| 显式声明 | 不需要 | 需要 `class X(ABC)` |
| 耦合度 | 松耦合 | 紧耦合 |
| 适用场景 | 接口抽象 | 强制实现 |

```python
from typing import Protocol, runtime_checkable

# Protocol 示例
class Drawable(Protocol):
    def draw(self) -> None: ...

class Shape:
    def __init__(self, name: str) -> None:
        self.name = name

    def draw(self) -> None:  # 隐式满足 Drawable
        print(f"Drawing {self.name}")

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        super().__init__("Circle")
        self.radius = radius

def render(shape: Drawable) -> None:
    shape.draw()  # 任何有 draw() 的对象都可以

circle = Circle(5)
render(circle)  # ✅ 自动满足 Drawable
```

#### 5.3 运行时检查

使用 `@runtime_checkable` 让 Protocol 支持 `isinstance` 检查：

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    def to_json(self) -> str: ...

class User:
    def __init__(self, name: str) -> None:
        self.name = name

    def to_json(self) -> str:
        return f'{{"name": "{self.name}"}}'

user = User("Alice")
print(isinstance(user, Serializable))  # True ✅
```

---

### Part 6: PEP 695 - 现代泛型语法

#### 6.1 `type` 关键字（Python 3.12+）

Python 3.12 引入了 `type` 关键字来定义泛型类型参数：

```python
# 旧式泛型（Python 3.9-3.11）
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

def first(lst: list[T]) -> T:
    return lst[0]

# 新式泛型（Python 3.12+）
type List[T] = list[T]
type Dict[K, V] = dict[K, V]

def first(lst: list[T]) -> T:
    return lst[0]
```

#### 6.2 泛型类

```python
# 旧式
from typing import TypeVar

T = TypeVar("T")

class Stack:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# 新式（Python 3.12+）
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# 使用
int_stack: Stack[int] = Stack()
int_stack.push(42)
```

#### 6.3 泛型函数

```python
# Python 3.12+
type Pair[T1, T2] = tuple[T1, T2]

def swap[T1, T2](pair: Pair[T1, T2]) -> Pair[T2, T1]:
    a, b = pair
    return (b, a)

result = swap((1, "one"))  # type: tuple[str, int]
```

#### 6.4 类型参数限定

使用 `type` 的 `bounds` 限定类型参数的上界：

```python
# 限定为数字类型（int 或 float 的子类）
type Numeric[T: (int, float)] = T

def add[T: (int, float)](a: T, b: T) -> T:
    return a + b  # 类型检查器知道结果是 T

add(1, 2)    # ✅
add(1.5, 2.5) # ✅
```

---

### Part 7: TypedDict 与类型安全的 **kwargs

#### 8.1 什么是 TypedDict？

TypedDict（PEP 589）允许你定义字典的结构，指定每个键的类型：

```python
# ❌ 普通字典 - 无类型安全
def create_user(user_data: dict) -> None:
    print(user_data["name"])  # 可能不存在
    print(user_data["age"])   # 类型未知

# ✅ TypedDict - 类型安全
from typing import TypedDict

class UserData(TypedDict):
    name: str
    age: int
    email: str

def create_user(user_data: UserData) -> None:
    print(user_data["name"])  # ✅ mypy 知道是 str
    print(user_data["age"])   # ✅ mypy 知道是 int
```

#### 8.2 基础用法

```python
from typing import TypedDict

# 定义 TypedDict
class User(TypedDict):
    name: str
    age: int
    email: str

# 创建实例
user: User = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
}

# ✅ 类型安全
print(user["name"])  # ✅ OK

# ❌ 类型错误 - mypy 会检测
invalid_user: User = {
    "name": "Bob",
    "age": "25",  # ❌ mypy error: Expected int, got str
    "email": "bob@example.com"
}
```

#### 8.3 可选字段与必需字段

```python
from typing import TypedDict, NotRequired

class UserProfile(TypedDict):
    name: str                    # 必需
    age: int                     # 必需
    email: NotRequired[str]      # 可选
    phone: NotRequired[str]      # 可选

# ✅ 有效 - 包含可选字段
user1: UserProfile = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "phone": "123-456-7890"
}

# ✅ 有效 - 不包含可选字段
user2: UserProfile = {
    "name": "Bob",
    "age": 25
}

# ❌ 无效 - 缺少必需字段
user3: UserProfile = {
    "name": "Charlie"
    # ❌ mypy error: Missing key "age"
}
```

#### 8.4 PEP 692: Unpack for **kwargs

**核心功能**: 使用 `Unpack[TypedDict]` 让 `**kwargs` 类型安全：

```python
from typing import TypedDict, Unpack

class UserData(TypedDict):
    name: str
    age: int
    email: str

def create_user(**kwargs: Unpack[UserData]) -> dict[str, str | int]:
    """类型安全的用户创建函数"""
    return {
        "name": kwargs["name"],      # ✅ mypy 知道是 str
        "age": kwargs["age"],        # ✅ mypy 知道是 int
        "email": kwargs["email"],    # ✅ mypy 知道是 str
    }

# ✅ 正确使用
user1 = create_user(
    name="Alice",
    age=30,
    email="alice@example.com"
)

# ❌ 类型错误 - mypy 会检测
user2 = create_user(
    name="Bob",
    age="25",  # ❌ mypy error: Expected int, got str
    email="bob@example.com"
)

# ❌ 缺少字段 - mypy 会检测
user3 = create_user(
    name="Charlie",
    age=25
    # ❌ mypy error: Missing required keyword argument "email"
)

# ❌ 额外字段 - mypy 会检测
user4 = create_user(
    name="David",
    age=35,
    email="david@example.com",
    phone="123-456-7890"  # ❌ mypy error: Unexpected keyword argument
)
```

#### 8.5 TypedDict 继承与组合

```python
from typing import TypedDict

class BasicUser(TypedDict):
    name: str
    email: str

class AdminUser(BasicUser):
    """继承 BasicUser 的所有字段"""
    role: str
    permissions: list[str]

# 使用
admin: AdminUser = {
    "name": "Admin",
    "email": "admin@example.com",
    "role": "administrator",
    "permissions": ["read", "write", "delete"]
}
```

#### 8.6 实际应用场景

**场景 1: API 请求/响应类型**

```python
from typing import TypedDict, NotRequired, Unpack

class APIRequest(TypedDict):
    method: str
    url: str
    headers: NotRequired[dict[str, str]]
    body: NotRequired[dict[str, object]]

class APIResponse(TypedDict):
    status: int
    data: dict[str, object]
    error: NotRequired[str]

def make_request(**kwargs: Unpack[APIRequest]) -> APIResponse:
    """类型安全的 API 请求"""
    # 实现省略
    return {"status": 200, "data": {"result": "success"}}

# 使用
response = make_request(
    method="GET",
    url="https://api.example.com/users"
)
```

**场景 2: 配置管理**

```python
class DatabaseConfig(TypedDict):
    host: str
    port: int
    database: str
    username: str
    password: str
    pool_size: NotRequired[int]
    timeout: NotRequired[int]

def connect_database(**config: Unpack[DatabaseConfig]) -> None:
    """连接数据库"""
    print(f"Connecting to {config['host']}:{config['port']}")

# 使用
connect_database(
    host="localhost",
    port=5432,
    database="myapp",
    username="user",
    password="pass",
    pool_size=10
)
```

#### 8.7 TypedDict vs 普通 dict vs class

| 特性 | TypedDict | 普通 dict | 普通 class |
|------|-----------|-----------|------------|
| 类型安全 | ✅ 字典结构 | ❌ 无 | ⚠️ 有限 |
| IDE 支持 | ✅ 自动补全 | ⚠️ 有限 | ✅ 自动补全 |
| 运行时检查 | ❌ 无 | ❌ 无 | ✅ 自己实现 |
| 可变性 | 字典 | 字典 | 可配置 |
| 适用场景 | API/配置 | 动态结构 | 业务逻辑 |

```python
# TypedDict - 用于字典结构（API、配置）
class APIPayload(TypedDict):
    user_id: int
    action: str
    data: NotRequired[dict[str, object]]

# 普通 class - 用于业务逻辑对象
class UserDTO:
    def __init__(self, name: str, email: str, age: int) -> None:
        self.name = name
        self.email = email
        self.age = age
```

> 💡 **L13 将学到**：`dataclasses.dataclass` 是 Python 3.7+ 的装饰器，可自动生成 `__init__`/`__repr__` 等方法，是定义数据对象的简洁方式。

---

### Part 8: mypy 配置与使用

#### 7.1 安装与基础使用

```bash
# 安装 mypy
uv add mypy --dev

# 运行类型检查
uv run mypy your_module.py

# 检查整个目录
uv run mypy your_package/
```

#### 7.2 pyproject.toml 配置

```toml
[tool.mypy]
python_version = "3.13"
strict = true           # 启用所有严格检查
warn_return_any = true  # 函数返回类型必须是注解的
warn_unused_configs = true
disallow_untyped_defs = true

[tool.mypy.overrides]
# 忽略第三方库的类型检查
ignore_missing_imports = true
```

#### 7.3 常见配置项

```toml
[tool.mypy]
# 基础配置
python_version = "3.13"
warn_return_any = true
warn_unused_ignores = true

# 严格模式（推荐）
strict = true

# 非严格模式的单个选项
disallow_untyped_defs = false  # 允许无注解函数
disallow_any_generics = false  # 允许泛型使用 Any
check_untyped_defs = true      # 检查未注解函数体

[tool.mypy-overrides."module:第三方库.*"]
ignore_missing_imports = true
```

#### 7.4 忽略特定行

```python
# type: ignore[具体错误类型]
result = some_function()  # type: ignore[operator]
```

---

## Part 9: Pydantic 运行时验证（框架类型系统）

> ⚠️ **本节为框架铺垫**：为后续 L27 FastAPI 的 Pydantic 使用做准备。

### 9.1 静态类型检查 vs 运行时验证

L10 讲解的 `mypy` 属于**静态类型检查**——在**运行前**由工具分析代码，发现类型错误。但静态检查有局限性：

```python
# mypy 无法检测以下运行时错误
def parse_age(data: dict) -> int:
    return int(data["age"])  # 如果 data["age"] 是 "abc"？

# API 请求数据（来自网络）无法用 mypy 检查
# POST /api/users body: {"name": "...", "age": "not_a_number"}
```

**解决方案**：使用 `Pydantic` 进行**运行时验证**——在程序运行时检查数据是否符合预期。

### 9.2 Pydantic BaseModel 基础

Pydantic 的核心是 `BaseModel`，它是一个**自带验证功能的类**：

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str          # 必须提供，且必须是 str
    age: int           # 必须提供，且必须是 int
    email: str | None  # 可选，提供时必须是 str

# ✅ 正常创建
user = User(name="Alice", age=25)
print(user.model_dump())
# {'name': 'Alice', 'age': 25, 'email': None}

# ❌ 类型错误 - Pydantic 自动验证并报错
try:
    user = User(name="Bob", age="not_a_number")
except ValidationError as e:
    print(e.error_count())  # 1 个错误
    # 1 validation error for User
    # age
    #   Input should be a valid integer...
```

### 9.3 Field() 定义验证规则

`Field()` 是 Pydantic 提供的特殊函数，用于为字段添加**验证约束**：

```python
from pydantic import BaseModel, Field
from typing import Annotated

class User(BaseModel):
    # Field() 在 Annotated 语义下工作
    name: Annotated[str, Field(min_length=2, max_length=50)]
    age: Annotated[int, Field(ge=0, le=150)]           # ge = greater or equal
    email: str | None = None
    password: Annotated[str, Field(min_length=8)]      # 最短 8 字符

# ✅ 正常
user = User(name="Alice", age=25, password="secure123")

# ❌ 验证失败
try:
    user = User(name="A", age=200, password="short")  # 3 个错误
except ValidationError as e:
    print(e.errors())
    # [
    #   {'type': 'string_too_short', 'loc': ('name',), 'msg': '...'},
    #   {'type': 'greater_than_equal', 'loc': ('age',), 'msg': '...'},
    #   {'type': 'string_too_short', 'loc': ('password',), 'msg': '...'}
    # ]
```

### 9.4 Annotated + Field：可扩展的类型元数据

这正是 `Annotated` 的设计目的——**允许框架在标准类型系统上扩展自己的语义**：

| 用法 | 来源 | 作用 |
|------|------|------|
| `Annotated[str, "description"]` | Python 标准 | 仅 IDE 提示 |
| `Annotated[str, Field(...)]` | Pydantic | 运行时验证 + IDE 提示 |

```python
from typing import Annotated
from pydantic import BaseModel, Field

# Pydantic 利用 Annotated 的第二个参数传递验证器
class Config(BaseModel):
    port: Annotated[int, Field(gt=0, le=65535, description="端口号")]
    debug: Annotated[bool, Field(description="调试模式")] = False
```

### 9.5 BaseModel vs dataclass vs TypedDict

| 特性 | BaseModel | @dataclass | TypedDict |
|------|-----------|------------|-----------|
| 运行时验证 | ✅ 自动 | ❌ 需手动 | ❌ 无 |
| 类型注解 | ✅ | ✅ | ✅ |
| Pydantic V2 性能 | ✅ 极快 | — | — |
| 适用场景 | API 数据、用户输入 | 简单数据结构 | 类型提示 dict |

**何时用 Pydantic**：处理来自 API、数据库、用户输入的**不可信数据**时，优先使用 `BaseModel`。

---

## 🚀 快速开始

从仓库根目录进入本课：

```bash
cd stage1-python-intermediate/lessons/L10-type-system
```

### 1. 运行示例代码

```bash
# 基础类型、Protocol、现代泛型、Callable、类型收窄、TypedDict
python examples/01_type_hints_basics.py
python examples/02_protocol.py
python examples/03_pep695_generics.py
python examples/04_callable_types.py
python examples/05_type_narrowing.py
python examples/07_typeddict.py
```

### 2. 完成练习题

```bash
# 练习题
python exercises/01_type_narrowing.py
python exercises/02_protocol.py
python exercises/03_generic_constraints.py
```

### 3. 查看参考答案

```bash
python solutions/01_type_basics_solution.py
python solutions/02_generic_stack_solution.py
python solutions/03_protocol_solution.py
```

### 4. 运行类型检查

```bash
uv run mypy examples/ -v
uv run mypy solutions/ -v
```

---

## 📝 练习题

### 练习 1: 类型注解基础

为以下函数添加完整的类型注解：

```python
def process_data(data, filters):
    """处理数据并应用过滤器"""
    result = []
    for item in data:
        if all(f(item) for f in filters):
            result.append(item)
    return result
```

### 练习 2: 泛型栈实现

使用 PEP 695 语法实现一个类型安全的栈：

```python
class Stack[T]:
    # 实现 push, pop, peek, is_empty
    pass
```

### 练习 3: Protocol 设计

设计一个 `Reversible` Protocol，并让多个类实现它：

```python
# 1. 定义 Reversible Protocol
class Reversible(Protocol):
    ...

# 2. 让 str, list, tuple 满足 Protocol
# 3. 编写使用 Reversible 的函数
def reverse_all(items: Reversible) -> Reversible:
    ...
```

---

## 📝 本章总结

### 核心知识点

1. **类型注解基础**
   - 使用 `:` 注解变量类型
   - 使用 `->` 注解函数返回类型
   - 类型注解是可选的，运行时不强制检查

2. **联合类型与可选类型**
   - `X | Y` 表示可以是 X 或 Y
   - `X | None` 等价于 `Optional[X]`
   - 使用 `isinstance` 实现类型守卫

3. **容器类型**
   - `list[T]`, `dict[K, V]`, `set[T]`
   - `tuple[T, ...]` 表示可变长度元组
   - 使用 `TypeAlias` 定义类型别名

4. **Callable 类型**
   - `Callable[[ParamTypes...], ReturnType]`
   - 接受函数作为参数或返回值

5. **Protocol 协议**
   - 结构性子类型（duck typing）
   - 不需要显式继承
   - 使用 `@runtime_checkable` 支持 `isinstance`

6. **PEP 695 现代泛型**
   - `type` 关键字定义泛型
   - 泛型类：`class Stack[T]: ...`
   - 泛型函数：`def func[T](x: T) -> T: ...`

7. **TypedDict 与类型安全 kwargs**
   - TypedDict 定义字典结构类型
   - PEP 692 `Unpack[TypedDict]` 让 `**kwargs` 类型安全
   - `NotRequired` 标记可选字段
   - TypedDict 继承实现字段组合

8. **mypy 静态检查**
   - `uv add mypy --dev` 安装
   - `uv run mypy .` 检查项目
   - 配置 `pyproject.toml` 定制规则

### 关键要点

- ✅ Python 类型注解是可选的，主要用于 IDE 和静态检查
- ✅ 优先使用 `X | Y` 而非 `Union[X, Y]`
- ✅ Protocol 是定义接口的首选方式（相比 ABC）
- ✅ PEP 695 `type` 语法是 Python 3.12+ 的现代写法
- ✅ mypy 是 Python 类型检查的事实标准
- ✅ TypedDict 适合 API 请求/响应、配置管理等字典结构场景
- ✅ Unpack[TypedDict] 让函数参数类型安全且灵活

### 常见陷阱

- ❌ 误以为类型注解会在运行时强制检查（不会）
- ❌ 使用过时的 `from typing import List` 语法
- ❌ 忘记 Protocol 不需要显式继承
- ❌ 在 `strict` 模式下遗漏注解导致检查失败
- ❌ TypedDict 继承时混淆 `total=True/False` 的默认值

### 实用技巧

- 💡 使用 `type` 别名简化复杂类型声明
- 💡 Protocol + `@runtime_checkable` 实现运行时接口检查
- 💡 使用 `reveal_type()` 帮助调试类型问题
- 💡 渐进式添加类型注解（先核心模块）
- 💡 `mypy --strict` 模式提供最佳类型安全保障
- 💡 TypedDict 继承时，子类 `total=False` 会覆盖父类默认值

### 典型应用场景

- 📦 定义 API 的请求/响应类型（TypedDict）
- 🔧 泛型数据结构（栈、队列、树）
- 🧩 依赖注入的接口定义（Protocol）
- 📝 第三方库的存根文件（`.pyi`）
- ⚙️ 配置管理（TypedDict + Unpack）

---

## 💭 课堂思考

1. **类型注解的实际作用**：为什么 Python 运行时不强制类型检查，但仍然推荐使用类型注解？类型注解的主要价值在哪里？

2. **Protocol vs ABC**：Protocol 使用"结构化子类型"而非"名义子类型"。思考一下，这种设计如何影响了 Python 的类型系统？

3. **泛型约束的边界**：使用 `bound` 约束泛型参数时，如果约束类型有副作用会怎样？PEP 695 的 `T: Constraint` 语法相比旧式的 `TypeVar("T", bound=...)` 有什么优势？

---

## 📚 参考资料

- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 544 - Protocols](https://peps.python.org/pep-0544/)
- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [mypy 官方文档](https://mypy.readthedocs.io/)
- [typing 模块文档](https://docs.python.org/zh-cn/3/library/typing.html)

---

## 📁 文件导航

| 目录       | 说明         |
| ---------- | ------------ |
| examples/  | 示例代码     |
| exercises/ | 练习题       |
| solutions/ | 参考答案     |
| tests/     | 单元测试     |
| lesson.md  | 详细教学内容 |

---

## ✅ 完成标准

- [ ] 完成所有练习题（3 个）
- [ ] 本课测试通过：`uv run pytest stage1-python-intermediate/lessons/L10-type-system/tests -q`
- [ ] 可选：安装 mypy 后检查 `solutions/` 类型提示
- [ ] 理解 Union、Optional、Callable 的用法
- [ ] 掌握 Protocol 定义和使用
- [ ] 了解 PEP 695 现代泛型语法

---

## 🔗 下一步

完成本课程后，继续学习：

- [L11: 迭代器与生成器](../L11-generators/lesson.md)
- [L12: Python 高级特性](../L12-advanced-features/lesson.md)

---

**课程整合说明**: 本课程合并了原 L12（类型提示基础）和 L12（类型提示进阶），整合了 PEP 695 新语法和 Protocol 协议，提供了完整的 Python 类型系统指南。学习时长约 6 小时，涵盖从基础注解到高级泛型的完整知识体系。
