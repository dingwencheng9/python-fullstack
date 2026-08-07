"""

from __future__ import annotations

FastAPI 结构化日志 - loguru
============================

本模块展示 FastAPI + loguru 的结构化日志设计：
- 告别 print() 调试
- 结构化 JSON 日志
- 请求链路追踪
- 多输出目标（控制台/文件）

架构设计：
---------
1. loguru 配置（全局过滤器）
2. 请求上下文注入（请求 ID）
3. 结构化日志输出（JSON 格式）
4. 日志轮转（rotating file）

对标：
-----
- 粉碎旧 Web 模块的 print() 调试（488 次）
- 呼应 L21 日志与配置

作者：Python 3.13 全栈课程
"""

from __future__ import annotations

import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field
from loguru import logger

# ============================================================
# loguru 配置（生产级）
# ============================================================


def setup_logging(log_level: str = "INFO") -> None:
    """
    配置 loguru

    **核心特性**:
    - 结构化 JSON 输出
    - 请求 ID 追踪
    - 日志轮转
    - 异步安全
    """
    # 移除默认处理器
    logger.remove()

    # 添加控制台处理器（带颜色）
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # 添加文件处理器（JSON 格式，用于 ELK/Grafana Loki）
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "app_{time}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="100 MB",  # 100MB 后轮转
        retention="7 days",  # 保留 7 天
        compression="zip",  # 压缩旧日志
        serialize=True,  # JSON 格式输出
        enqueue=True,  # 异步写入（多进程安全）
    )

    logger.info(f"日志系统已配置，级别: {log_level}")
    logger.info(f"日志文件目录: {log_dir}")


# ============================================================
# 请求上下文（请求 ID 注入）
# ============================================================

import uuid
from contextvars import ContextVar

# 上下文变量：存储当前请求 ID
request_id_var: ContextVar[str] = ContextVar("request_id", default="no-request")


class RequestContextMiddleware:
    """
    请求上下文中间件

    **功能**:
    - 为每个请求生成唯一 ID
    - 注入到 loguru 的上下文变量
    - 记录请求开始/结束日志
    """

    def __init__(self, app: FastAPI) -> None:
        self.app = app

    async def __call__(self, scope: dict, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # 生成请求 ID
        request_id = str(uuid.uuid4())[:8]

        # 注入到上下文变量
        token = request_id_var.set(request_id)

        # 记录请求开始
        logger.info(
            "请求开始",
            extra={
                "request_id": request_id,
                "method": scope.get("method"),
                "path": scope.get("path"),
                "client": scope.get("client"),
            },
        )

        # 记录开始时间
        start_time = time.time()

        # 记录响应状态
        status_code = 500

        async def send_wrapper(message: dict) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # 计算耗时
            elapsed = (time.time() - start_time) * 1000

            # 记录请求结束
            logger.info(
                "请求结束",
                extra={
                    "request_id": request_id,
                    "status_code": status_code,
                    "elapsed_ms": round(elapsed, 2),
                },
            )

            # 恢复上下文变量
            request_id_var.reset(token)


# ============================================================
# 业务日志（带请求 ID）
# ============================================================


def log_with_context(level: str, message: str, **kwargs) -> None:
    """
    带请求上下文的日志记录

    **用法**:
    ```python
    log_with_context("info", "用户登录成功", user_id=123)
    # 输出: 2024-01-01 12:00:00 | INFO | app.py:main:45 | 用户登录成功 | request_id=abc123 user_id=123
    ```
    """
    # 获取当前请求 ID
    request_id = request_id_var.get()

    # 构建日志额外数据
    extra = {"request_id": request_id, **kwargs}

    # 根据级别记录日志
    if level == "debug":
        logger.debug(message, extra=extra)
    elif level == "info":
        logger.info(message, extra=extra)
    elif level == "warning":
        logger.warning(message, extra=extra)
    elif level == "error":
        logger.error(message, extra=extra)
    elif level == "critical":
        logger.critical(message, extra=extra)
    else:
        logger.log(level, message, extra=extra)


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
# 内存存储（演示用）
# ============================================================

items_db: dict[int, dict] = {}
next_id = 1


# ============================================================
# FastAPI 应用（带结构化日志）
# ============================================================


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001 FastAPI lifespan 协议要求保留 app 参数
    """应用生命周期管理"""
    # 启动时配置日志
    setup_logging(log_level="INFO")
    logger.info("应用启动", extra={"event": "startup"})
    yield
    logger.info("应用关闭", extra={"event": "shutdown"})


app = FastAPI(
    title="结构化日志 API",
    description="FastAPI + loguru 结构化日志示例",
    version="1.0.0",
    lifespan=lifespan,
)

# 添加请求上下文中间件
RequestContextMiddleware(app)


# ============================================================
# API 路由（带结构化日志）
# ============================================================


@app.get("/", summary="欢迎页")
async def root() -> dict[str, str]:
    """
    欢迎页

    **日志特性**:
    - 自动记录请求开始/结束
    - 包含请求 ID
    """
    log_with_context("info", "访问欢迎页")
    return {
        "message": "FastAPI 结构化日志 API",
        "features": "loguru + 请求上下文 + JSON 日志",
    }


@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=201,
    summary="创建商品",
)
async def create_item(item: ItemCreate) -> ItemResponse:
    """
    创建商品

    **日志特性**:
    - 结构化参数记录
    - 错误追踪
    """
    global next_id

    log_with_context(
        "info",
        "创建商品",
        item_name=item.name,
        item_price=item.price,
    )

    try:
        # 模拟数据库操作
        new_item = {
            "id": next_id,
            "name": item.name,
            "price": item.price,
        }
        items_db[next_id] = new_item
        next_id += 1

        log_with_context(
            "info",
            "商品创建成功",
            item_id=new_item["id"],
        )

        return ItemResponse(**new_item)

    except Exception as e:
        log_with_context(
            "error",
            "商品创建失败",
            error=str(e),
        )
        raise


@app.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="获取商品",
)
async def get_item(item_id: int) -> ItemResponse:
    """
    获取商品详情

    **日志特性**:
    - 404 时记录警告
    - 成功时记录详情
    """
    log_with_context("info", "查询商品", item_id=item_id)

    if item_id not in items_db:
        log_with_context("warning", "商品不存在", item_id=item_id)
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="商品不存在")

    item = items_db[item_id]
    log_with_context("info", "商品查询成功", item_id=item_id, item_name=item["name"])

    return ItemResponse(**item)


# ============================================================
# 运行说明
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("FastAPI 结构化日志 API")
    print("=" * 80)
    print("\n核心特性:")
    print("  ✅ 告别 print() 调试")
    print("  ✅ 结构化 JSON 日志")
    print("  ✅ 请求链路追踪（请求 ID）")
    print("  ✅ 日志轮转（100MB/7天）")
    print("\n日志文件:")
    print("  - 控制台: 彩色格式（开发）")
    print("  - 文件: JSON 格式（生产）")
    print("\n示例请求:")
    print("  curl -X POST http://localhost:8000/items \\")
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"name": "iPhone", "price": 9999.0}\'')
    print("\n查看日志文件:")
    print("  ls -la examples/logs/")
    print("  cat examples/logs/app_*.log | jq .")
    print("\n按 Ctrl+C 停止\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
