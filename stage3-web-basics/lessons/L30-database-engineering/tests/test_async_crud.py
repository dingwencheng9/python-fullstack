"""L29 Exercise 1: 异步 CRUD 操作 - 测试套件。

测试异步 CRUD 操作：create_book, get_book_by_isbn, update_book_price,
delete_book, batch_create_books。
"""

from __future__ import annotations

import uuid

import pytest_asyncio


def _make_engine(db_url: str):
    """创建异步引擎。"""
    from sqlalchemy.ext.asyncio import create_async_engine

    return create_async_engine(db_url, echo=False)


def _make_session(engine, session_cls):
    """创建会话工厂。"""
    from sqlalchemy.ext.asyncio import async_sessionmaker

    return async_sessionmaker(engine, class_=session_cls, expire_on_commit=False)


class TestAsyncCRUD:
    """异步 CRUD 测试套件。"""

    @pytest_asyncio.fixture
    async def crud_module(self, solutions) -> object:
        """加载 CRUD 模块（每次测试重新创建引擎）。"""
        import importlib

        # 动态重新加载模块
        crud = solutions.solution_01_async_crud
        importlib.reload(crud)

        # 为这个测试创建独立的内存数据库
        db_url = "sqlite+aiosqlite:///:memory:"
        engine = _make_engine(db_url)
        session_factory = _make_session(engine, crud.AsyncSession)

        # 替换模块级全局变量
        crud.engine = engine
        crud.async_session = session_factory

        # 初始化表
        async with engine.begin() as conn:
            await conn.run_sync(crud.Base.metadata.create_all)

        yield crud

        # 清理
        await engine.dispose()

    @pytest_asyncio.fixture
    async def book_data(self) -> dict:
        """提供测试书籍数据。"""
        return {
            "title": "Python 3.13",
            "author": "张三",
            "isbn": f"978-7-111-{uuid.uuid4().hex[:4].upper()}",
        }

    async def test_create_book(self, crud_module, book_data: dict) -> None:
        """测试创建书籍。"""
        book = await crud_module.create_book(
            title=book_data["title"],
            author=book_data["author"],
            isbn=book_data["isbn"],
        )
        assert book is not None
        assert book.title == book_data["title"]
        assert book.author == book_data["author"]
        assert book.isbn == book_data["isbn"]

    async def test_get_book_by_isbn(self, crud_module, book_data: dict) -> None:
        """测试通过 ISBN 查询书籍。"""
        await crud_module.create_book(
            title=book_data["title"],
            author=book_data["author"],
            isbn=book_data["isbn"],
        )
        found = await crud_module.get_book_by_isbn(book_data["isbn"])
        assert found is not None
        assert found.title == book_data["title"]

    async def test_get_book_not_found(self, crud_module) -> None:
        """测试查询不存在的 ISBN。"""
        found = await crud_module.get_book_by_isbn("NONEXISTENT-ISBN")
        assert found is None

    async def test_update_book_price(self, crud_module, book_data: dict) -> None:
        """测试更新书籍价格。"""
        await crud_module.create_book(
            title=book_data["title"],
            author=book_data["author"],
            isbn=book_data["isbn"],
        )
        result = await crud_module.update_book_price(book_data["isbn"], 99.99)
        assert result is True
        book = await crud_module.get_book_by_isbn(book_data["isbn"])
        assert book is not None
        assert book.price == 99.99

    async def test_update_nonexistent_book(self, crud_module) -> None:
        """测试更新不存在的书籍。"""
        result = await crud_module.update_book_price("NONEXISTENT-ISBN", 50.0)
        assert result is False

    async def test_delete_book(self, crud_module, book_data: dict) -> None:
        """测试删除书籍。"""
        await crud_module.create_book(
            title=book_data["title"],
            author=book_data["author"],
            isbn=book_data["isbn"],
        )
        result = await crud_module.delete_book(book_data["isbn"])
        assert result is True
        found = await crud_module.get_book_by_isbn(book_data["isbn"])
        assert found is None

    async def test_delete_nonexistent_book(self, crud_module) -> None:
        """测试删除不存在的书籍。"""
        result = await crud_module.delete_book("NONEXISTENT-ISBN")
        assert result is False

    async def test_batch_create_books(self, crud_module) -> None:
        """测试批量创建书籍。"""
        books_data = [
            {
                "title": "Book 1",
                "author": "Author 1",
                "isbn": f"ISBN-BATCH-1-{uuid.uuid4().hex[:4]}",
            },
            {
                "title": "Book 2",
                "author": "Author 2",
                "isbn": f"ISBN-BATCH-2-{uuid.uuid4().hex[:4]}",
            },
            {
                "title": "Book 3",
                "author": "Author 3",
                "isbn": f"ISBN-BATCH-3-{uuid.uuid4().hex[:4]}",
            },
        ]
        books = await crud_module.batch_create_books(books_data)
        assert len(books) == 3
        for book, data in zip(books, books_data, strict=True):
            assert book.title == data["title"]
            assert book.author == data["author"]
