"""测试练习项目的标准答案

测试 EcommerceAnalytics 类的所有功能，包括:
- 数据加载和清洗
- RFM 计算
- 用户分层
- 内存优化
- 性能要求
- 端到端集成
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

pytest.importorskip("numpy", reason="需要 numpy/pandas 数据栈（uv sync --extra ai）")
pytest.importorskip("pandas", reason="需要 pandas 数据栈（uv sync --extra ai）")

import numpy as np
import pandas as pd

# 使用 module 级别的全局变量，由 fixture 注入
EcommerceAnalytics = None  # type: ignore[assignment]


@pytest.fixture(autouse=True)
def _inject_solutions(solutions, request) -> None:
    """从 solutions 模块动态注入被测类，避免静态导入。"""
    try:
        request.module.EcommerceAnalytics = solutions.project_ecommerce_analytics.EcommerceAnalytics
    except (AttributeError, ImportError) as e:
        pytest.skip(f"无法导入解决方案模块: {e}")


@pytest.fixture
def sample_orders_file(tmp_path: Path) -> str:
    """创建临时测试数据文件（固定 seed 保证可重现）"""
    rng = np.random.default_rng(42)

    # 创建小规模测试数据（10000 条订单）
    n_orders = 10_000
    n_users = 1_000

    base_date = datetime(2024, 1, 1)

    data = {
        "order_id": range(1, n_orders + 1),
        "user_id": rng.integers(1, n_users + 1, n_orders),
        "order_date": [(base_date + timedelta(days=int(rng.integers(0, 365)))).strftime("%Y-%m-%d") for _ in range(n_orders)],
        "price": rng.uniform(10, 1000, n_orders),
        "quantity": rng.integers(1, 10, n_orders),
        "category": rng.choice(["Electronics", "Clothing", "Food"], n_orders),
        "status": rng.choice(["completed", "pending", "cancelled"], n_orders),
        "payment_method": rng.choice(["credit_card", "debit_card", "paypal"], n_orders),
    }

    df = pd.DataFrame(data)

    # 添加一些缺失值和异常值（用于测试清洗逻辑）
    df.loc[df.sample(100, random_state=42).index, "price"] = np.nan
    df.loc[df.sample(50, random_state=43).index, "quantity"] = -1
    df.loc[df.sample(20, random_state=44).index, "user_id"] = np.nan

    # 添加重复订单（用于测试去重）
    duplicates = df.sample(100, random_state=45)
    df = pd.concat([df, duplicates], ignore_index=True)

    # 保存到 pytest 提供的临时目录（自动清理）
    output_path = tmp_path / "sample_orders.csv"
    df.to_csv(output_path, index=False)
    return str(output_path)


@pytest.fixture
def analytics() -> EcommerceAnalytics:
    """创建分析器实例"""
    return EcommerceAnalytics(
        analysis_date=datetime(2024, 12, 31),
        use_pyarrow=True,
        memory_optimize=True,
    )


class TestLoadOrders:
    """测试订单数据加载和清洗"""

    def test_load_orders_basic(self, analytics: EcommerceAnalytics, sample_orders_file: str) -> None:
        """测试基本加载功能"""
        df = analytics.load_orders(sample_orders_file)
        assert isinstance(df, pd.DataFrame)
        required_cols = ["order_id", "user_id", "order_date", "price", "quantity"]
        assert all(col in df.columns for col in required_cols)

    def test_load_orders_removes_duplicates(self, analytics: EcommerceAnalytics, sample_orders_file: str) -> None:
        """测试去重功能"""
        df = analytics.load_orders(sample_orders_file)
        assert df["order_id"].duplicated().sum() == 0

    def test_load_orders_filters_invalid_data(self, analytics: EcommerceAnalytics, sample_orders_file: str) -> None:
        """测试过滤异常值"""
        df = analytics.load_orders(sample_orders_file)
        assert (df["price"] > 0).all()
        assert (df["quantity"] > 0).all()


class TestCalculateRFM:
    """测试 RFM 计算"""

    def test_calculate_rfm_basic(self, analytics: EcommerceAnalytics) -> None:
        """测试基本 RFM 计算"""
        test_data = pd.DataFrame(
            {
                "order_id": [1, 2, 3, 4, 5],
                "user_id": [1, 1, 2, 2, 3],
                "order_date": pd.to_datetime(["2024-12-01", "2024-12-15", "2024-11-01", "2024-11-15", "2024-06-01"]),
                "price": [100.0, 200.0, 150.0, 250.0, 300.0],
                "quantity": [1, 2, 1, 1, 1],
            }
        )
        rfm_df = analytics.calculate_rfm(test_data)
        assert all(col in rfm_df.columns for col in ["user_id", "recency", "frequency", "monetary"])
        assert len(rfm_df) == 3


class TestSegmentCustomers:
    """测试用户分层"""

    def test_segment_customers_basic(self, analytics: EcommerceAnalytics) -> None:
        """测试基本分层功能"""
        rfm_data = pd.DataFrame(
            {
                "user_id": [1, 2, 3, 4],
                "recency": [10, 50, 200, 100],
                "frequency": [15, 6, 1, 3],
                "monetary": [15000.0, 6000.0, 1000.0, 3000.0],
            }
        )
        segmented_df = analytics.segment_customers(rfm_data)
        assert "segment" in segmented_df.columns


class TestOptimizeMemory:
    """测试内存优化"""

    def test_optimize_memory_basic(self, analytics: EcommerceAnalytics) -> None:
        """测试基本内存优化"""
        test_data = pd.DataFrame(
            {
                "small_int": np.random.randint(0, 100, 1000),
                "large_int": np.random.randint(0, 1_000_000, 1000),
                "float_col": np.random.randn(1000),
                "category_col": np.random.choice(["A", "B", "C"], 1000),
            }
        )
        original_memory = test_data.memory_usage(deep=True).sum()
        optimized_df = analytics.optimize_memory(test_data)
        optimized_memory = optimized_df.memory_usage(deep=True).sum()
        assert optimized_memory < original_memory


class TestPerformance:
    """测试性能要求"""

    def test_performance_requirements(self, analytics: EcommerceAnalytics, sample_orders_file: str) -> None:
        """测试整体性能要求"""
        import time

        start = time.time()
        df = analytics.load_orders(sample_orders_file)
        rfm_df = analytics.calculate_rfm(df)
        segmented_df = analytics.segment_customers(rfm_df)
        _ = analytics.optimize_memory(segmented_df)
        total_time = time.time() - start
        assert total_time < 5.0


class TestEndToEnd:
    """端到端集成测试"""

    def test_end_to_end_workflow(self, analytics: EcommerceAnalytics, sample_orders_file: str) -> None:
        """测试完整工作流"""
        df = analytics.load_orders(sample_orders_file)
        assert len(df) > 0
        rfm_df = analytics.calculate_rfm(df)
        assert len(rfm_df) > 0
        segmented_df = analytics.segment_customers(rfm_df)
        assert "segment" in segmented_df.columns
        optimized_df = analytics.optimize_memory(segmented_df)
        assert optimized_df.memory_usage(deep=True).sum() < segmented_df.memory_usage(deep=True).sum()


class TestGenerateReport:
    """测试报告生成"""

    def test_generate_report_structure(self, analytics: EcommerceAnalytics, sample_orders_file: str) -> None:
        """测试报告结构"""
        df = analytics.load_orders(sample_orders_file)
        rfm_df = analytics.calculate_rfm(df)
        segmented_df = analytics.segment_customers(rfm_df)
        analytics.optimize_memory(segmented_df)
        report = analytics.generate_report()
        assert isinstance(report, dict)
        assert "summary" in report
        assert "segments" in report
