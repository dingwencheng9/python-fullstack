"""

from __future__ import annotations

练习 4: PEP 695 泛型编程

目标：
  - 掌握 PEP 695 泛型语法
  - 理解泛型函数和泛型类
  - 使用 type 关键字定义类型别名

完成标准：
  - 实现所有泛型函数
  - 实现泛型队列类
  - 使用 type 定义类型别名
"""

from collections.abc import Callable

# TODO: 实现泛型函数


def map_list[T, R](items: list[T], mapper: Callable[[T], R]) -> list[R]:
    """
    泛型映射函数

    使用 PEP 695 语法:
    - def func[T, R](...) 声明类型参数
    - list[T] 和 list[R] 内置泛型

    示例:
        map_list([1, 2, 3], str) → ["1", "2", "3"]
        map_list(["a", "b"], len) → [1, 1]
    """
    # TODO: 实现
    raise NotImplementedError("请实现 map_list 函数")


def reduce_list[T, R](items: list[T], reducer: Callable[[R, T], R], initial: R) -> R:
    """
    泛型归约函数

    示例:
        reduce_list([1, 2, 3], lambda acc, x: acc + x, 0) → 6
        reduce_list(["a", "b"], lambda acc, x: acc + x, "") → "ab"
    """
    # TODO: 实现
    raise NotImplementedError("请实现 reduce_list 函数")


def zip_lists[T, U](list1: list[T], list2: list[U]) -> list[tuple[T, U]]:
    """
    泛型压缩函数

    示例:
        zip_lists([1, 2, 3], ["a", "b", "c"]) → [(1, "a"), (2, "b"), (3, "c")]
    """
    # TODO: 实现
    raise NotImplementedError("请实现 zip_lists 函数")


# TODO: 实现泛型队列类


class Queue[T]:
    """
    泛型队列（FIFO）

    使用 PEP 695 语法:
    - class Queue[T]: 声明类型参数

    🔒 Free-threading 考量:
    - 需要使用 Lock 保护 _items 列表
    """

    def __init__(self) -> None:
        """初始化队列"""
        # TODO: 实现
        raise NotImplementedError("请实现 Queue.__init__")

    def enqueue(self, item: T) -> None:
        """入队（线程安全）"""
        # TODO: 实现
        raise NotImplementedError("请实现 Queue.enqueue")

    def dequeue(self) -> T | None:
        """出队（线程安全）"""
        # TODO: 实现
        raise NotImplementedError("请实现 Queue.dequeue")

    def is_empty(self) -> bool:
        """判断是否为空"""
        # TODO: 实现
        raise NotImplementedError("请实现 Queue.is_empty")

    def size(self) -> int:
        """获取队列大小"""
        # TODO: 实现
        raise NotImplementedError("请实现 Queue.size")


# TODO: 使用 type 关键字定义类型别名

# type Optional[T] = T | None
# type Result[T, E] = T | E
# type Validator[T] = Callable[[T], bool]


# === 测试代码 ===
def test_generics():
    """测试泛型功能"""
    print("=" * 60)
    print("练习 4: PEP 695 泛型编程测试")
    print("=" * 60)

    # 测试泛型函数
    print("\n### 测试: 泛型函数")
    print("-" * 60)

    try:
        numbers = [1, 2, 3, 4, 5]
        strings = map_list(numbers, str)
        print(f"✓ map_list: {strings}")
    except NotImplementedError as e:
        print(f"✗ map_list: {e}")

    try:
        numbers = [1, 2, 3, 4, 5]
        total = reduce_list(numbers, lambda acc, x: acc + x, 0)
        print(f"✓ reduce_list: {total}")
    except NotImplementedError as e:
        print(f"✗ reduce_list: {e}")

    try:
        result = zip_lists([1, 2, 3], ["a", "b", "c"])
        print(f"✓ zip_lists: {result}")
    except NotImplementedError as e:
        print(f"✗ zip_lists: {e}")

    # 测试泛型类
    print("\n\n### 测试: 泛型队列")
    print("-" * 60)

    try:
        queue: Queue[int] = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        print(f"✓ 队列大小: {queue.size()}")
        print(f"✓ 出队: {queue.dequeue()}")
        print(f"✓ 出队: {queue.dequeue()}")
        print(f"✓ 队列大小: {queue.size()}")
    except NotImplementedError as e:
        print(f"✗ Queue: {e}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("\n任务:")
    print("  1. 实现所有泛型函数")
    print("  2. 实现泛型队列类（加 Lock 保护）")
    print("  3. 使用 type 关键字定义类型别名")
    print("  4. 运行测试验证功能")
    print("=" * 60)


if __name__ == "__main__":
    test_generics()
