"""示例 2: DuckDB SQL 扩展语法

展示 DuckDB 特有的 SQL 扩展：
- SAMPLE 子句
- QUALIFY 子句
- PIVOT 语句
- LATERAL JOIN
"""

from __future__ import annotations

import duckdb
import pandas as pd


def create_sample_data(con: duckdb.DuckDBPyConnection) -> None:
    """创建示例数据"""
    # 创建销售数据
    con.execute("""
        CREATE TABLE sales AS
        SELECT
            i AS order_id,
            (RANDOM() * 10 + 1)::INTEGER AS product_id,
            (RANDOM() * 100 + 1)::INTEGER AS customer_id,
            (RANDOM() * 1000 + 10)::DECIMAL(10,2) AS amount,
            DATE '2024-01-01' + INTERVAL (RANDOM() * 365) DAY AS sale_date
        FROM generate_series(1, 10000) t(i)
    """)

    # 创建产品数据
    con.execute("""
        CREATE TABLE products AS
        SELECT
            i AS product_id,
            'Product ' || i::VARCHAR AS name,
            CASE (RANDOM() * 4)::INTEGER
                WHEN 0 THEN 'Electronics'
                WHEN 1 THEN 'Clothing'
                WHEN 2 THEN 'Food'
                ELSE 'Home'
            END AS category,
            (RANDOM() * 500 + 50)::DECIMAL(10,2) AS base_price
        FROM generate_series(1, 10) t(i)
    """)

    # 创建客户数据
    con.execute("""
        CREATE TABLE customers AS
        SELECT
            i AS customer_id,
            'Customer ' || i::VARCHAR AS name,
            CASE (RANDOM() * 3)::INTEGER
                WHEN 0 THEN 'VIP'
                WHEN 1 THEN 'Regular'
                ELSE 'New'
            END AS tier,
            DATE '2020-01-01' + INTERVAL (RANDOM() * 1460) DAY AS registration_date
        FROM generate_series(1, 100) t(i)
    """)

    print("示例数据创建完成")


def sample_clause(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """SAMPLE 子句 - 数据采样"""
    print("\n" + "=" * 60)
    print("SAMPLE 子句示例")
    print("=" * 60)

    # 百分比采样 (1%)
    result1 = con.execute("""
        SELECT COUNT(*) AS count FROM sales SAMPLE (1)
    """).fetchdf()
    print("\n1% 采样结果数:", result1.iloc[0]["count"])

    # 固定行数采样
    result2 = con.execute("""
        SELECT * FROM sales USING SAMPLE 100 ROWS
    """).fetchdf()
    print("\n100 行采样:\n", result2.head())

    # 分层采样
    result3 = con.execute("""
        SELECT
            tier,
            COUNT(*) AS count
        FROM customers SAMPLE (50 PERCENT) BY (tier)
        GROUP BY tier
    """).fetchdf()
    print("\n分层采样（按 tier）:\n", result3)

    return result3


def qualify_clause(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """QUALIFY 子句 - 窗口函数过滤"""
    print("\n" + "=" * 60)
    print("QUALIFY 子句示例")
    print("=" * 60)

    # 找出每个客户购买最多的产品
    result = con.execute("""
        SELECT
            customer_id,
            product_id,
            total_amount,
            RANK() OVER (PARTITION BY customer_id ORDER BY total_amount DESC) AS rank
        FROM (
            SELECT
                customer_id,
                product_id,
                SUM(amount) AS total_amount
            FROM sales
            GROUP BY customer_id, product_id
        )
        QUALIFY RANK() OVER (PARTITION BY customer_id ORDER BY total_amount DESC) <= 3
        ORDER BY customer_id, rank
        LIMIT 20
    """).fetchdf()

    print("\n每个客户的 Top 3 产品:\n", result)
    return result


def pivot_statement(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """PIVOT 语句 - 透视表"""
    print("\n" + "=" * 60)
    print("PIVOT 语句示例")
    print("=" * 60)

    # 透视表：按月份和产品类别统计销售额
    result = con.execute("""
        PIVOT sales
        ON strftime(sale_date, '%Y-%m')
        USING SUM(amount)
        GROUP BY product_id
        LIMIT 10
    """).fetchdf()

    print("\n月度销售额透视表（部分）:\n", result)
    return result


def lateral_join(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """LATERAL JOIN - 横向子查询"""
    print("\n" + "=" * 60)
    print("LATERAL JOIN 示例")
    print("=" * 60)

    # 找出每个产品类别中购买金额最高的客户
    result = con.execute("""
        SELECT
            p.category,
            p.product_id,
            p.name AS product_name,
            top_customer.customer_id,
            top_customer.total_amount
        FROM products p,
        LATERAL (
            SELECT
                s.customer_id,
                SUM(s.amount) AS total_amount
            FROM sales s
            WHERE s.product_id = p.product_id
            GROUP BY s.customer_id
            ORDER BY total_amount DESC
            LIMIT 1
        ) AS top_customer
        ORDER BY p.category, top_customer.total_amount DESC
    """).fetchdf()

    print("\n每个产品的 Top 客户:\n", result)
    return result


def list_concat(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """DuckDB 特有的列表函数"""
    print("\n" + "=" * 60)
    print("列表函数示例")
    print("=" * 60)

    # 创建包含列表的表
    con.execute("""
        CREATE TABLE orders AS
        SELECT
            i AS order_id,
            customer_id,
            [i, i+1, i+2] AS product_ids,
            i * 100 AS amount
        FROM generate_series(1, 100) t(i)
    """)

    # 列表函数
    result = con.execute("""
        SELECT
            customer_id,
            list_concat(product_ids, [100, 200]) AS all_products,
            list_length(product_ids) AS num_products,
            list_extract(product_ids, 1) AS first_product
        FROM orders
        WHERE customer_id <= 5
    """).fetchdf()

    print("\n列表函数示例:\n", result)
    return result


def struct_and_nested(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """结构体和嵌套数据"""
    print("\n" + "=" * 60)
    print("结构体和嵌套数据示例")
    print("=" * 60)

    # 创建包含结构体的表
    con.execute("""
        CREATE TABLE events AS
        SELECT
            i AS event_id,
            customer_id,
            {
                'action': CASE (RANDOM() * 2)::INTEGER
                    WHEN 0 THEN 'click'
                    ELSE 'view'
                END,
                'page': 'product_' || (RANDOM() * 10)::INTEGER::VARCHAR,
                'timestamp': CURRENT_TIMESTAMP - INTERVAL (RANDOM() * 86400) SECOND
            } AS event_data
        FROM generate_series(1, 100) t(i)
    """)

    # 访问结构体字段
    result = con.execute("""
        SELECT
            event_id,
            customer_id,
            event_data.action,
            event_data.page
        FROM events
        LIMIT 10
    """).fetchdf()

    print("\n结构体访问示例:\n", result)
    return result


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("DuckDB SQL 扩展语法示例")
    print("=" * 60)

    con = duckdb.connect(":memory:")

    # 创建示例数据
    create_sample_data(con)

    # SAMPLE 子句
    sample_clause(con)

    # QUALIFY 子句
    qualify_clause(con)

    # PIVOT 语句
    pivot_statement(con)

    # LATERAL JOIN
    lateral_join(con)

    # 列表函数
    list_concat(con)

    # 结构体
    struct_and_nested(con)

    con.close()
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
