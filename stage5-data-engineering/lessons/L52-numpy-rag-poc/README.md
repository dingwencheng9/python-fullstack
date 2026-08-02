# L52: NumPy RAG PoC - 向量检索概念验证

> **课程编号**: L52
> **课程时长**: 2-3 小时
> **难度**: ⭐⭐⭐☆☆（中等）
> **前置课程**: L47 NumPy 科学计算, L50 Pandas 数据处理
> **状态**: ✅ 完整

## 📚 课程简介

本课程从零实现基于 NumPy 的向量检索系统，深入理解 RAG 的核心机制。

### 核心知识点

- 向量检索原理（余弦相似度、欧氏距离）
- 近似最近邻（ANN）算法原理
- HNSW/NSW 图索引基础
- 性能优化与批量处理

### 学习目标

- ✅ 理解向量检索的核心原理
- ✅ 实现纯 NumPy 向量相似度计算
- ✅ 了解 ANN 算法（NSW、IVF）原理
- ✅ 掌握性能优化技巧

## 📁 目录结构

| 目录 | 说明 |
|------|------|
| `examples/` | 示例代码 |
| `exercises/` | 练习题 |
| `solutions/` | 参考答案 |

## 🚀 快速开始

```bash
cd stage5-data-engineering/lessons/L52-numpy-rag-poc

# 运行示例
python examples/01_vector_basics.py

# 完成练习
python exercises/01_cosine_similarity.py
```

## ✅ 完成标准

- [ ] 完成所有练习题
- [ ] 理解向量检索原理
- [ ] 能够实现基本的相似度计算
- [ ] 了解 ANN 算法原理

## 🔗 下一步

- [L53: DuckDB OLAP 实战](../L53-duckdb-olap/) - 大规模数据分析
- [L65: RAG 向量数据库](../../../stage6-ai-agent/lessons/L57-rag-vector/) - 完整 RAG 系统
