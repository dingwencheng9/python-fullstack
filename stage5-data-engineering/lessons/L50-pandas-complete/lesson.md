# L50: Pandas Complete - 进阶数据处理技术

> **课程编号**: L50
> **所属阶段**: Stage 5 - 数据工程
> **预计时长**: 4 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: L47
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


---

## 📌 学习目标

完成本课程后，你将能够：

1. **掌握高级分组聚合**：GroupBy 高级用法、transform、agg 多函数
2. **精通复杂连接操作**：merge、join、concat 高级场景
3. **处理时间序列数据**：重采样、滚动窗口、时区处理
4. **实现窗口函数**：移动统计、累计计算、排名窗口
5. **优化大数据处理**：分块策略、内存映射、加速技巧

---

## 📚 课程内容

### 第一部分：高级分组聚合

#### 1.1 GroupBy 核心概念回顾

```python
import pandas as pd
import numpy as np

# 创建示例数据
df = pd.DataFrame({
    "category": ["A", "B", "A", "B", "A", "B"],
    "subcategory": ["X", "X", "Y", "Y", "X", "Y"],
    "value": [10, 20, 30, 40, 50, 60],
    "quantity": [1, 2, 3, 4, 5, 6],
})
```

#### 1.2 多层级分组与聚合

```python
# 单层分组
result = df.groupby("category")["value"].sum()

# 多层分组
result = df.groupby(["category", "subcategory"]).agg({
    "value": ["sum", "mean", "max"],
    "quantity": ["sum", "count"],
})
```

#### 1.3 transform 方法

```python
# 为每行添加分组统计
df["category_mean"] = df.groupby("category")["value"].transform("mean")
df["value_vs_category_mean"] = df["value"] / df["category_mean"]
```

#### 1.4 过滤分组

```python
# 过滤出总和大于 50 的分组
filtered = df.groupby("category").filter(lambda x: x["value"].sum() > 50)
```

---

### 第二部分：复杂连接操作

#### 2.1 merge 基础回顾

```python
# 创建连接示例数据
df1 = pd.DataFrame({
    "key": ["A", "B", "C"],
    "value1": [1, 2, 3],
})

df2 = pd.DataFrame({
    "key": ["A", "B", "D"],
    "value2": [10, 20, 40],
})
```

#### 2.2 多种连接类型

```python
# 内连接（默认）
inner = pd.merge(df1, df2, on="key", how="inner")

# 左连接
left = pd.merge(df1, df2, on="key", how="left")

# 全外连接
outer = pd.merge(df1, df2, on="key", how="outer")

# 交叉连接（笛卡尔积）
cross = pd.merge(df1, df2, how="cross")
```

#### 2.3 复合键连接

```python
df1 = pd.DataFrame({
    "year": [2020, 2021, 2020],
    "quarter": ["Q1", "Q1", "Q2"],
    "sales": [100, 150, 120],
})

df2 = pd.DataFrame({
    "year": [2020, 2020, 2021],
    "quarter": ["Q1", "Q2", "Q1"],
    "profit": [20, 25, 30],
})

# 使用复合键连接
result = pd.merge(df1, df2, on=["year", "quarter"])
```

#### 2.4 concat 高级用法

```python
# 沿轴连接
df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
df3 = pd.DataFrame({"C": [9, 10], "D": [11, 12]})

# 列拼接
result = pd.concat([df1, df2], axis=1)

# 行拼接
result = pd.concat([df1, df3], axis=1)

# 忽略索引
result = pd.concat([df1, df2], ignore_index=True)

# 层次化索引
result = pd.concat([df1, df2], keys=["first", "second"])
```

---

### 第三部分：时间序列处理

#### 3.1 DatetimeIndex

```python
# 创建时间序列数据
dates = pd.date_range("2024-01-01", periods=365, freq="D")
df = pd.DataFrame({
    "date": dates,
    "value": np.random.randn(365).cumsum(),
})
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
```

#### 3.2 重采样

```python
# 日 -> 月（月末）
monthly = df.resample("ME")["value"].sum()

# 日 -> 周
weekly = df.resample("W")["value"].mean()

# 重采样填充
monthly_filled = df.resample("ME").asfreq().fillna(method="ffill")
```

#### 3.3 滚动窗口

```python
# 移动平均
df["ma_7"] = df["value"].rolling(window=7).mean()
df["ma_30"] = df["value"].rolling(window=30).mean()

# 指数加权移动平均
df["ewma"] = df["value"].ewm(span=30).mean()

# 滚动窗口自定义函数
df["rolling_std"] = df["value"].rolling(window=20).std()
```

#### 3.4 时区处理

```python
# 设置时区
df_utc = df.tz_localize("UTC")
df_tokyo = df_utc.tz_convert("Asia/Tokyo")

# 直接创建带时区的时间戳
dates = pd.date_range("2024-01-01", periods=10, tz="Asia/Shanghai")
```

---

### 第四部分：窗口函数

#### 4.1 Expanding 窗口

```python
# 累计计算
df["cumsum"] = df["value"].expanding().sum()
df["cummax"] = df["value"].expanding().max()

# 累计百分比
df["cum_pct"] = df["value"].expanding().apply(
    lambda x: x.iloc[-1] / x.sum() * 100
)
```

#### 4.2 排名与百分位

```python
# 组内排名
df["rank"] = df.groupby("category")["value"].rank(method="dense", ascending=False)

# 百分位排名
df["pct_rank"] = df.groupby("category")["value"].rank(pct=True)
```

#### 4.3 lag/lead 操作

```python
# shift 实现 lag
df["prev_value"] = df["value"].shift(1)
df["next_value"] = df["value"].shift(-1)

# 计算变化率
df["change"] = df["value"] - df["prev_value"]
df["change_pct"] = (df["value"] - df["prev_value"]) / df["prev_value"] * 100
```

---

### 第五部分：性能优化

#### 5.1 分块处理大文件

```python
# 分块读取
chunks = []
for chunk in pd.read_csv("large_file.csv", chunksize=100_000):
    # 处理每个块
    processed = chunk.groupby("category")["value"].sum()
    chunks.append(processed)

# 合并结果
result = pd.concat(chunks).groupby(level=0).sum()
```

#### 5.2 category 类型优化

```python
# 字符串列转为 category
high_cardinality_col = df["high_cardinality_col"].astype("category")

# category 使用字典序排序
df["status"] = pd.Categorical(
    df["status"],
    categories=["pending", "processing", "completed", "failed"],
    ordered=True,
)
```

#### 5.3 eval 与 query

```python
# 使用 eval 进行高效计算
result = pd.eval("value1 + value2 * 2", target=df)

# 使用 query 进行过滤
filtered = df.query("category == 'A' and value > 10")
```

---


### 第六部分：Pandas 高级技巧

#### 6.1 链式调用与管道操作

```python
import pandas as pd
import numpy as np

# 创建示例数据
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "age": [25, 30, 35, 40, 45],
    "salary": [50000, 60000, 70000, 80000, 90000],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "join_date": ["2020-01-15", "2019-06-20", "2021-03-10", "2018-11-05", "2020-08-25"],
})

# 使用 pipe 进行链式操作
def add_bonus(df):
    df = df.copy()
    df["bonus"] = df["salary"] * 0.1
    return df

def add_tax(df):
    df = df.copy()
    df["tax"] = df["salary"] * 0.15
    return df

def add_net(df):
    df = df.copy()
    df["net_salary"] = df["salary"] + df["bonus"] - df["tax"]
    return df

# 链式调用
result = (
    df
    .pipe(add_bonus)
    .pipe(add_tax)
    .pipe(add_net)
)

print(result)
```

#### 6.2 条件赋值与 map

```python
# 使用 np.select 进行多条件赋值
df = pd.DataFrame({
    "score": [85, 72, 90, 55, 78, 92, 45, 88],
})

# 定义条件和对应的值
conditions = [
    df["score"] >= 90,      # 优秀
    df["score"] >= 80,      # 良好
    df["score"] >= 70,      # 中等
    df["score"] >= 60,      # 及格
]
choices = ["A", "B", "C", "D"]

df["grade"] = np.select(conditions, choices, default="F")

# 使用 map 进行映射
grade_map = {
    "A": "优秀",
    "B": "良好",
    "C": "中等",
    "D": "及格",
    "F": "不及格",
}
df["grade_cn"] = df["grade"].map(grade_map)

print(df)
```

#### 6.3 explode 与列表展开

```python
# 处理包含列表的列
df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "skills": [
        ["Python", "Java", "SQL"],
        ["JavaScript", "React"],
        ["Python", "Go", "Rust", "C++"],
    ],
})

# 展开列表为多行
exploded = df.explode("skills")
print(exploded)

# 统计技能出现次数
skill_counts = exploded["skills"].value_counts()
print(skill_counts)
```

#### 6.4 crosstab 交叉表

```python
# 创建交叉表
df = pd.DataFrame({
    "gender": ["男", "女", "男", "女", "男", "女"],
    "department": ["IT", "IT", "HR", "HR", "Sales", "Sales"],
    "satisfaction": ["高", "中", "高", "低", "中", "高"],
})

# 简单交叉表
crosstab = pd.crosstab(df["department"], df["satisfaction"])
print(crosstab)

# 带边距的交叉表
crosstab_with_margins = pd.crosstab(
    df["department"], 
    df["satisfaction"],
    margins=True,
    margins_name="总计"
)
print(crosstab_with_margins)

# 百分比交叉表
crosstab_pct = pd.crosstab(
    df["department"], 
    df["satisfaction"],
    normalize="index"  # 按行归一化
) * 100
print(crosstab_pct)
```

### 第七部分：复杂数据清洗

#### 7.1 字符串处理高级技巧

```python
import re

df = pd.DataFrame({
    "text": [
        "订单号: ORD-2024-001, 金额: ¥1234.56",
        "订单号: ORD-2024-002, 金额: ¥2345.67",
        "订单号: ORD-2024-003, 金额: ¥345.00",
        "用户邮箱: user@example.com, 注册时间: 2024-01-15",
    ],
})

# 提取数字
df["order_id"] = df["text"].str.extract(r"订单号: (ORD-\d+-\d+)")
df["amount"] = df["text"].str.extract(r"金额: ¥([\d.]+)")

# 提取邮箱
df["email"] = df["text"].str.extract(r"邮箱: (\S+@\S+)")

# 提取日期
df["date"] = df["text"].str.extract(r"(\d{4}-\d{2}-\d{2})")

print(df)
```

#### 7.2 缺失值高级处理

```python
import numpy as np
import pandas as pd

# 创建包含缺失值的数据
df = pd.DataFrame({
    "A": [1, 2, np.nan, 4, 5],
    "B": [np.nan, 2, 3, np.nan, 5],
    "C": [1, np.nan, np.nan, np.nan, 5],
})

# 插值填充
df_filled = df.interpolate(method="linear")

# 按分组填充
df["group"] = ["X", "X", "Y", "Y", "Y"]
df["A_filled"] = df.groupby("group")["A"].transform(lambda x: x.fillna(x.mean()))

# 前向/后向填充
df["B_ffill"] = df["B"].ffill()
df["B_bfill"] = df["B"].bfill()

# 使用模型预测填充
from sklearn.ensemble import RandomForestRegressor

def predict_fill(df, column):
    """使用其他列预测缺失值"""
    df_temp = df.copy()
    missing = df_temp[column].isna()
    
    if missing.sum() == 0:
        return df_temp[column]
    
    features = df_temp.columns.drop([column, "group"])
    X_train = df_temp.loc[~missing, features]
    y_train = df_temp.loc[~missing, column]
    X_pred = df_temp.loc[missing, features]
    
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    
    df_temp.loc[missing, column] = model.predict(X_pred)
    return df_temp[column]

print(df)
```

#### 7.3 重复值处理

```python
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Alice", "Charlie", "Bob", "Bob"],
    "age": [25, 30, 25, 35, 30, 30],
    "city": ["Beijing", "Shanghai", "Beijing", "Guangzhou", "Shanghai", "Shanghai"],
})

# 查找重复行
duplicates = df[df.duplicated(keep=False)]
print("重复行:")
print(duplicates)

# 基于多列查找重复
duplicates_multi = df[df.duplicated(subset=["name", "age"], keep=False)]
print("基于 name 和 age 的重复:")
print(duplicates_multi)

# 删除重复行（保留最后一条）
df_unique = df.drop_duplicates(subset=["name"], keep="last")
print("去重后:")
print(df_unique)

# 标记重复行
df["is_duplicate"] = df.duplicated(subset=["name"], keep=False)
print(df)
```

#### 7.4 异常值检测与处理

```python
import numpy as np
import pandas as pd

# 创建示例数据（包含异常值）
df = pd.DataFrame({
    "value": [10, 12, 11, 13, 12, 500, 11, 12, 1000, 13],
})

# 方法1: Z-score 方法
from scipy import stats

df["z_score"] = np.abs(stats.zscore(df["value"]))
df["is_outlier_zscore"] = df["z_score"] > 2

# 方法2: IQR 方法
Q1 = df["value"].quantile(0.25)
Q3 = df["value"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df["is_outlier_iqr"] = (df["value"] < lower_bound) | (df["value"] > upper_bound)

print(df)
print(f"IQR 边界: [{lower_bound}, {upper_bound}]")

# 处理异常值（替换为边界值）
df["value_cleaned"] = df["value"].clip(lower=lower_bound, upper=upper_bound)
print(df)
```

### 第八部分：Pandas 与 SQL 对比

#### 8.1 SQL 操作对照表

| SQL 操作 | Pandas 实现 |
|----------|-------------|
| `SELECT * FROM df` | `df` |
| `SELECT a, b FROM df` | `df[["a", "b"]]` |
| `WHERE a > 1` | `df[df["a"] > 1]` |
| `DISTINCT` | `df.drop_duplicates()` |
| `ORDER BY a DESC` | `df.sort_values("a", ascending=False)` |
| `GROUP BY a` | `df.groupby("a")` |
| `HAVING COUNT(*) > 1` | `df.groupby("a").filter(lambda x: len(x) > 1)` |
| `JOIN` | `pd.merge(df1, df2, on="key")` |
| `UNION` | `pd.concat([df1, df2])` |
| `LIMIT 10` | `df.head(10)` |
| `OFFSET 5` | `df.iloc[5:]` |

#### 8.2 复杂 SQL 转换为 Pandas

```python
import pandas as pd
import numpy as np

# 模拟 SQL 查询
# SELECT department, AVG(salary) as avg_salary, COUNT(*) as count
# FROM employees
# WHERE hire_date >= '2020-01-01'
# GROUP BY department
# HAVING COUNT(*) > 5
# ORDER BY avg_salary DESC
# LIMIT 10

employees = pd.DataFrame({
    "name": [f"Employee_{i}" for i in range(100)],
    "department": np.random.choice(["IT", "HR", "Sales", "Marketing"], 100),
    "salary": np.random.randint(5000, 50000, 100),
    "hire_date": pd.date_range("2018-01-01", periods=100, freq="D"),
})

# 转换为 Pandas
result = (
    employees[employees["hire_date"] >= "2020-01-01"]
    .groupby("department")
    .agg(
        avg_salary=("salary", "mean"),
        count=("salary", "count"),
    )
    .reset_index()
    .query("count > 5")
    .sort_values("avg_salary", ascending=False)
    .head(10)
)

print(result)
```

#### 8.3 窗口函数对比

```python
# SQL 窗口函数 vs Pandas

# SELECT 
#   name,
#   department,
#   salary,
#   AVG(salary) OVER (PARTITION BY department) as dept_avg,
#   salary - AVG(salary) OVER (PARTITION BY department) as diff
# FROM employees

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "department": ["IT", "IT", "HR", "HR", "IT"],
    "salary": [50000, 60000, 55000, 48000, 70000],
})

# Pandas 窗口函数
df["dept_avg"] = df.groupby("department")["salary"].transform("mean")
df["diff"] = df["salary"] - df["dept_avg"]

# RANK, ROW_NUMBER, DENSE_RANK
df["rank"] = df.groupby("department")["salary"].rank(method="dense", ascending=False)

print(df)
```

### 第九部分：Pandas 性能优化

#### 9.1 数据类型优化

```python
import pandas as pd
import numpy as np

# 创建大型 DataFrame
df = pd.DataFrame({
    "int_col": np.random.randint(0, 100, 1000000),
    "float_col": np.random.randn(1000000),
    "category_col": np.random.choice(["A", "B", "C", "D"], 1000000),
    "date_col": pd.date_range("2020-01-01", periods=1000000, freq="min"),
})

print(f"原始内存: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 优化整数类型
df["int_col"] = pd.to_numeric(df["int_col"], downcast="integer")

# 优化浮点类型
df["float_col"] = pd.to_numeric(df["float_col"], downcast="float")

# 转换为类别类型
df["category_col"] = df["category_col"].astype("category")

# 使用更小的日期类型
df["date_col"] = pd.to_datetime(df["date_col"]).astype("datetime64[ns]")

print(f"优化后内存: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
```

#### 9.2 向量化操作

```python
import pandas as pd
import numpy as np

# ❌ 低效：使用 apply
df = pd.DataFrame({"value": range(1000000)})

# 方法1：apply（慢）
df["squared_apply"] = df["value"].apply(lambda x: x ** 2)

# 方法2：向量化（快）
df["squared_vec"] = df["value"] ** 2

# 条件逻辑向量化
# ❌ 低效
df["label_apply"] = df["value"].apply(
    lambda x: "large" if x > 500000 else "small"
)

# ✅ 高效
df["label_vec"] = np.where(df["value"] > 500000, "large", "small")

# 时间对比
import time

df = pd.DataFrame({"value": range(1000000)})

start = time.time()
df["squared"] = df["value"].apply(lambda x: x ** 2)
apply_time = time.time() - start

start = time.time()
df["squared"] = df["value"] ** 2
vec_time = time.time() - start

print(f"apply: {apply_time:.4f}s, 向量化: {vec_time:.4f}s")
print(f"加速比: {apply_time / vec_time:.1f}x")
```

#### 9.3 分块处理大数据

```python
import pandas as pd

# 分块读取大文件
chunks = []
for chunk in pd.read_csv("large_file.csv", chunksize=100000):
    # 在每个块上执行操作
    processed = chunk[chunk["value"] > 100]
    chunks.append(processed)

# 合并结果
result = pd.concat(chunks, ignore_index=True)

# 或者使用 groupby + transform（内存友好）
def process_chunk(chunk):
    chunk["mean"] = chunk.groupby("category")["value"].transform("mean")
    return chunk

result = pd.concat([
    process_chunk(chunk) 
    for chunk in pd.read_csv("large_file.csv", chunksize=100000)
])
```

#### 9.4 使用 PyArrow 加速

```python
import pandas as pd

# 使用 PyArrow 引擎读取（更快）
df = pd.read_csv("data.csv", engine="pyarrow")

# 保存为 Parquet 格式（更小、更快）
df.to_parquet("data.parquet", engine="pyarrow")

# 读取 Parquet
df = pd.read_parquet("data.parquet")

# 使用 pyarrow 进行计算
import pyarrow.compute as pc

# PyArrow 列式计算比 Pandas 更快
result = pc.sum(df["column"].to_numpy())
```

### 第十部分：常见问题与解决方案

#### 10.1 SettingWithCopyWarning

```python
import pandas as pd

# 问题代码（会产生警告）
df = pd.DataFrame({"value": [1, 2, 3, 4, 5]})
subset = df[df["value"] > 2]
subset["value"] = subset["value"] * 2  # SettingWithCopyWarning!

# 解决方案1：使用 .copy()
df = pd.DataFrame({"value": [1, 2, 3, 4, 5]})
subset = df[df["value"] > 2].copy()
subset["value"] = subset["value"] * 2

# 解决方案2：使用 .loc
df = pd.DataFrame({"value": [1, 2, 3, 4, 5]})
df.loc[df["value"] > 2, "value"] *= 2

# 解决方案3：使用 .where
df = pd.DataFrame({"value": [1, 2, 3, 4, 5]})
df["value"] = df["value"].where(df["value"] <= 2, df["value"] * 2)
```

#### 10.2 内存不足问题

```python
import pandas as pd

# 监控内存使用
def get_memory_usage(df):
    return f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"

# 分批处理数据
def process_in_batches(df, batch_size=100000):
    results = []
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        # 处理每个批次
        processed = batch.groupby("category").sum()
        results.append(processed)
    return pd.concat(results)

# 使用更高效的数据类型
def optimize_dtypes(df):
    for col in df.select_dtypes(include=["int"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="integer")
    for col in df.select_dtypes(include=["float"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="float")
    return df
```

#### 10.3 日期处理常见问题

```python
import pandas as pd

# 问题1：字符串日期
df = pd.DataFrame({"date": ["2024-01-15", "2024/01/16", "15-01-2024"]})

# 统一转换为日期
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

# 问题2：时区处理
df = pd.DataFrame({
    "timestamp": pd.date_range("2024-01-01", periods=5, freq="h", tz="UTC")
})

# 转换时区
df["timestamp_cst"] = df["timestamp"].dt.tz_convert("Asia/Shanghai")

# 问题3：解析多种格式
def parse_date(date_str):
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    return pd.NaT

df["date"] = df["date"].apply(parse_date)
```

#### 10.4 多重索引操作

```python
import pandas as pd
import numpy as np

# 创建多层索引 DataFrame
df = pd.DataFrame({
    ("A", "x"): [1, 2, 3],
    ("A", "y"): [4, 5, 6],
    ("B", "x"): [7, 8, 9],
    ("B", "y"): [10, 11, 12],
})

# 设置列索引名
df.columns.names = ["group", "metric"]

# 访问单层
print(df["A"])  # 所有 A 组的数据
print(df[("A", "x")])  # 特定列

# 索引重命名
df = df.rename(columns={"x": "value_x", "y": "value_y"})

# 堆叠和展开
stacked = df.stack()  # 转为长格式
unstacked = stacked.unstack()  # 恢复宽格式

# 重置索引
df_flat = df.reset_index()
```



---

## 📂 课程资源

### 示例代码

- `examples/01_advanced_groupby.py` - 高级分组聚合示例
- `examples/02_complex_joins.py` - 复杂连接操作示例
- `examples/03_time_series.py` - 时间序列处理示例
- `examples/04_window_functions.py` - 窗口函数示例
- `examples/05_performance.py` - 性能优化示例

### 练习项目

- `exercises/exercise_01_sales_analysis.py` - 销售数据分析
- `exercises/exercise_02_time_series_forecast.py` - 时间序列预测
- `exercises/exercise_03_financial_portfolio.py` - 投资组合分析

---

## 🧪 测试

运行测试：

```bash
cd stage5-data-engineering/lessons/L50-pandas-complete
pytest tests/ -v
```

---

## 📖 参考资料

- [Pandas User Guide: Group By](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Pandas User Guide: Merge](https://pandas.pydata.org/docs/user_guide/merging.html)
- [Pandas User Guide: Time Series](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- [Pandas User Guide: Window](https://pandas.pydata.org/docs/user_guide/window.html)

---

## ✅ 完成标准

- [ ] 完成所有示例代码运行
- [ ] 完成练习项目
- [ ] 通过全部测试

---

## 🔗 下一步

- [L51: 异步数据管道](../L51-async-data-pipeline/README.md)
- [L52: NumPy RAG PoC](../L52-numpy-rag-poc/README.md)

---

**最后更新**: 2026-07-17
