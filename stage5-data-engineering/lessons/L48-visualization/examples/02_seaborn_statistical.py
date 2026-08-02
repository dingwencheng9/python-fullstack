"""

from __future__ import annotations

示例 2: Seaborn统计可视化 - 高级数据探索

教学目标：
1. 掌握Seaborn的核心特性
2. 理解统计图表的应用场景
3. 掌握多变量关系可视化
4. 理解FacetGrid和PairGrid

核心技术：
- 分布图（distplot, histplot, kdeplot）
- 分类图（boxplot, violinplot, swarmplot）
- 关系图（scatterplot, lineplot, regplot）
- 矩阵图（heatmap, clustermap）
- 多面板图（FacetGrid, PairGrid）

运行方式：
    python examples/02_seaborn_statistical.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ============================================================================
# 第一部分：理解Seaborn的设计理念
# ============================================================================


def explain_seaborn_philosophy():
    """解释Seaborn的设计理念

    Seaborn vs Matplotlib：
    - Matplotlib: 低级API，完全控制
    - Seaborn: 高级API，统计导向

    Seaborn优势：
    1. 默认样式更美观
    2. 自动计算统计量
    3. 支持DataFrame直接绘图
    4. 内置主题和调色板
    5. 专注于统计可视化

    核心理念：
    - 数据驱动（DataFrame优先）
    - 统计为中心
    - 美学优先
    """
    print("=" * 70)
    print("Part 1: Seaborn设计理念")
    print("=" * 70)

    print("""
Seaborn的三层架构：

1. 底层：Matplotlib
   - 提供绘图能力
   - 完全兼容

2. 中层：Seaborn核心
   - 统计计算
   - 美学优化
   - DataFrame集成

3. 高层：主题系统
   - 调色板
   - 样式主题
   - 上下文切换

Seaborn适用场景：
✅ 统计分析可视化
✅ 探索性数据分析（EDA）
✅ 快速生成美观图表
✅ 多变量关系展示
❌ 高度定制化（用Matplotlib）
❌ 实时更新图表
    """)


# ============================================================================
# 第二部分：分布可视化
# ============================================================================


class DistributionPlots:
    """分布可视化"""

    @staticmethod
    def histogram_and_kde():
        """直方图 + 核密度估计"""
        print("\n示例1: 直方图 + KDE")

        # 准备数据
        np.random.seed(42)
        data = np.random.randn(1000)

        # 创建图表
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # 1. 纯直方图
        sns.histplot(data, bins=30, ax=axes[0], color="steelblue")
        axes[0].set_title("直方图", fontsize=14)

        # 2. 直方图 + KDE
        sns.histplot(data, bins=30, kde=True, ax=axes[1], color="coral")
        axes[1].set_title("直方图 + KDE", fontsize=14)

        # 3. 纯KDE
        sns.kdeplot(data, ax=axes[2], fill=True, color="mediumseagreen")
        axes[2].set_title("核密度估计（KDE）", fontsize=14)

        plt.tight_layout()
        print("  已创建: 分布图对比")
        plt.close()

    @staticmethod
    def multiple_distributions():
        """多个分布对比"""
        print("\n示例2: 多分布对比")

        # 准备数据（三个不同分布）
        np.random.seed(42)
        group_a = np.random.normal(0, 1, 500)
        group_b = np.random.normal(2, 1.5, 500)
        group_c = np.random.normal(-1, 0.8, 500)

        df = pd.DataFrame(
            {
                "value": np.concatenate([group_a, group_b, group_c]),
                "group": ["A"] * 500 + ["B"] * 500 + ["C"] * 500,
            }
        )

        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # 1. 重叠直方图
        sns.histplot(data=df, x="value", hue="group", bins=40, alpha=0.6, ax=axes[0, 0])
        axes[0, 0].set_title("重叠直方图", fontsize=14)

        # 2. 重叠KDE
        sns.kdeplot(data=df, x="value", hue="group", fill=True, alpha=0.5, ax=axes[0, 1])
        axes[0, 1].set_title("重叠KDE", fontsize=14)

        # 3. 箱线图
        sns.boxplot(data=df, x="group", y="value", ax=axes[1, 0])
        axes[1, 0].set_title("箱线图", fontsize=14)

        # 4. 小提琴图
        sns.violinplot(data=df, x="group", y="value", ax=axes[1, 1])
        axes[1, 1].set_title("小提琴图", fontsize=14)

        plt.tight_layout()
        print("  已创建: 多分布对比")
        plt.close()


# ============================================================================
# 第三部分：分类数据可视化
# ============================================================================


class CategoricalPlots:
    """分类数据可视化"""

    @staticmethod
    def create_sample_data():
        """创建示例数据（模拟tips数据集）"""
        np.random.seed(42)
        n = 200

        df = pd.DataFrame(
            {
                "total_bill": np.random.gamma(2, 10, n),
                "tip": np.random.gamma(1.5, 2, n),
                "sex": np.random.choice(["Male", "Female"], n),
                "day": np.random.choice(["Thur", "Fri", "Sat", "Sun"], n),
                "time": np.random.choice(["Lunch", "Dinner"], n),
                "size": np.random.choice([2, 3, 4, 5], n),
            }
        )

        return df

    @staticmethod
    def box_violin_strip():
        """箱线图、小提琴图、散点图对比"""
        print("\n示例3: 分类图表对比")

        # 准备数据
        tips = CategoricalPlots.create_sample_data()

        # 创建图表
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))

        # 1. 箱线图（显示四分位数）
        sns.boxplot(data=tips, x="day", y="total_bill", ax=axes[0])
        axes[0].set_title("箱线图：显示分位数", fontsize=14)
        axes[0].set_ylabel("账单金额", fontsize=12)

        # 2. 小提琴图（显示分布形状）
        sns.violinplot(data=tips, x="day", y="total_bill", ax=axes[1])
        axes[1].set_title("小提琴图：显示分布", fontsize=14)
        axes[1].set_ylabel("账单金额", fontsize=12)

        # 3. 条形散点图
        sns.stripplot(data=tips, x="day", y="total_bill", ax=axes[2], size=3, alpha=0.5)
        axes[2].set_title("散点图：显示原始数据", fontsize=14)
        axes[2].set_ylabel("账单金额", fontsize=12)

        plt.tight_layout()
        print("  已创建: 分类图表对比")
        plt.close()


# ============================================================================
# 第四部分：关系可视化
# ============================================================================


class RelationalPlots:
    """关系可视化"""

    @staticmethod
    def scatter_regression():
        """散点图 + 回归线"""
        print("\n示例4: 散点图 + 回归")

        # 准备数据
        np.random.seed(42)
        n = 100
        x = np.random.randn(n)
        y = 2 * x + 1 + np.random.randn(n) * 0.5

        df = pd.DataFrame({"x": x, "y": y})

        # 创建图表
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # 1. 散点图
        sns.scatterplot(data=df, x="x", y="y", alpha=0.7, ax=axes[0])
        axes[0].set_title("散点图", fontsize=14)

        # 2. 回归图（拟合线 + 置信区间）
        sns.regplot(data=df, x="x", y="y", scatter_kws={"alpha": 0.5}, ax=axes[1])
        axes[1].set_title("回归图：线性拟合", fontsize=14)

        plt.tight_layout()
        print("  已创建: 散点图和回归图")
        plt.close()


# ============================================================================
# 第五部分：矩阵可视化
# ============================================================================


class MatrixPlots:
    """矩阵可视化"""

    @staticmethod
    def correlation_heatmap():
        """相关系数热力图"""
        print("\n示例5: 相关系数热力图")

        # 准备数据
        np.random.seed(42)
        data = np.random.randn(10, 8)
        df = pd.DataFrame(data, columns=[f"特征{i + 1}" for i in range(8)])

        # 计算相关系数
        corr = df.corr()

        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 8))

        # 热力图
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax, cbar_kws={"shrink": 0.8})
        ax.set_title("相关系数热力图", fontsize=14)

        plt.tight_layout()
        print("  已创建: 热力图")
        plt.close()


# ============================================================================
# 第六部分：完整演示
# ============================================================================


def main():
    """主演示函数"""

    # Part 1: 设计理念
    explain_seaborn_philosophy()

    # Part 2: 分布可视化
    print("\n" + "=" * 70)
    print("Part 2: 分布可视化")
    print("=" * 70)

    dist = DistributionPlots()
    dist.histogram_and_kde()
    dist.multiple_distributions()

    # Part 3: 分类可视化
    print("\n" + "=" * 70)
    print("Part 3: 分类数据可视化")
    print("=" * 70)

    cat = CategoricalPlots()
    cat.box_violin_strip()

    # Part 4: 关系可视化
    print("\n" + "=" * 70)
    print("Part 4: 关系可视化")
    print("=" * 70)

    rel = RelationalPlots()
    rel.scatter_regression()

    # Part 5: 矩阵可视化
    print("\n" + "=" * 70)
    print("Part 5: 矩阵可视化")
    print("=" * 70)

    matrix = MatrixPlots()
    matrix.correlation_heatmap()

    # 总结
    print("\n" + "=" * 70)
    print("关键要点总结")
    print("=" * 70)

    print("""
1. Seaborn核心优势：
   - 统计导向
   - DataFrame集成
   - 默认美观
   - 自动计算统计量

2. 分布可视化：
   - histplot: 直方图
   - kdeplot: 核密度估计
   - boxplot: 箱线图（四分位数）
   - violinplot: 小提琴图（分布形状）

3. 分类可视化：
   - barplot: 均值 + 置信区间
   - countplot: 频数统计
   - stripplot: 散点（避免重叠）

4. 关系可视化：
   - scatterplot: 散点图
   - regplot: 回归图（拟合线）
   - lineplot: 折线图（时间序列）

5. 矩阵可视化：
   - heatmap: 热力图
   - clustermap: 聚类热力图

6. 最佳实践：
   ✅ 使用DataFrame作为数据源
   ✅ 利用hue/size进行多变量映射
   ✅ 选择合适的调色板
   ✅ 添加标题和标签
   ❌ 避免过多颜色
   ❌ 避免3D图表
    """)


if __name__ == "__main__":
    main()
    print("\n✅ 示例演示完成")
