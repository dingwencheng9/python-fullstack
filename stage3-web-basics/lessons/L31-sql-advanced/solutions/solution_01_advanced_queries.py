"""L30 SQL 进阶练习参考答案。

设计目标：
- 使用 sqlite3 内存数据库，避免外部数据库依赖。
- 覆盖窗口函数、CTE、递归 CTE、索引查询计划四个核心能力。
"""

from __future__ import annotations

import sqlite3
from typing import Any


def create_learning_db() -> sqlite3.Connection:
    """创建练习用内存数据库并写入课程、电商与组织结构数据。"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer TEXT NOT NULL,
            category TEXT NOT NULL,
            ordered_on TEXT NOT NULL,
            amount INTEGER NOT NULL
        );

        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manager_id INTEGER REFERENCES employees(id),
            department TEXT NOT NULL,
            salary INTEGER NOT NULL
        );

        CREATE TABLE events (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            created_at TEXT NOT NULL,
            payload TEXT NOT NULL
        );
        """
    )
    conn.executemany(
        "INSERT INTO orders(customer, category, ordered_on, amount) VALUES (?, ?, ?, ?)",
        [
            ("alice", "book", "2026-01-01", 120),
            ("alice", "book", "2026-01-05", 80),
            ("bob", "book", "2026-01-03", 180),
            ("carol", "book", "2026-01-04", 70),
            ("alice", "tool", "2026-01-02", 220),
            ("bob", "tool", "2026-01-04", 90),
            ("carol", "tool", "2026-01-06", 260),
            ("dave", "tool", "2026-01-07", 140),
        ],
    )
    conn.executemany(
        "INSERT INTO employees(id, name, manager_id, department, salary) VALUES (?, ?, ?, ?, ?)",
        [
            (1, "Ada", None, "engineering", 300),
            (2, "Ben", 1, "engineering", 180),
            (3, "Chen", 1, "engineering", 170),
            (4, "Dora", 2, "engineering", 120),
            (5, "Eve", None, "data", 260),
            (6, "Finn", 5, "data", 150),
            (7, "Gina", 5, "data", 140),
        ],
    )
    conn.executemany(
        "INSERT INTO events(user_id, event_type, created_at, payload) VALUES (?, ?, ?, ?)",
        [
            (
                index % 16,
                "purchase" if index % 5 == 0 else "page_view",
                f"2026-02-{(index % 28) + 1:02d}",
                f"payload-{index}",
            )
            for index in range(240)
        ],
    )
    return conn


def top_customers_by_category(
    conn: sqlite3.Connection,
    *,
    limit: int = 2,
) -> list[dict[str, Any]]:
    """返回每个品类消费金额最高的前 N 名客户。"""
    rows = conn.execute(
        """
        WITH customer_totals AS (
            SELECT category, customer, SUM(amount) AS total_amount
            FROM orders
            GROUP BY category, customer
        ), ranked AS (
            SELECT
                category,
                customer,
                total_amount,
                ROW_NUMBER() OVER (
                    PARTITION BY category
                    ORDER BY total_amount DESC, customer ASC
                ) AS row_number
            FROM customer_totals
        )
        SELECT category, customer, total_amount, row_number
        FROM ranked
        WHERE row_number <= ?
        ORDER BY category, row_number;
        """,
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def category_running_total(conn: sqlite3.Connection, category: str) -> list[dict[str, Any]]:
    """返回指定品类按订单时间累计的销售额。"""
    rows = conn.execute(
        """
        SELECT
            ordered_on,
            customer,
            amount,
            SUM(amount) OVER (
                PARTITION BY category
                ORDER BY ordered_on, id
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS running_total
        FROM orders
        WHERE category = ?
        ORDER BY ordered_on, id;
        """,
        (category,),
    ).fetchall()
    return [dict(row) for row in rows]


def above_department_average(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """使用 CTE 查询高于本部门平均薪资的员工。"""
    rows = conn.execute(
        """
        WITH department_average AS (
            SELECT department, AVG(salary) AS avg_salary
            FROM employees
            GROUP BY department
        )
        SELECT e.department, e.name, e.salary, ROUND(d.avg_salary, 2) AS avg_salary
        FROM employees e
        JOIN department_average d ON d.department = e.department
        WHERE e.salary > d.avg_salary
        ORDER BY e.department, e.salary DESC;
        """
    ).fetchall()
    return [dict(row) for row in rows]


def organization_paths(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """使用递归 CTE 生成组织路径。"""
    rows = conn.execute(
        """
        WITH RECURSIVE org_tree(id, name, manager_id, depth, path) AS (
            SELECT id, name, manager_id, 0 AS depth, name AS path
            FROM employees
            WHERE manager_id IS NULL

            UNION ALL

            SELECT e.id, e.name, e.manager_id, org_tree.depth + 1, org_tree.path || ' > ' || e.name
            FROM employees e
            JOIN org_tree ON e.manager_id = org_tree.id
        )
        SELECT id, name, manager_id, depth, path
        FROM org_tree
        ORDER BY path;
        """
    ).fetchall()
    return [dict(row) for row in rows]


def create_event_lookup_index(conn: sqlite3.Connection) -> None:
    """创建覆盖事件查询条件与排序的复合索引。"""
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_events_user_type_created
        ON events(user_id, event_type, created_at DESC);
        """
    )


def event_query_plan(conn: sqlite3.Connection, user_id: int, event_type: str) -> list[str]:
    """返回事件查询的 EXPLAIN QUERY PLAN 明细。"""
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


def find_events(conn: sqlite3.Connection, user_id: int, event_type: str) -> list[dict[str, Any]]:
    """按用户和事件类型查询事件。"""
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
