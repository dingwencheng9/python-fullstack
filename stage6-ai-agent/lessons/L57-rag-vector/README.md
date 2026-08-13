# L57: RAG 向量数据库

> **课程编号**: L57
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 4-5 小时  
> **难度**: ⭐⭐⭐⭐☆ (中高级)

**课程目标**: 掌握向量数据库与 RAG 系统的生产级部署

---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ 理解向量数据库架构与索引原理
2. ✅ 使用 Qdrant、Chroma、Milvus 等向量数据库
3. ✅ 实现高效的向量检索和相似度搜索
4. ✅ 构建生产级 RAG 系统
5. ✅ 优化检索性能和查询效率
6. ✅ 实现向量数据库的持久化和扩展

---

## 📚 课程内容

### 第一部分：向量数据库基础

#### 1.1 什么是向量数据库？

**向量数据库** 专门用于存储和检索高维向量数据：

```
文本 → Embedding 模型 → 向量 → 向量数据库 → 相似度检索
```

**核心特性**:

- ✅ 高维向量存储（768, 1536, 4096 维）
- ✅ 快速相似度搜索（ANN - 近似最近邻）
- ✅ 元数据过滤
- ✅ 分布式扩展

#### 1.2 向量相似度

_(详细代码见 lesson.md)_

---

### 第二部分：Qdrant

#### 2.1 安装和配置

_(详细代码见 lesson.md)_

#### 2.2 基础操作

_(详细代码见 lesson.md)_

#### 2.3 过滤搜索

_(详细代码见 lesson.md)_

---

### 第三部分：Chroma

#### 3.1 基础使用

_(详细代码见 lesson.md)_

#### 3.2 LangChain 集成

_(详细代码见 lesson.md)_

---

### 第四部分：生产级 RAG 系统

#### 4.1 完整 RAG 架构

_(详细代码见 lesson.md)_

#### 4.2 批量索引

_(详细代码见 lesson.md)_

---

### 第五部分：性能优化

#### 5.1 索引优化

_(详细代码见 lesson.md)_

#### 5.2 缓存策略

_(详细代码见 lesson.md)_

---

## 🛠️ 前置要求

### 必备知识

- Python 基础
- 向量和嵌入概念
- RAG 架构理解

### 环境要求

_(详细代码见 lesson.md)_

### 安装依赖

```bash
uv add qdrant-client chromadb langchain langchain-openai
```

---

## 🚀 快速开始

### 1. 启动 Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 2. 创建向量存储

_(详细代码见 lesson.md)_

### 3. 添加和搜索

_(详细代码见 lesson.md)_

---

## 📝 练习

### 练习 1: 向量数据库操作

使用 Qdrant 进行 CRUD 操作

### 练习 2: RAG 系统

构建完整的 RAG 问答系统

### 练习 3: 性能优化

优化检索性能和索引速度

### 练习 4: 生产部署

部署可扩展的 RAG 服务

---

## 🧪 测试

_(详细代码见 lesson.md)_

---

## 📖 参考资料

- [Qdrant 文档](https://qdrant.tech/documentation/)
- [Chroma 文档](https://docs.trychroma.com/)
- [向量数据库对比](https://github.com/erikbern/ann-benchmarks)

---

## 📁 文件导航

| 目录       | 说明     |
| ---------- | -------- |
| examples/  | 示例代码 |
| exercises/ | 练习题   |
| solutions/ | 参考答案 |
| tests/     | 单元测试 |

---

## ✅ 完成标准

- [ ] 完成所有练习题
- [ ] 通过全部测试：`pytest tests/ -v`

## 🔗 下一步

完成本课后继续学习：

- [L58: LangGraph 工作流编排](../L58-langgraph-adv/README.md)
- L58 会学习 LangGraph，通过图结构编排复杂的多步骤 Agent 工作流。
