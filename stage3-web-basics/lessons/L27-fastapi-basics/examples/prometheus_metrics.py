"""

from __future__ import annotations

FastAPI Prometheus 指标 - prometheus-fastapi-instrumentator
============================================================

本模块展示 FastAPI + Prometheus 的指标暴露设计：
- HTTP 请求指标（请求数、延迟、错误率）
- 业务自定义指标
- /metrics 端点暴露
- Grafana 仪表盘

架构设计：
---------
1. prometheus-fastapi-instrumentator 自动注入
2. 自定义业务指标（订单数、用户注册）
3. Histogram/Summary/Counter/Gauge
4. /metrics 端点（Grafana/Prometheus 抓取）

对标：
-----
- 呼应 L31 监控告警（Prometheus + Grafana）
- 生产级可观测性：Metrics + Logs + Traces

作者：Python 3.13 全栈课程
"""

from __future__ import annotations

import asyncio
import contextlib
import random
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.metrics import Info

# ============================================================
# Prometheus 配置
# ============================================================


def setup_prometheus(app: FastAPI) -> Instrumentator:
    """
    配置 Prometheus 指标

    **核心特性**:
    - HTTP 请求自动指标
    - 自定义业务指标
    - /metrics 端点暴露
    """
    instrumentator = Instrumentator(
        should_group_status_codes=True,  # 按状态码分组
        should_ignore_untemplated=True,  # 忽略未模板化的路径
        should_respect_env_var=True,  # 尊重环境变量
        should_instrument_requests_inprogress=True,  # 追踪进行中的请求
        excluded_handlers=["/metrics", "/health"],  # 排除指标端点
        inprogress_name="http_requests_inprogress",  # 进行中请求指标名
        inprogress_labels=True,  # 添加标签
    )

    # 添加默认指标（请求数、延迟、响应大小）
    instrumentator.instrument(app)

    # 添加自定义指标
    instrumentator.add(
        Info(
            "custom_app_info",
            "应用自定义信息",
        ).requests(
            lambda: {
                "version": "1.0.0",
                "environment": "development",
            }
        )
    )

    # 暴露 /metrics 端点
    instrumentator.expose(app, endpoint="/metrics")

    return instrumentator


# ============================================================
# 自定义业务指标
# ============================================================

from prometheus_client import Counter, Histogram, Gauge

# 业务指标
# Counter：只增不减（请求数、错误数）
order_created_total = Counter(
    "order_created_total",
    "创建的订单总数",
    ["status"],  # status=success, failed
)

order_amount_histogram = Histogram(
    "order_amount_histogram",
    "订单金额分布",
    buckets=[10, 50, 100, 500, 1000, 5000, 10000],
)

active_users_gauge = Gauge(
    "active_users_gauge",
    "当前在线用户数",
)

# 缓存指标
cache_hits = Counter(
    "cache_hits_total",
    "缓存命中次数",
)

cache_misses = Counter(
    "cache_misses_total",
    "缓存未命中次数",
)

# 第三方 API 延迟
external_api_latency = Histogram(
    "external_api_latency_seconds",
    "第三方 API 延迟（秒）",
    ["service"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)


# ============================================================
# 业务逻辑（带指标埋点）
# ============================================================


async def call_external_api(service: str) -> dict:
    """
    模拟调用外部 API

    **指标埋点**:
    - 记录 API 延迟
    - 记录成功/失败
    """
    with external_api_latency.labels(service=service).time():
        # 模拟 API 调用
        await asyncio.sleep(random.uniform(0.01, 0.2))

        # 模拟失败（10% 概率）
        if random.random() < 0.1:
            raise Exception("API 调用失败")

        return {"status": "ok", "service": service}


# ============================================================
# 契约定义
# ============================================================


class OrderCreate(BaseModel):
    """订单创建请求"""

    product_id: Annotated[int, Field(gt=0, description="商品 ID")]
    quantity: Annotated[int, Field(gt=0, le=100, description="数量")]
    user_id: Annotated[int, Field(gt=0, description="用户 ID")]


class OrderResponse(BaseModel):
    """订单响应"""

    order_id: int
    product_id: int
    quantity: int
    user_id: int
    total_price: float
    status: str


# ============================================================
# 内存存储（演示用）
# ============================================================

orders_db: dict[int, dict] = {}
next_order_id = 1
products = {
    1: {"name": "iPhone", "price": 9999.0},
    2: {"name": "MacBook", "price": 19999.0},
    3: {"name": "AirPods", "price": 1999.0},
}


# ============================================================
# FastAPI 应用（带 Prometheus 指标）
# ============================================================


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001 FastAPI lifespan 协议要求保留 app 参数
    """应用生命周期管理"""
    # 模拟在线用户数
    active_users_gauge.set(100)

    # 定期更新在线用户数（模拟）
    async def update_users():
        while True:
            await asyncio.sleep(10)
            # 模拟用户数波动
            delta = random.randint(-10, 10)
            active_users_gauge.inc(delta)

    task = asyncio.create_task(update_users())
    yield
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task


app = FastAPI(
    title="Prometheus 指标 API",
    description="FastAPI + Prometheus 指标暴露示例",
    version="1.0.0",
    lifespan=lifespan,
)

# 配置 Prometheus
setup_prometheus(app)


# ============================================================
# API 路由（带指标埋点）
# ============================================================


@app.get("/", summary="欢迎页")
async def root() -> dict[str, str]:
    """欢迎页"""
    return {
        "message": "FastAPI Prometheus 指标 API",
        "metrics": "/metrics",
    }


@app.get("/health", summary="健康检查")
async def health_check() -> dict[str, str]:
    """
    健康检查端点

    **注意**: 此端点被排除在指标收集之外
    """
    return {"status": "healthy"}


@app.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    summary="创建订单",
)
async def create_order(order: OrderCreate) -> OrderResponse:
    """
    创建订单

    **指标埋点**:
    - 订单创建计数器
    - 订单金额直方图
    """
    global next_order_id

    try:
        # 获取商品信息
        product = products.get(order.product_id)
        if not product:
            order_created_total.labels(status="failed").inc()
            raise HTTPException(status_code=404, detail="商品不存在")

        # 计算总价
        total_price = product["price"] * order.quantity

        # 创建订单
        order_record = {
            "order_id": next_order_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "user_id": order.user_id,
            "total_price": total_price,
            "status": "created",
        }
        orders_db[next_order_id] = order_record
        next_order_id += 1

        # 指标埋点
        order_created_total.labels(status="success").inc()
        order_amount_histogram.observe(total_price)

        return OrderResponse(**order_record)

    except HTTPException:
        raise
    except Exception:
        order_created_total.labels(status="failed").inc()
        raise


@app.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    summary="获取订单",
)
async def get_order(order_id: Annotated[int, Path(gt=0)]) -> OrderResponse:
    """
    获取订单详情

    **缓存模拟**:
    - 模拟缓存命中/未命中
    """
    # 模拟缓存查找
    if random.random() < 0.7:  # 70% 命中
        cache_hits.inc()
    else:
        cache_misses.inc()

    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    return OrderResponse(**order)


@app.get("/products/{product_id}", summary="获取商品")
async def get_product(product_id: Annotated[int, Path(gt=0)]) -> dict:
    """
    获取商品信息

    **外部 API 调用**:
    - 记录 API 延迟
    """
    try:
        # 模拟调用外部 API
        await call_external_api("product_service")
        product = products.get(product_id)

        if not product:
            raise HTTPException(status_code=404, detail="商品不存在")

        return product

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 运行说明
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("FastAPI Prometheus 指标 API")
    print("=" * 80)
    print("\n核心特性:")
    print("  ✅ HTTP 请求自动指标")
    print("  ✅ 业务自定义指标（订单数、金额分布）")
    print("  ✅ 缓存命中率指标")
    print("  ✅ 第三方 API 延迟指标")
    print("\n端点:")
    print("  - API 文档: http://localhost:8000/docs")
    print("  - Prometheus 指标: http://localhost:8000/metrics")
    print("\nPromQL 示例:")
    print("  # 请求率")
    print("  rate(http_requests_total[5m])")
    print("  # 99 分位延迟")
    print("  histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))")
    print("  # 订单成功率")
    print("  rate(order_created_total{status='success'}[5m]) / rate(order_created_total[5m])")
    print("\n按 Ctrl+C 停止\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
