# Stage 5: 数据工程

> **阶段编号**: Stage 5
> **课程数量**: 7 课 (L47-L53)
> **预计学时**: ~40 小时
> **前置要求**: Stage 4（Web 开发进阶）

---

## 📚 课程列表

| 编号 | 课程名称 | 学时 | 难度 |
|------|----------|------|------|
| L47 | [Pandas 完整实战](lessons/L47-pandas/) | 4-5h | ⭐⭐⭐ |
| L48 | [数据可视化](lessons/L48-visualization/) | 4-5h | ⭐⭐⭐ |
| L49 | [DuckDB 基础](lessons/L49-duckdb/) | 5-6h | ⭐⭐⭐⭐ |
| L50 | [Pandas 高级特性](lessons/L50-pandas-complete/) | 6-8h | ⭐⭐⭐⭐ |
| L51 | [异步数据管道](lessons/L51-async-data-pipeline/) | 5-6h | ⭐⭐⭐⭐ |
| L52 | [NumPy RAG PoC](lessons/L52-numpy-rag-poc/) | 4-5h | ⭐⭐⭐⭐ |
| L53 | [DuckDB OLAP 综合实战](lessons/L53-duckdb-olap/) | 4-5h | ⭐⭐⭐⭐ |

---

## 🎯 学习路径

```
L47 Pandas 基础 → L48 可视化 → L49 DuckDB
        ↓               ↓              ↓
L50 Pandas 进阶 ← L52 异步管道 → L53 OLAP 综合
```

---

## 📖 学习目标

完成 Stage 5 后，你将掌握：

1. **Pandas 高级特性** — 数据清洗、合并、重塑、向量化操作、内存优化
2. **数据可视化** — Matplotlib、Seaborn、交互式图表、仪表盘设计
3. **DuckDB 基础** — 嵌入式 OLAP、SQL 扩展、窗口函数、Pandas 互操作
4. **NumPy RAG PoC** — ndarray、广播机制、矩阵运算、线性代数
5. **异步数据管道** — 生产级 ETL、背压控制、错误恢复、监控告警
6. **性能优化** — 向量化、内存管理、查询优化、并行计算
7. **数据质量** — 数据验证、异常检测、清洗策略、数据治理

---

## 🛠️ 环境要求

- **Python 版本**: 3.13.x
- **包管理**: uv
- **核心依赖**: pandas, numpy, duckdb, matplotlib, seaborn
- **可选依赖**: pyarrow, polars (性能对比)

```bash
# 安装依赖
uv sync

# 运行测试（全阶段）
uv run pytest stage5-data-engineering/lessons/ -v

# 运行单个课程测试
uv run pytest stage5-data-engineering/lessons/L50-pandas-complete/tests/ -v

# 代码检查
uv run ruff check stage5-data-engineering/
uv run mypy stage5-data-engineering/lessons/ --ignore-missing-imports
```

---

## 📁 课程结构

每个课程包含：

```
L{XX}-课程名/
├── README.md           # 课程概览与快速开始
├── lesson.md           # 详细教学内容
├── examples/           # 示例代码（可直接运行）
├── exercises/          # 练习题模板
├── solutions/          # 参考解答
└── tests/              # 单元测试
```

---

## 🔗 衔接课程

- **前置**: [Stage 4: Web 开发进阶](../stage4-web-advanced/)
- **后续**: [Stage 6: AI Agent 开发](../stage6-ai-agent/)

---

## 📊 统计数据

| 指标 | 数值 |
|------|------|
| 课程数量 | 7 |
| 示例代码 | ~80 个 |
| 练习题 | ~35 个 |
| 测试用例 | 500+ |
| 预计学时 | ~40 小时 |

---

## 🏆 完成标准

- [ ] 完成所有 7 个课程的学习
- [ ] 通过所有课程测试
- [ ] 完成所有练习题
- [ ] 能够构建生产级数据处理管道
- [ ] 掌握 DuckDB OLAP 分析技能
- [ ] 理解异步数据处理架构

---

## ⚡ 快速参考

### Pandas 常用操作

```python
import pandas as pd

# 读取数据
df = pd.read_csv("data.csv")

# 数据清洗
df = df.dropna()
df = df[df["age"] > 0]

# 分组聚合
result = df.groupby("category")["value"].agg(["mean", "sum", "count"])

# 导出结果
result.to_csv("result.csv")
```

### DuckDB 查询

```python
import duckdb

con = duckdb.connect("analytics.db")

# SQL 查询
result = con.execute("""
    SELECT category, SUM(revenue) as total
    FROM sales
    GROUP BY category
    ORDER BY total DESC
""").fetchdf()

# Pandas 互操作
df = con.execute("SELECT * FROM sales LIMIT 1000").df()
```

---

> **版本**: v4.1
> **最后更新**: 2026-07-18
