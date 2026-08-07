"""

from __future__ import annotations

SQLAlchemy 2.0 异步数据持久化 - 事务原子性与乐观锁
====================================================

本模块展示 SQLAlchemy 2.0 异步 ORM 的现代化实践：
- AsyncSession 事务管理
- 乐观锁（Optimistic Locking）防止并发冲突
- 慢查询追踪（OpenTelemetry）
- 连接池监控

架构设计：
---------
1. 异步模型定义（Base + Mapped）
2. 异步 Session 工厂
3. 事务上下文管理器
4. 乐观锁版本控制
5. OTel 数据库追踪

对标：
-----
- 粉碎旧模块的同步 ORM（100% Django 同步）
- 呼应 L09 OpenTelemetry 可观测性

作者：Python 3.13 全栈课程
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import UTC, datetime

# OpenTelemetry 集成
from opentelemetry import trace
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import DateTime, Float, Integer, String, select, update
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

tracer = trace.get_tracer(__name__)


# ============================================================
# 数据库配置
# ============================================================

# 异步数据库 URL（支持 PostgreSQL/MySQL/SQLite）
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"
# DATABASE_URL = "mysql+aiomysql://user:pass@localhost/dbname"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 开发环境：打印 SQL
    pool_size=20,  # 连接池大小
    max_overflow=10,  # 最大溢出连接
    pool_pre_ping=True,  # 连接健康检查
)

# 注入 OpenTelemetry 追踪（自动记录所有 SQL 查询）
SQLAlchemyInstrumentor().instrument(
    engine=engine.sync_engine,
    service="inventory-service",
)

# 创建异步 Session 工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 提交后对象仍可访问
)


# ============================================================
# 模型定义（SQLAlchemy 2.0 风格）
# ============================================================


class Base(DeclarativeBase):
    """ORM 基类"""


class Product(Base):
    """
    产品模型（带乐观锁）

    **乐观锁设计**:
    - version 字段追踪修改次数
    - 更新时检查版本号
    - 版本不匹配则抛出异常
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # 乐观锁版本字段（关键）
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="乐观锁版本号",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, stock={self.stock}, version={self.version})>"


class Order(Base):
    """订单模型"""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )


# ============================================================
# 异步 Session 依赖注入（FastAPI 风格）
# ============================================================


async def get_db() -> AsyncGenerator[AsyncSession]:
    """
    异步 Session 依赖注入

    **使用方式**:
    ```python
    @app.post("/products")
    async def create_product(db: AsyncSession = Depends(get_db)):
        ...
    ```
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# ============================================================
# 事务上下文管理器
# ============================================================


@asynccontextmanager
async def transaction_scope(session: AsyncSession):
    """
    事务上下文管理器

    **用途**:
    - 自动开启事务
    - 成功时提交
    - 失败时回滚

    **使用方式**:
    ```python
    async with transaction_scope(session):
        # 所有操作在同一事务中
        session.add(product)
        session.add(order)
    # 自动提交
    ```
    """
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise


# ============================================================
# 核心业务逻辑：库存扣减（乐观锁）
# ============================================================


async def deduct_stock_optimistic(
    session: AsyncSession,
    product_id: int,
    quantity: int,
) -> Product:
    """
    乐观锁库存扣减（防止超卖）

    **并发场景**:
    ```
    时刻 T1: 用户 A 读取库存 100，version=1
    时刻 T2: 用户 B 读取库存 100，version=1
    时刻 T3: 用户 A 扣减 10 → 库存 90，version=2 ✅
    时刻 T4: 用户 B 扣减 95 → version=1 != 2 ❌ 冲突检测
    ```

    **乐观锁优势**:
    - 无锁等待（高并发）
    - 冲突时重试
    - 适合读多写少场景

    Args:
        session: 异步 Session
        product_id: 产品 ID
        quantity: 扣减数量

    Returns:
        更新后的产品对象

    Raises:
        ValueError: 库存不足
        RuntimeError: 版本冲突（需重试）
    """
    with tracer.start_as_current_span("deduct_stock_optimistic") as span:
        span.set_attribute("product.id", product_id)
        span.set_attribute("quantity", quantity)

        # 步骤 1: 读取当前产品（获取版本号）
        stmt = select(Product).where(Product.id == product_id)
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            span.set_status(trace.Status(trace.StatusCode.ERROR, "产品不存在"))
            raise ValueError(f"产品 ID {product_id} 不存在")

        current_version = product.version
        span.set_attribute("product.version", current_version)
        span.set_attribute("product.stock", product.stock)

        # 步骤 2: 检查库存
        if product.stock < quantity:
            span.set_status(trace.Status(trace.StatusCode.ERROR, "库存不足"))
            raise ValueError(f"库存不足：需要 {quantity}，剩余 {product.stock}")

        # 步骤 3: 乐观锁更新（原子操作）
        update_stmt = (
            update(Product)
            .where(Product.id == product_id)
            .where(Product.version == current_version)  # 版本检查（关键）
            .values(
                stock=Product.stock - quantity,
                version=Product.version + 1,  # 版本递增
                updated_at=datetime.now(UTC),
            )
        )

        result = await session.execute(update_stmt)

        # 步骤 4: 检查更新行数
        if result.rowcount == 0:
            # 版本冲突（其他事务已修改）
            span.set_status(trace.Status(trace.StatusCode.ERROR, "版本冲突"))
            span.add_event(
                "version_conflict",
                {
                    "expected_version": current_version,
                },
            )
            raise RuntimeError(f"版本冲突：产品 {product_id} 已被其他事务修改，请重试")

        # 步骤 5: 刷新对象
        await session.refresh(product)

        span.add_event(
            "stock_deducted",
            {
                "new_stock": product.stock,
                "new_version": product.version,
            },
        )

        return product


# ============================================================
# 悲观锁对比实现
# ============================================================


async def deduct_stock_pessimistic(
    session: AsyncSession,
    product_id: int,
    quantity: int,
) -> Product:
    """
    悲观锁库存扣减（SELECT FOR UPDATE）

    **悲观锁机制**:
    - 读取时加锁
    - 其他事务等待
    - 适合写多读少场景

    **对比**:
    | 锁类型 | 等待 | 冲突 | 性能 | 适用场景 |
    |--------|------|------|------|----------|
    | 乐观锁 | ❌ 无 | ✅ 重试 | 高 | 读多写少 |
    | 悲观锁 | ✅ 阻塞 | ❌ 无 | 中 | 写多读少 |
    """
    with tracer.start_as_current_span("deduct_stock_pessimistic") as span:
        span.set_attribute("product.id", product_id)
        span.set_attribute("quantity", quantity)

        # SELECT FOR UPDATE（加排他锁）
        stmt = (
            select(Product).where(Product.id == product_id).with_for_update()  # 悲观锁
        )

        result = await session.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            raise ValueError(f"产品 ID {product_id} 不存在")

        # 检查库存
        if product.stock < quantity:
            raise ValueError(f"库存不足：需要 {quantity}，剩余 {product.stock}")

        # 直接更新（已加锁，无冲突风险）
        product.stock -= quantity
        product.updated_at = datetime.now(UTC)

        span.add_event("stock_deducted_with_lock")

        return product


# ============================================================
# 完整业务流程：创建订单（事务）
# ============================================================


async def create_order_with_transaction(
    session: AsyncSession,
    product_id: int,
    quantity: int,
) -> Order:
    """
    创建订单（完整事务流程）

    **事务边界**:
    1. 扣减库存（乐观锁）
    2. 创建订单记录
    3. 提交事务（原子性保证）

    **失败回滚**:
    - 库存不足 → 回滚
    - 版本冲突 → 回滚 + 重试
    - 任何异常 → 回滚
    """
    with tracer.start_as_current_span("create_order_with_transaction") as span:
        span.set_attribute("product.id", product_id)
        span.set_attribute("quantity", quantity)

        async with transaction_scope(session):
            # 步骤 1: 扣减库存（乐观锁）
            product = await deduct_stock_optimistic(session, product_id, quantity)

            # 步骤 2: 创建订单
            order = Order(
                product_id=product_id,
                quantity=quantity,
                total_price=product.price * quantity,
                status="pending",
            )
            session.add(order)

            # 步骤 3: 刷新获取 ID
            await session.flush()
            await session.refresh(order)

            span.set_attribute("order.id", order.id)
            span.set_attribute("order.total_price", order.total_price)
            span.add_event("order_created")

            return order


# ============================================================
# 慢查询示例（触发 OTel 追踪）
# ============================================================


async def slow_query_example(session: AsyncSession):
    """
    慢查询示例（触发 OpenTelemetry 追踪）

    **OTel 追踪内容**:
    - SQL 语句
    - 执行时间
    - 返回行数
    - 慢查询标记（> 100ms）
    """
    with tracer.start_as_current_span("slow_query_example") as span:
        # 模拟复杂查询
        stmt = select(Product).limit(1000)

        result = await session.execute(stmt)
        products = result.scalars().all()

        span.set_attribute("query.row_count", len(products))

        return products


# ============================================================
# 初始化数据库
# ============================================================


async def init_db():
    """创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 数据库表已创建")


async def seed_data():
    """插入测试数据"""
    async with AsyncSessionLocal() as session, transaction_scope(session):
        # 创建测试产品
        products = [
            Product(
                name="MacBook Pro M3",
                price=15999.0,
                stock=100,
                version=0,
            ),
            Product(
                name="iPhone 15 Pro",
                price=7999.0,
                stock=200,
                version=0,
            ),
        ]
        session.add_all(products)

    print("✅ 测试数据已插入")


# ============================================================
# 运行示例
# ============================================================


async def main():
    """主函数：演示完整流程"""
    print("=" * 80)
    print("SQLAlchemy 2.0 异步数据持久化 - 事务原子性与乐观锁")
    print("=" * 80 + "\n")

    # 初始化
    await init_db()
    await seed_data()

    async with AsyncSessionLocal() as session:
        # 示例 1: 创建订单（乐观锁 + 事务）
        print("\n示例 1: 创建订单（乐观锁 + 事务）")
        try:
            order = await create_order_with_transaction(session, product_id=1, quantity=5)
            print(f"✅ 订单创建成功: {order}")
        except Exception as e:
            print(f"❌ 订单创建失败: {e}")

        # 示例 2: 并发冲突模拟（需手动测试）
        print("\n示例 2: 乐观锁版本冲突检测")
        print("  提示：在两个终端同时运行此脚本，模拟并发冲突")

        # 示例 3: 慢查询追踪
        print("\n示例 3: 慢查询追踪（OpenTelemetry）")
        products = await slow_query_example(session)
        print(f"✅ 查询完成，返回 {len(products)} 条记录")

    print("\n" + "=" * 80)
    print("演示完成")
    print("=" * 80)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
