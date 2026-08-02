# Stage M: 企业级 AI 应用

> **阶段编号**: Stage M
> **课程数量**: 8 课 (M01-M08)
> **预计学时**: ~50 小时
> **前置要求**: Stage K (DevOps 与平台工程)

---

## 📚 课程列表

| 编号 | 课程名称 | 主题 | 学时 | 难度 |
|------|----------|------|------|------|
| M01 | Dify/Coze 工作流编排 | 可视化编排、节点配置、API 集成 | 6h | ⭐⭐⭐⭐ |
| M02 | LlamaIndex 高级 RAG | 索引策略、查询优化、混合检索 | 6h | ⭐⭐⭐⭐ |
| M03 | MLOps 实验追踪 | MLflow、实验管理、模型版本 | 5h | ⭐⭐⭐ |
| M04 | Litestar 框架 | 高性能 ASGI、路由优化、中间件 | 5h | ⭐⭐⭐⭐ |
| M05 | RAG 向量库深入 | 向量索引、相似度搜索、召回优化 | 6h | ⭐⭐⭐⭐ |
| M06 | AI Agent 最终项目 | 商业模式、定价策略、客户案例 | 4h | ⭐⭐⭐ |
| M07 | RAG 评估深度 | 评估指标、A/B 测试、效果优化 | 5h | ⭐⭐⭐⭐ |
| M08 | AI 产品发布与运营 | 产品发布、用户增长、数据驱动 | 5h | ⭐⭐⭐ |

---

## 🎯 学习路径

```
M01 工作流编排 → M02 高级 RAG
        ↓              ↓
M03 MLOps ← M04 Litestar → M05 向量库深入
                    ↓              ↓
            M06 商业大考 → M07 评估框架
                              ↓
                         M08 产品发布
```

---

## 📖 学习目标

完成 Stage M 后，你将掌握：

1. **工作流编排** — Dify/Coze 可视化编排、API 集成、自动化流程
2. **高级 RAG** — 索引策略、查询优化、混合检索、召回排序
3. **MLOps 实践** — 实验追踪、模型版本、参数管理
4. **高性能框架** — Litestar 框架、路由优化、中间件设计
5. **向量数据库** — 向量索引、相似度搜索、召回优化
6. **商业化能力** — 商业模式设计、定价策略、客户案例分析
7. **评估优化** — RAG 评估指标、A/B 测试、效果持续优化
8. **产品运营** — 产品发布、用户增长、数据驱动决策

---

## 🛠️ 环境要求

- **Python 版本**: 3.13.x
- **包管理**: uv
- **核心依赖**: llama-index, litestar, httpx, chromadb
- **可选依赖**: react, vue (前端项目)

```bash
# 安装依赖
uv sync

# 运行测试（全阶段）
uv run pytest stageM-enterprise/lessons/ -v

# 代码检查
uv run ruff check stageM-enterprise/
uv run mypy stageM-enterprise/lessons/ --ignore-missing-imports
```

---

## 📁 课程结构

每个课程包含：

```
M{XX}-课程名/
├── README.md           # 课程概览与快速开始
├── lesson.md           # 详细教学内容
├── examples/           # 示例代码（可直接运行）
├── exercises/          # 练习题模板
├── solutions/          # 参考解答
└── tests/              # 单元测试
```

---

## 🔗 衔接课程

- **前置**: [Stage K: DevOps 与平台工程](../stageK-devops/)
- **后续**: [Stage R: 前沿探索实验室](../stageR-frontier/)

---

## 📊 统计数据

| 指标 | 数值 |
|------|------|
| 课程数量 | 8 |
| 示例代码 | ~60 个 |
| 练习题 | ~30 个 |
| 测试用例 | 400+ |
| 预计学时 | ~50 小时 |

---

## 🏆 完成标准

- [ ] 完成所有 8 个课程的学习
- [ ] 通过所有课程测试
- [ ] 完成所有练习题
- [ ] 能够交付商业级 AI 应用
- [ ] 掌握 RAG 评估与优化方法
- [ ] 理解 AI 商业化路径

---

## ⚡ 快速参考

### LlamaIndex RAG 流程

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader

# 加载文档
documents = SimpleDirectoryReader("./data").load_data()

# 构建索引
index = VectorStoreIndex.from_documents(documents)

# 查询
query_engine = index.as_query_engine()
response = query_engine.query("用户问题")
```

### Litestar 路由

```python
from litestar import Litestar, get

@get("/api/agent/invoke")
async def invoke_agent(data: AgentRequest) -> AgentResponse:
    # Agent 调用逻辑
    pass

app = Litestar(route_handlers=[invoke_agent])
```

---

> **版本**: v5.0
> **最后更新**: 2026-07-22
