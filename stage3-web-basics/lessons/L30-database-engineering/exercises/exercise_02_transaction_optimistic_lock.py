"""
L29 Exercise 2: 事务管理与乐观锁

【练习目标】
1. 理解事务的 ACID 特性
2. 实现事务上下文管理器
3. 掌握乐观锁的实现方式

【前置知识】
- L29 lesson.md 第二章：事务原子性
- L29 lesson.md 第三章：乐观锁 vs 悲观锁

【任务描述】
完成以下 TODO 部分，实现事务管理和乐观锁功能。

【验收标准】
- ✅ 事务上下文管理器正确实现
- ✅ 乐观锁版本控制正常工作
- ✅ 并发更新时正确处理冲突
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


# ============================================================================
# 1. 数据库配置
# ============================================================================

engine = create_async_engine(
    "sqlite+aiosqlite:///bank.db",
    echo=False,
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# ============================================================================
# 2. 定义模型
# ============================================================================


class Base(DeclarativeBase):
    """所有模型的基类"""


class Account(Base):
    """银行账户模型（带乐观锁版本号）"""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    balance: Mapped[float] = mapped_column(default=0.0)
    version: Mapped[int] = mapped_column(default=1)  # 乐观锁版本号


# ============================================================================
# 3. 事务上下文管理器
# ============================================================================


# TODO 1: 实现事务上下文管理器
@asynccontextmanager
async def transaction_scope(session: AsyncSession) -> AsyncGenerator[AsyncSession]:
    """事务上下文管理器

    提示:
    - 使用 @asynccontextmanager 装饰器
    - try 块中 yield session
    - except 块中 rollback
    - finally 块中 close
    """


# ============================================================================
# 4. 基础操作
# ============================================================================


async def create_account(name: str, initial_balance: float = 0.0) -> Account:
    """创建账户"""
    async with async_session() as session:
        async with transaction_scope(session):
            account = Account(name=name, balance=initial_balance, version=1)
            session.add(account)
            await session.commit()
            await session.refresh(account)
            return account


async def get_account(account_id: int) -> Account | None:
    """获取账户"""
    async with async_session() as session:
        result = await session.execute(select(Account).where(Account.id == account_id))
        return result.scalar_one_or_none()


# ============================================================================
# 5. 乐观锁转账（核心练习）
# ============================================================================


async def transfer_with_optimistic_lock(
    from_account_id: int,
    to_account_id: int,
    amount: float,
) -> bool:
    """使用乐观锁进行转账

    乐观锁原理：
    1. 读取账户时记录当前 version
    2. 更新时 WHERE 条件包含 version
    3. 如果 version 不匹配，说明有其他事务在修改，返回失败

    提示:
    - 使用 UPDATE ... WHERE version = :expected_version
    - 检查 affected_rows == 1
    - 如果失败，返回 False
    """


# ============================================================================
# 测试代码
# ============================================================================

import asyncio


async def setup_db():
    """初始化数据库"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # 创建两个账户
    async with async_session() as session:
        async with transaction_scope(session):
            acc1 = Account(name="Alice", balance=1000.0, version=1)
            acc2 = Account(name="Bob", balance=500.0, version=1)
            session.add(acc1)
            session.add(acc2)
            await session.commit()


async def main():
    """测试事务和乐观锁"""
    await setup_db()
    print("✅ 数据库初始化成功")

    # 测试转账
    success = await transfer_with_optimistic_lock(1, 2, 100.0)
    print(f"✅ 转账 {'成功' if success else '失败'}")

    # 验证余额
    alice = await get_account(1)
    bob = await get_account(2)
    print(f"✅ Alice 余额: {alice.balance if alice else 'N/A'}")
    print(f"✅ Bob 余额: {bob.balance if bob else 'N/A'}")

    # 测试并发冲突（模拟）
    print("\n🔄 测试乐观锁冲突...")
    # TODO: 实现并发测试，验证乐观锁正确处理冲突

    await engine.dispose()
    print("\n🎉 测试完成!")


if __name__ == "__main__":
    asyncio.run(main())
