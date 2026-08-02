"""可视化模块。"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    import pandas as pd


def plot_source_counts(summary: pd.DataFrame, output: str | Path) -> Path:
    """按来源绘制页面数量柱状图。"""
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    ax = summary.plot.bar(x="source", y="pages", legend=False, figsize=(8, 4))
    ax.set_title("Pages by Source")
    ax.set_xlabel("Source")
    ax.set_ylabel("Pages")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
