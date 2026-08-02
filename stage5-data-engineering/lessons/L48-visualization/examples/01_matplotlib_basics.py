"""L18 示例 1: Matplotlib 基础图表"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


class ChartBuilder:
    """基础图表构建器"""

    def create_line_chart(self, x: np.ndarray, y: np.ndarray, title: str = "折线图") -> None:
        """创建折线图"""
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker="o", linestyle="-", linewidth=2, markersize=8)
        plt.title(title, fontsize=14)
        plt.xlabel("X轴", fontsize=12)
        plt.ylabel("Y轴", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    def create_bar_chart(self, categories: list, values: list, title: str = "柱状图") -> None:
        """创建柱状图"""
        plt.figure(figsize=(10, 6))
        plt.bar(categories, values, color="steelblue", alpha=0.8)
        plt.title(title, fontsize=14)
        plt.xlabel("类别", fontsize=12)
        plt.ylabel("数值", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

    def create_scatter_chart(self, x: np.ndarray, y: np.ndarray, title: str = "散点图") -> None:
        """创建散点图"""
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, alpha=0.6, s=50, c="coral")
        plt.title(title, fontsize=14)
        plt.xlabel("X轴", fontsize=12)
        plt.ylabel("Y轴", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()


def main() -> None:
    print("🎨 L18 示例 1: Matplotlib 基础图表\n")

    builder = ChartBuilder()

    # 折线图
    x = np.linspace(0, 10, 50)
    y = np.sin(x)
    builder.create_line_chart(x, y, "正弦函数")
    print("✅ 折线图创建成功")

    # 柱状图
    categories = ["A", "B", "C", "D", "E"]
    values = [23, 45, 56, 78, 32]
    builder.create_bar_chart(categories, values, "销售数据")
    print("✅ 柱状图创建成功")

    # 散点图
    x = np.random.randn(100)
    y = 2 * x + np.random.randn(100)
    builder.create_scatter_chart(x, y, "相关性分析")
    print("✅ 散点图创建成功")


if __name__ == "__main__":
    main()
