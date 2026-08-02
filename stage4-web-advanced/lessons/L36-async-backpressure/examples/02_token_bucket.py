"""Token Bucket 算法示例"""

import asyncio
import time
from dataclasses import dataclass, field


@dataclass
class TokenBucket:
    """Token Bucket 限流器"""

    capacity: float
    rate: float
    tokens: float = field(init=False)
    last_update: float = field(init=False)

    def __post_init__(self):
        self.tokens = self.capacity
        self.last_update = time.monotonic()

    def acquire(self, tokens: float = 1.0) -> bool:
        """尝试获取 Token"""
        now = time.monotonic()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


async def rate_limited_request(bucket: TokenBucket, request_id: int):
    """限流请求"""
    while not bucket.acquire():
        await asyncio.sleep(0.1)
    print(f"请求 {request_id} 执行")


async def main():
    bucket = TokenBucket(capacity=5, rate=2)  # 容量5，每秒补充2

    async with asyncio.TaskGroup() as tg:
        for i in range(20):
            tg.create_task(rate_limited_request(bucket, i))


if __name__ == "__main__":
    asyncio.run(main())
