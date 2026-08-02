"""L10: 类型系统 - PEP 695 泛型语法"""

# === Part 1: 类型参数列表 ===

# ❌ 旧式泛型（Python < 3.12）
from typing import TypeVar, Generic  # noqa: US035, US046
from collections.abc import Callable

T = TypeVar("T")
U = TypeVar("U")


def old_identity(x: T) -> T:
    return x


class OldContainer(Generic[T]):  # noqa: US046
    def __init__(self, value: T) -> None:
        self.value = value


# PEP 695 泛型（Python 3.12+）
def new_identity[T](x: T) -> T:
    """使用类型参数列表的泛型函数"""
    return x


class Container[T]:
    """使用类型参数列表的泛型类"""

    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value


# 测试
print(new_identity(42))  # 42
print(new_identity("hello"))  # hello
container = Container(100)
print(container.get())  # 100

# === Part 2: 多类型参数 ===


def pair[T, U](a: T, b: U) -> tuple[T, U]:
    """返回元组"""
    return (a, b)


def first_of_three[T, U, V](a: T, b: U, c: V) -> T:
    """返回第一个"""
    return a


print(pair(1, "hello"))  # (1, 'hello')
print(first_of_three(1, 2, 3))  # 1
print(first_of_three("a", "b", "c"))  # a

# === Part 3: 类型别名 ===

# ❌ 旧式类型别名（Python < 3.12）
from typing import TypeAlias  # noqa: US035

OldMatrix: TypeAlias = list[list[float]]  # noqa: US040
OldPoint: TypeAlias = tuple[float, float]  # noqa: US040

# PEP 695 类型别名（使用 type 关键字）
type Matrix = list[list[float]]
type Point = tuple[float, float]
type UserId = int
type UserName = str


def rotate_point(p: Point, angle: float) -> Point:
    """旋转二维点"""
    import math

    x, y = p
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)


point: Point = (1.0, 0.0)
print(rotate_point(point, 3.14159 / 2))  # 接近 (0, 1)

# === Part 4: 泛型约束 ===


# 使用类型参数约束
def largest[T: (int, float)](a: T, b: T) -> T:
    """返回较大值（需要支持比较）"""
    return a if a > b else b


print(largest(10, 20))  # 20
print(largest(3.14, 2.71))  # 3.14
# largest("a", "b")  # 错误：str 不在约束中

# === Part 5: 泛型接口 ===

from typing import Protocol


class Comparable[T](Protocol):  # type: ignore[valid-type,misc]
    """可比较协议"""

    def __lt__(self, other: T) -> bool: ...
    def __gt__(self, other: T) -> bool: ...
    def __le__(self, other: T) -> bool: ...
    def __ge__(self, other: T) -> bool: ...


def find_max[T: Comparable[T]](items: list[T]) -> T | None:  # type: ignore[valid-type]
    """找最大值"""
    if not items:
        return None
    max_val = items[0]
    for item in items[1:]:
        max_val = max(max_val, item)
    return max_val


print(find_max([3, 1, 4, 1, 5, 9, 2, 6]))  # 9
print(find_max([]))  # None

# === Part 6: 泛型装饰器 ===

from functools import wraps


def cache_result[T](func: Callable[..., T]) -> Callable[..., T]:
    """缓存结果的装饰器"""
    cache: dict[tuple[tuple, tuple], T] = {}  # type: ignore[type-arg]

    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> T:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


@cache_result
def expensive_computation(n: int) -> int:
    """模拟耗时计算"""
    return sum(range(n))


print(expensive_computation(10))
print(expensive_computation(10))  # 使用缓存

print("\n=== PEP 695 泛型示例完成 ===")
