"""L36: 异步背压机制 - 示例代码

本模块展示 FastAPI 中异步背压机制的实现，包括：
1. 信号量控制并发
2. 速率限制器
3. 队列满时的优雅降级
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

app = FastAPI(title="异步背压机制示例")


# =============================================================================
# 示例 1: 信号量控制并发
# =============================================================================


@dataclass
class SemaphorePool:
    """信号量池 - 控制同时处理的最大请求数"""

    max_concurrent: int = 10
    _semaphore: asyncio.Semaphore = field(default_factory=lambda: asyncio.Semaphore(10))

    @property
    def semaphore(self) -> asyncio.Semaphore:
        return self._semaphore

    def release(self) -> None:
        """释放信号量"""
        self._semaphore.release()

    def try_acquire(self) -> bool:
        """尝试获取信号量，返回是否成功"""
        return self._semaphore.locked() and self._semaphore.acquire_nowait()

    async def __aenter__(self) -> SemaphorePool:
        await self._semaphore.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()


# 全局信号量池
semaphore_pool = SemaphorePool(max_concurrent=10)


@app.get("/semaphore-demo")
async def semaphore_demo(request: Request) -> dict:
    """使用信号量控制并发访问"""

    async with semaphore_pool:
        # 模拟慢速操作
        await asyncio.sleep(0.1)
        return {
            "message": "请求处理成功",
            "active_requests": semaphore_pool._semaphore._value,
            "timestamp": time.time(),
        }


# =============================================================================
# 示例 2: 速率限制器
# =============================================================================


@dataclass
class TokenBucket:
    """令牌桶算法实现"""

    capacity: int  # 桶的容量
    refill_rate: float  # 每秒补充的令牌数
    tokens: float = field(default_factory=lambda: 0.0)
    last_refill: float = field(default_factory=time.time)

    def _refill(self) -> None:
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def try_consume(self, tokens: int = 1) -> bool:
        """尝试消费令牌"""
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


# 全局速率限制器 (100 请求/秒)
rate_limiter = TokenBucket(capacity=100, refill_rate=100.0)


@app.get("/rate-limited")
async def rate_limited_endpoint(request: Request) -> dict:
    """使用令牌桶算法进行速率限制"""

    if not rate_limiter.try_consume(1):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="请求过于频繁，请稍后再试",
        )

    return {
        "message": "请求处理成功",
        "remaining_tokens": rate_limiter.tokens,
        "timestamp": time.time(),
    }


# =============================================================================
# 示例 3: 滑动窗口限流
# =============================================================================


@dataclass
class SlidingWindowRateLimiter:
    """滑动窗口限流器"""

    max_requests: int  # 时间窗口内的最大请求数
    window_seconds: float  # 时间窗口大小（秒）

    _requests: list[float] = field(default_factory=list)

    def _cleanup_old_requests(self) -> None:
        """清理过期的请求记录"""
        now = time.time()
        cutoff = now - self.window_seconds
        self._requests = [req_time for req_time in self._requests if req_time > cutoff]

    def is_allowed(self) -> bool:
        """检查是否允许请求"""
        self._cleanup_old_requests()

        if len(self._requests) < self.max_requests:
            self._requests.append(time.time())
            return True
        return False

    def get_remaining(self) -> int:
        """获取剩余请求配额"""
        self._cleanup_old_requests()
        return max(0, self.max_requests - len(self._requests))


# 全局滑动窗口限流器 (每分钟 60 请求)
sliding_window = SlidingWindowRateLimiter(max_requests=60, window_seconds=60.0)


@app.get("/sliding-window")
async def sliding_window_endpoint(request: Request) -> dict:
    """使用滑动窗口算法进行速率限制"""

    if not sliding_window.is_allowed():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="请求频率超限，请稍后再试",
            headers={"Retry-After": "60"},
        )

    return {
        "message": "请求处理成功",
        "remaining": sliding_window.get_remaining(),
        "timestamp": time.time(),
    }


# =============================================================================
# 示例 4: 队列满时的优雅降级
# =============================================================================


@dataclass
class BackpressureQueue:
    """带背压的队列"""

    max_size: int
    _queue: asyncio.Queue = field(default_factory=asyncio.Queue)

    def __post_init__(self) -> None:
        self._queue = asyncio.Queue(maxsize=self.max_size)

    async def put(self, item: object) -> bool:
        """放入数据，如果队列满则返回 False"""
        try:
            self._queue.put_nowait(item)
            return True
        except asyncio.QueueFull:
            return False

    async def get(self) -> object:
        """获取数据"""
        return await self._queue.get()

    def qsize(self) -> int:
        """获取队列大小"""
        return self._queue.qsize()

    def is_full(self) -> bool:
        """检查队列是否已满"""
        return self._queue.full()


# 全局背压队列
backpressure_queue = BackpressureQueue(max_size=100)


@app.post("/enqueue")
async def enqueue_task(task_data: dict) -> dict:
    """将任务放入队列，如果队列满则拒绝"""

    success = await backpressure_queue.put(task_data)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="系统繁忙，请稍后再试",
            headers={"Retry-After": "5"},
        )

    return {
        "message": "任务已入队",
        "queue_size": backpressure_queue.qsize(),
        "timestamp": time.time(),
    }


# =============================================================================
# 示例 5: 依赖注入方式的限流
# =============================================================================


async def get_rate_limiter() -> SlidingWindowRateLimiter:
    """获取速率限制器依赖"""
    return sliding_window


async def rate_limit_check(
    rate_limiter: Annotated[SlidingWindowRateLimiter, Depends(get_rate_limiter)],
) -> SlidingWindowRateLimiter:
    """速率限制检查依赖"""
    if not rate_limiter.is_allowed():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="请求频率超限",
        )
    return rate_limiter


@app.get("/protected")
async def protected_endpoint(
    rate_limiter: Annotated[SlidingWindowRateLimiter, Depends(rate_limit_check)],
) -> dict:
    """使用依赖注入进行速率限制的保护端点"""

    return {
        "message": "受保护的端点访问成功",
        "remaining": rate_limiter.get_remaining(),
        "timestamp": time.time(),
    }


# =============================================================================
# 示例 6: 流式响应的背压处理
# =============================================================================


async def generate_items() -> AsyncGenerator[dict]:
    """生成数据流，模拟数据源"""

    for i in range(100):
        # 模拟慢速数据生成
        await asyncio.sleep(0.01)
        yield {"index": i, "data": f"item_{i}"}


@app.get("/stream")
async def stream_endpoint(request: Request) -> JSONResponse:
    """流式响应端点"""

    async def generate() -> AsyncGenerator[bytes]:
        async for item in generate_items():
            # 检查客户端是否断开连接
            if await request.is_disconnected():
                break
            yield (f"data: {item}\n\n").encode()

    return JSONResponse(
        content={"message": "使用 SSE 进行流式传输"},
        media_type="application/json",
    )


# =============================================================================
# 健康检查端点
# =============================================================================


@app.get("/health")
async def health_check() -> dict:
    """健康检查端点"""
    return {
        "status": "healthy",
        "active_concurrent": 10 - semaphore_pool._semaphore._value,
        "rate_limiter_remaining": rate_limiter.try_consume(0),  # 不消费，只检查
        "queue_size": backpressure_queue.qsize(),
        "timestamp": time.time(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
