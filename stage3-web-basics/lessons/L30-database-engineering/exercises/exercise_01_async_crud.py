"""
L29 Exercise 1: 异步 CRUD 操作

【练习目标】
1. 掌握 SQLAlchemy 2.0 异步 ORM 的基础用法
2. 实现异步的 CREATE、READ、UPDATE、DELETE 操作
3. 使用 asyncio.TaskGroup 实现并发数据库操作

【前置知识】
- L29 lesson.md 第一章：数据库技术债
- L19 异步编程基础

【任务描述】
完成以下 TODO 部分，实现一个异步的书籍管理模块。

【验收标准】
- ✅ async_sessionmaker 正确配置
- ✅ 所有 CRUD 操作使用 async/await
- ✅ 并发创建使用 asyncio.TaskGroup
- ✅ 错误处理完善
"""

from __future__ import annotations

# TODO 1: 导入必要的 SQLAlchemy 模块
# 提示: 需要 create_async_engine, async_sessionmaker, AsyncSession


# TODO 2: 定义 Base 类（使用 DeclarativeBase）


# TODO 3: 定义 Book 模型
# 字段: id, title, author, isbn (唯一), published_year, price


# TODO 4: 创建异步引擎和会话工厂
# 提示: 使用 SQLite + aiosqlite，数据库文件: books.db


# TODO 5: 实现 create_book 函数
async def create_book(title: str, author: str, isbn: str) -> Book | None:
    """创建一本书籍"""


# TODO 6: 实现 get_book_by_isbn 函数
async def get_book_by_isbn(isbn: str) -> Book | None:
    """根据 ISBN 查询书籍"""


# TODO 7: 实现 update_book_price 函数
async def update_book_price(isbn: str, new_price: float) -> bool:
    """更新书籍价格"""


# TODO 8: 实现 delete_book 函数
async def delete_book(isbn: str) -> bool:
    """删除书籍"""


# TODO 9: 实现 batch_create_books 函数（使用 TaskGroup）
async def batch_create_books(books_data: list[dict]) -> list[Book]:
    """批量创建书籍，使用 asyncio.TaskGroup 并发执行"""


# ============================================================================
# 测试代码（不要修改）
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
