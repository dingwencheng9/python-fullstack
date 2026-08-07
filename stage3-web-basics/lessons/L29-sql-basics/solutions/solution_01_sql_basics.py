"""L28 SQL 基础练习参考答案。

使用 Python 标准库 sqlite3 构建可离线运行的关系数据库练习，覆盖：
- DDL 建表与约束
- INSERT/SELECT/WHERE/ORDER BY
- JOIN 与 GROUP BY
- 参数化查询
"""

from __future__ import annotations

import sqlite3
from typing import Any


def create_blog_db() -> sqlite3.Connection:
    """创建博客样例数据库并写入初始数据。"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL DEFAULT '2026-01-01T00:00:00'
        );

        CREATE TABLE posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            published INTEGER NOT NULL DEFAULT 0,
            published_at TEXT
        );
        """
    )
    conn.executemany(
        "INSERT INTO users(id, username, email) VALUES (?, ?, ?)",
        [
            (1, "alice", "alice@example.com"),
            (2, "bob", "bob@example.com"),
            (3, "carol", "carol@example.com"),
        ],
    )
    conn.executemany(
        """
        INSERT INTO posts(id, user_id, title, content, published, published_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (1, 1, "HTTP 入门", "理解请求与响应", 1, "2026-01-02T09:00:00"),
            (2, 1, "SQL 基础", "SELECT 与 JOIN", 1, "2026-01-03T10:00:00"),
            (3, 2, "FastAPI 路由", "路径参数与依赖注入", 1, "2026-01-04T11:00:00"),
            (4, 3, "未发布草稿", "草稿内容", 0, None),
        ],
    )
    return conn


def list_published_posts(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """按发布时间倒序列出已发布文章及作者。"""
    rows = conn.execute(
        """
        SELECT p.id, p.title, u.username AS author, p.published_at
        FROM posts p
        JOIN users u ON u.id = p.user_id
        WHERE p.published = 1
        ORDER BY p.published_at DESC, p.id DESC;
        """
    ).fetchall()
    return [dict(row) for row in rows]


def count_posts_by_user(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """统计每个用户的文章数，包含 0 篇文章的用户。"""
    rows = conn.execute(
        """
        SELECT u.username, COUNT(p.id) AS post_count
        FROM users u
        LEFT JOIN posts p ON p.user_id = u.id
        GROUP BY u.id, u.username
        ORDER BY post_count DESC, u.username ASC;
        """
    ).fetchall()
    return [dict(row) for row in rows]


def search_posts(conn: sqlite3.Connection, keyword: str) -> list[dict[str, Any]]:
    """使用参数化查询按标题关键字搜索已发布文章。"""
    rows = conn.execute(
        """
        SELECT p.id, p.title, u.username AS author
        FROM posts p
        JOIN users u ON u.id = p.user_id
        WHERE p.published = 1 AND p.title LIKE ?
        ORDER BY p.id;
        """,
        (f"%{keyword}%",),
    ).fetchall()
    return [dict(row) for row in rows]


def create_user(conn: sqlite3.Connection, username: str, email: str) -> int:
    """创建用户并返回新用户 id。"""
    cursor = conn.execute(
        "INSERT INTO users(username, email) VALUES (?, ?)",
        (username, email),
    )
    return int(cursor.lastrowid)


def create_post(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    title: str,
    content: str,
    published: bool = False,
    published_at: str | None = None,
) -> int:
    """创建文章并返回新文章 id。"""
    cursor = conn.execute(
        """
        INSERT INTO posts(user_id, title, content, published, published_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, title, content, int(published), published_at),
    )
    return int(cursor.lastrowid)
