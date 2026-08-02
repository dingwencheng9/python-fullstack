# mypy: disable-error-code="untyped-decorator"
"""AI Fullstack Capstone FastAPI 应用。

from __future__ import annotations

注：FastAPI 装饰器在 mypy strict 下被视为 untyped（上游已知问题），
文件级关闭 ``untyped-decorator``，其他 strict 检查保留。
"""

from __future__ import annotations

import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from app.exceptions import register_exception_handlers
from app.metrics import app_start_time, get_metrics_content
from app.middleware import PrometheusMiddleware
from app.routes import chat, documents, health

TEMPLATE_DIR = Path(__file__).parent / "templates"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """应用生命周期管理：启动和关闭事件。

    启动时记录应用启动时间，关闭时清理所有缓存的 RAG 服务。

    ✅ 优雅关闭：
    1. 清理所有 RAG 服务缓存（释放向量和文档）
    2. 关闭所有 Embedder 的 ThreadPoolExecutor
    3. 确保在收到 K8s SIGTERM 信号时线程池能优雅退场
    """
    # 启动事件
    app_start_time.set(time.time())
    print("🚀 AI Fullstack Capstone 应用启动")

    yield  # 应用运行期间

    # 关闭事件
    print("🛑 应用关闭，清理资源...")

    # 清理 RAG 缓存（包括关闭 ThreadPoolExecutor）
    documents.cleanup_rag_cache()

    print("✅ 资源清理完成，线程池已优雅关闭")


app = FastAPI(title="AI Fullstack Capstone", lifespan=lifespan)
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# 注册 Prometheus 中间件
app.add_middleware(PrometheusMiddleware)

# 注册全局异常处理器
register_exception_handlers(app)

app.include_router(health.router)
app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/metrics")
async def metrics() -> Response:
    """Prometheus 指标端点"""
    content, content_type = get_metrics_content()
    return Response(content=content, media_type=content_type)
