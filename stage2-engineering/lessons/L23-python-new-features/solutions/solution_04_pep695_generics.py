"""

from __future__ import annotations

练习 4: PEP 695 泛型编程 - 参考答案

===============================================================================
解题思路: 使用 PEP 695 泛型语法实现通用数据结构和算法
===============================================================================
"""

from collections.abc import Callable
from threading import Lock

# ==================== 泛型函数实现 ====================


def map_list[T, R](items: list[T], mapper: Callable[[T], R]) -> list[R]:
    """泛型映射函数"""
    return [mapper(item) for item in items]


def reduce_list[T, R](items: list[T], reducer: Callable[[R, T], R], initial: R) -> R:
    """泛型归约函数"""
    result = initial
    for item in items:
        result = reducer(result, item)
    return result


def zip_lists[T, U](list1: list[T], list2: list[U]) -> list[tuple[T, U]]:
    """泛型压缩函数"""
    return [(list1[i], list2[i]) for i in range(min(len(list1), len(list2)))]


# ==================== 泛型队列类实现 ====================


class Queue[T]:
    """
    泛型队列（FIFO）

    🔒 Free-threading 线程安全:
    - 使用 Lock 保护 _items 列表
    - 在 python3.13t 环境下多线程安全
    """

    def __init__(self) -> None:
        """初始化队列"""
        self._items: list[T] = []
        self._lock = Lock()  # 🔒 Free-threading 线程安全

    def enqueue(self, item: T) -> None:
        """入队（线程安全）"""
        with self._lock:
            self._items.append(item)

    def dequeue(self) -> T | None:
        """出队（线程安全）"""
        with self._lock:
            return self._items.pop(0) if self._items else None

    def is_empty(self) -> bool:
        """判断是否为空"""
        with self._lock:
            return len(self._items) == 0

    def size(self) -> int:
        """获取队列大小"""
        with self._lock:
            return len(self._items)


# ==================== type 类型别名 ====================

type Optional[T] = T | None
type Result[T, E] = T | E
type Validator[T] = Callable[[T], bool]


# ==================== 测试代码 ====================


def test_generics():
    """测试泛型功能"""
    print("=" * 70)
    print("Python 3.13 PEP 695 泛型编程 - 参考答案")
    print("=" * 70)

    # 测试泛型函数
    print("\n1️⃣ 泛型函数")
    print("-" * 70)

    # map_list
    numbers = [1, 2, 3, 4, 5]
    strings = map_list(numbers, str)
    print(f"map_list([1,2,3,4,5], str) = {strings}")

    # reduce_list
    total = reduce_list(numbers, lambda acc, x: acc + x, 0)
    print(f"reduce_list([1,2,3,4,5], sum, 0) = {total}")

    product = reduce_list(numbers, lambda acc, x: acc * x, 1)
    print(f"reduce_list([1,2,3,4,5], mul, 1) = {product}")

    # zip_lists
    zipped = zip_lists([1, 2, 3], ["a", "b", "c"])
    print(f"zip_lists([1,2,3], ['a','b','c']) = {zipped}")

    # 测试泛型类
    print("\n\n2️⃣ 泛型队列")
    print("-" * 70)

    queue: Queue[int] = Queue()
    print(f"创建空队列，is_empty = {queue.is_empty()}")

    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    print(f"入队 10, 20, 30，size = {queue.size()}")

    print(f"出队: {queue.dequeue()}")
    print(f"出队: {queue.dequeue()}")
    print(f"剩余 size = {queue.size()}")

    # 字符串队列
    print("\n字符串队列:")
    str_queue: Queue[str] = Queue()
    str_queue.enqueue("hello")
    str_queue.enqueue("world")
    print(f"出队: {str_queue.dequeue()}")
    print(f"出队: {str_queue.dequeue()}")

    # 测试 type 类型别名
    print("\n\n3️⃣ type 类型别名")
    print("-" * 70)

    def validate_positive(x: int) -> bool:
        """验证器示例"""
        return x > 0

    validator: Validator[int] = validate_positive
    print(f"validator(5) = {validator(5)}")
    print(f"validator(-3) = {validator(-3)}")

    def safe_divide(a: int, b: int) -> Result[float, str]:
        """返回结果或错误消息"""
        if b == 0:
            return "除数不能为零"
        return a / b

    result1 = safe_divide(10, 2)
    print(f"safe_divide(10, 2) = {result1}")

    result2 = safe_divide(10, 0)
    print(f"safe_divide(10, 0) = {result2}")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    test_generics()
