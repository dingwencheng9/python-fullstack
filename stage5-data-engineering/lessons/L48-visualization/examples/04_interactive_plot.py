"""L49 示例 4: 交互式可视化"""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def interactive_scatter(df: pd.DataFrame, x: str, y: str, color: str) -> None:
    """交互式散点图（支持 hover/缩放）"""
    fig = px.scatter(df, x=x, y=y, color=color, title=f"{y} vs {x}", hover_data=df.columns)
    fig.show()


def interactive_timeseries(df: pd.DataFrame, date_col: str, value_col: str) -> None:
    """交互式时间序列"""
    fig = px.line(df, x=date_col, y=value_col, title=f"{value_col} 趋势")
    fig.update_xaxes(rangeslider_visible=True)
    fig.show()


if __name__ == "__main__":
    df = px.data.iris()
    interactive_scatter(df, "sepal_width", "sepal_length", "species")
