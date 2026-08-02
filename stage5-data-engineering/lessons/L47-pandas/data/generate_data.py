"""数据生成脚本 - L16 Pandas 高性能数据处理

from __future__ import annotations

生成用于性能测试的样本数据集:
- sample_orders.csv: 100万行订单数据（包含脏数据）
- sample_products.csv: 200行产品数据
"""

from __future__ import annotations

from pathlib import Path
import random

import numpy as np
import pandas as pd


def generate_sample_orders(n_rows: int = 1_000_000, seed: int = 42) -> pd.DataFrame:
    """生成订单数据集

    Args:
        n_rows: 生成的订单行数（不包含重复）
        seed: 随机种子，保证数据可复现

    Returns:
        包含订单数据的 DataFrame

    字段说明:
        - order_id: 订单ID（唯一，格式 ORD001 ~ ORDxxxxxx）
        - user_id: 用户ID（1-50000）
        - product_id: 产品ID（1-200）
        - quantity: 订单数量（1-20，包含1%异常值-1）
        - price: 订单金额（10.0-1000.0，包含5%缺失值）
        - order_date: 订单日期（2023-01-01 到 2024-12-31）
        - status: 订单状态（pending, completed, cancelled）
        - payment_method: 支付方式（credit_card, debit_card, paypal, cash）

    脏数据:
        - 5% price 缺失值（NaN）
        - 1% quantity 异常值（-1）
        - 0.5% 重复订单（通过复制行实现）
    """
    np.random.seed(seed)
    random.seed(seed)

    print(f"🚀 开始生成 {n_rows:,} 行订单数据...")

    # 生成基础数据
    data = {
        "order_id": [f"ORD{i:06d}" for i in range(1, n_rows + 1)],
        "user_id": np.random.randint(1, 50_001, n_rows),
        "product_id": np.random.randint(1, 201, n_rows),
        "quantity": np.random.randint(1, 21, n_rows),
        "price": np.random.uniform(10.0, 1000.0, n_rows),
        "order_date": pd.date_range(start="2023-01-01", end="2024-12-31", periods=n_rows),
        "status": np.random.choice(["pending", "completed", "cancelled"], n_rows, p=[0.2, 0.7, 0.1]),
        "payment_method": np.random.choice(["credit_card", "debit_card", "paypal", "cash"], n_rows, p=[0.4, 0.3, 0.2, 0.1]),
    }

    df = pd.DataFrame(data)

    # 注入脏数据
    print("💉 注入脏数据...")

    # 1. 5% price 缺失值
    missing_price_indices = np.random.choice(n_rows, size=int(n_rows * 0.05), replace=False)
    df.loc[missing_price_indices, "price"] = np.nan
    print(f"   ✓ 注入 {len(missing_price_indices):,} 个 price 缺失值（5%）")

    # 2. 1% quantity 异常值（-1）
    anomaly_quantity_indices = np.random.choice(n_rows, size=int(n_rows * 0.01), replace=False)
    df.loc[anomaly_quantity_indices, "quantity"] = -1
    print(f"   ✓ 注入 {len(anomaly_quantity_indices):,} 个 quantity 异常值（1%）")

    # 3. 0.5% 重复订单
    duplicate_count = int(n_rows * 0.005)
    duplicate_indices = np.random.choice(n_rows, size=duplicate_count, replace=False)
    duplicate_rows = df.iloc[duplicate_indices].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    print(f"   ✓ 添加 {duplicate_count:,} 行重复订单（0.5%）")

    # 随机打乱顺序
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    print(f"✅ 订单数据生成完成: {len(df):,} 行")
    return df


def generate_sample_products(n_products: int = 200, seed: int = 42) -> pd.DataFrame:
    """生成产品数据集

    Args:
        n_products: 生成的产品数量
        seed: 随机种子，保证数据可复现

    Returns:
        包含产品数据的 DataFrame

    字段说明:
        - product_id: 产品ID（1-200）
        - product_name: 产品名称
        - category: 产品类别（Electronics, Clothing, Food, Books, Home）
        - cost: 成本价格（5.0-500.0）
    """
    np.random.seed(seed)
    random.seed(seed)

    print(f"🚀 开始生成 {n_products} 行产品数据...")

    categories = ["Electronics", "Clothing", "Food", "Books", "Home"]
    category_prefixes = {
        "Electronics": ["Laptop", "Phone", "Tablet", "Camera", "Headphone"],
        "Clothing": ["Shirt", "Pants", "Dress", "Jacket", "Shoes"],
        "Food": ["Snack", "Beverage", "Fruit", "Vegetable", "Meat"],
        "Books": ["Novel", "Textbook", "Magazine", "Comic", "Dictionary"],
        "Home": ["Lamp", "Chair", "Table", "Curtain", "Carpet"],
    }

    products = []
    for i in range(1, n_products + 1):
        category = random.choice(categories)
        prefix = random.choice(category_prefixes[category])
        product_name = f"{prefix} {i % 100 + 1}"
        cost = round(np.random.uniform(5.0, 500.0), 2)

        products.append(
            {
                "product_id": i,
                "product_name": product_name,
                "category": category,
                "cost": cost,
            }
        )

    df = pd.DataFrame(products)
    print(f"✅ 产品数据生成完成: {len(df)} 行")
    return df


def main() -> None:
    """生成并保存样本数据"""
    print("=" * 60)
    print("📊 L16 Pandas 性能测试数据生成器")
    print("=" * 60)
    print()

    # 设置输出目录
    output_dir = Path(__file__).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成订单数据
    orders_df = generate_sample_orders(n_rows=1_000_000, seed=42)
    orders_file = output_dir / "sample_orders.csv"
    print(f"💾 保存订单数据到 {orders_file.name}...")
    orders_df.to_csv(orders_file, index=False)
    file_size_mb = orders_file.stat().st_size / (1024 * 1024)
    print(f"   ✓ 文件大小: {file_size_mb:.2f} MB")
    print()

    # 生成产品数据
    products_df = generate_sample_products(n_products=200, seed=42)
    products_file = output_dir / "sample_products.csv"
    print(f"💾 保存产品数据到 {products_file.name}...")
    products_df.to_csv(products_file, index=False)
    file_size_kb = products_file.stat().st_size / 1024
    print(f"   ✓ 文件大小: {file_size_kb:.2f} KB")
    print()

    # 数据统计
    print("=" * 60)
    print("📈 数据统计")
    print("=" * 60)
    print("订单数据:")
    print(f"  - 总行数: {len(orders_df):,}")

    # price 缺失值
    price_missing = orders_df["price"].isna().sum()
    price_missing_pct = orders_df["price"].isna().mean()
    print(f"  - price 缺失值: {price_missing:,} ({price_missing_pct:.1%})")

    # quantity 异常值
    quantity_anomaly = (orders_df["quantity"] == -1).sum()
    quantity_anomaly_pct = (orders_df["quantity"] == -1).mean()
    print(f"  - quantity 异常值: {quantity_anomaly:,} ({quantity_anomaly_pct:.1%})")

    # 重复订单
    duplicate_count = orders_df["order_id"].duplicated().sum()
    duplicate_pct = orders_df["order_id"].duplicated().mean()
    print(f"  - 重复 order_id: {duplicate_count:,} ({duplicate_pct:.1%})")

    print()
    print("产品数据:")
    print(f"  - 总行数: {len(products_df)}")
    print(f"  - 类别数: {products_df['category'].nunique()}")
    print()
    print("✅ 所有数据生成完成!")


if __name__ == "__main__":
    main()
