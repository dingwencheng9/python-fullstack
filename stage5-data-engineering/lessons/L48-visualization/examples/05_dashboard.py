"""L49 示例 5: 简单仪表盘 (4 图布局)"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_dashboard(df: pd.DataFrame) -> None:
    """创建 2×2 仪表盘"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    numeric = df.select_dtypes(include=[np.number])

    # 左上: 直方图
    numeric.hist(ax=axes[0, 0], bins=30, alpha=0.7)
    axes[0, 0].set_title("数值分布")

    # 右上: 相关性热力图
    im = axes[0, 1].imshow(numeric.corr(), cmap="RdBu_r")
    axes[0, 1].set_title("相关性矩阵")
    fig.colorbar(im, ax=axes[0, 1])

    # 左下: 箱线图
    numeric.plot.box(ax=axes[1, 0])
    axes[1, 0].set_title("箱线图")
    axes[1, 0].tick_params(axis="x", rotation=45)

    # 右下: 散点矩阵前2列
    cols = numeric.columns[:2]
    axes[1, 1].scatter(numeric[cols[0]], numeric[cols[1]], alpha=0.5)
    axes[1, 1].set_xlabel(cols[0])
    axes[1, 1].set_ylabel(cols[1])
    axes[1, 1].set_title(f"{cols[0]} vs {cols[1]}")

    plt.tight_layout()
    plt.show()
