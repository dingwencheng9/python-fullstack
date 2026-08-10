"""
L48 数据可视化 - 基准测试

测试维度:
1. 模块导入健康测试
2. 核心可视化逻辑测试
3. 异常边界测试

依赖处理:
- matplotlib/seaborn/plotly 通过 conftest.py 全局导入
- 如需跳过某个测试，使用 pytest.mark.skipif
"""

from __future__ import annotations

import matplotlib  # 确保 matplotlib 已安装
import pytest
import numpy as np
import pandas as pd

# 统一固定随机源，避免测试间相互污染
_RNG = np.random.default_rng(42)

# ============================================================================
# 测试维度 1: 模块导入健康测试
# ============================================================================

# ============================================================================
# 测试维度 1: 模块导入健康测试
# ============================================================================


def test_import_matplotlib():
    """测试 Matplotlib 导入并具备核心 API。"""
    import matplotlib
    import matplotlib.pyplot as plt

    assert hasattr(matplotlib, "__version__")
    assert callable(plt.subplots)
    assert callable(plt.close)


def test_import_seaborn():
    """测试 Seaborn 导入并具备核心 API。"""
    sns = pytest.importorskip("seaborn")
    assert callable(sns.scatterplot)
    assert hasattr(sns, "__version__")


def test_import_plotly():
    """测试 Plotly 导入并具备核心 API。"""
    px = pytest.importorskip("plotly.express")
    go = pytest.importorskip("plotly.graph_objects")
    assert callable(px.scatter)
    assert hasattr(go, "Figure")


# ============================================================================
# 测试维度 2: 核心可视化逻辑测试
# ============================================================================


def test_matplotlib_figure_creation():
    """测试 Matplotlib Figure 创建并可关闭。"""
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    fig, ax = plt.subplots()

    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)
    assert fig.number in plt.get_fignums()

    plt.close(fig)
    assert fig.number not in plt.get_fignums()


def test_matplotlib_line_plot():
    """测试 Matplotlib 折线图：xdata 与 ydata 与输入一致。"""
    import matplotlib.pyplot as plt

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, ax = plt.subplots()
    (line,) = ax.plot(x, y)

    assert len(line.get_xdata()) == 100
    assert np.allclose(line.get_xdata(), x)
    assert np.allclose(line.get_ydata(), y)

    plt.close(fig)


def test_matplotlib_scatter_plot():
    """测试 Matplotlib 散点图"""
    import matplotlib.pyplot as plt

    x = _RNG.standard_normal(50)
    y = _RNG.standard_normal(50)

    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y)

    offsets = scatter.get_offsets()
    assert offsets.shape == (50, 2)
    assert np.allclose(offsets[:, 0], x)
    assert np.allclose(offsets[:, 1], y)

    plt.close(fig)


def test_matplotlib_bar_chart():
    """测试 Matplotlib 柱状图"""
    import matplotlib.pyplot as plt

    categories = ["A", "B", "C", "D"]
    values = [23, 45, 56, 78]

    fig, ax = plt.subplots()
    bars = ax.bar(categories, values)

    assert len(bars) == 4

    plt.close(fig)


def test_matplotlib_histogram():
    """测试 Matplotlib 直方图"""
    import matplotlib.pyplot as plt

    data = _RNG.standard_normal(1000)

    fig, ax = plt.subplots()
    n, bins, _patches = ax.hist(data, bins=30)

    assert len(n) == 30
    assert len(bins) == 31
    assert int(n.sum()) == 1000  # 所有样本被分桶

    plt.close(fig)


def test_matplotlib_subplots():
    """测试 Matplotlib 子图"""
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    assert axes.shape == (2, 2)

    # 在每个子图上绘制
    for i, ax in enumerate(axes.flat):
        ax.plot([1, 2, 3], [1, 2, 3])
        ax.set_title(f"Subplot {i + 1}")

    plt.close(fig)


def test_matplotlib_customization():
    """测试 Matplotlib 自定义"""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])

    # 自定义标题和标签
    ax.set_title("Test Plot")
    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")

    assert ax.get_title() == "Test Plot"
    assert ax.get_xlabel() == "X Label"
    assert ax.get_ylabel() == "Y Label"

    plt.close(fig)


def test_seaborn_basic_plot():
    """测试 Seaborn 基础图表：能产生可识别的散点 PathCollection。"""
    sns = pytest.importorskip("seaborn")
    pd = pytest.importorskip("pandas")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PathCollection

    df = pd.DataFrame(
        {
            "x": _RNG.standard_normal(100),
            "y": _RNG.standard_normal(100),
            "category": _RNG.choice(["A", "B"], 100),
        }
    )

    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="x", y="y", hue="category", ax=ax)

    collections = [c for c in ax.collections if isinstance(c, PathCollection)]
    assert collections, "Seaborn scatterplot 应创建 PathCollection"
    total_points = sum(len(c.get_offsets()) for c in collections)
    assert total_points == 100

    plt.close(fig)


# ============================================================================
# 测试维度 3: 异常边界测试
# ============================================================================


def test_empty_data_plot():
    """测试空数据绘图"""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # 空数据
    x = []
    y = []

    # 应该不报错，只是不显示数据
    ax.plot(x, y)

    plt.close(fig)


def test_mismatched_data_lengths():
    """测试数据长度不匹配"""
    import matplotlib.pyplot as plt

    x = [1, 2, 3]
    y = [1, 2]  # 长度不匹配

    fig, ax = plt.subplots()

    # 应该抛出异常
    with pytest.raises(ValueError):
        ax.plot(x, y)

    plt.close(fig)


def test_invalid_data_types():
    """字符串 x 轴会被 matplotlib 当作分类轴 — 验证它真的画进去了。"""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    (line,) = ax.plot(["a", "b", "c"], [1, 2, 3])

    assert len(line.get_xdata()) == 3
    assert list(line.get_ydata()) == [1, 2, 3]

    plt.close(fig)


def test_nan_in_data():
    """测试数据中的 NaN"""
    import matplotlib.pyplot as plt

    x = [1, 2, np.nan, 4, 5]
    y = [1, 2, 3, 4, 5]

    fig, ax = plt.subplots()

    # Matplotlib 应该能处理 NaN（跳过或显示断点）
    ax.plot(x, y)

    plt.close(fig)


def test_infinite_values():
    """测试无穷大值"""
    import matplotlib.pyplot as plt

    x = [1, 2, 3, 4, 5]
    y = [1, np.inf, 3, -np.inf, 5]

    fig, ax = plt.subplots()

    # 应该能绘制，但无穷大值可能不可见
    ax.plot(x, y)

    plt.close(fig)


def test_figure_memory_leak():
    """测试 Figure 内存泄漏"""
    import matplotlib.pyplot as plt

    # 先关闭所有现有的 figure
    plt.close("all")

    # 创建多个 figure
    for _ in range(10):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 2, 3])
        plt.close(fig)  # 确保关闭

    # 应该不会有内存泄漏
    # 检查打开的 figure 数量
    assert len(plt.get_fignums()) == 0


def test_invalid_color():
    """测试无效颜色"""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # 无效颜色应该报错
    with pytest.raises((ValueError, AttributeError)):
        ax.plot([1, 2, 3], [1, 2, 3], color="invalid_color")

    plt.close(fig)


# ============================================================================
# 集成测试
# ============================================================================


def test_multi_plot_dashboard():
    """测试多图表仪表板"""
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(12, 8))

    # 创建网格布局
    ax1 = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(2, 2, 2)
    ax3 = plt.subplot(2, 2, 3)
    ax4 = plt.subplot(2, 2, 4)

    # 不同类型的图表
    ax1.plot([1, 2, 3], [1, 4, 9])
    ax2.scatter(_RNG.standard_normal(50), _RNG.standard_normal(50))
    ax3.bar(["A", "B", "C"], [10, 20, 15])
    ax4.hist(_RNG.standard_normal(1000), bins=20)

    plt.tight_layout()
    plt.close(fig)


def test_style_customization():
    """测试样式自定义"""
    import matplotlib.pyplot as plt

    # 使用内置样式
    available_styles = plt.style.available

    if "ggplot" in available_styles:
        with plt.style.context("ggplot"):
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [1, 2, 3])
            plt.close(fig)


def test_colormap_usage():
    """测试色图使用"""
    import matplotlib.pyplot as plt

    x = _RNG.standard_normal(100)
    y = _RNG.standard_normal(100)
    colors = _RNG.standard_normal(100)

    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y, c=colors, cmap="viridis")

    # 添加颜色条
    fig.colorbar(scatter, ax=ax)

    plt.close(fig)


def test_data_visualization_pipeline():
    """测试完整数据可视化流程"""
    import matplotlib.pyplot as plt
    import pandas as pd

    # 准备数据
    df = pd.DataFrame(
        {
            "x": _RNG.standard_normal(100),
            "y": _RNG.standard_normal(100),
            "category": _RNG.choice(["A", "B", "C"], 100),
            "size": _RNG.integers(10, 100, 100),
        }
    )

    # 创建可视化
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 散点图
    for category in df["category"].unique():
        mask = df["category"] == category
        axes[0].scatter(df.loc[mask, "x"], df.loc[mask, "y"], label=category, alpha=0.6)
    axes[0].legend()
    axes[0].set_title("Scatter by Category")

    # 柱状图
    category_counts = df["category"].value_counts()
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Category Counts")

    plt.tight_layout()
    plt.close(fig)


# ============================================================================
# 性能测试
# ============================================================================


def test_large_dataset_plot():
    """测试大数据集绘图"""
    import time

    import matplotlib.pyplot as plt

    # 大数据集
    x = _RNG.standard_normal(100000)
    y = _RNG.standard_normal(100000)

    fig, ax = plt.subplots()

    start = time.time()
    ax.scatter(x, y, alpha=0.1, s=1)
    elapsed = time.time() - start

    # 应该在合理时间内完成
    assert elapsed < 5.0

    plt.close(fig)


def test_multiple_figures_performance():
    """测试多 Figure 性能"""
    import time

    import matplotlib.pyplot as plt

    start = time.time()

    # 创建多个 figure
    for _ in range(20):
        fig, ax = plt.subplots()
        ax.plot(_RNG.standard_normal(100))
        plt.close(fig)

    elapsed = time.time() - start

    # 应该很快
    assert elapsed < 2.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

# ============================================================================
# 测试维度 4: 课程 solutions 函数（DataDashboard）
# ============================================================================


class TestDataDashboardFunctionality:
    """测试 DataDashboard 类的核心方法返回值与边界行为。"""

    @pytest.fixture(autouse=True)
    def _setup(self, solutions, request) -> None:
        """注入 solution 模块 + 生成测试数据。

        通过 importlib spec 加载 solutions 包，处理 seaborn 等
        可选依赖未安装时的跳过逻辑。
        """
        import importlib.util
        from pathlib import Path

        solution_dir = Path(__file__).resolve().parent.parent / "solutions"
        target = solution_dir / "project_data_dashboard.py"
        spec = importlib.util.spec_from_file_location("_test_L49_dashboard", target)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except ModuleNotFoundError:
            pytest.skip("seaborn 等可选依赖未安装")
        request.cls.DataDashboard = module.DataDashboard
        np.random.seed(42)
        dates = pd.date_range("2024-01-01", periods=50, freq="D")
        self.data = pd.DataFrame(
            {
                "revenue": np.cumsum(np.random.randn(50)) + 100,
                "users": np.cumsum(np.random.randn(50)) + 50,
                "cost": np.cumsum(np.random.randn(50)) + 30,
            },
            index=dates,
        )

    def test_dashboard_creation_returns_axes(self) -> None:
        """create_overview_dashboard 应创建 2×2 子图。"""
        dashboard = self.DataDashboard()
        dashboard.create_overview_dashboard(self.data)

        assert dashboard.fig is not None
        axes = dashboard.fig.axes
        assert len(axes) == 4, "2×2 子图应返回 4 个 Axes"

        plt.close(dashboard.fig)

    def test_correlation_heatmap_creates_figure(self) -> None:
        """create_correlation_heatmap 应创建包含热力图的 Figure。"""
        dashboard = self.DataDashboard()
        dashboard.create_correlation_heatmap(self.data)

        assert len(plt.get_fignums()) >= 1

        plt.close("all")

    def test_save_dashboard_without_fig_is_safe(self, capsys) -> None:
        """save_dashboard 在无 fig 时不应崩溃。"""
        dashboard = self.DataDashboard()
        dashboard.save_dashboard("test.png")
