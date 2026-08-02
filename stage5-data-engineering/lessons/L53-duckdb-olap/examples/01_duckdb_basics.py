"""示例 1: DuckDB 基础操作

展示 DuckDB 的基本用法：
- 连接与创建表
- 插入数据
- 查询数据
"""

from __future__ import annotations

import duckdb
import pandas as pd


def basic_connection() -> duckdb.DuckDBPyConnection:
    """基础连接操作"""
    # 内存数据库
    con = duckdb.connect(":memory:")

    # 持久化数据库
    # con = duckdb.connect("analytics.db")

    print("DuckDB 版本:", con.execute("SELECT version()").fetchone()[0])
    return con


def create_and_insert(con: duckdb.DuckDBPyConnection) -> None:
    """创建表和插入数据"""
    # 创建表
    con.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            department VARCHAR,
            salary DECIMAL(10,2),
            hire_date DATE
        )
    """)

    # 插入数据 - 方式1: VALUES
    con.execute("""
        INSERT INTO employees VALUES
        (1, 'Alice', 'Engineering', 80000, '2023-01-15'),
        (2, 'Bob', 'Sales', 65000, '2023-03-20'),
        (3, 'Charlie', 'Engineering', 85000, '2022-11-01'),
        (4, 'David', 'Marketing', 60000, '2024-01-10')
    """)

    # 插入数据 - 方式2: SELECT
    con.execute("""
        INSERT INTO employees
        SELECT
            10 + id,
            name || ' (Copy)',
            department,
            salary * 0.9,
            hire_date
        FROM employees
    """)


def basic_queries(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """基础查询"""
    # 查看所有数据
    print("\n所有员工:")
    result = con.execute("SELECT * FROM employees").fetchdf()
    print(result)

    # 条件查询
    print("\n工程部门员工:")
    result = con.execute("""
        SELECT name, salary
        FROM employees
        WHERE department = 'Engineering'
        ORDER BY salary DESC
    """).fetchdf()
    print(result)

    # 聚合查询
    print("\n部门薪资统计:")
    result = con.execute("""
        SELECT
            department,
            COUNT(*) AS employee_count,
            AVG(salary) AS avg_salary,
            MAX(salary) AS max_salary
        FROM employees
        GROUP BY department
    """).fetchdf()
    print(result)

    return result


def window_functions(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """窗口函数"""
    print("\n窗口函数示例:")
    result = con.execute("""
        SELECT
            name,
            department,
            salary,
            AVG(salary) OVER (PARTITION BY department) AS dept_avg,
            salary - AVG(salary) OVER (PARTITION BY department) AS vs_avg,
            RANK() OVER (ORDER BY salary DESC) AS salary_rank
        FROM employees
        ORDER BY salary_rank
    """).fetchdf()
    print(result)
    return result


def create_from_query(con: duckdb.DuckDBPyConnection) -> None:
    """从查询创建表"""
    # 创建汇总表
    con.execute("""
        CREATE TABLE dept_summary AS
        SELECT
            department,
            COUNT(*) AS count,
            SUM(salary) AS total_salary,
            AVG(salary) AS avg_salary
        FROM employees
        GROUP BY department
    """)

    print("\n部门汇总表:")
    print(con.execute("SELECT * FROM dept_summary").fetchdf())


def drop_and_cleanup(con: duckdb.DuckDBPyConnection) -> None:
    """清理资源"""
    con.execute("DROP TABLE IF EXISTS employees")
    con.execute("DROP TABLE IF EXISTS dept_summary")
    con.close()
    print("\n资源已清理")


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("DuckDB 基础操作示例")
    print("=" * 60)

    con = basic_connection()

    print("\n" + "=" * 60)
    print("创建表和插入数据")
    print("=" * 60)
    create_and_insert(con)

    print("\n" + "=" * 60)
    print("基础查询")
    print("=" * 60)
    basic_queries(con)

    print("\n" + "=" * 60)
    print("窗口函数")
    print("=" * 60)
    window_functions(con)

    print("\n" + "=" * 60)
    print("从查询创建表")
    print("=" * 60)
    create_from_query(con)

    drop_and_cleanup(con)


if __name__ == "__main__":
    main()
