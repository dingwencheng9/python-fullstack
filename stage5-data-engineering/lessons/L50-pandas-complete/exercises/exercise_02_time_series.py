"""练习 2: 时间序列预测

使用 Pandas 时间序列功能进行预测分析。
"""

from __future__ import annotations

import pandas as pd
import numpy as np


def load_time_series_data() -> pd.DataFrame:
    """加载时间序列数据"""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=730, freq="D")

    # 创建带有趋势和季节性的数据
    trend = np.linspace(0, 100, 730)
    seasonality = 20 * np.sin(2 * np.pi * np.arange(730) / 365)
    noise = np.random.randn(730) * 10

    return pd.DataFrame(
        {
            "date": dates,
            "value": trend + seasonality + noise + 100,
            "category": np.random.choice(["A", "B"], 730),
        }
    )


def q1_moving_average(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """Q1: 计算移动平均"""
    # TODO: 实现


def q2_exponential_smoothing(df: pd.DataFrame, span: int = 30) -> pd.DataFrame:
    """Q2: 指数平滑"""
    # TODO: 实现


def q3_seasonal_decomposition(df: pd.DataFrame) -> dict:
    """Q3: 季节性分解"""
    # TODO: 实现


def q4_forecast(df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    """Q4: 简单预测（移动平均法）"""
    # TODO: 实现


def q5_anomaly_detection(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """Q5: 异常检测（基于滚动标准差）"""
    # TODO: 实现


def main() -> None:
    """主函数"""
    df = load_time_series_data()
    df = df.set_index("date")

    print("数据形状:", df.shape)
    print("\n数据预览:")
    print(df.head())

    print("\n" + "=" * 60)
    print("Q1: 移动平均")
    print("=" * 60)
    result1 = q1_moving_average(df)
    print(result1)

    print("\n" + "=" * 60)
    print("Q2: 指数平滑")
    print("=" * 60)
    result2 = q2_exponential_smoothing(df)
    print(result2)

    print("\n" + "=" * 60)
    print("Q3: 季节性分解")
    print("=" * 60)
    result3 = q3_seasonal_decomposition(df)
    print(result3)

    print("\n" + "=" * 60)
    print("Q4: 预测")
    print("=" * 60)
    result4 = q4_forecast(df)
    print(result4)

    print("\n" + "=" * 60)
    print("Q5: 异常检测")
    print("=" * 60)
    result5 = q5_anomaly_detection(df)
    print(result5)


if __name__ == "__main__":
    main()
