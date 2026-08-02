"""示例 4: 窗口函数

展示高级窗口函数：
- rolling 与 expanding
- 排名窗口
- 自定义聚合
"""

from __future__ import annotations

import pandas as pd
import numpy as np


def create_stock_data() -> pd.DataFrame:
    """创建股票数据示例"""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=252, freq="B")  # 交易日

    return pd.DataFrame(
        {
            "date": dates,
            "symbol": ["AAPL"] * 126 + ["GOOGL"] * 126,
            "price": np.concatenate(
                [
                    np.cumsum(np.random.randn(126)) + 150,
                    np.cumsum(np.random.randn(126)) + 2800,
                ]
            ),
            "volume": np.random.randint(1_000_000, 10_000_000, 252),
        }
    )


def ranking_windows(df: pd.DataFrame) -> pd.DataFrame:
    """排名窗口函数"""
    # 按股票分组排名
    df["price_rank"] = df.groupby("symbol")["price"].rank(method="dense", ascending=False)
    df["price_rank_asc"] = df.groupby("symbol")["price"].rank(method="dense")

    # 百分位排名
    df["pct_rank"] = df.groupby("symbol")["price"].rank(pct=True)

    # 按天分组排名
    df["volume_rank"] = df.groupby("date")["volume"].rank(ascending=False)

    print("排名窗口示例:\n", df.head(20))
    return df


def cumulative_functions(df: pd.DataFrame) -> pd.DataFrame:
    """累计计算"""
    # 分组累计
    df["cumsum_price"] = df.groupby("symbol")["price"].cumsum()
    df["cumcount"] = df.groupby("symbol").cumcount()

    # 累计最大值（到当前位置的最大值）
    df["cummax"] = df.groupby("symbol")["price"].cummax()

    # 累计最小值
    df["cummin"] = df.groupby("symbol")["price"].cummin()

    # 是否创历史新高
    df["is_high"] = df["price"] == df["cummax"]

    print("\n累计函数示例:\n", df[["symbol", "price", "cumsum_price", "cummax", "is_high"]].head(20))
    return df


def shift_functions(df: pd.DataFrame) -> pd.DataFrame:
    """位移函数"""
    # 分组 shift
    df["prev_price"] = df.groupby("symbol")["price"].shift(1)
    df["next_price"] = df.groupby("symbol")["price"].shift(-1)

    # 5日前价格
    df["price_5d_ago"] = df.groupby("symbol")["price"].shift(5)

    # 计算收益率
    df["return_1d"] = (df["price"] - df["prev_price"]) / df["prev_price"] * 100
    df["return_5d"] = (df["price"] - df["price_5d_ago"]) / df["price_5d_ago"] * 100

    print("\n位移函数示例:\n", df[["symbol", "price", "prev_price", "return_1d"]].head(20))
    return df


def rolling_quantile(df: pd.DataFrame) -> pd.DataFrame:
    """滚动分位数"""
    # 20日滚动分位数
    df["q25"] = df.groupby("symbol")["price"].transform(lambda x: x.rolling(20).quantile(0.25))
    df["q50"] = df.groupby("symbol")["price"].transform(lambda x: x.rolling(20).quantile(0.50))
    df["q75"] = df.groupby("symbol")["price"].transform(lambda x: x.rolling(20).quantile(0.75))

    print("\n滚动分位数示例:\n", df[["symbol", "price", "q25", "q50", "q75"]].dropna().head(10))
    return df


def custom_rolling_agg(df: pd.DataFrame) -> pd.DataFrame:
    """自定义滚动聚合"""

    def bollinger_bands(prices: pd.Series, window: int = 20, num_std: float = 2.0) -> dict:
        """计算布林带"""
        ma = prices.rolling(window).mean()
        std = prices.rolling(window).std()
        return {
            "bb_upper": ma + num_std * std,
            "bb_middle": ma,
            "bb_lower": ma - num_std * std,
        }

    # 应用自定义函数
    for symbol in df["symbol"].unique():
        mask = df["symbol"] == symbol
        prices = df.loc[mask, "price"]
        bb = bollinger_bands(prices)
        df.loc[mask, "bb_upper"] = bb["bb_upper"].values
        df.loc[mask, "bb_middle"] = bb["bb_middle"].values
        df.loc[mask, "bb_lower"] = bb["bb_lower"].values

    # 布林带位置
    df["bb_position"] = (df["price"] - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])

    print("\n布林带示例:\n", df[["symbol", "price", "bb_upper", "bb_middle", "bb_lower", "bb_position"]].dropna().head(10))
    return df


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("窗口函数示例")
    print("=" * 60)

    df = create_stock_data()
    print(f"数据形状: {df.shape}")
    print(f"股票列表: {df['symbol'].unique()}")

    print("\n" + "=" * 60)
    print("排名窗口")
    print("=" * 60)
    df = ranking_windows(df)

    print("\n" + "=" * 60)
    print("累计函数")
    print("=" * 60)
    df = cumulative_functions(df)

    print("\n" + "=" * 60)
    print("位移函数")
    print("=" * 60)
    df = shift_functions(df)

    print("\n" + "=" * 60)
    print("滚动分位数")
    print("=" * 60)
    df = rolling_quantile(df)

    print("\n" + "=" * 60)
    print("自定义滚动聚合（布林带）")
    print("=" * 60)
    df = custom_rolling_agg(df)


if __name__ == "__main__":
    main()
