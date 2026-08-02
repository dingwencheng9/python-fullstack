"""示例 4: PEP 695 泛型语法 (Python 3.13)

展示：
- type 类型别名语法
- 泛型函数语法 [T]
- 泛型类语法
- 与 collections.abc 的组合
- 线程安全考量 (Python 3.14)
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Callable

# ============================================================================
# PEP 695: 类型别名 (type 关键字)
# ============================================================================


# 旧语法 (Python 3.9-3.11)
# from typing import TypeAlias
# Vector: TypeAlias = list[float]

# 新语法 (Python 3.13)
type Vector = list[float]
type Matrix = list[Vector]
type JsonValue = dict[str, object] | list[object] | str | int | float | bool | None


def demo_type_aliases() -> None:
    """演示类型别名"""
    print("=== PEP 695 类型别名 ===\n")

    # 使用 Vector 类型
    v1: Vector = [1.0, 2.0, 3.0]
    v2: Vector = [4.0, 5.0, 6.0]

    print(f"向量 1: {v1}")
    print(f"向量 2: {v2}")

    # 使用 Matrix 类型
    matrix: Matrix = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0],
    ]

    print(f"矩阵: {matrix}")

    # 使用 JsonValue 类型
    json_data: JsonValue = {
        "name": "Alice",
        "age": 30,
        "scores": [95, 87, 92],
    }

    print(f"JSON 数据: {json_data}")
    print()


# ============================================================================
# PEP 695: 泛型函数 [T]
# ============================================================================


# 旧语法 (Python 3.9-3.11)
# from typing import TypeVar
# T = TypeVar('T')
# def first_old(items: list[T]) -> T:
#     return items[0]


# 新语法 (Python 3.13)
def first[T](items: list[T]) -> T:
    """返回列表的第一个元素"""
    return items[0]


def last[T](items: list[T]) -> T:
    """返回列表的最后一个元素"""
    return items[-1]


def reverse[T](items: list[T]) -> list[T]:
    """反转列表"""
    return items[::-1]


def map_list[T, U](items: list[T], func: Callable[[T], U]) -> list[U]:
    """
    映射列表元素

    展示多个类型参数的使用
    """
    return [func(item) for item in items]


def demo_generic_functions() -> None:
    """演示泛型函数"""
    print("=== PEP 695 泛型函数 ===\n")

    # 整数列表
    numbers = [1, 2, 3, 4, 5]
    print(f"数字列表: {numbers}")
    print(f"第一个: {first(numbers)}")
    print(f"最后一个: {last(numbers)}")
    print(f"反转: {reverse(numbers)}")

    # 字符串列表
    words = ["hello", "world", "python"]
    print(f"\n字符串列表: {words}")
    print(f"第一个: {first(words)}")
    print(f"最后一个: {last(words)}")

    # 映射函数
    squared = map_list(numbers, lambda x: x**2)
    print(f"\n平方映射: {squared}")

    lengths = map_list(words, len)
    print(f"长度映射: {lengths}")

    print()


# ============================================================================
# PEP 695: 泛型类
# ============================================================================


# 旧语法 (Python 3.9-3.11)
# from typing import Generic, TypeVar
# T = TypeVar('T')
# class Stack(Generic[T]):
#     ...


# 新语法 (Python 3.13)
class Stack[T]:
    """
    泛型栈实现

    Python 3.14 线程安全考量：
        - 如果多个线程同时访问 _items，需要使用 threading.Lock
        - 在纯 asyncio 环境中，单事件循环保证线程安全
        - 如果需要跨线程共享，使用 queue.Queue 替代 list
    """

    def __init__(self) -> None:
        self._items: list[T] = []
        # 生产环境应添加: self._lock = threading.Lock()

    def push(self, item: T) -> None:
        """压栈"""
        # 在 Python 3.14 中，如果跨线程访问：
        # with self._lock:
        #     self._items.append(item)
        self._items.append(item)

    def pop(self) -> T:
        """出栈"""
        if not self._items:
            raise IndexError("Stack is empty")
        # 在 Python 3.14 中，如果跨线程访问：
        # with self._lock:
        #     return self._items.pop()
        return self._items.pop()

    def peek(self) -> T:
        """查看栈顶"""
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items[-1]

    def is_empty(self) -> bool:
        """检查是否为空"""
        return len(self._items) == 0

    def size(self) -> int:
        """栈大小"""
        return len(self._items)


class Queue[T]:
    """
    泛型队列实现

    Python 3.14 线程安全考量：
        - asyncio.Queue 内部使用锁，天然线程安全
        - 自定义 list 实现需要手动加锁
        - collections.deque 也需要在跨线程时加锁
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def enqueue(self, item: T) -> None:
        """入队"""
        self._items.append(item)

    def dequeue(self) -> T:
        """出队"""
        if not self._items:
            raise IndexError("Queue is empty")
        return self._items.pop(0)

    def is_empty(self) -> bool:
        """检查是否为空"""
        return len(self._items) == 0

    def size(self) -> int:
        """队列大小"""
        return len(self._items)


def demo_generic_classes() -> None:
    """演示泛型类"""
    print("=== PEP 695 泛型类 ===\n")

    # 整数栈
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    int_stack.push(3)

    print(f"整数栈大小: {int_stack.size()}")
    print(f"栈顶: {int_stack.peek()}")
    print(f"出栈: {int_stack.pop()}")
    print(f"出栈: {int_stack.pop()}")
    print(f"剩余大小: {int_stack.size()}")

    # 字符串队列
    str_queue: Queue[str] = Queue()
    str_queue.enqueue("first")
    str_queue.enqueue("second")
    str_queue.enqueue("third")

    print(f"\n字符串队列大小: {str_queue.size()}")
    print(f"出队: {str_queue.dequeue()}")
    print(f"出队: {str_queue.dequeue()}")
    print(f"剩余大小: {str_queue.size()}")

    print()


# ============================================================================
# PEP 695: 泛型 + 异步生成器
# ============================================================================


async def async_range[T](start: T, stop: T, step: T) -> AsyncGenerator[T]:
    """
    泛型异步范围生成器

    展示 PEP 695 与 AsyncGenerator 的组合
    """
    current = start
    while current < stop:
        await asyncio.sleep(0.01)
        yield current
        current += step  # type: ignore


async def async_map[T, U](
    items: AsyncGenerator[T],
    func: Callable[[T], U],
) -> AsyncGenerator[U]:
    """
    异步映射生成器

    展示泛型异步生成器的转换
    """
    async for item in items:
        yield func(item)


async def demo_generic_async_generators() -> None:
    """演示泛型异步生成器"""
    print("=== PEP 695 泛型异步生成器 ===\n")

    # 整数范围
    print("异步整数范围 (0-10, step=2):")
    async for num in async_range(0, 10, 2):
        print(f"  {num}", end=" ")
    print("\n")

    # 浮点数范围
    print("异步浮点数范围 (0.0-1.0, step=0.2):")
    async for num in async_range(0.0, 1.0, 0.2):
        print(f"  {num:.1f}", end=" ")
    print("\n")

    # 映射转换
    print("映射转换 (平方):")
    async for squared in async_map(async_range(1, 6, 1), lambda x: x**2):
        print(f"  {squared}", end=" ")
    print("\n")


# ============================================================================
# PEP 695: 泛型资源池（实战）
# ============================================================================


class ResourcePool[T]:
    """
    通用资源池

    Python 3.14 线程安全分析：
        - asyncio.Queue 在无 GIL 环境下是线程安全的
        - 如果从多个线程调用 acquire/release，需要确保：
          1. 所有调用都在同一个事件循环中
          2. 或使用 asyncio.Lock 保护资源池状态

    生产环境最佳实践：
        - 使用 asyncio.Queue（内置锁保护）
        - 避免跨线程共享资源池
        - 如果必须跨线程，使用 queue.Queue + 线程池
    """

    def __init__(self, resources: list[T]) -> None:
        self._all_resources = resources
        self._available: asyncio.Queue[T] = asyncio.Queue()
        self._initialized = False

    async def initialize(self) -> None:
        """初始化资源池"""
        if self._initialized:
            return

        for resource in self._all_resources:
            await self._available.put(resource)

        self._initialized = True
        print(f"资源池已初始化 ({len(self._all_resources)} 个资源)")

    async def acquire(self) -> T:
        """获取资源"""
        return await self._available.get()

    async def release(self, resource: T) -> None:
        """释放资源"""
        await self._available.put(resource)

    def size(self) -> int:
        """资源总数"""
        return len(self._all_resources)


async def demo_resource_pool() -> None:
    """演示通用资源池"""
    print("=== PEP 695 通用资源池 ===\n")

    # 创建连接池
    connections = [f"conn-{i}" for i in range(3)]
    pool: ResourcePool[str] = ResourcePool(connections)
    await pool.initialize()

    print(f"连接池大小: {pool.size()}\n")

    # 模拟并发任务
    async def worker(worker_id: int) -> None:
        conn = await pool.acquire()
        print(f"Worker-{worker_id} 获取连接: {conn}")
        await asyncio.sleep(0.1)
        print(f"Worker-{worker_id} 释放连接: {conn}")
        await pool.release(conn)

    # 5 个任务竞争 3 个连接
    async with asyncio.TaskGroup() as tg:
        for i in range(5):
            tg.create_task(worker(i))

    print("\n✓ 所有任务完成")
    print()


# ============================================================================
# 主程序
# ============================================================================


async def main() -> None:
    """运行所有示例"""
    # 类型别名
    demo_type_aliases()

    # 泛型函数
    demo_generic_functions()

    # 泛型类
    demo_generic_classes()

    # 泛型异步生成器
    await demo_generic_async_generators()

    # 通用资源池
    await demo_resource_pool()


if __name__ == "__main__":
    asyncio.run(main())
