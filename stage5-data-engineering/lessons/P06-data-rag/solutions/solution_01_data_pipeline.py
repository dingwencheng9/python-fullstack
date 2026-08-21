"""P06 练习 1: 数据管道与 ETL"""

from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Optional

# ============ 数据加载 ============

def load_csv(file_path: str) -> pd.DataFrame:
    """加载 CSV 文件"""
    # TODO: 使用 Pandas 加载 CSV
    # 提示: pd.read_csv()
    pass

def load_parquet(file_path: str) -> pd.DataFrame:
    """加载 Parquet 文件（使用 PyArrow 后端）"""
    # TODO: 使用 PyArrow 后端加速加载
    # 提示: pd.read_parquet(..., dtype_backend="pyarrow")
    pass

# ============ 数据清洗 ============

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """清洗销售数据"""
    # TODO: 实现以下清洗步骤
    # 1. 类型优化：金额转为 float32
    # 2. 缺失值填充：数值用中位数，类别用众数
    # 3. 删除重复行
    # 4. 异常值处理：金额超出 3 倍标准差的数据

    df = df.copy()

    # 你的代码:
    # 1. 类型优化
    # if 'amount' in df.columns:
    #     df['amount'] = df['amount'].astype('float32')

    # 2. 缺失值填充
    # ...

    # 3. 删除重复
    # ...

    # 4. 异常值
    # ...

    return df

def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """按类别聚合统计"""
    # TODO: 按 category 分组，计算：
    # - count: 数量
    # - total: 总金额
    # - avg: 平均金额
    # - max: 最大金额

    # 你的代码:
    # result = df.groupby('category').agg({
    #     'amount': ['count', 'sum', 'mean', 'max']
    # })

    return pd.DataFrame()

# ============ 运行测试 ============

if __name__ == "__main__":
    # 创建示例数据
    df = pd.DataFrame({
        'category': ['A', 'B', 'A', 'B', 'C', 'A'],
        'amount': [100.0, 200.0, 150.0, 300.0, np.nan, 120.0],
        'quantity': [1, 2, 1, 3, 2, 1]
    })

    print("原始数据:")
    print(df)
    print()

    print("清洗后:")
    cleaned = clean_sales_data(df)
    print(cleaned)
    print()

    print("按类别聚合:")
    agg = aggregate_by_category(cleaned)
    print(agg)
