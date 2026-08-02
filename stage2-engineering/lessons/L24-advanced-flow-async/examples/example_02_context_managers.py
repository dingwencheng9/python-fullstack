"""示例 2: 上下文管理器

展示：
- @contextmanager 装饰器
- @asynccontextmanager 装饰器
- 手写类 vs 装饰器对比
- 资源管理最佳实践
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager
from typing import TextIO

# ============================================================================
# 手写上下文管理器类 (旧模式)
# ============================================================================


class FileManagerOld:
    """手写文件管理器（旧模式）"""

    def __init__(self, filename: str, mode: str = "r") -> None:
        self.filename = filename
        self.mode = mode
        self.file: TextIO | None = None

    def __enter__(self) -> TextIO:
        print(f"[Old] 打开文件: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        if self.file:
            print(f"[Old] 关闭文件: {self.filename}")
            self.file.close()


# ============================================================================
# 装饰器上下文管理器 (现代模式)
# ============================================================================


@contextmanager
def file_manager(filename: str, mode: str = "r") -> Generator[TextIO]:
    """文件管理器（现代模式）"""
    print(f"[New] 打开文件: {filename}")
    file = open(filename, mode)

    try:
        yield file  # 进入 with 块
    finally:
        print(f"[New] 关闭文件: {filename}")
        file.close()


def demo_context_managers() -> None:
    """对比手写类和装饰器"""
    print("=== 上下文管理器对比 ===\n")

    # 创建测试文件
    with open("/tmp/test.txt", "w") as f:
        f.write("Hello, World!")

    # 旧模式
    print("1. 旧模式（手写类）:")
    with FileManagerOld("/tmp/test.txt") as f:
        content = f.read()
        print(f"   内容: {content}")

    print()

    # 新模式
    print("2. 新模式（装饰器）:")
    with file_manager("/tmp/test.txt") as f:
        content = f.read()
        print(f"   内容: {content}")

    print()


# ============================================================================
# 异步上下文管理器
# ============================================================================


class AsyncResourceOld:
    """手写异步资源管理器（旧模式）"""

    def __init__(self, name: str) -> None:
        self.name = name

    async def __aenter__(self) -> str:
        print(f"[Old Async] 打开资源: {self.name}")
        await asyncio.sleep(0.1)
        return self.name

    async def __aexit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        print(f"[Old Async] 关闭资源: {self.name}")
        await asyncio.sleep(0.1)


@asynccontextmanager
async def async_resource(name: str) -> AsyncGenerator[str]:
    """异步资源管理器（现代模式）"""
    print(f"[New Async] 打开资源: {name}")
    await asyncio.sleep(0.1)

    try:
        yield name
    finally:
        print(f"[New Async] 关闭资源: {name}")
        await asyncio.sleep(0.1)


async def demo_async_context_managers() -> None:
    """对比异步上下文管理器"""
    print("=== 异步上下文管理器对比 ===\n")

    # 旧模式
    print("1. 旧模式（手写类）:")
    async with AsyncResourceOld("Database") as resource:
        print(f"   使用资源: {resource}")

    print()

    # 新模式
    print("2. 新模式（装饰器）:")
    async with async_resource("Database") as resource:
        print(f"   使用资源: {resource}")

    print()


# ============================================================================
# 实战：数据库连接池
# ============================================================================


class ConnectionPool:
    """模拟数据库连接池"""

    def __init__(self, size: int) -> None:
        self.size = size
        self.connections: list[int] = []

    async def connect(self) -> None:
        """连接"""
        print(f"正在创建 {self.size} 个连接...")
        for i in range(self.size):
            await asyncio.sleep(0.1)
            self.connections.append(i)
        print(f"✓ 连接池已创建 ({len(self.connections)} 个连接)")

    async def close(self) -> None:
        """关闭"""
        print(f"正在关闭 {len(self.connections)} 个连接...")
        for conn in self.connections:
            await asyncio.sleep(0.05)
        self.connections.clear()
        print("✓ 连接池已关闭")

    async def query(self, sql: str) -> list[dict[str, object]]:
        """查询"""
        await asyncio.sleep(0.1)
        return [{"id": 1, "name": "Test"}]


@asynccontextmanager
async def db_pool(size: int = 5) -> AsyncGenerator[ConnectionPool]:
    """数据库连接池上下文管理器"""
    pool = ConnectionPool(size)

    # 初始化
    await pool.connect()

    try:
        yield pool
    finally:
        # 清理
        await pool.close()


async def demo_db_pool() -> None:
    """演示数据库连接池"""
    print("=== 数据库连接池示例 ===\n")

    async with db_pool(size=3) as pool:
        print("\n执行查询:")
        results = await pool.query("SELECT * FROM users")
        print(f"  结果: {results}")

    print()


# ============================================================================
# 实战：监控上下文
# ============================================================================


@contextmanager
def timer(name: str) -> Generator[None]:
    """计时器上下文"""
    print(f"[{name}] 开始")
    start = time.time()

    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"[{name}] 完成，耗时: {elapsed:.3f}s")


def demo_timer() -> None:
    """演示计时器"""
    print("=== 计时器示例 ===\n")

    with timer("数据处理"):
        time.sleep(0.5)
        print("  处理中...")

    print()


# ============================================================================
# 实战：事务管理
# ============================================================================


@asynccontextmanager
async def transaction() -> AsyncGenerator[dict[str, object]]:
    """事务上下文管理器"""
    print("BEGIN TRANSACTION")
    tx = {"active": True, "operations": []}

    try:
        yield tx

        # 成功提交
        if tx["active"]:
            print("COMMIT TRANSACTION")
            print(f"  执行了 {len(tx['operations'])} 个操作")

    except Exception as e:
        # 回滚
        print("ROLLBACK TRANSACTION")
        print(f"  原因: {e}")
        raise


async def demo_transaction() -> None:
    """演示事务管理"""
    print("=== 事务管理示例 ===\n")

    # 成功的事务
    print("1. 成功事务:")
    async with transaction() as tx:
        tx["operations"].append("INSERT")
        tx["operations"].append("UPDATE")
        print("  执行操作...")

    print()

    # 失败的事务
    print("2. 失败事务:")
    try:
        async with transaction() as tx:
            tx["operations"].append("INSERT")
            print("  执行操作...")
            raise ValueError("数据验证失败")
    except ValueError:
        pass

    print()


# ============================================================================
# 主程序
# ============================================================================


async def main() -> None:
    """运行所有示例"""
    # 同步上下文管理器
    demo_context_managers()

    # 异步上下文管理器
    await demo_async_context_managers()

    # 数据库连接池
    await demo_db_pool()

    # 计时器
    demo_timer()

    # 事务管理
    await demo_transaction()


if __name__ == "__main__":
    asyncio.run(main())
