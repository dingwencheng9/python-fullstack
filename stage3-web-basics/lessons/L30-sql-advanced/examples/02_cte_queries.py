"""L30 SQL 进阶示例 2：普通 CTE 与递归 CTE。

运行方式：
    uv run python stage3-web-basics/lessons/L30-sql-advanced/examples/02_cte_queries.py
"""

from __future__ import annotations

import sqlite3
from typing import Any


def create_org_db() -> sqlite3.Connection:
    """创建组织架构样例数据库。"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manager_id INTEGER REFERENCES employees(id),
            department TEXT NOT NULL,
            salary INTEGER NOT NULL
        );
        """
    )
    conn.executemany(
        "INSERT INTO employees(id, name, manager_id, department, salary) VALUES (?, ?, ?, ?, ?)",
        [
            (1, "Ada", None, "engineering", 280),
            (2, "Ben", 1, "engineering", 180),
            (3, "Chen", 1, "engineering", 170),
            (4, "Dora", 2, "engineering", 120),
            (5, "Eve", None, "data", 260),
            (6, "Finn", 5, "data", 150),
            (7, "Gina", 5, "data", 140),
        ],
    )
    return conn


def above_department_average(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """使用普通 CTE 查询高于部门平均薪资的员工。"""
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


def organization_tree(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """使用递归 CTE 展开组织树。"""
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


def main() -> None:
    with create_org_db() as conn:
        print("高于部门平均薪资的员工：")
        for row in above_department_average(conn):
            print(row)

        print("\n组织树：")
        for row in organization_tree(conn):
            print("  " * row["depth"] + row["name"] + f" ({row['path']})")


if __name__ == "__main__":
    main()
