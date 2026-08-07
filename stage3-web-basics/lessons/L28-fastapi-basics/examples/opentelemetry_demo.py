"""

from __future__ import annotations

FastAPI 无侵入式可观测性 - OpenTelemetry
=======================================

本模块展示 FastAPI + OpenTelemetry 的可观测性设计：
- 两行代码注入全局追踪
- 手动 Span 追踪业务逻辑
- 分布式追踪（Trace ID 传播）
- 告别 print() 调试

架构设计：
---------
1. 自动注入（FastAPIInstrumentor）
2. 手动 Span（业务逻辑追踪）
3. 结构化日志（structlog）
4. Trace 导出（Jaeger/OTLP）

对标：
-----
- 粉碎旧 Web 模块的 print() 调试（488 次）
- 生产级可观测性三支柱：Metrics + Logs + Traces

作者：Python 3.13 全栈课程
"""

import asyncio
import time
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

# OpenTelemetry 核心库
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pydantic import BaseModel, Field

# ============================================================
# OpenTelemetry 配置（生产级）
# ============================================================


def setup_telemetry(service_name: str = "fastapi-service") -> None:
    """
    配置 OpenTelemetry

    **两行代码注入全局追踪**：
    1. 创建 TracerProvider
    2. FastAPIInstrumentor.instrument(app)

    **导出器**:
    - 开发: Console Exporter（终端输出）
    - 生产: OTLP Exporter（Jaeger/Grafana Tempo）
    """
    # 创建 Resource（标识服务）
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": "1.0.0",
            "deployment.environment": "development",
        }
    )

    # 创建 TracerProvider
    provider = TracerProvider(resource=resource)

    # 配置导出器（生产环境使用 OTLP）
    # exporter = OTLPSpanExporter(endpoint="http://localhost:4317")

    # 开发环境：控制台导出器
    from opentelemetry.sdk.trace.export import ConsoleSpanExporter

    exporter = ConsoleSpanExporter()

    # 批量处理器（性能优化）
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    # 设置全局 TracerProvider
    trace.set_tracer_provider(provider)

    print("✅ OpenTelemetry 已配置")
    print(f"   服务名: {service_name}")
    print("   导出器: ConsoleSpanExporter（开发模式）")
    print("   生产环境: 替换为 OTLPSpanExporter\n")


# ============================================================
# 契约定义
# ============================================================


class OrderCreate(BaseModel):
    """订单创建请求"""

    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=100)
    user_id: int = Field(gt=0)


class OrderResponse(BaseModel):
    """订单响应"""

    order_id: int
    product_id: int
    quantity: int
    user_id: int
    total_price: float
    status: str


# ============================================================
# 业务逻辑（带手动 Span）
# ============================================================

# 获取 Tracer（每个模块一个）
tracer = trace.get_tracer(__name__)


async def validate_product(product_id: int) -> dict[str, float]:
    """
    验证产品库存和价格

    **手动 Span**:
    - 追踪业务逻辑执行时间
    - 记录关键属性（product_id）
    - 记录事件（库存不足）
    """
    # 创建手动 Span
    with tracer.start_as_current_span("validate_product") as span:
        # 记录 Span 属性
        span.set_attribute("product.id", product_id)

        # 模拟数据库查询
        await asyncio.sleep(0.05)

        # 模拟产品数据
        product = {
            "id": product_id,
            "name": f"Product {product_id}",
            "price": 99.99 + product_id,
            "stock": 50,
        }

        # 记录事件
        span.add_event(
            "product_validated",
            {
                "product.name": product["name"],
                "product.stock": product["stock"],
            },
        )

        if product["stock"] < 1:
            # 记录错误
            span.set_status(trace.Status(trace.StatusCode.ERROR, "库存不足"))
            span.record_exception(ValueError("库存不足"))
            raise HTTPException(status_code=400, detail="库存不足")

        return product


async def check_user_credit(user_id: int, amount: float) -> bool:
    """
    检查用户信用额度

    **手动 Span**:
    - 追踪外部服务调用
    - 记录调用结果
    """
    with tracer.start_as_current_span("check_user_credit") as span:
        span.set_attribute("user.id", user_id)
        span.set_attribute("credit.amount", amount)

        # 模拟外部信用检查 API 调用
        await asyncio.sleep(0.08)

        # 模拟结果
        has_credit = amount < 10000.0

        span.set_attribute("credit.approved", has_credit)

        if has_credit:
            span.add_event("credit_approved")
        else:
            span.add_event("credit_rejected")
            span.set_status(trace.Status(trace.StatusCode.ERROR, "信用额度不足"))

        return has_credit


async def create_order_record(order_data: dict) -> int:  # noqa: ARG001  教学示例：mock 实现，order_data 未使用
    """
    创建订单记录

    **手动 Span**:
    - 追踪数据库写入
    - 记录订单 ID
    """
    with tracer.start_as_current_span("create_order_record") as span:
        # 模拟数据库插入
        await asyncio.sleep(0.03)

        # 生成订单 ID
        order_id = int(time.time() * 1000) % 1000000

        span.set_attribute("order.id", order_id)
        span.add_event("order_created")

        return order_id


async def send_confirmation_email(user_id: int, order_id: int) -> None:
    """
    发送确认邮件

    **手动 Span**:
    - 追踪邮件服务调用
    - fire-and-forget（不阻塞主流程）
    """
    with tracer.start_as_current_span("send_confirmation_email") as span:
        span.set_attribute("user.id", user_id)
        span.set_attribute("order.id", order_id)

        # 模拟邮件服务 API 调用
        await asyncio.sleep(0.1)

        span.add_event("email_sent")


# ============================================================
# FastAPI 应用（带可观测性）
# ============================================================


# 生命周期：启动时配置 OpenTelemetry
@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001  FastAPI lifespan 协议要求保留 app 参数
    """应用生命周期管理"""
    # 启动时配置 OpenTelemetry
    setup_telemetry(service_name="order-api")
    yield
    # 关闭时清理（可选）


app = FastAPI(
    title="可观测性 API",
    description="FastAPI + OpenTelemetry 示例",
    version="1.0.0",
    lifespan=lifespan,
)


# ✅ 两行代码注入全局追踪（第 2 步）
FastAPIInstrumentor.instrument_app(app)


@app.get("/")
async def root() -> dict[str, str]:
    """
    根路径

    **自动追踪**:
    - FastAPIInstrumentor 自动创建 Span
    - 记录 HTTP 方法、路径、状态码
    """
    return {
        "message": "FastAPI 可观测性 API",
        "features": "OpenTelemetry + 自动追踪",
    }


@app.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    summary="创建订单",
    description="创建订单（完整的分布式追踪）",
)
async def create_order(order: OrderCreate) -> OrderResponse:
    """
    创建订单（完整的业务逻辑追踪）

    **Trace 结构**:
    ```
    POST /orders [auto span]
    ├── validate_product [manual span]
    ├── check_user_credit [manual span]
    ├── create_order_record [manual span]
    └── send_confirmation_email [manual span]
    ```

    **可观测性特性**:
    - 自动追踪 HTTP 请求（FastAPIInstrumentor）
    - 手动追踪业务逻辑（tracer.start_as_current_span）
    - 记录关键属性和事件
    - 错误自动关联到 Span
    """
    # 获取当前 Span（自动注入的）
    current_span = trace.get_current_span()
    current_span.set_attribute("order.product_id", order.product_id)
    current_span.set_attribute("order.quantity", order.quantity)
    current_span.set_attribute("order.user_id", order.user_id)

    # 步骤 1: 验证产品
    product = await validate_product(order.product_id)

    # 步骤 2: 计算总价
    total_price = product["price"] * order.quantity
    current_span.set_attribute("order.total_price", total_price)

    # 步骤 3: 检查用户信用
    has_credit = await check_user_credit(order.user_id, total_price)
    if not has_credit:
        raise HTTPException(status_code=402, detail="信用额度不足")

    # 步骤 4: 创建订单记录
    order_id = await create_order_record(
        {
            "product_id": order.product_id,
            "quantity": order.quantity,
            "user_id": order.user_id,
            "total_price": total_price,
        }
    )

    # 步骤 5: 发送确认邮件（异步，不阻塞）
    asyncio.create_task(send_confirmation_email(order.user_id, order_id))

    # 记录成功事件
    current_span.add_event(
        "order_completed",
        {
            "order.id": order_id,
        },
    )

    return OrderResponse(
        order_id=order_id,
        product_id=order.product_id,
        quantity=order.quantity,
        user_id=order.user_id,
        total_price=total_price,
        status="created",
    )


@app.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    summary="获取订单详情",
)
async def get_order(order_id: Annotated[int, Path(gt=0)]) -> OrderResponse:
    """
    获取订单详情

    **自动追踪**:
    - HTTP 请求自动创建 Span
    - 包含路径参数（order_id）
    """
    # 手动追踪数据库查询
    with tracer.start_as_current_span("get_order_from_db") as span:
        span.set_attribute("order.id", order_id)

        # 模拟数据库查询
        await asyncio.sleep(0.02)

        # 模拟订单数据
        return OrderResponse(
            order_id=order_id,
            product_id=1,
            quantity=2,
            user_id=100,
            total_price=199.98,
            status="completed",
        )


@app.get(
    "/health",
    summary="健康检查",
    description="Kubernetes 健康探针端点",
)
async def health_check() -> dict[str, str]:
    """
    健康检查端点

    **可观测性**:
    - 不记录到 Trace（高频调用）
    - 可配置 exclude_urls 排除
    """
    return {"status": "healthy"}


# ============================================================
# 运行说明
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("FastAPI 可观测性 API")
    print("=" * 80)
    print("\n核心特性:")
    print("  ✅ OpenTelemetry 自动追踪")
    print("  ✅ 手动 Span 业务逻辑追踪")
    print("  ✅ 分布式追踪（Trace ID 传播）")
    print("  ✅ 告别 print() 调试")
    print("\n启动服务器...")
    print("  - API 文档: http://localhost:8000/docs")
    print("\n示例请求:")
    print("  curl -X POST http://localhost:8000/orders \\")
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"product_id": 1, "quantity": 2, "user_id": 100}\'')
    print("\n查看 Trace:")
    print("  - 终端输出: ConsoleSpanExporter")
    print("  - 生产环境: Jaeger UI (http://localhost:16686)")
    print("\n按 Ctrl+C 停止\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
