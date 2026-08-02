"""L18 标准答案: 数据可视化仪表板"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class DataDashboard:
    """数据可视化仪表板 - 标准答案"""

    def __init__(self):
        self.fig = None
        sns.set_theme(style="whitegrid")

    def create_overview_dashboard(self, data: pd.DataFrame) -> None:
        """创建概览仪表板（2x2子图）"""
        self.fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        self.fig.suptitle("数据分析仪表板", fontsize=16, fontweight="bold")

        # 子图1: 折线图
        axes[0, 0].plot(data.index, data.iloc[:, 0], marker="o")
        axes[0, 0].set_title("时间序列趋势")
        axes[0, 0].set_xlabel("时间")
        axes[0, 0].set_ylabel("数值")
        axes[0, 0].grid(True, alpha=0.3)

        # 子图2: 柱状图
        axes[0, 1].bar(range(len(data.columns)), data.mean())
        axes[0, 1].set_title("各列均值对比")
        axes[0, 1].set_xticks(range(len(data.columns)))
        axes[0, 1].set_xticklabels(data.columns, rotation=45)

        # 子图3: 箱线图
        data.boxplot(ax=axes[1, 0])
        axes[1, 0].set_title("数值分布箱线图")
        axes[1, 0].set_ylabel("数值")

        # 子图4: 散点图
        axes[1, 1].scatter(data.iloc[:, 0], data.iloc[:, 1], alpha=0.6)
        axes[1, 1].set_title("变量相关性")
        axes[1, 1].set_xlabel(data.columns[0])
        axes[1, 1].set_ylabel(data.columns[1])

        plt.tight_layout()

    def create_time_series_chart(self, data: pd.DataFrame) -> None:
        """时间序列图表"""
        plt.figure(figsize=(12, 6))
        for col in data.columns:
            plt.plot(data.index, data[col], label=col, marker="o", markersize=3)
        plt.title("时间序列对比", fontsize=14)
        plt.xlabel("时间", fontsize=12)
        plt.ylabel("数值", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    def create_distribution_analysis(self, data: pd.DataFrame) -> None:
        """分布分析图"""
        plt.figure(figsize=(12, 6))
        for col in data.columns:
            sns.kdeplot(data[col], label=col, fill=True, alpha=0.3)
        plt.title("数据分布分析", fontsize=14)
        plt.xlabel("数值", fontsize=12)
        plt.ylabel("密度", fontsize=12)
        plt.legend()
        plt.tight_layout()

    def create_correlation_heatmap(self, data: pd.DataFrame) -> None:
        """相关性热力图"""
        plt.figure(figsize=(10, 8))
        sns.heatmap(data.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True, linewidths=1)
        plt.title("变量相关性热力图", fontsize=14)
        plt.tight_layout()

    def save_dashboard(self, filename: str) -> None:
        """保存仪表板"""
        if self.fig:
            self.fig.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"✅ 仪表板已保存: {filename}")


def main() -> None:
    print("🎨 L18 标准答案: 数据可视化仪表板\n")

    # 生成测试数据
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=100)
    data = pd.DataFrame(
        {
            "A": np.cumsum(np.random.randn(100)),
            "B": np.cumsum(np.random.randn(100)),
            "C": np.cumsum(np.random.randn(100)),
            "D": np.cumsum(np.random.randn(100)),
        },
        index=dates,
    )

    dashboard = DataDashboard()

    # 创建概览仪表板
    dashboard.create_overview_dashboard(data)
    print("✅ 概览仪表板创建成功")

    # 创建时间序列图
    dashboard.create_time_series_chart(data)
    print("✅ 时间序列图创建成功")

    # 创建分布分析
    dashboard.create_distribution_analysis(data)
    print("✅ 分布分析图创建成功")

    # 创建相关性热力图
    dashboard.create_correlation_heatmap(data)
    print("✅ 相关性热力图创建成功")


if __name__ == "__main__":
    main()
