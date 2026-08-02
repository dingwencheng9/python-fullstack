"""L50 DuckDB 测试"""

from __future__ import annotations

import pytest

# 确保 duckdb 已安装（在核心依赖中）
pytest.importorskip("duckdb", reason="需要 duckdb（已在核心依赖中）")

import duckdb
import pandas as pd


def test_basic_query():
    """测试 DuckDB 基本查询"""
    conn = duckdb.connect()
    result = conn.execute("SELECT 1 AS a").fetchall()
    assert result == [(1,)]


def test_query_dataframe():
    """测试查询 Python DataFrame"""
    conn = duckdb.connect()
    data = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    conn.register("df", data)
    result = conn.execute("SELECT SUM(x) AS total FROM df").fetchone()
    assert result[0] == 6


def test_aggregation():
    """测试分组聚合"""
    conn = duckdb.connect()
    df = pd.DataFrame({"grp": ["A", "A", "B"], "val": [10, 20, 30]})
    conn.register("df", df)
    result = conn.execute("""
        SELECT grp, SUM(val) AS total
        FROM df
        GROUP BY grp
        ORDER BY grp
    """).fetchall()
    assert result == [("A", 30), ("B", 30)]


def test_window_function():
    """测试窗口函数"""
    conn = duckdb.connect()
    df = pd.DataFrame({"date": [1, 2, 3], "val": [10, 20, 30]})
    conn.register("df", df)
    result = conn.execute("""
        SELECT val, SUM(val) OVER (ORDER BY date) AS cum
        FROM df
        ORDER BY date
    """).fetchall()
    assert result == [(10, 10), (20, 30), (30, 60)]


def test_csv_query():
    """测试直接查询 CSV"""
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age\nAlice,30\nBob,25\n")
        path = f.name
    conn = duckdb.connect()
    result = conn.execute(f"SELECT COUNT(*) AS cnt FROM read_csv_auto('{path}')").fetchone()
    assert result[0] == 2
    os.unlink(path)


def test_register():
    """测试 register 方法"""
    conn = duckdb.connect()
    df = pd.DataFrame({"id": [1, 2, 3]})
    conn.register("my_table", df)
    result = conn.execute("SELECT COUNT(*) FROM my_table").fetchone()
    assert result[0] == 3


@pytest.mark.parametrize(
    "values,expected_sum",
    [
        ([1, 2, 3], 6),
        ([10, 20], 30),
        ([5], 5),
    ],
)
def test_parametrized_sum(values, expected_sum):
    """参数化：求和测试"""
    conn = duckdb.connect()
    df = pd.DataFrame({"v": values})
    conn.register("df", df)
    result = conn.execute("SELECT SUM(v) FROM df").fetchone()
    assert result[0] == expected_sum


# ============================================================================
# 新增: solutions 函数测试
# ============================================================================


class TestWindowFunctionsSolution:
    """测试 01_window_functions 的函数化实现。"""

    @pytest.fixture(autouse=True)
    def _setup(self, solutions) -> None:
        """注入 solution 模块到测试类。"""
        s = getattr(solutions, "01_window_functions")
        self.generate_sales_data = s.generate_sales_data
        self.compute_window_metrics = s.compute_window_metrics
        self.get_total_cumulative = s.get_total_cumulative

    def test_generate_returns_dataframe(self) -> None:
        """generate_sales_data 应返回 DataFrame。"""
        df = self.generate_sales_data()
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["date", "region", "amount"]
        assert len(df) == 50

    def test_generate_deterministic(self) -> None:
        """相同 seed 应产生相同数据。"""
        a = self.generate_sales_data(seed=7)
        b = self.generate_sales_data(seed=7)
        pd.testing.assert_frame_equal(a, b)

    def test_window_metrics_adds_columns(self) -> None:
        """compute_window_metrics 应添加 cumulative/vs_avg/rank 三列。"""
        df = self.generate_sales_data()
        result = self.compute_window_metrics(df)
        expected_cols = {"date", "region", "amount", "cumulative", "vs_avg", "rank"}
        assert set(result.columns) == expected_cols
        assert len(result) == 50

    def test_cumulative_is_monotonic(self) -> None:
        """累计总和应单调递增。"""
        df = self.generate_sales_data()
        result = self.compute_window_metrics(df)
        cum = result["cumulative"].values
        assert all(cum[i] <= cum[i + 1] for i in range(len(cum) - 1))

    def test_total_cumulative_matches_sum(self) -> None:
        """get_total_cumulative 应等于 amount 总和。"""
        df = self.generate_sales_data()
        result = self.compute_window_metrics(df)
        total = self.get_total_cumulative(result)
        assert total == pytest.approx(float(df["amount"].sum()), rel=1e-6)


class TestPandasDuckDBMixSolution:
    """测试 02_pandas_duckdb_mix 的函数化实现。"""

    @pytest.fixture(autouse=True)
    def _setup(self, solutions) -> None:
        """注入 solution 模块到测试类。"""
        s = getattr(solutions, "02_pandas_duckdb_mix")
        self.generate_raw_data = s.generate_raw_data
        self.clean_data = s.clean_data
        self.aggregate_monthly = s.aggregate_monthly
        self.to_pivot_table = s.to_pivot_table
        self.run_full_pipeline = s.run_full_pipeline

    def test_generate_raw_return_shape(self) -> None:
        """有效 seed 应生成 365 行。"""
        raw = self.generate_raw_data(seed=1)
        assert len(raw) == 365
        assert list(raw.columns) == ["date", "product", "sales"]

    def test_clean_removes_non_positive(self) -> None:
        """clean_data 应移除 sales <= 0 的行。"""
        raw = self.generate_raw_data()
        cleaned = self.clean_data(raw)
        assert all(cleaned["sales"] > 0)
        assert "month" in cleaned.columns

    def test_aggregate_monthly_groups(self) -> None:
        """aggregate_monthly 应返回月+产品分组结果。"""
        raw = self.generate_raw_data()
        cleaned = self.clean_data(raw)
        agg = self.aggregate_monthly(cleaned)
        assert set(agg.columns) >= {"month", "product", "orders", "revenue"}
        # 12 个月 × 3 个产品 → 最多 36 行
        assert len(agg) <= 36

    def test_pivot_shape(self) -> None:
        """透视表应为 12 行 × 3 列。"""
        raw = self.generate_raw_data()
        pivot = self.to_pivot_table(self.aggregate_monthly(self.clean_data(raw)))
        assert pivot.shape == (12, 3)

    def test_full_pipeline_deterministic(self) -> None:
        """相同 seed 运行全管线应产生相同透视表。"""
        a = self.run_full_pipeline(seed=99)
        b = self.run_full_pipeline(seed=99)
        pd.testing.assert_frame_equal(a, b)

    def test_pipeline_output_is_positive(self) -> None:
        """管线输出的透视表不应有负值。"""
        pivot = self.run_full_pipeline()
        assert (pivot.values >= 0).all()
