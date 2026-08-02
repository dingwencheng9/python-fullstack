"""练习 1: 电商数据分析 - 参考答案"""

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
    return con.execute("""
        SELECT
            p.category,
            SUM(s.amount) AS total_sales,
            COUNT(*) AS order_count
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_sales DESC
    """).df()


def q2_customer_segments(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Q2: 客户分层分析（VIP vs Regular）"""
    return con.execute("""
        SELECT
            c.tier,
            COUNT(DISTINCT c.customer_id) AS customer_count,
            SUM(s.amount) AS total_sales,
            AVG(s.amount) AS avg_order_value
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.tier
    """).df()


def q3_monthly_trend(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Q3: 月度销售趋势"""
    return con.execute("""
        SELECT
            strftime(sale_date, '%Y-%m') AS month,
            SUM(amount) AS total_sales,
            COUNT(*) AS order_count
        FROM sales
        GROUP BY strftime(sale_date, '%Y-%m')
        ORDER BY month
    """).df()


def q4_channel_performance(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Q4: 渠道表现对比"""
    return con.execute("""
        SELECT
            channel,
            SUM(amount) AS total_sales,
            COUNT(*) AS order_count,
            AVG(amount) AS avg_order_value
        FROM sales
        GROUP BY channel
        ORDER BY total_sales DESC
    """).df()


def q5_top_customers(con: duckdb.DuckDBPyConnection, n: int = 100) -> pd.DataFrame:
    """Q5: Top N 客户"""
    return con.execute(f"""
        SELECT
            c.customer_id,
            c.name,
            c.tier,
            SUM(s.amount) AS total_spent,
            COUNT(*) AS order_count
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_id, c.name, c.tier
        ORDER BY total_spent DESC
        LIMIT {n}
    """).df()


def q6_cohort_retention(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Q6: 用户留存分析"""
    return con.execute("""
        WITH first_purchase AS (
            SELECT
                customer_id,
                DATE_TRUNC('month', MIN(sale_date)) AS cohort_month
            FROM sales
            GROUP BY customer_id
        ),
        cohort_size AS (
            SELECT cohort_month, COUNT(*) AS n_customers
            FROM first_purchase
            GROUP BY cohort_month
        ),
        cohort_activity AS (
            SELECT
                fp.cohort_month,
                DATE_TRUNC('month', s.sale_date) AS activity_month,
                COUNT(DISTINCT s.customer_id) AS active_customers
            FROM sales s
            JOIN first_purchase fp ON s.customer_id = fp.customer_id
            GROUP BY fp.cohort_month, DATE_TRUNC('month', s.sale_date)
        )
        SELECT
            ca.cohort_month,
            cs.n_customers AS cohort_size,
            ca.activity_month,
            ca.active_customers,
            ROUND(ca.active_customers * 100.0 / cs.n_customers, 2) AS retention_rate
        FROM cohort_activity ca
        JOIN cohort_size cs ON ca.cohort_month = cs.cohort_month
        ORDER BY ca.cohort_month, ca.activity_month
    """).df()


def main() -> None:
    """主函数"""
    con = load_data()

    print("数据加载完成")

    print("\n" + "=" * 60)
    print("Q1: 按销售额排序的类别")
    print("=" * 60)
    print(q1_top_categories(con))

    print("\n" + "=" * 60)
    print("Q2: 客户分层分析")
    print("=" * 60)
    print(q2_customer_segments(con))

    print("\n" + "=" * 60)
    print("Q3: 月度销售趋势")
    print("=" * 60)
    print(q3_monthly_trend(con))

    print("\n" + "=" * 60)
    print("Q4: 渠道表现")
    print("=" * 60)
    print(q4_channel_performance(con))

    print("\n" + "=" * 60)
    print("Q5: Top 客户")
    print("=" * 60)
    print(q5_top_customers(con, 100))

    print("\n" + "=" * 60)
    print("Q6: 用户留存")
    print("=" * 60)
    print(q6_cohort_retention(con))

    con.close()


if __name__ == "__main__":
    main()
