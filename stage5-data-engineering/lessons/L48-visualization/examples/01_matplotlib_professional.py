"""

from __future__ import annotations

示例 1: Matplotlib核心技术 - 专业数据可视化

教学目标：
1. 掌握Matplotlib的核心组件（Figure, Axes）
2. 理解matplotlib的两种API风格
3. 掌握常用图表类型和定制化
4. 理解颜色、样式和布局系统

核心技术：
- Figure和Axes对象
- 面向对象API vs pyplot API
- 多子图布局（subplot, subplots）
- 样式定制（颜色、线型、标记）
- 中文字体配置

运行方式：
    python examples/01_matplotlib_professional.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# 第一部分：理解Matplotlib架构
# ============================================================================


def explain_matplotlib_architecture():
    """解释Matplotlib的核心架构

    核心概念：
    - Figure：整个画布（窗口）
    - Axes：单个图表区域（可以有多个）
    - Axis：坐标轴（X轴、Y轴）
    - Artist：所有可视化元素的基类

    两种API风格：
    1. pyplot API（便捷）：plt.plot(), plt.scatter()
    2. 面向对象API（推荐）：fig, ax = plt.subplots(); ax.plot()

    为什么推荐面向对象API？
    - 更明确的对象控制
    - 更容易管理多子图
    - 更适合复杂可视化
    """
    print("=" * 70)
    print("Part 1: Matplotlib架构详解")
    print("=" * 70)

    print("""
Matplotlib架构层次：

┌─────────────────────────────────────┐
│           Figure (画布)              │
│  ┌──────────────┐  ┌──────────────┐ │
│  │   Axes 1     │  │   Axes 2     │ │
│  │  (图表区域)   │  │  (图表区域)   │ │
│  │  ┌────────┐  │  │  ┌────────┐  │ │
│  │  │ Line   │  │  │  │ Scatter│  │ │
│  │  │ (线条)  │  │  │  │ (散点) │  │ │
│  │  └────────┘  │  │  └────────┘  │ │
│  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────┘

关键组件：
- Figure: 整个窗口/画布
- Axes: 单个图表（包含坐标轴、数据等）
- Axis: X轴、Y轴
- Artists: Line, Text, Patch等可视化元素
    """)


# ============================================================================
# 第二部分：基础图表类型
# ============================================================================


class BasicCharts:
    """基础图表类型"""

    @staticmethod
    def line_chart():
        """折线图 - 展示趋势"""
        print("\n示例1: 折线图（Line Chart）")

        # 准备数据
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)

        # 创建图表（面向对象API）
        fig, ax = plt.subplots(figsize=(10, 6))

        # 绘制两条线
        ax.plot(x, y1, label="sin(x)", color="blue", linewidth=2, linestyle="-")
        ax.plot(x, y2, label="cos(x)", color="red", linewidth=2, linestyle="--")

        # 定制化
        ax.set_title("三角函数对比", fontsize=14, fontweight="bold")
        ax.set_xlabel("X轴", fontsize=12)
        ax.set_ylabel("Y轴", fontsize=12)
        ax.legend(loc="upper right", fontsize=10)
        ax.grid(True, alpha=0.3, linestyle=":")

        # 添加水平线（参考线）
        ax.axhline(y=0, color="black", linestyle="-", linewidth=0.5)

        plt.tight_layout()
        print("  已创建: 折线图")
        plt.close()

    @staticmethod
    def scatter_plot():
        """散点图 - 展示分布和相关性"""
        print("\n示例2: 散点图（Scatter Plot）")

        # 准备数据（模拟两个变量的关系）
        np.random.seed(42)
        n = 100
        x = np.random.randn(n)
        y = 2 * x + 1 + np.random.randn(n) * 0.5  # y = 2x + 1 + noise
        colors = np.random.rand(n)  # 颜色映射
        sizes = np.random.rand(n) * 100 + 20  # 大小变化

        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 6))

        # 散点图（带颜色和大小映射）
        scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap="viridis", edgecolors="black", linewidth=0.5)

        # 添加趋势线
        z = np.polyfit(x, y, 1)  # 线性拟合
        p = np.poly1d(z)
        ax.plot(x, p(x), "r--", alpha=0.8, linewidth=2, label=f"趋势线: y={z[0]:.2f}x+{z[1]:.2f}")

        # 定制化
        ax.set_title("散点图：变量关系分析", fontsize=14)
        ax.set_xlabel("变量 X", fontsize=12)
        ax.set_ylabel("变量 Y", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 添加颜色条
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label("颜色映射值", fontsize=10)

        plt.tight_layout()
        print("  已创建: 散点图")
        plt.close()

    @staticmethod
    def bar_chart():
        """柱状图 - 展示分类数据"""
        print("\n示例3: 柱状图（Bar Chart）")

        # 准备数据
        categories = ["A", "B", "C", "D", "E"]
        values = [23, 45, 56, 78, 32]

        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 6))

        # 柱状图（带渐变颜色）
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(categories)))
        bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor="black")

        # 在柱子上添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.0f}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        # 定制化
        ax.set_title("分类数据对比", fontsize=14)
        ax.set_xlabel("类别", fontsize=12)
        ax.set_ylabel("数值", fontsize=12)
        ax.set_ylim(0, max(values) * 1.1)  # 留出空间显示标签
        ax.grid(axis="y", alpha=0.3, linestyle="--")

        plt.tight_layout()
        print("  已创建: 柱状图")
        plt.close()

    @staticmethod
    def histogram():
        """直方图 - 展示分布"""
        print("\n示例4: 直方图（Histogram）")

        # 准备数据（正态分布）
        np.random.seed(42)
        data = np.random.randn(1000)

        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 6))

        # 直方图
        n, bins, patches = ax.hist(data, bins=30, color="steelblue", alpha=0.7, edgecolor="black")

        # 添加正态分布曲线
        mu, sigma = data.mean(), data.std()
        x = np.linspace(data.min(), data.max(), 100)
        y = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (x - mu)) ** 2)
        # 缩放到直方图的尺度
        y = y * len(data) * (bins[1] - bins[0])
        ax.plot(x, y, "r--", linewidth=2, label=f"正态分布 (μ={mu:.2f}, σ={sigma:.2f})")

        # 定制化
        ax.set_title("数据分布直方图", fontsize=14)
        ax.set_xlabel("数值", fontsize=12)
        ax.set_ylabel("频数", fontsize=12)
        ax.legend()
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        print("  已创建: 直方图")
        plt.close()


# ============================================================================
# 第三部分：高级布局技术
# ============================================================================


def advanced_layouts():
    """高级布局技术"""
    print("\n" + "=" * 70)
    print("Part 2: 高级布局技术")
    print("=" * 70)

    # 1. 多子图网格
    print("\n布局1: 2x2网格")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 左上：折线图
    x = np.linspace(0, 10, 100)
    axes[0, 0].plot(x, np.sin(x), "b-")
    axes[0, 0].set_title("折线图")
    axes[0, 0].grid(True, alpha=0.3)

    # 右上：散点图
    axes[0, 1].scatter(np.random.randn(50), np.random.randn(50), alpha=0.6)
    axes[0, 1].set_title("散点图")
    axes[0, 1].grid(True, alpha=0.3)

    # 左下：柱状图
    axes[1, 0].bar(["A", "B", "C"], [1, 2, 3], color="steelblue")
    axes[1, 0].set_title("柱状图")
    axes[1, 0].grid(axis="y", alpha=0.3)

    # 右下：直方图
    axes[1, 1].hist(np.random.randn(1000), bins=30, color="coral", alpha=0.7)
    axes[1, 1].set_title("直方图")
    axes[1, 1].grid(axis="y", alpha=0.3)

    plt.tight_layout()
    print("  已创建: 2x2网格布局")
    plt.close()

    # 2. 不规则布局
    print("\n布局2: 不规则布局（GridSpec）")
    fig = plt.figure(figsize=(12, 8))
    from matplotlib import gridspec

    gs = gridspec.GridSpec(3, 3, figure=fig)

    # 大图（占2x2）
    ax1 = fig.add_subplot(gs[0:2, 0:2])
    ax1.plot(np.random.randn(100).cumsum())
    ax1.set_title("主图（大）", fontsize=14)

    # 小图1（右上）
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.bar(["A", "B"], [1, 2])
    ax2.set_title("辅助图1")

    # 小图2（右中）
    ax3 = fig.add_subplot(gs[1, 2])
    ax3.scatter(np.random.randn(30), np.random.randn(30))
    ax3.set_title("辅助图2")

    # 底部横向图
    ax4 = fig.add_subplot(gs[2, :])
    ax4.hist(np.random.randn(1000), bins=50, alpha=0.7)
    ax4.set_title("分布图（宽）")

    plt.tight_layout()
    print("  已创建: 不规则布局")
    plt.close()


# ============================================================================
# 第四部分：样式定制
# ============================================================================


def style_customization():
    """样式定制技术"""
    print("\n" + "=" * 70)
    print("Part 3: 样式定制")
    print("=" * 70)

    # 1. 颜色系统
    print("\n定制1: 颜色系统")
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.linspace(0, 10, 100)

    # 不同颜色表示方式
    ax.plot(x, np.sin(x), color="blue", label="命名颜色: blue")
    ax.plot(x, np.sin(x - 1), color="#FF5733", label="十六进制: #FF5733")
    ax.plot(x, np.sin(x - 2), color=(0.2, 0.8, 0.3), label="RGB元组: (0.2, 0.8, 0.3)")
    ax.plot(x, np.sin(x - 3), color="C4", label="默认调色板: C4")

    ax.set_title("Matplotlib颜色系统", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    print("  已创建: 颜色系统示例")
    plt.close()

    # 2. 线型和标记
    print("\n定制2: 线型和标记")
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.linspace(0, 10, 20)

    # 不同线型和标记
    ax.plot(x, x, "-", label="实线 -")
    ax.plot(x, x + 1, "--", label="虚线 --")
    ax.plot(x, x + 2, "-.", label="点划线 -.")
    ax.plot(x, x + 3, ":", label="点线 :")
    ax.plot(x, x + 4, "o-", label="圆形标记 o-")
    ax.plot(x, x + 5, "s--", label="方形标记 s--")
    ax.plot(x, x + 6, "^:", label="三角标记 ^:")

    ax.set_title("线型和标记样式", fontsize=14)
    ax.legend(ncol=2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    print("  已创建: 线型和标记示例")
    plt.close()

    # 3. 使用样式表
    print("\n定制3: 内置样式表")
    print(f"  可用样式: {len(plt.style.available)} 个")
    print("  推荐样式: seaborn-v0_8, ggplot, bmh, fivethirtyeight")

    # 使用seaborn样式
    with plt.style.context("seaborn-v0_8"):
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.linspace(0, 10, 100)
        for i in range(5):
            ax.plot(x, np.sin(x + i), label=f"线条 {i + 1}")
        ax.set_title("Seaborn样式", fontsize=14)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        print("  已创建: Seaborn样式示例")
        plt.close()


# ============================================================================
# 第五部分：完整演示
# ============================================================================


def main():
    """主演示函数"""

    # Part 1: 架构讲解
    explain_matplotlib_architecture()

    # Part 2: 基础图表
    print("\n" + "=" * 70)
    print("Part 2: 基础图表类型")
    print("=" * 70)

    charts = BasicCharts()
    charts.line_chart()
    charts.scatter_plot()
    charts.bar_chart()
    charts.histogram()

    # Part 3: 高级布局
    advanced_layouts()

    # Part 4: 样式定制
    style_customization()

    # 总结
    print("\n" + "=" * 70)
    print("关键要点总结")
    print("=" * 70)

    print("""
1. Matplotlib架构：
   - Figure: 整个画布
   - Axes: 图表区域（推荐面向对象API）
   - Artists: 可视化元素

2. 基础图表：
   - 折线图: 趋势分析
   - 散点图: 相关性
   - 柱状图: 分类对比
   - 直方图: 分布展示

3. 布局技术：
   - plt.subplots(m, n): 规则网格
   - GridSpec: 不规则布局
   - tight_layout(): 自动调整

4. 样式定制：
   - 颜色: 命名/十六进制/RGB
   - 线型: -, --, -., :
   - 标记: o, s, ^, v
   - 样式表: plt.style.use()

5. 最佳实践：
   ✅ 使用面向对象API（fig, ax）
   ✅ 添加标题、标签、图例
   ✅ 使用grid提升可读性
   ✅ tight_layout避免重叠
   ❌ 避免过度装饰
   ❌ 避免3D图表（难以解读）
    """)


if __name__ == "__main__":
    main()
    print("\n✅ 示例演示完成")
