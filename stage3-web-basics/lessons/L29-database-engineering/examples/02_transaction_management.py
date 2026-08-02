"""

from __future__ import annotations

L10 示例 2: 异步事务管理

展示 SQLAlchemy 2.0 异步事务的核心概念：
1. 基础事务管理
2. 事务回滚
3. 嵌套事务（SAVEPOINT）
4. 并发事务处理
5. 事务隔离级别
"""

import asyncio

from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ============================================================================
# 1. 定义模型
# ============================================================================


class Base(DeclarativeBase):
    """基类"""


class Account(Base):
    """账户模型（用于演示事务）"""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    balance: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self) -> str:
        return f"Account(id={self.id}, name={self.name!r}, balance={self.balance:.2f})"


class TransactionLog(Base):
    """交易日志模型"""

    __tablename__ = "transaction_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_account: Mapped[str] = mapped_column(String(50))
    to_account: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float]
    status: Mapped[str] = mapped_column(String(20))  # success, failed, pending

    def __repr__(self) -> str:
        return f"TransactionLog(id={self.id}, from={self.from_account!r}, to={self.to_account!r}, amount={self.amount:.2f}, status={self.status!r})"


# ============================================================================
# 2. 配置数据库
# ============================================================================

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# ============================================================================
# 3. 基础函数
# ============================================================================


async def create_tables() -> None:
    """创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_account(name: str, initial_balance: float = 0.0) -> Account:
    """创建账户"""
    async with async_session() as session:
        account = Account(name=name, balance=initial_balance)
        session.add(account)
        await session.commit()
        await session.refresh(account)
        return account


async def get_account(name: str) -> Account | None:
    """获取账户"""
    async with async_session() as session:
        stmt = select(Account).where(Account.name == name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


# ============================================================================
# 4. 事务管理示例
# ============================================================================


async def transfer_money_basic(
    from_account: str,
    to_account: str,
    amount: float,
) -> bool:
    """
    基础转账（演示事务的原子性）

    事务确保：要么全部成功，要么全部回滚。
    """
    print(f"\n{'=' * 70}")
    print(f"基础转账: {from_account} -> {to_account}, 金额: {amount}")
    print("=" * 70)

    async with async_session() as session, session.begin():  # 自动管理事务
        # 1. 查询账户
        stmt = select(Account).where(Account.name == from_account)
        result = await session.execute(stmt)
        from_acc = result.scalar_one_or_none()

        stmt = select(Account).where(Account.name == to_account)
        result = await session.execute(stmt)
        to_acc = result.scalar_one_or_none()

        if not from_acc or not to_acc:
            print("❌ 账户不存在")
            return False

        if from_acc.balance < amount:
            print(f"❌ 余额不足: {from_acc.balance:.2f} < {amount:.2f}")
            return False

        # 2. 执行转账
        from_acc.balance -= amount
        to_acc.balance += amount

        print("✅ 转账成功")
        print(f"   {from_account}: {from_acc.balance:.2f}")
        print(f"   {to_account}: {to_acc.balance:.2f}")

        # 3. 自动提交（离开 async with 块时）
        return True


async def transfer_money_with_rollback(
    from_account: str,
    to_account: str,
    amount: float,
    should_fail: bool = False,
) -> bool:
    """
    带回滚的转账（演示异常处理）

    如果发生异常，事务自动回滚。
    """
    print(f"\n{'=' * 70}")
    print(f"带回滚转账: {from_account} -> {to_account}, 金额: {amount}")
    if should_fail:
        print("⚠️  将触发失败")
    print("=" * 70)

    try:
        async with async_session() as session, session.begin():
            # 查询账户
            stmt = select(Account).where(Account.name == from_account)
            result = await session.execute(stmt)
            from_acc = result.scalar_one_or_none()

            stmt = select(Account).where(Account.name == to_account)
            result = await session.execute(stmt)
            to_acc = result.scalar_one_or_none()

            if not from_acc or not to_acc:
                raise ValueError("账户不存在")

            if from_acc.balance < amount:
                raise ValueError(f"余额不足: {from_acc.balance:.2f} < {amount:.2f}")

            # 执行转账
            from_acc.balance -= amount
            to_acc.balance += amount

            # 模拟失败
            if should_fail:
                raise Exception("模拟的转账失败")  # noqa: TRY002

            print("✅ 转账成功")
            print(f"   {from_account}: {from_acc.balance:.2f}")
            print(f"   {to_account}: {to_acc.balance:.2f}")
            return True

    except Exception as e:
        print(f"❌ 转账失败: {e}")
        print("🔄 事务已自动回滚")
        return False


async def transfer_with_log(
    from_account: str,
    to_account: str,
    amount: float,
) -> bool:
    """
    带日志的转账（演示多表事务）

    在一个事务中操作多个表。
    """
    print(f"\n{'=' * 70}")
    print(f"带日志转账: {from_account} -> {to_account}, 金额: {amount}")
    print("=" * 70)

    async with async_session() as session, session.begin():
        try:
            # 1. 查询账户
            stmt = select(Account).where(Account.name == from_account)
            result = await session.execute(stmt)
            from_acc = result.scalar_one_or_none()

            stmt = select(Account).where(Account.name == to_account)
            result = await session.execute(stmt)
            to_acc = result.scalar_one_or_none()

            if not from_acc or not to_acc:
                raise ValueError("账户不存在")

            if from_acc.balance < amount:
                raise ValueError("余额不足")

            # 2. 执行转账
            from_acc.balance -= amount
            to_acc.balance += amount

            # 3. 记录日志
            log = TransactionLog(
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                status="success",
            )
            session.add(log)

            print("✅ 转账成功")
            print(f"   {from_account}: {from_acc.balance:.2f}")
            print(f"   {to_account}: {to_acc.balance:.2f}")
            print(f"   日志: {log}")

            return True

        except Exception as e:
            # 记录失败日志
            log = TransactionLog(
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                status="failed",
            )
            session.add(log)

            print(f"❌ 转账失败: {e}")
            print(f"   日志: {log}")
            return False


async def transfer_with_savepoint(
    transfers: list[tuple[str, str, float]],
) -> list[bool]:
    """
    使用 SAVEPOINT 的批量转账

    SAVEPOINT 允许部分回滚，而不是回滚整个事务。
    """
    print(f"\n{'=' * 70}")
    print(f"批量转账（使用 SAVEPOINT）: {len(transfers)} 笔")
    print("=" * 70)

    results = []

    async with async_session() as session, session.begin():
        for i, (from_acc, to_acc, amount) in enumerate(transfers, 1):
            print(f"\n转账 {i}: {from_acc} -> {to_acc}, {amount}")

            # 创建 SAVEPOINT
            async with session.begin_nested():
                try:
                    # 查询账户
                    stmt = select(Account).where(Account.name == from_acc)
                    result = await session.execute(stmt)
                    from_account = result.scalar_one_or_none()

                    stmt = select(Account).where(Account.name == to_acc)
                    result = await session.execute(stmt)
                    to_account = result.scalar_one_or_none()

                    if not from_account or not to_account:
                        raise ValueError("账户不存在")

                    if from_account.balance < amount:
                        raise ValueError("余额不足")

                    # 执行转账
                    from_account.balance -= amount
                    to_account.balance += amount

                    print("   ✅ 成功")
                    results.append(True)

                except Exception as e:
                    print(f"   ❌ 失败: {e}")
                    print("   🔄 回滚到 SAVEPOINT（其他转账不受影响）")
                    results.append(False)
                    # SAVEPOINT 自动回滚，但不影响外层事务

        # 所有转账处理完后，提交外层事务
        print(f"\n总结: {sum(results)}/{len(results)} 笔成功")

    return results


# ============================================================================
# 5. 演示主函数
# ============================================================================


async def main() -> None:
    """运行所有演示"""
    print("=" * 70)
    print("SQLAlchemy 异步事务管理演示")
    print("=" * 70)

    # 创建表
    await create_tables()
    print("\n✅ 表创建完成\n")

    # 创建测试账户
    print("创建测试账户...")
    await create_account("Alice", 1000.0)
    await create_account("Bob", 500.0)
    await create_account("Charlie", 300.0)
    print()

    # 示例 1: 基础转账
    await transfer_money_basic("Alice", "Bob", 100.0)

    # 示例 2: 成功转账
    await transfer_money_with_rollback("Bob", "Charlie", 50.0)

    # 示例 3: 失败转账（余额不足）
    await transfer_money_with_rollback("Charlie", "Alice", 1000.0)

    # 示例 4: 失败转账（模拟异常）
    await transfer_money_with_rollback("Alice", "Bob", 50.0, should_fail=True)

    # 示例 5: 带日志的转账
    await transfer_with_log("Alice", "Charlie", 200.0)

    # 示例 6: 使用 SAVEPOINT 的批量转账
    transfers = [
        ("Alice", "Bob", 100.0),  # 成功
        ("Bob", "Charlie", 50.0),  # 成功
        ("Charlie", "Alice", 1000.0),  # 失败（余额不足）
        ("Bob", "Alice", 100.0),  # 成功
    ]
    await transfer_with_savepoint(transfers)

    # 查看最终余额
    print(f"\n{'=' * 70}")
    print("最终余额:")
    print("=" * 70)
    for name in ["Alice", "Bob", "Charlie"]:
        account = await get_account(name)
        if account:
            print(f"  {account}")

    print("\n演示完成！")


# ============================================================================
# 运行
# ============================================================================

if __name__ == "__main__":
    asyncio.run(main())
