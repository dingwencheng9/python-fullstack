"""L16 Pandas 高性能数据处理 - 示例代码测试

from __future__ import annotations

测试 examples/ 目录下的所有示例代码:
- 01_vectorization_pipeline.py: 向量化数据处理管道
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("numpy", reason="需要 numpy/pandas 数据栈（uv sync --extra ai）")
pytest.importorskip("pandas", reason="需要 pandas 数据栈（uv sync --extra ai）")

import numpy as np
import pandas as pd

# sys.path 注入由同目录 conftest.py 统一管理，严禁在此污染

# 定义 examples 目录路径
_EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


class TestDataPipeline:
    """测试 DataPipeline 向量化管道"""

    @pytest.fixture
    def pipeline(self):
        """创建测试管道实例"""
        # 动态导入以避免路径问题
        import importlib.util

        spec = importlib.util.spec_from_file_location("vectorization_pipeline", _EXAMPLES_DIR / "01_vectorization_pipeline.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.DataPipeline(use_pyarrow=True)

    @pytest.fixture
    def pipeline_no_pyarrow(self):
        """创建不使用 PyArrow 的管道实例"""
        import importlib.util

        spec = importlib.util.spec_from_file_location("vectorization_pipeline", _EXAMPLES_DIR / "01_vectorization_pipeline.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.DataPipeline(use_pyarrow=False)

    @pytest.fixture
    def small_orders_df(self):
        """创建小型测试订单数据"""
        import numpy as np

        n_rows = 1000
        data = {
            "order_id": [f"ORD{i:06d}" for i in range(n_rows)],
            "user_id": np.random.randint(1, 100, n_rows),
            "product_id": np.random.randint(1, 50, n_rows),
            "quantity": np.random.randint(1, 21, n_rows),
            "price": np.random.uniform(10.0, 1000.0, n_rows),
            "order_date": pd.date_range(start="2023-01-01", periods=n_rows),
            "status": np.random.choice(["pending", "completed", "cancelled"], n_rows),
            "payment_method": np.random.choice(["credit_card", "debit_card", "paypal", "cash"], n_rows),
        }
        df = pd.DataFrame(data)

        # 注入脏数据
        # 5% price 缺失值
        missing_indices = np.random.choice(n_rows, size=int(n_rows * 0.05), replace=False)
        df.loc[missing_indices, "price"] = np.nan

        # 1% quantity 异常值
        anomaly_indices = np.random.choice(n_rows, size=int(n_rows * 0.01), replace=False)
        df.loc[anomaly_indices, "quantity"] = -1

        return df

    def test_init_default(self, pipeline):
        """测试默认初始化"""
        # use_pyarrow 可能因为 PyArrow 未安装而被设为 False
        assert isinstance(pipeline.use_pyarrow, bool)
        assert hasattr(pipeline, "_performance_stats")
        assert isinstance(pipeline._performance_stats, dict)

    def test_init_no_pyarrow(self, pipeline_no_pyarrow):
        """测试禁用 PyArrow 初始化"""
        assert pipeline_no_pyarrow.use_pyarrow is False

    def test_load_data(self, pipeline, sample_orders_path):
        """测试数据加载功能"""
        # 加载前 10000 行进行快速测试
        df = pipeline.load_data(str(sample_orders_path), chunksize=10_000)

        # 验证数据加载成功
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10_000
        assert "order_id" in df.columns
        assert "price" in df.columns
        assert "quantity" in df.columns

        # 验证 PyArrow 后端已应用（仅在可用时检查）
        if pipeline.use_pyarrow:
            assert "pyarrow" in str(df["user_id"].dtype).lower()

    def test_clean_missing_values(self, pipeline, small_orders_df):
        """测试缺失值清理功能"""
        # 记录原始缺失值数量
        original_missing = small_orders_df["price"].isna().sum()
        assert original_missing > 0, "测试数据应包含缺失值"

        # 清理缺失值
        cleaned_df = pipeline.clean_missing_values(small_orders_df.copy())

        # 验证缺失值已被处理
        assert cleaned_df["price"].isna().sum() == 0, "所有缺失值应被填充"

        # 验证使用中位数填充（检查填充值合理性）
        filled_values = cleaned_df.loc[small_orders_df["price"].isna(), "price"]
        assert len(filled_values) > 0
        assert filled_values.nunique() == 1, "所有缺失值应填充相同的中位数"

    def test_transform_types(self, pipeline, small_orders_df):
        """测试类型转换功能"""
        # 清理数据后再转换类型
        cleaned_df = pipeline.clean_missing_values(small_orders_df.copy())
        transformed_df = pipeline.transform_types(cleaned_df)

        # 验证类型优化
        # user_id 应从 int64 优化为更小的整数类型
        assert transformed_df["user_id"].dtype != small_orders_df["user_id"].dtype
        assert "int" in str(transformed_df["user_id"].dtype).lower()

        # status 和 payment_method 应转为 category
        assert transformed_df["status"].dtype.name == "category"
        assert transformed_df["payment_method"].dtype.name == "category"

        # quantity 应优化为 int8（范围 1-20）
        assert "int8" in str(transformed_df["quantity"].dtype).lower()

    def test_calculate_features(self, pipeline, small_orders_df):
        """测试特征计算功能"""
        # 清理和转换数据
        cleaned_df = pipeline.clean_missing_values(small_orders_df.copy())
        transformed_df = pipeline.transform_types(cleaned_df)

        # 计算特征
        featured_df = pipeline.calculate_features(transformed_df)

        # 验证新特征列存在
        assert "total_amount" in featured_df.columns
        assert "price_category" in featured_df.columns
        assert "is_high_value" in featured_df.columns
        assert "order_month" in featured_df.columns

        # 验证特征计算正确性
        # total_amount = price * quantity
        assert (featured_df["total_amount"] == featured_df["price"] * featured_df["quantity"]).all()

        # price_category 应为 low/medium/high
        assert set(featured_df["price_category"].unique()).issubset({"low", "medium", "high"})

        # is_high_value 应为布尔值
        assert featured_df["is_high_value"].dtype == bool

        # order_month 应为 1-12
        assert featured_df["order_month"].min() >= 1
        assert featured_df["order_month"].max() <= 12

    def test_benchmark_vs_loop(self, pipeline, small_orders_df):
        """测试性能基准对比（向量化应快于循环）"""
        # 清理和转换数据
        cleaned_df = pipeline.clean_missing_values(small_orders_df.copy())
        transformed_df = pipeline.transform_types(cleaned_df)

        # 运行性能基准测试
        results = pipeline.benchmark_vs_loop(transformed_df)

        # 验证结果结构
        assert "vectorized_time" in results
        assert "apply_time" in results
        assert "iterrows_time" in results
        assert "speedup_vs_apply" in results
        assert "speedup_vs_iterrows" in results

        # 验证向量化比 apply 快至少 10 倍
        assert results["speedup_vs_apply"] >= 10.0, f"向量化应比 apply 快至少 10 倍，实际: {results['speedup_vs_apply']:.1f}x"

        # 验证向量化比 iterrows 快至少 50 倍
        assert results["speedup_vs_iterrows"] >= 50.0, f"向量化应比 iterrows 快至少 50 倍，实际: {results['speedup_vs_iterrows']:.1f}x"

    def test_generate_report(self, pipeline, small_orders_df):
        """测试性能报告生成"""
        # 执行完整管道
        cleaned_df = pipeline.clean_missing_values(small_orders_df.copy())
        transformed_df = pipeline.transform_types(cleaned_df)
        _ = pipeline.calculate_features(transformed_df)
        pipeline.benchmark_vs_loop(transformed_df)

        # 生成报告
        report = pipeline.generate_report()

        # 验证报告包含关键信息
        assert isinstance(report, str)
        assert len(report) > 0
        assert "向量化数据处理管道" in report
        assert "性能统计" in report or "性能" in report

    def test_full_pipeline_integration(self, pipeline, sample_orders_path):
        """测试完整管道集成"""
        # 加载数据
        df = pipeline.load_data(str(sample_orders_path), chunksize=5_000)

        # 清理缺失值
        cleaned_df = pipeline.clean_missing_values(df)
        assert cleaned_df["price"].isna().sum() == 0

        # 转换类型
        transformed_df = pipeline.transform_types(cleaned_df)
        assert transformed_df["status"].dtype.name == "category"

        # 计算特征
        featured_df = pipeline.calculate_features(transformed_df)
        assert "total_amount" in featured_df.columns
        assert "price_category" in featured_df.columns

        # 验证数据完整性
        assert len(featured_df) == len(df)
        assert featured_df["price"].notna().all()


class TestMemoryOptimizer:
    """测试 MemoryOptimizer 内存优化器"""

    @pytest.fixture
    def optimizer(self):
        """创建测试优化器实例"""
        import importlib.util

        spec = importlib.util.spec_from_file_location("memory_optimizer", _EXAMPLES_DIR / "02_memory_optimizer.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.MemoryOptimizer()

    @pytest.fixture
    def test_df(self):
        """创建测试数据集（包含各种需要优化的类型）"""
        import numpy as np

        n_rows = 10_000
        data = {
            # 整数列（可以从 int64 优化为更小类型）
            "small_int": np.random.randint(0, 100, n_rows),  # 0-100 -> int8
            "medium_int": np.random.randint(0, 10_000, n_rows),  # 0-10k -> int16
            "large_int": np.random.randint(0, 1_000_000, n_rows),  # 0-1M -> int32
            # 浮点数列（可以从 float64 优化为 float32）
            "price": np.random.uniform(10.0, 1000.0, n_rows),
            "discount": np.random.uniform(0.0, 0.5, n_rows),
            # 高重复字符串列（应转为 category）
            "status": np.random.choice(["active", "inactive", "pending"], n_rows),
            "category": np.random.choice(["A", "B", "C", "D", "E"], n_rows),
            "region": np.random.choice(["North", "South", "East", "West"], n_rows),
            "priority": np.random.choice(["low", "medium", "high"], n_rows),
            # 低重复字符串列（不应转为 category）
            "user_id": [f"USER{i:06d}" for i in range(n_rows)],
            # 稀疏列（大量零值，应使用稀疏数组）
            "rare_event": np.random.choice([0, 1], n_rows, p=[0.98, 0.02]),
        }
        return pd.DataFrame(data)

    def test_analyze_memory_usage(self, optimizer, test_df):
        """测试内存分析功能"""
        analysis = optimizer.analyze_memory_usage(test_df)

        # 验证返回 DataFrame
        assert isinstance(analysis, pd.DataFrame)

        # 验证包含必要的列
        required_columns = [
            "column",
            "dtype",
            "memory_mb",
            "recommended_dtype",
            "potential_savings_mb",
        ]
        for col in required_columns:
            assert col in analysis.columns, f"缺少列: {col}"

        # 验证所有列都被分析
        assert len(analysis) == len(test_df.columns)

        # 验证内存占用为正数
        assert (analysis["memory_mb"] > 0).all()

        # 验证有优化建议
        assert analysis["recommended_dtype"].notna().any()

    def test_optimize_dtypes(self, optimizer, test_df):
        """测试数据类型优化功能"""
        # 记录原始内存
        original_memory = test_df.memory_usage(deep=True).sum()

        # 优化数据类型
        optimized_df = optimizer.optimize_dtypes(test_df.copy())

        # 验证数据完整性（值不变）
        assert len(optimized_df) == len(test_df)
        assert set(optimized_df.columns) == set(test_df.columns)

        # 验证类型优化
        # small_int (0-100) 应优化为 int8
        assert "int8" in str(optimized_df["small_int"].dtype).lower()

        # medium_int (0-10k) 应优化为 int16
        assert "int16" in str(optimized_df["medium_int"].dtype).lower()

        # large_int (0-1M) 应优化为 int32
        assert "int32" in str(optimized_df["large_int"].dtype).lower()

        # 浮点数应优化为 float32
        assert optimized_df["price"].dtype == np.float32
        assert optimized_df["discount"].dtype == np.float32

        # 验证内存减少（optimize_dtypes 只优化数值列，不处理字符串）
        optimized_memory = optimized_df.memory_usage(deep=True).sum()
        memory_reduction = (original_memory - optimized_memory) / original_memory
        # 由于有多个字符串列，数值优化的效果会被稀释，降低期望值
        assert memory_reduction > 0.05, f"内存应至少减少 5%，实际: {memory_reduction * 100:.1f}%"

    def test_convert_to_categorical(self, optimizer, test_df):
        """测试 category 类型转换功能"""
        # 优化前内存
        original_memory = test_df.memory_usage(deep=True).sum()

        # 转换为 categorical（阈值 0.5，即唯一值 < 50% 时转换）
        categorical_df = optimizer.convert_to_categorical(test_df.copy(), threshold=0.5)

        # 验证高重复列转为 category
        assert categorical_df["status"].dtype.name == "category"
        assert categorical_df["category"].dtype.name == "category"

        # 验证低重复列保持不变（user_id 唯一值 = 100%）
        assert categorical_df["user_id"].dtype == test_df["user_id"].dtype

        # 验证数值列不受影响
        assert categorical_df["small_int"].dtype == test_df["small_int"].dtype

        # 验证内存减少
        categorical_memory = categorical_df.memory_usage(deep=True).sum()
        assert categorical_memory < original_memory

    def test_enable_sparse_arrays(self, optimizer, test_df):
        """测试稀疏数组优化功能"""
        # 优化前内存
        original_memory = test_df.memory_usage(deep=True).sum()

        # 启用稀疏数组（稀疏度阈值 0.95）
        sparse_df = optimizer.enable_sparse_arrays(test_df.copy(), sparsity_threshold=0.95)

        # 验证稀疏列转为稀疏数组（rare_event 98% 为 0）
        assert isinstance(sparse_df["rare_event"].dtype, pd.SparseDtype)

        # 验证非稀疏列保持不变
        assert not isinstance(sparse_df["small_int"].dtype, pd.SparseDtype)
        assert not isinstance(sparse_df["price"].dtype, pd.SparseDtype)

        # 验证内存减少
        sparse_memory = sparse_df.memory_usage(deep=True).sum()
        assert sparse_memory < original_memory

    def test_benchmark_optimization(self, optimizer, test_df):
        """测试优化基准测试功能"""
        # 运行优化基准测试
        results = optimizer.benchmark_optimization(test_df)

        # 验证结果结构
        assert isinstance(results, dict)
        required_keys = [
            "original_memory_mb",
            "optimized_memory_mb",
            "memory_reduction_pct",
            "optimization_time",
        ]
        for key in required_keys:
            assert key in results, f"缺少键: {key}"

        # 验证内存减少 >= 50%
        assert results["memory_reduction_pct"] >= 50.0, f"内存应至少减少 50%，实际: {results['memory_reduction_pct']:.1f}%"

        # 验证原始内存大于优化后内存
        assert results["original_memory_mb"] > results["optimized_memory_mb"]

        # 验证优化时间为正数
        assert results["optimization_time"] > 0

    def test_aggressive_optimization(self, optimizer, test_df):
        """测试激进优化模式"""
        # 激进优化（更积极地降级类型）
        aggressive_df = optimizer.optimize_dtypes(test_df.copy(), aggressive=True)

        # 验证数据完整性
        assert len(aggressive_df) == len(test_df)

        # 激进模式应产生更多优化
        normal_df = optimizer.optimize_dtypes(test_df.copy(), aggressive=False)
        aggressive_memory = aggressive_df.memory_usage(deep=True).sum()
        normal_memory = normal_df.memory_usage(deep=True).sum()

        # 激进模式内存应 <= 正常模式
        assert aggressive_memory <= normal_memory

    def test_full_optimization_pipeline(self, optimizer, test_df):
        """测试完整优化流程集成"""
        # 1. 分析内存
        analysis = optimizer.analyze_memory_usage(test_df)
        assert len(analysis) > 0

        # 2. 优化类型
        optimized_df = optimizer.optimize_dtypes(test_df.copy())
        assert optimized_df["small_int"].dtype != test_df["small_int"].dtype

        # 3. 转换 category
        categorical_df = optimizer.convert_to_categorical(optimized_df, threshold=0.5)
        assert categorical_df["status"].dtype.name == "category"

        # 4. 启用稀疏数组
        sparse_df = optimizer.enable_sparse_arrays(categorical_df, sparsity_threshold=0.95)
        assert isinstance(sparse_df["rare_event"].dtype, pd.SparseDtype)

        # 5. 验证最终内存减少
        original_memory = test_df.memory_usage(deep=True).sum()
        final_memory = sparse_df.memory_usage(deep=True).sum()
        reduction = (original_memory - final_memory) / original_memory * 100

        assert reduction >= 50.0, f"完整优化应至少减少 50% 内存，实际: {reduction:.1f}%"


# ============================================================================
# 边界测试和错误处理
# ============================================================================


class TestDataPipelineEdgeCases:
    """测试 DataPipeline 边界情况"""

    @pytest.fixture
    def pipeline(self):
        """创建测试管道实例"""
        import importlib.util

        spec = importlib.util.spec_from_file_location("vectorization_pipeline", _EXAMPLES_DIR / "01_vectorization_pipeline.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.DataPipeline(use_pyarrow=False)

    def test_empty_dataframe(self, pipeline):
        """测试空 DataFrame 处理"""
        df = pd.DataFrame()

        # 清理空 DataFrame 不应崩溃
        cleaned = pipeline.clean_missing_values(df)
        assert len(cleaned) == 0

    def test_single_row_dataframe(self, pipeline):
        """测试单行 DataFrame"""
        df = pd.DataFrame(
            {
                "order_id": [1],
                "user_id": [100],
                "product_id": [200],
                "price": [99.99],
                "quantity": [1],
                "order_date": ["2024-01-01"],
                "status": ["completed"],
                "payment_method": ["credit_card"],
            }
        )

        # 完整管道应能处理单行数据
        cleaned = pipeline.clean_missing_values(df)
        transformed = pipeline.transform_types(cleaned)
        featured = pipeline.calculate_features(transformed)

        assert len(featured) == 1
        assert "total_amount" in featured.columns

    def test_all_missing_values(self, pipeline):
        """测试全 NaN 列"""
        df = pd.DataFrame({"order_id": [1, 2, 3], "price": [np.nan, np.nan, np.nan], "quantity": [1, 2, 3]})

        # 清理后应删除全 NaN 列或填充
        cleaned = pipeline.clean_missing_values(df)
        # price 列应被处理（删除或填充）
        assert "order_id" in cleaned.columns
        assert "quantity" in cleaned.columns

    def test_extreme_values(self, pipeline):
        """测试极端值"""
        df = pd.DataFrame(
            {
                "order_id": [1, 2, 3],
                "user_id": [1, 2, 3],
                "product_id": [1, 2, 3],
                "price": [0.01, 999999.99, 50.0],  # 极小和极大值
                "quantity": [1, 1000, 5],  # 正常和极大数量
                "order_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "status": ["completed", "pending", "cancelled"],
                "payment_method": ["credit_card", "paypal", "bank_transfer"],
            }
        )

        cleaned = pipeline.clean_missing_values(df)
        transformed = pipeline.transform_types(cleaned)
        featured = pipeline.calculate_features(transformed)

        # 应能处理极端值
        assert len(featured) == 3
        assert featured["total_amount"].max() > 999999

    def test_duplicate_rows(self, pipeline):
        """测试重复行处理"""
        df = pd.DataFrame(
            {
                "order_id": [1, 1, 2],  # 重复的 order_id
                "user_id": [100, 100, 200],
                "product_id": [1, 1, 2],
                "price": [10.0, 10.0, 20.0],
                "quantity": [1, 1, 2],
                "order_date": ["2024-01-01", "2024-01-01", "2024-01-02"],
                "status": ["completed", "completed", "pending"],
                "payment_method": ["credit_card", "credit_card", "paypal"],
            }
        )

        # 管道应能处理重复数据（即使不去重）
        cleaned = pipeline.clean_missing_values(df)
        assert len(cleaned) >= 2  # 可能去重也可能不去重

    def test_invalid_date_format(self, pipeline):
        """测试无效日期格式"""
        df = pd.DataFrame(
            {
                "order_id": [1, 2, 3],
                "user_id": [1, 2, 3],
                "product_id": [1, 2, 3],
                "price": [10.0, 20.0, 30.0],
                "quantity": [1, 2, 3],
                "order_date": ["2024-01-01", "invalid-date", "2024-01-03"],
                "status": ["completed", "pending", "cancelled"],
                "payment_method": ["credit_card", "paypal", "bank_transfer"],
            }
        )

        # 应能处理无效日期（转换为 NaT 或删除）
        cleaned = pipeline.clean_missing_values(df)
        transformed = pipeline.transform_types(cleaned)
        # 不应崩溃
        assert len(transformed) >= 2


class TestMemoryOptimizerEdgeCases:
    """测试 MemoryOptimizer 边界情况"""

    @pytest.fixture
    def optimizer(self):
        """创建测试优化器实例"""
        import importlib.util

        spec = importlib.util.spec_from_file_location("memory_optimizer", _EXAMPLES_DIR / "02_memory_optimizer.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.MemoryOptimizer()

    def test_empty_dataframe_optimization(self, optimizer):
        """测试空 DataFrame 优化"""
        df = pd.DataFrame()

        # 空 DataFrame 优化不应崩溃
        optimized = optimizer.optimize_dtypes(df)
        assert len(optimized) == 0

    def test_single_column_optimization(self, optimizer):
        """测试单列优化"""
        df = pd.DataFrame({"value": [1, 2, 3, 4, 5]})

        optimized = optimizer.optimize_dtypes(df)
        assert "value" in optimized.columns
        # 应优化为更小的整数类型
        assert optimized["value"].dtype != "int64"

    def test_all_string_columns(self, optimizer):
        """测试全字符串列"""
        df = pd.DataFrame({"col1": ["a", "b", "c"], "col2": ["x", "y", "z"]})

        optimized = optimizer.optimize_dtypes(df)
        # 字符串列应保持不变或转为 category
        assert len(optimized) == 3

    def test_mixed_nan_values(self, optimizer):
        """测试混合 NaN 值"""
        df = pd.DataFrame(
            {
                "int_col": [1, 2, np.nan, 4, 5],
                "float_col": [1.1, np.nan, 3.3, 4.4, 5.5],
                "str_col": ["a", "b", None, "d", "e"],
            }
        )

        # 优化应保留 NaN 值
        optimized = optimizer.optimize_dtypes(df)
        assert optimized["float_col"].isna().sum() == 1
        assert optimized["str_col"].isna().sum() == 1

    def test_negative_values(self, optimizer):
        """测试负数优化"""
        df = pd.DataFrame({"value": [-100, -50, 0, 50, 100]})

        optimized = optimizer.optimize_dtypes(df)
        # 应能正确处理负数范围
        assert optimized["value"].min() == -100
        assert optimized["value"].max() == 100

    def test_boolean_columns(self, optimizer):
        """测试布尔列优化"""
        df = pd.DataFrame({"flag": [True, False, True, False, True]})

        optimized = optimizer.optimize_dtypes(df)
        # 布尔列应保持布尔类型
        assert optimized["flag"].dtype == bool

    def test_categorical_with_few_unique(self, optimizer):
        """测试少量唯一值的分类转换"""
        df = pd.DataFrame({"category": ["A", "B", "A", "B", "A", "B"] * 100})

        # 应转为 category 类型
        categorical_df = optimizer.convert_to_categorical(df, threshold=0.5)
        assert categorical_df["category"].dtype.name == "category"

    def test_categorical_with_many_unique(self, optimizer):
        """测试大量唯一值的分类"""
        df = pd.DataFrame({"unique_id": range(1000)})

        # 不应转为 category（唯一值太多）
        categorical_df = optimizer.convert_to_categorical(df, threshold=0.5)
        assert categorical_df["unique_id"].dtype.name != "category"

    def test_sparse_with_zeros(self, optimizer):
        """测试稀疏数组（大量零）"""
        df = pd.DataFrame({"sparse_col": [0] * 95 + [1, 2, 3, 4, 5]})

        sparse_df = optimizer.enable_sparse_arrays(df, sparsity_threshold=0.9)
        # 应转为稀疏数组
        assert isinstance(sparse_df["sparse_col"].dtype, pd.SparseDtype)

    def test_no_optimization_needed(self, optimizer):
        """测试不需要优化的情况"""
        df = pd.DataFrame(
            {
                "already_int8": pd.array([1, 2, 3], dtype="int8"),
                "already_category": pd.Categorical(["A", "B", "C"]),
            }
        )

        optimized = optimizer.optimize_dtypes(df)
        # 已优化的类型应保持不变或被进一步优化（如 int8 -> uint8）
        assert optimized["already_int8"].dtype in ["int8", "uint8"]
        # category 类型应保持
        assert isinstance(optimized["already_category"].dtype, pd.CategoricalDtype)
