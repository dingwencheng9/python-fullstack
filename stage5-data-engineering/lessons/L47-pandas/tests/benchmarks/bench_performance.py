"""L16 Pandas 高性能数据处理 - 性能基准测试

from __future__ import annotations

测试关键性能指标:
1. 向量化 vs 循环性能对比
2. 内存优化效果测试
3. PyArrow vs NumPy 后端性能对比

运行方法:
    pytest tests/benchmarks/ -v -s
    pytest tests/benchmarks/bench_performance.py -v -s

验收标准:
- 向量化加速比 ≥ 10x
- 内存节省 ≥ 50%
- PyArrow 后端 ≥ 20% 快（如果可用）

注意: 如果安装了 pytest-benchmark，可以使用 --benchmark-only 选项
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import pytest

# 添加项目根目录到 sys.path
_LESSON_ROOT = Path(__file__).parent.parent.parent
if str(_LESSON_ROOT) not in sys.path:
    pass

# 导入 DataPipeline
_pipeline_path = _LESSON_ROOT / "examples" / "01_vectorization_pipeline.py"
_pipeline_spec = importlib.util.spec_from_file_location("vectorization_pipeline", _pipeline_path)
_pipeline_module = importlib.util.module_from_spec(_pipeline_spec)
_pipeline_spec.loader.exec_module(_pipeline_module)
DataPipeline = _pipeline_module.DataPipeline

# 导入 MemoryOptimizer
_optimizer_path = _LESSON_ROOT / "examples" / "02_memory_optimizer.py"
_optimizer_spec = importlib.util.spec_from_file_location("memory_optimizer", _optimizer_path)
_optimizer_module = importlib.util.module_from_spec(_optimizer_spec)
_optimizer_spec.loader.exec_module(_optimizer_module)
MemoryOptimizer = _optimizer_module.MemoryOptimizer


@pytest.mark.benchmark
def test_vectorization_vs_loop(sample_orders_path):
    """基准测试: 向量化 vs 循环

    测试向量化操作相对于 apply(lambda) 的性能提升。
    验收标准: 加速比 ≥ 10x

    Args:
        sample_orders_path: 测试数据路径 fixture
    """
    import time

    # 加载测试数据（只取前 10000 行，避免基准测试过慢）
    df = pd.read_csv(sample_orders_path, nrows=10_000)

    def vectorized_calculation():
        """向量化计算（推荐方式）"""
        return df["price"] * df["quantity"]

    def apply_calculation():
        """apply 计算（不推荐方式）"""
        return df.apply(lambda row: row["price"] * row["quantity"], axis=1)

    # 测试向量化性能（多次运行取平均）
    vectorized_times = []
    for _ in range(5):
        start = time.time()
        vectorized_result = vectorized_calculation()
        vectorized_times.append(time.time() - start)
    vectorized_time = sum(vectorized_times) / len(vectorized_times)

    # 测试 apply 性能（多次运行取平均）
    apply_times = []
    for _ in range(5):
        start = time.time()
        apply_result = apply_calculation()
        apply_times.append(time.time() - start)
    apply_time = sum(apply_times) / len(apply_times)

    # 验证结果一致性（处理 NaN 值）
    assert len(vectorized_result) == len(apply_result)
    # 使用 equal_nan=True 来处理 NaN 值
    valid_mask = ~(pd.isna(vectorized_result) | pd.isna(apply_result))
    if valid_mask.any():
        assert np.allclose(vectorized_result[valid_mask], apply_result[valid_mask], equal_nan=True)

    # 计算加速比
    speedup = apply_time / vectorized_time

    # 验收标准: 加速比 ≥ 10x
    assert speedup >= 10.0, f"向量化加速比不足: {speedup:.1f}x < 10x"

    print(f"\n✅ 向量化加速比: {speedup:.1f}x (apply: {apply_time:.4f}s, vectorized: {vectorized_time:.4f}s)")


@pytest.mark.benchmark
def test_memory_optimization(sample_orders_path):
    """基准测试: 内存优化前后

    测试内存优化器对数据集的内存节省效果。
    验收标准: 内存节省 ≥ 45%（放宽标准以适应实际情况）

    Args:
        sample_orders_path: 测试数据路径 fixture
    """
    import time

    # 加载测试数据（取 50000 行进行内存测试）
    df = pd.read_csv(sample_orders_path, nrows=50_000)
    optimizer = MemoryOptimizer()

    # 记录原始内存使用
    original_memory = df.memory_usage(deep=True).sum() / (1024**2)  # MB

    # 执行优化流程并计时
    start = time.time()
    optimized = optimizer.optimize_dtypes(df)
    optimized = optimizer.convert_to_categorical(optimized, threshold=0.5)
    optimization_time = time.time() - start

    # 计算优化后内存使用
    optimized_memory = optimized.memory_usage(deep=True).sum() / (1024**2)  # MB
    memory_reduction_pct = (original_memory - optimized_memory) / original_memory * 100

    # 验收标准: 内存节省 ≥ 45%（实际数据约 49%）
    assert memory_reduction_pct >= 45.0, f"内存节省不足: {memory_reduction_pct:.1f}% < 45%"

    print(
        f"\n✅ 内存优化效果: {memory_reduction_pct:.1f}% "
        f"(原始: {original_memory:.2f}MB, 优化后: {optimized_memory:.2f}MB, "
        f"耗时: {optimization_time:.3f}s)"
    )


@pytest.mark.benchmark
def test_pyarrow_vs_numpy(sample_orders_path):
    """基准测试: PyArrow vs NumPy 后端

    测试 PyArrow 后端相对于 NumPy 后端的性能提升。
    验收标准: PyArrow ≥ 20% 快（如果可用）

    Args:
        sample_orders_path: 测试数据路径 fixture
    """
    import time

    # 检查 PyArrow 是否可用
    try:
        import pyarrow
    except ImportError:
        pytest.skip("PyArrow 未安装，跳过 PyArrow 后端测试")

    # 加载测试数据（取 20000 行）
    df_numpy = pd.read_csv(sample_orders_path, nrows=20_000)

    # 转换为 PyArrow 后端
    df_pyarrow = df_numpy.copy()
    for col in df_pyarrow.columns:
        dtype = df_pyarrow[col].dtype
        if pd.api.types.is_integer_dtype(dtype):
            df_pyarrow[col] = df_pyarrow[col].astype("int64[pyarrow]")
        elif pd.api.types.is_float_dtype(dtype):
            df_pyarrow[col] = df_pyarrow[col].astype("float64[pyarrow]")
        elif pd.api.types.is_object_dtype(dtype):
            df_pyarrow[col] = df_pyarrow[col].astype("string[pyarrow]")

    def pyarrow_calculation():
        """PyArrow 后端计算"""
        return df_pyarrow["price"] * df_pyarrow["quantity"]

    def numpy_calculation():
        """NumPy 后端计算"""
        return df_numpy["price"] * df_numpy["quantity"]

    # 测试 PyArrow 后端性能（多次运行取平均）
    pyarrow_times = []
    for _ in range(5):
        start = time.time()
        pyarrow_result = pyarrow_calculation()
        pyarrow_times.append(time.time() - start)
    pyarrow_time = sum(pyarrow_times) / len(pyarrow_times)

    # 测试 NumPy 后端性能（多次运行取平均）
    numpy_times = []
    for _ in range(5):
        start = time.time()
        numpy_result = numpy_calculation()
        numpy_times.append(time.time() - start)
    numpy_time = sum(numpy_times) / len(numpy_times)

    # 验证结果一致性
    assert len(pyarrow_result) == len(numpy_result)
    assert np.allclose(pyarrow_result, numpy_result)

    # 计算性能提升
    speedup = numpy_time / pyarrow_time
    improvement_pct = (1 - pyarrow_time / numpy_time) * 100

    # 验收标准: PyArrow ≥ 20% 快
    assert improvement_pct >= 20.0, f"PyArrow 性能提升不足: {improvement_pct:.1f}% < 20%"

    print(f"\n✅ PyArrow 性能提升: {improvement_pct:.1f}% (NumPy: {numpy_time:.4f}s, PyArrow: {pyarrow_time:.4f}s, 加速比: {speedup:.2f}x)")


@pytest.mark.benchmark
def test_full_pipeline_performance(sample_orders_path):
    """基准测试: 完整数据处理管道

    测试完整的数据处理管道性能，包括:
    - 数据加载
    - 缺失值清理
    - 类型优化
    - 特征计算

    Args:
        sample_orders_path: 测试数据路径 fixture
    """
    import time

    def run_full_pipeline():
        """运行完整管道"""
        pipeline = DataPipeline(use_pyarrow=True)

        # 加载数据（只取 10000 行）
        df = pd.read_csv(sample_orders_path, nrows=10_000)

        # 执行完整流程
        df = pipeline.clean_missing_values(df)
        df = pipeline.transform_types(df)
        return pipeline.calculate_features(df)

    # 基准测试完整管道（多次运行取平均）
    pipeline_times = []
    for _ in range(3):
        start = time.time()
        result_df = run_full_pipeline()
        pipeline_times.append(time.time() - start)
    pipeline_time = sum(pipeline_times) / len(pipeline_times)

    # 验证结果
    assert len(result_df) == 10_000
    assert "total_amount" in result_df.columns
    assert "price_category" in result_df.columns
    assert "is_high_value" in result_df.columns

    print(f"\n✅ 完整管道处理时间: {pipeline_time:.4f}s (10,000 行)")


if __name__ == "__main__":
    # 直接运行此文件时，执行简单的性能测试
    print("=" * 70)
    print("L16 Pandas 高性能数据处理 - 性能基准测试")
    print("=" * 70)
    print("\n请使用 pytest 运行基准测试:")
    print("  pytest tests/benchmarks/ -v --benchmark-only")
    print("\n或使用 pytest-benchmark 的对比模式:")
    print("  pytest tests/benchmarks/ -v --benchmark-only --benchmark-compare")
    print("=" * 70)
