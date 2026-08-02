"""

from __future__ import annotations

练习 2: Pandas + DuckDB 混合工作流

1. 用 Pandas 读取和清洗数据
2. 用 DuckDB SQL 进行聚合分析
3. 将结果传回 Pandas 做可视化

import pandas as pd
import numpy as np
import duckdb

# 模拟数据
np.random.seed(42)
raw = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=365),
    "product": np.random.choice(["A", "B", "C"], 365),
    "sales": np.random.uniform(0, 1000, 365).round(2),
})

# 1. Pandas 清洗: 过滤掉 sales=0 的行

# 2. DuckDB 聚合: 按月统计销售额

# 3. 结果转为 Pandas
"""
