# L64: Agent 部署与监控

> **课程编号**: L64
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐⭐（AI Agent 专家级）
> **前置课程**: L63 Agent 评估
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L63**: Agent 评估与调试（理解 Agent 质量保障）

**如果你还没有学习以上课程，建议先完成前置课程。**

---

> **课程定位**: Stage 6 AI Agent 系统 - 生产化部署与运维  
> **前置要求**: L48-L64 Agent 完整体系  
> **后续课程**: 无 (Stage 5 完结)  
> **学习时长**: 4-5 小时

---

---

## 📚 目录

- [第一章：FastAPI 封装](#第一章fastapi-封装)
- [第二章：容器化部署](#第二章容器化部署)
- [第三章：监控与告警](#第三章监控与告警)
- [第四章：生产最佳实践](#第四章生产最佳实践)

---

## 第一章：FastAPI 封装

### 1.1 基础 API 结构

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import uvicorn

# 请求模型
class AgentRequest(BaseModel):
    query: str = Field(..., description="用户查询", min_length=1)
    session_id: str | None = Field(None, description="会话 ID")
    stream: bool = Field(False, description="是否流式响应")

# 响应模型
class AgentResponse(BaseModel):
    result: str
    session_id: str
    tokens_used: int
    latency: float

# 创建 App
app = FastAPI(
    title="Agent API",
    description="生产级 AI Agent 服务",
    version="1.0.0"
)

# Agent 实例 (全局)
agent = create_agent()

@app.post("/agent/chat", response_model=AgentResponse)
async def chat(request: AgentRequest):
    """Agent 对话接口"""
    import time
    start_time = time.time()

    try:
        result = await agent.arun(
            request.query,
            session_id=request.session_id
        )

        return AgentResponse(
            result=result,
            session_id=request.session_id or "new",
            tokens_used=agent.last_tokens,
            latency=time.time() - start_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```python
---

### 1.2 流式响应 (SSE)

```python
from fastapi.responses import StreamingResponse
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

@app.post("/agent/stream")
async def stream_chat(request: AgentRequest):
    """流式对话"""

    async def generate():
        async for chunk in agent.astream(request.query):
            # 发送 SSE 格式
            yield f"data: {chunk}\n\n"

        # 结束标记
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```python
---

### 1.3 健康检查

```python
from datetime import datetime

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/ready")
async def readiness_check():
    """就绪检查"""
    try:
        # 检查依赖服务
        await check_database()
        await check_redis()
        await check_llm()

        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Not ready: {str(e)}")
```sql
---

## 第二章：容器化部署

### 2.1 Dockerfile

```dockerfile
# 多阶段构建
FROM python:3.13-slim as builder

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 生产镜像
FROM python:3.13-slim

WORKDIR /app

# 复制依赖
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# 复制应用
COPY . .

# 非 root 用户
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```bash
---

### 2.2 docker-compose.yml

```yaml
version: "3.8"

services:
  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
      - POSTGRES_URL=postgresql://postgres:password@postgres:5432/agent_db
    depends_on:
      - redis
      - postgres
    restart: unless-stopped
    networks:
      - agent-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - agent-network

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: agent_db
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - agent-network

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    networks:
      - agent-network

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus
    networks:
      - agent-network

volumes:
  redis-data:
  postgres-data:
  prometheus-data:
  grafana-data:

networks:
  agent-network:
    driver: bridge
```yaml
---

### 2.3 Kubernetes 部署

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-api
  labels:
    app: agent-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-api
  template:
    metadata:
      labels:
        app: agent-api
    spec:
      containers:
        - name: agent-api
          image: agent-api:1.0.0
          ports:
            - containerPort: 8000
          env:
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: agent-secrets
                  key: openai-api-key
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "2Gi"
              cpu: "2000m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: agent-api-service
spec:
  selector:
    app: agent-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```python
---

## 第三章：监控与告警

### 3.1 Prometheus 指标

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi import Response

# 定义指标
request_count = Counter(
    'agent_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'agent_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

active_sessions = Gauge(
    'agent_active_sessions',
    'Number of active sessions'
)

token_usage = Counter(
    'agent_tokens_total',
    'Total tokens used',
    ['model']
)

# 中间件
@app.middleware("http")
async def metrics_middleware(request, call_next):
    method = request.method
    endpoint = request.url.path

    # 记录请求
    with request_duration.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)

    # 记录状态
    request_count.labels(
        method=method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()

    return response

# 暴露指标
@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
```yaml
---

### 3.2 prometheus.yml 配置

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "agent-api"
    static_configs:
      - targets: ["agent-api:8000"]
    metrics_path: "/metrics"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

rule_files:
  - "alerts.yml"
```yaml
---

### 3.3 Grafana 告警规则

```yaml
# alerts.yml
groups:
  - name: agent_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(agent_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} requests/sec"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(agent_request_duration_seconds_bucket[5m])) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P95 latency is {{ $value }} seconds"

      - alert: HighTokenUsage
        expr: rate(agent_tokens_total[1h]) > 1000000
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High token usage"
          description: "Token usage is {{ $value }} tokens/hour"
```python
---

## 第四章：生产最佳实践

### 4.1 优雅关闭

```python
import signal
import asyncio

class GracefulShutdown:
    def __init__(self):
        self.is_shutting_down = False
        self.active_requests = 0

    async def shutdown(self):
        """优雅关闭"""
        print("Shutting down gracefully...")
        self.is_shutting_down = True

        # 等待活跃请求完成
        while self.active_requests > 0:
            print(f"Waiting for {self.active_requests} requests to finish...")
            await asyncio.sleep(1)

        print("Shutdown complete")

shutdown_handler = GracefulShutdown()

@app.middleware("http")
async def track_requests(request, call_next):
    if shutdown_handler.is_shutting_down:
        return Response("Service is shutting down", status_code=503)

    shutdown_handler.active_requests += 1
    try:
        response = await call_next(request)
        return response
    finally:
        shutdown_handler.active_requests -= 1

# 信号处理
def signal_handler(signum, frame):
    asyncio.create_task(shutdown_handler.shutdown())

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```python
---

### 4.2 限流与降级

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 限流器
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/agent/chat")
@limiter.limit("10/minute")  # 每分钟 10 次
async def chat(request: Request, data: AgentRequest):
    """限流保护"""
    return await agent.arun(data.query)

# 降级策略
@app.post("/agent/chat")
async def chat_with_fallback(data: AgentRequest):
    """降级保护"""
    try:
        # 尝试主模型
        result = await agent.arun(data.query, model="gpt-4o")
        return {"result": result, "model": "gpt-4o"}
    except Exception as e:
        # 降级到小模型
        logger.warning(f"Fallback to gpt-4o-mini: {e}")
        result = await agent.arun(data.query, model="gpt-4o-mini")
        return {"result": result, "model": "gpt-4o-mini"}
```python
---

### 4.3 结构化日志

```python
import structlog
from datetime import datetime

# 配置结构化日志
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

@app.post("/agent/chat")
async def chat(request: AgentRequest):
    """结构化日志"""
    logger.info(
        "agent_request_received",
        query=request.query[:100],
        session_id=request.session_id,
        user_ip=request.client.host
    )

    try:
        result = await agent.arun(request.query)

        logger.info(
            "agent_request_completed",
            session_id=request.session_id,
            tokens=agent.last_tokens,
            latency=agent.last_latency
        )

        return {"result": result}
    except Exception as e:
        logger.error(
            "agent_request_failed",
            error=str(e),
            session_id=request.session_id
        )
        raise
```text
---

## 第五章：Ollama 本地模型部署

### 5.1 Ollama 简介

**Ollama** 提供本地 LLM 推理能力，适合：
- ✅ 隐私敏感场景（数据不出境）
- ✅ 开发/测试环境（零 API 成本）
- ✅ 低延迟本地推理
- ✅ 完全可控的模型版本

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull llama3.2        # 基础对话
ollama pull llama3.2:3b     # 3B 参数版本（更快）
ollama pull qwen2.5:7b      # 阿里通义（中文优化）
ollama pull nomic-embed-text  # 向量嵌入模型

# 启动服务
ollama serve
```

### 5.2 Ollama + LangChain 集成

```python
# 安装: uv add langchain-ollama

from langchain_ollama import ChatOllama, OllamaEmbeddings

# 1. Chat 模型配置
llm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434",
    temperature=0.7,
    num_ctx=4096,  # 上下文窗口
    num_gpu=1,     # GPU 加速
)

# 2. 向量嵌入配置
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434",
)

# 3. 简单对话
response = llm.invoke("你好，请介绍一下自己")
print(response.content)
```python
---

### 5.3 Ollama Agent 实现

```python
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool

# 配置 Ollama LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    num_ctx=2048,
)

# 定义工具
@tool
def search_code(query: str) -> str:
    """搜索代码库"""
    return f"找到 {query} 相关代码..."

@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"

# 创建 Agent
tools = [search_code, calculate]
agent = create_react_agent(llm, tools, prompt=react_prompt)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10
)

# 执行
result = executor.invoke({"input": "计算 (100 + 200) * 3"})
print(result["output"])
```

### 5.4 Ollama + LangGraph 状态机

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.redis import RedisSaver
from langchain_ollama import ChatOllama
import redis.asyncio as aioredis

# 1. 配置
llm = ChatOllama(model="llama3.2", temperature=0)

# 2. Redis Checkpointer（跨请求保持状态）
redis_client = aioredis.from_url("redis://localhost:6379")
checkpointer = RedisSaver(client=redis_client, session_ttl=3600)

# 3. 定义节点
def agent_node(state: dict) -> dict:
    """Agent 节点"""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state: dict) -> str:
    """条件路由"""
    messages = state["messages"]
    last_message = messages[-1]
    if "完成" in last_message.content:
        return END
    return "agent"

# 4. 构建图
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)

# 5. 编译
app = graph.compile(checkpointer=checkpointer)

# 6. 使用
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke(
    {"messages": [("user", "你好")]},
    config
)
```

### 5.5 Ollama Docker 部署

```yaml
# docker-compose.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
      - OLLAMA_NUM_PARALLEL=2
      - OLLAMA_MAX_LOADED_MODELS=2
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - LLM_MODEL=llama3.2
      - REDIS_URL=redis://redis:6379
    depends_on:
      ollama:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  ollama_data:
```

### 5.6 Ollama vs OpenAI API 对比

| 特性 | Ollama | OpenAI API |
|------|--------|------------|
| 成本 | 免费（本地） | 按 token 计费 |
| 隐私 | 数据不出境 | 数据发送云端 |
| 延迟 | 依赖硬件 | 通常较低 |
| 模型控制 | 完全可控 | 受限于 API |
| 部署难度 | 中等 | 简单 |
| 适用场景 | 隐私/开发/测试 | 生产/大规模 |

**推荐策略**:
- 开发测试: **Ollama**（零成本）
- 生产部署: **OpenAI / vLLM**（高可用）
- 隐私敏感: **Ollama + 私有化部署**

---

## 第六章：vLLM 生产推理

### 6.1 vLLM 简介

**vLLM** 是高性能 LLM 推理引擎，支持：
- ✅ PagedAttention（显存优化）
- ✅ 张量并行（多 GPU）
- ✅ 流式输出
- ✅ OpenAI API 兼容

```bash
# 安装 vLLM
uv add vllm

# 启动 vLLM 服务器
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.2-3B-Instruct \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.9 \
    --port 8000
```

### 6.2 vLLM + LangChain

```python
from langchain_openai import ChatOpenAI

# vLLM 兼容 OpenAI API
llm = ChatOpenAI(
    model="meta-llama/Llama-3.2-3B-Instruct",
    openai_api_base="http://localhost:8000/v1",  # vLLM 端点
    api_key="dummy",  # vLLM 不需要真实 key
    temperature=0.7,
)

response = llm.invoke("你好")
print(response.content)
```

---

## 🎯 最佳实践总结

### ✅ 生产部署检查清单

- [ ] 使用多阶段 Dockerfile 减小镜像体积
- [ ] 非 root 用户运行容器
- [ ] 配置健康检查和就绪检查
- [ ] 设置资源限制 (CPU/内存)
- [ ] 实现优雅关闭
- [ ] 添加限流保护
- [ ] 配置监控指标
- [ ] 设置告警规则
- [ ] 使用结构化日志
- [ ] 配置日志轮转
- [ ] 密钥环境变量管理
- [ ] 多副本部署 (至少 3 个)

### 部署架构

```python
Internet
    ↓
Load Balancer (nginx/Traefik)
    ↓
┌───────────────────────────────────┐
│  Agent API Pods (3 replicas)      │
│  - Health Check                   │
│  - Metrics Endpoint               │
└───────────────────────────────────┘
    ↓
┌───────────────────────────────────┐
│  Infrastructure                   │
│  - Redis (cache)                  │
│  - PostgreSQL (persistence)       │
│  - Prometheus (metrics)           │
│  - Grafana (visualization)        │
└───────────────────────────────────┘
```text
---

## 第五章：生产级 Docker Compose

单容器部署适合演示，生产环境需要多服务编排。典型 AI Agent 系统至少包含：

```text
API 服务 ──→ PostgreSQL    (会话/用户/任务状态)
        ├─→ Redis        (缓存/限流/队列)
        └─→ Qdrant       (向量检索/RAG)
```yaml
### 5.1 Compose 服务拆分

生产级 `docker-compose.yml` 不是把所有东西塞进一个容器，而是明确服务边界：

- `api`: FastAPI + Agent 业务逻辑
- `postgres`: 结构化数据
- `redis`: 缓存、限流、短期状态
- `qdrant`: 向量库

示例见 `examples/02_docker_compose_prod.yml`。

### 5.2 depends_on + healthcheck

仅写 `depends_on` 不够。Docker 只保证启动顺序，不保证服务真的可用。

```yaml
depends_on:
  postgres:
    condition: service_healthy
```yaml
这样 API 会等 PostgreSQL 的 healthcheck 通过后再启动。

### 5.3 资源限制

生产环境要为服务设置 CPU/内存边界，防止单个服务拖垮整台机器。

```yaml
deploy:
  resources:
    limits:
      cpus: "1.0"
      memory: 1G
```yaml
## 第六章：环境变量与密钥管理

`.env.example` 应提交到仓库，真实 `.env` 不应提交。

必备变量：

- `DATABASE_URL`
- `REDIS_URL`
- `QDRANT_URL`
- `JWT_SECRET`
- `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`

示例见 `examples/03_env_example.txt`。

## 第七章：健康检查与回滚

### 7.1 health / ready / metrics

| 端点       | 含义       | 用途               |
| ---------- | ---------- | ------------------ |
| `/health`  | 进程还活着 | Docker healthcheck |
| `/ready`   | 依赖都可用 | 流量切换           |
| `/metrics` | 指标暴露   | Prometheus         |

### 7.2 本地健康检查脚本

Docker Compose 可用 CLI 脚本做本地检查：

```yaml
healthcheck:
  test: ["CMD", "python", "-m", "app.healthcheck"]
```python
对应 Python 代码见 `examples/04_healthcheck.py`。

### 7.3 回滚策略

最简单的回滚策略：镜像版本固定。

```bash
# 发布前
docker compose pull
docker compose up -d

# 回滚到上一版本
docker compose down
docker compose up -d api=python-fullstack-agent:previous
```

## 第八章：上线前检查清单

- [ ] `.env` 已配置，且没有提交到 Git
- [ ] `JWT_SECRET` 长度 ≥ 32 字符
- [ ] PostgreSQL/Redis/Qdrant 都有 volume
- [ ] 所有服务都有 healthcheck
- [ ] API 等待依赖 service_healthy
- [ ] 日志可查看：`docker compose logs -f api`
- [ ] 数据备份策略已确认
- [ ] 回滚镜像 tag 已记录

---

## 🔗 延伸阅读

### 相关课程

- **L42 FastAPI 可观测性** - OpenTelemetry
- **L49 安全网关** - JWT 认证
- **L63 Agent 评估** - 质量保证

### 推荐资源

- [FastAPI 部署文档](https://fastapi.tiangolo.com/deployment/)
- [Docker 最佳实践](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes 生产最佳实践](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Prometheus 监控指南](https://prometheus.io/docs/practices/naming/)

---

## 📝 练习题

### 练习 1: FastAPI 封装

实现完整 Agent API:

- 请求/响应模型
- 错误处理
- 健康检查

### 练习 2: Docker 部署

编写部署配置:

- Dockerfile
- docker-compose.yml
- 环境变量管理

### 练习 3: 监控系统

实现监控:

- Prometheus 指标
- Grafana 面板
- 告警规则

---

**练习答案**: 参见 `solutions/` 目录

**🎉 **恭喜完成 Stage 6 AI Agent 系统全部课程！**

## 🔗 下一步

[L65: Agent SSE 流式路由](../L65-agent-sse-router/)
