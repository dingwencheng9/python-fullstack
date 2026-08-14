# L49: DuckDB — 嵌入式数据分析引擎

> **课程编号**: L49  
> **所属阶段**: Stage 5 - 数据工程  
> **预计时长**: 6 小时  
> **难度**: ⭐⭐⭐ (中级)

---

DuckDB 是一个**嵌入式 OLAP 数据库**：零依赖、纯 Python、直接查询 CSV/Parquet，不需要服务进程。
是 Pandas 的"分析引擎"替代方案，单文件即可，速度快 5-10 倍。

---

## 🎯 学习目标

1. ✅ 理解 DuckDB 与 Pandas / SQLite / PostgreSQL 的适用场景区别
2. ✅ 使用 DuckDB 直接查询 CSV/Parquet 文件（零导入）
3. ✅ 实现 DuckDB + Pandas 混合分析工作流
4. ✅ 使用 SQL 窗口函数进行高级分析（rolling、ranking、percentile）
5. ✅ 理解 DuckDB 在百万行数据上的性能优势
6. ✅ 掌握 DuckDB 与 Parquet 的列式存储协同

---

## 📋 前置知识

- [L47: Pandas 完整实战](../L47-pandas/) — 知道如何清洗与聚合 DataFrame
- [L48: 数据可视化](../L48-visualization/) — 知道分析结果如何服务图表表达
- 基础 SQL（SELECT/JOIN/GROUP BY/WINDOW）

---

## 📁 文件导航

| 目录                           | 说明                                           |
| ------------------------------ | ---------------------------------------------- |
| `examples/01_basic_queries.py` | DuckDB 入门：连接、查询、Pandas 互操作         |
| `examples/02_sales_analysis.py`  | 销售分析、聚合与窗口函数                      |
| `exercises/`                   | 2 个递进练习（窗口函数 → Pandas/DuckDB 混合） |
| `solutions/`                   | 参考答案                                       |
| `tests/`                       | 单元测试（覆盖率 ≥ 80%）                       |

---

## 🚀 快速开始

```bash
# 安装（已在 pyproject extra=ai 中）
uv sync --extra ai

# 跑示例
uv run python stage5-data-engineering/lesso../L49-duckdb/examples/01_basic_queries.py

# 跑测试
PYTHONPATH=. uv run pytest stage5-data-engineering/lesso../L49-duckdb/tests/ --no-cov -v
```

---

## 📚 核心概念

| 概念              | 说明                                             |
| ----------------- | ------------------------------------------------ |
| **DuckDB**        | 嵌入式 OLAP 引擎，单文件持久化或纯内存           |
| **零依赖**        | `uv add duckdb` 即可，无需服务进程          |
| **直接查询**      | `duckdb.sql("SELECT * FROM 'data.csv'")`，免导入 |
| **Pandas 互操作** | `duckdb.sql("SELECT ... FROM df").df()`          |
| **列式存储**      | Parquet 友好，分析查询比 SQLite 快 5-10x         |
| **向量化执行**    | 多线程并行，单机能跑亿级数据                     |

---

## 🔍 何时用 DuckDB vs Pandas vs PostgreSQL？

| 场景                             | 选择                    |
| -------------------------------- | ----------------------- |
| 内存够、单次分析 < 100 万行      | **Pandas**              |
| 内存吃紧、要扫 GB 级 CSV/Parquet | **DuckDB**              |
| 需要多人共享、事务、长期持久化   | **PostgreSQL**          |
| 嵌入到桌面应用、零运维           | **DuckDB**              |
| 需要复杂 SQL（窗口、CTE）        | **DuckDB / PostgreSQL** |

---

## 🚨 常见陷阱

| 陷阱                  | 表现                                | 解决                                                  |
| --------------------- | ----------------------------------- | ----------------------------------------------------- |
| 大表 ORDER BY 卡      | 100 万行排序慢                      | 加 `LIMIT` 或先 `WHERE` 过滤                          |
| Pandas DataFrame 转换 | `duckdb.sql(... FROM df)` 找不到 df | 必须先 `con.register("df", df)` 或用 `duckdb.from_df` |
| 时区混乱              | 时间列时而 UTC 时而本地             | `CAST(col AS TIMESTAMP WITH TIME ZONE)`               |
| Parquet 分区扫错      | 直接读整个目录变慢                  | 用 `PARTITION BY` 提示                                |

---

## ✅ 完成标准

- [ ] 能用 DuckDB 直接查询 CSV/Parquet 文件，不预先导入
- [ ] 掌握 DuckDB + Pandas 混合工作流
- [ ] 写过至少一个含窗口函数的 SQL（如 `ROW_NUMBER() OVER (PARTITION BY ...)`）
- [ ] 能解释 DuckDB 比 SQLite 在分析场景快的原因（列式 + 向量化）
- [ ] 通过全部 pytest 测试

---

## 💼 接单价值

DuckDB 是数据分析报告类外包的"提速利器"：

- 客户给 5GB CSV，不用建 PG，直接 DuckDB SQL49 查询
- 出报告时 SQL49 比 Pandas 链式调用更易读、易交付
- 详见 [`extensions/freelance-toolkit/playbooks/crawler-playbook.md`](../../../extensions/freelance-toolkit/playbooks/crawler-playbook.md) "数据分析报告"章节

---

## 🔗 下一步

完成本课后继续学习：

- [L50: Pandas 高级操作与性能优化](../L50-pandas-complete/README.md)

> 📖 **学习路径提示**：L50 将深入学习 Pandas 高级用法和性能优化。
