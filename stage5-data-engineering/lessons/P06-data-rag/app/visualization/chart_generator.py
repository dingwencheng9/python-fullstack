"""P06: 图表生成模块"""

from matplotlib.figure import Figure


class ChartGenerator:
    """图表生成器"""

    def __init__(self):
        pass

    def create_dashboard(self, data: dict) -> Figure:
        """创建仪表板"""
        import matplotlib.pyplot as plt
        from pandas import DataFrame

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        if "data" in data and isinstance(data["data"], DataFrame):
            df = data["data"]
            numeric_cols = df.select_dtypes(include=["number"]).columns[:4]

            for i, col in enumerate(numeric_cols):
                ax = axes[i // 2, i % 2]
                ax.plot(df[col].head(20))
                ax.set_title(col)
                ax.grid(True)

        plt.tight_layout()
        return fig

    def save_figure(self, fig: Figure, path: str) -> None:
        """保存图表"""
        fig.savefig(path, dpi=100)
