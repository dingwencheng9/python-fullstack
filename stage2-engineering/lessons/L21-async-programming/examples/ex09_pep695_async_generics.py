"""

from __future__ import annotations

L19 示例 9: PEP 695 泛型语法在异步编程中的应用

展示 Python 3.13 PEP 695 新泛型语法如何与异步编程结合：
1. 泛型异步函数
2. 泛型异步生成器
3. 泛型异步上下文管理器
4. 泛型异步迭代器
5. Free-threading 考量 (Python 3.14)

作者: Python 3.13 全栈课程
日期: 2026-06-09
Python版本: 3.13+
"""

import asyncio
from collections.abc import AsyncGenerator, AsyncIterator, Callable
from contextlib import asynccontextmanager
from threading import Lock
from typing import Any  # Any 用于表示未知类型的原始数据，无原生替代

# ============================================
# PEP 695: 泛型异步函数
# ============================================


async def fetch_data[T](
    url: str,
    parser: Callable[[dict[str, Any]], T],
) -> T:
    """
    泛型异步获取函数

    Python 3.13 PEP 695 特性：
    - 使用 [T] 声明类型参数，无需 TypeVar
    - 类型推断自动传播到返回值
    - IDE 能准确推断出返回类型

    Args:
        url: 数据源 URL（演示用，实际未使用）
        parser: 解析函数，将原始数据转换为类型 T

    Returns:
        解析后的数据，类型为 T
    """
    await asyncio.sleep(0.1)  # 模拟网络请求
    raw_data = {"id": 1, "name": "Alice", "score": 95}
    return parser(raw_data)


async def fetch_multiple[T](
    urls: list[str], parser: Callable[[dict[str, Any]], T]
) -> list[T]:
    """
    并发获取多个资源（泛型版本）

    🔒 线程安全（Python 3.14）：
    - asyncio.gather 本身是线程安全的
    - 可以在 Free-threading 环境中安全使用
    """
    tasks = [fetch_data(url, parser) for url in urls]
    return await asyncio.gather(*tasks)


# ============================================
# PEP 695: 泛型异步生成器
# ============================================


async def async_range[T](
    start: int, stop: int, transformer: Callable[[int], T]
) -> AsyncGenerator[T]:
    """
    泛型异步生成器

    PEP 695 优势：
    - [T] 声明让返回类型自动推断为 AsyncGenerator[T]
    - 无需显式导入和声明 TypeVar

    Args:
        start: 起始值
        stop: 结束值
        transformer: 转换函数，将 int 转换为类型 T

    Yields:
        转换后的值，类型为 T
    """
    for i in range(start, stop):
        await asyncio.sleep(0.01)  # 模拟异步操作
        yield transformer(i)


async def paginate[T](items: list[T], page_size: int) -> AsyncGenerator[list[T]]:
    """
    异步分页生成器（泛型版本）

    应用场景：
    - 大数据集分批处理
    - 内存优化
    - 流式 API 响应

    🔒 线程安全（Python 3.14）：
    - 生成器本身不持有可变状态，线程安全
    - items 参数为不可变引用，安全
    """
    for i in range(0, len(items), page_size):
        await asyncio.sleep(0.05)  # 模拟异步处理
        yield items[i : i + page_size]


# ============================================
# PEP 695: 泛型异步上下文管理器
# ============================================


@asynccontextmanager
async def async_resource[T](
    resource: T,
    setup: Callable[[T], None] | None = None,
    cleanup: Callable[[T], None] | None = None,
) -> AsyncIterator[T]:
    """
    泛型异步资源管理器

    PEP 695 特性：
    - [T] 自动推断资源类型
    - 使用 | None 而非 Optional[Callable]

    Args:
        resource: 要管理的资源
        setup: 可选的初始化函数
        cleanup: 可选的清理函数

    Yields:
        管理的资源
    """
    # 初始化
    if setup:
        setup(resource)
    print(f"🔧 资源初始化: {type(resource).__name__}")

    try:
        yield resource
    finally:
        # 清理
        if cleanup:
            cleanup(resource)
        print(f"🧹 资源清理: {type(resource).__name__}")
        await asyncio.sleep(0.01)  # 模拟异步清理


class AsyncPool[T]:
    """
    泛型异步对象池

    Free-threading（PEP 703/779）考量：
    - 使用 Lock 保护内部状态 (_available)
    - 在 Free-threading 模式下确保并发安全
    """

    def __init__(self, factory: Callable[[], T], size: int) -> None:
        """
        初始化对象池

        Args:
            factory: 对象工厂函数
            size: 池大小
        """
        self._available: list[T] = [factory() for _ in range(size)]
        self._in_use: set[T] = set()
        # 🔒 线程安全：保护池状态
        self._lock = Lock()

    async def acquire(self) -> T:
        """
        从池中获取对象

        🔒 线程安全（Python 3.14）：
        使用锁保护 _available 和 _in_use 的修改
        """
        while True:
            with self._lock:
                if self._available:
                    obj = self._available.pop()
                    self._in_use.add(obj)
                    return obj
            # 无可用对象，等待后重试
            await asyncio.sleep(0.01)

    async def release(self, obj: T) -> None:
        """
        归还对象到池

        🔒 线程安全（Python 3.14）：
        使用锁保护状态修改
        """
        with self._lock:
            if obj in self._in_use:
                self._in_use.remove(obj)
                self._available.append(obj)

    @asynccontextmanager
    async def get(self) -> AsyncIterator[T]:
        """
        上下文管理器方式使用池对象

        使用示例:
            async with pool.get() as obj:
                # 使用 obj
                pass
        """
        obj = await self.acquire()
        try:
            yield obj
        finally:
            await self.release(obj)


# ============================================
# PEP 695: 类型别名与泛型组合
# ============================================

# 使用 type 关键字定义类型别名（Python 3.13）
type AsyncFetcher[T] = Callable[[str], AsyncGenerator[T]]
type AsyncTransformer[T, R] = Callable[[T], R]
type AsyncResult[T] = T | Exception


async def safe_fetch[T](fetcher: Callable[[], T | Exception]) -> AsyncResult[T]:
    """
    安全获取函数（返回结果或异常）

    Python 3.13 类型提示最佳实践：
    - 使用 T | Exception 而非 Union[T, Exception]
    - 使用 type 关键字定义类型别名
    """
    try:
        await asyncio.sleep(0.01)
        return fetcher()
    except Exception as e:
        return e


# ============================================
# 演示函数
# ============================================


async def demo_generic_async_functions() -> None:
    """演示泛型异步函数"""
    print("\n" + "=" * 60)
    print("1. PEP 695: 泛型异步函数")
    print("=" * 60)

    # 定义解析器
    def parse_user(data: dict[str, Any]) -> dict[str, str | int]:
        return {"id": data["id"], "name": data["name"], "score": data["score"]}

    # 单个请求
    user = await fetch_data("https://api.example.com/user/1", parse_user)
    print(f"✅ 获取用户: {user}")

    # 批量请求
    urls = [f"https://api.example.com/user/{i}" for i in range(1, 4)]
    users = await fetch_multiple(urls, parse_user)
    print(f"✅ 批量获取 {len(users)} 个用户")


async def demo_generic_async_generators() -> None:
    """演示泛型异步生成器"""
    print("\n" + "=" * 60)
    print("2. PEP 695: 泛型异步生成器")
    print("=" * 60)

    # 使用异步范围生成器
    print("生成平方数序列:")
    async for square in async_range(1, 6, lambda x: x**2):
        print(f"  {square}", end=" ")
    print()

    # 使用分页生成器
    items = list(range(1, 21))
    print(f"\n分页处理 {len(items)} 个项目 (每页 5 个):")
    page_num = 1
    async for page in paginate(items, 5):
        print(f"  第 {page_num} 页: {page}")
        page_num += 1


async def demo_generic_context_managers() -> None:
    """演示泛型异步上下文管理器"""
    print("\n" + "=" * 60)
    print("3. PEP 695: 泛型异步上下文管理器")
    print("=" * 60)

    # 使用泛型资源管理器
    class Connection:
        def __init__(self, name: str) -> None:
            self.name = name

    def setup_conn(conn: Connection) -> None:
        print(f"  设置连接: {conn.name}")

    def cleanup_conn(conn: Connection) -> None:
        print(f"  关闭连接: {conn.name}")

    async with async_resource(
        Connection("db-primary"), setup=setup_conn, cleanup=cleanup_conn
    ) as conn:
        print(f"  ✅ 使用连接: {conn.name}")


async def demo_generic_pool() -> None:
    """演示泛型异步对象池"""
    print("\n" + "=" * 60)
    print("4. PEP 695: 泛型异步对象池 + Free-threading 考量")
    print("=" * 60)
    print("🔒 对象池使用 Lock 保护，Free-threading 安全\n")

    # 创建连接池
    class DBConnection:
        _counter = 0

        def __init__(self) -> None:
            DBConnection._counter += 1
            self.id = DBConnection._counter

        def __repr__(self) -> str:
            return f"Connection#{self.id}"

    pool: AsyncPool[DBConnection] = AsyncPool(DBConnection, size=3)

    # 使用连接池
    async def use_connection(task_id: int) -> None:
        async with pool.get() as conn:
            print(f"  任务 {task_id} 使用 {conn}")
            await asyncio.sleep(0.05)
            print(f"  任务 {task_id} 完成")

    # 并发执行多个任务
    tasks = [use_connection(i) for i in range(5)]
    await asyncio.gather(*tasks)


async def demo_type_aliases() -> None:
    """演示类型别名与泛型"""
    print("\n" + "=" * 60)
    print("5. type 关键字 + 泛型组合")
    print("=" * 60)

    # 使用 AsyncResult 类型别名
    result1: AsyncResult[int] = await safe_fetch(lambda: 42)
    print(f"✅ 成功结果: {result1}")

    result2: AsyncResult[str] = await safe_fetch(
        lambda: (_ for _ in ()).throw(ValueError("错误"))  # type: ignore
    )
    print(f"❌ 错误结果: {result2}")


async def main() -> None:
    """主函数"""
    print("\n" + "=" * 60)
    print("  Python 3.13 PEP 695 泛型 × 异步编程")
    print("=" * 60)
    print("\n🚀 展示 PEP 695 新语法在异步编程中的应用")
    print("   运行环境要求: Python 3.13 (PEP 695)")
    print("   Free-threading: Python 3.14 (实验性)\n")

    await demo_generic_async_functions()
    await demo_generic_async_generators()
    await demo_generic_context_managers()
    await demo_generic_pool()
    await demo_type_aliases()

    print("\n" + "=" * 60)
    print("  演示完成")
    print("=" * 60)
    print("\n✨ PEP 695 核心优势:")
    print("  1. 无需导入 TypeVar - 使用 [T] 声明")
    print("  2. 类型自动推断 - IDE 支持更好")
    print("  3. 语法简洁 - 代码更易读")
    print("  4. 与 async/await 完美结合")
    print("\n🔒 Free-threading 考量:")
    print("  - AsyncPool 使用 Lock 保护状态")
    print("  - asyncio 原语本身线程安全")
    print("  - 建议使用 python3.13t 测试无 GIL 性能")
    print()


if __name__ == "__main__":
    asyncio.run(main())
