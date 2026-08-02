# R03: PEP 649/810 延迟注解

> **课程编号**: R03
> **所属阶段**: Stage R - 前沿探索实验室
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: R01, R02, L10
> **版本**: v5.0
> **最后更新**: 2026-07-22
> **核心版本**: Python 3.14 (实验性)

---

## 📌 学习目标

完成本课程后，你将能够：

1. **理解 PEP 649 延迟注解求值**：运行时评估类型注解，消除 `from __future__ import annotations`
2. **掌握 PEP 810 类型参数默认值**：泛型类型的默认类型参数
3. **评估迁移影响**：识别代码中对字符串化注解的依赖
4. **优化启动性能**：减少大型代码库的导入时间

---

## 📖 课程导读

### 问题：注解的性能陷阱

Python 类型注解一直存在一个悖论：

```python
# 问题：注解在定义时就被字符串化
class MyClass:
    def method(self, x: "SomeType") -> "AnotherType":
        # 注解是字符串，需要 eval() 才能使用
        pass

# 这导致：
# 1. 必须 import SomeType，即使运行时不需要
# 2. 循环导入成为常见问题
# 3. 启动时间变慢
```

### 解决方案：PEP 649 / PEP 810

| PEP | 标题 | 作用 |
|-----|------|------|
| PEP 649 | Deferred Evaluation Of Annotations Using Descriptors | 延迟注解求值 |
| PEP 810 | Type Parameter Defaults | 泛型默认值 |

---

## Part 1: PEP 649 延迟注解

### 1.1 当前行为 vs PEP 649

```python
# Python 3.10-3.13（当前行为）
from __future__ import annotations  # 字符串化注解

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hello, {self.name}!"

# 注解是字符串，get_type_hints() 需要 import
import typing

hints = typing.get_type_hints(User)
# {'name': <class 'str'>, 'age': <class 'int'>, 'greet': <class 'str'>}
```

```python
# Python 3.14+ with PEP 649（未来行为）
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hello, {self.name}!"

# 无需 __future__ import，注解自动延迟求值
# 运行时才评估注解，get_type_hints() 更快
import typing
hints = typing.get_type_hints(User)
# {'name': <class 'str'>, 'age': <class 'int'>, 'greet': <class 'str'>}
```

### 1.2 注解表达式的运行时求值

```python
# PEP 649 核心机制

class User:
    name: str
    age: int

    # 注解可以引用尚未导入的类型
    metadata: "Metadata"  # 只要运行时有 Metadata 即可
    friends: list["User"]  # 自引用

# __annotations__ 不再是字符串字典
# 而是延迟求值对象
import typing
from typing import get_type_hints, get_origin, get_args

class Demo:
    field: list[int]

# 获取原始注解（可能是延迟对象）
raw = Demo.__annotations__
print(f"原始: {raw}")  # {'field': list[int]}

# 获取运行时类型（强制求值）
resolved = get_type_hints(Demo)
print(f"解析: {resolved}")  # {'field': list}
```

### 1.3 类型表达式对象

```python
# PEP 649 引入了类型表达式对象

from typing import TypeAlias, TypeVar

# 延迟注解的内部表示
class TypeExpr:
    """类型表达式基类"""
    def __class_getitem__(cls, item):
        return TypeExpr(item)

# 示例：注解的实际结构
T = TypeVar("T")

class Container:
    items: list[T]  # 运行时是 TypeExpr(list[T])

    def get_type(self) -> type:
        from typing import get_type_hints
        return get_type_hints(self.__class__)["items"]
```

---

## Part 2: PEP 810 类型参数默认值

### 2.1 泛型默认类型参数

```python
# PEP 810 之前：泛型不能有默认值
from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")

# ❌ 错误：泛型不能有默认值
class Container(Generic[T, U = str]):  # 不支持
    pass

# ✅ 变通：使用 bound 或多个 TypeVar
class Container1(Generic[T]):
    pass

class StringContainer(Generic[T]):
    pass
```

```python
# PEP 810 之后：泛型可以有默认值

from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")

# ✅ 正确：类型参数可以有默认值
class Container(Generic[T, U = str, V = int]):
    """容器，默认 U=str, V=int"""
    def __init__(self, items: list[T], metadata: U = None, flag: V = None):
        self.items = items
        self.metadata = metadata
        self.flag = flag

# 使用默认类型
c1: Container[str] = Container(["a", "b"])
# 等价于 Container[str, str, int]
print(c1.metadata)  # None，使用默认值 str

# 覆盖部分默认值
c2: Container[str, bytes] = Container([b"a"])
# 覆盖 U=bytes，使用默认 V=int
print(type(c2.flag))  # <class 'int'>

# 显式指定所有类型
c3: Container[str, bytes, float] = Container([1.0], b"x", 3.14)
```

### 2.2 泛型默认值实战

```python
from typing import Generic, TypeVar, Protocol, runtime_checkable

T = TypeVar("T")
U = TypeVar("U")
C = TypeVar("C", bound="Comparable")

@runtime_checkable
class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...
    def __gt__(self, other) -> bool: ...

class Repository(Generic[T, U = "T"]):
    """
    数据仓库

    T: 实体类型
    U: ID 类型，默认为 T 的 ID 类型
    """

    def __init__(self, db_connection):
        self._db = db_connection

    def find(self, id: U) -> T | None:
        """根据 ID 查找实体"""
        # 实现查找逻辑
        ...

    def find_all(self) -> list[T]:
        """查找所有实体"""
        ...

# 示例：使用默认值
class User:
    id: int
    name: str

class UserRepository(Repository[User]):
    """User 仓库，ID 类型默认为 int"""
    def __init__(self, db):
        super().__init__(db)

repo = UserRepository(connection)
user = repo.find(123)  # id: int

# 显式指定 ID 类型
class UserWithUUID:
    id: str  # 自定义 ID
    name: str

class UUIDUserRepository(Repository[UserWithUUID, str]):
    """UUID 类型的 User 仓库"""
    pass
```

### 2.3 TypeVar 的默认值

```python
from typing import TypeVar, Generic, Union

T = TypeVar("T")
M = TypeVar("M", default=dict)  # PEP 810

class Cache(Generic[T, M]):
    """缓存，支持不同的映射类型"""

    def __init__(self, store: M = None):
        self._store: M = store or {}

    def get(self, key: str) -> T | None:
        return self._store.get(key)

    def set(self, key: str, value: T):
        self._store[key] = value

# 使用默认的 dict
c1: Cache[int] = Cache()
print(type(c1._store))  # <class 'dict'>

# 使用自定义映射
from collections import OrderedDict
c2: Cache[int, OrderedDict[str, int]] = Cache(OrderedDict())
print(type(c2._store))  # <class 'collections.OrderedDict'>
```

---

## Part 3: 迁移指南

### 3.1 检测代码中的注解依赖

```python
"""
检测代码中对字符串化注解的依赖
"""
import ast
import sys
from pathlib import Path
from typing import Any

class AnnotationDependencyVisitor(ast.NodeVisitor):
    """检测注解中的字符串字面量"""

    def __init__(self):
        self.string_annotations: list[tuple[str, str]] = []  # (file, annotation)
        self.eval_in_annotations: list[tuple[str, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for annotation in node.returns, *node.args.annotations:
            if isinstance(annotation, ast.Constant) and isinstance(annotation.value, str):
                self.string_annotations.append((node.name, annotation.value))
        self.generic_visit(node)

def check_file(file_path: Path) -> dict[str, Any]:
    """检查文件中的注解依赖"""
    source = file_path.read_text()
    tree = ast.parse(source)

    visitor = AnnotationDependencyVisitor()
    visitor.visit(tree)

    return {
        "file": str(file_path),
        "string_annotations": visitor.string_annotations,
        "eval_usage": visitor.eval_in_annotations,
    }

def scan_directory(directory: Path) -> list[dict]:
    """扫描目录中的所有 Python 文件"""
    results = []
    for py_file in directory.rglob("*.py"):
        if "__pycache__" not in str(py_file):
            results.append(check_file(py_file))
    return results

# 使用示例
if __name__ == "__main__":
    results = scan_directory(Path("src"))
    for result in results:
        if result["string_annotations"]:
            print(f"文件: {result['file']}")
            for name, annotation in result["string_annotations"]:
                print(f"  - {name}: {annotation}")
```

### 3.2 渐进式迁移策略

```python
# 迁移策略：从 __future__ import 逐步移除

# 阶段 1：保持 __future__ import（当前）
from __future__ import annotations

class OldStyle:
    value: "str"  # 字符串注解
    items: "list[int]"  # 需要 eval

# 阶段 2：移除 __future__ import（PEP 649）
# 不用 import 注解也是延迟求值

class NewStyle:
    value: str  # 直接注解
    items: list[int]  # 直接注解
    deferred: "FutureType"  # 仅在真正需要延迟时使用字符串

# 阶段 3：清理字符串注解
class CleanStyle:
    # PEP 649 下不再需要字符串注解
    value: str
    items: list[int]

    # 仅在存在循环引用时使用字符串
    self_reference: "Self"  # 自引用需要
```

### 3.3 向后兼容代码

```python
"""
编写同时兼容 PEP 649 前后的代码
"""
from typing import TYPE_CHECKING, get_type_hints

class CompatibleClass:
    """兼容 PEP 649 前后的类"""

    # 类型别名放在 TYPE_CHECKING 块中
    if TYPE_CHECKING:
        from .models import User, Order

        UserList = list[User]
        OrderDict = dict[str, Order]

    # 运行时注解使用泛型
    users: list["User"]  # PEP 649 前需要引号
    orders: dict[str, "Order"]  # PEP 649 后可以省略引号

    @classmethod
    def get_users(cls) -> "UserList":
        """返回用户列表"""
        ...

    def process(self) -> "OrderDict":
        """处理订单"""
        ...

# get_type_hints() 在两种模式下都能工作
def get_annotations(cls: type) -> dict:
    """安全获取注解"""
    try:
        return get_type_hints(cls)
    except Exception:
        # 回退到原始注解
        return getattr(cls, "__annotations__", {})
```

---

## Part 4: 性能影响

### 4.1 启动时间对比

```python
# benchmark_annotations.py

import time
import sys

def measure_import_time(module_name: str) -> float:
    """测量模块导入时间"""
    if module_name in sys.modules:
        del sys.modules[module_name]

    start = time.perf_counter()
    __import__(module_name)
    return time.perf_counter() - start

# 测试不同模式下的导入时间
print("=== 注解导入时间对比 ===")

# 模式 1：字符串注解（需要 import）
print("字符串注解:")
t1 = measure_import_time("some_module_with_string_annotations")

# 模式 2：延迟注解（PEP 649）
print("延迟注解:")
t2 = measure_import_time("some_module_with_deferred_annotations")

print(f"改进: {(t1 - t2) / t1 * 100:.1f}%")
```

### 4.2 get_type_hints 性能

```python
import time
from typing import get_type_hints

class LargeClass:
    """大型类，有很多注解"""
    field1: int
    field2: str
    field3: list[int]
    field4: dict[str, "NestedType"]  # 字符串注解
    field5: "ForwardRef"
    field6: tuple[int, str, float]
    # ... 100+ 更多字段

def benchmark_get_type_hints():
    """测试 get_type_hints 性能"""

    # 清理缓存
    LargeClass.__annotations__ = {}  # 重置

    iterations = 10000

    # 测量
    start = time.perf_counter()
    for _ in range(iterations):
        try:
            get_type_hints(LargeClass)
        except Exception:
            pass
    elapsed = time.perf_counter() - start

    print(f"get_type_hints x {iterations}: {elapsed:.3f}s")
    print(f"平均每次: {elapsed / iterations * 1000:.3f}ms")
```

---

## 💡 常见陷阱

### 陷阱 1: 注解中的副作用

```python
# ❌ 错误：注解中有副作用
class Bad:
    value: int = (print("副作用!"), 42)[1]  # 每次类定义都打印

# ✅ 正确：注解应该是纯的
class Good:
    value: int  # 无副作用
```

### 陷阱 2: 依赖 __annotations__ 字符串格式

```python
# ❌ 错误：依赖字符串格式
class Bad:
    x: "list[int]"

annotation = Bad.__annotations__["x"]
# PEP 649 后 annotation 是类型，不是字符串
if isinstance(annotation, str):
    # PEP 649 后不再进入这个分支
    pass

# ✅ 正确：使用 get_type_hints
from typing import get_type_hints

class Good:
    x: list[int]

hints = get_type_hints(Good)
# hints["x"] 永远是类型对象
```

---

## 📚 延伸阅读

- [PEP 649 - Deferred Evaluation Of Annotations](https://peps.python.org/pep-0649/)
- [PEP 810 - Type Parameter Defaults](https://peps.python.org/pep-0810/)
- [Python typing documentation](https://docs.python.org/3/library/typing.html)

---

## ✅ 自检清单

- [ ] 解释 PEP 649 和 PEP 810 的区别
- [ ] 识别代码中对字符串化注解的依赖
- [ ] 使用泛型默认值重构代码
- [ ] 编写向后兼容的类型注解代码
- [ ] 评估 PEP 649 对启动性能的影响

---

## 🔗 下一步

- [R04: t-string 与格式化新纪元](../R04-tstring-fstring/lesson.md)
- [R05: Python 路线图与未来展望](../R05-python-roadmap/lesson.md)

---

**课程制作**: Python 3.13 全栈课程组
**最后更新**: 2026-07-22
**版本**: v5.0
