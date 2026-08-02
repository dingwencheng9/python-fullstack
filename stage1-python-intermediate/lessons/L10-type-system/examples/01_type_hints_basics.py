"""L10: 类型系统 - 类型提示基础示例"""

import math

# === Part 1: 基础类型提示 ===


def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """加法"""
    return a + b


def get_user() -> dict[str, str]:
    """返回用户字典"""
    return {"name": "Alice", "email": "alice@example.com"}


# 运行测试
print(greet("World"))  # Hello, World!
print(add(1, 2))  # 3
print(get_user())  # {'name': 'Alice', 'email': 'alice@example.com'}

# === Part 2: Union 和 Optional ===


def parse_number(value: str) -> int | float | None:
    """解析数字，失败返回 None"""
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return None


def find_user(users: list[dict], user_id: int | None = None) -> dict | None:  # type: ignore[type-arg]
    """查找用户，id 为空返回第一个"""
    if user_id is None:
        return users[0] if users else None
    return next((u for u in users if u.get("id") == user_id), None)


# 测试
print(parse_number("42"))  # 42
print(parse_number("3.14"))  # 3.14
print(parse_number("abc"))  # None

users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
print(find_user(users))  # {'id': 1, 'name': 'Alice'}
print(find_user(users, 2))  # {'id': 2, 'name': 'Bob'}
print(find_user(users, 999))  # None

# === Part 3: 类型别名（旧式 vs PEP 695 新式）===

# ❌ 旧式类型别名（Python < 3.12）
from typing import TypeAlias  # noqa: US035

Matrix: TypeAlias = list[list[float]]  # noqa: US040
Point: TypeAlias = tuple[float, float]  # noqa: US040

# ✅ 新式类型别名（PEP 695，Python 3.12+）:
# type Matrix = list[list[float]]
# type Point = tuple[float, float]


def rotate_point(p: Point, angle: float) -> Point:
    """旋转二维点"""
    import math

    x, y = p
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)


matrix: Matrix = [[1.0, 2.0], [3.0, 4.0]]
point: Point = (1.0, 0.0)
print(rotate_point(point, math.pi / 2))  # 接近 (0, 1)

# === Part 4: 泛型函数 ===

from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")


def first_element(items: list[T]) -> T | None:
    """返回第一个元素"""
    return items[0] if items else None


def pair(a: T, b: U) -> tuple[T, U]:
    """创建元组"""
    return (a, b)


def identity(x: T) -> T:
    """恒等函数"""
    return x


# 测试
print(first_element([1, 2, 3]))  # 1
print(first_element([]))  # None
print(pair("hello", 42))  # ('hello', 42)
print(identity(42))  # 42

# === Part 5: 泛型容器（旧式 vs PEP 695 新式）===

from typing import Generic


# ❌ 旧式泛型类（Python < 3.12）
class Stack(Generic[T]):  # noqa: US046
    """泛型栈"""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0


# 测试
stack: Stack[int] = Stack()
stack.push(1)
stack.push(2)
print(stack.peek())  # 2
print(stack.pop())  # 2
print(stack.is_empty())  # False

string_stack: Stack[str] = Stack()
string_stack.push("hello")
print(string_stack.pop())  # hello

print("\n=== 类型提示基础示例完成 ===")
