"""示例 1: 高级分组聚合

展示 GroupBy 的高级用法：
- 多函数聚合
- transform 方法
- 过滤分组
"""

from __future__ import annotations

import pandas as pd
import numpy as np


def create_sample_data() -> pd.DataFrame:
    """创建示例销售数据"""
    np.random.seed(42)
    n = 1000

    categories = ["电子产品", "服装", "食品", "家居"]
    regions = ["华北", "华东", "华南", "西南"]

    return pd.DataFrame(
        {
            "order_id": range(1, n + 1),
            "category": np.random.choice(categories, n),
            "region": np.random.choice(regions, n),
            "sales": np.random.uniform(10, 1000, n).round(2),
            "quantity": np.random.randint(1, 10, n),
            "cost": np.random.uniform(5, 500, n).round(2),
            "date": pd.date_range("2024-01-01", periods=n, freq="h"),
        }
    )


def basic_groupby(df: pd.DataFrame) -> pd.DataFrame:
    """基础分组聚合"""
    # 按类别统计销售额
    by_category = df.groupby("category")["sales"].sum()
    print("按类别销售额:\n", by_category)

    # 按类别和地区统计
    by_both = df.groupby(["category", "region"]).agg(
        {
            "sales": ["sum", "mean", "count"],
            "quantity": "sum",
            "cost": "mean",
        }
    )
    print("\n按类别和地区统计:\n", by_both)
    return by_both


def transform_example(df: pd.DataFrame) -> pd.DataFrame:
    """transform 方法：为每行添加分组统计"""
    # 添加类别平均销售额
    df["category_avg_sales"] = df.groupby("category")["sales"].transform("mean")

    # 添加地区总销售额
    df["region_total_sales"] = df.groupby("region")["sales"].transform("sum")

    # 添加每行销售额占类别总额的百分比
    df["sales_pct_of_category"] = df["sales"] / df.groupby("category")["sales"].transform("sum") * 100

    return df


def filter_example(df: pd.DataFrame) -> pd.DataFrame:
    """过滤分组"""
    # 过滤出销售额超过平均值的类别
    high_value_categories = df.groupby("category").filter(lambda x: x["sales"].mean() > 400)
    print(f"高价值类别订单数: {len(high_value_categories)}")
    return high_value_categories


def pivot_table_example(df: pd.DataFrame) -> pd.DataFrame:
    """透视表"""
    pivot = pd.pivot_table(
        df,
        values="sales",
        index="region",
        columns="category",
        aggfunc="sum",
        fill_value=0,
    )
    print("\n透视表:\n", pivot)
    return pivot


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("高级分组聚合示例")
    print("=" * 60)

    df = create_sample_data()
    print(f"数据形状: {df.shape}")
    print(f"数据预览:\n{df.head()}")

    print("\n" + "=" * 60)
    print("基础分组聚合")
    print("=" * 60)
    basic_groupby(df)

    print("\n" + "=" * 60)
    print("transform 方法")
    print("=" * 60)
    df = transform_example(df)
    print(df[["category", "sales", "category_avg_sales", "sales_pct_of_category"]].head(10))

    print("\n" + "=" * 60)
    print("过滤分组")
    print("=" * 60)
    filter_example(df)

    print("\n" + "=" * 60)
    print("透视表")
    print("=" * 60)
    pivot_table_example(df)


if __name__ == "__main__":
    main()
