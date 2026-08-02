"""L50 DuckDB 基础查询示例"""

from __future__ import annotations

import duckdb
import pandas as pd


def basic_queries() -> None:
    """基本 SQL 查询"""
    conn = duckdb.connect()
    result = conn.execute("SELECT 42 AS answer").fetchall()
    print(f"基础查询: {result}")

    # 多列 + 计算
    result = conn.execute("""
        SELECT
            'Hello' AS greet,
            42 AS num,
            3.14 AS pi,
            num * 2 AS doubled
    """).fetchall()
    print(f"多列: {result}")


def query_dataframe() -> None:
    """查询 Python DataFrame"""
    pd.DataFrame(
        {
            "city": ["北京", "上海", "广州", "深圳"],
            "population": [2154, 2475, 1868, 1768],
            "area_km2": [16411, 6341, 7434, 1997],
        }
    )

    result = duckdb.sql("""
        SELECT city, population,
               ROUND(population / area_km2, 1) AS density
        FROM df
        WHERE population > 2000
        ORDER BY density DESC
    """).df()
    print(f"\nDataFrame 查询:\n{result}")


def file_query() -> None:
    """直接查询 CSV 文件"""
    import os
    import tempfile

    # 创建临时 CSV
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,city\nAlice,30,北京\nBob,25,上海\nCharlie,35,广州\n")
        tmp_path = f.name

    conn = duckdb.connect()
    result = conn.execute(f"""
        SELECT * FROM read_csv_auto('{tmp_path}')
        WHERE age >= 30
    """).df()
    print(f"CSV 查询:\n{result}")
    os.unlink(tmp_path)


if __name__ == "__main__":
    basic_queries()
    query_dataframe()
    file_query()
