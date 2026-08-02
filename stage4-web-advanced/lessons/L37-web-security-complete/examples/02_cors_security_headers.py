"""CORS 精细配置与安全响应头

本模块演示 FastAPI 中 CORS 中间件配置与安全响应头的完整实现。

参考: lesson.md 第六章

示例:
    $ uv run python examples/02_cors_security_headers.py
    $ curl -I http://localhost:8000/  # 查看安全响应头
    $ curl -X OPTIONS http://localhost:8000/api/items \\
        -H "Origin: https://app.example.com" \\
        -H "Access-Control-Request-Method: GET" \\
        -v
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ==============================================================================
# 第六章: CORS 精细配置
# ==============================================================================

# --------------------------------------------------------------------------
# 6.1 CORS 基础配置
# --------------------------------------------------------------------------

# 场景 1: 生产环境推荐配置（精确白名单）
ALLOWED_ORIGINS = ["https://app.example.com", "https://admin.example.com"]
CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS = ["Authorization", "Content-Type", "X-Request-ID"]
EXPOSE_HEADERS = ["X-Request-ID", "X-RateLimit-Remaining"]

# 场景 2: 开发环境配置（宽松模式）
# 仅开发环境使用，生产环境禁用
CORS_DEV_ORIGINS = "*"
CORS_DEV_METHODS = "*"
CORS_DEV_HEADERS = "*"

# 场景 3: 仅允许 GET/POST（最严格）
CORS_STRICT_ORIGIN = "https://app.example.com"
CORS_STRICT_METHODS = ["GET", "POST"]


# --------------------------------------------------------------------------
# 6.2 安全响应头中间件（@app.middleware 装饰器模式）
# --------------------------------------------------------------------------


# CSP 配置集合
class CSP:
    """CSP 配置集合"""

    # 基础 CSP: 仅允许同源
    BASIC = "default-src 'self'"

    # 详细 CSP: 允许特定外部资源
    DETAILED = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net; "
        "style-src 'self' https://fonts.googleapis.com; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://fonts.gstatic.com; "
        "connect-src 'self' https://api.example.com; "
        "frame-ancestors 'none';"
    )

    # 严格 CSP: 禁止所有外部资源
    STRICT = "default-src 'none'; script-src 'none'; style-src 'self'; img-src 'self'; frame-ancestors 'none';"


# --------------------------------------------------------------------------
# 6.3 完整 FastAPI 应用示例
# --------------------------------------------------------------------------

app = FastAPI(
    title="CORS & Security Headers Demo",
    version="1.0.0",
)

# 1. 添加 CORS 中间件
# 注意：此处直接内联参数，避免 dict 解包导致的类型推断问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com", "https://admin.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID", "X-RateLimit-Remaining"],
    max_age=3600,
)


# 2. 安全响应头中间件
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next: Any) -> Any:
    """安全响应头中间件

    添加以下安全响应头:
    - Strict-Transport-Security (HSTS)
    - X-Frame-Options
    - X-Content-Type-Options
    - X-XSS-Protection
    - Referrer-Policy
    - Permissions-Policy
    - Content-Security-Policy
    """
    response = await call_next(request)

    # HSTS: 仅对 HTTPS 响应添加
    # 浏览器在 1 年内强制使用 HTTPS 访问
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

    # X-Frame-Options: 防止点击劫持
    # DENY = 完全禁止嵌入
    # SAMEORIGIN = 仅允许同源嵌入
    response.headers["X-Frame-Options"] = "DENY"

    # X-Content-Type-Options: 防止 MIME 类型嗅探
    response.headers["X-Content-Type-Options"] = "nosniff"

    # X-XSS-Protection: XSS 过滤器（现代浏览器已内置，仅兼容性保留）
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Referrer-Policy: 控制 Referer 头发送策略
    # strict-origin-when-cross-origin: 同源完整 URL，跨域仅发送 origin
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Permissions-Policy: 禁用不必要的浏览器特性
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), payment=()"

    # Content-Security-Policy: 防止 XSS 攻击
    # default-src 'self': 仅允许同源
    # script-src 'self': 仅允许同源脚本
    # style-src 'self' 'unsafe-inline': 允许内联样式（某些框架需要）
    # img-src 'self' data: https:: 允许图片和数据 URI
    # frame-ancestors 'none': 禁止被 iframe 嵌入
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )

    return response


# 3. 请求 ID 中间件
@app.middleware("http")
async def request_id_middleware(request: Request, call_next: Any) -> Any:
    """请求 ID 中间件

    为每个请求分配唯一 ID，便于日志追踪和问题排查。
    支持通过 X-Request-ID 请求头传递已有 ID（用于分布式追踪）。
    """
    # 优先使用请求头中的 X-Request-ID（用于分布式追踪）
    # 否则生成新的 UUID
    request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex)

    # 将 request_id 存入 request state 供后续使用
    request.state.request_id = request_id

    response = await call_next(request)

    # 在响应头中返回 request_id
    response.headers["X-Request-ID"] = request_id

    return response


# --------------------------------------------------------------------------
# 路由定义
# --------------------------------------------------------------------------


@app.get("/")
async def root() -> dict[str, str]:
    """首页"""
    return {
        "message": "欢迎使用 CORS & Security Headers 演示服务器",
        "docs": "/docs",
    }


@app.get("/api/items")
async def list_items() -> dict[str, list[str]]:
    """获取列表（支持 CORS）"""
    return {"items": ["item1", "item2", "item3"]}


@app.post("/api/items")
async def create_item(item: dict[str, object]) -> dict[str, object]:
    """创建条目（支持 CORS）"""
    return {"created": item}


@app.get("/headers")
async def show_headers(request: Request) -> dict[str, object]:
    """显示当前请求的响应头（用于调试）"""
    return {"request_id": getattr(request.state, "request_id", None)}


@app.get("/cors-demo")
async def cors_demo(request: Request) -> dict[str, Any]:
    """CORS 演示端点

    返回请求的 Origin 和当前配置的允许来源，
    便于测试 CORS 配置是否正确。
    """
    origin = request.headers.get("origin", "无")
    allowed_origins = ["https://app.example.com", "https://admin.example.com"]
    return {
        "origin": origin,
        "allowed_origins": ", ".join(allowed_origins),
        "is_allowed": origin in allowed_origins,
    }


# --------------------------------------------------------------------------
# 预检请求处理
# --------------------------------------------------------------------------

# FastAPI 的 CORS 中间件会自动处理 OPTIONS 预检请求，
# 但如果需要自定义预检处理逻辑，可以添加以下路由:


@app.options("/api/items")
async def options_items() -> JSONResponse:
    """预检请求处理

    FastAPI CORS 中间件会自动返回正确的 CORS 响应头，
    此路由仅用于演示目的。
    """
    return JSONResponse(
        content={"message": "OK"},
        status_code=200,
    )


# --------------------------------------------------------------------------
# 独立中间件类（BaseHTTPMiddleware 模式）
# --------------------------------------------------------------------------

# 除了 @app.middleware 装饰器，还可以使用类方式定义中间件：
# from starlette.middleware.base import BaseHTTPMiddleware
#
# class SecurityHeadersMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         response = await call_next(request)
#         response.headers["X-Frame-Options"] = "DENY"
#         return response
#
# app.add_middleware(SecurityHeadersMiddleware)
#
# 推荐使用 @app.middleware 装饰器方式，因为：
# 1. 类型注解更简单
# 2. 代码更直观
# 3. 中间件顺序更清晰


# --------------------------------------------------------------------------
# 动态 CORS 配置（基于数据库）
# --------------------------------------------------------------------------


async def get_allowed_origins() -> list[str]:
    """从数据库或配置中心获取允许的 CORS 源

    这是一个模拟函数，实际项目中应从数据库或 Redis 读取。
    """
    return [
        "https://app.example.com",
        "https://admin.example.com",
    ]


@app.middleware("http")
async def dynamic_cors_middleware(request: Request, call_next: Any) -> Any:
    """动态 CORS 中间件（基于数据库配置）

    适用场景：
    - 需要在运行时动态调整允许的域名
    - 允许多租户场景下各租户配置自己的域名
    """
    origin = request.headers.get("origin", "")
    allowed_origins = await get_allowed_origins()

    response = await call_next(request)

    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"

    return response


# --------------------------------------------------------------------------
# 运行入口
# --------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("CORS & Security Headers Demo Server")
    print("  访问 http://localhost:8000/docs 查看 API 文档")
    print("=" * 60 + "\n")

    uvicorn.run(
        "examples.02_cors_security_headers:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
