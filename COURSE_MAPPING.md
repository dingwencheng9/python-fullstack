# Python 3.13 全栈课程 — 完整课程映射表

> **文档层级**: L1 - 核心导航
> **文档版本**: v2.3
> **受众**: 所有学习者、课程维护者
> **更新频率**: 低（课程编号变化时更新）
> **最后更新**: 2026-08-02（v2.3: 课程编号全面修正，P01 收官项目，Stage S 编号修正）

---

## 📊 课程体系总览

### 通用核心阶段（Core）- 使用 L 编号

| Stage | 名称 | 课程范围 | 课程数 | CORE | ELECTIVE | 状态 |
|-------|------|----------|--------|------|----------|------|
| Stage 0 | Python 基础 | L01-L09, P01 | 10 | L01-L09, P01 | — | ✅ 完整 |
| Stage 1 | Python 进阶 | L10-L18 | 9 | L10-L11 | L12-L18 | ✅ 完整 |
| Stage 2 | 现代工程 | L19-L27 | 9 | L19-L27 | — | ✅ 完整 |
| Stage 3 | Web 开发基础 | L26-L35 | 10 | L26-L35 | — | ✅ 完整 |
| Stage 4 | Web 开发进阶 | L36-L46 | 11 | L36-L43, L45-L46 | L44 | ✅ 完整 |
| Stage 5 | 数据工程 | L47-L53 | 7 | L47-L48, L50-L53 | L49 | ✅ 完整 |
| Stage 6 | AI Agent 开发 | L54-L65 | 12 | L54-L65 | — | ✅ 完整 |

### 垂直专精阶段（Specialization）- 独立编号

| Stage | 名称 | 课程范围 | 课程数 | CORE | ELECTIVE | 状态 |
|-------|------|----------|--------|------|----------|------|
| Stage A | AI Agent 企业级 | A01-A20 | 20 | A01-A05 | A06-A20 | 🔶 完善中（A01-A05 完整） |
| Stage S | Python 爬虫专精 | S01-S09 | 9 | S01-S09 | — | 🔶 骨架 |
| Stage K | DevOps 与平台工程 | K01-K05 | 5 | K01-K05 | — | ✅ 完整 |
| Stage M | 企业级 AI 应用 | M01-M08 | 8 | M01-M08 | — | 🔶 骨架 |
| Stage R | 前沿探索实验室 | R01-R10 | 10 | R01-R10 | — | 🔶 骨架 |

**总计**: 11 个 Stage · 118 节课程
**通用核心**: 66 节课（L01-L65）
**垂直专精**: 52 节（S:9 + K:5 + M:8 + R:10 + A:20）
**建议总学时**: ~615 小时

---

### 课程状态说明

| 状态 | 含义 | 测试要求 |
|------|------|----------|
| ✅ 完整 | 内容完整，测试覆盖 | 必须有完整测试 |
| 🔶 完善中 | 主体完成，需补充 | 建议有测试 |
| 🔶 骨架 | 占位状态，内容待实现 | 豁免测试要求 |

> ⚠️ **测试规则修订 (2026-07-19)**: 测试要求按课程类型分层。有 exercises 的课程必须有测试；只有 examples 的概念课可选；骨架课程豁免。

### 扩展知识点说明

> 📅 **新增 (2026-07-22)**: 以下课程包含**选修扩展**，作为核心内容的延伸学习。

| 课程 | 扩展内容 | 整合位置 |
|------|----------|----------|
| L27 FastAPI | GraphQL API（Strawberry） | 附录 A |
| L29 数据库工程 | MongoDB 异步驱动（Motor） | 附录 A |
| L52 RAG 向量检索 | Elasticsearch 全文搜索 | 附录 A |

---

## 🎓 Stage 0: Python 基础（L01-L09, P01）

**定位**: 零基础入门段，从变量到面向对象

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 |
|------|--------|----------|------|------|------|
| L01 | `L01-python-core` | Python 核心语法 | 6 | 6 | 5 |
| L02 | `L02-operators-control` | 运算符与控制流 | 7 | 9 | 7 |
| L03 | `L03-data-structures` | 数据结构 | 4 | 6 | 4 |
| L04 | `L04-functions-modules` | 函数与模块 | 4 | 5 | 5 |
| L05 | `L05-debugging-tools` | 调试工具与开发环境 | 2 | 2 | — |
| L06 | `L06-exceptions` | 异常处理（Exceptions） | 4 | 6 | 4 |
| L07 | `L07-oop-basics` | 面向对象基础 | 4 | 10 | 4 |
| L08 | `L08-magic-methods` | 魔术方法（Magic Methods） | 4 | 9 | 4 |
| L09 | `L09-file-operations` | 文件操作 | 4 | 5 | 7 |
| P01 | `P01-student-manager` | 学员管理系统（收官项目） | 3 | 5 | 4 |

**前置要求**: 无
**建议学时**: 50 小时

---

## 🚀 Stage 1: Python 进阶（L10-L18, P02）

**定位**: 进阶语法与工程思维，为生产代码奠基

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 轨道 |
|------|--------|----------|------|------|------|------|
| L10 | `L10-type-system` | Python 类型系统完整指南 | 4 | 6 | 6 | CORE |
| L11 | `L11-generators` | 迭代器与生成器 | 4 | 6 | 6 | CORE |
| L12 | `L12-generator-advanced` | 生成器进阶 | — | — | — | ELECTIVE |
| L13 | `L13-advanced-features` | Python 高级特性 | — | — | — | ELECTIVE |
| L14 | `L14-decorator-advanced` | 装饰器进阶 | — | — | — | ELECTIVE |
| L15 | `L15-descriptors` | 描述符与属性 | — | — | — | ELECTIVE |
| L16 | `L16-concurrency-intro` | 并发编程入门 | — | — | — | ELECTIVE |
| L17 | `L17-functional` | 函数式编程 | — | — | — | ELECTIVE |
| L18 | `L18-regex` | 正则表达式 | — | — | — | ELECTIVE |
| **P02** | `P02-data-pipeline` | 数据处理管道系统（收官项目） | 4 | 4 | 4 | CORE |

**前置要求**: Stage 0 完成
**建议学时**: 45 小时

---

## ⚙️ Stage 2: 现代工程（L19-L26, P03）

**定位**: 工程化内功与异步核心，Pytest + 工具链 + 异步

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 |
|------|--------|----------|------|------|------|
| L19 | `L19-pytest-complete` | Pytest 完整实战 — 从单元测试到 CI/CD | 6 | 9 | 4 |
| L20 | `L20-toolchain` | 现代化工具链 - 从环境到生态 | 9 | 12 | 19 |
| L21 | `L21-async-programming` | 异步核心进阶 | 6 | 8 | 4 |
| L22 | `L22-decorators` | 装饰器深度探索 | 7 | 7 | 10 |
| L23 | `L23-python-new-features` | Python 新特性与版本迁移 | 7 | 11 | 5 |
| L24 | `L24-advanced-flow-async` | 高阶流控与异步协同 | 2 | 5 | 5 |
| L25 | `L25-extreme-abstraction-performance` | 极限抽象与性能优化 | 2 | 4 | 7 |
| L26 | `L26-threading` | 线程与并发 | 3 | 5 | 3 |
| **P03** | `P03-engineering-project` | 工程化综合项目（收官项目） | 2 | 3 | 7 |

**前置要求**: Stage 1 完成
**建议学时**: 55 小时（含收官项目）

---

## 🌐 Stage 3: Web 开发基础（L27-L35, P04）

**定位**: HTTP + FastAPI + 数据库，构建 CRUD 应用

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 |
|------|--------|----------|------|------|------|
| L27 | `L27-http` | HTTP 协议与抓包基础 | 3 | 5 | 3 |
| L28 | `L28-fastapi-basics` | FastAPI 可观测性与契约驱动 | 2 | 6 | 3 |
| L29 | `L29-sql-basics` | 数据库基础与 SQL 入门 | 1 | 3 | 3 |
| L30 | `L30-database-engineering` | 异步数据持久化与事务原子性 | 2 | 5 | 4 |
| L31 | `L31-sql-advanced` | SQL 进阶 - 高级特性与性能优化 | 1 | 3 | 3 |
| L32 | `L32-docker` | Docker 容器化基础 | 2 | 4 | 3 |
| L33 | `L33-sse` | SSE 服务器推送事件 | 3 | 5 | 4 |
| L34 | `L34-websocket` | WebSocket 实时通信 | 2 | 4 | 3 |
| L35 | `L35-htmx` | HTMX + FastAPI 全栈开发 | 1 | 3 | 3 |
| **P04** | `P04-web-project` | Web 基础综合项目（收官项目） | 3 | 5 | 3 |

**前置要求**: Stage 2 完成
**建议学时**: 50 小时（含收官项目）

---

## 🔒 Stage 4: Web 开发进阶（L36-L46, P05）

**定位**: 安全、性能、微服务、分布式系统

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 轨道 |
|------|--------|----------|------|------|------|------|
| L36 | `L36-async-backpressure` | 异步背压机制 | 3 | 2 | 4 | CORE |
| L37 | `L37-web-security-complete` | Web 安全完整实践 | 3 | 5 | 3 | CORE |
| L38 | `L38-auth-authorization` | 认证与授权 | 1 | 3 | 4 | CORE |
| L39 | `L39-e2e-testing` | E2E 测试工程化 | 1 | 2 | 4 | CORE |
| L40 | `L40-message-queue` | 消息队列 | 2 | 4 | 3 | CORE |
| L41 | `L41-api-performance` | API 性能优化 | 1 | 3 | 4 | CORE |
| L42 | `L42-caching-strategy` | 缓存策略与实现 | 2 | 2 | 2 | CORE |
| L43 | `L43-async-tasks` | 异步任务处理 | 1 | 2 | 4 | CORE |
| L44 | `L44-microservices-basics` | 微服务架构基础 | 2 | 2 | 2 | ELECTIVE |
| L45 | `L45-distributed-systems` | 分布式系统实战 | 1 | 3 | 4 | CORE |
| L46 | `L46-websocket-advanced` | WebSocket 高级应用 | 1 | 3 | 4 | CORE |
| **P05** | `P05-realtime-collaboration` | 实时协作 SaaS 平台（收官项目） | 2 | — | 1 | CORE |

**前置要求**: Stage 3 完成
**建议学时**: 60 小时（含收官项目）

---

## 📊 Stage 5: 数据工程（L47-L53）

**定位**: Pandas + DuckDB + NumPy + 异步管道 + 向量检索

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 轨道 |
|------|--------|----------|------|------|------|------|
| L47 | `L47-pandas` | Pandas 完整实战 | 3 | 4 | 7 | CORE |
| L48 | `L48-visualization` | 数据可视化 | 4 | 4 | 3 | CORE |
| L49 | `L49-duckdb` | DuckDB — 嵌入式数据分析引擎 | 2 | 4 | 3 | ELECTIVE |
| L50 | `L50-pandas-complete` | Pandas 进阶数据处理技术 | 3 | 4 | 2 | CORE |
| L51 | `L51-async-data-pipeline` | 异步数据管道 | 3 | 5 | 4 | CORE |
| L52 | `L52-numpy-rag-poc` | NumPy RAG PoC - 向量检索概念验证 | 2 | 2 | 4 | CORE |
| L53 | `L53-duckdb-olap` | DuckDB OLAP 实战与性能调优 | 1 | 1 | 2 | CORE |
| **P06** | `P06-data-rag` | 数据分析与 RAG 智能报告平台（收官项目） | 2 | — | 1 | CORE |

**前置要求**: Stage 4 完成
**建议学时**: 50 小时（含收官项目）

---

## 🤖 Stage 6: AI Agent 开发（L54-L65）- CORE

**定位**: 现代 Python 全栈标配，所有 AI 应用的基础能力

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 状态 |
|------|--------|----------|------|------|------|------|
| L54 | `L54-agent-basics` | Agent 基础与工具调用 | 2 | 4 | 3 | ✅ |
| L55 | `L55-mcp-protocol` | MCP 协议入门 | 1 | 2 | 2 | ✅ |
| L56 | `L56-langchain` | 从数据到 AI — LangChain 基础与应用编排 | 2 | 3 | 3 | ✅ |
| L57 | `L57-rag-vector` | RAG 向量数据库 | 5 | 6 | 2 | ✅ |
| L58 | `L58-langgraph-adv` | LangGraph 工作流编排（基础） | 3 | 3 | 1 | ✅ |
| L59 | `L59-agent-memory` | Agent 记忆与上下文管理 | 1 | 2 | 2 | ✅ |
| L60 | `L60-agent-planning` | Agent 规划与推理 | 1 | 2 | 2 | ✅ |
| L61 | `L61-multi-agent` | 多智能体编排 (Multi-Agent Orchestration) | 1 | 4 | 6 | ✅ |
| L62 | `L62-langgraph-server` | LangGraph 高级模式与生产部署 | 1 | 2 | 2 | ✅ |
| L63 | `L63-agent-evaluation` | Agent 评估与调试 | 1 | 2 | 2 | ✅ |
| L64 | `L64-agent-deployment` | Agent 部署与监控 | 2 | 3 | 3 | ✅ |
| L65 | `L65-agent-sse-router` | Agent SSE 流式路由 | 1 | 4 | 3 | ✅ |

**前置要求**: Stage 5 完成
**建议学时**: 50 小时

---

## 🚀 Stage A: AI Agent 企业级（A01-A20）- SPECIALIZATION

**定位**: AI 工程师进阶方向，安全、合规、架构、监控、成本管理

### A01-A05: 安全与合规方向

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 状态 |
|------|--------|----------|------|------|------|------|
| A01 | `A01-agent-security` | Agent 安全与对抗防护 | 1 | 1 | 1 | 🔶 |
| A02 | `A02-agent-compliance` | Agent 合规与审计 | 1 | 1 | 1 | 🔶 |
| A03 | `A03-agent-monitoring` | Agent 全链路监控 | 1 | 1 | 1 | 🔶 |
| A04 | `A04-agent-cost` | Agent 成本控制与性能优化 | 1 | 1 | 1 | 🔶 |
| A05 | `A05-agent-project` | Agent 护栏集成实战 | 1 | 1 | 1 | 🔶 |

### A06-A10: 架构与安全方向

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 状态 |
|------|--------|----------|------|------|------|------|
| A06 | `A06-agent-arch-patterns` | Agent 架构设计模式 | 2 | 2 | 3 | 🔶 |
| A07 | `A07-agent-pentest` | Agent 安全渗透测试 | 2 | 2 | 3 | 🔶 |
| A08 | `A08-agent-guardrails` | Agent 安全护栏 | 2 | 2 | 2 | 🔶 |
| A09 | `A09-agent-privacy` | Agent 隐私保护 | 2 | 2 | 2 | 🔶 |
| A10 | `A10-agent-audit-log` | Agent 审计日志 | 2 | 2 | 2 | 🔶 |

### A11-A15: 稳定性与运维方向

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 状态 |
|------|--------|----------|------|------|------|------|
| A11 | `A11-agent-rate-limit` | Agent 限流管理 | 2 | 2 | 2 | 🔶 |
| A12 | `A12-agent-slo` | Agent SLO 监控 | 2 | 2 | 2 | 🔶 |
| A13 | `A13-agent-cost-management` | Agent Token 计费与配额系统 | 2 | 2 | 2 | 🔶 |
| A14 | `A14-agent-model-routing` | Agent 模型路由 | 2 | 2 | 2 | 🔶 |
| A15 | `A15-agent-fallback` | Agent 容错处理 | 2 | 2 | 2 | 🔶 |

### A16-A20: 性能与架构方向

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 状态 |
|------|--------|----------|------|------|------|------|
| A16 | `A16-agent-caching` | Agent 缓存策略 | 2 | 2 | 2 | 🔶 |
| A17 | `A17-agent-pipeline` | Agent 流水线 | 2 | 2 | 2 | 🔶 |
| A18 | `A18-agent-finetuning` | Agent 微调 | 2 | 2 | 2 | 🔶 |
| A19 | `A19-agent-multi-tenant` | Agent 多租户 | 2 | 2 | 2 | 🔶 |
| A20 | `A20-agent-project` | 多租户 Agent 平台终极项目 | 2 | 2 | 2 | 🔶 |

**建议**: 完成 Stage 6 后，根据职业方向选修 Stage A 课程

**前置要求**: Stage 6 (L54-L65) 完成
**建议学时**: 60 小时

---

## 🕷️ Stage S: Python 爬虫专精（S01-S09）

**定位**: 垂直领域专精课程，从前端基础到 JavaScript 逆向和 App 逆向

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 状态 |
|------|--------|----------|------|------|------|------|
| S01 | `S01-frontend-basics` | 前端基础 — HTML/CSS/DOM | 0 | 0 | 1 | 🔶 骨架 |
| S02 | `S02-xpath-beautifulsoup` | 网页数据解析 — XPath 与 BS4 | 0 | 0 | 1 | 🔶 骨架 |
| S03 | `S03-scrapy-framework` | 工业级爬虫 — Scrapy 框架 | 0 | 0 | 1 | 🔶 骨架 |
| S04 | `S04-selenium-playwright` | 自动化抓包 — Selenium 与 Playwright | 0 | 0 | 1 | 🔶 骨架 |
| S05 | `S05-js-reverse-basics` | JavaScript 逆向基础 | 0 | 0 | 1 | 🔶 骨架 |
| S06 | `S06-js-reverse-advanced` | JavaScript 逆向实战 | 0 | 0 | 1 | 🔶 骨架 |
| S07 | `S07-app-reverse-basics` | App 逆向入门 | 0 | 0 | 1 | 🔶 骨架 |
| S08 | `S08-frida-dynamic` | Frida 动态分析 | 0 | 0 | 1 | 🔶 骨架 |
| S09 | `S09-scraping-project` | 爬虫综合项目 | 0 | 0 | 1 | 🔶 骨架 |

**前置要求**: Stage 0 完成
**建议学时**: 80 小时

---

## ☸️ Stage K: DevOps 与平台工程（K01-K05）

**定位**: Agent 可观测性 + K8s + Helm + GitOps + 平台工程

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 状态 |
|------|--------|----------|------|------|------|------|
| K01 | `K01-agent-observability` | Agent 可观测性工程 | 3 | 3 | 2 | ✅ 完整 |
| K02 | `K02-kubernetes-basics` | Kubernetes 基础 | 1 | 1 | 1 | ✅ 完整 |
| K03 | `K03-kubernetes-advanced` | Kubernetes 进阶 | 1 | 1 | 1 | ✅ 完整 |
| K04 | `K04-helm-gitops` | Helm 与 GitOps | 1 | 1 | 1 | ✅ 完整 |
| K05 | `K05-platform-engineering` | 平台工程与 IDP | 1 | 1 | 1 | ✅ 完整 |

**前置要求**: Stage 6 (L54-L65) 完成
**建议学时**: 30 小时

---

## 🏢 Stage M: 企业级 AI 应用（M01-M08）

**定位**: Dify/Coze + LlamaIndex + MLOps + RAG 深度 + 商业化

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 状态 |
|------|--------|----------|------|------|------|------|
| M01 | `M01-dify-coze-workflow` | Dify/Coze 工作流编排 | 1 | 1 | 1 | ✅ 完整 |
| M02 | `M02-llamaindex-advanced` | LlamaIndex 高级 RAG | 1 | 1 | 1 | ✅ 完整 |
| M03 | `M03-mlops-experiment` | MLOps 实验追踪 | 1 | 1 | 1 | ✅ 完整 |
| M04 | `M04-litestar-framework` | Litestar 高性能框架 | 1 | 1 | 1 | ✅ 完整 |
| M05 | `M05-rag-vector-deep` | RAG 向量库深入 | 1 | 1 | 1 | ✅ 完整 |
| M06 | `M06-ai-agent-final` | AI Agent 商业大考 | 1 | 1 | 1 | ✅ 完整 |
| M07 | `M07-rag-eval-deep` | RAG 评估框架深度 | 1 | 1 | 1 | ✅ 完整 |
| M08 | `M08-ai-product-launch` | AI 产品发布与运营 | 1 | 1 | 1 | ✅ 完整 |

**前置要求**: Stage 6 (L54-L65) 完成
**建议学时**: 50 小时

---

## 🔬 Stage R: 前沿探索实验室（R01-R10）

**定位**: Python 3.14t + WASI + Wasm + AI 辅助编程 + 毕业展望

| 编号 | 目录名 | 课程标题 | 练习 | 答案 | 测试 | 状态 |
|------|--------|----------|------|------|------|------|
| R01 | `R01-python-314t-full` | Python 3.14t 完全体 | 1 | 1 | 1 | ✅ 完整 |
| R02 | `R02-gil-fallback-avoid` | GIL Free Fallback 策略 | 1 | 1 | 1 | ✅ 完整 |
| R03 | `R03-pep-649-810-lazy` | PEP 649/810 延迟注解 | 1 | 1 | 1 | ✅ 完整 |
| R04 | `R04-tstring-fstring` | t-string 与格式化新纪元 | 1 | 1 | 1 | ✅ 完整 |
| R05 | `R05-python-roadmap` | Python 路线图与未来展望 | 1 | 1 | 1 | ✅ 完整 |
| R06 | `R06-wasi-edge-deploy` | WASI 边缘部署 | 1 | 1 | 1 | ✅ 完整 |
| R07 | `R07-wasm-benchmark` | Wasm 性能基准 | 1 | 1 | 1 | ✅ 完整 |
| R08 | `R08-python-315-preview` | Python 3.15 预览 | 1 | 1 | 1 | ✅ 完整 |
| R09 | `R09-ai-coding-future` | AI 辅助编程未来 | 1 | 1 | 1 | ✅ 完整 |
| R10 | `R10-course-graduation` | 课程毕业与展望 | 1 | 1 | 1 | ✅ 完整 |

**前置要求**: Stage M (M01-M08) 完成
**建议学时**: 45 小时

---

## 🎯 学习路径建议

### 路径1: Python 全栈工程师（推荐）
```
Stage 0 → Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage A → Stage K → Stage M → Stage R
```
预计学时: 500 小时

### 路径2: AI Agent 工程师
```
Stage 0 → Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage A
```
预计学时: 340 小时

### 路径3: Python 爬虫工程师
```
Stage 0 → Stage 1 → Stage 2 → Stage 3 → Stage S → Stage K
```
预计学时: 230 小时

### 路径4: DevOps 平台工程师
```
Stage 0 → Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage K → Stage M
```
预计学时: 295 小时

### 路径5: 快速通道（有 Python 基础）
```
Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6
```
预计学时: 240 小时

---

## 📚 技术栈索引

### 通用核心阶段（L 编号）

| 技术 | 对应课程 |
|------|----------|
| Python 3.13/3.14 | L01-L27 |
| FastAPI | L27, L34, L35 |
| SQLAlchemy + PostgreSQL | L28-L30 |
| Docker | L31 |
| WebSocket / SSE | L32, L33, L46 |
| 安全 / 认证 / 授权 | L37, L38 |
| 消息队列 / 异步任务 | L40, L43 |
| 缓存 / 性能 | L41, L42 |
| 微服务 / 分布式 | L44, L45 |
| NumPy / Pandas / DuckDB | L47-L52 |
| LangChain / LangGraph | L56, L58, L62 |
| Agent / MCP | L54, L55 |
| RAG / 向量数据库 | L57, L65 |

### 垂直专精阶段（S/K/M/R/A 编号）

| 技术 | 对应课程 |
|------|----------|
| **Stage A: AI Agent 企业级** | |
| Agent 安全 / 合规 / 护栏 | A01, A02, A08 |
| Agent 监控 / 可观测性 | A03, A04 |
| Agent 成本管理 / 模型路由 | A04, A13, A14 |
| Agent 容错 / 降级 / 缓存 | A15, A16 |
| Agent 流水线 / 微调 | A17, A18 |
| **Stage S: 爬虫专精** | |
| 爬虫 / 逆向工程 | S01-S09 |
| **Stage K: DevOps 平台** | |
| Kubernetes / Helm / GitOps | K02, K03, K04 |
| Agent 可观测性 | K01 |
| 平台工程 / IDP | K05 |
| **Stage M: AI 应用** | |
| Dify / Coze / LlamaIndex | M01, M02 |
| MLOps / Litestar / RAG 深度 | M03, M04, M05, M07 |
| AI Agent 商业应用 | M06, M08 |
| **Stage R: 前沿探索** | |
| Python 3.14t / WASI / Wasm | R01, R02, R06, R07 |
| AI 辅助编程 | R09 |

---

## 📊 课程完成度统计

### 通用核心阶段（L 编号）

| Stage | 课程数 | 练习 | 答案 | 测试 | 完成度 |
|-------|--------|------|------|------|--------|
| Stage 0 | 10 | 42 | 54 | 39 | 100% |
| Stage 1 | 9 | 26 | 37 | 35 | 100% |
| Stage 2 | 9 | 45 | 65 | 60 | 100% |
| Stage 3 | 10 | 20 | 39 | 27 | 100% |
| Stage 4 | 11 | 18 | 27 | 36 | 100% |
| Stage 5 | 7 | 18 | 20 | 25 | 100% |
| Stage 6 | 12 | 19 | 30 | 29 | 100% |
| **合计** | **68** | **188** | **272** | **251** | **100%** |

### 垂直专精阶段（A/S/K/M/R 编号）

| Stage | 课程数 | 练习 | 答案 | 测试 | 完成度 |
|-------|--------|------|------|------|--------|
| Stage A | 20 | 34 | 34 | 34 | 🔶 完善中（A01-A05 完整） |
| Stage S | 9 | 0 | 0 | 9 | 🔶 骨架 |
| Stage K | 5 | 7 | 7 | 6 | ✅ 完整 |
| Stage M | 8 | 8 | 8 | 8 | 🔶 骨架 |
| Stage R | 10 | 10 | 10 | 10 | 🔶 骨架 |
| **合计** | **52** | **59** | **59** | **67** | — |

**整体完成度**:
- ✅ 完整课程: 68 (Core) + 37 (K:5 + M:8 + R:10) = 105 课
- 🔶 完善中: 21 (Stage A: 20 + Stage S: 1)
- 🔶 骨架: 0

---

## 🔗 相关文档

- [README.md](README.md) - 项目主入口
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [docs/knowledge/README.md](docs/knowledge/README.md) - 知识点文档索引
- [docs/knowledge/COURSE_KNOWLEDGE_MAP.md](docs/knowledge/COURSE_KNOWLEDGE_MAP.md) - 阶段·课程·知识点完整映射表
- [docs/knowledge/KNOWLEDGE_DAG.md](docs/knowledge/KNOWLEDGE_DAG.md) - 知识点 DAG 依赖图
- [docs/knowledge/ARCHIVED_INDEX.md](docs/knowledge/ARCHIVED_INDEX.md) - 历史审计报告归档索引
