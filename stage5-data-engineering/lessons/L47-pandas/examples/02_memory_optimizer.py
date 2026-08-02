"""示例 2: 内存优化器

from __future__ import annotations

演示如何优化 Pandas DataFrame 的内存占用，减少 50%+ 的内存使用。

核心技术:
- 整数类型降级 (int64 → int8/int16/int32)
- 浮点类型降级 (float64 → float32)
- Category 类型转换（高重复字符串）
- 稀疏数组优化（高稀疏度数据）
"""

from __future__ import annotations

import time
from typing import Any

import numpy as np
import pandas as pd


class MemoryOptimizer:
    """内存优化工具

    提供多种内存优化策略:
    1. 分析内存使用情况
    2. 优化数据类型（整数/浮点降级）
    3. 转换为 category 类型（高重复字符串）
    4. 启用稀疏数组（高稀疏度数据）
    5. 性能基准测试

    Example:
        >>> optimizer = MemoryOptimizer()
        >>> analysis = optimizer.analyze_memory_usage(df)
        >>> optimized_df = optimizer.optimize_dtypes(df)
        >>> categorical_df = optimizer.convert_to_categorical(optimized_df)
        >>> sparse_df = optimizer.enable_sparse_arrays(categorical_df)
        >>> results = optimizer.benchmark_optimization(df)
    """

    def analyze_memory_usage(self, df: pd.DataFrame) -> pd.DataFrame:
        """分析 DataFrame 的内存使用情况

        为每一列生成内存分析报告，包括当前类型、内存占用、
        推荐类型和潜在节省。

        Args:
            df: 待分析的 DataFrame

        Returns:
            分析报告 DataFrame，包含以下列:
            - column: 列名
            - dtype: 当前数据类型
            - memory_mb: 内存占用 (MB)
            - recommended_dtype: 推荐的数据类型
            - potential_savings_mb: 潜在节省 (MB)

        Example:
            >>> analysis = optimizer.analyze_memory_usage(df)
            >>> print(analysis.sort_values("potential_savings_mb", ascending=False))
        """
        analysis_data = []

        for col in df.columns:
            col_data = df[col]
            current_dtype = str(col_data.dtype)
            current_memory = col_data.memory_usage(deep=True) / (1024**2)  # MB

            # 推荐类型和潜在节省
            recommended_dtype, potential_savings = self._recommend_dtype(col_data)

            analysis_data.append(
                {
                    "column": col,
                    "dtype": current_dtype,
                    "memory_mb": current_memory,
                    "recommended_dtype": recommended_dtype,
                    "potential_savings_mb": potential_savings,
                }
            )

        analysis_df = pd.DataFrame(analysis_data)
        return analysis_df.sort_values("potential_savings_mb", ascending=False)

    def _recommend_dtype(self, series: pd.Series) -> tuple[str, float]:
        """为单列推荐最佳数据类型

        Args:
            series: 待分析的列

        Returns:
            (推荐类型, 潜在节省MB)
        """
        current_memory = series.memory_usage(deep=True) / (1024**2)
        current_dtype = series.dtype

        # 整数类型优化
        if pd.api.types.is_integer_dtype(current_dtype):
            max_val = series.max()
            min_val = series.min()

            if min_val >= 0:  # 无符号整数
                if max_val < 256:
                    return "uint8", current_memory * 0.875
                if max_val < 65536:
                    return "uint16", current_memory * 0.75
                if max_val < 4294967296:
                    return "uint32", current_memory * 0.5
            else:  # 有符号整数
                if min_val >= -128 and max_val < 128:
                    return "int8", current_memory * 0.875
                if min_val >= -32768 and max_val < 32768:
                    return "int16", current_memory * 0.75
                if min_val >= -2147483648 and max_val < 2147483648:
                    return "int32", current_memory * 0.5

        # 浮点类型优化
        elif pd.api.types.is_float_dtype(current_dtype) and current_dtype == np.float64:
            return "float32", current_memory * 0.5

        # 字符串类型优化
        elif pd.api.types.is_object_dtype(current_dtype) or pd.api.types.is_string_dtype(current_dtype):
            if series.nunique() / len(series) < 0.5:  # 重复率 > 50%
                return "category", current_memory * 0.7

        return str(current_dtype), 0.0

    def optimize_dtypes(self, df: pd.DataFrame, aggressive: bool = False) -> pd.DataFrame:
        """优化 DataFrame 的数据类型

        将整数和浮点数降级为更小的类型，减少内存占用。

        Args:
            df: 待优化的 DataFrame
            aggressive: 是否启用激进优化模式（可能损失精度）

        Returns:
            优化后的 DataFrame（新副本）

        Example:
            >>> optimized_df = optimizer.optimize_dtypes(df)
            >>> aggressive_df = optimizer.optimize_dtypes(df, aggressive=True)
        """
        df_optimized = df.copy()

        for col in df_optimized.columns:
            col_data = df_optimized[col]
            dtype = col_data.dtype

            # 整数类型优化
            if pd.api.types.is_integer_dtype(dtype):
                df_optimized[col] = self._optimize_integer(col_data)

            # 浮点类型优化
            elif pd.api.types.is_float_dtype(dtype):
                df_optimized[col] = self._optimize_float(col_data, aggressive)

        return df_optimized

    def _optimize_integer(self, series: pd.Series) -> pd.Series:
        """优化整数列的数据类型"""
        col_min, col_max = series.min(), series.max()

        if col_min >= 0:  # 无符号整数
            if col_max < 256:
                return series.astype(np.uint8)
            if col_max < 65536:
                return series.astype(np.uint16)
            if col_max < 4294967296:
                return series.astype(np.uint32)
            return series.astype(np.uint64)
        # 有符号整数
        if col_min >= -128 and col_max < 128:
            return series.astype(np.int8)
        if col_min >= -32768 and col_max < 32768:
            return series.astype(np.int16)
        if col_min >= -2147483648 and col_max < 2147483648:
            return series.astype(np.int32)
        return series.astype(np.int64)

    def _optimize_float(self, series: pd.Series, aggressive: bool) -> pd.Series:
        """优化浮点列的数据类型"""
        if series.dtype != np.float64:
            return series

        if aggressive:
            return series.astype(np.float32)

        # 保守模式：检查精度损失
        converted = series.astype(np.float32)
        max_error = np.abs(series - converted.astype(np.float64)).max()
        relative_error = max_error / (series.abs().max() + 1e-10)

        return converted if relative_error < 0.001 else series

    def convert_to_categorical(self, df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
        """将高重复列转换为 category 类型

        对于唯一值比例 < threshold 的对象列，转换为 category。
        category 类型节省内存：存储整数索引而非重复字符串。

        Args:
            df: 待转换的 DataFrame
            threshold: 唯一值比例阈值（默认 0.5，即重复率 > 50%）

        Returns:
            转换后的 DataFrame（新副本）
        """
        df_categorical = df.copy()

        for col in df_categorical.columns:
            col_data = df_categorical[col]

            # 处理对象类型或字符串类型列
            if pd.api.types.is_object_dtype(col_data.dtype) or pd.api.types.is_string_dtype(col_data.dtype):
                if col_data.nunique() / len(col_data) < threshold:
                    df_categorical[col] = col_data.astype("category")

        return df_categorical

    def enable_sparse_arrays(self, df: pd.DataFrame, sparsity_threshold: float = 0.95) -> pd.DataFrame:
        """启用稀疏数组优化

        对于稀疏度 > threshold 的列，转换为稀疏数组。
        稀疏数组只存储非零值，大幅节省内存。

        Args:
            df: 待优化的 DataFrame
            sparsity_threshold: 稀疏度阈值（默认 0.95，即 95% 为零）

        Returns:
            优化后的 DataFrame（新副本）
        """
        df_sparse = df.copy()

        for col in df_sparse.columns:
            col_data = df_sparse[col]

            if pd.api.types.is_numeric_dtype(col_data.dtype):
                sparsity = ((col_data == 0).sum() + col_data.isna().sum()) / len(col_data)

                if sparsity > sparsity_threshold:
                    df_sparse[col] = pd.arrays.SparseArray(col_data, fill_value=0)

        return df_sparse

    def benchmark_optimization(self, df: pd.DataFrame) -> dict[str, Any]:
        """优化效果基准测试

        执行完整的优化流程，并返回优化前后的内存对比。

        Args:
            df: 待优化的 DataFrame

        Returns:
            基准测试结果字典
        """
        original_memory = df.memory_usage(deep=True).sum() / (1024**2)
        start_time = time.time()

        # 执行优化流程
        optimized_df = self.optimize_dtypes(df)
        optimized_df = self.convert_to_categorical(optimized_df, threshold=0.5)
        optimized_df = self.enable_sparse_arrays(optimized_df, sparsity_threshold=0.95)

        optimization_time = time.time() - start_time
        optimized_memory = optimized_df.memory_usage(deep=True).sum() / (1024**2)

        return {
            "original_memory_mb": original_memory,
            "optimized_memory_mb": optimized_memory,
            "memory_reduction_pct": (original_memory - optimized_memory) / original_memory * 100,
            "optimization_time": optimization_time,
        }


def main() -> None:
    """演示内存优化器的使用"""
    print("=" * 70)
    print("示例 2: 内存优化器")
    print("=" * 70)

    # 创建测试数据集
    n_rows = 100_000
    test_data = {
        "small_int": np.random.randint(0, 100, n_rows),
        "medium_int": np.random.randint(0, 10_000, n_rows),
        "large_int": np.random.randint(0, 1_000_000, n_rows),
        "price": np.random.uniform(10.0, 1000.0, n_rows),
        "discount": np.random.uniform(0.0, 0.5, n_rows),
        "status": np.random.choice(["active", "inactive", "pending"], n_rows),
        "category": np.random.choice(["A", "B", "C", "D", "E"], n_rows),
        "user_id": [f"USER{i:06d}" for i in range(n_rows)],
        "rare_event": np.random.choice([0, 1], n_rows, p=[0.98, 0.02]),
    }
    df = pd.DataFrame(test_data)
    print(f"\n📊 数据集: {len(df):,} 行 × {len(df.columns)} 列")

    optimizer = MemoryOptimizer()

    # 内存分析报告
    print("\n" + "=" * 70)
    print("内存分析报告")
    print("=" * 70)
    analysis = optimizer.analyze_memory_usage(df)
    print(analysis.to_string(index=False))
    print(f"\n💾 总内存: {analysis['memory_mb'].sum():.2f} MB")
    print(f"💰 潜在节省: {analysis['potential_savings_mb'].sum():.2f} MB")

    # 优化基准测试
    print("\n" + "=" * 70)
    print("优化基准测试")
    print("=" * 70)
    results = optimizer.benchmark_optimization(df)
    print(f"📦 原始内存: {results['original_memory_mb']:.2f} MB")
    print(f"📦 优化后内存: {results['optimized_memory_mb']:.2f} MB")
    print(f"📉 内存减少: {results['memory_reduction_pct']:.1f}%")
    print(f"⏱️  优化耗时: {results['optimization_time']:.3f}s")

    # 分步演示
    print("\n" + "=" * 70)
    print("分步优化演示")
    print("=" * 70)
    original_memory = df.memory_usage(deep=True).sum() / (1024**2)
    print(f"\n原始内存: {original_memory:.2f} MB")

    df_step1 = optimizer.optimize_dtypes(df)
    memory_step1 = df_step1.memory_usage(deep=True).sum() / (1024**2)
    pct1 = (original_memory - memory_step1) / original_memory * 100
    print(f"优化数据类型后: {memory_step1:.2f} MB (-{pct1:.1f}%)")

    df_step2 = optimizer.convert_to_categorical(df_step1)
    memory_step2 = df_step2.memory_usage(deep=True).sum() / (1024**2)
    pct2 = (original_memory - memory_step2) / original_memory * 100
    print(f"转换 category 后: {memory_step2:.2f} MB (-{pct2:.1f}%)")

    df_step3 = optimizer.enable_sparse_arrays(df_step2)
    memory_step3 = df_step3.memory_usage(deep=True).sum() / (1024**2)
    pct3 = (original_memory - memory_step3) / original_memory * 100
    print(f"启用稀疏数组后: {memory_step3:.2f} MB (-{pct3:.1f}%)")

    print("\n" + "=" * 70)
    print("✅ 内存优化完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()
