"""L50 测试套件

测试高级 Pandas 操作。
"""

from __future__ import annotations

import pandas as pd
import pytest


class TestAdvancedGroupby:
    """测试高级分组聚合"""

    @pytest.fixture
    def sample_df(self) -> pd.DataFrame:
        """创建示例数据"""
        return pd.DataFrame(
            {
                "category": ["A", "B", "A", "B", "A", "B"],
                "value": [10, 20, 30, 40, 50, 60],
                "quantity": [1, 2, 3, 4, 5, 6],
            }
        )

    def test_basic_groupby_sum(self, sample_df: pd.DataFrame) -> None:
        """测试基础分组求和"""
        result = sample_df.groupby("category")["value"].sum()
        assert result["A"] == 90
        assert result["B"] == 120

    def test_multi_agg(self, sample_df: pd.DataFrame) -> None:
        """测试多函数聚合"""
        result = sample_df.groupby("category").agg(
            {
                "value": ["sum", "mean"],
                "quantity": "sum",
            }
        )
        assert result.loc["A", ("value", "sum")] == 90
        assert result.loc["A", ("value", "mean")] == 30


class TestComplexJoins:
    """测试复杂连接操作"""

    @pytest.fixture
    def df1(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "key": ["A", "B", "C"],
                "value1": [1, 2, 3],
            }
        )

    @pytest.fixture
    def df2(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "key": ["A", "B", "D"],
                "value2": [10, 20, 40],
            }
        )

    def test_inner_join(self, df1: pd.DataFrame, df2: pd.DataFrame) -> None:
        """测试内连接"""
        result = pd.merge(df1, df2, on="key", how="inner")
        assert len(result) == 2
        assert set(result["key"]) == {"A", "B"}

    def test_left_join(self, df1: pd.DataFrame, df2: pd.DataFrame) -> None:
        """测试左连接"""
        result = pd.merge(df1, df2, on="key", how="left")
        assert len(result) == 3
        assert result.loc[result["key"] == "C", "value2"].isna().all()


class TestTimeSeries:
    """测试时间序列处理"""

    @pytest.fixture
    def ts_df(self) -> pd.DataFrame:
        """创建时间序列数据"""
        dates = pd.date_range("2024-01-01", periods=10, freq="D")
        return pd.DataFrame(
            {
                "date": dates,
                "value": range(10),
            }
        ).set_index("date")

    def test_resample_monthly(self, ts_df: pd.DataFrame) -> None:
        """测试月度重采样"""
        monthly = ts_df["value"].resample("ME").sum()
        assert monthly.iloc[0] == sum(range(10))

    def test_rolling_mean(self, ts_df: pd.DataFrame) -> None:
        """测试滚动平均"""
        result = ts_df["value"].rolling(window=3).mean()
        assert result.iloc[2] == pytest.approx(1.0)


class TestWindowFunctions:
    """测试窗口函数"""

    @pytest.fixture
    def stock_df(self) -> pd.DataFrame:
        """创建股票数据"""
        return pd.DataFrame(
            {
                "symbol": ["AAPL"] * 5 + ["GOOGL"] * 5,
                "price": [100, 102, 101, 103, 105, 200, 202, 201, 203, 205],
            }
        )

    def test_groupby_rank(self, stock_df: pd.DataFrame) -> None:
        """测试分组排名"""
        result = stock_df.groupby("symbol")["price"].rank()
        assert result.iloc[0] == 1  # AAPL 第一天最低

    def test_cumsum_by_group(self, stock_df: pd.DataFrame) -> None:
        """测试分组累计和"""
        result = stock_df.groupby("symbol")["price"].cumsum()
        assert result.iloc[0] == 100
        assert result.iloc[4] == 511  # AAPL 累计


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
