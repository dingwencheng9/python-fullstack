"""L50 练习 2: 参考答案 — Pandas + DuckDB 混合工作流。

将原始脚本重构为可测试函数。
"""

from __future__ import annotations

import duckdb
import numpy as np
import pandas as pd


def generate_raw_data(seed: int = 42) -> pd.DataFrame:
    """生成原始销售数据。

    Args:
        seed: 随机种子（默认 42）

    Returns:
        包含 date/product/sales 列的 DataFrame（含零值/负值，模拟脏数据）
    """
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "date": pd.date_range("2025-01-01", periods=365, freq="D"),
            "product": rng.choice(["A", "B", "C"], 365),
            "sales": rng.uniform(0, 1000, 365).round(2),
        }
    )


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Pandas 数据清洗：过滤无效行 + 添加月份列。

    Args:
        df: 原始销售数据

    Returns:
        清洗后的 DataFrame（sales > 0，含 month 列）
    """
    cleaned = df[df["sales"] > 0].copy()
    cleaned["month"] = cleaned["date"].dt.month
    return cleaned


def aggregate_monthly(cleaned: pd.DataFrame) -> pd.DataFrame:
    """DuckDB 按月+产品维度聚合。

    Args:
        cleaned: clean_data 的返回值

    Returns:
        包含 month/product/orders/revenue 的聚合结果
    """
    conn = duckdb.connect()
    conn.register("data", cleaned)
    return conn.execute("""
        SELECT month, product,
               COUNT(*) AS orders,
               SUM(sales) AS revenue
        FROM data
        GROUP BY month, product
        ORDER BY month, product
    """).df()


def to_pivot_table(aggregated: pd.DataFrame) -> pd.DataFrame:
    """将聚合结果透视：month 为行，product 为列。

    Args:
        aggregated: aggregate_monthly 的返回值

    Returns:
        透视后的 DataFrame（shape = [12, 3]）
    """
    return aggregated.pivot_table(index="month", columns="product", values="revenue", aggfunc="sum").fillna(0).astype(int)


def run_full_pipeline(seed: int = 42) -> pd.DataFrame:
    """运行完整 Pandas → DuckDB → Pandas 混合工作流。

    1. Pandas 清洗
    2. DuckDB 聚合
    3. Pandas 透视

    Args:
        seed: 随机种子

    Returns:
        透视后的月度产品收入表
    """
    raw = generate_raw_data(seed)
    cleaned = clean_data(raw)
    aggregated = aggregate_monthly(cleaned)
    return to_pivot_table(aggregated)


# 保留可直接运行的入口（兼容原脚本体验）
if __name__ == "__main__":
    pivot = run_full_pipeline()
    print(pivot)
