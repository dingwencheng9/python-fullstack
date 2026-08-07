"""

from __future__ import annotations

L32 SSE 服务器推送事件 - SSE 完整集成示例
======================================

本模块展示如何集成：
1. 流式事件捕获系统（02_streaming_events.py）
2. FastAPI SSE 路由（agent_chat_router.py）
3. JWT 认证（Stage 4 安全网关）
4. OpenTelemetry 追踪

作者：Python 3.13 全栈课程
"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# ============================================================
# 1. OpenTelemetry 初始化
# ============================================================


def setup_telemetry(service_name: str = "agent-chat-api"):
    """
    初始化 OpenTelemetry

    **集成点**: stage3-web-basics/lessons/L27-fastapi-basics
    """
    # 创建 Resource
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": "1.0.0",
            "deployment.environment": "development",
        }
    )

    # 创建 Tracer Provider
    provider = TracerProvider(resource=resource)

    # 添加 OTLP Exporter（发送到 Jaeger）
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4317",
        insecure=True,
    )

    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)

    # 设置全局 Tracer Provider
    trace.set_tracer_provider(provider)

    return provider


# ============================================================
# 2. FastAPI 应用初始化
# ============================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    **启动**:
    - 初始化 OpenTelemetry
    - 连接数据库
    - 加载模型

    **关闭**:
    - 清理资源
    """
    # 启动
    print("🚀 应用启动中...")

    # 初始化 OpenTelemetry
    provider = setup_telemetry()
    print("✅ OpenTelemetry 已初始化")

    yield

    # 关闭
    print("🛑 应用关闭中...")

    # 强制刷新 Spans
    provider.force_flush()
    print("✅ OpenTelemetry Spans 已刷新")


app = FastAPI(
    title="AI Agent Chat API",
    description="流式 Agent 对话 API（SSE）",
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# 3. 中间件配置
# ============================================================

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

# FastAPI OpenTelemetry 自动追踪
FastAPIInstrumentor.instrument_app(app)


# ============================================================
# 4. 路由注册
# ============================================================

# 导入 Agent Chat Router
from agent_chat_router import router as agent_router

app.include_router(agent_router)


# ============================================================
# 5. 根端点
# ============================================================


@app.get("/")
async def root():
    """根端点"""
    return {
        "service": "AI Agent Chat API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/v1/agent/chat",
            "health": "/api/v1/agent/health",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health():
    """全局健康检查"""
    return {
        "status": "healthy",
        "services": {
            "api": "ok",
            "telemetry": "ok",
        },
    }


# ============================================================
# 6. 测试脚本
# ============================================================


async def test_sse_endpoint():
    """
    测试 SSE 端点

    **依赖**: httpx
    """
    import httpx

    print("=" * 80)
    print("测试 SSE 端点")
    print("=" * 80 + "\n")

    url = "http://localhost:8000/api/v1/agent/chat"
    headers = {
        "Authorization": "Bearer demo-token",
        "Content-Type": "application/json",
    }
    data = {
        "message": "搜索关于 Python 异步编程的知识",
        "stream": True,
    }

    print(f"请求 URL: {url}")
    print(f"请求头: {headers}")
    print(f"请求体: {data}\n")
    print("=" * 80)
    print("SSE 事件流:")
    print("=" * 80 + "\n")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=data, headers=headers) as response:
                print(f"状态码: {response.status_code}\n")

                if response.status_code != 200:
                    print(f"错误: {await response.aread()}")
                    return

                current_event = None

                async for line in response.aiter_lines():
                    if not line.strip():
                        continue

                    if line.startswith("event:"):
                        current_event = line.replace("event:", "").strip()
                        print(f"\n[{current_event}]", end=" ")

                    elif line.startswith("data:"):
                        data_str = line.replace("data:", "").strip()

                        try:
                            import json

                            data = json.loads(data_str)

                            # Token 流式渲染
                            if data.get("event_type") == "on_chat_model_stream":
                                if not data.get("is_final"):
                                    print(data["token"], end="", flush=True)
                                else:
                                    print()  # 换行

                            # 工具调用
                            elif data.get("event_type") == "on_tool_start":
                                print(f"\n\n🔧 工具调用: {data['tool_name']}")
                                print(f"   参数: {data['tool_input']}")

                            elif data.get("event_type") == "on_tool_end":
                                status = "✅ 成功" if data["success"] else "❌ 失败"
                                print(f"   {status} (耗时: {data['duration_ms']:.2f}ms)")

                            # 连接/完成事件
                            elif data.get("type") in ["connection", "completion"]:
                                print(f"{data}")

                        except json.JSONDecodeError:
                            print(data_str)

        print("\n\n" + "=" * 80)
        print("测试完成")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ 错误: {e}")


# ============================================================
# 7. 主程序
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 测试模式
        asyncio.run(test_sse_endpoint())
    else:
        # 启动服务
        import uvicorn

        print("=" * 80)
        print("启动 AI Agent Chat API")
        print("=" * 80 + "\n")

        print("服务地址: http://localhost:8000")
        print("API 文档: http://localhost:8000/docs")
        print("健康检查: http://localhost:8000/health")
        print("\n测试命令:")
        print("  python app.py test")
        print("\n" + "=" * 80 + "\n")

        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
