"""练习 2: 向量化 vs 循环。

from __future__ import annotations

对比同样计算任务的向量化和 for 循环执行时间。
"""

import pandas as pd


# ========================================
# 📝 练习：对比向量化与循环的性能差异
#
# 🎯 目标：理解向量化操作的性能优势
#
# 📌 要求：
# 1. 实现使用循环的计算函数
# 2. 实现使用向量化的计算函数
# 3. 测量并对比执行时间
# 4. 计算性能提升比例
# 5. 处理不同规模的数据
#
# 💡 实现提示：
# - 循环版本使用 iterrows() 或 for 循环
# - 向量化版本使用 Pandas/NumPy 操作
# - 使用 time.perf_counter() 测量时间
# - 确保两种方法得到相同结果
#
# ✅ 验收标准：
# - 两种方法结果一致
# - 正确测量执行时间
# - 向量化方法显著更快
# - 输出清晰的性能对比
# ========================================


def calculate_with_loop(df: pd.DataFrame) -> pd.Series:
    """使用循环计算：(价格 * 数量) + 税费

    Args:
        df: 包含 price, quantity, tax 列的 DataFrame

    Returns:
        计算结果的 Series

    Examples:
        >>> df = pd.DataFrame({
        ...     'price': [10, 20, 30],
        ...     'quantity': [2, 3, 1],
        ...     'tax': [1, 2, 3]
        ... })
        >>> result = calculate_with_loop(df)
        >>> len(result) == len(df)
        True
    """
    # 👉 TODO: 实现循环计算
    # 1. 创建空列表存储结果
    # 2. 使用 iterrows() 遍历每一行
    # 3. 计算每行: (price * quantity) + tax
    # 4. 返回 pd.Series(results)
    #
    # 示例代码：
    # results = []
    # for idx, row in df.iterrows():
    #     total = (row['price'] * row['quantity']) + row['tax']
    #     results.append(total)
    # return pd.Series(results, index=df.index)
    raise NotImplementedError


def calculate_with_vectorization(df: pd.DataFrame) -> pd.Series:
    """使用向量化计算：(价格 * 数量) + 税费

    Args:
        df: 包含 price, quantity, tax 列的 DataFrame

    Returns:
        计算结果的 Series

    Examples:
        >>> df = pd.DataFrame({
        ...     'price': [10, 20, 30],
        ...     'quantity': [2, 3, 1],
        ...     'tax': [1, 2, 3]
        ... })
        >>> result = calculate_with_vectorization(df)
        >>> len(result) == len(df)
        True
    """
    # 👉 TODO: 实现向量化计算
    # 直接对列进行操作：
    # return (df['price'] * df['quantity']) + df['tax']
    raise NotImplementedError


def benchmark_performance(size: int = 10000) -> dict[str, float]:
    """性能基准测试

    Args:
        size: 数据规模

    Returns:
        包含执行时间和加速比的字典

    Examples:
        >>> result = benchmark_performance(size=100)
        >>> 'loop_time' in result
        True
        >>> 'vectorized_time' in result
        True
        >>> result['speedup'] > 1
        True
    """
    # 👉 TODO: 实现性能测试
    # 1. 生成测试数据
    # 2. 测量循环方法的执行时间
    # 3. 测量向量化方法的执行时间
    # 4. 计算加速比
    # 5. 返回结果字典
    #
    # 示例代码：
    # # 生成测试数据
    # df = pd.DataFrame({
    #     'price': np.random.rand(size) * 100,
    #     'quantity': np.random.randint(1, 10, size),
    #     'tax': np.random.rand(size) * 10
    # })
    #
    # # 测量循环时间
    # start = time.perf_counter()
    # result_loop = calculate_with_loop(df)
    # loop_time = time.perf_counter() - start
    #
    # # 测量向量化时间
    # start = time.perf_counter()
    # result_vec = calculate_with_vectorization(df)
    # vec_time = time.perf_counter() - start
    #
    # # 验证结果一致
    # assert np.allclose(result_loop, result_vec), "Results don't match!"
    #
    # return {
    #     'loop_time': loop_time,
    #     'vectorized_time': vec_time,
    #     'speedup': loop_time / vec_time
    # }
    raise NotImplementedError


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 向量化 vs 循环性能对比")
    print("=" * 60)

    print("\n💡 完成上述函数后，取消下面的注释测试：")
    print()

    # # 小规模测试（验证正确性）
    # print("✅ 验证正确性（小数据集）:")
    # test_df = pd.DataFrame({
    #     'price': [10.0, 20.0, 30.0],
    #     'quantity': [2, 3, 1],
    #     'tax': [1.0, 2.0, 3.0]
    # })
    #
    # result_loop = calculate_with_loop(test_df)
    # result_vec = calculate_with_vectorization(test_df)
    #
    # print(f"  循环结果: {result_loop.tolist()}")
    # print(f"  向量化结果: {result_vec.tolist()}")
    # print(f"  结果一致: {np.allclose(result_loop, result_vec)}")
    #
    # # 性能对比测试
    # print("\n📊 性能对比（不同规模）:")
    # sizes = [1000, 10000, 100000]
    #
    # for size in sizes:
    #     print(f"\n数据规模: {size:,} 行")
    #     result = benchmark_performance(size)
    #     print(f"  循环时间: {result['loop_time']:.4f} 秒")
    #     print(f"  向量化时间: {result['vectorized_time']:.4f} 秒")
    #     print(f"  🚀 加速比: {result['speedup']:.1f}x")

    print("\n" + "=" * 60)
    print("📚 关键要点:")
    print("   - 向量化操作通常快 10-100 倍")
    print("   - 避免在 Pandas 中使用循环")
    print("   - 数据规模越大，优势越明显")
    print("=" * 60)
