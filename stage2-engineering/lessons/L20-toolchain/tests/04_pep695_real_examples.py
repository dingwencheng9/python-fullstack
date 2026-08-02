"""
PEP 695 真实代码示例

展示 Python 3.12+ PEP 695 新语法特性的实际应用。
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
N = TypeVar("N", int, float)


def get_first[T](lst: list[T]) -> T | None:
    """返回列表第一个元素"""
    return lst[0] if lst else None


def get_last[T](lst: list[T]) -> T | None:
    """返回列表最后一个元素"""
    return lst[-1] if lst else None


def reverse[T](lst: list[T]) -> list[T]:
    """返回反转后的新列表（原列表不变）"""
    return lst[::-1]


def add[N: (int, float)](a: N, b: N) -> N:
    """加法，支持 int 和 float"""
    return a + b


def multiply[N: (int, float)](lst: list[N]) -> N:
    """列表元素连乘"""
    if not lst:
        return 1  # type: ignore
    result = lst[0]
    for item in lst[1:]:
        result = result * item
    return result


# 多类型参数泛型
def map_keys[K, V](mapping: dict[K, V]) -> list[K]:
    """返回字典的所有键"""
    return list(mapping.keys())


def map_values[K, V](mapping: dict[K, V]) -> list[V]:
    """返回字典的所有值"""
    return list(mapping.values())


def invert_dict[K, V](mapping: dict[K, V]) -> dict[V, K]:
    """反转字典"""
    return {v: k for k, v in mapping.items()}


class Pair[K, V]:
    """多类型参数泛型类"""

    def __init__(self, key: K, value: V) -> None:
        self._key = key
        self._value = value

    def get_key(self) -> K:
        return self._key

    def get_value(self) -> V:
        return self._value

    def swap(self) -> Pair[V, K]:
        return Pair(self._value, self._key)


# 类型别名
type Point = tuple[int, int]


def create_point(x: int, y: int) -> Point:
    """创建点"""
    return (x, y)


def transform_point(p: Point, func: callable) -> Point:
    """变换点"""
    return (func(p[0]), func(p[1]))


# 泛型类
class Stack[T]:
    """泛型栈实现"""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T | None:
        return self._items.pop() if self._items else None

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def size(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0


class ThreadSafeStack[T]:
    """线程安全的泛型栈"""

    def __init__(self) -> None:
        self._items: list[T] = []
        self._lock_count = 0

    def push(self, item: T) -> None:
        self._lock_count += 1
        self._items.append(item)
        self._lock_count -= 1

    def pop(self) -> T | None:
        self._lock_count += 1
        result = self._items.pop() if self._items else None
        self._lock_count -= 1
        return result

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def size(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def is_locked(self) -> bool:
        return self._lock_count > 0


# 泛型仓储
class Repository[T]:
    """泛型数据仓储"""

    def __init__(self) -> None:
        self._data: dict[int, T] = {}
        self._next_id = 1

    def add(self, item: T) -> int:
        item_id = self._next_id
        self._data[item_id] = item
        self._next_id += 1
        return item_id

    def get(self, item_id: int) -> T | None:
        return self._data.get(item_id)

    def find_all(self) -> list[T]:
        return list(self._data.values())

    def filter(self, predicate: callable) -> list[T]:
        return [item for item in self._data.values() if predicate(item)]

    def update(self, item_id: int, item: T) -> bool:
        if item_id in self._data:
            self._data[item_id] = item
            return True
        return False

    def delete(self, item_id: int) -> bool:
        if item_id in self._data:
            del self._data[item_id]
            return True
        return False


# 泛型缓存
class Cache[K, V]:
    """FIFO 泛型缓存"""

    def __init__(self, max_size: int = 10) -> None:
        self._cache: dict[K, V] = {}
        self._max_size = max_size

    def set(self, key: K, value: V) -> None:
        if len(self._cache) >= self._max_size and key not in self._cache:
            first_key = next(iter(self._cache))
            del self._cache[first_key]
        self._cache[key] = value

    def get(self, key: K) -> V | None:
        return self._cache.get(key)

    def has(self, key: K) -> bool:
        return key in self._cache

    def size(self) -> int:
        return len(self._cache)

    def clear(self) -> None:
        self._cache.clear()


# 工厂函数
def create_list[T](iterable: Iterable[T]) -> list[T]:
    """从可迭代对象创建列表"""
    return list(iterable)


def create_dict[K, V](pairs: Iterable[tuple[K, V]]) -> dict[K, V]:
    """从键值对创建字典"""
    return dict(pairs)


def map_list[T](lst: list[T], func: callable) -> list:
    """映射列表"""
    return [func(x) for x in lst]


def filter_list[T](lst: list[T], predicate: callable) -> list[T]:
    """过滤列表"""
    return [x for x in lst if predicate(x)]


def demonstrate_pep695_syntax() -> None:
    """演示 PEP 695 语法"""
    print("=== PEP 695 语法演示 ===")
    print("函数泛型: 类型参数可以直接在函数定义中声明")
    print("类泛型: 类型参数可以直接在类定义中声明")
    print("类型别名: 使用 type 关键字定义简洁的类型别名")
    print("泛型仓储: Repository[T] 支持泛型数据存储")


def show_thread_safety_notes() -> None:
    """显示线程安全注意事项"""
    print("=== 线程安全注意事项 ===")
    print("1. 泛型类本身不提供线程安全")
    print("2. ThreadSafeStack 演示了基本的线程安全模式")
    print("3. 实际生产环境中应使用 threading.Lock")
    print("4. Python 的 GIL 不等于线程安全")
    print("5. Free-threading 模式下需要显式同步")
    print("6. 纯函数不涉及共享状态，可安全并发")
    print("7. 可变容器需要加锁保护")


def demonstrate() -> dict[str, str]:
    """演示 PEP 695 特性"""
    # 泛型函数
    numbers = [1, 2, 3, 4, 5]
    result = {
        "get_first": str(get_first(numbers)),
        "get_last": str(get_last(numbers)),
        "reverse": str(reverse(numbers)),
        "add": str(add(10, 20)),
        "multiply": str(multiply([2, 3, 4])),
    }

    # 泛型类
    stack = Stack()
    stack.push(1)
    stack.push(2)
    result["stack"] = f"size={stack.size()}, peek={stack.peek()}"

    # 线程安全栈
    ts_stack = ThreadSafeStack()
    ts_stack.push("Python")
    ts_stack.push("3.13")
    result["thread_safe_stack"] = f"size={ts_stack.size()}, peek={ts_stack.peek()}"

    return result
