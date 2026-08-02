"""

from __future__ import annotations

练习 1: 基础 CRUD 操作 - Python 3.13 参考答案

本解决方案展示：
1. Python 3.13 PEP 695 泛型语法
2. asyncio.TaskGroup 并发数据库操作
3. match/case 模式匹配
4. Free-threading 线程安全设计

【解题思路】
1. 模型设计：
   - 使用 DeclarativeBase 作为基类
   - 使用 Mapped[type] 提供类型安全
   - 必需字段: Mapped[str]
   - 可选字段: Mapped[int | None]
   - 唯一约束: unique=True

2. 数据库配置：
   - create_async_engine() 创建异步引擎
   - async_sessionmaker() 创建会话工厂
   - expire_on_commit=False 避免对象过期

3. CRUD 实现模式（Python 3.13 增强）：
   - CREATE: session.add() + commit() + refresh()
   - READ: select() + execute() + scalar_one_or_none()
   - UPDATE: 查询对象 → 修改属性 → commit()
   - DELETE: session.delete() + commit()
   - LIST: select() + execute() + scalars().all()
   - BATCH: asyncio.TaskGroup 并发操作

4. 异步模式：
   - 所有函数使用 async def
   - 数据库操作使用 await
   - 会话管理使用 async with
   - 并发操作使用 asyncio.TaskGroup

【关键知识点】
- Mapped 类型注解（SQLAlchemy 2.0 新特性）
- PEP 695 泛型语法（Python 3.13）
- asyncio.TaskGroup 结构化并发（Python 3.13）
- match/case 模式匹配（Python 3.10+）
- Free-threading 线程安全设计（Python 3.14）

作者：Python 3.13 全栈课程
"""

import asyncio
from typing import Any

from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ============================================================================
# 1. 定义 Base 和 Book 模型
# ============================================================================


class Base(DeclarativeBase):
    """所有模型的基类"""


class Book(Base):
    """书籍模型"""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(50))
    isbn: Mapped[str] = mapped_column(String(13), unique=True)
    published_year: Mapped[int | None] = mapped_column(default=None)
    price: Mapped[float | None] = mapped_column(default=None)

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title!r}, author={self.author!r}, isbn={self.isbn!r}, year={self.published_year}, price={self.price})"


# ============================================================================
# 2. 配置数据库连接（Python 3.13 Free-threading 说明）
# ============================================================================

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 🔒 Free-threading 线程安全说明:
# - SQLAlchemy 异步引擎使用连接池管理连接
# - 每个 AsyncSession 在自己的 asyncio task 中运行
# - 连接池在 event loop 内是线程安全的
# - Python 3.14 环境下避免跨线程共享 session
engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# ============================================================================
# 3. 泛型仓储模式（Python 3.13 PEP 695 泛型）
# ============================================================================


class Repository[T]:
    """
    泛型仓储基类（Python 3.13 PEP 695 泛型语法）

    🚀 Python 3.13 PEP 695 特性:
    - 使用 class Repository[T]: 定义泛型类
    - 相比旧语法更简洁直观
    - 类型推断更准确

    泛型参数:
        T: 模型类型
    """

    def __init__(self, model_class: type[T]) -> None:
        self.model_class = model_class

    async def get_by_id(self, entity_id: int) -> T | None:
        """根据ID查询实体"""
        async with async_session() as session:
            stmt = select(self.model_class).where(self.model_class.id == entity_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def list_all(self) -> list[T]:
        """列出所有实体"""
        async with async_session() as session:
            stmt = select(self.model_class).order_by(self.model_class.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())


# ============================================================================
# 4. CRUD 函数实现（增强版）
# ============================================================================


async def create_tables() -> None:
    """创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_book(
    title: str,
    author: str,
    isbn: str,
    published_year: int | None = None,
    price: float | None = None,
) -> Book:
    """创建书籍"""
    async with async_session() as session:
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            published_year=published_year,
            price=price,
        )
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book


async def get_book_by_id(book_id: int) -> Book | None:
    """
    根据ID查询书籍（使用 match/case 处理结果）

    🎯 Python 3.10+ match/case 模式匹配
    """
    async with async_session() as session:
        stmt = select(Book).where(Book.id == book_id)
        result = await session.execute(stmt)
        book = result.scalar_one_or_none()

        # 使用 match/case 处理查询结果
        match book:
            case None:
                return None
            case Book():
                return book
            case _:
                return None


async def get_book_by_isbn(isbn: str) -> Book | None:
    """根据ISBN查询书籍"""
    async with async_session() as session:
        stmt = select(Book).where(Book.isbn == isbn)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def list_all_books() -> list[Book]:
    """列出所有书籍"""
    async with async_session() as session:
        stmt = select(Book).order_by(Book.id)
        result = await session.execute(stmt)
        return list(result.scalars().all())


async def update_book_price(book_id: int, new_price: float) -> Book | None:
    """更新书籍价格"""
    async with async_session() as session:
        stmt = select(Book).where(Book.id == book_id)
        result = await session.execute(stmt)
        book = result.scalar_one_or_none()

        if not book:
            return None

        book.price = new_price
        await session.commit()
        await session.refresh(book)
        return book


async def delete_book(book_id: int) -> bool:
    """删除书籍"""
    async with async_session() as session:
        stmt = select(Book).where(Book.id == book_id)
        result = await session.execute(stmt)
        book = result.scalar_one_or_none()

        if not book:
            return False

        await session.delete(book)
        await session.commit()
        return True


async def search_books_by_author(author: str) -> list[Book]:
    """根据作者搜索书籍"""
    async with async_session() as session:
        stmt = select(Book).where(Book.author == author).order_by(Book.title)
        result = await session.execute(stmt)
        return list(result.scalars().all())


# ============================================================================
# 5. 批量操作（使用 asyncio.TaskGroup）
# ============================================================================


async def create_books_batch(books_data: list[dict[str, Any]]) -> list[Book]:
    """
    批量创建书籍（使用 asyncio.TaskGroup 并发）

    🚀 Python 3.13 asyncio.TaskGroup:
    - 结构化并发，自动等待所有任务完成
    - 异常安全，任何任务失败会取消其他任务
    - 相比手动 gather，代码更清晰

    Args:
        books_data: 书籍数据列表

    Returns:
        创建的书籍列表
    """
    books: list[Book] = []

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(
                create_book(
                    title=data["title"],
                    author=data["author"],
                    isbn=data["isbn"],
                    published_year=data.get("published_year"),
                    price=data.get("price"),
                )
            )
            for data in books_data
        ]

    # 收集结果
    for task in tasks:
        books.append(task.result())

    return books


async def get_books_batch(book_ids: list[int]) -> list[Book | None]:
    """
    批量查询书籍（使用 asyncio.TaskGroup 并发）

    🚀 使用 TaskGroup 并发查询多个书籍

    Args:
        book_ids: 书籍ID列表

    Returns:
        书籍列表（可能包含 None）
    """
    books: list[Book | None] = []

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(get_book_by_id(book_id)) for book_id in book_ids]

    # 收集结果
    for task in tasks:
        books.append(task.result())

    return books


# ============================================================================
# 6. 测试代码
# ============================================================================


async def test_crud_operations() -> None:
    """测试所有 CRUD 操作"""
    print("=" * 70)
    print("测试书籍管理系统 - Python 3.13")
    print("=" * 70)
    print()

    # 1. 创建表
    print("1️⃣  创建表")
    await create_tables()
    print("✅ 表创建完成\n")

    # 2. 创建书籍
    print("2️⃣  创建书籍")
    book1 = await create_book(
        "Python编程",
        "Guido van Rossum",
        "9781234567890",
        2020,
        99.0,
    )
    print(f"✅ 创建: {book1}")

    book2 = await create_book(
        "深入理解计算机系统",
        "Randal E. Bryant",
        "9780136108047",
        2010,
        129.0,
    )
    print(f"✅ 创建: {book2}")

    book3 = await create_book(
        "算法导论",
        "Thomas H. Cormen",
        "9780262033848",
        2009,
        139.0,
    )
    print(f"✅ 创建: {book3}\n")

    # 3. 查询书籍
    print("3️⃣  查询书籍")
    book = await get_book_by_id(1)
    print(f"✅ 按ID查询: {book}")

    book = await get_book_by_isbn("9780136108047")
    print(f"✅ 按ISBN查询: {book}\n")

    # 4. 列出所有书籍
    print("4️⃣  列出所有书籍")
    books = await list_all_books()
    print(f"✅ 共 {len(books)} 本书:")
    for b in books:
        print(f"   {b}")
    print()

    # 5. 更新价格
    print("5️⃣  更新价格")
    updated = await update_book_price(1, 89.0)
    print(f"✅ 更新: {updated}\n")

    # 6. 搜索作者
    print("6️⃣  搜索作者")
    books = await search_books_by_author("Guido van Rossum")
    print(f"✅ 找到 {len(books)} 本书:")
    for b in books:
        print(f"   {b}")
    print()

    # 7. 测试 asyncio.TaskGroup 批量创建
    print("7️⃣  批量创建书籍（使用 TaskGroup）")
    batch_data = [
        {
            "title": "Effective Python",
            "author": "Brett Slatkin",
            "isbn": "9780134853987",
            "published_year": 2019,
            "price": 79.0,
        },
        {
            "title": "Fluent Python",
            "author": "Luciano Ramalho",
            "isbn": "9781491946008",
            "published_year": 2015,
            "price": 89.0,
        },
    ]
    batch_books = await create_books_batch(batch_data)
    print(f"✅ 批量创建了 {len(batch_books)} 本书")
    for b in batch_books:
        print(f"   {b}")
    print()

    # 8. 测试 asyncio.TaskGroup 批量查询
    print("8️⃣  批量查询书籍（使用 TaskGroup）")
    book_ids = [1, 2, 3, 4, 5]
    batch_books = await get_books_batch(book_ids)
    print(f"✅ 批量查询了 {len(batch_books)} 个ID:")
    for book_id, b in zip(book_ids, batch_books, strict=True):
        print(f"   ID {book_id}: {b if b else 'Not Found'}")
    print()

    # 9. 测试泛型仓储
    print("9️⃣  测试泛型仓储（PEP 695）")
    repo = Repository[Book](Book)
    book = await repo.get_by_id(1)
    print(f"✅ 仓储查询: {book}")

    all_books = await repo.list_all()
    print(f"✅ 仓储列表: {len(all_books)} 本书\n")

    # 10. 删除书籍
    print("🔟  删除书籍")
    success = await delete_book(3)
    print(f"✅ 删除结果: {success}")

    books = await list_all_books()
    print(f"✅ 剩余 {len(books)} 本书\n")

    print("=" * 70)
    print("测试完成！Python 3.13 特性已验证")
    print("=" * 70)


# ============================================================================
# 运行
# ============================================================================

if __name__ == "__main__":
    asyncio.run(test_crud_operations())
