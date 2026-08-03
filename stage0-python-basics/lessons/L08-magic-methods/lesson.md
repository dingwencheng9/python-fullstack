# L08: 魔术方法（Magic Methods）

> **课程编号**: L08
> **所属阶段**: Stage 0 - Python 编程基础
> **预计时长**: 4 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: L07（面向对象基础）
> **版本**: v2.2
> **最后更新**: 2026-08-02
> **核心版本**: Python 3.13

---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ 掌握构造和表示方法：`__init__`、`__repr__`、`__str__`
2. ✅ 掌握比较和哈希方法：`__eq__`、`__hash__`、`__lt__`
3. ✅ 理解算术运算符重载：`__add__`、`__sub__`
4. ✅ 掌握容器协议：`__getitem__`、`__len__`、`__contains__`
5. ✅ 理解可调用对象：`__call__`
6. ✅ 了解迭代器协议 `__iter__`（选学，属容器协议进阶内容）
7. ✅ 了解属性访问协议：`__getattr__`、`__setattr__`

---

## 📖 课程导读

### 什么是魔术方法？

**魔术方法**（Magic Methods，也叫 Dunder Methods）是 Python 中以双下划线 `__` 开头和结尾的特殊方法。它们不是我们主动调用的，而是由 Python 的某些操作自动触发的。

```python
class Person:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

p = Person("Alice")  # __init__ 被自动调用
print(p)              # __str__ 被自动调用
```

### 为什么要学习魔术方法？

| 功能 | 不使用魔术方法 | 使用魔术方法 |
|------|---------------|-------------|
| 打印对象 | `print(p.name)` | `print(p)` |
| 比较对象 | `equals(p1, p2)` | `p1 == p2` |
| 集合操作 | `my_set.contains(s, x)` | `x in my_set` |
| 数学运算 | `vec_add(v1, v2)` | `v1 + v2` |

魔术方法让你的类与 Python 的内置语法无缝集成，代码更 Pythonic。

---

## Part 1: 基础魔术方法

### 1.1 `__init__` - 构造方法

`__init__` 在对象创建时自动调用，用于初始化实例属性：

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name      # 实例属性
        self.age = age

p = Person("Alice", 30)
print(p.name)  # Alice
print(p.age)   # 30
```

### 1.2 `__repr__` - 开发者表示

`__repr__` 提供对象的"官方"字符串表示，主要用于调试：

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, age={self.age!r})"

p = Person("Alice", 30)
print(repr(p))  # Person(name='Alice', age=30)
```

> **最佳实践**: `__repr__` 的返回值应该是**可执行**的 Python 代码，能 recreates 相同对象。

### 1.3 `__str__` - 用户友好表示

`__str__` 提供用户友好的字符串表示：

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return f"{self.name}, {self.age}岁"

p = Person("Alice", 30)
print(p)        # Alice, 30岁（优先调用 __str__）
print(str(p))   # Alice, 30岁
```

### 1.4 `__repr__` vs `__str__` 的区别

```python
class Book:
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author

    def __repr__(self) -> str:
        return f"Book(title={self.title!r}, author={self.author!r})"

    def __str__(self) -> str:
        return f"《{self.title}》- {self.author}"

book = Book("Python入门", "张三")

print(book)        # 《Python入门》- 张三（__str__，用户友好）
print(repr(book))  # Book(title='Python入门', author='张三')（__repr__，开发者视角）
```

**触发时机**:
- `print()` / `str()` → 优先 `__str__`，无则回退 `__repr__`
- `repr()` / 直接在交互式环境显示 → `__repr__`

---

## Part 2: 算术运算符重载

### 2.1 二元运算符

```python
class Point:
    """二维点"""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Point) -> Point:
        """p1 + p2"""
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        """p1 - p2"""
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


p1 = Point(1, 2)
p2 = Point(3, 4)

print(p1 + p2)  # Point(4.0, 6.0)
print(p2 - p1)  # Point(2.0, 2.0)
```

### 2.2 标量乘法与右乘

```python
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __mul__(self, scalar: float) -> Point:
        """point * scalar"""
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Point:
        """scalar * point（反序乘法）"""
        return self * scalar

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


p = Point(2, 3)

print(p * 3)    # Point(6.0, 9.0)  - 调用 __mul__
print(3 * p)    # Point(6.0, 9.0)  - 调用 __rmul__
```

> **关键点**: `__rmul__` 处理反序情况 `3 * point`。实现时可直接复用 `__mul__`。

### 2.3 运算符方法速查

| 方法 | 运算符 | 示例 |
|------|--------|------|
| `__add__` | `+` | `a + b` |
| `__sub__` | `-` | `a - b` |
| `__mul__` | `*` | `a * b` |
| `__truediv__` | `/` | `a / b` |
| `__floordiv__` | `//` | `a // b` |
| `__mod__` | `%` | `a % b` |
| `__pow__` | `**` | `a ** b` |
| `__neg__` | `-` | `-a`（一元） |
| `__pos__` | `+` | `+a`（一元） |

---

## Part 3: 比较运算符

### 3.1 相等与哈希

`__eq__` 定义相等性判断，`__hash__` 使对象可用于 set 和 dict 的键：

```python
class Version:
    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return False
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __hash__(self) -> int:
        """必须与 __eq__ 一致"""
        return hash((self.major, self.minor, self.patch))

    def __repr__(self) -> str:
        return f"Version({self.major}.{self.minor}.{self.patch})"


v1 = Version(1, 2, 3)
v2 = Version(1, 2, 3)
v3 = Version(1, 2, 4)

print(v1 == v2)  # True
print(v1 == v3)  # False

# 可放入 set
versions = {v1, v2, v3}
print(len(versions))  # 2（v1 和 v2 被视为同一个元素）
```

> ⚠️ **重要规则**: 如果两个对象相等（`__eq__` 返回 True），它们必须具有相同的哈希值（`__hash__` 返回相同值）。

### 3.2 排序比较

```python
class Version:
    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return False
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __lt__(self, other: Version) -> bool:
        """小于比较"""
        return (
            (self.major, self.minor, self.patch)
            < (other.major, other.minor, other.patch)
        )

    def __le__(self, other: Version) -> bool:
        return self == other or self < other

    def __gt__(self, other: Version) -> bool:
        return other < self

    def __ge__(self, other: Version) -> bool:
        return self == other or other < self

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.patch))


# 用于排序
versions = [
    Version(2, 0, 0),
    Version(1, 2, 3),
    Version(1, 2, 4),
]
print(sorted(versions))  # [Version(1.2.3), Version(1.2.4), Version(2.0.0)]
```

### 3.3 比较方法速查

| 方法 | 运算符 | 说明 |
|------|--------|------|
| `__eq__` | `==` | 相等 |
| `__ne__` | `!=` | 不等（默认取反 `__eq__`） |
| `__lt__` | `<` | 小于 |
| `__le__` | `<=` | 小于等于 |
| `__gt__` | `>` | 大于 |
| `__ge__` | `>=` | 大于等于 |
| `__hash__` | `hash()` | 哈希值 |

---

## Part 3.5: __slots__ 内存优化

### 3.5.1 什么是 __slots__？

`__slots__` 是 Python 的一种内存优化机制，通过**限制实例属性**来减少对象内存占用：

```python
# ❌ 普通类：使用 __dict__ 存储属性（内存开销大）
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

p = Point(1, 2)
print(p.__dict__)  # {'x': 1, 'y': 2}  ← 每个实例有自己的字典
```

```python
# ✅ 使用 __slots__：禁用 __dict__（内存优化）
class Point:
    __slots__ = ('x', 'y')  # 只允许这两个属性

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

p = Point(1, 2)
print(hasattr(p, '__dict__'))  # False ← 没有 __dict__！
```

### 3.5.2 内存对比

```python
import sys

class PointNormal:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class PointSlotted:
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

p1 = PointNormal(1, 2)
p2 = PointSlotted(1, 2)

print(f"普通类: {sys.getsizeof(p1.__dict__)} bytes (属性字典)")
print(f"__slots__: {sys.getsizeof(p2)} bytes (无字典)")

# 创建大量实例时的内存节省
# 100万个点：普通类约 350MB，__slots__ 约 80MB
```

### 3.5.3 __slots__ 的限制

```python
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

p = Point(1, 2)

# ✅ 可以添加 __slots__ 中声明的属性
p.x = 10
p.y = 20

# ❌ 无法添加未声明的属性
p.z = 30  # AttributeError: 'Point' object has no attribute 'z'

# ❌ 无法使用 __dict__（除非显式添加）
p.__dict__  # AttributeError
```

### 3.5.4 __slots__ 与继承

```python
# 父类使用 __slots__
class Base:
    __slots__ = ('x', 'y')

# 子类继承 __slots__
class Point(Base):
    __slots__ = ('z',)  # 只需添加子类的新属性

p = Point(1, 2, 3)
print(p.x, p.y, p.z)  # 1 2 3
```

### 3.5.5 使用场景

| 场景 | 推荐 | 原因 |
|------|------|------|
| 大量简单对象 | ✅ 使用 | 显著节省内存 |
| 需要动态添加属性 | ❌ 不用 | 限制太多 |
| 数据类（dataclass） | ⚠️ 看情况 | dataclass 可配合 slots=True |
| 游戏引擎粒子系统 | ✅ 使用 | 数百万粒子时必用 |

```python
# dataclass + slots（Python 3.10+）
from dataclasses import dataclass

@dataclass(slots=True)
class Particle:
    x: float
    y: float
    z: float
    velocity: tuple[float, float, float]
```

---

## Part 4: 容器与迭代器

### 4.1 `__len__` - 长度

```python
class Stack:
    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        self._items.append(item)

    def pop(self) -> str | None:
        if not self._items:
            return None
        return self._items.pop()

    def __len__(self) -> int:
        """len(stack)"""
        return len(self._items)


stack = Stack()
stack.push("apple")
stack.push("banana")
print(len(stack))  # 2
```

### 4.2 `__contains__` - 成员检查

```python
class Stack:
    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        self._items.append(item)

    def __contains__(self, item: str) -> bool:
        """item in stack"""
        return item in self._items


stack = Stack()
stack.push("apple")
stack.push("banana")
print("apple" in stack)   # True
print("orange" in stack)  # False
```

### 4.3 `__iter__` - 迭代器

> **📌 提示**：`__iter__` 是容器协议中的进阶内容，本节仅展示概念性示例，不做深入讲解。

```python
class Stack:
    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        self._items.append(item)

    def __iter__(self) -> StackIterator:
        """for item in stack"""
        return StackIterator(self._items.copy())


class StackIterator:
    """Stack 的迭代器"""

    def __init__(self, items: list[str]) -> None:
        self._items = items
        self._index = 0

    def __iter__(self) -> StackIterator:
        """返回迭代器自身"""
        return self

    def __next__(self) -> str:
        if self._index >= len(self._items):
            return  # 迭代结束，Python 会自动抛出 StopIteration
        item = self._items[self._index]
        self._index += 1
        return item


stack = Stack()
stack.push("a")
stack.push("b")
stack.push("c")

for item in stack:
    print(item)
# 输出: a, b, c
```

### 4.4 容器协议速查

| 方法 | 运算符/函数 | 说明 |
|------|-------------|------|
| `__len__` | `len(obj)` | 返回长度 |
| `__contains__` | `item in obj` | 成员检查 |
| `__iter__` | `iter(obj)` | 返回迭代器 |
| `__getitem__` | `obj[key]` | 索引访问 |

---

## Part 5: 可调用对象

### 5.1 `__call__` 使对象可调用

```python
class Counter:
    """带状态的计数器"""

    def __init__(self) -> None:
        self._count = 0

    def __call__(self) -> int:
        """使实例可像函数一样调用"""
        self._count += 1
        return self._count

    @property
    def count(self) -> int:
        return self._count

    def reset(self) -> None:
        self._count = 0


counter = Counter()

print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
print(f"总调用: {counter.count}")  # 总调用: 3

counter.reset()
print(counter())  # 1
```

### 5.2 `__call__` 的应用场景

| 应用 | 示例 |
|------|------|
| 记忆化 | `@lru_cache` 装饰器 |
| 带状态的函数 | 计数器、ID 生成器 |
| 延迟计算 | 懒加载对象 |
| 策略模式 | 可切换的算法 |

---

## Part 6: 属性访问协议

### 6.1 `__getattr__` - 属性访问拦截

`__getattr__` 在访问**不存在的**属性时调用：

```python
class LazyObject:
    def __init__(self) -> None:
        object.__setattr__(self, "_data", {})
        object.__setattr__(self, "_loaded", False)

    def __getattr__(self, name: str) -> str:
        """访问不存在的属性时调用"""
        if name.startswith("_"):
            return f"[私有属性: {name}]"  # 私有属性用替代值
        if name not in self._data:
            return f"[未加载: {name}]"
        return self._data[name]

    def load(self, key: str, value: str) -> None:
        self._data[key] = value


obj = LazyObject()
obj.load("name", "Alice")
obj.load("age", "30")

print(obj.name)  # Alice
print(obj.age)   # 30
print(obj.city)  # [未加载: city]
```

### 6.2 `__setattr__` - 属性设置拦截

`__setattr__` 在设置**任何**属性时调用：

```python
class ValidationObject:
    def __init__(self) -> None:
        # 注意：需要用 object.__setattr__ 避免递归
        object.__setattr__(self, "_data", {})
        object.__setattr__(self, "_frozen", False)

    def __setattr__(self, name: str, value: str) -> None:
        """设置属性时调用"""
        if object.__getattribute__(self, "_frozen"):
            print("⚠️ 对象已冻结，修改被忽略")  # 冻结状态下不执行设置
            return
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value

    def __getattr__(self, name: str) -> str:
        if name not in self._data:
            return f"[未设置: {name}]"
        return self._data[name]


obj = ValidationObject()
obj.name = "Alice"
print(obj.name)  # Alice
```

### 6.3 避免无限递归

在 `__setattr__` 中设置实例属性时，需要避免递归：

```python
# ❌ 错误：无限递归
def __setattr__(self, name: str, value: str) -> None:
    self.name = value  # 再次调用 __setattr__！

# ✅ 正确：使用 object.__setattr__
def __setattr__(self, name: str, value: str) -> None:
    object.__setattr__(self, name, value)
```

---

## 🎓 核心知识点总结

### 魔术方法分类

| 类别 | 方法 | 触发场景 |
|------|------|---------|
| **构造/表示** | `__init__`, `__repr__`, `__str__` | 对象创建、打印 |
| **比较/哈希** | `__eq__`, `__hash__`, `__lt__` 等 | 比较、排序、集合 |
| **算术运算** | `__add__`, `__sub__`, `__mul__`, `__rmul__` | 数学运算 |
| **容器协议** | `__len__`, `__contains__`（`__iter__` 选学） | 集合操作、迭代 |
| **可调用对象** | `__call__` | 像函数一样调用 |
| **属性访问** | `__getattr__`, `__setattr__` | 属性操作拦截 |

### 完整示例：Vector 向量类

```python
class Vector:
    """二维向量"""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    # 算术运算
    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector:
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vector:
        return self * scalar

    # 比较运算
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    # 表示
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    # 方法
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5


# 使用示例
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)       # Vector(4.0, 6.0)
print(v1 - v2)       # Vector(2.0, 2.0)
print(v1 * 2)        # Vector(6.0, 8.0)
print(2 * v1)        # Vector(6.0, 8.0)
print(v1 == v2)      # False
print(v1.magnitude())  # 5.0
print(f"向量: {v1}")  # 向量: (3.0, 4.0)
```

---

## 💡 常见陷阱与最佳实践

### 陷阱 1：忘记 `__hash__` 的一致性

```python
# ❌ 错误：相等对象哈希不同
class Bad:
    def __init__(self, value: int) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bad):
            return False
        return self.value == other.value

    # 忘记定义 __hash__ 或哈希不一致


# ✅ 正确
class Good:
    def __init__(self, value: int) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Good):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
```

### 陷阱 2：`__repr__` 与 `__str__` 混淆

```python
# ❌ 错误：只实现 __str__，__repr__ 变成默认的类名+地址
class Bad:
    def __str__(self) -> str:
        return "用户友好"


# ✅ 推荐：都实现，至少实现 __repr__
class Good:
    def __repr__(self) -> str:
        return f"Good()"

    def __str__(self) -> str:
        return "用户友好"
```

### 陷阱 3：反序运算符未实现

```python
# ❌ 错误：只能 point * 3，不能 3 * point
class Point:
    def __mul__(self, scalar: float) -> Point:
        return Point(self.x * scalar, self.y * scalar)


# ✅ 正确：同时实现 __rmul__
class Point:
    def __mul__(self, scalar: float) -> Point:
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Point:
        return self * scalar
```

### 最佳实践 1：immutable 对象优先

```python
# 推荐：不可变对象 — 不提供内部修改接口
# 详见 L09 综合项目中的 @dataclass 章节

# ❌ 可变对象（容易产生意外修改）
# class Vector:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

# ✅ 不可变对象（推荐，但需要手动实现）
class ImmutableVector:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)

    def __add__(self, other: "ImmutableVector") -> "ImmutableVector":
        return ImmutableVector(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

### 最佳实践 2：使用 functools.total_ordering

```python
# functools.total_ordering 在 Stage 1 L12 装饰器章节学习
# 该装饰器可以自动从 __eq__ 和 __lt__ 生成其他比较运算符
```

---

## 🚀 实战案例：Money 货币类

```python
class Money:
    """带单位的货币类"""

    def __init__(self, dollars: int, cents: int) -> None:
        self.dollars = dollars
        self.cents = cents
        self._normalize()

    def _normalize(self) -> None:
        """进位归一化"""
        self.dollars += self.cents // 100
        self.cents = self.cents % 100

    def __repr__(self) -> str:
        return f"Money({self.dollars}, {self.cents})"

    def __str__(self) -> str:
        return f"${self.dollars}.{self.cents:02d}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.dollars == other.dollars and self.cents == other.cents

    def __add__(self, other: Money) -> Money:
        total_cents = self.dollars * 100 + self.cents
        total_cents += other.dollars * 100 + other.cents
        return Money(0, total_cents)

    def __sub__(self, other: Money) -> Money:
        total_cents = self.dollars * 100 + self.cents
        other_cents = other.dollars * 100 + other.cents
        if total_cents < other_cents:
            # 提前返回：不允许负余额（L08 将学到用 raise 抛出异常）
            return Money(0, 0)
        return Money(0, total_cents - other_cents)


# 使用
m1 = Money(1, 50)
m2 = Money(2, 75)
print(m1 + m2)  # $4.25
print(repr(m1 + m2))  # Money(4, 25)
```

---

## 📚 延伸阅读

### 官方文档
- [Data Model - Python 官方文档](https://docs.python.org/zh-cn/3.13/reference/datamodel.html)
- [Emulating numeric types](https://docs.python.org/zh-cn/3.13/reference/datamodel.html#emulating-numeric-types)
- [Basic customization](https://docs.python.org/zh-cn/3.13/reference/datamodel.html#basic-customization)

### 推荐资源
- [Python Magic Methods Guide](https://rszalski.github.io/magicmethods/) - 完整的魔术方法参考

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 解释什么是魔术方法以及为什么使用它们
- [ ] 实现 `__init__`、`__repr__`、`__str__`
- [ ] 实现比较运算符 `__eq__`、`__hash__`、`__lt__`
- [ ] 实现算术运算符 `__add__`、`__sub__`、`__mul__`、`__rmul__`
- [ ] 实现容器协议 `__len__`、`__contains__`（`__iter__` 选学，见 L11）
- [ ] 实现 `__call__` 使对象可调用
- [ ] 理解 `__getattr__` 和 `__setattr__` 的使用场景
- [ ] 避免常见陷阱（哈希一致性、反序运算符）

---

## 🔗 下一步

完成本课程后，继续学习：

- [L09: 异常处理](../L09-exceptions/lesson.md)

在下一课中，我们将学习：
- 异常的概念和分类
- try/except 语句
- 自定义异常类
- 异常的最佳实践
