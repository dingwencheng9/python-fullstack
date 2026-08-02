"""L18 练习题: 数据可视化仪表板"""

from __future__ import annotations

import pandas as pd


class DataDashboard:
    """数据可视化仪表板 - 学员需实现

    要求: 创建多图表仪表板，展示数据分析结果
    """

    def __init__(self):
        raise NotImplementedError

    def create_overview_dashboard(self, data: pd.DataFrame) -> None:
        """TODO: 创建概览仪表板（4个子图）"""
        raise NotImplementedError

    def create_time_series_chart(self, data: pd.DataFrame) -> None:
        """TODO: 时间序列图表"""
        raise NotImplementedError

    def create_distribution_analysis(self, data: pd.DataFrame) -> None:
        """TODO: 分布分析图"""
        raise NotImplementedError

    def create_correlation_heatmap(self, data: pd.DataFrame) -> None:
        """TODO: 相关性热力图"""
        raise NotImplementedError

    def save_dashboard(self, filename: str) -> None:
        """TODO: 保存仪表板为图片"""
        raise NotImplementedError
