# Python 3.13 全栈课程 — 阶段·课程·知识点完整映射表

> **文档版本**: v3.0
> **创建日期**: 2026-07-21
> **最后更新**: 2026-08-02（v3.0: Stage 0-2 课程编号全面修正）
> **范围**: Stage 0-6 + Stage A/P/K/M/R

---

## 📊 课程体系总览

### 体系架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    Python 3.13 全栈课程体系                          │
├─────────────────────────────────────────────────────────────────┤
│  通用核心阶段（Core）            │  垂直专精阶段（Specialization）    │
│  ─────────────────────          │  ─────────────────────          │
│  Stage 0-6 (L01-L65)         │  Stage A/P/K/M/R              │
│  ~585 小时                     │  ~280 小时                      │
└─────────────────────────────────────────────────────────────────┘
```

### 阶段完成度一览

| 阶段 | 名称 | 课程数 | 状态 | 完成度 |
|------|------|--------|------|--------|
| Stage 0 | Python 基础 | 10 (L01-L09, P01) | ✅ 完整 | 100% |
| Stage 1 | Python 进阶 | 7 | ✅ 完整 | 100% |
| Stage 2 | 现代工程 | 9 | ✅ 完整 | 100% |
| Stage 3 | Web 开发基础 | 10 | ✅ 完整 | 100% |
| Stage 4 | Web 开发进阶 | 11 | ✅ 完整 | 100% |
| Stage 5 | 数据工程 | 7 | ✅ 完整 | 100% |
| Stage 6 | AI Agent 开发 | 12 | ✅ 完整 | 100% |
| Stage A | AI Agent 企业级 | 20 | 🔶 完善中 | 25% |
| Stage P | Python 爬虫专精 | 9 | 🔶 骨架 | 0% |
| Stage K | DevOps 平台工程 | 5 | ✅ 完整 | 100% |
| Stage M | 企业级 AI 应用 | 8 | 🔶 骨架 | 0% |
| Stage R | 前沿探索实验室 | 10 | 🔶 骨架 | 0% |

**总计**: 11 个 Stage · 117 课程 · ~610 学时

---

## Stage 0: Python 基础（L01-L09, P01）

**能力等级**: S0 → S1  
**建议学时**: 40 小时  
**前置要求**: 无

### 课程与知识点

| 课程 | 标题 | 知识点数 | 核心知识点 |
|------|------|----------|------------|
| L01 | Python 核心语法 | 9 | 变量、数据类型、REPL、f-string、类型转换 |
| L02 | 运算符与控制流 | 10 | 算术/比较/逻辑运算符、if/elif/else、for/while、break/continue、match-case |
| L03 | 数据结构 | 9 | list、dict、set、列表推导式、collections |
| L04 | 函数与模块 | 7 | def、参数传递、作用域、import、lambda、__init__.py |
| L05 | 调试工具与开发环境 | 6 | pdb、breakpoint、traceback、IDE 调试、uv 工具链 |
| L06 | 文件操作 | 8 | 文件读写、pathlib、JSON、with 上下文、基础 OOP |
| L07 | 面向对象基础 | 8 | 类、对象、继承、super()、@property、类变量 vs 实例变量、MRO |
| L08 | 魔术方法 | 10 | __init__、__str__、__repr__、__iter__、__next__、__enter__、__exit__、__call__、描述符协议 |
| L09 | 异常处理 | 8 | try/except、raise、自定义异常、else/finally、异常链、traceback |
| P01 | 学员管理系统 | 6 | 综合实战：文件操作、OOP、异常处理、命令行参数、项目结构 |

**阶段知识点总数**: ~81 个

---

## Stage 1: Python 进阶（L10-L18）

**能力等级**: S1 → S2  
**建议学时**: 35 小时  
**前置要求**: Stage 0 完成

### 课程与知识点

| 课程 | 标题 | 知识点数 | 核心知识点 |
|------|------|----------|------------|
| L10 | Python 类型系统 | 8 | Protocol、Union/Optional、泛型、TypeVar、TypedDict |
| L11 | 迭代器与生成器 | 8 | `__iter__`/`__next__`、yield、生成器表达式、itertools |
| L12 | 生成器进阶 | 4 | yield from、send()、异步生成器、生成器管道模式 |
| L13 | Python 高级特性 | 7 | 闭包、上下文管理器、@contextmanager、suppress、ExitStack |
| L14 | 装饰器进阶 | 5 | 带参装饰器、装饰器工厂、装饰器链、类装饰器 |
| L15 | 描述符与属性 | 7 | __get__/__set__/__delete__、property、数据描述符、验证描述符 |
| L16 | 并发编程入门 | 7 | async/await、EventLoop、Task、gather、异步上下文管理器 |
| L17 | 函数式编程 | 8 | map/filter/reduce、functools、partial、缓存 |
| L18 | 正则表达式 | 8 | re 模块、模式匹配、贪婪/非贪婪、分组、编译 |

**阶段知识点总数**: ~66 个

---

## Stage 2: 现代工程（L19-L27）

**能力等级**: S2 → S3  
**建议学时**: 50 小时  
**前置要求**: Stage 1 完成

### 课程与知识点

| 课程 | 标题 | 知识点数 | 核心知识点 |
|------|------|----------|------------|
| L19 | Pytest 完整实战 | 8 | fixture、Mock、parametrize、conftest、覆盖率 |
| L20 | 现代化工具链 | 6 | uv、ruff、mypy、pre-commit、CI 配置 |
| L21 | 异步编程核心 | 10 | asyncio.run()、TaskGroup、gather、shield、取消 |
| L22 | 装饰器深度探索 | 9 | 参数装饰器、类装饰器、functools.wraps、装饰器工厂 |
| L23 | Python 新特性 | 6 | PEP 695、match-case、异常组、类型参数 |
| L24 | 高阶流控与异步协同 | 6 | Semaphore、Event、Condition、Barrie |
| L25 | 极限抽象与性能优化 | 6 | `__slots__`、猴子补丁、元类、abc |
| L26 | 线程与并发 | 7 | Thread、Lock、RLock、Queue、线程池 |
| L27 | 工程化综合项目 | 5 | TDD 实战、CI/CD 集成、生产级代码规范 |

**阶段知识点总数**: ~63 个

---

## Stage 3: Web 开发基础（L26-L35）

**能力等级**: S3 → S4  
**建议学时**: 45 小时  
**前置要求**: Stage 2 完成

### 课程与知识点

| 课程 | 标题 | 知识点数 | 核心知识点 |
|------|------|----------|------------|
| L26 | HTTP 协议与抓包 | 6 | GET/POST、状态码、Headers、Session、httpx |
| L27 | FastAPI 可观测性 | 7 | @app.get、请求/响应模型、Pydantic、日志、OpenAPI |
| L28 | 数据库基础与 SQL | 8 | SELECT、INSERT、JOIN、GROUP BY、子查询 |
| L29 | 异步数据持久化 | 7 | asyncpg、事务、连接池、SQLAlchemy 2.0 |
| L30 | SQL 进阶 | 6 | 索引、查询优化、EXPLAIN、视图、触发器 |
| L31 | Docker 容器化 | 6 | Dockerfile、镜像构建、网络、卷、docker-compose |
| L32 | SSE 服务器推送 | 5 | Server-Sent Events、流式响应、EventSource |
| L33 | WebSocket 实时通信 | 6 | 双向通信、心跳、消息广播、pytest-asyncio |
| L34 | HTMX + FastAPI | 5 | 渐进增强、无刷新交互、HTMX 模板 |
| L35 | Web 基础综合项目 | 6 | CRUD + 认证实战、Docker Compose 部署 |

**阶段知识点总数**: ~68 个

---

## Stage 4: Web 开发进阶（L36-L46）

**能力等级**: S4 → S5  
**建议学时**: 50 小时  
**前置要求**: Stage 3 完成

### 课程与知识点

| 课程 | 标题 | 知识点数 | 核心知识点 |
|------|------|----------|------------|
| L36 | 异步背压机制 | 6 | Semaphore、限流、队列、熔断、Rate Limiter |
| L37 | Web 安全完整实践 | 8 | XSS、CSRF、SQL 注入、SQLAlchemy 参数化 |
| L38 | 认证与授权 | 7 | JWT、OAuth2、RBAC、JWT 签名验证 |
| L39 | E2E 测试工程化 | 6 | Playwright、CI 集成、屏幕截图、可访问性 |
| L40 | 消息队列 | 7 | RabbitMQ、Redis Pub/Sub、发布/订阅模式 |
| L41 | API 性能优化 | 6 | Profiling、CProfile、热点分析、连接复用 |
| L42 | 缓存策略 | 7 | Redis、TTL、缓存失效、分布式锁、缓存穿透 |
| L43 | 异步任务处理 | 5 | Celery、后台任务、定时任务、结果存储 |
| L44 | 微服务架构基础 | 6 | 服务拆分、API 网关、BFF、容器编排 |
| L45 | 分布式系统实战 | 7 | 一致性、CAP 定理、Raft 概述、共识算法 |
| L46 | WebSocket 高级应用 | 5 | 集群、水平扩展、Redis 适配器、粘性会话 |

**阶段知识点总数**: ~76 个

---

## Stage 5: 数据工程（L47-L53）

**能力等级**: S5 → S6  
**建议学时**: 40 小时  
**前置要求**: Stage 4 完成

### 课程与知识点

| 课程 | 标题 | 知识点数 | 核心知识点 |
|------|------|----------|------------|
| L47 | NumPy 科学计算 | 8 | 数组创建、广播、向量运算、SIMD、ufunc |
| L48 | 数据可视化 | 7 | Matplotlib、Seaborn、Plotly、交互图表 |
| L49 | DuckDB 嵌入式分析 | 6 | OLAP、SQLite 替代、向量化执行 |
| L50 | Pandas 数据处理 | 9 | DataFrame、groupby、merge、聚合、清洗 |
| L51 | 异步数据管道 | 6 | 异步 ETL、批量处理、chunk、Pandas 集成 |
| L52 | NumPy RAG PoC | 5 | 向量检索、相似度计算、Embedding |
| L53 | DuckDB OLAP 实战 | 5 | 性能调优、索引、压缩、执行计划 |

**阶段知识点总数**: ~46 个

---

## Stage 6: AI Agent 开发（L54-L65）

**能力等级**: S6 → S7  
**建议学时**: 50 小时  
**前置要求**: Stage 5 完成  
**状态**: ✅ 完整

### 课程与知识点

| 课程 | 标题 | 知识点数 | 核心知识点 |
|------|------|----------|------------|
| L54 | LangGraph 工作流 | 7 | StateGraph、条件边、节点、LangServe |
| L55 | LangChain 基础 | 7 | LCEL、PromptTemplate、Chain、输出解析器 |
| L56 | Agent 基础与工具调用 | 8 | ReAct、Tool Use、AgentExecutor |
| L57 | LangGraph 进阶 | 6 | Memory、Checkpointer、跨图调用 |
| L58 | Agent 记忆管理 | 6 | 短期/长期记忆、摘要、向量存储 |
| L59 | Agent 规划与推理 | 6 | CoT、ToT、ReAct、反思模式 |
| L60 | MCP 协议入门 | 7 | Model Context Protocol、Server/Client、工具注册 |
| L61 | 多智能体编排 | 8 | Agent 协作、任务分配、对话路由 |
| L62 | Agent 评估与调试 | 6 | 指标、日志、回放、Traceloop |
| L63 | Agent 部署与监控 | 7 | Docker、K8s、OTel、Prometheus |
| L64 | Agent SSE 流式路由 | 5 | 流式输出、Token 控制、SSE + AI |
| L65 | RAG 向量数据库 | 8 | Qdrant/Milvus、Embedding、相似度检索 |

**阶段知识点总数**: ~81 个（L54-L65）

---

## Stage A: AI Agent 企业级（A01-A20）

**能力等级**: S7 → S8  
**建议学时**: 80 小时  
**前置要求**: Stage 6 完成

### 课程与知识点

| 课程 | 标题 | 知识点数 | 状态 |
|------|------|----------|------|
| A01 | Agent 安全与对抗防护 | 6 | 🔶 完善中 |
| A02 | Agent 合规与伦理 | 6 | 🔶 完善中 |
| A03 | Agent 监控与可观测性 | 6 | 🔶 完善中 |
| A04 | Agent 成本优化 | 6 | 🔶 完善中 |
| A05 | Agent 企业级项目实战 | 6 | 🔶 完善中 |
| A06 | Agent 架构设计模式 | 6 | 🔶 完善中 |
| A07 | Agent 安全渗透测试 | 6 | 🔶 完善中 |
| A08-A20 | Agent 企业级专题 | — | 🔶 完善中 |

**阶段知识点总数**: ~105 个（A01-A20）

---

## Stage P: Python 爬虫专精（S01-S09）

**能力等级**: P1 → P5  
**建议学时**: 80 小时  
**前置要求**: Stage 0 完成  
**状态**: 🔶 骨架（课程目录待创建）

### 课程规划

| 课程 | 标题 | 知识点数 | 核心知识点 | 状态 |
|------|------|----------|------------|------|
| S01 | 前端基础 | 8 | HTML/CSS 选择器、DOM、Network 面板、XPath | 🔶 |
| S02 | 网页数据解析 | 9 | Requests、XPath、Beautiful Soup、反爬应对 | 🔶 |
| S03 | Scrapy 工业级爬虫 | 8 | Spider、Pipeline、分布式 Scrapy-Redis | 🔶 |
| S04 | 自动化抓包 | 8 | Selenium、Playwright、反检测、mitmproxy | 🔶 |
| S05 | JavaScript 逆向基础 | 8 | JS 核心、加密算法、代码混淆、反调试 | 🔶 |
| S06 | JavaScript 逆向实战 | 9 | 滑块、Token 生成、AST 解混淆、Hook | 🔶 |
| S07 | App 逆向入门 | 8 | APK 分析、反编译、native 函数、签名校验 | 🔶 |
| S08 | Frida 动态分析 | 8 | Hook、RPC、SO 逆向、内存操作 | 🔶 |
| S09 | 爬虫综合项目 | 6 | 全站采集、反反爬、部署监控 | 🔶 |

**阶段知识点总数**: ~72 个（规划中）

---

## Stage K: DevOps 平台工程（K01-K05）

**能力等级**: K1 → K5  
**建议学时**: 30 小时  
**前置要求**: Stage 6 完成

### 课程与知识点

| 课程 | 标题 | 知识点数 | 核心知识点 |
|------|------|----------|------------|
| K01 | AI Agent 部署与可观测性 | 8 | Prometheus、Grafana、OpenTelemetry |
| K02 | Kubernetes 基础 | 8 | Pod、Deployment、Service、ConfigMap |
| K03 | Kubernetes 进阶 | 8 | 存储、网络、安全、RBAC |
| K04 | Helm 与 GitOps | 8 | Chart 开发、ArgoCD、自动化部署 |
| K05 | 平台工程 | 8 | 内部开发者平台、Backstage、IaC |

**阶段知识点总数**: ~40 个

---

## Stage M: 企业级商业应用（M01-M08）

**能力等级**: M3 → M5  
**建议学时**: 50 小时  
**前置要求**: Stage 6 或 Stage K 完成

### 课程与知识点

| 课程 | 标题 | 知识点数 | 状态 |
|------|------|----------|------|
| M01 | Dify/Coze 工作流 | 7 | 🔶 骨架 |
| M02 | LlamaIndex 高级 RAG | 7 | 🔶 骨架 |
| M03 | MLOps 实验追踪 | 7 | 🔶 骨架 |
| M04 | Litestar 轻量框架 | 7 | 🔶 骨架 |
| M05 | RAG 向量库深入 | 7 | 🔶 骨架 |
| M06 | AI Agent 商业大考 | 7 | 🔶 骨架 |
| M07 | RAG 评估框架深度 | 7 | 🔶 骨架（选修）|
| M08 | AI 产品发布与运营 | 7 | 🔶 骨架 |

**阶段知识点总数**: ~56 个（规划中）

---

## Stage R: 前沿探索实验室（R01-R10）

**能力等级**: R1 → R5  
**建议学时**: 40 小时  
**前置要求**: Stage M 或 Stage 6 完成

### 课程与知识点

| 课程 | 标题 | 知识点数 | 状态 |
|------|------|----------|------|
| R01 | Python 3.14t 完全体 | 7 | 🔶 骨架 |
| R02 | GIL Fallback 策略 | 7 | 🔶 骨架 |
| R03 | PEP 649/810 延迟注解 | 7 | 🔶 骨架（选修）|
| R04 | t-string 与格式化 | 7 | 🔶 骨架 |
| R05 | Python 路线图 | 7 | 🔶 骨架（选修）|
| R06 | WASI 边缘部署 | 7 | 🔶 骨架 |
| R07 | Wasm 性能基准 | 7 | 🔶 骨架 |
| R08 | Python 3.15 预览 | 7 | 🔶 骨架 |
| R09 | AI 辅助编程未来 | 7 | 🔶 骨架 |
| R10 | 课程毕业与展望 | 7 | 🔶 骨架 |

**阶段知识点总数**: ~70 个（规划中）

---

## 📈 知识点统计总表

### 按阶段统计

| 阶段 | 课程数 | 知识点数 | 平均每课 | 完成度 |
|------|--------|----------|----------|--------|
| Stage 0 | 10 | 81 | 8.1 | 100% |
| Stage 1 | 9 | 66 | 7.3 | 100% |
| Stage 2 | 9 | 63 | 7.0 | 100% |
| Stage 3 | 10 | 68 | 6.8 | 100% |
| Stage 4 | 11 | 76 | 6.9 | 100% |
| Stage 5 | 7 | 46 | 6.6 | 100% |
| Stage 6 | 12 | 81 | 6.8 | 100% |
| **Core 小计** | **65** | **457** | **7.0** | **100%** |
| Stage A | 20 | 105 | 5.3 | 25% |
| Stage P | 9 | ~72（规划） | 8.0 | 0% |
| Stage K | 5 | ~40 | 8.0 | 100% |
| Stage M | 8 | ~56（规划） | 7.0 | 0% |
| Stage R | 10 | ~70（规划） | 7.0 | 0% |
| **Spec 小计** | **52** | **~343** | **6.6** | **8%** |
| **总计** | **117** | **~800** | **6.8** | **63%** |

### 按知识域统计

| 知识域 | 课程覆盖 | 知识点数 |
|--------|----------|----------|
| Python 基础语法 | L01-L09, P01 | 81 |
| Python 进阶语法 | L10-L18 | 66 |
| 工程化工具链 | L17-L18, L25 | 19 |
| 异步编程 | L14, L19, L22, L36 | 29 |
| 装饰器与元编程 | L20, L23 | 15 |
| Web 开发 | L26-L35, L46 | 65 |
| 安全与认证 | L37, L38 | 15 |
| 微服务架构 | L40, L44, L45 | 20 |
| 数据工程 | L47-L53 | 46 |
| AI Agent | L54-L65 | 81 |
| AI Agent 企业级 | A01-A20 | 105 |
| 爬虫技术 | S01-S09 | 72 |
| DevOps | K01-K05 | 40 |
| 企业应用 | M01-M08 | 56 |
| 前沿探索 | R01-R10 | 70 |

---

## 🎓 学习路径推荐

### 路径 1: Python 全栈工程师（推荐）
```
Stage 0 → 1 → 2 → 3 → 4 → 5 → 6 → A → K → M → R
```
预计学时: ~500 小时

### 路径 2: AI Agent 工程师
```
Stage 0 → 1 → 2 → 3 → 4 → 5 → 6 → A
```
预计学时: ~340 小时

### 路径 3: Python 爬虫工程师
```
Stage 0 → 1 → 2 → P → K
```
预计学时: ~230 小时

### 路径 4: 快速通道
```
Stage 2 → 3 → 4 → 5 → 6 → A
```
预计学时: ~240 小时

---

## 🔗 相关文档

| 文档 | 说明 |
|------|------|
| [COURSE_MAPPING.md](https://github.com/nexo/python313-fullstack/blob/main/COURSE_MAPPING.md) | 课程完整映射表 |
| [docs/knowledge/README.md](./README.md) | 知识点文档索引 |
| [docs/knowledge/KNOWLEDGE_DAG.md](./KNOWLEDGE_DAG.md) | 知识点 DAG 依赖图 |
| [docs/knowledge/KNOWLEDGE_FRAMEWORK.md](./KNOWLEDGE_FRAMEWORK.md) | 知识体系框架 |
| [docs/knowledge/COMPREHENSIVE_AUDIT_REPORT.md](https://github.com/nexo/python313-fullstack/blob/main/docs/knowledge/COMPREHENSIVE_AUDIT_REPORT.md) | 综合审计报告 |

---

**最后更新**: 2026-07-24
**维护者**: Python 3.13 全栈课程组
