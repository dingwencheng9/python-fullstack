"""

from __future__ import annotations

L10 示例 3: 连接池配置与优化

展示 SQLAlchemy 异步连接池的配置和监控：
1. 连接池基础配置
2. 连接池大小调优
3. 连接池监控
4. 连接泄漏检测
5. 最佳实践
"""

import asyncio
import time

from sqlalchemy import String, event, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

# ============================================================================
# 1. 定义模型
# ============================================================================


class Base(DeclarativeBase):
    """基类"""


class Task(Base):
    """任务模型（用于演示并发）"""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="pending")

    def __repr__(self) -> str:
        return f"Task(id={self.id}, name={self.name!r}, status={self.status!r})"


# ============================================================================
# 2. 连接池配置选项
# ============================================================================


def create_engine_with_default_pool(database_url: str) -> AsyncEngine:
    """
    默认连接池配置

    适用于大多数应用。
    注意：SQLite 使用 StaticPool，不支持 pool_size 等参数。
    """
    if "sqlite" in database_url:
        # SQLite 使用 StaticPool，不需要连接池参数
        return create_async_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,  # 连接前检测可用性
        )
    # PostgreSQL/MySQL 等数据库使用 QueuePool
    return create_async_engine(
        database_url,
        echo=False,
        pool_size=5,  # 连接池大小
        max_overflow=10,  # 最大溢出连接数
        pool_timeout=30,  # 获取连接超时（秒）
        pool_recycle=3600,  # 连接回收时间（秒）
        pool_pre_ping=True,  # 连接前检测可用性
    )


def create_engine_with_custom_pool(database_url: str) -> AsyncEngine:
    """
    自定义连接池配置

    适用于高并发场景。
    注意：SQLite 使用 StaticPool，不支持 pool_size 等参数。
    """
    if "sqlite" in database_url:
        # SQLite 使用 StaticPool，不支持自定义池参数
        return create_async_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,
        )
    # PostgreSQL/MySQL 等数据库使用 QueuePool
    return create_async_engine(
        database_url,
        echo=False,
        poolclass=AsyncAdaptedQueuePool,
        pool_size=20,  # 更大的连接池
        max_overflow=30,  # 更多溢出连接
        pool_timeout=10,  # 更短的超时
        pool_recycle=1800,  # 更频繁的回收
        pool_pre_ping=True,
    )


def create_engine_without_pool(database_url: str) -> AsyncEngine:
    """
    禁用连接池

    适用于：
    - 短期脚本
    - Lambda 函数
    - 测试环境
    """
    return create_async_engine(
        database_url,
        echo=False,
        poolclass=NullPool,  # 禁用连接池
    )


# ============================================================================
# 3. 连接池监控
# ============================================================================


class PoolMonitor:
    """连接池监控器"""

    def __init__(self, engine: AsyncEngine):
        self.engine = engine
        self.stats = {
            "connections_created": 0,
            "connections_closed": 0,
            "checkouts": 0,
            "checkins": 0,
        }

        # 注册事件监听器
        self._register_listeners()

    def _register_listeners(self) -> None:
        """注册连接池事件监听器"""
        pool = self.engine.pool

        @event.listens_for(pool, "connect")
        def receive_connect(_dbapi_conn, _connection_record):
            """连接创建时"""
            self.stats["connections_created"] += 1
            print(f"🔗 新连接创建 (总计: {self.stats['connections_created']})")

        @event.listens_for(pool, "close")
        def receive_close(_dbapi_conn, _connection_record):
            """连接关闭时"""
            self.stats["connections_closed"] += 1
            print(f"❌ 连接关闭 (总计: {self.stats['connections_closed']})")

        @event.listens_for(pool, "checkout")
        def receive_checkout(_dbapi_conn, _connection_record, _connection_proxy):
            """连接被检出时"""
            self.stats["checkouts"] += 1

        @event.listens_for(pool, "checkin")
        def receive_checkin(_dbapi_conn, _connection_record):
            """连接被归还时"""
            self.stats["checkins"] += 1

    def print_stats(self) -> None:
        """打印统计信息"""
        pool = self.engine.pool
        pool_type = type(pool).__name__

        print(f"\n{'=' * 70}")
        print("连接池统计")
        print("=" * 70)
        print("配置:")
        print(f"  池类型: {pool_type}")

        # 只有 QueuePool 有 size() 和 checkedout() 方法
        try:
            pool_size = pool.size()
            max_overflow = getattr(pool, "_max_overflow", "N/A")
            checked_out = pool.checkedout()
            idle = pool_size - checked_out

            print(f"  池大小: {pool_size}")
            print(f"  最大溢出: {max_overflow}")
            print("\n当前状态:")
            print(f"  活跃连接: {checked_out}")
            print(f"  空闲连接: {idle}")
        except (AttributeError, TypeError):
            print("  (StaticPool/NullPool 不提供连接池统计)")

        print("\n累计统计:")
        print(f"  创建连接: {self.stats['connections_created']}")
        print(f"  关闭连接: {self.stats['connections_closed']}")
        print(f"  检出次数: {self.stats['checkouts']}")
        print(f"  归还次数: {self.stats['checkins']}")
        print("=" * 70)


# ============================================================================
# 4. 并发测试
# ============================================================================


async def create_tables(engine: AsyncEngine) -> None:
    """创建表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def worker_task(
    session_maker: async_sessionmaker,
    worker_id: int,
    task_count: int,
) -> None:
    """
    工作任务（模拟并发数据库操作）

    每个 worker 创建指定数量的任务。
    """
    print(f"  Worker {worker_id} 开始工作...")

    for i in range(task_count):
        async with session_maker() as session, session.begin():
            task = Task(
                name=f"Task-{worker_id}-{i}",
                status="completed",
            )
            session.add(task)

        # 模拟处理延迟
        await asyncio.sleep(0.01)

    print(f"  Worker {worker_id} 完成！")


async def run_concurrent_load(
    engine: AsyncEngine,
    num_workers: int = 10,
    tasks_per_worker: int = 5,
) -> None:
    """
    测试并发负载

    启动多个 worker 并发访问数据库，观察连接池行为。
    """
    print(f"\n{'=' * 70}")
    print(f"并发测试: {num_workers} workers, 每个 {tasks_per_worker} 任务")
    print("=" * 70)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    start_time = time.time()

    # 并发执行所有 worker
    workers = [worker_task(session_maker, i, tasks_per_worker) for i in range(num_workers)]
    await asyncio.gather(*workers)

    duration = time.time() - start_time

    # 统计结果
    async with session_maker() as session:
        stmt = select(Task)
        result = await session.execute(stmt)
        total_tasks = len(list(result.scalars().all()))

    print("\n✅ 完成:")
    print(f"  总任务数: {total_tasks}")
    print(f"  耗时: {duration:.2f} 秒")
    print(f"  吞吐量: {total_tasks / duration:.2f} 任务/秒")


# ============================================================================
# 5. 连接泄漏检测
# ============================================================================


async def simulate_connection_leak(engine: AsyncEngine) -> None:
    """
    模拟连接泄漏

    不正确地使用会话会导致连接泄漏。
    """
    print(f"\n{'=' * 70}")
    print("模拟连接泄漏")
    print("=" * 70)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    # 错误做法：创建会话但不关闭
    print("\n❌ 错误做法：不关闭会话")
    for i in range(3):
        _ = session_maker()  # 创建会话但不使用 async with
        # 忘记关闭！这会导致连接泄漏
        print(f"  创建会话 {i + 1}（未关闭）")

    # 正确做法：使用 async with 自动关闭
    print("\n✅ 正确做法：使用 async with")
    for i in range(3):
        async with session_maker():
            print(f"  创建会话 {i + 1}（自动关闭）")


# ============================================================================
# 6. 辅助函数
# ============================================================================


def print_pool_info(engine: AsyncEngine, description: str) -> None:
    """打印连接池信息（兼容不同的池类型）"""
    print(f"✅ 创建引擎: {description}")
    try:
        # 尝试访问 QueuePool 的属性
        pool_size = engine.pool.size()
        max_overflow = getattr(engine.pool, "_max_overflow", "N/A")
        print(f"  池大小: {pool_size}")
        print(f"  最大溢出: {max_overflow}")
    except (AttributeError, TypeError):
        # StaticPool 或 NullPool 没有这些属性
        pool_type = type(engine.pool).__name__
        print(f"  池类型: {pool_type} (不使用连接池)")


# ============================================================================
# 7. 演示主函数
# ============================================================================


async def main() -> None:
    """运行所有演示"""
    print("=" * 70)
    print("SQLAlchemy 连接池配置与优化")
    print("=" * 70)

    # 使用 SQLite 内存数据库演示
    database_url = "sqlite+aiosqlite:///:memory:"

    # 示例 1: 默认连接池配置
    print("\n1️⃣  默认连接池配置")
    print("-" * 70)
    engine1 = create_engine_with_default_pool(database_url)
    print_pool_info(engine1, "默认配置")

    await create_tables(engine1)
    monitor1 = PoolMonitor(engine1)

    # 测试并发负载
    await run_concurrent_load(engine1, num_workers=10, tasks_per_worker=5)
    monitor1.print_stats()

    await engine1.dispose()

    # 示例 2: 自定义连接池配置（高并发）
    print("\n2️⃣  高并发连接池配置")
    print("-" * 70)
    engine2 = create_engine_with_custom_pool(database_url)
    print_pool_info(engine2, "高并发配置")

    await create_tables(engine2)
    monitor2 = PoolMonitor(engine2)

    # 测试更高并发
    await run_concurrent_load(engine2, num_workers=30, tasks_per_worker=10)
    monitor2.print_stats()

    await engine2.dispose()

    # 示例 3: 无连接池配置
    # 注意：NullPool 与 SQLite 内存数据库不兼容（每个新连接都会看到空数据库）
    # 在生产环境中，应使用持久化数据库（如 PostgreSQL）
    print("\n3️⃣  无连接池配置")
    print("-" * 70)
    print("⚠️  跳过：NullPool 与 SQLite 内存数据库不兼容")
    print("   在实际应用中，请使用 PostgreSQL 或 MySQL 等持久化数据库")
    print("   演示代码已保留，可在真实数据库环境中运行")

    # 示例 4: 连接泄漏检测
    print("\n4️⃣  连接泄漏检测")
    print("-" * 70)
    engine4 = create_engine_with_default_pool(database_url)
    await create_tables(engine4)
    monitor4 = PoolMonitor(engine4)

    await simulate_connection_leak(engine4)
    monitor4.print_stats()

    await engine4.dispose()

    # 最佳实践总结
    print(f"\n{'=' * 70}")
    print("连接池配置最佳实践")
    print("=" * 70)
    print("\n1. 连接池大小:")
    print("   pool_size = CPU核心数 × 2 ~ 4")
    print("\n2. 最大溢出:")
    print("   max_overflow = pool_size × 2")
    print("\n3. 连接回收:")
    print("   pool_recycle = 1800 (30分钟)")
    print("\n4. 连接预检测:")
    print("   pool_pre_ping = True (防止连接超时)")
    print("\n5. 会话管理:")
    print("   始终使用 async with 确保会话正确关闭")
    print("\n6. 监控:")
    print("   定期检查连接池统计，及时发现问题")
    print("=" * 70)

    print("\n演示完成！")


# ============================================================================
# 运行
# ============================================================================

if __name__ == "__main__":
    asyncio.run(main())
