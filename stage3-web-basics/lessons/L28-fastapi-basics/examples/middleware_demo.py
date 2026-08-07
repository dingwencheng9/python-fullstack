"""

from __future__ import annotations

FastAPI 中间件实战 - 请求拦截与响应处理
=========================================

本模块展示 FastAPI 中间件的设计与使用：
- 请求拦截（Authentication/CORS/Logging）
- 响应处理（Headers/CORS/Compression）
- 中间件顺序与依赖
- 生产级中间件实现

架构设计：
---------
1. 自定义中间件（请求 ID/日志/CORS）
2. 第三方中间件集成（RateLimit/Compression）
3. 中间件执行顺序
4. 依赖注入 vs 中间件

对标：
-----
- 呼应 L26 HTTP 协议（中间件链）
- 为 L34 FastAPI 安全奠基

作者：Python 3.13 全栈课程
"""

from __future__ import annotations

import time
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Security,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware

# ============================================================
# 中间件 1: 请求 ID 注入
# ============================================================


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    请求 ID 中间件

    **功能**:
    - 为每个请求生成唯一 ID
    - 注入到请求状态（request.state）
    - 添加到响应头（X-Request-ID）
    """

    async def dispatch(self, request: Request, call_next):
        # 生成请求 ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])

        # 存储到请求状态
        request.state.request_id = request_id

        # 记录开始时间
        start_time = time.time()

        # 调用下游
        response = await call_next(request)

        # 计算耗时
        elapsed = (time.time() - start_time) * 1000

        # 添加响应头
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = str(round(elapsed, 2))

        return response


# ============================================================
# 中间件 2: 安全头（Security Headers）
# ============================================================


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    安全头中间件

    **功能**:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY
    - Strict-Transport-Security: max-age=31536000
    - Content-Security-Policy: default-src 'self'
    """

    CSP = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://api.example.com;"

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # 添加安全头
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = self.CSP

        return response


# ============================================================
# 中间件 3: 请求日志
# ============================================================


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    请求日志中间件

    **功能**:
    - 记录请求详情
    - 记录响应状态
    - 记录处理耗时
    """

    def __init__(self, app, log_file: Path | None = None) -> None:
        super().__init__(app)
        self.log_file = log_file

    async def dispatch(self, request: Request, call_next):
        # 获取请求 ID
        request_id = getattr(request.state, "request_id", "unknown")

        # 记录请求
        log_entry = {
            "timestamp": time.time(),
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client": str(request.client.host) if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", ""),
        }

        # 调用下游
        response = await call_next(request)

        # 更新日志
        log_entry["status_code"] = response.status_code
        log_entry["process_time_ms"] = response.headers.get("X-Process-Time-Ms", "0")

        # 打印日志
        print(
            f"[{log_entry['timestamp']:.3f}] "
            f"{log_entry['method']} {log_entry['path']} "
            f"→ {log_entry['status_code']} "
            f"({log_entry['process_time_ms']}ms) "
            f"[{request_id}]"
        )

        return response


# ============================================================
# 中间件 4: 速率限制（简化版）
# ============================================================


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    速率限制中间件

    **功能**:
    - 基于 IP 的速率限制
    - 滑动窗口算法
    - 返回 429 Too Many Requests

    **生产建议**: 使用 Redis + Lua 脚本实现分布式限流
    """

    def __init__(
        self,
        app,
        max_requests: int = 100,
        window_seconds: int = 60,
    ) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        # 获取客户端 IP
        client_ip = request.client.host if request.client else "unknown"

        # 清理过期记录
        now = time.time()
        if client_ip in self.requests:
            self.requests[client_ip] = [ts for ts in self.requests[client_ip] if now - ts < self.window_seconds]
        else:
            self.requests[client_ip] = []

        # 检查限流
        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "TooManyRequests",
                    "message": f"速率限制: 每 {self.window_seconds} 秒最多 {self.max_requests} 请求",
                    "retry_after": self.window_seconds,
                },
                headers={
                    "Retry-After": str(self.window_seconds),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(now) + self.window_seconds),
                },
            )

        # 记录请求
        self.requests[client_ip].append(now)

        # 计算剩余配额
        remaining = self.max_requests - len(self.requests[client_ip])

        # 调用下游
        response = await call_next(request)

        # 添加限流头
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(now) + self.window_seconds)

        return response


# ============================================================
# API Key 认证（依赖注入方式）
# ============================================================


API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

# 模拟 API Keys
VALID_API_KEYS = {
    "dev-key-12345": {"user_id": 1, "name": "Developer", "tier": "pro"},
    "prod-key-67890": {"user_id": 2, "name": "Production", "tier": "enterprise"},
}


async def verify_api_key(api_key: Annotated[str | None, Security(API_KEY_HEADER)]) -> dict:
    """
    API Key 认证依赖

    **用法**:
    ```python
    @app.get("/protected")
    async def protected_route(user: dict = Depends(verify_api_key)):
        return {"user": user}
    ```
    """
    if api_key is None:
        raise HTTPException(
            status_code=401,
            headers={"WWW-Authenticate": "API-Key"},
            detail="缺少 API Key",
        )

    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            headers={"WWW-Authenticate": "API-Key"},
            detail="无效的 API Key",
        )

    return VALID_API_KEYS[api_key]


# ============================================================
# 契约定义
# ============================================================


class ItemCreate(BaseModel):
    """商品创建请求"""

    name: Annotated[str, Field(min_length=1, max_length=100, description="商品名称")]
    price: Annotated[float, Field(gt=0, description="商品价格")]


class ItemResponse(BaseModel):
    """商品响应"""

    id: int
    name: str
    price: float


# ============================================================
# 内存存储
# ============================================================

items_db: dict[int, dict] = {}
next_id = 1


# ============================================================
# FastAPI 应用（带多层中间件）
# ============================================================


app = FastAPI(
    title="中间件实战 API",
    description="FastAPI 中间件：请求 ID / 安全头 / 日志 / 限流",
    version="1.0.0",
)

# 添加中间件（注意：顺序是从下到上）
# 1. GZip 压缩（最后添加，最先执行）
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 2. CORS（跨域资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com", "https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 3. 速率限制
app.add_middleware(
    RateLimitMiddleware,
    max_requests=100,
    window_seconds=60,
)

# 4. 安全头
app.add_middleware(SecurityHeadersMiddleware)

# 5. 请求日志
app.add_middleware(RequestLoggingMiddleware)

# 6. 请求 ID（最先添加，最后执行）
app.add_middleware(RequestIDMiddleware)


# ============================================================
# API 路由
# ============================================================


@app.get("/", summary="欢迎页")
async def root(request: Request) -> dict:
    """
    欢迎页

    **响应头**:
    - X-Request-ID: 请求唯一标识
    - X-Process-Time-Ms: 处理耗时
    - 安全相关头
    """
    return {
        "message": "FastAPI 中间件实战 API",
        "request_id": request.state.request_id,
        "features": [
            "X-Request-ID 注入",
            "Security Headers",
            "Request Logging",
            "Rate Limiting",
            "CORS",
            "GZip Compression",
        ],
    }


@app.get("/public", summary="公开端点")
async def public_endpoint() -> dict:
    """
    公开端点

    **无需认证**
    """
    return {"message": "公开数据", "data": [1, 2, 3]}


@app.get(
    "/protected",
    summary="受保护端点",
)
async def protected_endpoint(
    user: Annotated[dict, Security(verify_api_key)],
) -> dict:
    """
    受保护端点

    **认证方式**: API Key Header (X-API-Key)

    **用法**:
    ```bash
    curl -H "X-API-Key: dev-key-12345" http://localhost:8000/protected
    ```
    """
    return {
        "message": "受保护数据",
        "user": user,
        "data": {"secret": "API 密钥有效"},
    }


@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=201,
    summary="创建商品（需认证）",
)
async def create_item(
    item: ItemCreate,
    user: Annotated[dict, Security(verify_api_key)],
) -> ItemResponse:
    """
    创建商品

    **认证**: API Key Header
    """
    global next_id

    new_item = {
        "id": next_id,
        "name": item.name,
        "price": item.price,
    }
    items_db[next_id] = new_item
    next_id += 1

    return ItemResponse(**new_item)


@app.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="获取商品",
)
async def get_item(item_id: int) -> ItemResponse:
    """
    获取商品详情

    **限流**: 60 秒内最多 100 请求
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="商品不存在")

    return ItemResponse(**items_db[item_id])


@app.get("/health", summary="健康检查")
async def health_check() -> dict:
    """
    健康检查

    **无认证**
    """
    return {"status": "healthy"}


# ============================================================
# 运行说明
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("FastAPI 中间件实战 API")
    print("=" * 80)
    print("\n中间件顺序（从上到下执行）:")
    print("  1. GZip 压缩（响应压缩）")
    print("  2. CORS（跨域资源共享）")
    print("  3. Rate Limiting（速率限制）")
    print("  4. Security Headers（安全头）")
    print("  5. Request Logging（日志）")
    print("  6. Request ID（请求 ID）")
    print("\n测试命令:")
    print("  # 公开端点")
    print("  curl http://localhost:8000/public")
    print("\n  # 受保护端点（需 API Key）")
    print("  curl -H 'X-API-Key: dev-key-12345' http://localhost:8000/protected")
    print("\n  # 查看响应头")
    print("  curl -I http://localhost:8000/")
    print("\n  # 速率限制测试（100+ 请求）")
    print("  for i in {1..110}; do curl -s http://localhost:8000/public -o /dev/null; done")
    print("\n按 Ctrl+C 停止\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
