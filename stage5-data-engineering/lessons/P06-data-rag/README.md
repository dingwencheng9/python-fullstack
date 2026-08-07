# P06: 数据分析与 RAG 智能报告平台

> **课程编号**: P06
> **所属阶段**: Stage 5 - 数据工程
> **预计时长**: 6-10 小时
> **难度**: ⭐⭐⭐⭐⭐（专家级）
> **前置课程**: L47-L53（全部 Stage 5 课程）
> **版本**: v1.0
> **核心版本**: Python 3.13

---

## 🚀 快速开始

```bash
# 从仓库根目录进入本课
cd stage5-data-engineering/lessons/P06-data-rag

# 安装依赖
uv sync

# 运行示例
uv run python examples/01_project_overview.py

# 运行练习
uv run python exercises/exercise_01_data_pipeline.py

# 运行测试
uv run pytest tests/ -q
```

## 📚 学习路径

1. 阅读 [`lesson.md`](lesson.md)，理解项目架构和整合知识点。
2. 运行 `examples/*.py`，观察各模块实现。
3. 完成 [`exercises/`](exercises/) 目录下的练习。
4. 对照 [`solutions/`](solutions/) 优化实现。
5. 运行 `uv run pytest tests/ -q` 验证理解。

## 📁 目录结构

| 路径 | 用途 |
|------|------|
| [`examples/`](examples/) | 示例代码：数据管道、ETL、可视化、RAG |
| [`exercises/`](exercises/) | 练习题 |
| [`solutions/`](solutions/) | 参考答案 |
| [`tests/`](tests/) | 单元测试 |
| [`lesson.md`](lesson.md) | 完整课程文档 |

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解项目整体架构。
- [ ] 运行全部示例，理解各模块实现。
- [ ] 完成数据管道 + ETL 练习。
- [ ] 完成 RAG 向量检索练习。
- [ ] 完成数据可视化练习。
- [ ] 通过 `uv run pytest tests/ -q`。

---

## 🔗 前置课程回顾

| 课程 | 核心知识 | 本项目应用 |
|------|----------|-------------|
| L47 | Pandas 向量化 | 数据加载与清洗 |
| L48 | 数据可视化 | Matplotlib 图表 |
| L49 | DuckDB | OLAP 查询 |
| L50 | Pandas 进阶 | 复杂数据处理 |
| L51 | 异步数据管道 | ETL 流程 |
| L52 | NumPy RAG | 向量检索 |
| L53 | DuckDB OLAP | 查询优化 |

## 🎯 项目概述

**DataRag** - 数据分析与 RAG 智能报告平台

- 📊 数据加载与清洗 (Pandas)
- 📈 数据可视化报告 (Matplotlib)
- 🗄️ OLAP 查询引擎 (DuckDB)
- 🔄 异步 ETL 管道 (asyncio)
- 🔍 RAG 智能问答 (NumPy)
