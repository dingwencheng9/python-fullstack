"""L50 练习 1: 参考答案 — 窗口函数分析。

将原始脚本重构为可测试函数。
"""

from __future__ import annotations

import duckdb
import numpy as np
import pandas as pd


def generate_sales_data(seed: int = 42) -> pd.DataFrame:
    """生成销售测试数据。

    Args:
        seed: 随机种子（默认 42，保证可复现）

    Returns:
        包含 date/region/amount 列的 DataFrame
    """
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "date": pd.date_range("2025-01-01", periods=50, freq="D"),
            "region": rng.choice(["A", "B", "C"], 50),
            "amount": rng.uniform(100, 1000, 50).round(2),
        }
    )


def compute_window_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """对销售数据执行窗口函数分析。

    计算：
    - cumulative: 按日期累计销售额
    - vs_avg: 与区域内均值的偏差
    - rank: 区域内按销售额降序排名

    Args:
        df: 包含 date/region/amount 列的销售数据

    Returns:
        添加 cumulative/vs_avg/rank 列的结果 DataFrame
    """
    conn = duckdb.connect()
    conn.register("sales", df)
    result = conn.execute("""
        SELECT date, region, amount,
               SUM(amount) OVER (ORDER BY date) AS cumulative,
               amount - AVG(amount) OVER (PARTITION BY region) AS vs_avg,
               RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS rank
        FROM sales
        ORDER BY date
    """).df()
    return result


def get_total_cumulative(result: pd.DataFrame) -> float:
    """获取累计总和（最后一行 cumulative 列的值）。

    Args:
        result: compute_window_metrics 的返回值

    Returns:
        累计销售总额
    """
    return float(result["cumulative"].iloc[-1])


# 保留可直接运行的入口（兼容原脚本体验）
if __name__ == "__main__":
    df = generate_sales_data()
    result = compute_window_metrics(df)
    print(result.head(10))
    print(f"\n累计总和: {get_total_cumulative(result):.2f}")
