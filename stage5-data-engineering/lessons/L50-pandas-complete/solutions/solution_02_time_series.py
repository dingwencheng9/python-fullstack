"""练习 2: 时间序列预测 - 参考答案"""

from __future__ import annotations

import pandas as pd
import numpy as np


def load_time_series_data() -> pd.DataFrame:
    """加载时间序列数据"""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=730, freq="D")

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
    result = df.copy()
    result[f"ma_{window}"] = result["value"].rolling(window=window).mean()
    result[f"ma_{window * 2}"] = result["value"].rolling(window=window * 2).mean()
    return result


def q2_exponential_smoothing(df: pd.DataFrame, span: int = 30) -> pd.DataFrame:
    """Q2: 指数平滑"""
    result = df.copy()
    result["ema"] = result["value"].ewm(span=span, adjust=False).mean()
    return result


def q3_seasonal_decomposition(df: pd.DataFrame) -> dict:
    """Q3: 季节性分解"""
    from statsmodels.tsa.seasonal import seasonal_decompose

    decomposition = seasonal_decompose(df["value"], model="additive", period=365)

    return {
        "trend": decomposition.trend.dropna(),
        "seasonal": decomposition.seasonal,
        "residual": decomposition.resid.dropna(),
    }


def q4_forecast(df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    """Q4: 简单预测（移动平均法）"""
    df["value"].iloc[-1]
    avg = df["value"].tail(7).mean()

    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=days, freq="D")

    return pd.DataFrame(
        {
            "date": future_dates,
            "forecast": [avg] * days,
            "method": "7-day moving average",
        }
    )


def q5_anomaly_detection(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """Q5: 异常检测（基于滚动标准差）"""
    result = df.copy()
    rolling_mean = result["value"].rolling(window=30).mean()
    rolling_std = result["value"].rolling(window=30).std()

    result["z_score"] = (result["value"] - rolling_mean) / rolling_std
    result["is_anomaly"] = abs(result["z_score"]) > threshold

    return result[result["is_anomaly"]]


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
    print(q1_moving_average(df))

    print("\n" + "=" * 60)
    print("Q2: 指数平滑")
    print("=" * 60)
    print(q2_exponential_smoothing(df))

    print("\n" + "=" * 60)
    print("Q3: 季节性分解")
    print("=" * 60)
    result3 = q3_seasonal_decomposition(df)
    print(f"趋势分量范围: {result3['trend'].min():.2f} - {result3['trend'].max():.2f}")
    print(f"季节性分量范围: {result3['seasonal'].min():.2f} - {result3['seasonal'].max():.2f}")

    print("\n" + "=" * 60)
    print("Q4: 预测")
    print("=" * 60)
    print(q4_forecast(df))

    print("\n" + "=" * 60)
    print("Q5: 异常检测")
    print("=" * 60)
    print(q5_anomaly_detection(df))


if __name__ == "__main__":
    main()
