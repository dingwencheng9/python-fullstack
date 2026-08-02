"""Prometheus 指标收集中间件

自动记录所有 HTTP 请求的指标：
- 请求计数
- 延迟直方图
- 请求/响应大小
- 活跃请求数
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import override

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.metrics import (
    active_requests,
    http_request_duration_seconds,
    http_request_size_bytes,
    http_requests_total,
    http_response_size_bytes,
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Prometheus 指标收集中间件"""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    @override
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """处理请求并记录指标"""
        # 跳过 /metrics 端点本身（避免递归收集）
        if request.url.path == "/metrics":
            return await call_next(request)

        # 提取请求信息
        method = request.method
        path = self._normalize_path(request.url.path)

        # 记录请求大小
        request_size = int(request.headers.get("content-length", 0))
        http_request_size_bytes.labels(method=method, path=path).observe(request_size)

        # 记录活跃请求（进入）
        active_requests.labels(method=method, path=path).inc()

        # 记录请求开始时间
        start_time = time.perf_counter()

        try:
            # 执行请求
            response = await call_next(request)

            # 记录请求延迟
            duration = time.perf_counter() - start_time
            http_request_duration_seconds.labels(method=method, path=path).observe(duration)

            # 记录响应大小
            response_size = int(response.headers.get("content-length", 0))
            http_response_size_bytes.labels(method=method, path=path).observe(response_size)

            # 记录请求计数
            http_requests_total.labels(
                method=method, path=path, status_code=response.status_code
            ).inc()

            return response

        except Exception as exc:
            # 记录异常请求
            duration = time.perf_counter() - start_time
            http_request_duration_seconds.labels(method=method, path=path).observe(duration)
            http_requests_total.labels(method=method, path=path, status_code=500).inc()
            raise exc

        finally:
            # 记录活跃请求（退出）
            active_requests.labels(method=method, path=path).dec()

    @staticmethod
    def _normalize_path(path: str) -> str:
        """规范化路径（聚合动态参数）

        例如：/documents/123 → /documents/{id}
        """
        # 简单路径（无需规范化）
        if path in ("/", "/health", "/metrics", "/docs", "/openapi.json", "/redoc"):
            return path

        # 文档相关路径
        if path.startswith("/documents/"):
            parts = path.split("/")
            if len(parts) >= 3 and parts[2].isdigit():
                return "/documents/{id}"
            return "/documents"

        # Chat 路径
        if path.startswith("/chat"):
            return "/chat"

        # 其他路径保持原样
        return path
