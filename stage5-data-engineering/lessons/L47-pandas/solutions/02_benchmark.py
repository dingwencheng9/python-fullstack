"""L48 练习2 参考：性能基准"""

from __future__ import annotations

import pandas as pd


def measure_sum(df: pd.DataFrame) -> float:
    """测试 DataFrame 列求和性能"""
    import time

    start = time.time()
    df["value"].sum()
    elapsed = time.time() - start
    return elapsed
