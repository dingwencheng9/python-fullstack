"""练习 2: 异步上下文管理器与资源池

任务：
实现一个带连接池的异步资源管理器

要求：
1. 使用 @asynccontextmanager 装饰器
2. 实现连接池的获取/释放逻辑
3. 使用 PEP 695 泛型语法
4. 通过 mypy --strict 检查
5. 考虑 Python 3.14 的线程安全
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

# ============================================================================
# 连接池基础类（已提供）
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
    """连接池"""

    def __init__(self, size: int) -> None:
        self.size = size
        self.connections: list[Connection] = []
        self.available: asyncio.Queue[Connection] = asyncio.Queue()
        self._initialized = False

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
# TODO: 学生需要实现的部分
# ============================================================================


@asynccontextmanager
async def get_connection(pool: ConnectionPool) -> AsyncGenerator[Connection]:
    """
    从连接池获取连接的上下文管理器

    TODO: 实现以下功能
    1. 从连接池获取连接
    2. yield 连接给调用者
    3. 在 finally 块中释放连接（无论是否发生异常）

    使用方式:
        async with get_connection(pool) as conn:
            result = await conn.execute("SELECT * FROM users")

    线程安全说明 (Python 3.14):
        asyncio.Queue 在无 GIL 环境下是线程安全的，
        但如果直接使用 list 操作需要加锁保护。
    """
    # TODO: 实现
    raise NotImplementedError("请实现 get_connection")
    yield  # 占位符，移除并实现真正的 yield


# 使用 PEP 695 泛型语法定义通用资源池
type ResourcePool[T] = list[T]  # PEP 695: 类型别名


def create_pool[T](items: list[T]) -> ResourcePool[T]:
    """
    创建通用资源池

    TODO: 实现以下功能
    1. 接受任意类型的资源列表
    2. 返回资源池（实际上就是列表，但类型更明确）
    3. 展示 PEP 695 的泛型语法

    示例:
        pool = create_pool([1, 2, 3, 4, 5])
        pool = create_pool(["conn1", "conn2", "conn3"])
    """
    # TODO: 实现
    raise NotImplementedError("请实现 create_pool")


# ============================================================================
# 测试代码
# ============================================================================


async def test_connection_pool() -> None:
    """测试连接池"""
    pool = ConnectionPool(size=3)
    await pool.initialize()

    print("\n执行并发查询:")

    try:
        # 使用连接池执行 5 个并发查询
        async with asyncio.TaskGroup() as tg:
            for i in range(5):
                tg.create_task(execute_query(pool, f"Query-{i}"))

        print("\n✓ 所有查询完成")

    except* NotImplementedError:
        print("\n✗ 请先实现 get_connection 函数")

    finally:
        await pool.close()


async def execute_query(pool: ConnectionPool, query: str) -> None:
    """执行单个查询"""
    try:
        async with get_connection(pool) as conn:
            result = await conn.execute(query)
            print(f"  查询 {query} 完成: {len(result)} 条结果")
    except NotImplementedError:
        raise


if __name__ == "__main__":
    asyncio.run(test_connection_pool())
