"""练习 1: 电商数据分析

使用 DuckDB 分析电商销售数据。
"""

from __future__ import annotations

import duckdb
import pandas as pd


def load_data() -> duckdb.DuckDBPyConnection:
    """加载数据"""
    con = duckdb.connect(":memory:")

    # 创建销售数据
    con.execute("""
        CREATE TABLE sales AS
        SELECT
            i AS order_id,
            (RANDOM() * 1000 + 1)::INTEGER AS product_id,
            (RANDOM() * 500 + 1)::INTEGER AS customer_id,
            (RANDOM() * 1000 + 10)::DECIMAL(10,2) AS amount,
            (RANDOM() * 5 + 1)::INTEGER AS quantity,
            DATE '2024-01-01' + INTERVAL (RANDOM() * 365) DAY AS sale_date,
            CASE (RANDOM() * 3)::INTEGER
                WHEN 0 THEN 'online'
                WHEN 1 THEN 'store'
                ELSE 'wholesale'
            END AS channel
        FROM generate_series(1, 100000) t(i)
    """)

    # 创建客户数据
    con.execute("""
        CREATE TABLE customers AS
        SELECT
            i AS customer_id,
            'Customer ' || i::VARCHAR AS name,
            CASE (RANDOM() * 2)::INTEGER
                WHEN 0 THEN 'VIP'
                ELSE 'Regular'
            END AS tier,
            DATE '2020-01-01' + INTERVAL (RANDOM() * 1460) DAY AS registration_date
        FROM generate_series(1, 500) t(i)
    """)

    # 创建产品数据
    con.execute("""
        CREATE TABLE products AS
        SELECT
            i AS product_id,
            'Product ' || i::VARCHAR AS name,
            CASE (RANDOM() * 3)::INTEGER
                WHEN 0 THEN 'Electronics'
                WHEN 1 THEN 'Clothing'
                WHEN 2 THEN 'Food'
                ELSE 'Home'
            END AS category,
            (RANDOM() * 500 + 50)::DECIMAL(10,2) AS price
        FROM generate_series(1, 1000) t(i)
    """)

    return con


def q1_top_categories(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Q1: 按销售额排序的产品类别"""
    # TODO: 实现


def q2_customer_segments(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Q2: 客户分层分析（VIP vs Regular）"""
    # TODO: 实现


def q3_monthly_trend(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Q3: 月度销售趋势"""
    # TODO: 实现


def q4_channel_performance(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Q4: 渠道表现对比"""
    # TODO: 实现


def q5_top_customers(con: duckdb.DuckDBPyConnection, n: int = 100) -> pd.DataFrame:
    """Q5: Top N 客户"""
    # TODO: 实现


def q6_cohort_retention(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Q6: 用户留存分析"""
    # TODO: 实现


def main() -> None:
    """主函数"""
    con = load_data()

    print("数据加载完成")

    print("\n" + "=" * 60)
    print("Q1: 按销售额排序的类别")
    print("=" * 60)
    result1 = q1_top_categories(con)
    print(result1)

    print("\n" + "=" * 60)
    print("Q2: 客户分层分析")
    print("=" * 60)
    result2 = q2_customer_segments(con)
    print(result2)

    print("\n" + "=" * 60)
    print("Q3: 月度销售趋势")
    print("=" * 60)
    result3 = q3_monthly_trend(con)
    print(result3)

    print("\n" + "=" * 60)
    print("Q4: 渠道表现")
    print("=" * 60)
    result4 = q4_channel_performance(con)
    print(result4)

    print("\n" + "=" * 60)
    print("Q5: Top 客户")
    print("=" * 60)
    result5 = q5_top_customers(con, 100)
    print(result5)

    print("\n" + "=" * 60)
    print("Q6: 用户留存")
    print("=" * 60)
    result6 = q6_cohort_retention(con)
    print(result6)

    con.close()


if __name__ == "__main__":
    main()
