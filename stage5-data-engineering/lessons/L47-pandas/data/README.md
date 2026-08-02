# L48 数据集说明

本目录包含 L48 Pandas 完整实战课程使用的样本数据集。

---

## 📊 数据集概述

### sample_orders.csv

**订单数据集** - 用于性能测试和优化实践

- **行数**: 1,005,000 行（包含 0.5% 重复）
- **文件大小**: ~200 MB
- **用途**: 性能基准测试、向量化操作、内存优化

### sample_products.csv

**产品数据集** - 用于关联查询测试

- **行数**: 200 行
- **文件大小**: ~5 KB
- **用途**: JOIN 操作、分组聚合

---

## 📋 字段说明

### sample_orders.csv

| 字段             | 类型     | 说明                                 | 示例        |
| ---------------- | -------- | ------------------------------------ | ----------- |
| `order_id`       | string   | 订单唯一标识                         | ORD000001   |
| `user_id`        | int64    | 用户ID（1-50000）                    | 12345       |
| `product_id`     | int64    | 产品ID（1-200）                      | 42          |
| `quantity`       | int64    | 订单数量（1-20，含异常值-1）         | 5           |
| `price`          | float64  | 订单金额（10.0-1000.0，含缺失值）    | 299.99      |
| `order_date`     | datetime | 订单日期（2023-01-01 至 2024-12-31） | 2024-06-15  |
| `status`         | string   | 订单状态                             | completed   |
| `payment_method` | string   | 支付方式                             | credit_card |

**订单状态分布**:

- `pending`: 20%
- `completed`: 70%
- `cancelled`: 10%

**支付方式分布**:

- `credit_card`: 40%
- `debit_card`: 30%
- `paypal`: 20%
- `cash`: 10%

### sample_products.csv

| 字段           | 类型    | 说明                  | 示例        |
| -------------- | ------- | --------------------- | ----------- |
| `product_id`   | int64   | 产品唯一标识（1-200） | 1           |
| `product_name` | string  | 产品名称              | Laptop 45   |
| `category`     | string  | 产品类别              | Electronics |
| `cost`         | float64 | 成本价格（5.0-500.0） | 399.99      |

**产品类别**:

- Electronics（电子产品）
- Clothing（服装）
- Food（食品）
- Books（图书）
- Home（家居）

---

## 🔍 数据特征

### 脏数据（模拟真实场景）

1. **price 缺失值**: 5%（约 50,000 行）
   - 用于测试缺失值处理和填充策略

2. **quantity 异常值**: 1%（约 10,000 行为 -1）
   - 用于测试数据清洗和异常值检测

3. **重复订单**: 0.5%（约 5,000 行重复）
   - 用于测试去重操作和数据完整性检查

### 数据分布

- **用户数**: 50,000 个唯一用户
- **产品数**: 200 个唯一产品
- **日期范围**: 2023-01-01 至 2024-12-31（2年）
- **订单金额**: 10.0 至 1000.0（均匀分布）

---

## 🚀 生成方法

### 使用数据生成脚本

```bash
# 进入数据目录
cd stage5-data-engineering/lessons/L48-pandas-complete/data

# 运行生成脚本
python generate_data.py
```

### 输出示例

```
============================================================
📊 L48 Pandas 性能测试数据生成器
============================================================

🚀 开始生成 1,000,000 行订单数据...
💉 注入脏数据...
   ✓ 注入 50,000 个 price 缺失值（5%）
   ✓ 注入 10,000 个 quantity 异常值（1%）
   ✓ 添加 5,000 行重复订单（0.5%）
✅ 订单数据生成完成: 1,005,000 行
💾 保存订单数据到 sample_orders.csv...
   ✓ 文件大小: 201.34 MB

🚀 开始生成 200 行产品数据...
✅ 产品数据生成完成: 200 行
💾 保存产品数据到 sample_products.csv...
   ✓ 文件大小: 5.42 KB

============================================================
📈 数据统计
============================================================
订单数据:
  - 总行数: 1,005,000
  - price 缺失值: 50,000 (5.0%)
  - quantity 异常值: 10,000 (1.0%)
  - 重复 order_id: 5,000 (0.5%)

产品数据:
  - 总行数: 200
  - 类别数: 5

✅ 所有数据生成完成!
```

---

## 💡 使用示例

### 加载数据

```python
import pandas as pd

# 加载订单数据
orders = pd.read_csv("data/sample_orders.csv", parse_dates=["order_date"])

# 加载产品数据
products = pd.read_csv("data/sample_products.csv")

print(f"订单数据: {len(orders):,} 行")
print(f"产品数据: {len(products)} 行")
```

### 基础数据检查

```python
# 检查缺失值
print("缺失值统计:")
print(orders.isnull().sum())

# 检查异常值
print(f"\nquantity 为 -1 的行数: {(orders['quantity'] == -1).sum()}")

# 检查重复
print(f"重复 order_id 数量: {orders['order_id'].duplicated().sum()}")
```

### 数据清洗示例

```python
# 删除重复订单
orders_clean = orders.drop_duplicates(subset=["order_id"], keep="first")

# 过滤异常数量
orders_clean = orders_clean[orders_clean["quantity"] > 0]

# 填充缺失价格（使用中位数）
median_price = orders_clean["price"].median()
orders_clean["price"].fillna(median_price, inplace=True)

print(f"清洗后: {len(orders_clean):,} 行")
```

---

## 📝 注意事项

1. **随机种子**: 数据生成使用固定随机种子（seed=42），确保结果可复现
2. **文件大小**: sample_orders.csv 约 200MB，确保有足够磁盘空间
3. **内存需求**: 加载完整数据集需要约 500MB 内存
4. **Git 忽略**: CSV 文件已添加到 .gitignore，不会提交到仓库

---

## 🔗 相关资源

- [L16 课程说明](../README.md)
- [数据生成脚本](generate_data.py)
- [性能优化示例](../demos/)
- [练习题](../exercises/)

---

**版本**: 1.0.0
