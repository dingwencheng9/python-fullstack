"""练习 3: 投资组合分析 - 参考答案"""

from __future__ import annotations

import pandas as pd
import numpy as np


def load_portfolio_data() -> pd.DataFrame:
    """加载投资组合数据"""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=252, freq="B")

    stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    n = len(dates)

    data = {}
    for stock in stocks:
        returns = np.random.randn(n) * 0.02
        prices = 100 * np.exp(np.cumsum(returns))
        data[stock] = prices

    df = pd.DataFrame(data, index=dates)
    df.index.name = "date"
    return df


def q1_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Q1: 计算日收益率"""
    return df.pct_change().dropna()


def q2_cumulative_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Q2: 计算累计收益率"""
    normalized = df / df.iloc[0] * 100
    return normalized - 100


def q3_volatility(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """Q3: 计算滚动波动率（标准差）"""
    returns = df.pct_change()
    return returns.rolling(window=window).std() * np.sqrt(252)


def q4_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Q4: 计算收益率相关性矩阵"""
    returns = df.pct_change().dropna()
    return returns.corr()


def q5_sharpe_ratio(df: pd.DataFrame, risk_free_rate: float = 0.02) -> pd.Series:
    """Q5: 计算夏普比率"""
    returns = df.pct_change().dropna()
    mean_return = returns.mean() * 252
    std_return = returns.std() * np.sqrt(252)
    return (mean_return - risk_free_rate) / std_return


def q6_portfolio_return(df: pd.DataFrame, weights: list[float]) -> float:
    """Q6: 计算投资组合预期收益"""
    returns = df.pct_change().dropna()
    return returns.mean().dot(weights) * 252


def q7_max_drawdown(df: pd.DataFrame) -> dict:
    """Q7: 计算最大回撤"""
    cumulative = df / df.iloc[0]
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max

    max_dd = drawdown.min()
    max_dd_idx = drawdown.idxmin()

    peak = running_max.loc[:max_dd_idx].idxmax()
    trough = max_dd_idx

    return {
        "max_drawdown": max_dd,
        "peak_date": peak,
        "trough_date": trough,
        "recovery_date": None,  # 需要额外计算
    }


def main() -> None:
    """主函数"""
    df = load_portfolio_data()

    print("数据形状:", df.shape)
    print("\n股价预览:")
    print(df.head())

    print("\n" + "=" * 60)
    print("Q1: 日收益率")
    print("=" * 60)
    print(q1_daily_returns(df))

    print("\n" + "=" * 60)
    print("Q2: 累计收益率")
    print("=" * 60)
    print(q2_cumulative_returns(df))

    print("\n" + "=" * 60)
    print("Q3: 滚动波动率")
    print("=" * 60)
    print(q3_volatility(df))

    print("\n" + "=" * 60)
    print("Q4: 相关性矩阵")
    print("=" * 60)
    print(q4_correlation_matrix(df))

    print("\n" + "=" * 60)
    print("Q5: 夏普比率")
    print("=" * 60)
    print(q5_sharpe_ratio(df))

    print("\n" + "=" * 60)
    print("Q6: 投资组合收益")
    print("=" * 60)
    weights = [0.2, 0.2, 0.2, 0.2, 0.2]
    result6 = q6_portfolio_return(df, weights)
    print(f"等权重组合收益: {result6:.4f}")

    print("\n" + "=" * 60)
    print("Q7: 最大回撤")
    print("=" * 60)
    print(q7_max_drawdown(df))


if __name__ == "__main__":
    main()
