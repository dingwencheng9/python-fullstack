# L49:  DuckDB — 嵌入式数据分析引擎

> **课程时长**: 2-3 小时
> **难度**: ⭐⭐⭐⭐☆（数据工程）
> **所属阶段**: Stage 5 - 数据工程  
> **课程编号**: L49
> **所属阶段**: Stage 5 - 数据工程
> **预计时长**: 2-3 小时
> **难度**: ⭐⭐⭐⭐☆（数据工程）
> **前置课程**: L49
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L48**: Pandas 完整实战
- **L49**: 数据可视化

**如果你还没有学习以上课程，建议先完成前置课程。**

---

> 前置课程: L49 Pandas 完整实战 / L49 数据可视化 | 预计时长: 6h | 难度: ⭐⭐⭐

DuckDB 是一个嵌入式 OLAP 数据库，专为数据分析场景设计。它不需要单独的服务器进程，可以直接在 Python 进程中运行。

## 1. DuckDB 是什么？

### 1.1 为什么需要 DuckDB？

传统数据分析工作流的痛点：

```
CSV/Parquet → Pandas → 内存 → 分析 → 可视化
              ↑ 内存上限、单线程、数据搬运成本高
```

DuckDB 的方式：

```
CSV/Parquet → DuckDB → SQL49 → 结果 → 可视化
              ↑ 列式存储、向量化执行、直接查询文件
```

| 特性       | Pandas            | DuckDB               |
| ---------- | ----------------- | -------------------- |
| 数据量上限 | 内存 (通常 <10GB) | 磁盘 + 内存 (100GB+) |
| 执行引擎   | 单线程            | 向量化 + 多线程      |
| 数据模型   | DataFrame         | 关系型 (SQL)         |
| 文件格式   | 内存中处理        | 直接查询 CSV/Parquet |
| 安装       | 依赖 numpy        | 纯 Python，零依赖    |

### 1.2 安装

```bash
uv add duckdb
# 零依赖，纯 Python，5 秒安装
```

## 2. 基础查询

### 2.1 连接与查询

```python
import duckdb

# 创建内存数据库连接
conn = duckdb.connect()

# SQL49 查询
result = conn.execute("SELECT 42 AS answer").fetchall()
print(result)  # [(42,)]

# 直接返回 DataFrame
df = conn.execute("SELECT * FROM read_csv_auto('data.csv')").df()
```

DuckDB 支持**免导入直接查询文件**，这是它最大的优势。

### 2.2 查询 CSV 文件

```python
# 直接查询 CSV（无需先加载到 DataFrame）
conn = duckdb.connect()
result = conn.execute("""
    SELECT
        region,
        COUNT(*) AS orders,
        ROUND(SUM(amount), 2) AS total,
        ROUND(AVG(amount), 2) AS avg_order
    FROM read_csv_auto('sales.csv')
    WHERE amount > 0
    GROUP BY region
    ORDER BY total DESC
""").df()
```

对于数据分析来说，这比 Pandas 的 `groupby().agg()` 更直观。

### 2.3 查询 Parquet 文件

```python
# Parquet 是列式存储格式，DuckDB 原生支持
result = conn.execute("""
    SELECT
        date_trunc('month', order_date) AS month,
        COUNT(*) AS orders
    FROM read_parquet('orders/*.parquet')
    GROUP BY month
    ORDER BY month
""").df()
```

## 3. DuckDB + Python 深度集成

### 3.1 与 Pandas DataFrame 互操作

```python
import pandas as pd
import duckdb

# Python DataFrame → DuckDB SQL49 查询
df = pd.DataFrame({
    "city": ["北京", "上海", "广州", "深圳"],
    "population": [2154, 2475, 1868, 1768],
})

result = duckdb.sql("""
    SELECT city, population
    FROM df
    WHERE population > 2000
    ORDER BY population DESC
""").df()
print(result)
```

**关键**: `duckdb.sql` 可以直接查询 Python 变量（`df` 是 Python 变量名），无需导入。

### 3.2 Python 变量绑定

```python
min_pop = 2000
result = duckdb.sql(
    "SELECT city, population FROM df WHERE population > ?",
    params=[min_pop]
).df()
```

## 4. 实战：销售分析

### 4.1 生成模拟数据

```python
import duckdb
import numpy as np
import pandas as pd

# 生成 10 万条销售记录
np.random.seed(42)
dates = pd.date_range("2025-01-01", "2025-12-31")
df = pd.DataFrame({
    "order_date": np.random.choice(dates, 100000),
    "region": np.random.choice(["华北", "华东", "华南", "西部"], 100000),
    "category": np.random.choice(["电子产品", "服装", "食品", "家居"], 100000),
    "amount": np.random.uniform(10, 5000, 100000).round(2),
})
```

### 4.2 月度销售趋势

```python
conn = duckdb.connect()
# 注册 DataFrame 为虚拟表
conn.register("sales", df)

monthly = conn.execute("""
    SELECT
        date_trunc('month', order_date) AS month,
        COUNT(*) AS orders,
        SUM(amount) AS revenue,
        AVG(amount) AS avg_order
    FROM sales
    GROUP BY month
    ORDER BY month
""").df()
```

### 4.3 Top 产品类别

```python
top_categories = conn.execute("""
    SELECT
        region,
        category,
        COUNT(*) AS sales_count,
        SUM(amount) AS total_revenue,
        RANK() OVER (PARTITION BY region ORDER BY SUM(amount) DESC) AS rank
    FROM sales
    GROUP BY region, category
    QUALIFY rank <= 3
    ORDER BY region, rank
""").df()
```

`QUALIFY` 是 DuckDB 对 SQL49 的扩展，等价于对窗口函数的结果过滤。

### 4.4 性能对比

```python
import time

# DuckDB
start = time.time()
result = conn.execute("""
    SELECT region, SUM(amount) FROM sales GROUP BY region
""").fetchall()
duckdb_time = time.time() - start

# Pandas
start = time.time()
pandas_result = df.groupby("region")["amount"].sum()
pandas_time = time.time() - start

print(f"DuckDB: {duckdb_time:.3f}s | Pandas: {pandas_time:.3f}s")
```

对 10 万行分组聚合，DuckDB 通常比 Pandas 快 2-5 倍。

## 5. 进阶功能

### 5.1 窗口函数

```python
conn.execute("""
    SELECT
        order_date,
        amount,
        SUM(amount) OVER (ORDER BY order_date) AS cumulative,
        AVG(amount) OVER (ORDER BY order_date ROWS 6 PRECEDING) AS ma_7d,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) AS rank
    FROM sales
""").df()
```

窗口函数是 SQL49 中最强大的分析工具之一。

### 5.2 集合运算

```python
# UNION, EXCEPT, INTERSECT
result = conn.execute("""
    SELECT category FROM sales WHERE region = '华北'
    INTERSECT
    SELECT category FROM sales WHERE region = '华东'
""").df()
```

### 5.3 导出数据

```python
# 结果写入 CSV
conn.execute("COPY (SELECT * FROM sales WHERE amount > 1000) TO 'high_value.csv'")

# 结果写入 Parquet
conn.execute("COPY monthly_sales TO 'monthly.parquet' (FORMAT PARQUET)")
```

## 6. 与 Pandas 的选择策略

| 场景            | 推荐工具       | 原因                     |
| --------------- | -------------- | ------------------------ |
| 小数据集 (<1GB) | Pandas         | 生态丰富，语法灵活       |
| 大数据集 (>1GB) | DuckDB         | 磁盘不溢出，多线程       |
| 多表 JOIN       | DuckDB         | SQL49 JOIN 比 merge() 直观 |
| 数据清洗        | Pandas         | 字符串处理更 Pythonic    |
| 探索性分析      | DuckDB         | SQL49 即查即得             |
| 机器学习预处理  | Pandas/sklearn | 接口标准化               |
| ETL49 管道        | DuckDB         | 直接读写文件，零拷贝     |

## 7. 小结

## 7. 内存限制与OOM调试（生产必备）

### 7.1 内存限制器配置

```python
import duckdb

# ❌ 错误：未设置内存限制，OOM 风险
conn = duckdb.connect()
conn.execute("""
    SELECT * FROM read_parquet('large_data/*.parquet')
    JOIN another_large_table USING (id)
""")
# 可能导致系统内存耗尽

# ✅ 正确：设置内存上限
conn = duckdb.connect()
conn.execute("SET memory_limit='4GB'")  # 限制 4GB
conn.execute("SET temp_directory='/data/tmp'")  # 溢出到磁盘

result = conn.execute("""
    SELECT * FROM read_parquet('large_data/*.parquet')
    JOIN another_large_table USING (id)
""").fetchdf()
```

**生产环境最佳实践**:

```python
# 根据系统内存动态设置
import psutil

available_memory = psutil.virtual_memory().available
memory_limit = int(available_memory * 0.7)  # 使用 70% 可用内存

conn.execute(f"SET memory_limit='{memory_limit}B'")
conn.execute("SET preserve_insertion_order=false")  # 性能优化
```

### 7.2 OOM 调试与排查

**常见 OOM 场景**:

```python
# ❌ 场景 1：隐式物化（Materialization）
conn.execute("""
    CREATE TABLE huge_result AS
    SELECT * FROM read_parquet('10TB_data/*.parquet')
    WHERE condition = 'rare_value'
""")
# 整个结果集被物化到内存

# ✅ 正确：流式查询 + LIMIT
for batch in conn.execute("""
    SELECT * FROM read_parquet('10TB_data/*.parquet')
    WHERE condition = 'rare_value'
    LIMIT 1000000
""").fetch_df_chunk(100000):
    process_batch(batch)
```

```python
# ❌ 场景 2：笛卡尔积爆炸
conn.execute("""
    SELECT * FROM table1
    CROSS JOIN table2
    CROSS JOIN table3
""")
# 结果集 = n1 * n2 * n3

# ✅ 正确：使用 JOIN 条件
conn.execute("""
    SELECT * FROM table1 t1
    JOIN table2 t2 ON t1.id = t2.id
    JOIN table3 t3 ON t2.key = t3.key
""")
```

### 7.3 临时溢出磁盘机制

```python
# 配置溢出策略
conn.execute("SET temp_directory='/fast_ssd/duckdb_tmp'")
conn.execute("SET max_memory='8GB'")

# 超过内存限制时自动溢出
result = conn.execute("""
    SELECT customer_id, SUM(amount) as total
    FROM read_parquet('orders_100GB/*.parquet')
    GROUP BY customer_id
    ORDER BY total DESC
""").fetchdf()
```

**监控溢出行为**:

```python
# 查询执行统计
stats = conn.execute("PRAGMA database_size").fetchall()
temp_usage = conn.execute("SELECT * FROM duckdb_temporary_files()").fetchdf()
print(f"临时文件使用: {temp_usage}")
```

---

## 8. 多文件Parquet极致性能

### 8.1 直接查询 vs 传统 ETL

**反面教材（低效）**:

```python
# ❌ 错误：逐文件加载 + 拼接
import pandas as pd
from pathlib import Path

dfs = []
for file in Path('data').glob('*.parquet'):
    df = pd.read_parquet(file)  # 每次加载到内存
    dfs.append(df)

result = pd.concat(dfs)  # 内存翻倍
filtered = result[result['amount'] > 1000]
```

**性能数据**:

- 100 个文件（每个 500MB）
- 总耗时: ~45 秒
- 峰值内存: ~60GB

**正面教材（高效）**:

```python
# ✅ 正确：DuckDB 直接查询多文件
result = conn.execute("""
    SELECT * FROM read_parquet('data/*.parquet')
    WHERE amount > 1000
""").fetchdf()
```

**性能数据**:

- 相同数据
- 总耗时: ~8 秒（**5.6x 加速**）
- 峰值内存: ~4GB（**93% 节省**）

### 8.2 Parquet 谓词下推（Predicate Pushdown）

```python
# ❌ 错误：先加载全部数据再过滤
df = pd.read_parquet('large_data.parquet')
filtered = df[df['date'] >= '2024-01-01']

# ✅ 正确：谓词下推到 Parquet 读取层
result = conn.execute("""
    SELECT * FROM read_parquet('large_data.parquet')
    WHERE date >= '2024-01-01'
""").fetchdf()
```

**原理**:

- Parquet 存储列级元数据（min/max/null_count）
- DuckDB 读取元数据后跳过不符合条件的 Row Group
- 减少磁盘 I/O 和解压开销

**实测对比**:

```python
# Pandas 方式（加载全部）
# 文件: 10GB Parquet，1 亿行
# 读取时间: 25 秒
# 内存: 15GB

# DuckDB 方式（谓词下推）
# 读取时间: 3 秒（只读取匹配的 Row Groups）
# 内存: 2GB
```

### 8.3 分区裁剪（Partition Pruning）

```python
# Hive 分区结构
# data/
#   year=2023/month=01/*.parquet
#   year=2023/month=02/*.parquet
#   year=2024/month=01/*.parquet

# ❌ 错误：扫描所有分区
result = conn.execute("""
    SELECT * FROM read_parquet('data/**/*.parquet', hive_partitioning=true)
    WHERE year = 2024 AND month = 1
""").fetchdf()
# DuckDB 自动裁剪，只读取匹配分区

# ✅ 更高效：直接指定路径
result = conn.execute("""
    SELECT * FROM read_parquet('data/year=2024/month=01/*.parquet')
""").fetchdf()
```

---

## 9. 多线程与CPU打满实战

### 9.1 线程配置与性能

```python
import duckdb

# ❌ 错误：使用默认单线程
conn = duckdb.connect()
result = conn.execute("""
    SELECT category, SUM(amount)
    FROM read_parquet('large_data.parquet')
    GROUP BY category
""").fetchdf()

# ✅ 正确：配置多线程
conn = duckdb.connect()
conn.execute("SET threads=8")  # 使用 8 线程

result = conn.execute("""
    SELECT category, SUM(amount)
    FROM read_parquet('large_data.parquet')
    GROUP BY category
""").fetchdf()
```

**性能对比（12 核 CPU）**:

```python
# 单线程: 18.5 秒
# 4 线程:   5.2 秒（3.6x）
# 8 线程:   2.8 秒（6.6x）
# 12 线程:  2.1 秒（8.8x）
```

### 9.2 Python 3.13 环境下的多线程行为

```python
# Python 3.13（有 GIL）
# DuckDB 的 C++ 核心绕过 GIL
import time
import duckdb

conn = duckdb.connect()
conn.execute("SET threads=12")

start = time.time()
result = conn.execute("""
    SELECT
        category,
        COUNT(*) as cnt,
        AVG(amount) as avg_amount,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) as median
    FROM read_parquet('data/*.parquet')
    GROUP BY category
""").fetchdf()
elapsed = time.time() - start

print(f"耗时: {elapsed:.2f}s")
print(f"CPU 利用率: ~1200%（12 核全打满）")
```

**关键原理**:

- DuckDB 的查询执行引擎是 C++ 实现
- 不受 Python GIL49 限制
- 在 `execute()` 调用期间释放 GIL
- 多线程并行处理数据

### 9.3 并行查询调优

```python
# ❌ 错误：过度并行导致上下文切换
conn.execute("SET threads=64")  # 远超 CPU 核数

# ✅ 正确：线程数 = CPU 核数
import os
conn.execute(f"SET threads={os.cpu_count()}")

# ✅ 进阶：根据查询类型调优
# I/O 密集型：线程数 = 2 * CPU 核数
# CPU 密集型：线程数 = CPU 核数
```

---

## 10. 向量化执行引擎深度解析

### 10.1 什么是向量化执行？

**传统行式处理（Pandas）**:

```python
# ❌ 低效：逐行处理
total = 0
for index, row in df.iterrows():
    if row['amount'] > 1000:
        total += row['amount'] * 1.1
```

**向量化处理（DuckDB）**:

```python
# ✅ 高效：批量向量化
result = conn.execute("""
    SELECT SUM(amount * 1.1)
    FROM table
    WHERE amount > 1000
""").fetchone()[0]
```

**性能差距**:

- 行式处理: 100 万行需要 ~8 秒
- 向量化: 100 万行需要 ~0.02 秒（**400x 加速**）

### 10.2 向量化 vs 标量处理

```python
# ❌ 标量处理（循环）
result = []
for val in data:
    if val > threshold:
        result.append(val * factor)

# ✅ 向量化处理（SIMD）
result = conn.execute("""
    SELECT value * ?
    FROM table
    WHERE value > ?
""", [factor, threshold]).fetchdf()
```

**CPU 层面的差异**:

- 标量: 每次处理 1 个值
- 向量化: 每次处理 8-16 个值（SIMD 指令）
- 缓存命中率提升（连续内存访问）

### 10.3 列式存储优势

```python
# 行式存储（Pandas）
# [id, name, amount, date, ...]
# [1, 'A', 100, '2024-01-01', ...]
# 查询 SUM(amount) 需要跳过其他列

# 列式存储（DuckDB + Parquet）
# amount: [100, 200, 300, ...]
# 只读取需要的列，连续内存访问
```

**I/O 对比**:

```python
# 查询：SELECT SUM(amount) FROM table
# 表结构：10 列，每列 1GB

# Pandas（行式）: 读取 10GB（全部列）
# DuckDB（列式）: 读取 1GB（只读 amount 列）
# I/O 节省: 90%
```

---

## 11. 生产环境部署检查清单

### 11.1 性能配置

```python
# 生产环境标准配置
conn = duckdb.connect('analytics.db')

# 内存管理
conn.execute("SET memory_limit='16GB'")
conn.execute("SET temp_directory='/data/tmp'")

# 并行度
import os
conn.execute(f"SET threads={os.cpu_count()}")

# 查询优化
conn.execute("SET enable_object_cache=true")
conn.execute("SET preserve_insertion_order=false")

# 进度显示（调试用）
conn.execute("SET enable_progress_bar=true")
```

### 11.2 错误处理与重试

```python
import duckdb
from typing import Any

def safe_query(conn: duckdb.DuckDBPyConnection, sql: str, max_retries: int = 3) -> Any:
    """带重试的查询执行"""
    for attempt in range(max_retries):
        try:
            return conn.execute(sql).fetchdf()
        except duckdb.OutOfMemoryException:
            # OOM 错误：降低内存限制
            current_limit = conn.execute("SHOW memory_limit").fetchone()[0]
            new_limit = int(current_limit * 0.7)
            conn.execute(f"SET memory_limit='{new_limit}B'")
            print(f"OOM detected, reducing memory limit to {new_limit}")
        except duckdb.IOException as e:
            # I/O 错误：检查文件
            print(f"I/O error: {e}")
            raise
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Query failed (attempt {attempt + 1}): {e}")

    raise RuntimeError("Query failed after max retries")
```

### 11.3 监控与日志

```python
# 查询执行统计
result = conn.execute("""
    SELECT * FROM read_parquet('data/*.parquet')
    WHERE date >= '2024-01-01'
""")

# 获取查询计划
explain = conn.execute("""
    EXPLAIN ANALYZE
    SELECT * FROM read_parquet('data/*.parquet')
    WHERE date >= '2024-01-01'
""").fetchall()

print("查询计划:")
for line in explain:
    print(line[0])
```

---

## 12. 常见错误与调试

### 错误 1: 内存溢出（OOM）

**症状**:

```
duckdb.OutOfMemoryException: Out of Memory Error: failed to allocate data
```

**原因**:

```python
# ❌ 未设置内存限制
conn = duckdb.connect()
conn.execute("SELECT * FROM huge_table")
```

**解决方案**:

```python
# ✅ 设置内存限制 + 临时目录
conn = duckdb.connect()
conn.execute("SET memory_limit='4GB'")
conn.execute("SET temp_directory='/data/tmp'")

# ✅ 使用流式查询
for chunk in conn.execute("SELECT * FROM huge_table").fetch_df_chunk(100000):
    process(chunk)
```

### 错误 2: 文件锁定

**症状**:

```
duckdb.IOException: Could not open file: file is locked
```

**原因**:

```python
# ❌ 多个连接同时写入同一个数据库
conn1 = duckdb.connect('data.db')
conn2 = duckdb.connect('data.db')  # 锁冲突
```

**解决方案**:

```python
# ✅ 使用单一连接 + 事务
conn = duckdb.connect('data.db')
conn.execute("BEGIN TRANSACTION")
conn.execute("INSERT INTO table VALUES (...)")
conn.execute("COMMIT")

# ✅ 或使用内存数据库
conn = duckdb.connect(':memory:')
```

### 错误 3: Parquet 文件损坏

**症状**:

```
duckdb.IOException: Failed to read Parquet file: invalid metadata
```

**调试**:

```python
# ✅ 验证文件完整性
import pyarrow.parquet as pq

try:
    metadata = pq.read_metadata('file.parquet')
    print(f"行数: {metadata.num_rows}")
    print(f"列数: {metadata.num_columns}")
except Exception as e:
    print(f"文件损坏: {e}")

# ✅ 跳过损坏文件
files = ['file1.parquet', 'file2.parquet', 'file3.parquet']
valid_files = []

for file in files:
    try:
        conn.execute(f"SELECT COUNT(*) FROM read_parquet('{file}')").fetchone()
        valid_files.append(file)
    except:
        print(f"跳过损坏文件: {file}")

result = conn.execute(f"""
    SELECT * FROM read_parquet({valid_files})
""").fetchdf()
```

### 错误 4: 隐式类型转换性能

**症状**: 查询很慢

**原因**:

```python
# ❌ 类型不匹配导致全表扫描
conn.execute("""
    SELECT * FROM table
    WHERE id = '123'  -- id 是 INTEGER，'123' 是字符串
""")
```

**解决方案**:

```python
# ✅ 使用正确类型
conn.execute("""
    SELECT * FROM table
    WHERE id = 123  -- 类型匹配
""")

# ✅ 显式转换
conn.execute("""
    SELECT * FROM table
    WHERE id = CAST(? AS INTEGER)
""", ['123'])
```

### 调试技巧

**1. 查看查询计划**:

```python
plan = conn.execute("EXPLAIN SELECT ...").fetchall()
for line in plan:
    print(line[0])
```

**2. 启用性能分析**:

```python
conn.execute("SET enable_profiling=true")
result = conn.execute("SELECT ...").fetchdf()
profile = conn.execute("PRAGMA profile_output").fetchall()
print(profile)
```

**3. 监控内存使用**:

```python
import psutil
import os

process = psutil.Process(os.getpid())
before = process.memory_info().rss / 1024 / 1024

result = conn.execute("SELECT ...").fetchdf()

after = process.memory_info().rss / 1024 / 1024
print(f"内存增长: {after - before:.2f} MB")
```

---

## 13. 高阶进阶：Polars × DuckDB 零拷贝生态融合

### 13.1 为什么需要 Polars + DuckDB？

**单独使用的限制**:

| 工具       | 优势                               | 劣势                           |
| ---------- | ---------------------------------- | ------------------------------ |
| **Polars** | 极致的 DataFrame 性能（Rust 实现） | SQL49 表达能力弱                 |
| **DuckDB** | 强大的 SQL49 分析引擎                | DataFrame API 不如 Polars 灵活 |

**融合后的威力**: 利用 **Apache Arrow** 协议实现零拷贝数据传递

### 13.2 Apache Arrow 零拷贝原理

```python
# ❌ 错误：传统跨工具数据传递（内存拷贝）
import polars as pl
import duckdb

# Polars DataFrame
df_polars = pl.DataFrame({
    'id': range(10_000_000),
    'value': range(10_000_000)
})

# 转换为 Pandas（触发拷贝）
df_pandas = df_polars.to_pandas()  # 拷贝 1

# 传递给 DuckDB（再次拷贝）
conn = duckdb.connect()
conn.register('data', df_pandas)  # 拷贝 2

result = conn.execute("SELECT * FROM data WHERE value > 5000000").fetchdf()

# 总内存峰值: 原始数据 + 2 次拷贝 = 3x 内存
```

**问题**:

- 2 次内存拷贝（Polars → Pandas → DuckDB）
- 内存峰值 3x 原始数据
- 拷贝耗时 ~2-3 秒（1000 万行）

```python
# ✅ 正确：零拷贝传递（Arrow 共享内存）
import polars as pl
import duckdb

# Polars DataFrame（内部是 Arrow 格式）
df_polars = pl.DataFrame({
    'id': range(10_000_000),
    'value': range(10_000_000)
})

# 通过 Arrow Table 零拷贝
arrow_table = df_polars.to_arrow()  # 零拷贝（返回指针）

conn = duckdb.connect()
result_arrow = conn.execute("""
    SELECT * FROM arrow_table WHERE value > 5000000
""").arrow()  # 返回 Arrow Table（零拷贝）

# 转回 Polars（零拷贝）
result_polars = pl.from_arrow(result_arrow)

print(f"结果行数: {len(result_polars):,}")
# 输出: 结果行数: 4,999,999
```

**关键点**:

- ✅ `to_arrow()`: 零拷贝（返回内存指针）
- ✅ `arrow_table` 直接被 DuckDB 识别（共享内存）
- ✅ `arrow()`: DuckDB 结果返回 Arrow 格式（零拷贝）
- ✅ `from_arrow()`: Polars 接收 Arrow（零拷贝）

**性能对比**:

```python
import time

# 传统方式（拷贝）
start = time.time()
df_pandas = df_polars.to_pandas()
conn.register('data', df_pandas)
result = conn.execute("SELECT * FROM data WHERE value > 5000000").fetchdf()
time_copy = time.time() - start

# 零拷贝方式（Arrow）
start = time.time()
arrow_table = df_polars.to_arrow()
result_arrow = conn.execute("SELECT * FROM arrow_table WHERE value > 5000000").arrow()
result_polars = pl.from_arrow(result_arrow)
time_zero_copy = time.time() - start

print(f"拷贝方式: {time_copy:.2f}s")
print(f"零拷贝: {time_zero_copy:.2f}s")
print(f"加速: {time_copy / time_zero_copy:.1f}x")

# 输出示例:
# 拷贝方式: 3.45s
# 零拷贝: 0.28s
# 加速: 12.3x
```

### 13.3 实战：Polars 清洗 + DuckDB 分析

```python
import polars as pl
import duckdb

# ❌ 错误：全部用 Polars 写 SQL49 风格代码
df = pl.read_csv('sales_large.csv')

# Polars 的 SQL49 表达不如 DuckDB 直观
result = (
    df.filter(pl.col('amount') > 1000)
      .group_by('region')
      .agg([
          pl.col('amount').sum().alias('total'),
          pl.col('amount').mean().alias('avg')
      ])
      .sort('total', descending=True)
)

# ✅ 正确：Polars 清洗 + DuckDB 分析
# 第一步：Polars 清洗（利用 Rust 性能）
df_clean = (
    pl.read_csv('sales_large.csv')
      .with_columns([
          pl.col('amount').cast(pl.Float64),
          pl.col('date').str.strptime(pl.Date, '%Y-%m-%d')
      ])
      .filter(pl.col('amount') > 0)
)

# 第二步：转 Arrow 零拷贝
arrow_table = df_clean.to_arrow()

# 第三步：DuckDB SQL49 分析（利用 SQL49 表达力）
conn = duckdb.connect()
result = conn.execute("""
    SELECT
        region,
        COUNT(*) as orders,
        SUM(amount) as total,
        AVG(amount) as avg_order,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) as median,
        RANK() OVER (ORDER BY SUM(amount) DESC) as rank
    FROM arrow_table
    WHERE amount > 1000
    GROUP BY region
    ORDER BY total DESC
""").arrow()

# 第四步：转回 Polars 继续处理
result_polars = pl.from_arrow(result)
print(result_polars)
```

**优势**:

- ✅ Polars 清洗快（Rust 多线程）
- ✅ DuckDB SQL49 表达力强（窗口函数、QUALIFY）
- ✅ 零拷贝传递（Arrow 协议）

---

## 14. 小结

- **DuckDB** = 嵌入式 OLAP，纯 Python，零依赖
- **直接查询文件** = CSV/Parquet 免导入
- **Pandas 互操作** = `duckdb.sql("SELECT ... FROM df")`
- **SQL49 分析** = 窗口函数、集合运算、QUALIFY
- **性能** = 向量化多线程，2-5x Pandas
- **Polars 融合** = Apache Arrow 零拷贝，12x 加速
- **生产部署** = 内存限制、OOM 防护、多线程配置
- **缺点** = 不支持并发写入，不适合 OLTP

---

## 📝 练习题

### 练习 1: 基础查询

使用 DuckDB 直接查询 CSV 文件，完成：

- 按地区分组统计
- 计算月度趋势
- 使用窗口函数排名

### 练习 2: Polars 零拷贝

实现 Polars + DuckDB 零拷贝管道：

- Polars 清洗数据
- Arrow 零拷贝传递
- DuckDB SQL49 分析
- 转回 Polars 输出

### 练习 3: 性能优化

优化以下场景的性能：

- 100GB Parquet 文件分析
- 多表 JOIN（1 亿行 × 1000 万行）
- 内存受限环境（4GB）

---

**练习答案**: 参见 `solutions/` 目录

**下一课**: [L49 数据可视化](../L48-visualization/lesson.md)


## 🔗 下一步


[L50: Pandas 数据处理实战](../L50-pandas-complete/)
