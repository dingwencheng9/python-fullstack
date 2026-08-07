"""
L29 Exercise 1: 异步 CRUD 操作 - 参考答案
"""

from __future__ import annotations

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


# ============================================================================
# 2. 创建异步引擎和会话工厂
# ============================================================================


engine = create_async_engine(
    "sqlite+aiosqlite:///books.db",
    echo=False,
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# ============================================================================
# 3. CRUD 实现
# ============================================================================


async def create_book(title: str, author: str, isbn: str) -> Book | None:
    """创建一本书籍"""
    async with async_session() as session:
        book = Book(title=title, author=author, isbn=isbn)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book


async def get_book_by_isbn(isbn: str) -> Book | None:
    """根据 ISBN 查询书籍"""
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.isbn == isbn))
        return result.scalar_one_or_none()


async def update_book_price(isbn: str, new_price: float) -> bool:
    """更新书籍价格"""
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.isbn == isbn))
        book = result.scalar_one_or_none()
        if book is None:
            return False
        book.price = new_price
        await session.commit()
        return True


async def delete_book(isbn: str) -> bool:
    """删除书籍"""
    async with async_session() as session:
        result = await session.execute(select(Book).where(Book.isbn == isbn))
        book = result.scalar_one_or_none()
        if book is None:
            return False
        await session.delete(book)
        await session.commit()
        return True


async def batch_create_books(books_data: list[dict]) -> list[Book]:
    """批量创建书籍，使用 asyncio.TaskGroup 并发执行"""
    import asyncio

    async def _create(book_data: dict) -> Book:
        return await create_book(
            title=book_data["title"],
            author=book_data["author"],
            isbn=book_data["isbn"],
        )

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(_create(data)) for data in books_data]

    return [task.result() for task in tasks]


# ============================================================================
# 测试代码
# ============================================================================

import asyncio


async def main():
    """测试所有实现"""
    # 创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("✅ 表创建成功")

    # 测试 create_book
    book = await create_book("Python 3.13", "张三", "978-7-111-00001-1")
    print(f"✅ 创建书籍: {book.title}")

    # 测试 get_book_by_isbn
    found = await get_book_by_isbn("978-7-111-00001-1")
    print(f"✅ 查询书籍: {found.title if found else '未找到'}")

    # 测试 update_book_price
    updated = await update_book_price("978-7-111-00001-1", 99.99)
    print(f"✅ 更新价格: {'成功' if updated else '失败'}")

    # 测试 batch_create_books
    books = await batch_create_books(
        [
            {"title": "Book 1", "author": "Author 1", "isbn": "978-7-111-00002-1"},
            {"title": "Book 2", "author": "Author 2", "isbn": "978-7-111-00003-1"},
            {"title": "Book 3", "author": "Author 3", "isbn": "978-7-111-00004-1"},
        ]
    )
    print(f"✅ 批量创建: {len(books)} 本书")

    # 测试 delete_book
    deleted = await delete_book("978-7-111-00001-1")
    print(f"✅ 删除书籍: {'成功' if deleted else '失败'}")

    # 清理
    await engine.dispose()
    print("\n🎉 所有测试通过!")


if __name__ == "__main__":
    asyncio.run(main())
