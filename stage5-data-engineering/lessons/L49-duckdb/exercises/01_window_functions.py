"""

from __future__ import annotations

练习 1: 窗口函数分析

使用 DuckDB 窗口函数完成：

1. 按日期排序计算销售额的累计总和 (cumulative)
2. 计算每笔订单 vs 同品类的平均销售额差异
3. 为每个区域按销售额排名 (RANK)

import duckdb
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=50),
    "region": np.random.choice(["A", "B", "C"], 50),
    "amount": np.random.uniform(100, 1000, 50).round(2),
})

conn = duckdb.connect()
conn.register("sales", df)

# 你的 SQL
"""
