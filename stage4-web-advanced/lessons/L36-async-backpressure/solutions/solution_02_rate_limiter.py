"""参考答案 2：Token Bucket 速率限制器

基于 exercise_02_rate_limiter.py 的参考答案
"""

import asyncio
import time
from dataclasses import dataclass


class TokenBucket:
    """Token Bucket 速率限制器

    算法说明：
    - 桶以固定速率 rate 补充 token
    - 桶有最大容量 capacity
    - 获取 token 时，如果桶中有足够的 token 则立即返回
    - 否则等待直到有足够的 token
    """

    def __init__(
        self,
        rate: float = 100.0,
        capacity: int = 50,
        initial_tokens: float | None = None,
    ):
        """初始化 Token Bucket

        Args:
            rate: 每秒补充的 token 数量
            capacity: 桶的最大容量
            initial_tokens: 初始 token 数量，默认等于 capacity
        """
        self._rate = rate
        self._capacity = capacity
        self._tokens = initial_tokens if initial_tokens is not None else capacity
        self._last_update = time.monotonic()
        self._lock = asyncio.Lock()

    def _add_tokens(self) -> None:
        """根据时间流逝补充 token"""
        now = time.monotonic()
        elapsed = now - self._last_update
        self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
        self._last_update = now

    async def acquire(self, tokens: int = 1, blocking: bool = True) -> bool:
        """获取 token

        Args:
            tokens: 需要获取的 token 数量
            blocking: 是否阻塞等待，False 时立即返回

        Returns:
            True 获取成功，False 桶中 token 不足且 non-blocking 模式
        """
        async with self._lock:
            self._add_tokens()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            if not blocking:
                return False
            # 计算需要等待的时间
            needed = tokens - self._tokens
            wait_time = needed / self._rate
            # 释放锁后等待
            self._lock.release()
            try:
                await asyncio.sleep(wait_time)
            finally:
                await self._lock.acquire()
            # 等待后再次尝试
            self._add_tokens()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    async def try_acquire(self, tokens: int = 1) -> bool:
        """非阻塞获取 token（快捷方法）"""
        return await self.acquire(tokens=tokens, blocking=False)

    def available_tokens(self) -> float:
        """查看当前可用 token 数量"""
        return self._tokens


class RateLimiter:
    """基于 Token Bucket 的速率限制器

    封装 TokenBucket，提供更友好的 API
    """

    def __init__(
        self,
        requests_per_second: float = 100.0,
        burst_size: int = 50,
    ):
        """初始化速率限制器

        Args:
            requests_per_second: 每秒允许的请求数
            burst_size: 突发容量
        """
        self._bucket = TokenBucket(rate=requests_per_second, capacity=burst_size)

    async def __aenter__(self):
        """上下文管理器入口"""
        await self._bucket.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        return False

    async def acquire(self) -> None:
        """获取许可"""
        await self._bucket.acquire()


# ============ 测试代码 ============


async def test_token_bucket_basic():
    """测试 Token Bucket 基本功能"""
    bucket = TokenBucket(rate=10.0, capacity=10, initial_tokens=10)

    # 测试初始 token
    assert bucket.available_tokens() == 10.0, "初始 token 应为 10"

    # 消耗 5 个 token
    success = await bucket.try_acquire(5)
    assert success, "初始 token 充足时应获取成功"
    assert bucket.available_tokens() == 5.0, "剩余 token 应为 5"

    # 尝试获取超过剩余的 token（非阻塞）
    success = await bucket.try_acquire(10)
    assert not success, "token 不足时应返回失败"

    print("✅ Token Bucket 基本功能测试通过")


async def test_token_bucket_refill():
    """测试 Token Bucket 补充"""
    bucket = TokenBucket(rate=10.0, capacity=10, initial_tokens=0)

    # 等待 0.5 秒，应该补充 5 个 token
    await asyncio.sleep(0.5)
    assert bucket.available_tokens() >= 4.5, "0.5秒应补充约5个token"

    # 获取 5 个 token
    success = await bucket.try_acquire(5)
    assert success, "应有足够的 token"

    print("✅ Token Bucket 补充测试通过")


async def test_rate_limiter():
    """测试 RateLimiter"""
    limiter = RateLimiter(requests_per_second=100.0, burst_size=50)

    # 突发容量测试（应能快速获取多个）
    start = time.monotonic()
    for _ in range(50):
        await limiter.acquire()
    elapsed = time.monotonic() - start
    assert elapsed < 0.1, f"突发请求不应等待太久: {elapsed}s"

    # 再次请求应被限流
    start = time.monotonic()
    await limiter.acquire()
    elapsed = time.monotonic() - start
    assert elapsed > 0.01, "超过突发容量后应开始限流"

    print("✅ RateLimiter 测试通过")


async def test_rate_limiter_context_manager():
    """测试 RateLimiter 上下文管理器"""
    limiter = RateLimiter(requests_per_second=100.0, burst_size=10)

    async with limiter:
        # 在上下文中执行操作
        pass

    print("✅ RateLimiter 上下文管理器测试通过")


async def run_all_tests():
    """运行所有测试"""
    await test_token_bucket_basic()
    await test_token_bucket_refill()
    await test_rate_limiter()
    await test_rate_limiter_context_manager()
    print("\n🎉 所有测试通过!")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
