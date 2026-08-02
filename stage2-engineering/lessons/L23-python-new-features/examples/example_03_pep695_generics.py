"""

from __future__ import annotations

L21 示例 3: Python 3.13 PEP 695 泛型语法

展示 Python 3.13 的新泛型语法特性：
1. PEP 695 泛型函数 (def func[T](...))
2. PEP 695 泛型类 (class Name[T]:)
3. type 类型别名
4. 泛型与 Free-threading 的结合

作者: Python 3.13 全栈课程
日期: 2026-06-09
Python版本: 3.13+
"""

import sys
from collections.abc import Callable
from threading import Lock

# ============================================
# 1. PEP 695 泛型函数
# ============================================


def find_first[T](items: list[T], predicate: Callable[[T], bool]) -> T | None:
    """
    使用 PEP 695 泛型语法查找第一个匹配的元素

    Python 3.13 新语法:
    - def func[T](...) 替代 TypeVar
    - list[T] 内置泛型
    - T | None 管道符联合类型

    🔒 Free-threading 考量:
    - 纯函数，无可变状态，线程安全
    """
    for item in items:
        if predicate(item):
            return item
    return None


def filter_items[T](items: list[T], predicate: Callable[[T], bool]) -> list[T]:
    """
    使用泛型过滤列表

    类型参数 T 自动推断:
    - filter_items([1, 2, 3], lambda x: x > 1) → list[int]
    - filter_items(["a", "b"], lambda x: len(x) > 0) → list[str]
    """
    return [item for item in items if predicate(item)]


def transform[T, R](items: list[T], mapper: Callable[[T], R]) -> list[R]:
    """
    泛型映射转换

    多个类型参数:
    - T: 输入类型
    - R: 输出类型

    示例:
    - transform([1, 2, 3], str) → ["1", "2", "3"]
    - transform(["a", "b"], len) → [1, 1]
    """
    return [mapper(item) for item in items]


def group_by[T, K](items: list[T], key_func: Callable[[T], K]) -> dict[K, list[T]]:
    """
    泛型分组

    类型参数:
    - T: 元素类型
    - K: 键类型

    示例:
    - group_by([1, 2, 3, 4], lambda x: x % 2) → {0: [2, 4], 1: [1, 3]}
    """
    result: dict[K, list[T]] = {}
    for item in items:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


# ============================================
# 2. PEP 695 泛型类
# ============================================


class Container[T]:
    """
    泛型容器类

    Python 3.13 新语法:
    - class Name[T]: 替代 Generic[T]
    - 类型参数声明更简洁

    🔒 Free-threading 考量:
    - _value 可变，需要锁保护
    """

    def __init__(self, value: T) -> None:
        self._value = value
        self._lock = Lock()  # 🔒 Free-threading 线程安全

    def get(self) -> T:
        """获取值（线程安全）"""
        with self._lock:
            return self._value

    def set(self, value: T) -> None:
        """设置值（线程安全）"""
        with self._lock:
            self._value = value

    def update(self, updater: Callable[[T], T]) -> None:
        """使用函数更新值（线程安全）"""
        with self._lock:
            self._value = updater(self._value)


class Pair[T, U]:
    """
    泛型配对类

    多个类型参数:
    - T: 第一个元素类型
    - U: 第二个元素类型
    """

    def __init__(self, first: T, second: U) -> None:
        self.first = first
        self.second = second

    def swap(self) -> "Pair[U, T]":
        """交换元素"""
        return Pair(self.second, self.first)

    def map_first[R](self, mapper: Callable[[T], R]) -> "Pair[R, U]":
        """映射第一个元素"""
        return Pair(mapper(self.first), self.second)

    def map_second[R](self, mapper: Callable[[U], R]) -> "Pair[T, R]":
        """映射第二个元素"""
        return Pair(self.first, mapper(self.second))


class Stack[T]:
    """
    泛型栈

    🔒 Free-threading 考量:
    - _items 可变列表，需要锁保护
    - 在 python3.13t 环境下多线程安全
    """

    def __init__(self) -> None:
        self._items: list[T] = []
        self._lock = Lock()  # 🔒 Free-threading 线程安全

    def push(self, item: T) -> None:
        """入栈（线程安全）"""
        with self._lock:
            self._items.append(item)

    def pop(self) -> T | None:
        """出栈（线程安全）"""
        with self._lock:
            return self._items.pop() if self._items else None

    def peek(self) -> T | None:
        """查看栈顶（线程安全）"""
        with self._lock:
            return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        """判断是否为空"""
        with self._lock:
            return len(self._items) == 0

    def size(self) -> int:
        """获取大小"""
        with self._lock:
            return len(self._items)


# ============================================
# 3. type 类型别名
# ============================================

# Python 3.13 type 关键字定义类型别名
type Result[T] = T | Exception
type JsonValue = str | int | float | bool | None | dict[str, "JsonValue"] | list["JsonValue"]
type Predicate[T] = Callable[[T], bool]
type Mapper[T, R] = Callable[[T], R]


def safe_execute[T](func: Callable[[], T]) -> Result[T]:
    """
    安全执行函数，返回结果或异常

    使用 type 类型别名:
    - Result[T] = T | Exception
    """
    try:
        return func()
    except Exception as e:
        return e


# ============================================
# 4. 综合示例
# ============================================


def demonstrate_generics() -> None:
    """演示泛型功能"""
    print("=" * 70)
    print("Python 3.13 PEP 695 泛型语法演示")
    print("=" * 70)
    print(f"\nPython 版本: {sys.version}")
    print()

    # 示例 1: 泛型函数
    print("1️⃣ 泛型函数")
    print("-" * 70)

    numbers = [1, 2, 3, 4, 5]
    first_even = find_first(numbers, lambda x: x % 2 == 0)
    print(f"查找第一个偶数: {first_even}")

    evens = filter_items(numbers, lambda x: x % 2 == 0)
    print(f"过滤偶数: {evens}")

    strings = transform(numbers, str)
    print(f"转换为字符串: {strings}")

    grouped = group_by(numbers, lambda x: x % 2)
    print(f"按奇偶分组: {grouped}")

    # 示例 2: 泛型类
    print("\n\n2️⃣ 泛型类")
    print("-" * 70)

    container = Container(42)
    print(f"容器初始值: {container.get()}")

    container.update(lambda x: x * 2)
    print(f"更新后值: {container.get()}")

    pair = Pair("Alice", 25)
    print(f"配对: ({pair.first}, {pair.second})")

    swapped = pair.swap()
    print(f"交换后: ({swapped.first}, {swapped.second})")

    stack: Stack[int] = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"栈大小: {stack.size()}")
    print(f"栈顶元素: {stack.peek()}")
    print(f"出栈: {stack.pop()}")

    # 示例 3: type 类型别名
    print("\n\n3️⃣ type 类型别名")
    print("-" * 70)

    result1 = safe_execute(lambda: 42)
    print(f"成功执行: {result1}")

    result2 = safe_execute(lambda: int("not_a_number"))
    print(f"执行失败: {type(result2).__name__}: {result2}")


def show_type_system_improvements() -> None:
    """展示类型系统改进"""
    print("\n\n" + "=" * 70)
    print("Python 3.13 类型系统改进总结")
    print("=" * 70)

    improvements = [
        ("PEP 695 泛型语法", "def func[T](...) 和 class Name[T]:"),
        ("type 关键字", "type Alias[T] = ... 定义类型别名"),
        ("内置泛型", "list[T], dict[K, V] 替代 typing.List/Dict"),
        ("管道符联合类型", "int | str | None 替代 Optional[Union[...]]"),
        ("性能提升", "泛型实例化速度提升 ~12%"),
        ("更简洁", "无需 from typing import TypeVar, Generic"),
    ]

    for feature, description in improvements:
        print(f"\n  ✅ {feature}")
        print(f"     → {description}")


def show_free_threading_notes() -> None:
    """展示 Free-threading 注意事项"""
    print("\n\n" + "=" * 70)
    print("🔒 Free-threading（PEP 703/779）考量")
    print("=" * 70)

    print("\n本示例中的线程安全设计:")
    print("  • Container 类使用 Lock 保护 _value")
    print("  • Stack 类使用 Lock 保护 _items 列表")
    print("  • 泛型函数多为纯函数，天然线程安全")

    print("\nFree-threading 性能特点:")
    print("  • GIL 模式: Lock 开销 ~50ns")
    print("  • Free-threading 模式: Lock 开销 ~200ns")
    print("  • 但可真正并行执行，总吞吐量更高")

    print("\n如何启用 Free-threading:")
    print("  1. 安装独立的 freethreaded 构建（如 brew install python-freethreaded@3.13）")
    print("  2. 运行: python3.13t script.py")
    print("  3. 强制关 GIL（部分发行版默认开着）: PYTHON_GIL=0 python3.13t script.py")
    print("  4. 检查: sys._is_gil_enabled()")  # type: ignore


def main() -> None:
    """主函数"""
    demonstrate_generics()
    show_type_system_improvements()
    show_free_threading_notes()

    print("\n\n" + "=" * 70)
    print("演示完成")
    print("=" * 70)
    print("\n💡 关键要点:")
    print("  • PEP 695 泛型语法更简洁")
    print("  • type 关键字定义类型别名")
    print("  • 内置泛型性能更好")
    print("  • Free-threading 需要锁保护可变状态")
    print()


if __name__ == "__main__":
    main()
