#!/usr/bin/env python3
"""
SQL 查询构建器

本文档演示如何用 Python 构建 SQL 查询，包括 SELECT、INSERT、UPDATE、DELETE 等。
"""

from dataclasses import dataclass
from typing import Any, Optional
import sqlite3


@dataclass
class SQLQuery:
    """SQL 查询构建器"""

    table: str
    columns: list[str] = None
    conditions: dict[str, Any] = None
    order_by: str = None
    limit: int = None
    offset: int = None

    def select(self) -> str:
        """生成 SELECT 语句"""
        cols = ", ".join(self.columns) if self.columns else "*"
        query = f"SELECT {cols} FROM {self.table}"

        if self.conditions:
            where = " AND ".join(f"{k} = ?" for k in self.conditions.keys())
            query += f" WHERE {where}"

        if self.order_by:
            query += f" ORDER BY {self.order_by}"

        if self.limit:
            query += f" LIMIT {self.limit}"

        if self.offset:
            query += f" OFFSET {self.offset}"

        return query

    def insert(self) -> tuple[str, list]:
        """生成 INSERT 语句"""
        cols = ", ".join(self.columns)
        placeholders = ", ".join(["?"] * len(self.columns))
        query = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"
        values = list(self.conditions.values()) if self.conditions else []
        return query, values

    def update(self) -> tuple[str, list]:
        """生成 UPDATE 语句"""
        set_clause = ", ".join(f"{k} = ?" for k in self.columns)
        query = f"UPDATE {self.table} SET {set_clause}"

        values = [self.conditions[k] for k in self.columns]

        if self.conditions.get("WHERE"):
            where = self.conditions["WHERE"]
            query += f" WHERE {where}"
            values.append(where)

        return query, values

    def delete(self) -> tuple[str, list]:
        """生成 DELETE 语句"""
        query = f"DELETE FROM {self.table}"

        if self.conditions:
            where = " AND ".join(f"{k} = ?" for k in self.conditions.keys())
            query += f" WHERE {where}"

        return query, list(self.conditions.values())


def demo_basic_queries():
    """演示基本查询"""
    print("=" * 70)
    print("SQL 查询构建器演示")
    print("=" * 70)

    # SELECT 查询
    print("\n📋 SELECT 查询:")
    print("-" * 50)

    query = SQLQuery(
        table="users",
        columns=["id", "name", "email"],
        conditions={"status": "active"},
        order_by="created_at DESC",
        limit=10,
    )

    print(f"SQL: {query.select()}")
    print(f"参数: {list(query.conditions.values())}")

    # INSERT 查询
    print("\n➕ INSERT 查询:")
    print("-" * 50)

    query = SQLQuery(
        table="users",
        columns=["name", "email", "password_hash"],
        conditions={"name": "Alice", "email": "alice@example.com", "password_hash": "hashed123"},
    )

    sql, values = query.insert()
    print(f"SQL: {sql}")
    print(f"参数: {values}")


def demo_join_queries():
    """演示 JOIN 查询"""
    print("\n" + "=" * 70)
    print("JOIN 查询示例")
    print("=" * 70)

    # INNER JOIN
    print("\n🔗 INNER JOIN:")
    print("-" * 50)
    sql = """
SELECT u.name, o.order_id, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
ORDER BY o.created_at DESC
"""
    print(sql)

    # LEFT JOIN
    print("\n🔗 LEFT JOIN:")
    print("-" * 50)
    sql = """
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING order_count > 0
"""
    print(sql)


def demo_aggregation():
    """演示聚合查询"""
    print("\n" + "=" * 70)
    print("聚合查询示例")
    print("=" * 70)

    queries = [
        ("COUNT", "SELECT COUNT(*) FROM users"),
        ("SUM", "SELECT SUM(amount) FROM orders WHERE status = 'completed'"),
        ("AVG", "SELECT AVG(price) FROM products"),
        ("MIN/MAX", "SELECT MIN(created_at), MAX(created_at) FROM orders"),
        (
            "GROUP BY",
            """
SELECT status, COUNT(*) as count
FROM orders
GROUP BY status
HAVING count > 10
ORDER BY count DESC
""",
        ),
        (
            "子查询",
            """
SELECT name, email
FROM users
WHERE id IN (
    SELECT user_id
    FROM orders
    WHERE total > 1000
)
""",
        ),
    ]

    for name, sql in queries:
        print(f"\n{name}:")
        print("-" * 30)
        print(sql.strip())


def demo_sql_injection_prevention():
    """演示 SQL 注入防护"""
    print("\n" + "=" * 70)
    print("SQL 注入防护")
    print("=" * 70)

    # ❌ 危险：字符串拼接
    print("\n❌ 危险方式（字符串拼接）:")
    print("-" * 50)
    user_input = "admin'; DROP TABLE users; --"
    dangerous_sql = f"SELECT * FROM users WHERE name = '{user_input}'"
    print(f"输入: {user_input}")
    print(f"SQL: {dangerous_sql}")

    # ✅ 安全：参数化查询
    print("\n✅ 安全方式（参数化查询）:")
    print("-" * 50)
    safe_sql = "SELECT * FROM users WHERE name = ?"
    print(f"SQL: {safe_sql}")
    print(f"参数: ['{user_input}']")
    print(">>> 参数会被安全转义，不会执行 DROP TABLE")


def demo_orm_best_practices():
    """演示生产环境 ORM 最佳实践（SQLAlchemy 2.0）"""
    print("\n" + "=" * 70)
    print("生产环境最佳实践：SQLAlchemy ORM")
    print("=" * 70)

    # ✅ ORM 自动参数化，永远不拼接用户输入
    print("\n✅ 推荐方式（SQLAlchemy ORM）:")
    print("-" * 50)
    print("""
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession

    # 创建查询：ORM 自动处理参数化
    query = select(User).where(User.name == user_input)
    # 生成的 SQL: SELECT * FROM users WHERE name = :name
    # 用户输入作为安全参数传递，绝不拼入 SQL 字符串

    result = await session.execute(query)
    user = result.scalar_one_or_none()
    """)

    print("ORM 优势:")
    print("  1. 自动参数化 → 零 SQL 注入风险")
    print("  2. 类型安全 → 编辑器自动补全")
    print("  3. 可移植性 → 切换数据库只需改连接字符串")
    print("  4. 关联查询 → relationship 自动加载")

    # 对比表格
    print("\n📊 SQL vs ORM 对比:")
    print("-" * 50)
    print("""
    | 场景           | SQL 字符串拼接    | ORM 参数化查询      |
    |----------------|------------------|-------------------|
    | SQL 注入风险   | 高（危险）        | 低（安全）          |
    | 类型检查       | 无               | 有（IDE 提示）      |
    | 维护成本       | 高（手写 SQL）    | 低（自动生成）      |
    | 数据库迁移     | 需重写 SQL       | 自动（alembic）     |
    | 关联查询       | 手写 JOIN        | relationship 自动   |
    """)


if __name__ == "__main__":
    demo_basic_queries()
    demo_join_queries()
    demo_aggregation()
    demo_sql_injection_prevention()
    demo_orm_best_practices()
