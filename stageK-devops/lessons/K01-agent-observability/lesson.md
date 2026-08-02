# K01 AI Agent 部署与可观测性

> **课程版本**: v1.0
> **Python 版本**: 3.13+
> **依赖**: `fastapi`, `prometheus-client`, `opentelemetry-api`, `structlog`

---

## 🎯 课程目标

本课程将帮助你：

1. 掌握 Docker 多阶段构建技术
2. 实现安全的环境配置与密钥管理
3. 集成 Prometheus 指标采集
4. 配置 OpenTelemetry 分布式追踪
5. 构建结构化日志系统

---

## 📖 目录

1. [为什么需要可观测性](#1-为什么需要可观测性)
2. [Docker 容器化](#2-docker-容器化)
3. [环境配置与密钥管理](#3-环境配置与密钥管理)
4. [Prometheus 指标采集](#4-prometheus-指标采集)
5. [OpenTelemetry 分布式追踪](#5-opentelemetry-分布式追踪)
6. [Grafana 仪表板](#6-grafana-仪表板)
7. [结构化日志](#7-结构化日志)
8. [生产级部署模式](#8-生产级部署模式)

---

## 1. 为什么需要可观测性

### 1.1 传统日志的局限性

```python
# 传统日志：难以查询和分析
print(f"User {user_id} logged in at {timestamp}")  # 非结构化
logging.info("Request processed")  # 缺少上下文
```

### 1.2 可观测性三大支柱

```
┌─────────────────────────────────────────────────┐
│                 可观测性                          │
├─────────────────┬─────────────────┬───────────────┤
│     指标        │      追踪       │     日志      │
│   (Metrics)    │    (Traces)    │    (Logs)    │
├─────────────────┼─────────────────┼───────────────┤
│  请求率、延迟   │  请求完整路径   │  事件详情     │
│  错误率、资源   │  性能瓶颈分析   │  调试信息     │
│  告警触发       │  错误根因       │  审计追踪     │
└─────────────────┴─────────────────┴───────────────┘
```

### 1.3 Agent 的特殊需求

| 需求 | 描述 |
|------|------|
| Token 使用量 | 追踪每次请求的 token 消耗 |
| LLM 调用延迟 | 监控 LLM 响应时间 |
| 工具调用统计 | 记录 Agent 使用的工具 |
| 成本分析 | 按用户/会话计算成本 |

---

## 2. Docker 容器化

### 2.1 多阶段构建

```dockerfile
# Dockerfile - Agent 多阶段构建

# 阶段 1: 构建
FROM python:3.13-slim AS builder

WORKDIR /app

# 安装 uv
RUN pip install uv

# 复制依赖文件
COPY pyproject.toml ./

# 使用 uv 安装依赖（仅安装生产依赖）
RUN uv sync --frozen --no-dev

# 阶段 2: 运行
FROM python:3.13-slim AS runner

WORKDIR /app

# 从构建阶段复制依赖
COPY --from=builder /app/.venv /app/.venv

# 复制应用代码
COPY agent/ ./agent/
COPY pyproject.toml ./

# 设置环境变量
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 非 root 用户运行
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "-m", "agent.server"]
```

### 2.2 健康检查端点

```python
"""agent/server.py - 带健康检查的 Agent 服务"""

from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    await initialize_agent()
    yield
    # 关闭时清理
    await cleanup_agent()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "version": "1.0.0",
    }


@app.get("/ready")
async def readiness_check():
    """就绪检查端点"""
    # 检查依赖服务是否可用
    checks = {
        "llm": await check_llm_connection(),
        "vector_store": await check_vector_store(),
        "cache": await check_cache(),
    }

    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503

    return JSONResponse(
        status_code=status_code,
        content={"ready": all_ready, "checks": checks},
    )
```

### 2.3 Docker Compose 本地开发

```yaml
# docker-compose.dev.yml
services:
  agent:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LOG_LEVEL=DEBUG
    volumes:
      - ./agent:/app/agent
    depends_on:
      - redis
      - prometheus

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
```

---

## 3. 环境配置与密钥管理

### 3.1 pydantic-settings 配置

```python
"""agent/config.py - 配置管理"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # 应用配置
    app_name: str = "ai-agent"
    app_version: str = "1.0.0"
    debug: bool = False

    # LLM 配置
    openai_api_key: str = Field(default="", description="OpenAI API Key")
    anthropic_api_key: str = Field(default="", description="Anthropic API Key")
    default_model: str = "gpt-4o-mini"

    # 数据库配置
    database_url: str = "postgresql://user:pass@localhost:5432/agent"

    # Redis 配置
    redis_url: str = "redis://localhost:6379/0"

    # 可观测性配置
    otlp_endpoint: str = "http://localhost:4317"
    metrics_enabled: bool = True
    tracing_enabled: bool = True

    # 速率限制
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000


settings = Settings()
```

### 3.2 密钥管理最佳实践

```python
"""agent/secrets.py - 密钥管理"""

import os
from typing import Optional


class SecretManager:
    """密钥管理器"""

    @staticmethod
    def get_api_key(key_name: str) -> str:
        """获取 API Key"""
        # 1. 优先从环境变量获取
        api_key = os.environ.get(key_name)
        if api_key:
            return api_key

        # 2. 尝试从密钥管理服务获取（生产环境）
        api_key = SecretManager._get_from_secrets_manager(key_name)
        if api_key:
            return api_key

        raise ValueError(f"API Key not found: {key_name}")

    @staticmethod
    def _get_from_secrets_manager(key_name: str) -> Optional[str]:
        """从密钥管理服务获取"""
        # 实现与 AWS Secrets Manager / HashiCorp Vault 的集成
        # 这里作为占位符
        return None

    @staticmethod
    def rotate_api_key(key_name: str) -> None:
        """轮换 API Key"""
        # 实现密钥轮换逻辑
        pass
```

### 3.3 环境变量验证

```python
"""agent/validation.py - 配置验证"""

from pydantic import field_validator
from pydantic_settings import BaseSettings


class ValidatedSettings(BaseSettings):
    """带验证的配置"""

    openai_api_key: str = ""

    @field_validator("openai_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """验证 API Key 格式"""
        if not v:
            # 生产环境必须提供
            if os.environ.get("PRODUCTION"):
                raise ValueError("OPENAI_API_KEY is required in production")
            return v

        # 验证格式
        if not v.startswith("sk-"):
            raise ValueError("Invalid OpenAI API Key format")

        return v
```

---

## 4. Prometheus 指标采集

### 4.1 基础指标

```python
"""agent/metrics.py - Prometheus 指标定义"""

from prometheus_client import Counter, Histogram, Gauge, Info
from functools import wraps
import time


# ============== 计数器 ==============

request_counter = Counter(
    "agent_requests_total",
    "Total number of requests",
    ["method", "endpoint", "status"],
)

llm_call_counter = Counter(
    "agent_llm_calls_total",
    "Total number of LLM calls",
    ["model", "status"],
)

tool_call_counter = Counter(
    "agent_tool_calls_total",
    "Total number of tool calls",
    ["tool_name", "status"],
)


# ============== 直方图 ==============

request_duration = Histogram(
    "agent_request_duration_seconds",
    "Request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0],
)

llm_duration = Histogram(
    "agent_llm_duration_seconds",
    "LLM call duration in seconds",
    ["model"],
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
)

token_usage = Histogram(
    "agent_token_usage",
    "Token usage per request",
    ["model", "token_type"],
    buckets=[100, 500, 1000, 5000, 10000, 50000],
)


# ============== 仪表 ==============

active_requests = Gauge(
    "agent_active_requests",
    "Number of active requests",
)

model_queue_size = Gauge(
    "agent_model_queue_size",
    "Number of requests waiting for model",
    ["model"],
)


# ============== 信息 ==============

app_info = Info("agent", "Agent application info")


# ============== 装饰器 ==============

def track_request(method: str, endpoint: str):
    """请求跟踪装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            active_requests.inc()

            try:
                result = await func(*args, **kwargs)
                request_counter.labels(
                    method=method,
                    endpoint=endpoint,
                    status="success",
                ).inc()
                return result
            except Exception as e:
                request_counter.labels(
                    method=method,
                    endpoint=endpoint,
                    status="error",
                ).inc()
                raise
            finally:
                duration = time.time() - start_time
                request_duration.labels(
                    method=method,
                    endpoint=endpoint,
                ).observe(duration)
                active_requests.dec()

        return wrapper
    return decorator
```

### 4.2 FastAPI 集成

```python
"""agent/metrics_server.py - 指标暴露"""

from fastapi import FastAPI
from prometheus_client import make_asgi_app, REGISTRY
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Agent with Metrics")

# Prometheus 指标端点
metrics_app = make_asgi_app(registry=REGISTRY)
app.mount("/metrics", metrics_app)


@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### 4.3 自定义业务指标

```python
"""agent/business_metrics.py - 业务指标"""

from prometheus_client import Counter, Histogram


# Agent 特定指标
conversation_started = Counter(
    "agent_conversations_started_total",
    "Total conversations started",
    ["user_id", "source"],
)

conversation_completed = Counter(
    "agent_conversations_completed_total",
    "Total conversations completed",
    ["user_id", "outcome"],
)

agent_turns = Histogram(
    "agent_conversation_turns",
    "Number of turns per conversation",
    buckets=[1, 2, 5, 10, 20, 50],
)

tool_execution_time = Histogram(
    "agent_tool_execution_seconds",
    "Tool execution time",
    ["tool_name", "status"],
)

cost_accumulated = Histogram(
    "agent_cost_usd",
    "Accumulated cost in USD",
    ["user_id", "model"],
    buckets=[0.01, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0],
)


class MetricsRecorder:
    """指标记录器"""

    @staticmethod
    def record_llm_call(model: str, duration: float, tokens: int, cost: float):
        """记录 LLM 调用"""
        llm_call_counter.labels(model=model, status="success").inc()
        llm_duration.labels(model=model).observe(duration)
        token_usage.labels(model=model, token_type="total").observe(tokens)

    @staticmethod
    def record_tool_call(tool_name: str, duration: float, status: str):
        """记录工具调用"""
        tool_call_counter.labels(tool_name=tool_name, status=status).inc()
        tool_execution_time.labels(tool_name=tool_name, status=status).observe(duration)

    @staticmethod
    def record_conversation(user_id: str, turns: int, cost: float):
        """记录会话"""
        conversation_completed.labels(user_id=user_id, outcome="success").inc()
        agent_turns.observe(turns)
        cost_accumulated.labels(user_id=user_id, model="all").observe(cost)
```

---

## 5. OpenTelemetry 分布式追踪

### 5.1 基础配置

```python
"""agent/tracing.py - OpenTelemetry 配置"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.trace import Status, StatusCode


# 创建资源
resource = Resource(attributes={
    SERVICE_NAME: "ai-agent",
    "service.version": "1.0.0",
    "deployment.environment": "production",
})

# 配置追踪提供者
trace_provider = TracerProvider(resource=resource)

# 添加 OTLP 导出器
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True,
)
trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# 设置全局追踪提供者
trace.set_tracer_provider(trace_provider)

# 获取追踪器
tracer = trace.get_tracer(__name__)
```

### 5.2 追踪装饰器

```python
"""agent/trace_decorators.py - 追踪装饰器"""

from opentelemetry import trace
from functools import wraps

tracer = trace.get_tracer(__name__)


def traced(span_name: str = None):
    """追踪装饰器"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            name = span_name or func.__name__
            with tracer.start_as_current_span(name) as span:
                try:
                    # 设置属性
                    span.set_attribute("function.name", func.__name__)

                    # 执行函数
                    result = await func(*args, **kwargs)

                    # 记录结果
                    span.set_attribute("result.success", True)
                    return result

                except Exception as e:
                    # 记录错误
                    span.set_attribute("result.success", False)
                    span.set_attribute("error.message", str(e))
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            name = span_name or func.__name__
            with tracer.start_as_current_span(name) as span:
                try:
                    span.set_attribute("function.name", func.__name__)
                    result = func(*args, **kwargs)
                    span.set_attribute("result.success", True)
                    return result
                except Exception as e:
                    span.set_attribute("result.success", False)
                    span.set_attribute("error.message", str(e))
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise

        # 返回正确的包装器
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


# 使用示例
@traced("agent.llm.call")
async def call_llm(prompt: str, model: str) -> str:
    """LLM 调用追踪"""
    with tracer.start_as_current_span("llm.request") as span:
        span.set_attribute("llm.model", model)
        span.set_attribute("llm.prompt.length", len(prompt))

        # 调用 LLM
        response = await actual_llm_call(prompt, model)

        span.set_attribute("llm.response.length", len(response))
        return response


@traced("agent.tool.execute")
async def execute_tool(tool_name: str, args: dict) -> dict:
    """工具执行追踪"""
    with tracer.start_as_current_span("tool.execution") as span:
        span.set_attribute("tool.name", tool_name)

        start_time = time.time()
        result = await actual_tool_call(tool_name, args)
        duration = time.time() - start_time

        span.set_attribute("tool.duration", duration)
        span.set_attribute("tool.status", "success")

        return result
```

### 5.3 上下文传播

```python
"""agent/context_propagation.py - 上下文传播"""

from opentelemetry import context
from opentelemetry.propagate import inject, extract
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import httpx


# 配置传播器
propagator = TraceContextTextMapPropagator()


class TracingHTTPClient:
    """带追踪的 HTTP 客户端"""

    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """发送请求并传播追踪上下文"""

        # 注入当前上下文到请求头
        headers = kwargs.get("headers", {})
        inject(headers)
        kwargs["headers"] = headers

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, **kwargs)
            return response


# 服务间调用
async def call_downstream_service(service_url: str, data: dict):
    """调用下游服务并传播追踪"""

    propagator = TraceContextTextMapPropagator()

    # 从当前上下文提取
    with tracer.start_as_current_span("call.downstream") as span:
        # 注入到 HTTP 头
        headers = {}
        inject(headers)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                service_url,
                json=data,
                headers=headers,
            )

            span.set_attribute("downstream.status", response.status_code)
            return response.json()
```

---

## 6. Grafana 仪表板

### 6.1 Prometheus 数据源配置

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ai-agent'
    static_configs:
      - targets: ['agent:8000']
    metrics_path: '/metrics'
```

### 6.2 Agent 仪表板 JSON

```json
{
  "dashboard": {
    "title": "AI Agent Metrics",
    "panels": [
      {
        "title": "Requests per Second",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(agent_requests_total[1m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Request Duration (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(agent_request_duration_seconds_bucket[5m]))",
            "legendFormat": "p95"
          }
        ]
      },
      {
        "title": "LLM Call Duration",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(agent_llm_duration_seconds_bucket[5m]))",
            "legendFormat": "{{model}} p95"
          }
        ]
      },
      {
        "title": "Token Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(agent_token_usage_total[1m])",
            "legendFormat": "{{model}} {{token_type}}"
          }
        ]
      },
      {
        "title": "Active Requests",
        "type": "stat",
        "targets": [
          {
            "expr": "agent_active_requests",
            "legendFormat": "Active"
          }
        ]
      },
      {
        "title": "Conversation Completion Rate",
        "type": "gauge",
        "targets": [
          {
            "expr": "rate(agent_conversations_completed_total[5m]) / rate(agent_conversations_started_total[5m])",
            "legendFormat": "Completion Rate"
          }
        ]
      }
    ]
  }
}
```

### 6.3 告警规则

```yaml
# alerts.yml
groups:
  - name: agent_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(agent_requests_total{status="error"}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(agent_request_duration_seconds_bucket[5m])) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High request latency"

      - alert: LLMCostSpike
        expr: rate(agent_cost_usd[1h]) > 100
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "LLM cost spike detected"
```

---

## 7. 结构化日志

### 7.1 structlog 配置

```python
"""agent/logging.py - 结构化日志配置"""

import structlog
import logging
import sys


def configure_logging(log_level: str = "INFO"):
    """配置结构化日志"""

    # 配置标准库日志
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    # 配置 structlog
    structlog.configure(
        processors=[
            # 添加时间戳
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            # 格式化时间
            structlog.processors.TimeStamper(fmt="iso"),
            # 添加请求 ID
            structlog.contextvars.merge_contextvars,
            # 异常处理
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            # JSON 序列化
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


# 获取日志器
log = structlog.get_logger()
```

### 7.2 业务日志

```python
"""agent/business_logging.py - 业务日志"""

import structlog
from datetime import datetime

log = structlog.get_logger()


class AgentLogger:
    """Agent 业务日志记录器"""

    @staticmethod
    def log_request(user_id: str, request: dict, response: dict, duration: float):
        """记录请求"""
        log.info(
            "agent.request",
            user_id=user_id,
            request_id=request.get("id"),
            prompt_length=len(request.get("prompt", "")),
            response_length=len(response.get("text", "")),
            duration_ms=round(duration * 1000, 2),
            timestamp=datetime.utcnow().isoformat(),
        )

    @staticmethod
    def log_tool_call(tool_name: str, args: dict, result: dict, duration: float):
        """记录工具调用"""
        log.info(
            "agent.tool_call",
            tool_name=tool_name,
            args=args,
            success=result.get("success", False),
            duration_ms=round(duration * 1000, 2),
            timestamp=datetime.utcnow().isoformat(),
        )

    @staticmethod
    def log_error(error: Exception, context: dict):
        """记录错误"""
        log.error(
            "agent.error",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context,
            timestamp=datetime.utcnow().isoformat(),
        )

    @staticmethod
    def log_cost(user_id: str, model: str, tokens: int, cost: float):
        """记录成本"""
        log.info(
            "agent.cost",
            user_id=user_id,
            model=model,
            tokens=tokens,
            cost_usd=round(cost, 4),
            timestamp=datetime.utcnow().isoformat(),
        )


# 使用示例
logger = AgentLogger()

# 记录请求
logger.log_request(
    user_id="user_123",
    request={"id": "req_001", "prompt": "Hello"},
    response={"text": "Hi there!"},
    duration=1.5,
)

# 记录错误
try:
    # 可能失败的代码
    pass
except Exception as e:
    logger.log_error(e, {"user_id": "user_123", "request_id": "req_001"})
```

---

## 8. 生产级部署模式

### 8.1 优雅关闭

```python
"""agent/graceful_shutdown.py - 优雅关闭"""

import asyncio
from contextlib import asynccontextmanager


class GracefulShutdown:
    """优雅关闭管理器"""

    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.is_shutting_down = False

    async def wait_for_shutdown(self):
        """等待关闭信号"""
        await self.shutdown_event.wait()

    def trigger_shutdown(self):
        """触发关闭"""
        self.is_shutting_down = True
        self.shutdown_event.set()


shutdown_manager = GracefulShutdown()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""

    # 启动
    log.info("Starting application...")

    # 启动后台任务
    background_task = asyncio.create_task(background_processor())

    yield

    # 关闭
    log.info("Shutting down gracefully...")

    # 1. 停止接受新请求
    shutdown_manager.trigger_shutdown()

    # 2. 等待正在处理的请求完成
    await wait_for_active_requests(timeout=30)

    # 3. 关闭后台任务
    background_task.cancel()
    try:
        await background_task
    except asyncio.CancelledError:
        pass

    # 4. 刷新指标
    flush_metrics()

    # 5. 关闭连接
    await close_connections()

    log.info("Shutdown complete")


async def wait_for_active_requests(timeout: float = 30):
    """等待活跃请求完成"""
    start = asyncio.get_event_loop().time()

    while active_requests_count() > 0:
        if asyncio.get_event_loop().time() - start > timeout:
            log.warning("Timeout waiting for active requests")
            break
        await asyncio.sleep(1)
```

### 8.2 限流中间件

```python
"""agent/rate_limit.py - 限流中间件"""

from fastapi import FastAPI, Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address)


app = FastAPI()


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """限流异常处理"""
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": str(exc),
            "retry_after": exc.detail,
        },
    )


@app.get("/api/agent")
@limiter.limit("60/minute")
async def agent_endpoint(request: Request):
    """带限流的 Agent 端点"""
    return {"message": "OK"}
```

---

## 📝 总结

本课程涵盖了 AI Agent 部署与可观测性的核心实践：

| 主题 | 关键点 |
|------|--------|
| Docker 多阶段构建 | 减小镜像体积，提高安全性 |
| 配置管理 | pydantic-settings，密钥分离 |
| Prometheus 指标 | 请求延迟、Token 使用、错误率 |
| OpenTelemetry 追踪 | 分布式追踪、上下文传播 |
| Grafana 仪表板 | 可视化监控、告警规则 |
| 结构化日志 | JSON 格式、易于查询 |

---

## 🔗 延伸学习

- [L64 Agent 部署与监控](../../../stage6-ai-agent/lessons/L64-agent-deployment/) - 基础部署
- [K02 Kubernetes 基础](../K02-kubernetes-basics/) - K8s 编排

---

*课程版本: v1.0 | 最后更新: 2026-07-20*


## 🔗 下一步


[K02: Kubernetes 基础](../K02-kubernetes-basics/)
