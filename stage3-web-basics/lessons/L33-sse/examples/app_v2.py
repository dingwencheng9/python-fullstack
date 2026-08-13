"""

from __future__ import annotations

L32 SSE 服务器推送事件 - FastAPI 主程序 V2
======================================

本模块实现 Agent 流式对话的完整 FastAPI 应用。

核心能力：
1. AsyncPG + Redis 连接池管理
2. OpenTelemetry 可观测性
3. 生命周期钩子 (lifespan)
4. 健康检查端点
5. CORS 中间件

作者：Python 3.13 全栈课程
"""

from contextlib import asynccontextmanager
import os

from agent_chat_router_v2 import (
    cleanup_storage,
    initialize_storage,
    router as agent_router_v2,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# ============================================================
# 1. 配置
# ============================================================


class Config:
    """应用配置"""

    # 数据库配置（⚠️ 生产环境必须从环境变量设置）
    # 演示时使用 secrets.token_hex() 动态生成（仅内存有效）
    import secrets
    _default_db_pass = secrets.token_hex(16)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://postgres:{_default_db_pass}@localhost:5432/agent_db"
    )  # type: ignore[assignment]
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")  # type: ignore[assignment]

    # OpenTelemetry 配置
    OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    OTEL_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "agent-chat-api")

    # 应用配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))


config = Config()


# ============================================================
# 2. OpenTelemetry 初始化
# ============================================================


def setup_opentelemetry():
    """
    初始化 OpenTelemetry

    **配置**:
    - OTLP gRPC Exporter
    - Jaeger 后端
    - FastAPI 自动 instrumentation
    """
    # 创建资源
    resource = Resource.create(
        {
            "service.name": config.OTEL_SERVICE_NAME,
            "service.version": "2.0",
        }
    )

    # 创建 TracerProvider
    provider = TracerProvider(resource=resource)

    # 创建 OTLP Exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint=config.OTEL_EXPORTER_OTLP_ENDPOINT,
        insecure=True,  # 开发环境，生产环境使用 TLS
    )

    # 添加 BatchSpanProcessor
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    # 设置全局 TracerProvider
    trace.set_tracer_provider(provider)

    print("✅ OpenTelemetry 已初始化")
    print(f"   服务名: {config.OTEL_SERVICE_NAME}")
    print(f"   OTLP 端点: {config.OTEL_EXPORTER_OTLP_ENDPOINT}")


# ============================================================
# 3. 生命周期管理
# ============================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    **启动时**:
    - 初始化 OpenTelemetry
    - 建立 PostgreSQL 连接池
    - 建立 Redis 连接池

    **关闭时**:
    - 优雅关闭数据库连接
    - 优雅关闭 Redis 连接
    """
    # 启动
    print("=" * 80)
    print("启动 AI Agent Chat API V2")
    print("=" * 80 + "\n")

    # 初始化 OpenTelemetry
    setup_opentelemetry()

    # 初始化存储系统
    await initialize_storage(
        config.DATABASE_URL,
        config.REDIS_URL,
    )

    print(f"\n服务地址: http://{config.HOST}:{config.PORT}")
    print(f"API 文档: http://{config.HOST}:{config.PORT}/docs")
    print(f"健康检查: http://{config.HOST}:{config.PORT}/health")
    print("\n🚀 应用启动完成\n")
    print("=" * 80 + "\n")

    yield

    # 关闭
    print("\n" + "=" * 80)
    print("关闭 AI Agent Chat API V2")
    print("=" * 80 + "\n")

    await cleanup_storage()

    print("✅ 应用已关闭\n")
    print("=" * 80)


# ============================================================
# 4. FastAPI 应用
# ============================================================

app = FastAPI(
    title="AI Agent Chat API V2",
    description="生产级 AI Agent 对话系统（支持会话持久化和 Token 智能压缩）",
    version="2.0.0",
    lifespan=lifespan,
)


# ============================================================
# 5. 中间件
# ============================================================

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 6. 健康检查
# ============================================================


@app.get("/health", tags=["健康检查"])
async def health_check():
    """
    健康检查端点

    **返回**: 应用状态
    """
    return JSONResponse(
        {
            "status": "healthy",
            "service": config.OTEL_SERVICE_NAME,
            "version": "2.0.0",
        }
    )


@app.get("/", tags=["根路径"])
async def root():
    """
    根路径

    **返回**: API 信息
    """
    return JSONResponse(
        {
            "message": "AI Agent Chat API V2",
            "docs": "/docs",
            "health": "/health",
            "version": "2.0.0",
            "features": [
                "SSE 流式响应",
                "PostgreSQL + Redis 双层存储",
                "Token 智能压缩",
                "会话持久化",
                "OpenTelemetry 追踪",
            ],
        }
    )


# ============================================================
# 7. 挂载路由
# ============================================================

# Agent V2 路由
app.include_router(
    agent_router_v2,
    prefix="",  # 路由已包含 /api/v2/agent
)


# ============================================================
# 8. OpenTelemetry FastAPI Instrumentation
# ============================================================

# 自动 instrumentation（在应用创建后调用）
FastAPIInstrumentor.instrument_app(app)


# ============================================================
# 9. 主程序
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app_v2:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,  # 开发模式，生产环境设为 False
        log_level=config.LOG_LEVEL.lower(),
    )
