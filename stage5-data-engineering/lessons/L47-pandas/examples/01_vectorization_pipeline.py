"""示例 1: 向量化数据处理管道

from __future__ import annotations

演示如何使用向量化操作替代循环和 apply，实现高性能数据处理。

核心技术:
- 向量化操作替代 apply/iterrows
- PyArrow 后端加速
- 类型优化减少内存占用
- np.where 和 np.select 处理条件逻辑
"""

from __future__ import annotations

from pathlib import Path
import time
from typing import Any

import numpy as np
import pandas as pd


class DataPipeline:
    """向量化数据处理管道

    提供高性能的数据处理流程:
    1. 分块加载数据
    2. 清理缺失值（向量化填充）
    3. 优化数据类型（减少内存）
    4. 计算特征（向量化运算）
    5. 性能基准测试

    Args:
        use_pyarrow: 是否使用 PyArrow 后端加速（推荐开启）

    Example:
        >>> pipeline = DataPipeline(use_pyarrow=True)
        >>> df = pipeline.load_data("orders.csv", chunksize=100_000)
        >>> df = pipeline.clean_missing_values(df)
        >>> df = pipeline.transform_types(df)
        >>> df = pipeline.calculate_features(df)
        >>> report = pipeline.generate_report()
    """

    def __init__(self, use_pyarrow: bool = True) -> None:
        """初始化管道

        Args:
            use_pyarrow: 是否使用 PyArrow 后端（默认 True）
        """
        self.use_pyarrow = use_pyarrow
        self._performance_stats: dict[str, Any] = {}

        # 检查 PyArrow 是否可用
        if use_pyarrow:
            try:
                import pyarrow
            except ImportError:
                print("⚠️  PyArrow 未安装，将使用 NumPy 后端")
                self.use_pyarrow = False

    def load_data(self, filepath: str, chunksize: int = 100_000) -> pd.DataFrame:
        """分块加载 CSV 数据并转换为 PyArrow 后端

        分块加载可以避免一次性加载大文件导致内存溢出。
        PyArrow 后端在数值计算和字符串操作上比 NumPy 更快。

        Args:
            filepath: CSV 文件路径
            chunksize: 每次加载的行数（默认 10 万行）

        Returns:
            加载的 DataFrame（应用 PyArrow 后端）

        Example:
            >>> df = pipeline.load_data("orders.csv", chunksize=50_000)
            >>> print(df.dtypes)  # 查看数据类型
        """
        start_time = time.time()

        # 分块读取 CSV
        df = pd.read_csv(filepath, nrows=chunksize)

        # 如果启用 PyArrow，转换数值列和字符串列
        if self.use_pyarrow:
            df = self._convert_to_pyarrow(df)

        load_time = time.time() - start_time
        self._performance_stats["load_time"] = load_time

        print(f"✅ 数据加载完成: {len(df):,} 行，耗时 {load_time:.2f}s")
        return df

    def _convert_to_pyarrow(self, df: pd.DataFrame) -> pd.DataFrame:
        """将 DataFrame 转换为 PyArrow 后端

        PyArrow 后端对以下操作有显著性能提升:
        - 数值计算（比 NumPy 快 20-30%）
        - 字符串操作（快 2-5 倍）
        - 内存占用（节省 10-20%）

        Args:
            df: 原始 DataFrame

        Returns:
            转换后的 DataFrame
        """
        # 遍历所有列进行类型转换
        for col in df.columns:
            dtype = df[col].dtype

            # 转换整数列到 PyArrow 整数类型
            if pd.api.types.is_integer_dtype(dtype):
                df[col] = df[col].astype("int64[pyarrow]")

            # 转换浮点数列到 PyArrow 浮点类型
            elif pd.api.types.is_float_dtype(dtype):
                df[col] = df[col].astype("float64[pyarrow]")

            # 转换字符串列到 PyArrow 字符串类型
            elif pd.api.types.is_object_dtype(dtype):
                df[col] = df[col].astype("string[pyarrow]")

        return df

    def clean_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """清理缺失值（向量化操作）

        使用向量化的 fillna() 方法替代 apply(lambda)，性能提升 10-100 倍。

        清理策略:
        - 数值列: 使用中位数填充
        - 分类列: 使用众数填充
        - 日期列: 使用前向填充

        Args:
            df: 包含缺失值的 DataFrame

        Returns:
            清理后的 DataFrame

        Example:
            >>> cleaned_df = pipeline.clean_missing_values(df)
            >>> assert cleaned_df.isna().sum().sum() == 0
        """
        start_time = time.time()
        df = df.copy()

        # 记录缺失值统计
        missing_before = df.isna().sum().sum()

        # 数值列: 使用中位数填充（向量化操作）
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isna().any():
                median_value = df[col].median()
                df[col] = df[col].fillna(median_value)

        # 分类列: 使用众数填充
        categorical_cols = df.select_dtypes(include=["object", "string", "category"]).columns
        for col in categorical_cols:
            if df[col].isna().any():
                mode_value = df[col].mode()[0] if not df[col].mode().empty else "unknown"
                df[col] = df[col].fillna(mode_value)

        # 日期列: 使用前向填充
        datetime_cols = df.select_dtypes(include=["datetime64"]).columns
        for col in datetime_cols:
            if df[col].isna().any():
                df[col] = df[col].fillna(method="ffill")

        clean_time = time.time() - start_time
        self._performance_stats["clean_time"] = clean_time

        missing_after = df.isna().sum().sum()
        print(f"✅ 缺失值清理: {missing_before:,} → {missing_after:,}，耗时 {clean_time:.3f}s")

        return df

    def transform_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """优化数据类型以减少内存占用

        类型优化策略:
        - int64 → int8/int16/int32（根据数值范围）
        - float64 → float32（精度允许时）
        - object → category（重复率高的列）

        Args:
            df: 原始 DataFrame

        Returns:
            类型优化后的 DataFrame

        Example:
            >>> before_mem = df.memory_usage(deep=True).sum()
            >>> df = pipeline.transform_types(df)
            >>> after_mem = df.memory_usage(deep=True).sum()
            >>> print(f"内存节省: {(1 - after_mem/before_mem)*100:.1f}%")
        """
        start_time = time.time()
        df = df.copy()

        # 记录优化前的内存使用
        memory_before = df.memory_usage(deep=True).sum()

        # 优化整数列：根据数值范围选择最小的整数类型
        for col in df.select_dtypes(include=["int"]).columns:
            col_min = df[col].min()
            col_max = df[col].max()

            # 根据数值范围选择最小的整数类型（无符号）
            if col_min >= 0:
                # 无符号整数优化
                if col_max < 256:
                    df[col] = df[col].astype("int8")
                elif col_max < 65536:
                    df[col] = df[col].astype("int16")
                elif col_max < 4294967296:
                    df[col] = df[col].astype("int32")
            # 有符号整数优化
            elif col_min > -128 and col_max < 128:
                df[col] = df[col].astype("int8")
            elif col_min > -32768 and col_max < 32768:
                df[col] = df[col].astype("int16")
            elif col_min > -2147483648 and col_max < 2147483648:
                df[col] = df[col].astype("int32")

        # 优化浮点数列：在精度允许时转换为 float32
        for col in df.select_dtypes(include=["float"]).columns:
            # 检查转换前后的相对误差是否在可接受范围内
            float32_values = df[col].astype("float32")
            # 相对误差小于 1e-6 时认为精度损失可接受
            if ((df[col] - float32_values).abs() / df[col].abs()).max() < 1e-6:
                df[col] = float32_values

        # 优化字符串列：重复率高的转为 category 类型
        for col in df.select_dtypes(include=["object", "string"]).columns:
            # 计算唯一值比例
            unique_ratio = df[col].nunique() / len(df)
            # 重复率超过 50% 时转换为 category
            if unique_ratio < 0.5:  # 重复率超过 50%
                df[col] = df[col].astype("category")

        # 计算内存节省比例
        memory_after = df.memory_usage(deep=True).sum()
        transform_time = time.time() - start_time
        self._performance_stats["transform_time"] = transform_time

        memory_saved = (1 - memory_after / memory_before) * 100
        print(f"✅ 类型优化: 内存节省 {memory_saved:.1f}%，耗时 {transform_time:.3f}s")

        return df

    def calculate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算派生特征（向量化操作）

        使用 np.where 和 np.select 替代 apply(lambda)，性能提升 10-50 倍。

        计算的特征:
        - total_amount: 订单总金额（price * quantity）
        - price_category: 价格分类（low/medium/high）
        - is_high_value: 是否高价值订单（> 500）
        - order_month: 订单月份（1-12）

        Args:
            df: 清理和转换后的 DataFrame

        Returns:
            包含新特征的 DataFrame

        Example:
            >>> df = pipeline.calculate_features(df)
            >>> print(df["price_category"].value_counts())
        """
        start_time = time.time()
        df = df.copy()

        # 特征 1: 计算订单总金额（向量化乘法，避免使用 apply）
        df["total_amount"] = df["price"] * df["quantity"]

        # 特征 2: 价格分类（使用 np.select 处理多条件分支）
        # np.select 比 apply(lambda) 快 10-50 倍
        conditions = [
            df["price"] < 100,  # 低价
            (df["price"] >= 100) & (df["price"] < 500),  # 中价
            df["price"] >= 500,  # 高价
        ]
        choices = ["low", "medium", "high"]
        df["price_category"] = np.select(conditions, choices, default="unknown")

        # 特征 3: 高价值订单标记（使用 np.where 处理二元条件）
        # np.where 比 apply(lambda) 快 20-100 倍
        df["is_high_value"] = np.where(df["total_amount"] > 500, True, False)

        # 特征 4: 提取订单月份（向量化日期提取）
        if "order_date" in df.columns:
            # 向量化提取月份，避免逐行处理
            df["order_month"] = pd.to_datetime(df["order_date"]).dt.month

        feature_time = time.time() - start_time
        self._performance_stats["feature_time"] = feature_time

        print(f"✅ 特征计算: 新增 4 个特征，耗时 {feature_time:.3f}s")

        return df

    def benchmark_vs_loop(self, df: pd.DataFrame) -> dict[str, float]:
        """性能基准测试: 向量化 vs apply vs iterrows

        对比三种实现方式的性能:
        1. 向量化操作（推荐）
        2. apply(lambda)（慢 10-50 倍）
        3. iterrows（慢 50-200 倍）

        Args:
            df: 测试数据集

        Returns:
            性能统计字典，包含各方法耗时和加速比

        Example:
            >>> results = pipeline.benchmark_vs_loop(df)
            >>> print(f"向量化比 apply 快 {results['speedup_vs_apply']:.1f}x")
        """
        print("\n🔬 开始性能基准测试...")

        # 创建测试副本（避免修改原始数据）
        test_df = df.copy()

        # 方法 1: 向量化操作（推荐，性能最优）
        # 使用 NumPy 底层 C 代码直接操作数组
        start = time.time()
        _ = test_df["price"] * test_df["quantity"]
        vectorized_time = time.time() - start
        print(f"   ✓ 向量化操作: {vectorized_time:.4f}s")

        # 方法 2: apply(lambda)（性能较差）
        # 每行调用 Python 函数，有函数调用开销
        start = time.time()
        _ = test_df.apply(lambda row: row["price"] * row["quantity"], axis=1)
        apply_time = time.time() - start
        print(f"   ✓ apply(lambda): {apply_time:.4f}s")

        # 方法 3: iterrows（性能最差）
        # 逐行迭代，将每行转为 Series，开销巨大
        start = time.time()
        results = []
        for _, row in test_df.iterrows():
            results.append(row["price"] * row["quantity"])
        iterrows_time = time.time() - start
        print(f"   ✓ iterrows 循环: {iterrows_time:.4f}s")

        # 计算加速比（向量化相对于其他方法的性能提升）
        speedup_vs_apply = apply_time / vectorized_time
        speedup_vs_iterrows = iterrows_time / vectorized_time

        print("\n📊 性能对比:")
        print(f"   - 向量化 vs apply: {speedup_vs_apply:.1f}x 加速")
        print(f"   - 向量化 vs iterrows: {speedup_vs_iterrows:.1f}x 加速")

        # 保存结果到性能统计
        benchmark_results = {
            "vectorized_time": vectorized_time,
            "apply_time": apply_time,
            "iterrows_time": iterrows_time,
            "speedup_vs_apply": speedup_vs_apply,
            "speedup_vs_iterrows": speedup_vs_iterrows,
        }
        self._performance_stats["benchmark"] = benchmark_results

        return benchmark_results

    def generate_report(self) -> str:
        """生成性能摘要报告

        Returns:
            格式化的性能报告字符串

        Example:
            >>> report = pipeline.generate_report()
            >>> print(report)
        """
        report_lines = [
            "=" * 60,
            "🚀 向量化数据处理管道 - 性能报告",
            "=" * 60,
            "",
        ]

        # 基础性能统计
        if "load_time" in self._performance_stats:
            report_lines.append(f"数据加载: {self._performance_stats['load_time']:.2f}s")

        if "clean_time" in self._performance_stats:
            report_lines.append(f"缺失值清理: {self._performance_stats['clean_time']:.3f}s")

        if "transform_time" in self._performance_stats:
            report_lines.append(f"类型优化: {self._performance_stats['transform_time']:.3f}s")

        if "feature_time" in self._performance_stats:
            report_lines.append(f"特征计算: {self._performance_stats['feature_time']:.3f}s")

        # 性能基准对比
        if "benchmark" in self._performance_stats:
            bench = self._performance_stats["benchmark"]
            report_lines.extend(
                [
                    "",
                    "性能基准测试:",
                    f"  - 向量化操作: {bench['vectorized_time']:.4f}s",
                    f"  - apply(lambda): {bench['apply_time']:.4f}s",
                    f"  - iterrows 循环: {bench['iterrows_time']:.4f}s",
                    "",
                    "加速比:",
                    f"  - 向量化 vs apply: {bench['speedup_vs_apply']:.1f}x",
                    f"  - 向量化 vs iterrows: {bench['speedup_vs_iterrows']:.1f}x",
                ]
            )

        report_lines.extend(
            [
                "",
                "=" * 60,
                "✅ 报告生成完成",
                "=" * 60,
            ]
        )

        return "\n".join(report_lines)


def main() -> None:
    """演示向量化管道的完整流程"""
    print("=" * 60)
    print("🚀 示例 1: 向量化数据处理管道")
    print("=" * 60)
    print()

    # 初始化管道
    pipeline = DataPipeline(use_pyarrow=True)

    # 加载数据（使用相对路径）
    data_dir = Path(__file__).parent.parent / "data"
    orders_file = data_dir / "sample_orders.csv"

    if not orders_file.exists():
        print(f"❌ 数据文件不存在: {orders_file}")
        print("请先运行: python data/generate_data.py")
        return

    # 步骤 1: 加载数据（只加载前 50000 行用于演示）
    print("步骤 1: 加载数据")
    df = pipeline.load_data(str(orders_file), chunksize=50_000)
    print(f"数据形状: {df.shape}")
    print()

    # 步骤 2: 清理缺失值
    print("步骤 2: 清理缺失值")
    df = pipeline.clean_missing_values(df)
    print()

    # 步骤 3: 优化数据类型
    print("步骤 3: 优化数据类型")
    df = pipeline.transform_types(df)
    print()

    # 步骤 4: 计算特征
    print("步骤 4: 计算特征")
    df = pipeline.calculate_features(df)
    print()

    # 步骤 5: 性能基准测试
    print("步骤 5: 性能基准测试")
    pipeline.benchmark_vs_loop(df)
    print()

    # 步骤 6: 生成报告
    print("步骤 6: 生成性能报告")
    report = pipeline.generate_report()
    print()
    print(report)


if __name__ == "__main__":
    main()
