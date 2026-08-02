"""示例 3: 时间序列处理

展示时间序列数据处理：
- DatetimeIndex
- 重采样
- 滚动窗口
- 时区处理
"""

from __future__ import annotations

import pandas as pd
import numpy as np


def create_time_series_data(n: int = 365) -> pd.DataFrame:
    """创建时间序列示例数据"""
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    np.random.seed(42)

    return pd.DataFrame(
        {
            "date": dates,
            "value": np.random.randn(n).cumsum() + 100,
            "volume": np.random.randint(1000, 10000, n),
        }
    )


def datetime_index_operations(df: pd.DataFrame) -> pd.DataFrame:
    """DatetimeIndex 操作"""
    # 设置日期为索引
    df = df.set_index("date")

    # 按年、月、日访问数据
    print("2024年3月数据:\n", df["2024-03"])
    print("\n3月份数据:\n", df[df.index.month == 3])
    print("\n周一数据:\n", df[df.index.dayofweek == 0])

    # 日期范围切片
    print("\n1月1日 - 1月15日:\n", df["2024-01-01":"2024-01-15"])

    return df


def resampling_examples(df: pd.DataFrame) -> None:
    """重采样示例"""
    # 日 -> 月
    monthly = df["value"].resample("ME").agg(["sum", "mean", "std"])
    print("月度统计:\n", monthly)

    # 日 -> 周
    weekly = df["value"].resample("W").agg(["sum", "mean"])
    print("\n周度统计:\n", weekly)

    # 日 -> 季度
    quarterly = df["value"].resample("QE").agg(["sum", "mean"])
    print("\n季度统计:\n", quarterly)

    # 上采样（插值）
    daily_upsampled = df["value"].resample("h").interpolate()
    print("\n小时插值（部分）:\n", daily_upsampled.head())


def rolling_window_examples(df: pd.DataFrame) -> pd.DataFrame:
    """滚动窗口示例"""
    # 7日移动平均
    df["ma_7"] = df["value"].rolling(window=7).mean()

    # 30日移动平均
    df["ma_30"] = df["value"].rolling(window=30).mean()

    # 7日移动标准差
    df["std_7"] = df["value"].rolling(window=7).std()

    # 7日最小/最大值
    df["min_7"] = df["value"].rolling(window=7).min()
    df["max_7"] = df["value"].rolling(window=7).max()

    # 指数加权移动平均
    df["ewma_7"] = df["value"].ewm(span=7).mean()
    df["ewma_30"] = df["value"].ewm(span=30).mean()

    print("滚动窗口计算结果（前10行）:\n", df[["value", "ma_7", "ewma_7"]].head(10))
    return df


def expanding_window_examples(df: pd.DataFrame) -> pd.DataFrame:
    """扩展窗口示例"""
    # 累计最大值
    df["cummax"] = df["value"].expanding().max()

    # 累计最小值
    df["cummin"] = df["value"].expanding().min()

    # 累计均值
    df["cummean"] = df["value"].expanding().mean()

    # 累计和
    df["cumsum"] = df["value"].expanding().sum()

    print("扩展窗口计算结果（前10行）:\n", df[["value", "cummax", "cummean"]].head(10))
    return df


def timezone_examples() -> None:
    """时区处理示例"""
    # 创建 UTC 时间序列
    dates_utc = pd.date_range("2024-01-01", periods=24, freq="h", tz="UTC")
    df_utc = pd.DataFrame(
        {
            "datetime": dates_utc,
            "value": range(24),
        }
    ).set_index("datetime")

    print("UTC 时间:\n", df_utc)

    # 转换为不同时区
    df_shanghai = df_utc.tz_convert("Asia/Shanghai")
    print("\n上海时间:\n", df_shanghai)

    df_tokyo = df_utc.tz_convert("Asia/Tokyo")
    print("\n东京时间:\n", df_tokyo)

    # 本地化
    dates_naive = pd.date_range("2024-01-01", periods=10, freq="D")
    df_naive = pd.DataFrame(
        {
            "datetime": dates_naive,
            "value": range(10),
        }
    ).set_index("datetime")

    df_localized = df_naive.tz_localize("Asia/Shanghai")
    print("\n本地化后:\n", df_localized)


def lag_lead_examples(df: pd.DataFrame) -> pd.DataFrame:
    """lag/lead 操作示例"""
    # shift 实现 lag
    df["prev_1"] = df["value"].shift(1)
    df["prev_7"] = df["value"].shift(7)

    # shift(-1) 实现 lead
    df["next_1"] = df["value"].shift(-1)

    # 计算变化
    df["change"] = df["value"] - df["prev_1"]
    df["change_pct"] = df["change"] / df["prev_1"] * 100

    # 环比（与前一天相比）
    df["chain_ratio"] = df["value"] / df["prev_1"]

    # 同比（与去年同期相比，假设有足够数据）
    df["yoy_change"] = df["value"] - df["value"].shift(365)

    print("lag/lead 示例（前10行）:\n", df[["value", "prev_1", "change", "change_pct"]].head(10))
    return df


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("时间序列处理示例")
    print("=" * 60)

    df = create_time_series_data(365)
    print(f"数据形状: {df.shape}")
    print(f"数据预览:\n{df.head()}")

    print("\n" + "=" * 60)
    print("DatetimeIndex 操作")
    print("=" * 60)
    df = datetime_index_operations(df)

    print("\n" + "=" * 60)
    print("重采样示例")
    print("=" * 60)
    resampling_examples(df)

    print("\n" + "=" * 60)
    print("滚动窗口示例")
    print("=" * 60)
    df = rolling_window_examples(df)

    print("\n" + "=" * 60)
    print("扩展窗口示例")
    print("=" * 60)
    df = expanding_window_examples(df)

    print("\n" + "=" * 60)
    print("时区处理示例")
    print("=" * 60)
    timezone_examples()

    print("\n" + "=" * 60)
    print("lag/lead 示例")
    print("=" * 60)
    df = lag_lead_examples(df)


if __name__ == "__main__":
    main()
