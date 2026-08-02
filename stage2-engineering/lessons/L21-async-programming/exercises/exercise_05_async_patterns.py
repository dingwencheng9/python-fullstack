"""练习 5: 指数退避重试 + 令牌桶限流.

学习目标：
- 实现带指数退避和 jitter 的异步重试
- 实现令牌桶限流器
- 将两者结合用于生产级 API 调用模式
"""

from __future__ import annotations

import asyncio
import random
import time


# ============================================================
# 指数退避重试
# ============================================================


async def retry_with_backoff(
    func,
    *,
    max_retries: int = 5,
    initial_delay: float = 0.3,
    backoff_factor: float = 2.0,
    jitter: bool = True,
) -> str:
    """指数退避重试装饰器。"""
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception:
            if attempt == max_retries - 1:
                raise
            actual = delay * (0.5 + random.random()) if jitter else delay
            print(f"  重试 {attempt + 1}/{max_retries}，等待 {actual:.2f}s")
            await asyncio.sleep(actual)
            delay = min(delay * backoff_factor, 30.0)
    raise RuntimeError("不应到达这里")


async def test_retry() -> None:
    """测试指数退避重试。"""
    print("=" * 60)
    print("练习 5: 指数退避重试 + 令牌桶限流")
    print("=" * 60)
    print()

    call_count = 0

    async def flaky_operation() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 4:
            raise ValueError(f"第 {call_count} 次失败")
        return "成功"

    result = await retry_with_backoff(flaky_operation, max_retries=5)
    assert result == "成功"
    assert call_count == 4, f"期望 4 次调用，得到 {call_count}"
    print(f"  重试成功: {result}（共调用 {call_count} 次）")
    print("✅ 指数退避重试测试通过")


# ============================================================
# 令牌桶限流器
# ============================================================


class TokenBucket:
    """令牌桶限流器。"""

    def __init__(self, rate: float, capacity: int) -> None:
        self.rate = rate
        self.capacity = capacity
        self.tokens = float(capacity)
        self.last_update = time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> bool:
        """尝试获取令牌。"""
        async with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    async def wait_for_token(self, tokens: int = 1) -> None:
        """阻塞直到获取令牌。"""
        while not await self.acquire(tokens):
            await asyncio.sleep(0.05)


async def test_token_bucket() -> None:
    """测试令牌桶限流器。"""
    bucket = TokenBucket(rate=5.0, capacity=10)  # 每秒 5 个，容量 10

    start = time.monotonic()
    for i in range(10):
        await bucket.wait_for_token()
        print(f"  请求 {i + 1} 通过")
    elapsed = time.monotonic() - start

    # 前 10 个请求使用初始令牌（无需等待），应在 0.5 秒内完成
    assert elapsed < 1.0, f"前 10 个请求应几乎瞬时完成，实际 {elapsed:.2f}s"
    print(f"  前 10 个请求耗时: {elapsed:.3f}s")
    print("✅ 令牌桶限流器测试通过")


# ============================================================
# 自检入口
# ============================================================


async def main() -> None:
    try:
        await test_retry()
        await test_token_bucket()
    except Exception as exc:
        print(f"❌ 错误: {exc}")
        raise SystemExit(1) from exc

    print()
    print("🎉 练习 5 完成！")
    print()
    print("总结：")
    print("  - asyncio.Queue: 生产者/消费者")
    print("  - asyncio.Event: 一次性信号")
    print("  - asyncio.Condition: 条件变量")
    print("  - as_completed: 按完成顺序处理")
    print("  - asyncio.TaskGroup: 结构化并发")
    print("  - asyncio.timeout: 超时管理")
    print("  - 优雅关闭: Event + 任务管理")
    print("  - 熔断器: 防止级联失败")
    print("  - 重试+退避: 指数回退 + jitter")


if __name__ == "__main__":
    asyncio.run(main())
