"""练习 1: 销售数据分析

使用高级 Pandas 技术分析销售数据。
"""

from __future__ import annotations

import pandas as pd
import numpy as np


def load_data() -> pd.DataFrame:
    """加载销售数据"""
    # 创建示例销售数据
    np.random.seed(42)
    n = 10000

    categories = ["电子产品", "服装", "食品", "家居", "美妆"]
    regions = ["华北", "华东", "华南", "西南", "西北"]
    channels = ["线上", "线下", "批发"]

    return pd.DataFrame(
        {
            "order_id": range(1, n + 1),
            "date": pd.date_range("2024-01-01", periods=n, freq="30min"),
            "category": np.random.choice(categories, n),
            "region": np.random.choice(regions, n),
            "channel": np.random.choice(channels, n, p=[0.5, 0.3, 0.2]),
            "sales": np.random.uniform(10, 5000, n).round(2),
            "quantity": np.random.randint(1, 20, n),
            "cost": np.random.uniform(5, 2500, n).round(2),
            "customer_id": np.random.randint(1, 2000, n),
        }
    )


def q1_top_categories(df: pd.DataFrame) -> pd.Series:
    """Q1: 按销售额排序的类别"""
    # 按类别统计总销售额
    # TODO: 实现


def q2_category_region_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Q2: 每个类别在每个地区的销售额（透视表）"""
    # TODO: 实现


def q3_growth_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Q3: 计算每个类别的月环比增长率"""
    # TODO: 实现


def q4_customer_value(df: pd.DataFrame) -> pd.DataFrame:
    """Q4: 识别高价值客户（按累计消费排序，取前 10%）"""
    # TODO: 实现


def q5_category_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Q5: 计算每个类别近7天滚动平均销售额"""
    # TODO: 实现


def q6_profit_margin(df: pd.DataFrame) -> pd.DataFrame:
    """Q6: 计算每个类别、地区的利润率"""
    # TODO: 实现


def q7_cohort_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Q7: 用户留存分析（同月首次购买的用户，后续月份留存率）"""
    # TODO: 实现


def q8_seasonality(df: pd.DataFrame) -> pd.DataFrame:
    """Q8: 分析销售数据的周期性（周几最高/最低）"""
    # TODO: 实现


def main() -> None:
    """主函数"""
    df = load_data()

    print("数据形状:", df.shape)
    print("\n数据预览:")
    print(df.head())

    # 测试各函数
    print("\n" + "=" * 60)
    print("Q1: 按销售额排序的类别")
    print("=" * 60)
    result1 = q1_top_categories(df)
    print(result1)

    print("\n" + "=" * 60)
    print("Q2: 类别-地区销售额透视表")
    print("=" * 60)
    result2 = q2_category_region_sales(df)
    print(result2)

    print("\n" + "=" * 60)
    print("Q3: 月环比增长率")
    print("=" * 60)
    result3 = q3_growth_rate(df)
    print(result3)

    print("\n" + "=" * 60)
    print("Q4: 高价值客户")
    print("=" * 60)
    result4 = q4_customer_value(df)
    print(result4)

    print("\n" + "=" * 60)
    print("Q5: 滚动平均销售额")
    print("=" * 60)
    result5 = q5_category_trend(df)
    print(result5)

    print("\n" + "=" * 60)
    print("Q6: 利润率分析")
    print("=" * 60)
    result6 = q6_profit_margin(df)
    print(result6)

    print("\n" + "=" * 60)
    print("Q7: 用户留存分析")
    print("=" * 60)
    result7 = q7_cohort_analysis(df)
    print(result7)

    print("\n" + "=" * 60)
    print("Q8: 销售周期性")
    print("=" * 60)
    result8 = q8_seasonality(df)
    print(result8)


if __name__ == "__main__":
    main()
