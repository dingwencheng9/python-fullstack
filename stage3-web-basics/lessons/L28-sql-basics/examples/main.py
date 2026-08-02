"""L28 SQL 基础示例代码。

运行方式：
    uv run python stage3-web-basics/lessons/L28-sql-basics/examples/main.py
"""

from __future__ import annotations

import sqlite3


def main() -> None:
    """演示建表、插入、查询、JOIN 与 GROUP BY。"""
    with sqlite3.connect(":memory:") as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE
            );

            CREATE TABLE posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                title TEXT NOT NULL,
                published INTEGER NOT NULL DEFAULT 0,
                published_at TEXT
            );
            """
        )
        conn.executemany(
            "INSERT INTO users(username, email) VALUES (?, ?)",
            [
                ("alice", "alice@example.com"),
                ("bob", "bob@example.com"),
            ],
        )
        conn.executemany(
            "INSERT INTO posts(user_id, title, published, published_at) VALUES (?, ?, ?, ?)",
            [
                (1, "HTTP 入门", 1, "2026-01-02T09:00:00"),
                (1, "SQL 基础", 1, "2026-01-03T10:00:00"),
                (2, "草稿", 0, None),
            ],
        )

        print("已发布文章：")
        for row in conn.execute(
            """
            SELECT p.title, u.username AS author, p.published_at
            FROM posts p
            JOIN users u ON u.id = p.user_id
            WHERE p.published = 1
            ORDER BY p.published_at DESC;
            """
        ):
            print(dict(row))

        print("\n用户文章数：")
        for row in conn.execute(
            """
            SELECT u.username, COUNT(p.id) AS post_count
            FROM users u
            LEFT JOIN posts p ON p.user_id = u.id
            GROUP BY u.id, u.username
            ORDER BY post_count DESC;
            """
        ):
            print(dict(row))


if __name__ == "__main__":
    main()
