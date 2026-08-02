"""L16 Pandas 高性能数据处理 - 集成测试

from __future__ import annotations

端到端测试完整的数据处理流程:
1. test_full_pipeline_integration: 加载 → 清洗 → 转换 → 分析
2. test_memory_optimization_integration: 分析 → 优化 → 验证
3. test_combined_optimization_integration: 管道 + 内存优化组合
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("numpy", reason="需要 numpy/pandas 数据栈（uv sync --extra ai）")
pytest.importorskip("pandas", reason="需要 pandas 数据栈（uv sync --extra ai）")

import numpy as np
import pandas as pd

# sys.path 注入由同目录 conftest.py 统一管理，严禁在此污染
_LESSON_ROOT = Path(__file__).parent.parent
_EXAMPLES_DIR = _LESSON_ROOT / "examples"


@pytest.fixture
def data_pipeline():
    """创建 DataPipeline 实例"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("vectorization_pipeline", _EXAMPLES_DIR / "01_vectorization_pipeline.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.DataPipeline(use_pyarrow=False)  # 使用 NumPy 后端以确保兼容性


@pytest.fixture
def memory_optimizer():
    """创建 MemoryOptimizer 实例"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("memory_optimizer", _EXAMPLES_DIR / "02_memory_optimizer.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.MemoryOptimizer()


class TestFullPipelineIntegration:
    """测试完整数据处理管道的端到端流程"""

    def test_full_pipeline_integration(self, data_pipeline, sample_orders_path):
        """端到端测试: 加载 → 清洗 → 转换 → 分析

        验证完整流程:
        1. 加载数据（前 10000 行用于快速测试）
        2. 清洗缺失值
        3. 优化数据类型
        4. 计算派生特征
        5. 验证数据质量和完整性
        """
        # 步骤 1: 加载数据
        df = data_pipeline.load_data(str(sample_orders_path), chunksize=10_000)

        # 验证加载成功
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert len(df) <= 10_000  # 不超过 chunksize
        assert "load_time" in data_pipeline._performance_stats

        # 记录原始数据信息
        original_shape = df.shape
        original_columns = set(df.columns)

        # 步骤 2: 清洗缺失值
        df_cleaned = data_pipeline.clean_missing_values(df)

        # 验证清洗效果
        assert isinstance(df_cleaned, pd.DataFrame)
        assert df_cleaned.shape[0] == original_shape[0]  # 行数不变
        assert df_cleaned.isna().sum().sum() == 0  # 无缺失值
        assert "clean_time" in data_pipeline._performance_stats

        # 步骤 3: 优化数据类型
        df_transformed = data_pipeline.transform_types(df_cleaned)

        # 验证类型优化
        assert isinstance(df_transformed, pd.DataFrame)
        assert df_transformed.shape == df_cleaned.shape  # 形状不变
        assert "transform_time" in data_pipeline._performance_stats

        # 验证内存优化效果
        memory_before = df_cleaned.memory_usage(deep=True).sum()
        memory_after = df_transformed.memory_usage(deep=True).sum()
        assert memory_after <= memory_before  # 内存不增加

        # 步骤 4: 计算派生特征
        df_final = data_pipeline.calculate_features(df_transformed)

        # 验证特征计算
        assert isinstance(df_final, pd.DataFrame)
        assert df_final.shape[0] == original_shape[0]  # 行数不变

        # 验证新特征存在
        new_features = {"total_amount", "price_category", "is_high_value"}
        assert new_features.issubset(set(df_final.columns))

        # 验证原始列仍然存在
        assert original_columns.issubset(set(df_final.columns))

        # 验证特征值的合理性
        # 注意: 数据中可能存在负数 quantity（脏数据），因此 total_amount 可能为负
        assert df_final["total_amount"].notna().all()  # 无缺失值
        assert set(df_final["price_category"].unique()).issubset({"low", "medium", "high", "unknown"})
        assert df_final["is_high_value"].dtype == bool
        assert "feature_time" in data_pipeline._performance_stats

        # 步骤 5: 验证数据完整性
        # 检查数据一致性：total_amount = price * quantity
        calculated_total = df_final["price"] * df_final["quantity"]
        assert np.allclose(df_final["total_amount"], calculated_total, rtol=1e-3, atol=1e-6)

        # 检查价格分类逻辑
        low_price_mask = df_final["price_category"] == "low"
        if low_price_mask.any():
            assert (df_final.loc[low_price_mask, "price"] < 100).all()

        high_price_mask = df_final["price_category"] == "high"
        if high_price_mask.any():
            assert (df_final.loc[high_price_mask, "price"] >= 500).all()

        # 检查高价值订单标记逻辑
        high_value_mask = df_final["is_high_value"]
        assert (df_final.loc[high_value_mask, "total_amount"] > 500).all()

        low_value_mask = ~df_final["is_high_value"]
        assert (df_final.loc[low_value_mask, "total_amount"] <= 500).all()

        print(f"✅ 完整管道测试通过: {original_shape[0]:,} 行处理完成")
        print(f"   - 原始列数: {len(original_columns)}")
        print(f"   - 最终列数: {len(df_final.columns)}")
        print(f"   - 新增特征: {len(df_final.columns) - len(original_columns)}")

    def test_pipeline_performance_stats(self, data_pipeline, sample_orders_path):
        """测试管道性能统计信息的收集"""
        # 执行完整流程
        df = data_pipeline.load_data(str(sample_orders_path), chunksize=5_000)
        df = data_pipeline.clean_missing_values(df)
        df = data_pipeline.transform_types(df)
        df = data_pipeline.calculate_features(df)

        # 验证所有性能指标都被记录
        expected_stats = {"load_time", "clean_time", "transform_time", "feature_time"}
        assert expected_stats.issubset(set(data_pipeline._performance_stats.keys()))

        # 验证所有指标都是正数
        for stat_name, stat_value in data_pipeline._performance_stats.items():
            if stat_name != "benchmark":
                assert stat_value > 0, f"{stat_name} 应该是正数"

        # 生成并验证报告
        report = data_pipeline.generate_report()
        assert isinstance(report, str)
        assert len(report) > 0
        assert "性能报告" in report

        print("✅ 性能统计测试通过")
        print(report)


class TestMemoryOptimizationIntegration:
    """测试内存优化的端到端流程"""

    def test_memory_optimization_integration(self, memory_optimizer, sample_orders_path):
        """端到端测试: 分析 → 优化 → 验证

        验证完整优化流程:
        1. 加载原始数据
        2. 分析内存使用情况
        3. 优化数据类型
        4. 转换为 category 类型
        5. 验证内存节省效果
        6. 验证数据完整性
        """
        # 步骤 1: 加载原始数据
        df = pd.read_csv(sample_orders_path, nrows=10_000)
        original_memory = df.memory_usage(deep=True).sum() / (1024**2)  # MB
        original_shape = df.shape

        print(f"\n📊 原始数据: {original_shape[0]:,} 行 × {original_shape[1]} 列")
        print(f"💾 原始内存: {original_memory:.2f} MB")

        # 步骤 2: 分析内存使用情况
        analysis = memory_optimizer.analyze_memory_usage(df)

        # 验证分析报告
        assert isinstance(analysis, pd.DataFrame)
        assert len(analysis) == len(df.columns)
        assert set(analysis.columns) == {
            "column",
            "dtype",
            "memory_mb",
            "recommended_dtype",
            "potential_savings_mb",
        }

        # 验证分析数据的合理性
        assert (analysis["memory_mb"] >= 0).all()
        assert (analysis["potential_savings_mb"] >= 0).all()

        total_potential_savings = analysis["potential_savings_mb"].sum()
        print(f"💰 潜在节省: {total_potential_savings:.2f} MB")

        # 步骤 3: 优化数据类型
        df_optimized = memory_optimizer.optimize_dtypes(df, aggressive=False)

        # 验证优化后的数据结构
        assert isinstance(df_optimized, pd.DataFrame)
        assert df_optimized.shape == original_shape  # 形状不变
        assert set(df_optimized.columns) == set(df.columns)  # 列不变

        # 验证内存减少
        optimized_memory_step1 = df_optimized.memory_usage(deep=True).sum() / (1024**2)
        assert optimized_memory_step1 <= original_memory
        memory_saved_step1 = (1 - optimized_memory_step1 / original_memory) * 100
        print(f"📉 类型优化后: {optimized_memory_step1:.2f} MB (-{memory_saved_step1:.1f}%)")

        # 步骤 4: 转换为 category 类型
        df_categorical = memory_optimizer.convert_to_categorical(df_optimized, threshold=0.5)

        # 验证 category 转换
        assert isinstance(df_categorical, pd.DataFrame)
        assert df_categorical.shape == original_shape

        # 验证高重复列被转换为 category
        for col in df_categorical.columns:
            if df_categorical[col].dtype.name == "category":
                # 验证重复率确实高
                unique_ratio = df[col].nunique() / len(df)
                assert unique_ratio < 0.5, f"{col} 被转换为 category，但重复率不足 50%"

        # 验证内存进一步减少
        optimized_memory_step2 = df_categorical.memory_usage(deep=True).sum() / (1024**2)
        assert optimized_memory_step2 <= optimized_memory_step1
        memory_saved_step2 = (1 - optimized_memory_step2 / original_memory) * 100
        print(f"📉 Category 转换后: {optimized_memory_step2:.2f} MB (-{memory_saved_step2:.1f}%)")

        # 步骤 5: 验证数据完整性
        # 对于数值列，验证值没有改变
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                original_values = df[col].fillna(-999)
                optimized_values = df_categorical[col].fillna(-999)

                # 使用相对误差检查（允许浮点精度损失）
                if pd.api.types.is_float_dtype(df[col]):
                    assert np.allclose(original_values, optimized_values, rtol=1e-3, atol=1e-6)
                else:
                    assert (original_values == optimized_values).all()

        # 对于字符串列，验证值没有改变
        for col in df.columns:
            if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
                # 分类列需先转回 object 再 fillna，否则 pandas 2.x 拒绝插入新 category
                original_values = df[col].fillna("__NULL__").astype(str)
                optimized_values = df_categorical[col].astype(object).fillna("__NULL__").astype(str)
                assert (original_values == optimized_values).all()

        # 步骤 6: 验证总体优化效果
        total_memory_saved = (1 - optimized_memory_step2 / original_memory) * 100
        assert total_memory_saved >= 0  # 至少不增加内存

        print("✅ 内存优化测试通过")
        print(f"   - 总内存节省: {total_memory_saved:.1f}%")
        print(f"   - 原始内存: {original_memory:.2f} MB")
        print(f"   - 最终内存: {optimized_memory_step2:.2f} MB")

    def test_benchmark_optimization(self, memory_optimizer, sample_orders_path):
        """测试优化基准测试功能"""
        # 加载测试数据
        df = pd.read_csv(sample_orders_path, nrows=5_000)

        # 执行基准测试
        results = memory_optimizer.benchmark_optimization(df)

        # 验证结果结构
        assert isinstance(results, dict)
        expected_keys = {
            "original_memory_mb",
            "optimized_memory_mb",
            "memory_reduction_pct",
            "optimization_time",
        }
        assert set(results.keys()) == expected_keys

        # 验证结果合理性
        assert results["original_memory_mb"] > 0
        assert results["optimized_memory_mb"] > 0
        assert results["optimized_memory_mb"] <= results["original_memory_mb"]
        assert results["memory_reduction_pct"] >= 0
        assert results["memory_reduction_pct"] <= 100
        assert results["optimization_time"] > 0

        print("✅ 基准测试通过")
        print(f"   - 原始内存: {results['original_memory_mb']:.2f} MB")
        print(f"   - 优化后: {results['optimized_memory_mb']:.2f} MB")
        print(f"   - 内存减少: {results['memory_reduction_pct']:.1f}%")
        print(f"   - 耗时: {results['optimization_time']:.3f}s")


class TestCombinedOptimizationIntegration:
    """测试管道和内存优化的组合使用"""

    def test_combined_optimization_integration(self, data_pipeline, memory_optimizer, sample_orders_path):
        """端到端测试: 完整流程 + 内存优化

        验证最佳实践：先清洗和特征工程，再优化内存
        """
        # 阶段 1: 数据处理管道
        print("\n=== 阶段 1: 数据处理管道 ===")

        df = data_pipeline.load_data(str(sample_orders_path), chunksize=10_000)
        df = data_pipeline.clean_missing_values(df)
        df = data_pipeline.calculate_features(df)

        # 记录处理后的内存
        memory_before_optimization = df.memory_usage(deep=True).sum() / (1024**2)
        print(f"处理后内存: {memory_before_optimization:.2f} MB")

        # 阶段 2: 内存优化
        print("\n=== 阶段 2: 内存优化 ===")

        analysis = memory_optimizer.analyze_memory_usage(df)
        print(f"可优化列数: {len(analysis[analysis['potential_savings_mb'] > 0])}")

        df_optimized = memory_optimizer.optimize_dtypes(df, aggressive=False)
        df_optimized = memory_optimizer.convert_to_categorical(df_optimized, threshold=0.5)

        # 验证最终结果
        memory_after_optimization = df_optimized.memory_usage(deep=True).sum() / (1024**2)
        total_reduction = (1 - memory_after_optimization / memory_before_optimization) * 100

        print(f"优化后内存: {memory_after_optimization:.2f} MB")
        print(f"总内存节省: {total_reduction:.1f}%")

        # 验证数据质量
        assert df_optimized.shape[0] == df.shape[0]  # 行数不变
        assert set(df_optimized.columns) == set(df.columns)  # 列不变

        # 验证派生特征的正确性（允许浮点误差）
        assert np.allclose(
            df_optimized["total_amount"],
            df_optimized["price"] * df_optimized["quantity"],
            rtol=1e-3,
        )

        # 验证内存确实减少
        assert memory_after_optimization <= memory_before_optimization

        print("\n✅ 组合优化测试通过")
        print(f"   - 最终形状: {df_optimized.shape}")
        print(f"   - 总内存节省: {total_reduction:.1f}%")

    def test_integration_performance_within_limit(self, data_pipeline, memory_optimizer, sample_orders_path):
        """测试集成测试在合理时间内完成（< 10秒）"""
        import time

        start_time = time.time()

        # 执行完整流程
        df = data_pipeline.load_data(str(sample_orders_path), chunksize=5_000)
        df = data_pipeline.clean_missing_values(df)
        df = data_pipeline.transform_types(df)
        df = data_pipeline.calculate_features(df)

        df = memory_optimizer.optimize_dtypes(df)
        df = memory_optimizer.convert_to_categorical(df)

        total_time = time.time() - start_time

        # 验证时间在合理范围内
        assert total_time < 10.0, f"集成测试耗时过长: {total_time:.2f}s > 10s"

        print(f"✅ 性能测试通过: 总耗时 {total_time:.2f}s")
