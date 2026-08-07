"""练习 2 参考答案：指标端点。

from __future__ import annotations

实现思路：
- 用一个 ``Metrics`` 数据类按 ``(method, path)`` 维度累计计数和总耗时
- 用 FastAPI ``BaseHTTPMiddleware`` 中间件拦截每个请求，记录前后时间差
- ``/metrics`` 端点把累计数据序列化为 JSON

教学简化：纯 Python dict 即可，不引入 prometheus_client。
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from starlette.requests import Request
    from starlette.responses import Response


@dataclass
class Metrics:
    """单维度（method, path）的指标聚合。"""

    count: int = 0
    total_seconds: float = 0.0

    def record(self, elapsed: float) -> None:
        self.count += 1
        self.total_seconds += elapsed

    @property
    def avg_seconds(self) -> float:
        return self.total_seconds / self.count if self.count else 0.0


@dataclass
class MetricsRegistry:
    """按 (method, path) 维度收集请求计数和耗时。"""

    by_route: dict[tuple[str, str], Metrics] = field(default_factory=lambda: defaultdict(Metrics))

    def record(self, method: str, path: str, elapsed: float) -> None:
        self.by_route[(method, path)].record(elapsed)

    def snapshot(self) -> dict[str, dict[str, float | int]]:
        return {
            f"{method} {path}": {
                "count": metrics.count,
                "total_seconds": round(metrics.total_seconds, 6),
                "avg_seconds": round(metrics.avg_seconds, 6),
            }
            for (method, path), metrics in self.by_route.items()
        }


class MetricsMiddleware(BaseHTTPMiddleware):
    """记录每个请求的方法、路径、耗时。"""

    def __init__(self, app: FastAPI, registry: MetricsRegistry) -> None:
        super().__init__(app)
        self._registry = registry

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        # 排除 /metrics 自身，避免观察者效应污染数据
        if request.url.path == "/metrics":
            return await call_next(request)
        started = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - started
        self._registry.record(request.method, request.url.path, elapsed)
        return response


def add_metrics(app: FastAPI) -> MetricsRegistry:
    """在 ``app`` 上注册 metrics 中间件和 /metrics 端点。

    返回 ``MetricsRegistry`` 以便测试时直接访问累计数据。
    """
    registry = MetricsRegistry()
    app.add_middleware(MetricsMiddleware, registry=registry)

    @app.get("/metrics")
    async def metrics() -> dict[str, dict[str, float | int]]:
        return registry.snapshot()

    return registry


if __name__ == "__main__":
    from core.settings import get_settings

    settings = get_settings()
    import uvicorn

    demo = FastAPI(title="Metrics demo")

    @demo.get("/")
    async def root() -> dict[str, str]:
        return {"status": "ok"}

    add_metrics(demo)
    uvicorn.run(
        demo,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
    )
