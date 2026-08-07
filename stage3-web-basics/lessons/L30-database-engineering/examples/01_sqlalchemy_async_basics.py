"""

from __future__ import annotations

L10 示例 1: SQLAlchemy 2.0 异步基础

展示 SQLAlchemy 2.0 异步模式的核心功能：
1. 异步引擎和会话配置
2. ORM 模型定义（使用 Mapped 类型）
3. 基础 CRUD 操作
4. 异步查询构建
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
# 1. 定义 Base 类
# ============================================================================


class Base(DeclarativeBase):
    """所有模型的基类"""


# ============================================================================
# 2. 定义 User 模型
# ============================================================================


class User(Base):
    """
    用户模型

    使用 Mapped 类型注解，提供类型安全和编辑器提示。
    """

    __tablename__ = "users"

    # 主键
    id: Mapped[int] = mapped_column(primary_key=True)

    # 必需字段
    name: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100))

    # 可选字段（使用 Optional）
    age: Mapped[int | None] = mapped_column(default=None)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r}, age={self.age})"


# ============================================================================
# 3. 创建异步引擎和会话
# ============================================================================

# 使用 SQLite 内存数据库（方便演示）
# 生产环境使用: postgresql+asyncpg://user:pass@localhost/db
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 打印 SQL 语句（调试用）
)

# 创建异步会话工厂
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,  # 提交后不过期对象
    class_=AsyncSession,
)


# ============================================================================
# 4. CRUD 操作函数
# ============================================================================


async def create_tables() -> None:
    """创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 表创建完成\n")


async def create_user(name: str, email: str, age: int | None = None) -> User:
    """
    创建用户

    使用 async with 自动管理会话。
    """
    async with async_session() as session:
        user = User(name=name, email=email, age=age)
        session.add(user)
        await session.commit()
        await session.refresh(user)  # 刷新以获取数据库生成的 ID
        print(f"✅ 创建用户: {user}")
        return user


async def get_user_by_id(user_id: int) -> User | None:
    """
    根据 ID 查询用户

    使用 select() 构建查询。
    """
    async with async_session() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            print(f"✅ 查询用户: {user}")
        else:
            print(f"❌ 用户 ID {user_id} 不存在")

        return user


async def get_user_by_name(name: str) -> User | None:
    """根据名称查询用户"""
    async with async_session() as session:
        stmt = select(User).where(User.name == name)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            print(f"✅ 查询用户: {user}")
        else:
            print(f"❌ 用户 '{name}' 不存在")

        return user


async def list_all_users() -> list[User]:
    """
    列出所有用户

    使用 scalars() 获取对象列表。
    """
    async with async_session() as session:
        stmt = select(User).order_by(User.id)
        result = await session.execute(stmt)
        users = list(result.scalars().all())

        print(f"✅ 共 {len(users)} 个用户:")
        for user in users:
            print(f"   {user}")

        return users


async def update_user_age(user_id: int, new_age: int) -> User | None:
    """
    更新用户年龄

    先查询，修改属性，然后提交。
    """
    async with async_session() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            print(f"❌ 用户 ID {user_id} 不存在")
            return None

        user.age = new_age
        await session.commit()
        await session.refresh(user)

        print(f"✅ 更新用户: {user}")
        return user


async def delete_user(user_id: int) -> bool:
    """
    删除用户

    返回是否成功删除。
    """
    async with async_session() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            print(f"❌ 用户 ID {user_id} 不存在")
            return False

        await session.delete(user)
        await session.commit()

        print(f"✅ 删除用户: {user}")
        return True


# ============================================================================
# 5. 高级查询示例
# ============================================================================


async def filter_users_by_age(min_age: int) -> list[User]:
    """查询年龄大于等于指定值的用户"""
    async with async_session() as session:
        stmt = select(User).where(User.age >= min_age).order_by(User.age)
        result = await session.execute(stmt)
        users = list(result.scalars().all())

        print(f"✅ 年龄 >= {min_age} 的用户 ({len(users)} 个):")
        for user in users:
            print(f"   {user}")

        return users


async def count_users() -> int:
    """统计用户数量"""
    from sqlalchemy import func

    async with async_session() as session:
        stmt = select(func.count()).select_from(User)
        result = await session.execute(stmt)
        count = result.scalar()

        print(f"✅ 用户总数: {count}")
        return count or 0


# ============================================================================
# 6. 演示主函数
# ============================================================================


async def main() -> None:
    """运行所有演示"""
    print("=" * 70)
    print("SQLAlchemy 2.0 异步模式演示")
    print("=" * 70)
    print()

    # 创建表
    await create_tables()

    # CREATE - 创建用户
    print("1️⃣  创建用户")
    print("-" * 70)
    await create_user("Alice", "alice@example.com", 30)
    await create_user("Bob", "bob@example.com", 25)
    await create_user("Charlie", "charlie@example.com", 35)
    print()

    # READ - 查询用户
    print("2️⃣  查询用户")
    print("-" * 70)
    await get_user_by_id(1)
    await get_user_by_name("Bob")
    await get_user_by_id(999)  # 不存在
    print()

    # LIST - 列出所有用户
    print("3️⃣  列出所有用户")
    print("-" * 70)
    await list_all_users()
    print()

    # UPDATE - 更新用户
    print("4️⃣  更新用户")
    print("-" * 70)
    await update_user_age(2, 26)
    print()

    # FILTER - 高级查询
    print("5️⃣  高级查询")
    print("-" * 70)
    await filter_users_by_age(30)
    await count_users()
    print()

    # DELETE - 删除用户
    print("6️⃣  删除用户")
    print("-" * 70)
    await delete_user(3)
    await list_all_users()
    print()

    print("=" * 70)
    print("演示完成！")
    print("=" * 70)


# ============================================================================
# 运行
# ============================================================================

if __name__ == "__main__":
    asyncio.run(main())
