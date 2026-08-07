"""L30 SQL 进阶示例 3：索引与 EXPLAIN QUERY PLAN。

运行方式：
    uv run python stage3-web-basics/lessons/L30-sql-advanced/examples/03_query_plan_indexes.py
"""

from __future__ import annotations

import sqlite3
from typing import Any


def create_event_db(row_count: int = 200) -> sqlite3.Connection:
    """创建事件表并写入可观察查询计划的数据量。"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE events (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            created_at TEXT NOT NULL,
            payload TEXT NOT NULL
        );
        """
    )
    rows = [
        (
            index % 20,
            "purchase" if index % 7 == 0 else "page_view",
            f"2026-01-{(index % 28) + 1:02d}",
            f"payload-{index}",
        )
        for index in range(row_count)
    ]
    conn.executemany(
        "INSERT INTO events(user_id, event_type, created_at, payload) VALUES (?, ?, ?, ?)",
        rows,
    )
    return conn


def explain_user_event_query(conn: sqlite3.Connection, user_id: int, event_type: str) -> list[str]:
    """返回查询计划描述，用于观察是否使用索引。"""
    rows = conn.execute(
        """
        EXPLAIN QUERY PLAN
        SELECT id, created_at, payload
        FROM events
        WHERE user_id = ? AND event_type = ?
        ORDER BY created_at DESC;
        """,
        (user_id, event_type),
    ).fetchall()
    return [row["detail"] for row in rows]


def create_covering_index(conn: sqlite3.Connection) -> None:
    """创建覆盖 WHERE 与 ORDER BY 的复合索引。"""
    conn.execute(
        """
        CREATE INDEX idx_events_user_type_created
        ON events(user_id, event_type, created_at DESC);
        """
    )


def find_events(conn: sqlite3.Connection, user_id: int, event_type: str) -> list[dict[str, Any]]:
    """执行与查询计划相同的业务查询。"""
    rows = conn.execute(
        """
        SELECT id, created_at, payload
        FROM events
        WHERE user_id = ? AND event_type = ?
        ORDER BY created_at DESC;
        """,
        (user_id, event_type),
    ).fetchall()
    return [dict(row) for row in rows]


def main() -> None:
    with create_event_db() as conn:
        print("建索引前：")
        print("\n".join(explain_user_event_query(conn, 7, "purchase")))

        create_covering_index(conn)
        print("\n建索引后：")
        print("\n".join(explain_user_event_query(conn, 7, "purchase")))

        print("\n查询结果前 3 行：")
        for row in find_events(conn, 7, "purchase")[:3]:
            print(row)


if __name__ == "__main__":
    main()
