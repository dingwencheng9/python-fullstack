"""练习 1: 销售数据分析 - 参考答案"""

from __future__ import annotations

import pandas as pd
import numpy as np


def load_data() -> pd.DataFrame:
    """加载销售数据"""
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
    return df.groupby("category")["sales"].sum().sort_values(ascending=False)


def q2_category_region_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Q2: 每个类别在每个地区的销售额（透视表）"""
    return df.pivot_table(values="sales", index="category", columns="region", aggfunc="sum", fill_value=0)


def q3_growth_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Q3: 计算每个类别的月环比增长率"""
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")

    monthly = df.groupby(["category", "month"])["sales"].sum().unstack(level=0)
    growth = monthly.pct_change() * 100
    return growth.round(2)


def q4_customer_value(df: pd.DataFrame) -> pd.DataFrame:
    """Q4: 识别高价值客户（按累计消费排序，取前 10%）"""
    customer_value = df.groupby("customer_id")["sales"].sum().reset_index()
    customer_value = customer_value.sort_values("sales", ascending=False)
    threshold = customer_value["sales"].quantile(0.9)
    return customer_value[customer_value["sales"] >= threshold]


def q5_category_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Q5: 计算每个类别近7天滚动平均销售额"""
    df = df.copy()
    df["date_only"] = df["date"].dt.date
    daily = df.groupby(["category", "date_only"])["sales"].sum().reset_index()
    daily = daily.sort_values(["category", "date_only"])
    daily["rolling_avg"] = daily.groupby("category")["sales"].transform(lambda x: x.rolling(7, min_periods=1).mean())
    return daily


def q6_profit_margin(df: pd.DataFrame) -> pd.DataFrame:
    """Q6: 计算每个类别、地区的利润率"""
    df = df.copy()
    df["profit"] = df["sales"] - df["cost"]
    df["margin"] = df["profit"] / df["sales"] * 100
    return df.groupby(["category", "region"])["margin"].mean().round(2).unstack()


def q7_cohort_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Q7: 用户留存分析（同月首次购买的用户，后续月份留存率）"""
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")

    first_purchase = df.groupby("customer_id")["month"].min().reset_index()
    first_purchase.columns = ["customer_id", "cohort_month"]

    df = df.merge(first_purchase, on="customer_id")
    df["cohort_index"] = df["month"].astype(int) - df["cohort_month"].astype(int)

    cohort_counts = df.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique()
    cohort_table = cohort_counts.unstack(level=0)

    cohort_size = cohort_table.iloc[:, 0]
    retention = cohort_table.divide(cohort_size, axis=0) * 100
    return retention.round(2)


def q8_seasonality(df: pd.DataFrame) -> pd.DataFrame:
    """Q8: 分析销售数据的周期性（周几最高/最低）"""
    df = df.copy()
    df["day_of_week"] = df["date"].dt.day_name()
    by_day = df.groupby("day_of_week")["sales"].sum()
    by_day = by_day.sort_values(ascending=False)
    return pd.DataFrame({"total_sales": by_day, "rank": range(1, len(by_day) + 1)})


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
    print(q1_top_categories(df))

    print("\n" + "=" * 60)
    print("Q2: 类别-地区销售额透视表")
    print("=" * 60)
    print(q2_category_region_sales(df))

    print("\n" + "=" * 60)
    print("Q3: 月环比增长率")
    print("=" * 60)
    print(q3_growth_rate(df))

    print("\n" + "=" * 60)
    print("Q4: 高价值客户")
    print("=" * 60)
    print(q4_customer_value(df))

    print("\n" + "=" * 60)
    print("Q5: 滚动平均销售额")
    print("=" * 60)
    print(q5_category_trend(df).head(10))

    print("\n" + "=" * 60)
    print("Q6: 利润率分析")
    print("=" * 60)
    print(q6_profit_margin(df))

    print("\n" + "=" * 60)
    print("Q7: 用户留存分析")
    print("=" * 60)
    print(q7_cohort_analysis(df))

    print("\n" + "=" * 60)
    print("Q8: 销售周期性")
    print("=" * 60)
    print(q8_seasonality(df))


if __name__ == "__main__":
    main()
