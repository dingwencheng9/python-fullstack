"""L36: 异步背压机制 - 生产级实现

本模块展示生产环境中使用的背压策略：
1. 自适应限流
2. 熔断器模式
3. 重试与退避
"""

from __future__ import annotations

import asyncio
import random
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeVar

from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="异步背压机制 - 生产级实现")

T = TypeVar("T")


# =============================================================================
# 示例 1: 熔断器模式
# =============================================================================


class CircuitState(Enum):
    """熔断器状态"""

    CLOSED = "closed"  # 正常
    OPEN = "open"  # 熔断
    HALF_OPEN = "half_open"  # 半开


@dataclass
class CircuitBreaker:
    """熔断器实现"""

    failure_threshold: int = 5  # 失败次数阈值
    recovery_timeout: float = 60.0  # 恢复超时（秒）
    half_open_max_calls: int = 3  # 半开状态下的最大调用次数

    _state: CircuitState = field(default=CircuitState.CLOSED)
    _failure_count: int = field(default=0)
    _last_failure_time: float = field(default=0.0)
    _half_open_calls: int = field(default=0)

    def _should_attempt_reset(self) -> bool:
        """检查是否应该尝试重置熔断器"""
        if self._state != CircuitState.OPEN:
            return False

        elapsed = time.time() - self._last_failure_time
        return elapsed >= self.recovery_timeout

    def _record_success(self) -> None:
        """记录成功调用"""
        self._failure_count = 0
        self._half_open_calls = 0
        self._state = CircuitState.CLOSED

    def _record_failure(self) -> None:
        """记录失败调用"""
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN

    def is_available(self) -> bool:
        """检查是否可用"""
        if self._state == CircuitState.CLOSED:
            return True

        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
                return True
            return False

        # 半开状态
        return self._half_open_calls < self.half_open_max_calls

    async def call(self, func: Callable[..., T], *args: object, **kwargs: object) -> T:
        """执行函数调用，受熔断器保护"""
        if not self.is_available():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="服务暂时不可用（熔断器开启）",
            )

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if self._state == CircuitState.HALF_OPEN:
                self._half_open_calls += 1
                if self._half_open_calls >= self.half_open_max_calls:
                    self._record_success()

            return result

        except Exception:
            self._record_failure()

            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN

            raise


# 全局熔断器
circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30.0,
    half_open_max_calls=3,
)


# =============================================================================
# 示例 2: 重试与指数退避
# =============================================================================


@dataclass
class RetryConfig:
    """重试配置"""

    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0


async def retry_with_backoff(
    func: Callable[..., T],
    *args: object,
    config: RetryConfig | None = None,
    **kwargs: object,
) -> T:
    """带指数退避的重试机制"""

    config = config or RetryConfig()
    last_exception: Exception | None = None

    for attempt in range(config.max_attempts):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        except Exception as e:
            last_exception = e

            if attempt < config.max_attempts - 1:
                # 计算退避延迟
                delay = min(
                    config.base_delay * (config.exponential_base**attempt),
                    config.max_delay,
                )
                # 添加抖动
                delay *= 0.5 + random.random()

                await asyncio.sleep(delay)

    raise last_exception


# =============================================================================
# 示例 3: 自适应限流
# =============================================================================


@dataclass
class AdaptiveRateLimiter:
    """自适应限流器"""

    min_rate: float = 10.0  # 最小速率（请求/秒）
    max_rate: float = 1000.0  # 最大速率（请求/秒）
    current_rate: float = field(default=100.0)  # 当前速率
    increase_factor: float = 1.1  # 增加因子
    decrease_factor: float = 0.5  # 减少因子

    _tokens: float = field(default=100.0)
    _last_update: float = field(default_factory=time.time)

    def _update_tokens(self) -> None:
        """更新令牌"""
        now = time.time()
        elapsed = now - self._last_update
        self._tokens = min(self.max_rate, self._tokens + elapsed * self.current_rate)
        self._last_update = now

    def try_acquire(self, tokens: int = 1) -> bool:
        """尝试获取令牌"""
        self._update_tokens()

        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def record_success(self) -> None:
        """记录成功"""
        # 成功时逐渐增加速率
        self.current_rate = min(self.max_rate, self.current_rate * self.increase_factor)

    def record_failure(self) -> None:
        """记录失败"""
        # 失败时降低速率
        self.current_rate = max(self.min_rate, self.current_rate * self.decrease_factor)


adaptive_limiter = AdaptiveRateLimiter()


# =============================================================================
# 示例 4: 连接池管理
# =============================================================================


@dataclass
class ConnectionPool:
    """连接池管理"""

    max_size: int
    min_size: int = 0
    _connections: asyncio.Queue = field(default_factory=asyncio.Queue)
    _semaphore: asyncio.Semaphore = field(default_factory=lambda: asyncio.Semaphore(1))
    _created: int = 0

    def __post_init__(self) -> None:
        self._connections = asyncio.Queue(maxsize=self.max_size)
        self._semaphore = asyncio.Semaphore(self.max_size)

    async def get_connection(self) -> object:
        """获取连接"""
        if not self._connections.empty():
            return await self._connections.get()

        if self._created < self.max_size:
            self._created += 1
            return await self._create_connection()

        # 等待连接释放
        return await asyncio.wait_for(self._connections.get(), timeout=30.0)

    async def release_connection(self, conn: object) -> None:
        """释放连接"""
        try:
            self._connections.put_nowait(conn)
        except asyncio.QueueFull:
            await self._close_connection(conn)

    async def _create_connection(self) -> object:
        """创建新连接（模拟）"""
        await asyncio.sleep(0.1)  # 模拟连接建立
        return {"id": self._created, "created_at": time.time()}

    async def _close_connection(self, conn: object) -> None:
        """关闭连接"""
        self._created -= 1

    @property
    def available(self) -> int:
        """可用连接数"""
        return self._connections.qsize()

    @property
    def in_use(self) -> int:
        """使用中连接数"""
        return self.max_size - self.available


pool = ConnectionPool(max_size=10, min_size=2)


# =============================================================================
# 示例 5: 健康检查与指标
# =============================================================================


@app.get("/health/circuit")
async def circuit_breaker_health() -> dict:
    """熔断器健康状态"""
    return {
        "state": circuit_breaker._state.value,
        "failure_count": circuit_breaker._failure_count,
        "is_available": circuit_breaker.is_available(),
    }


@app.get("/health/rate")
async def rate_limiter_health() -> dict:
    """自适应限流器健康状态"""
    return {
        "current_rate": adaptive_limiter.current_rate,
        "min_rate": adaptive_limiter.min_rate,
        "max_rate": adaptive_limiter.max_rate,
    }


@app.get("/health/pool")
async def connection_pool_health() -> dict:
    """连接池健康状态"""
    return {
        "max_size": pool.max_size,
        "available": pool.available,
        "in_use": pool.in_use,
    }


# =============================================================================
# 综合示例端点
# =============================================================================


@app.get("/circuit-protected")
async def circuit_protected_endpoint() -> dict:
    """受熔断器保护的端点"""

    async def unreliable_service() -> dict:
        # 模拟不稳定的服务
        if random.random() < 0.3:
            raise HTTPException(status_code=500, detail="服务错误")
        return {"message": "服务正常"}

    result = await circuit_breaker.call(unreliable_service)
    return result


@app.get("/retry-demo")
async def retry_demo_endpoint() -> dict:
    """带重试的端点"""

    call_count = 0

    async def flaky_service() -> dict:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("临时错误")
        return {"message": f"成功（尝试了 {call_count} 次）"}

    result = await retry_with_backoff(flaky_service, config=RetryConfig(max_attempts=5))
    return result


@app.get("/pool-demo")
async def pool_demo_endpoint() -> dict:
    """连接池演示"""
    conn = await pool.get_connection()
    try:
        # 使用连接
        await asyncio.sleep(0.1)
        return {
            "message": "使用连接成功",
            "connection_id": conn["id"],
            "pool_available": pool.available,
            "pool_in_use": pool.in_use,
        }
    finally:
        await pool.release_connection(conn)


@app.get("/adaptive-rate")
async def adaptive_rate_endpoint() -> dict:
    """自适应限流演示"""
    if not adaptive_limiter.try_acquire(1):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="速率限制",
        )

    return {
        "message": "请求成功",
        "current_rate": adaptive_limiter.current_rate,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
