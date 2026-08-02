"""L50 DuckDB 销售分析实战"""

from __future__ import annotations

import duckdb
import numpy as np
import pandas as pd


def generate_sales_data(n: int = 100000) -> pd.DataFrame:
    """生成模拟销售数据"""
    np.random.seed(42)
    dates = pd.date_range("2025-01-01", "2025-12-31")
    return pd.DataFrame(
        {
            "order_date": np.random.choice(dates, n),
            "region": np.random.choice(["华北", "华东", "华南", "西部"], n),
            "category": np.random.choice(["电子产品", "服装", "食品", "家居"], n),
            "amount": np.random.uniform(10, 5000, n).round(2),
        }
    )


def monthly_trends(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """月度销售趋势"""
    return conn.execute("""
        SELECT
            date_trunc('month', order_date) AS month,
            COUNT(*) AS orders,
            SUM(amount) AS revenue,
            AVG(amount) AS avg_order
        FROM sales
        GROUP BY month
        ORDER BY month
    """).df()


def top_categories(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """各地区 Top 3 品类"""
    return conn.execute("""
        SELECT region, category,
               COUNT(*) AS sales_count,
               SUM(amount) AS total_revenue,
               RANK() OVER (PARTITION BY region ORDER BY SUM(amount) DESC) AS rank
        FROM sales
        GROUP BY region, category
        QUALIFY rank <= 3
        ORDER BY region, rank
    """).df()


def compare_performance(conn: duckdb.DuckDBPyConnection, df: pd.DataFrame) -> dict:
    """DuckDB vs Pandas 性能对比"""
    import time

    start = time.time()
    conn.execute("SELECT region, SUM(amount) FROM sales GROUP BY region").fetchall()
    duckdb_time = time.time() - start

    start = time.time()
    df.groupby("region")["amount"].sum()
    pandas_time = time.time() - start

    return {
        "duckdb_s": round(duckdb_time, 4),
        "pandas_s": round(pandas_time, 4),
        "speedup": round(pandas_time / duckdb_time, 1),
    }


if __name__ == "__main__":
    df = generate_sales_data()
    conn = duckdb.connect()
    conn.register("sales", df)

    print("月度趋势:")
    print(monthly_trends(conn).head())
    print("\nTop 品类:")
    print(top_categories(conn))
    print("\n性能对比:")
    perf = compare_performance(conn, df)
    print(f"  DuckDB: {perf['duckdb_s']:.3f}s")
    print(f"  Pandas: {perf['pandas_s']:.3f}s")
    print(f"  加速比: {perf['speedup']}x")
