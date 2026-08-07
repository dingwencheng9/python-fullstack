"""L30 SQL 进阶示例 1：窗口函数。

本示例只使用 Python 标准库 sqlite3，便于在无 PostgreSQL 的学习环境中运行。
SQLite 3.25+ 支持本课使用的窗口函数语法。

运行方式：
    uv run python stage3-web-basics/lessons/L30-sql-advanced/examples/01_window_functions.py
"""

from __future__ import annotations

import sqlite3
from typing import Any


def create_sales_db() -> sqlite3.Connection:
    """创建内存数据库并写入销售样例数据。"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            region TEXT NOT NULL,
            seller TEXT NOT NULL,
            sold_on TEXT NOT NULL,
            amount INTEGER NOT NULL
        );
        """
    )
    conn.executemany(
        "INSERT INTO sales(region, seller, sold_on, amount) VALUES (?, ?, ?, ?)",
        [
            ("north", "Alice", "2026-01-01", 120),
            ("north", "Alice", "2026-01-03", 80),
            ("north", "Bob", "2026-01-02", 160),
            ("north", "Bob", "2026-01-04", 40),
            ("south", "Carol", "2026-01-01", 200),
            ("south", "Dave", "2026-01-02", 150),
            ("south", "Carol", "2026-01-05", 90),
            ("south", "Dave", "2026-01-06", 60),
        ],
    )
    return conn


def top_sellers_by_region(conn: sqlite3.Connection, limit: int = 2) -> list[dict[str, Any]]:
    """使用 ROW_NUMBER 选出每个区域销售额最高的前 N 名销售。"""
    rows = conn.execute(
        """
        WITH seller_totals AS (
            SELECT region, seller, SUM(amount) AS total_amount
            FROM sales
            GROUP BY region, seller
        ), ranked AS (
            SELECT
                region,
                seller,
                total_amount,
                ROW_NUMBER() OVER (
                    PARTITION BY region
                    ORDER BY total_amount DESC, seller ASC
                ) AS row_number
            FROM seller_totals
        )
        SELECT region, seller, total_amount, row_number
        FROM ranked
        WHERE row_number <= ?
        ORDER BY region, row_number;
        """,
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def running_region_total(conn: sqlite3.Connection, region: str) -> list[dict[str, Any]]:
    """使用 SUM(...) OVER 计算某个区域按日期滚动累计销售额。"""
    rows = conn.execute(
        """
        SELECT
            sold_on,
            seller,
            amount,
            SUM(amount) OVER (
                PARTITION BY region
                ORDER BY sold_on, id
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS running_total
        FROM sales
        WHERE region = ?
        ORDER BY sold_on, id;
        """,
        (region,),
    ).fetchall()
    return [dict(row) for row in rows]


def main() -> None:
    with create_sales_db() as conn:
        print("每个区域 Top 2 销售：")
        for row in top_sellers_by_region(conn):
            print(row)

        print("\nnorth 区域滚动累计销售额：")
        for row in running_region_total(conn, "north"):
            print(row)


if __name__ == "__main__":
    main()
