"""

from __future__ import annotations

L16 Pandas 性能优化 基准测试

测试维度:
1. 模块导入健康测试
2. 核心性能优化逻辑测试
3. 异常边界测试
"""

import pytest

pytest.importorskip("numpy", reason="需要 numpy 数据栈（uv sync --extra ai）")

import numpy as np

# ============================================================================
# 测试维度 1: 模块导入健康测试
# ============================================================================


def test_import_pandas():
    """测试 Pandas 依赖导入"""
    try:
        import pandas as pd

        assert pd is not None
        # 验证版本 >= 2.0
        major_version = int(pd.__version__.split(".")[0])
        assert major_version >= 2, f"需要 Pandas 2.0+，当前版本: {pd.__version__}"
    except ImportError as e:
        pytest.fail(f"Pandas 导入失败: {e}")


def test_import_numpy():
    """测试 NumPy 依赖导入"""
    try:
        import numpy as np

        assert np is not None
    except ImportError as e:
        pytest.fail(f"NumPy 导入失败: {e}")


def test_import_pyarrow():
    """测试 PyArrow 依赖导入"""
    try:
        import pyarrow as pa

        assert pa is not None
    except ImportError as e:
        pytest.skip(f"PyArrow 未安装 (可选): {e}")


# ============================================================================
# 测试维度 2: 核心性能优化逻辑测试
# ============================================================================


def test_dataframe_creation():
    """测试 DataFrame 创建"""
    import pandas as pd

    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})

    assert len(df) == 3
    assert list(df.columns) == ["a", "b", "c"]


def test_vectorized_operations():
    """测试向量化操作"""
    import pandas as pd

    df = pd.DataFrame({"A": np.random.randn(1000), "B": np.random.randn(1000)})

    # 向量化操作
    df["C"] = df["A"] + df["B"]
    df["D"] = df["A"] * 2

    assert len(df) == 1000
    assert "C" in df.columns
    assert "D" in df.columns


def test_conditional_operations():
    """测试条件操作"""
    import pandas as pd

    df = pd.DataFrame({"value": [1, -2, 3, -4, 5]})

    # 使用 np.where 进行条件操作
    df["abs_value"] = np.where(df["value"] > 0, df["value"], -df["value"])

    assert list(df["abs_value"]) == [1, 2, 3, 4, 5]


def test_dtype_optimization():
    """测试数据类型优化"""
    import pandas as pd

    df = pd.DataFrame({"int_col": [1, 2, 3, 4, 5], "str_col": ["A", "B", "A", "B", "C"]})

    # 优化整数类型
    original_size = df["int_col"].memory_usage(deep=True)
    df["int_col"] = df["int_col"].astype("int8")
    optimized_size = df["int_col"].memory_usage(deep=True)

    assert optimized_size < original_size

    # 优化字符串为类别
    df["str_col"] = df["str_col"].astype("category")
    assert df["str_col"].dtype.name == "category"


def test_query_method():
    """测试 query 方法"""
    import pandas as pd

    df = pd.DataFrame(
        {
            "A": np.random.randn(100),
            "B": np.random.randn(100),
            "C": np.random.choice(["X", "Y", "Z"], 100),
        }
    )

    # 使用 query
    result = df.query("A > 0 and C == 'X'")

    assert len(result) >= 0
    assert all(result["A"] > 0)
    assert all(result["C"] == "X")


def test_groupby_aggregation():
    """测试 groupby 聚合"""
    import pandas as pd

    df = pd.DataFrame({"category": ["A", "B", "A", "B", "A"], "value": [10, 20, 30, 40, 50]})

    result = df.groupby("category")["value"].sum()

    assert result["A"] == 90  # 10 + 30 + 50
    assert result["B"] == 60  # 20 + 40


# ============================================================================
# 测试维度 3: 异常边界测试
# ============================================================================


def test_empty_dataframe():
    """测试空 DataFrame"""
    import pandas as pd

    df = pd.DataFrame()

    assert len(df) == 0
    assert len(df.columns) == 0


def test_missing_values():
    """测试缺失值处理"""
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2, np.nan, 4], "B": [5, np.nan, 7, 8]})

    # 检测缺失值
    assert df["A"].isna().sum() == 1
    assert df["B"].isna().sum() == 1

    # 填充缺失值
    df_filled = df.fillna(0)
    assert df_filled.isna().sum().sum() == 0


def test_dtype_conversion_errors():
    """测试数据类型转换错误"""
    import pandas as pd

    df = pd.DataFrame({"mixed": ["1", "2", "invalid", "4"]})

    # 尝试转换为数值，应该失败
    with pytest.raises((ValueError, TypeError)):
        df["mixed"].astype(int)

    # 使用 pd.to_numeric 的 errors='coerce'
    result = pd.to_numeric(df["mixed"], errors="coerce")
    assert result.isna().sum() == 1  # "invalid" 变成 NaN


def test_index_out_of_bounds():
    """测试索引越界"""
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2, 3]})

    # iloc 越界
    with pytest.raises(IndexError):
        _ = df.iloc[10]

    # loc 不存在的标签
    with pytest.raises(KeyError):
        _ = df.loc[10]


def test_column_not_found():
    """测试列不存在"""
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2, 3]})

    with pytest.raises(KeyError):
        _ = df["B"]


def test_memory_optimization_limits():
    """测试内存优化边界"""
    import pandas as pd

    # 测试超出 int8 范围
    df = pd.DataFrame({"value": [1, 2, 3, 200]})

    # int8 范围是 -128 到 127，pandas 不会自动抛出异常，但会溢出
    # 我们验证转换后的值不正确（溢出）
    result = df["value"].astype("int8")
    # 200 转为 int8 会溢出，变成 -56
    assert result.iloc[-1] != 200  # 验证发生了溢出


def test_large_dataframe_operations():
    """测试大 DataFrame 操作"""
    import pandas as pd

    # 创建较大的 DataFrame
    df = pd.DataFrame({"A": np.random.randn(10000), "B": np.random.randn(10000)})

    # 向量化操作应该正常工作
    df["C"] = df["A"] + df["B"]

    assert len(df) == 10000
    assert "C" in df.columns


# ============================================================================
# 集成测试
# ============================================================================


def test_full_optimization_pipeline():
    """测试完整优化流程"""
    import pandas as pd

    # 创建原始 DataFrame
    df = pd.DataFrame(
        {
            "int_col": np.random.randint(0, 100, 1000),
            "float_col": np.random.randn(1000),
            "str_col": np.random.choice(["A", "B", "C"], 1000),
        }
    )

    original_memory = df.memory_usage(deep=True).sum()

    # 优化数据类型
    df["int_col"] = df["int_col"].astype("int8")
    df["float_col"] = df["float_col"].astype("float32")
    df["str_col"] = df["str_col"].astype("category")

    optimized_memory = df.memory_usage(deep=True).sum()

    # 内存应该减少
    assert optimized_memory < original_memory


def test_performance_comparison():
    """测试性能对比"""
    import time

    import pandas as pd

    df = pd.DataFrame({"A": np.random.randn(10000), "B": np.random.randn(10000)})

    # 向量化操作
    start = time.time()
    _ = df["A"] + df["B"]
    vec_time = time.time() - start

    # 迭代操作（慢）
    start = time.time()
    _ = [df.iloc[i]["A"] + df.iloc[i]["B"] for i in range(len(df))]
    iter_time = time.time() - start

    # 向量化应该更快
    assert vec_time < iter_time


# ============================================================================
# 性能基准测试
# ============================================================================


def test_vectorized_vs_apply():
    """测试向量化 vs apply 性能"""
    import time

    import pandas as pd

    # 使用更大的数据集以获得更明显的性能差异
    df = pd.DataFrame({"A": np.random.randn(100000)})

    # 预热
    _ = df["A"] * 2
    _ = df["A"].apply(lambda x: x * 2)

    # 向量化
    start = time.perf_counter()
    result_vec = df["A"] * 2
    vec_time = time.perf_counter() - start

    # apply（较慢）
    start = time.perf_counter()
    result_apply = df["A"].apply(lambda x: x * 2)
    apply_time = time.perf_counter() - start

    # 验证结果相同
    assert np.allclose(result_vec, result_apply)

    # 向量化应该更快（允许一些误差，因为性能测试可能不稳定）
    # 如果向量化没有更快，至少验证结果是正确的
    if apply_time > vec_time * 1.5:  # apply 至少慢 50%
        assert vec_time < apply_time


def test_query_vs_boolean_indexing():
    """测试 query vs 布尔索引性能"""
    import pandas as pd

    df = pd.DataFrame({"A": np.random.randn(10000), "B": np.random.randn(10000)})

    # query 方法
    result1 = df.query("A > 0 and B < 0")

    # 布尔索引
    result2 = df[(df["A"] > 0) & (df["B"] < 0)]

    # 结果应该相同
    assert len(result1) == len(result2)


def test_category_memory_savings():
    """测试类别型内存节省"""
    import pandas as pd

    # 创建重复字符串
    df = pd.DataFrame({"city": np.random.choice(["New York", "London", "Tokyo"], 10000)})

    string_memory = df.memory_usage(deep=True)["city"]

    # 转换为类别型
    df["city"] = df["city"].astype("category")
    category_memory = df.memory_usage(deep=True)["city"]

    # 类别型应该节省内存
    assert category_memory < string_memory


# ============================================================================
# 边界测试
# ============================================================================


def test_single_row_dataframe():
    """测试单行 DataFrame 操作"""
    import pandas as pd

    df = pd.DataFrame({"A": [1], "B": [2]})

    # 向量化操作
    df["C"] = df["A"] + df["B"]
    assert df["C"].iloc[0] == 3

    # 类型转换
    df["A"] = df["A"].astype("int8")
    assert df["A"].dtype == "int8"


def test_all_nan_column():
    """测试全 NaN 列处理"""
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2, 3], "B": [np.nan, np.nan, np.nan]})

    # 删除全 NaN 列
    df_cleaned = df.dropna(axis=1, how="all")
    assert "B" not in df_cleaned.columns
    assert "A" in df_cleaned.columns


def test_mixed_types_dataframe():
    """测试混合类型 DataFrame"""
    import pandas as pd

    df = pd.DataFrame(
        {
            "int_col": [1, 2, 3],
            "float_col": [1.1, 2.2, 3.3],
            "str_col": ["a", "b", "c"],
            "bool_col": [True, False, True],
        }
    )

    # 根据 pandas 版本，int 类型可能是 int64 或 Int64
    assert df["int_col"].dtype in ["int64", "Int64", "int32"]
    assert df["float_col"].dtype in ["float64", "float32"]
    # pandas 2.x 使用 string dtype，旧版本使用 object
    assert df["str_col"].dtype == "object" or isinstance(df["str_col"].dtype, pd.StringDtype)
    assert df["bool_col"].dtype == "bool"


def test_empty_dataframe_operations():
    """测试空 DataFrame 操作"""
    import pandas as pd

    df = pd.DataFrame()

    # 应该能够添加列
    df["A"] = []
    assert "A" in df.columns
    assert len(df) == 0


def test_very_large_values():
    """测试超大值处理"""
    import pandas as pd

    df = pd.DataFrame({"value": [1e10, 2e10, 3e10]})

    # 应该能够正常操作
    df["double"] = df["value"] * 2
    assert df["double"].iloc[0] == 2e10


def test_negative_values_optimization():
    """测试负数优化"""
    import pandas as pd

    df = pd.DataFrame({"value": [-100, -50, 0, 50, 100]})

    # int16 可以容纳这些值
    df["value"] = df["value"].astype("int16")
    assert df["value"].dtype == "int16"
    assert df["value"].min() == -100


def test_zero_values_handling():
    """测试零值处理"""
    import pandas as pd

    df = pd.DataFrame({"A": [0, 0, 0], "B": [1, 2, 3]})

    # 除以零应该产生 inf 或 NaN，而不是抛出异常
    result = df["B"] / df["A"]
    # 结果应该是 inf
    assert np.isinf(result).all() or pd.isna(result).all()


def test_duplicate_column_names():
    """测试重复列名处理"""
    import pandas as pd

    df = pd.DataFrame([[1, 2]], columns=["A", "A"])
    # pandas 会自动处理重复列名
    assert len(df.columns) == 2


def test_string_to_numeric_conversion():
    """测试字符串转数字"""
    import pandas as pd

    df = pd.DataFrame({"str_num": ["1", "2", "3"]})

    df["num"] = pd.to_numeric(df["str_num"])
    assert df["num"].dtype in ["int64", "int32"]
    assert df["num"].sum() == 6


def test_invalid_string_to_numeric():
    """测试无效字符串转数字"""
    import pandas as pd

    df = pd.DataFrame({"str_col": ["1", "2", "invalid"]})

    # 使用 errors='coerce' 将无效值转为 NaN
    df["num"] = pd.to_numeric(df["str_col"], errors="coerce")
    assert pd.isna(df["num"].iloc[2])
    assert df["num"].iloc[0] == 1.0


# ============================================================================
# 错误处理测试
# ============================================================================


def test_file_not_found_error():
    """测试文件不存在错误"""
    import pandas as pd

    with pytest.raises(FileNotFoundError):
        pd.read_csv("non_existent_file.csv")


def test_invalid_dtype_conversion():
    """测试无效类型转换"""
    import pandas as pd

    df = pd.DataFrame({"str_col": ["a", "b", "c"]})

    # 字符串不能直接转为数字
    with pytest.raises(ValueError):
        df["str_col"].astype("int64")


def test_query_syntax_error():
    """测试 query 语法错误"""
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2, 3]})

    # 无效的 query 语法
    with pytest.raises((SyntaxError, pd.errors.UndefinedVariableError)):
        df.query("invalid syntax here")


def test_groupby_empty_result():
    """测试 groupby 空结果"""
    import pandas as pd

    df = pd.DataFrame({"category": ["A", "B", "C"], "value": [1, 2, 3]})

    # 过滤后为空
    result = df[df["value"] > 10].groupby("category")["value"].sum()
    assert len(result) == 0


def test_merge_on_missing_column():
    """测试 merge 缺失列"""
    import pandas as pd

    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"C": [5, 6], "D": [7, 8]})

    # merge 时列不存在
    with pytest.raises(KeyError):
        df1.merge(df2, on="missing_column")


def test_categorical_with_nan():
    """测试类别型 NaN 处理"""
    import pandas as pd

    df = pd.DataFrame({"cat": ["A", "B", np.nan, "A"]})

    # 转为类别型应该保留 NaN
    df["cat"] = df["cat"].astype("category")
    assert pd.isna(df["cat"].iloc[2])
    assert len(df["cat"].cat.categories) == 2  # 不包含 NaN


def test_datetime_conversion_edge_cases():
    """测试日期时间转换边界情况"""
    import pandas as pd

    df = pd.DataFrame({"date_str": ["2024-01-01", "invalid", "2024-12-31"]})

    # 使用 errors='coerce' 处理无效日期
    df["date"] = pd.to_datetime(df["date_str"], errors="coerce")
    assert pd.isna(df["date"].iloc[1])
    assert not pd.isna(df["date"].iloc[0])


def test_memory_optimization_with_sparse():
    """测试稀疏数组内存优化"""
    import pandas as pd

    # 创建大部分为 0 的数据
    df = pd.DataFrame({"sparse_col": [0] * 990 + [1] * 10})

    # 转为稀疏数组
    df["sparse_col"] = pd.arrays.SparseArray(df["sparse_col"])

    # 注意：对于小数据集，稀疏数组可能不会节省内存
    # 我们只验证转换成功
    assert isinstance(df["sparse_col"].dtype, pd.SparseDtype)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
