"""

from __future__ import annotations

FastAPI 异步全链路 - TaskGroup 并发聚合
======================================

本模块展示 FastAPI 异步全链路设计：
- 异步数据库查询（SQLAlchemy 2.0 async）
- 异步外部 API 调用（httpx async）
- TaskGroup 结构化并发（Python 3.11+）
- 完整的错误处理

架构设计：
---------
1. 异步数据库层（模拟 SQLAlchemy 2.0）
2. 异步外部服务调用
3. TaskGroup 并发 I/O 聚合
4. 结构化错误处理（ExceptionGroup）

对标：
-----
- 呼应 L06 异步编程（TaskGroup + ExceptionGroup）
- 呼应 L07 高阶流控（AsyncGenerator + 流式处理）

作者：Python 3.13 全栈课程
"""

import asyncio
import random
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

# ============================================================
# 契约定义
# ============================================================


class ProductBase(BaseModel):
    """产品基础模型"""

    name: str = Field(min_length=1, max_length=200)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductDetail(ProductBase):
    """产品详情（含外部数据）"""

    id: int
    description: str
    created_at: datetime

    # 外部服务数据
    reviews_count: int = Field(description="评论数（外部服务）")
    avg_rating: float = Field(ge=0, le=5, description="平均评分（外部服务）")
    related_products: list[int] = Field(description="相关产品 ID（外部服务）")


class AggregatedResponse(BaseModel):
    """聚合响应（多数据源）"""

    product: ProductDetail
    metadata: dict[str, str] = Field(description="元数据")
    processing_time_ms: float = Field(description="处理耗时（毫秒）")


# ============================================================
# 模拟异步数据库层（SQLAlchemy 2.0 风格）
# ============================================================


@dataclass
class Product:
    """数据库模型"""

    id: int
    name: str
    price: float
    stock: int
    description: str
    created_at: datetime


# 模拟数据库
products_db: dict[int, Product] = {
    1: Product(
        id=1,
        name="MacBook Pro M3",
        price=15999.0,
        stock=50,
        description="Apple 最新款笔记本",
        created_at=datetime(2024, 11, 1),
    ),
    2: Product(
        id=2,
        name="iPhone 15 Pro",
        price=7999.0,
        stock=200,
        description="Apple 旗舰手机",
        created_at=datetime(2024, 9, 15),
    ),
}


async def get_product_from_db(product_id: int) -> Product | None:
    """
    异步数据库查询（模拟 SQLAlchemy 2.0）

    实际代码：
    async with async_session() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()
    """
    # 模拟数据库查询延迟（50-100ms）
    await asyncio.sleep(0.05 + random.random() * 0.05)
    return products_db.get(product_id)


# ============================================================
# 模拟外部微服务调用
# ============================================================


async def get_product_reviews(product_id: int) -> dict[str, int | float]:
    """
    异步外部服务：获取产品评论统计

    模拟调用评论服务 API
    """
    # 模拟网络延迟（100-200ms）
    await asyncio.sleep(0.1 + random.random() * 0.1)

    # 模拟 HTTP 请求
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(f"https://reviews-api/products/{product_id}")
    #     return response.json()

    # 模拟返回数据
    return {
        "reviews_count": 127 + product_id * 10,
        "avg_rating": 4.2 + (product_id % 8) * 0.1,
    }


async def get_related_products(product_id: int) -> list[int]:
    """
    异步外部服务：获取相关产品推荐

    模拟调用推荐服务 API
    """
    # 模拟网络延迟（80-150ms）
    await asyncio.sleep(0.08 + random.random() * 0.07)

    # 模拟推荐算法返回
    related = [(product_id + i) % 10 + 1 for i in range(1, 4)]
    return [p for p in related if p != product_id]


async def log_product_access(product_id: int, user_ip: str) -> None:
    """
    异步外部服务：记录产品访问日志

    模拟调用日志服务 API（fire-and-forget）
    """
    # 模拟网络延迟（30-50ms）
    await asyncio.sleep(0.03 + random.random() * 0.02)

    # 实际代码：发送到 Kafka/RabbitMQ
    print(f"📝 日志: 用户 {user_ip} 访问产品 {product_id}")


# ============================================================
# FastAPI 应用
# ============================================================

app = FastAPI(
    title="异步全链路 API",
    description="FastAPI + TaskGroup 并发聚合示例",
    version="1.0.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    """根路径"""
    return {
        "message": "FastAPI 异步全链路 API",
        "features": "TaskGroup + 并发 I/O",
    }


@app.get(
    "/products/{product_id}",
    response_model=AggregatedResponse,
    summary="获取产品详情（聚合）",
    description="并发查询多个数据源，使用 TaskGroup 聚合结果",
)
async def get_product_detail(
    product_id: Annotated[int, Path(gt=0, description="产品 ID")],
) -> AggregatedResponse:
    """
    获取产品详情（异步全链路 + TaskGroup 并发）

    **数据源**:
    1. 数据库：产品基础信息
    2. 评论服务：评论数 + 平均评分
    3. 推荐服务：相关产品列表

    **并发策略**:
    - 使用 TaskGroup 并发查询 3 个数据源
    - 结构化错误处理（ExceptionGroup）
    - 总耗时 = max(单个查询耗时)，非 sum
    """
    start_time = asyncio.get_event_loop().time()

    try:
        # ✅ 使用 TaskGroup 并发查询（Python 3.11+）
        async with asyncio.TaskGroup() as tg:
            # 任务 1: 数据库查询
            task_db = tg.create_task(get_product_from_db(product_id), name="db_query")

            # 任务 2: 评论服务
            task_reviews = tg.create_task(get_product_reviews(product_id), name="reviews_service")

            # 任务 3: 推荐服务
            task_related = tg.create_task(get_related_products(product_id), name="recommendation_service")

            # 任务 4: 日志服务（fire-and-forget）
            tg.create_task(log_product_access(product_id, "127.0.0.1"), name="logging_service")

        # TaskGroup 会等待所有任务完成
        # 如果任何任务失败，会抛出 ExceptionGroup

        # 获取结果
        product = task_db.result()
        reviews = task_reviews.result()
        related = task_related.result()

        # 检查产品是否存在
        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"产品 ID {product_id} 不存在",
            )

        # 构建聚合响应
        product_detail = ProductDetail(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            description=product.description,
            created_at=product.created_at,
            reviews_count=reviews["reviews_count"],
            avg_rating=reviews["avg_rating"],
            related_products=related,
        )

        # 计算处理时间
        processing_time = (asyncio.get_event_loop().time() - start_time) * 1000

        return AggregatedResponse(
            product=product_detail,
            metadata={
                "sources": "database + reviews_api + recommendation_api",
                "concurrent_tasks": "3",
                "concurrency_model": "TaskGroup",
            },
            processing_time_ms=round(processing_time, 2),
        )

    except* HTTPException as eg:
        # HTTPException 应该原样向外抛（让 FastAPI 渲染对应状态码），
        # 不能被下面的 ExceptionGroup 包成 500。
        # ExceptionGroup 中可能包含多个 HTTPException，取第一个抛出。
        raise eg.exceptions[0] from None
    except* Exception as eg:
        # ✅ 其余异常做结构化错误处理（ExceptionGroup）
        # except* 语法（Python 3.11+）

        # 提取所有异常
        errors = [str(exc) for exc in eg.exceptions]

        raise HTTPException(
            status_code=500,
            detail={
                "error": "ServiceError",
                "message": "部分服务调用失败",
                "failed_tasks": errors,
            },
        ) from eg


@app.get(
    "/products/{product_id}/stream",
    summary="流式获取产品详情",
    description="使用异步生成器流式返回数据",
)
async def stream_product_detail(product_id: Annotated[int, Path(gt=0, description="产品 ID")]):
    """
    流式返回产品详情（呼应 L07 高阶流控）

    **流式响应**:
    - 实时返回每个数据源的结果
    - 客户端无需等待所有数据源完成
    - 降低首字节时间（TTFB）
    """
    import json

    from fastapi.responses import StreamingResponse

    async def generate_stream():
        """异步生成器：流式产生数据"""

        # 第 1 块：数据库数据
        product = await get_product_from_db(product_id)
        if product:
            yield (
                json.dumps(
                    {
                        "source": "database",
                        "data": {
                            "id": product.id,
                            "name": product.name,
                            "price": product.price,
                        },
                    }
                )
                + "\n"
            )

        # 第 2 块：评论数据
        reviews = await get_product_reviews(product_id)
        yield (
            json.dumps(
                {
                    "source": "reviews",
                    "data": reviews,
                }
            )
            + "\n"
        )

        # 第 3 块：推荐数据
        related = await get_related_products(product_id)
        yield (
            json.dumps(
                {
                    "source": "recommendations",
                    "data": {"related_products": related},
                }
            )
            + "\n"
        )

    return StreamingResponse(
        generate_stream(),
        media_type="application/x-ndjson",  # Newline Delimited JSON
    )


# ============================================================
# 性能对比：串行 vs 并发
# ============================================================


@app.get(
    "/products/{product_id}/serial",
    summary="串行获取（性能对比）",
    description="串行查询数据源（慢）",
)
async def get_product_serial(product_id: Annotated[int, Path(gt=0)]) -> dict[str, Any]:
    """
    串行查询（性能对比）

    **问题**: 总耗时 = sum(单个查询耗时)
    """
    start_time = asyncio.get_event_loop().time()

    # ❌ 串行查询（慢）
    await get_product_from_db(product_id)
    await get_product_reviews(product_id)
    await get_related_products(product_id)

    processing_time = (asyncio.get_event_loop().time() - start_time) * 1000

    return {
        "method": "串行查询",
        "processing_time_ms": round(processing_time, 2),
        "note": "总耗时 = 数据库 + 评论 + 推荐（约 250-350ms）",
    }


@app.get(
    "/products/{product_id}/concurrent",
    summary="并发获取（性能优化）",
    description="并发查询数据源（快）",
)
async def get_product_concurrent(product_id: Annotated[int, Path(gt=0)]) -> dict[str, Any]:
    """
    并发查询（性能优化）

    **优势**: 总耗时 = max(单个查询耗时)
    """
    start_time = asyncio.get_event_loop().time()

    # ✅ 并发查询（快）
    async with asyncio.TaskGroup() as tg:
        tg.create_task(get_product_from_db(product_id))
        tg.create_task(get_product_reviews(product_id))
        tg.create_task(get_related_products(product_id))

    processing_time = (asyncio.get_event_loop().time() - start_time) * 1000

    return {
        "method": "并发查询（TaskGroup）",
        "processing_time_ms": round(processing_time, 2),
        "note": "总耗时 = max(数据库, 评论, 推荐)（约 100-200ms）",
        "speedup": "约 2-3x 加速",
    }


# ============================================================
# 运行说明
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("FastAPI 异步全链路 API")
    print("=" * 80)
    print("\n核心特性:")
    print("  ✅ TaskGroup 并发聚合")
    print("  ✅ 异步数据库查询")
    print("  ✅ 异步外部服务调用")
    print("  ✅ 流式响应")
    print("\n启动服务器...")
    print("  - API 文档: http://localhost:8000/docs")
    print("\n性能对比:")
    print("  - 串行: /products/1/serial  (约 250-350ms)")
    print("  - 并发: /products/1/concurrent (约 100-200ms)")
    print("\n按 Ctrl+C 停止\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
