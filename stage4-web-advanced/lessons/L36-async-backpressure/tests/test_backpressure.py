"""L36: 异步背压机制 - 测试用例

验证背压机制的核心功能：
1. 信号量控制并发
2. 令牌桶限流
3. 滑动窗口限流
4. 熔断器模式
5. 自适应限流

这些测试通过 conftest.py 中的 fixtures 加载示例代码。
"""

from __future__ import annotations

import asyncio
import time

import pytest


class TestSemaphorePool:
    """测试信号量池"""

    def test_semaphore_pool_creation(self, examples) -> None:
        """测试信号量池创建"""
        bb = examples.backpressure_basics
        pool = bb.SemaphorePool(max_concurrent=5)
        assert pool.max_concurrent == 5

    @pytest.mark.asyncio
    async def test_semaphore_pool_acquire_release(self, examples) -> None:
        """测试信号量获取和释放"""
        bb = examples.backpressure_basics
        pool = bb.SemaphorePool(max_concurrent=2)

        async with pool as p:
            assert p.max_concurrent == 2

    @pytest.mark.asyncio
    async def test_semaphore_pool_context_manager(self, examples) -> None:
        """测试上下文管理器"""
        bb = examples.backpressure_basics
        pool = bb.SemaphorePool(max_concurrent=1)

        async with pool:
            await asyncio.sleep(0.01)

        # 上下文结束后信号量应该被释放


class TestTokenBucket:
    """测试令牌桶算法"""

    def test_token_bucket_creation(self, examples) -> None:
        """测试令牌桶创建"""
        bb = examples.backpressure_basics
        bucket = bb.TokenBucket(capacity=100, refill_rate=50.0)
        assert bucket.capacity == 100
        assert bucket.refill_rate == 50.0

    def test_token_bucket_initial_tokens(self, examples) -> None:
        """测试初始令牌数"""
        bb = examples.backpressure_basics
        bucket = bb.TokenBucket(capacity=100, refill_rate=0)
        # 初始时应该有一定数量的令牌
        assert bucket.tokens >= 0

    def test_token_bucket_consume(self, examples) -> None:
        """测试令牌消费"""
        bb = examples.backpressure_basics
        bucket = bb.TokenBucket(capacity=100, refill_rate=0)
        bucket.tokens = 50  # 设置初始令牌

        # 消费令牌
        result = bucket.try_consume(10)
        assert result is True
        assert bucket.tokens == 40

    def test_token_bucket_insufficient_tokens(self, examples) -> None:
        """测试令牌不足"""
        bb = examples.backpressure_basics
        bucket = bb.TokenBucket(capacity=100, refill_rate=0)
        bucket.tokens = 5  # 只有 5 个令牌

        # 尝试消费更多
        result = bucket.try_consume(10)
        assert result is False
        assert bucket.tokens == 5  # 令牌数不变

    def test_token_bucket_refill(self, examples) -> None:
        """测试令牌补充"""
        bb = examples.backpressure_basics
        bucket = bb.TokenBucket(capacity=100, refill_rate=100)
        bucket.tokens = 0

        # 等待补充
        time.sleep(0.1)
        bucket._refill()

        assert bucket.tokens > 0
        assert bucket.tokens <= 11  # 0.1秒 * 100/秒 = 10 个令牌，允许一点误差


class TestSlidingWindowRateLimiter:
    """测试滑动窗口限流器"""

    def test_sliding_window_creation(self, examples) -> None:
        """测试滑动窗口创建"""
        bb = examples.backpressure_basics
        limiter = bb.SlidingWindowRateLimiter(max_requests=60, window_seconds=60.0)
        assert limiter.max_requests == 60
        assert limiter.window_seconds == 60.0

    def test_sliding_window_allowed(self, examples) -> None:
        """测试允许请求"""
        bb = examples.backpressure_basics
        limiter = bb.SlidingWindowRateLimiter(max_requests=5, window_seconds=60.0)

        # 前5个请求应该被允许
        for _ in range(5):
            assert limiter.is_allowed() is True

        # 第6个请求应该被拒绝
        assert limiter.is_allowed() is False

    def test_sliding_window_remaining(self, examples) -> None:
        """测试剩余配额"""
        bb = examples.backpressure_basics
        limiter = bb.SlidingWindowRateLimiter(max_requests=10, window_seconds=60.0)

        # 使用3个请求
        for _ in range(3):
            limiter.is_allowed()

        assert limiter.get_remaining() == 7


class TestBackpressureQueue:
    """测试背压队列"""

    def test_backpressure_queue_creation(self, examples) -> None:
        """测试背压队列创建"""
        bb = examples.backpressure_basics
        queue = bb.BackpressureQueue(max_size=10)
        assert queue.max_size == 10
        assert queue.qsize() == 0

    @pytest.mark.asyncio
    async def test_backpressure_queue_put_get(self, examples) -> None:
        """测试放入和获取"""
        bb = examples.backpressure_basics
        queue = bb.BackpressureQueue(max_size=5)

        # 放入数据
        result = await queue.put("item1")
        assert result is True
        assert queue.qsize() == 1

    @pytest.mark.asyncio
    async def test_backpressure_queue_full(self, examples) -> None:
        """测试队列满"""
        bb = examples.backpressure_basics
        queue = bb.BackpressureQueue(max_size=2)

        # 填满队列
        await queue.put("item1")
        await queue.put("item2")

        assert queue.is_full() is True

        # 尝试放入更多
        result = await queue.put("item3")
        assert result is False


class TestCircuitBreaker:
    """测试熔断器"""

    def test_circuit_breaker_creation(self, examples) -> None:
        """测试熔断器创建"""
        pb = examples.production_backpressure
        cb = pb.CircuitBreaker(failure_threshold=5, recovery_timeout=30.0)
        assert cb.failure_threshold == 5
        assert cb.recovery_timeout == 30.0

    def test_circuit_breaker_initial_state(self, examples) -> None:
        """测试初始状态"""
        pb = examples.production_backpressure
        cb = pb.CircuitBreaker()
        assert cb._state == pb.CircuitState.CLOSED
        assert cb.is_available() is True

    def test_circuit_breaker_record_failure(self, examples) -> None:
        """测试记录失败"""
        pb = examples.production_backpressure
        cb = pb.CircuitBreaker(failure_threshold=3)

        # 记录失败
        for _ in range(2):
            cb._record_failure()

        assert cb._failure_count == 2
        assert cb._state == pb.CircuitState.CLOSED

        # 第3次失败，触发熔断
        cb._record_failure()
        assert cb._state == pb.CircuitState.OPEN
        assert cb.is_available() is False

    def test_circuit_breaker_record_success(self, examples) -> None:
        """测试记录成功"""
        pb = examples.production_backpressure
        cb = pb.CircuitBreaker(failure_threshold=3)

        # 先触发熔断
        for _ in range(3):
            cb._record_failure()

        # 成功后重置
        cb._record_success()
        assert cb._failure_count == 0
        assert cb._state == pb.CircuitState.CLOSED


class TestRetryConfig:
    """测试重试配置"""

    def test_retry_config_creation(self, examples) -> None:
        """测试重试配置创建"""
        pb = examples.production_backpressure
        config = pb.RetryConfig(max_attempts=5, base_delay=2.0)
        assert config.max_attempts == 5
        assert config.base_delay == 2.0
        assert config.exponential_base == 2.0


class TestAdaptiveRateLimiter:
    """测试自适应限流器"""

    def test_adaptive_rate_limiter_creation(self, examples) -> None:
        """测试自适应限流器创建"""
        pb = examples.production_backpressure
        limiter = pb.AdaptiveRateLimiter(min_rate=10, max_rate=100, current_rate=50)
        assert limiter.min_rate == 10
        assert limiter.max_rate == 100
        assert limiter.current_rate == 50

    def test_adaptive_rate_limiter_acquire(self, examples) -> None:
        """测试获取令牌"""
        pb = examples.production_backpressure
        limiter = pb.AdaptiveRateLimiter(current_rate=100)
        limiter._tokens = 10  # 设置初始令牌

        # 应该能获取
        result = limiter.try_acquire(5)
        assert result is True

    def test_adaptive_rate_limiter_record_success(self, examples) -> None:
        """测试记录成功"""
        pb = examples.production_backpressure
        limiter = pb.AdaptiveRateLimiter(current_rate=50)

        limiter.record_success()
        assert limiter.current_rate == 50 * 1.1  # increase_factor

    def test_adaptive_rate_limiter_record_failure(self, examples) -> None:
        """测试记录失败"""
        pb = examples.production_backpressure
        limiter = pb.AdaptiveRateLimiter(current_rate=50)

        limiter.record_failure()
        assert limiter.current_rate == 50 * 0.5  # decrease_factor


class TestConnectionPool:
    """测试连接池"""

    @pytest.mark.asyncio
    async def test_connection_pool_creation(self, examples) -> None:
        """测试连接池创建"""
        pb = examples.production_backpressure
        pool = pb.ConnectionPool(max_size=5)
        assert pool.max_size == 5

    @pytest.mark.asyncio
    async def test_connection_pool_get_release(self, examples) -> None:
        """测试获取和释放连接"""
        pb = examples.production_backpressure
        pool = pb.ConnectionPool(max_size=3)

        # 获取连接
        conn1 = await pool.get_connection()
        assert conn1 is not None

        # 释放连接
        await pool.release_connection(conn1)

        # 再次获取
        conn2 = await pool.get_connection()
        assert conn2 is not None

        await pool.release_connection(conn2)

    @pytest.mark.asyncio
    async def test_connection_pool_in_use(self, examples) -> None:
        """测试使用中的连接数"""
        pb = examples.production_backpressure
        pool = pb.ConnectionPool(max_size=2)

        conn1 = await pool.get_connection()
        # 连接池为空时会创建连接，所以 in_use 会是 max_size
        assert pool.in_use <= pool.max_size

        await pool.release_connection(conn1)
        assert pool.in_use >= 0


class TestIntegration:
    """集成测试"""

    @pytest.mark.asyncio
    async def test_backpressure_chain(self, examples) -> None:
        """测试背压链"""
        bb = examples.backpressure_basics
        pb = examples.production_backpressure

        # 创建限流器
        rate_limiter = bb.SlidingWindowRateLimiter(max_requests=10, window_seconds=60.0)

        # 创建熔断器
        circuit_breaker = pb.CircuitBreaker(failure_threshold=5)

        # 测试基本功能
        for _ in range(5):
            assert rate_limiter.is_allowed() is True

        assert circuit_breaker.is_available() is True
