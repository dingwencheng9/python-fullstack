"""练习 2 答案: 异步上下文管理器与资源池

===============================================================================
解题思路
===============================================================================

1. 异步上下文管理器核心模式：
   - 使用 @asynccontextmanager 装饰器
   - 在 yield 前获取资源
   - 在 finally 块中释放资源（保证无论如何都会释放）

2. PEP 695 泛型语法：
   - type Alias[T] = SomeType[T]  # 类型别名
   - def func[T](x: T) -> T:       # 泛型函数
   - class Container[T]:           # 泛型类

3. 线程安全考量（Python 3.14 无 GIL 环境）：
   - asyncio.Queue 内部使用锁，天然线程安全
   - 如果直接操作 list，需要使用 asyncio.Lock 保护
   - 建议优先使用 asyncio 内置的线程安全数据结构

===============================================================================
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

# ============================================================================
# 连接池基础类
# ============================================================================


class Connection:
    """模拟数据库连接"""

    def __init__(self, conn_id: int) -> None:
        self.conn_id = conn_id
        self.in_use = False

    async def execute(self, query: str) -> list[dict[str, object]]:
        """执行查询"""
        await asyncio.sleep(0.1)
        return [{"id": 1, "data": f"Result for: {query}"}]


class ConnectionPool:
    """
    连接池实现

    线程安全说明 (Python 3.14):
        - asyncio.Queue 使用内部锁，在无 GIL 环境下安全
        - _initialized 标志应使用 asyncio.Lock 保护（生产环境）
        - 当前实现适用于单事件循环场景
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.connections: list[Connection] = []
        self.available: asyncio.Queue[Connection] = asyncio.Queue()
        self._initialized = False
        # 生产环境应添加: self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """初始化连接池"""
        if self._initialized:
            return

        print(f"初始化连接池（大小: {self.size}）")
        for i in range(self.size):
            conn = Connection(i)
            self.connections.append(conn)
            await self.available.put(conn)

        self._initialized = True
        print("✓ 连接池已初始化")

    async def acquire(self) -> Connection:
        """获取连接"""
        conn = await self.available.get()
        conn.in_use = True
        print(f"  获取连接 #{conn.conn_id}")
        return conn

    async def release(self, conn: Connection) -> None:
        """释放连接"""
        conn.in_use = False
        await self.available.put(conn)
        print(f"  释放连接 #{conn.conn_id}")

    async def close(self) -> None:
        """关闭连接池"""
        print("关闭连接池")
        self.connections.clear()


# ============================================================================
# 解答：异步上下文管理器
# ============================================================================


@asynccontextmanager
async def get_connection(pool: ConnectionPool) -> AsyncGenerator[Connection]:
    """
    从连接池获取连接的上下文管理器

    关键实现：
    1. 在 yield 前获取连接
    2. yield 连接给调用者
    3. 在 finally 中释放（保证无论是否异常都会执行）
    """
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)


# ============================================================================
# 解答：PEP 695 泛型语法
# ============================================================================


# PEP 695: 类型别名（使用 type 关键字）
type ResourcePool[T] = list[T]


def create_pool[T](items: list[T]) -> ResourcePool[T]:
    """
    创建通用资源池

    PEP 695 泛型语法说明：
    - [T] 在函数名后声明类型参数
    - 不需要 from typing import TypeVar
    - T 的作用域仅限于该函数
    """
    return items


# 扩展：PEP 695 泛型类示例
class GenericPool[T]:
    """
    通用资源池（PEP 695 泛型类语法）

    Python 3.14 线程安全考量：
        - 如果多个线程同时访问 _items，需要使用 threading.Lock
        - 在纯 asyncio 环境中，使用 asyncio.Lock
        - 当前实现假设单线程/单事件循环
    """

    def __init__(self, items: list[T]) -> None:
        self._items = items
        self._available: asyncio.Queue[T] = asyncio.Queue()
        # 生产环境应添加: self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """初始化池"""
        for item in self._items:
            await self._available.put(item)

    async def acquire(self) -> T:
        """获取资源"""
        return await self._available.get()

    async def release(self, item: T) -> None:
        """释放资源"""
        await self._available.put(item)


# ============================================================================
# 高级示例：泛型上下文管理器
# ============================================================================


@asynccontextmanager
async def managed_resource[T](pool: GenericPool[T]) -> AsyncGenerator[T]:
    """
    泛型资源管理器

    展示 PEP 695 + asynccontextmanager 的组合使用
    """
    resource = await pool.acquire()
    try:
        yield resource
    finally:
        await pool.release(resource)


# ============================================================================
# 测试代码
# ============================================================================


async def test_connection_pool() -> None:
    """测试连接池"""
    pool = ConnectionPool(size=3)
    await pool.initialize()

    print("\n执行并发查询:")

    # 使用连接池执行 5 个并发查询（3 个连接，需要排队）
    async with asyncio.TaskGroup() as tg:
        for i in range(5):
            tg.create_task(execute_query(pool, f"Query-{i}"))

    print("\n✓ 所有查询完成")

    await pool.close()


async def execute_query(pool: ConnectionPool, query: str) -> None:
    """执行单个查询"""
    async with get_connection(pool) as conn:
        result = await conn.execute(query)
        print(f"  查询 {query} 完成: {len(result)} 条结果")


async def test_generic_pool() -> None:
    """测试泛型资源池"""
    print("\n" + "=" * 60)
    print("测试 PEP 695 泛型资源池")
    print("=" * 60)

    # 创建字符串资源池
    string_pool: ResourcePool[str] = create_pool(["A", "B", "C"])
    print(f"字符串池: {string_pool}")

    # 创建整数资源池
    int_pool: ResourcePool[int] = create_pool([1, 2, 3, 4, 5])
    print(f"整数池: {int_pool}")

    # 测试泛型类
    generic_pool = GenericPool([10, 20, 30])
    await generic_pool.initialize()

    print("\n测试泛型池的获取/释放:")
    async with managed_resource(generic_pool) as item:
        print(f"  获取资源: {item}")
        await asyncio.sleep(0.1)
    print("  资源已释放")


async def main() -> None:
    """主测试函数"""
    print("=" * 60)
    print("L22 练习 2: 异步上下文管理器与资源池 - 参考答案")
    print("=" * 60)

    # 测试连接池
    await test_connection_pool()

    # 测试泛型池
    await test_generic_pool()

    print("\n" + "=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
