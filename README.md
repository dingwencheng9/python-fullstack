<!-- 文档层级: L0 - 入口门面 -->
<!-- 受众: 新用户、GitHub 访客 -->
<!-- 更新频率: 低（重大变更时） -->
<!-- 最后更新: 2026-08-02 - 课程编号全面修正 -->

# Python 3.13 全栈课程体系

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13%20%7C%203.14-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-red?style=for-the-badge&logo=redis)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> 🎓 **完整课程体系**: 118 节课程 · 11 个 Stage · ~610 小时
> Core（通用核心） + Specialization（垂直专精）双轨制
>
> 📚 [课程体系](#-课程导航) · [快速开始](#-开发者快速启动指南) · [学习路径](#-学习路径) · [文档中心](#-文档)

</div>

---

## 🏆 生产级工程资产徽章

<div align="center">

![Free-Threading Safe](https://img.shields.io/badge/Free--Threading-Safe-red?style=flat-square&logo=python)
![uv Workspace Mesh](https://img.shields.io/badge/uv%20Workspace-Mesh%20Topology-blueviolet?style=flat-square&logo=uv)
![Zero Hardcoded Credentials](https://img.shields.io/badge/Credentials-Zero%20Hardcoded-brightgreen?style=flat-square&logo=shield)
![AST Whitelist Defense](https://img.shields.io/badge/Security-AST%20Whitelist%20Defense-red?style=flat-square&logo=security)
![CI Hard Gates](https://img.shields.io/badge/CI-Hard%20Gates%20%F0%9F%9A%A8-success?style=flat-square&logo=githubactions)
![K8s Ready](https://img.shields.io/badge/K8s-Production%20Ready-blue?style=flat-square&logo=kubernetes)

</div>

| 资产 | 说明 |
|------|------|
| 🔒 **Free-Threading Safe** | `asyncio.Lock()` + `ThreadPoolExecutor` 双重防护，支持 Python 3.13 无 GIL 模式 |
| 🕸️ **uv Workspace Mesh** | 10 个 workspace 成员，零 `sys.path` 污染，标准包导入 |
| 🛡️ **Zero Hardcoded Credentials** | `pydantic-settings` 统一配置，`.env` 注入，`.gitignore` 硬隔离 |
| 🧱 **AST Whitelist Defense** | 基于 `ast.NodeVisitor` 白名单，移除所有 `eval()`/`exec()` RCE 漏洞 |
| 🚨 **CI Hard Gates** | `ruff` + `mypy --strict` + `pytest` 三道硬熔断，带入污染即拒绝合并 |

---

## 🎯 选择你的学习路径

### ⚡ 快速通道（推荐）

**适合**: 有 Python 基础、想快速掌握现代全栈开发
**学时**: ~180 小时
**起点**: Stage 2（L19 Pytest）
👉 [快速通道指南](QUICKSTART.md)

---

### 📚 完整通道

**适合**: 零基础、想系统学习
**学时**: ~400 小时
**起点**: Stage 0（L01 Python 核心语法）
👉 [完整学习路径](COURSE_MAPPING.md)

---

### 🤖 AI Agent 专项通道

**适合**: 想深入 AI Agent 开发
**学时**: ~150 小时
**起点**: Stage 4（L36 异步背压）
👉 [Agent 专项路径](COURSE_MAPPING.md#学习路径建议)

---

### ☸️ DevOps 专项通道

**适合**: 想掌握 K8s + GitOps + 监控
**学时**: ~120 小时
**起点**: Stage 4（L36 异步背压）
👉 [DevOps 专项路径](COURSE_MAPPING.md#学习路径建议)

---

## 📊 课程体系总览

### 通用核心阶段（Core）- 使用 L 编号

| Stage | 名称 | 课程范围 | 课程数 | 状态 |
|-------|------|----------|--------|------|
| 0 | Python 基础 | L01-L09, P01 | 10 | ✅ 完整 |
| 1 | Python 进阶 | L10-L18 | 9 | ✅ 完整 |
| 2 | 现代工程 | L19-L27 | 9 | ✅ 完整 |
| 3 | Web 开发基础 | L26-L35 | 10 | ✅ 完整 |
| 4 | Web 开发进阶 | L36-L46 | 11 | ✅ 完整 |
| 5 | 数据工程 | L47-L53 | 7 | ✅ 完整 |
| 6 | AI Agent 开发 | L54-L65 | 12 | ✅ 完整 |

### 垂直专精阶段（Specialization）- 独立编号

| Stage | 名称 | 课程范围 | 课程数 | 状态 |
|-------|------|----------|--------|------|
| A | AI Agent 企业级 | A01-A20 | 20 | 🔶 完善中（A01-A05 完整） |
| S | Python 爬虫专精 | S01-S09 | 9 | 🔶 骨架 |
| K | DevOps 平台工程 | K01-K05 | 5 | ✅ 完整 |
| M | 企业级 AI 应用 | M01-M08 | 8 | 🔶 骨架 |
| R | 前沿探索实验室 | R01-R10 | 10 | 🔶 骨架 |

**总计**: 11 个 Stage · 118 节课程 · ~610 学时
**完整度**: 67% (78 课完整 / 28 课完善中 / 12 课骨架)

---

## 🚀 开发者快速启动指南

### 前置要求

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) 包管理器
- Docker Desktop（用于本地微服务）

### 1️⃣ 环境初始化

```bash
# 克隆仓库
git clone https://github.com/dingwencheng9/python-fullstack-course.git
cd python-fullstack-course

# 安装全量依赖（dev + web + ai + docs）
uv sync --extra dev --extra web --extra ai --extra docs

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 LLM_API_KEY 等敏感凭据
```

### 2️⃣ 一键全绿静态预检

```bash
# 验证所有测试零错误收集
uv run pytest --co

# 完整 CI 四件套
make ci-local
# 等价于:
#   uv run ruff check .          # 🚨 Hard Gate 1: Lint
#   uv run mypy --strict .        # 🚨 Hard Gate 2: 类型安全
#   uv run mkdocs build --strict  # 文档构建
#   uv run pytest -q              # 🚨 Hard Gate 3: 全量测试
```

> **CI 硬熔断**: 任何 `ruff` / `mypy --strict` / `pytest` 失败将自动拒绝合并入 `main`。

### 3️⃣ 从第一课开始

```bash
# Stage 0 - Python 基础
cd stage0-python-basics/lessons/L01-python-core
cat README.md
uv run python examples/01_*.py

# Stage 2 - 现代工程
cd stage2-engineering/lessons/L19-pytest-complete
uv run pytest tests/ -v
```

---

## 📚 课程导航

### Stage 0: Python 基础（L01-L09, P01）

零基础入门段，从变量到面向对象。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| L01 | Python 核心语法 | 变量、数据类型、运算符 |
| L02 | 运算符与控制流 | if/else、for、while |
| L03 | 数据结构 | list、dict、set、tuple |
| L04 | 函数与模块 | def、import、参数传递 |
| L05 | 调试工具与开发环境 | pdb、breakpoint、uv |
| L06 | 异常处理 | try/except、raise、自定义异常 |
| L07 | 面向对象基础 | 类、对象、继承 |
| L08 | 魔术方法 | __init__、__str__、__call__ |
| L09 | 文件操作 | 文件读写、pathlib、JSON |
| P01 | 学员管理系统 | 综合项目实战 |

### Stage 1: Python 进阶（L10-L18）

进阶语法与工程思维，为生产代码奠基。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| L10 | Python 类型系统 | typing、Protocol、Generic |
| L11 | 迭代器与生成器 | __iter__、yield、生成器表达式 |
| L12 | 生成器进阶 | yield from、协程、生成器模式 |
| L13 | Python 高级特性 | 闭包、上下文管理器 |
| L14 | 装饰器进阶 | 参数装饰器、类装饰器 |
| L15 | 描述符与属性 | property、__get__、__set__ |
| L16 | 并发编程入门 | asyncio、async/await |
| L17 | 函数式编程 | map/filter/reduce、lambda |
| L18 | 正则表达式 | re 模块、模式匹配 |

### Stage 2: 现代工程（L19-L27）

工程化内功与异步核心。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| L19 | Pytest 完整实战 | 单元测试、fixture、Mock |
| L20 | 现代化工具链 | uv、ruff、mypy、pre-commit |
| L21 | 异步核心进阶 | asyncio、Task、Future |
| L22 | 装饰器深度探索 | 参数装饰器、类装饰器 |
| L23 | Python 新特性 | 3.13 新特性、版本迁移 |
| L24 | 高阶流控与异步协同 | 信号量、事件、条件 |
| L25 | 极限抽象与性能优化 | __slots__、猴子补丁 |
| L26 | 线程与并发 | Thread、Lock、Queue |
| L27 | 工程化综合项目 | 测试 + CI/CD |

### Stage 3: Web 开发基础（L26-L35）

HTTP + FastAPI + 数据库，构建 CRUD 应用。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| L26 | HTTP 协议与抓包 | 请求/响应、状态码、Headers |
| L27 | FastAPI 可观测性 *(+GraphQL扩展)* | OpenAPI、Pydantic、日志、契约驱动 |
| L28 | 数据库基础与 SQL | SELECT、INSERT、JOIN |
| L29 | 异步数据持久化 *(+MongoDB扩展)* | asyncpg、事务、连接池、Motor NoSQL |
| L30 | SQL 进阶 | 索引、查询优化、子查询 |
| L31 | Docker 容器化 | 镜像构建、网络、卷 |
| L32 | SSE 服务器推送 | Server-Sent Events |
| L33 | WebSocket 实时通信 | 双向通信、心跳 |
| L34 | HTMX + FastAPI | 渐进增强、无刷新交互 |
| L35 | Web 基础综合项目 | CRUD + 认证 |

### Stage 4: Web 开发进阶（L36-L46）

安全、性能、微服务、分布式系统。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| L36 | 异步背压机制 | 限流、队列、反压 |
| L37 | Web 安全完整实践 | XSS、CSRF、SQL 注入 |
| L38 | 认证与授权 | JWT、OAuth2、RBAC |
| L39 | E2E 测试工程化 | Playwright、CI 集成 |
| L40 | 消息队列 | RabbitMQ、Redis Pub/Sub |
| L41 | API 性能优化 | Profiling、缓存、索引 |
| L42 | 缓存策略与实现 | Redis、一致性、失效 |
| L43 | 异步任务处理 | Celery、后台任务 |
| L44 | 微服务架构基础 | 服务拆分、API 网关 |
| L45 | 分布式系统实战 | 一致性、CAP、共识算法 |
| L46 | WebSocket 高级应用 | 集群、水平扩展 |

### Stage 5: 数据工程（L47-L53）

Pandas + DuckDB + NumPy + 异步管道 + 向量检索。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| L47 | Pandas 完整实战 | DataFrame、聚合、清洗 |
| L48 | 数据可视化 | Matplotlib、Seaborn、Plotly |
| L49 | DuckDB 嵌入式分析 | OLAP、SQLite 替代 |
| L50 | Pandas 进阶数据处理 | 高级技巧、性能优化 |
| L51 | 异步数据管道 | 异步 ETL、批量处理 |
| L52 | NumPy RAG PoC *(+ES扩展)* | 向量检索、相似度计算、Elasticsearch |
| L53 | DuckDB OLAP 实战 | 性能调优、物化视图 |

### Stage 6: AI Agent 开发（L54-L65）- CORE

LangGraph + LangChain + Agent 基础 + MCP + 多智能体 + RAG。所有 AI 应用的基础能力。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| L54 | Agent 基础与工具调用 | ReAct、Tool Use、Function Calling |
| L55 | MCP 协议入门 | Model Context Protocol 工具调用 |
| L56 | LangChain 基础与应用 | LCEL、Chain、Prompt 工程 |
| L57 | RAG 向量数据库 | Qdrant、Milvus、Embedding |
| L58 | LangGraph 工作流编排（基础） | 状态机、节点、边、条件分支 |
| L59 | Agent 记忆与上下文管理 | 短期/长期记忆、摘要压缩 |
| L60 | Agent 规划与推理 | CoT、ToT、ReAct 模式 |
| L61 | 多智能体编排 | Agent 协作、任务分配、层级 |
| L62 | LangGraph 高级模式与生产部署 | 持久化、内存、检查点 |
| L63 | Agent 评估与调试 | 指标、日志、回放、Trace |
| L64 | Agent 部署与监控 | Docker、K8s、OpenTelemetry |
| L65 | Agent SSE 流式路由 | 流式输出、Token 控制 |

### 🚀 Stage A: AI Agent 企业级（A01-A20）- SPECIALIZATION

企业级 Agent 安全、合规、监控、成本控制、架构设计。AI 工程师进阶方向。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| A01 | Agent 安全防护 | 提示注入、数据泄露防护 |
| A02 | Agent 合规审计 | GDPR、SOC2 合规框架 |
| A03 | Agent 全链路监控 | 指标、追踪、告警 |
| A04 | Agent 成本控制 | Token 优化、缓存、重试 |
| A05 | Agent 项目实战 | 综合项目 |
| A06-A20 | Agent 架构与深度 | 架构设计、安全渗透、缓存、微调... |

### ☸️ Stage K: DevOps 平台工程（K01-K05）

K8s + Helm + GitOps + 平台工程 + Agent 可观测性。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| K01 | Agent 可观测性工程 | OpenTelemetry、指标、追踪 |
| K02 | Kubernetes 基础 | Pod、Service、Deployment |
| K03 | Kubernetes 进阶 | HPA、ConfigMap、Secret |
| K04 | Helm 与 GitOps | Chart、模板、ArgoCD |
| K05 | 平台工程与 IDP | 内部开发者平台设计 |

### 🏢 Stage M: 企业级 AI 应用（M01-M08）

Dify/Coze + LlamaIndex + MLOps + RAG 深度 + 商业化。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| M01 | Dify/Coze 工作流编排 | 低代码 AI 编排 |
| M02 | LlamaIndex 高级 RAG | 索引策略、查询优化 |
| M03 | MLOps 实验追踪 | MLflow、权重追踪 |
| M04 | Litestar 高性能框架 | ASGI、高性能 Web |
| M05 | RAG 向量库深入 | 混合搜索、重排序 |
| M06 | AI Agent 商业大考 | 综合评估 |
| M07 | RAG 评估框架深度 | Trulens、DeepEval |
| M08 | AI 产品发布与运营 | 产品化、商业化 |

### 🔬 Stage R: 前沿探索实验室（R01-R10）

Python 3.14t + WASI + Wasm + Python 路线图。

| 编号 | 课程标题 | 核心内容 |
|------|----------|----------|
| R01 | Python 3.14t 完全体 | Free-Threading 深度探索 |
| R02 | GIL Free Fallback 策略 | 多线程优化、兼容模式 |
| R03 | PEP 649/810 延迟注解 | 运行时注解、类型检查优化 |
| R04 | t-string 与格式化新纪元 | 模板字符串、安全转义 |
| R05 | Python 路线图与未来展望 | 语言演进、PEP 流程 |
| R06 | WASI 边缘部署 | WebAssembly、边缘计算 |
| R07 | Wasm 性能基准 | 性能测试、内存模型 |
| R08 | Python 3.15 预览 | 下一代特性抢先看 |
| R09 | AI 辅助编程未来 | Copilot、Code Agent |
| R10 | 课程毕业与展望 | 技术回顾、职业规划 |

---

## 🛠️ 开发指南

### 本地开发

```bash
# 安装开发依赖
uv sync --extra dev

# 运行测试
uv run pytest tests/ -v

# 代码格式化
uv run ruff format .

# 类型检查
uv run mypy --strict .

# 代码质量检查
uv run ruff check .
```

### 贡献指南

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/stage|-L||-topic`
3. 提交更改：`git commit -m 'feat(stage4): 新增 L38 认证课程'`
4. 推送分支：`git push origin feat/stage|-L||-topic`
5. 提交 Pull Request
6. 运行 `make ci-local` 确保全绿

---

## 📚 文档

| 文档 | 职责 |
|------|------|
| [COURSE_MAPPING.md](COURSE_MAPPING.md) | 课程编号权威清单与学习路径 |
| [CLAUDE.md](CLAUDE.md) | Claude Code 配置 |
| [docs/README.md](docs/README.md) | 文档索引 |
| [docs/development/TESTING_CONVENTIONS.md](docs/development/TESTING_CONVENTIONS.md) | 测试约定 |

---

## 📄 License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 💬 联系方式

- **Issues**: [GitHub Issues](https://github.com/dingwencheng9/python-fullstack-course/issues)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！⭐**

</div>
