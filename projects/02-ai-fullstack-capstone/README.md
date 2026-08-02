# 项目 2: AI Fullstack Capstone — 作品集级 AI 知识助手

> **难度**: ⭐⭐⭐⭐⭐ | **预计时间**: 14h | **前置课程**: Stage 3/4/5 全部核心课

## 项目目标

构建一个完整 AI 全栈应用：导入文档 → 检索知识 → Agent 回答 → HTMX/SSE 前端交互 → CI/CD → Docker Compose 部署。

```
文档导入 → 分块 → 向量检索/关键词检索 → Agent 生成回答 → SSE 流式输出
```

## 功能范围

### P0 — 必做

- `/health` 健康检查
- 文档导入 API
- 内存知识库检索（无外部服务依赖）
- Mock LLM Agent（无 API Key 可运行）
- HTMX 首页
- SSE 流式回答
- 教学版 RBAC（viewer / editor / admin + workspace 隔离）
- pytest 测试

### P1 — 可选

- Qdrant 向量库
- DuckDB 持久化
- WebSocket Chat
- Docker Compose 多服务

## 🚀 快速开始

### 一键启动（推荐，无需 API Key）

项目默认使用 Mock LLM Agent，**不需要真实 OpenAI API Key** 即可完整跑通：

```bash
# 从仓库根目录运行
bash projects/02-ai-fullstack-capstone/run.sh
```

访问：http://localhost:8000

### 手动启动

```bash
cd projects/02-ai-fullstack-capstone
uv sync --extra web --extra ai
PYTHONPATH=. uv run uvicorn app.main:app --reload
```

### 配置真实 API Key（可选）

```bash
cp .env.example .env
# 如需切换真实 LLM，再编辑 .env 填入 OPENAI_API_KEY
# 不填时仍使用 Mock LLM，可离线运行
```

### 运行测试

```bash
PYTHONPATH=. uv run pytest tests/ -v --no-cov
```

## 教学版 RBAC

本项目使用 Header 模拟企业级多租户权限模型，不引入登录、JWT 或数据库迁移，重点教学 RBAC 的核心边界。

### Header 协议

| Header           | 示例                          | 说明                             |
| ---------------- | ----------------------------- | -------------------------------- |
| `X-User-Id`      | `alice`                       | 当前用户 ID，缺省为 `anonymous`  |
| `X-Role`         | `viewer` / `editor` / `admin` | 当前角色，缺省为 `viewer`        |
| `X-Workspace-Id` | `acme`                        | 当前 workspace，缺省为 `default` |

### 权限矩阵

| 角色     | chat | stream chat | upload documents | stats |
| -------- | ---- | ----------- | ---------------- | ----- |
| `viewer` | ✅   | ✅          | ❌               | ❌    |
| `editor` | ✅   | ✅          | ✅               | ❌    |
| `admin`  | ✅   | ✅          | ✅               | ✅    |

### 示例

```bash
# editor 上传文档到 acme workspace
curl -X POST http://localhost:8000/documents \
  -H 'X-User-Id: alice' \
  -H 'X-Role: editor' \
  -H 'X-Workspace-Id: acme' \
  -H 'Content-Type: application/json' \
  -d '{"title":"LangGraph","content":"LangGraph 使用状态机"}'

# viewer 在同 workspace 提问
curl -X POST http://localhost:8000/chat \
  -H 'X-User-Id: bob' \
  -H 'X-Role: viewer' \
  -H 'X-Workspace-Id: acme' \
  -H 'Content-Type: application/json' \
  -d '{"question":"LangGraph 是什么"}'

# viewer 不能上传文档（403）
curl -X POST http://localhost:8000/documents \
  -H 'X-Role: viewer' \
  -H 'Content-Type: application/json' \
  -d '{"title":"Nope","content":"forbidden"}'
```

> 这是教学版 RBAC：Header 只用于演示权限边界，不是生产安全方案。生产环境应使用 JWT/OAuth + 数据库持久化。

## 项目结构

```
projects/02-ai-fullstack-capstone/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   │   ├── chat.py
│   │   ├── documents.py
│   │   └── health.py
│   ├── services/
│   │   ├── rag.py
│   │   ├── agent.py
│   │   ├── vector_store.py
│   │   └── storage.py
│   ├── templates/index.html
│   └── static/style.css
├── tests/
├── docker-compose.yml
├── .env.example
└── README.md
```

## 快速开始

```bash
cd projects/02-ai-fullstack-capstone
python -m pytest tests/ -v
```

## 评分标准

| 维度       | 权重 | 要求                           |
| ---------- | ---- | ------------------------------ |
| 后端 API   | 25%  | health/documents/chat 路由完整 |
| RAG 检索   | 25%  | 能检索相关文档片段             |
| Agent 回答 | 20%  | Mock LLM 可离线运行            |
| 前端交互   | 15%  | HTMX + SSE 可用                |
| 测试质量   | 15%  | 12+ 测试，覆盖错误路径         |
