"""
L47: 分布式系统实战 - 示例 1: Redis 分布式锁

本示例展示如何实现 Redis 分布式锁。
"""

import asyncio
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass


@dataclass
class LockResult:
    """加锁结果"""

    success: bool
    lock_id: str | None = None


class RedisDistributedLock:
    """
    Redis 分布式锁实现

    特性：
    - SET NX EX 原子操作
    - 自动过期防止死锁
    - 可重入（通过 lock_id 验证）
    """

    def __init__(self, redis_client, key: str, timeout: int = 10):
        self.redis = redis_client
        self.key = f"lock:{key}"
        self.timeout = timeout
        self.lock_id: str | None = None

    async def acquire(self) -> LockResult:
        """尝试获取锁"""
        lock_id = str(uuid.uuid4())

        # SET key value NX EX timeout - 原子操作
        acquired = await self.redis.set(
            self.key,
            lock_id,
            nx=True,  # 仅在 key 不存在时设置
            ex=self.timeout,  # 过期时间（秒）
        )

        if acquired:
            self.lock_id = lock_id
            return LockResult(success=True, lock_id=lock_id)

        return LockResult(success=False)

    async def release(self) -> bool:
        """释放锁（仅释放自己持有的锁）"""
        if self.lock_id is None:
            return False

        # Lua 脚本：检查 lock_id 是否匹配，匹配则删除
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """

        result = await self.redis.eval(script, 1, self.key, self.lock_id)
        self.lock_id = None
        return result == 1

    @asynccontextmanager
    async def __call__(self):
        """上下文管理器用法"""
        result = await self.acquire()
        if not result.success:
            raise RuntimeError(f"获取锁失败: {self.key}")

        try:
            yield
        finally:
            await self.release()


class MockRedis:
    """模拟 Redis 客户端（用于演示）"""

    def __init__(self):
        self._data: dict[str, str] = {}
        self._expiry: dict[str, float] = {}

    async def set(self, key: str, value: str, nx: bool = False, ex: int = None) -> bool:
        """SET 命令"""
        if nx and key in self._data:
            return False

        self._data[key] = value
        if ex:
            self._expiry[key] = asyncio.get_event_loop().time() + ex
        return True

    async def get(self, key: str) -> str | None:
        """GET 命令"""
        return self._data.get(key)

    async def delete(self, key: str) -> int:
        """DEL 命令"""
        if key in self._data:
            del self._data[key]
            return 1
        return 0

    async def eval(self, script: str, num_keys: int, *args) -> int:
        """EVAL 命令（简化实现）"""
        # 简化：直接比较并删除
        key = args[0]
        expected_value = args[1]

        if self._data.get(key) == expected_value:
            await self.delete(key)
            return 1
        return 0


async def demo_distributed_lock():
    """演示分布式锁"""
    print("=" * 60)
    print("Redis 分布式锁演示")
    print("=" * 60)

    # 使用模拟 Redis
    redis = MockRedis()

    # 创建锁
    lock = RedisDistributedLock(redis, "order:create", timeout=10)

    # 获取锁
    print("\n尝试获取锁...")
    result = await lock.acquire()
    print(f"获取结果: {result}")

    if result.success:
        print("✅ 锁获取成功，执行业务逻辑...")
        await asyncio.sleep(0.5)

        print("释放锁...")
        released = await lock.release()
        print(f"释放结果: {released}")

    # 演示锁竞争
    print("\n演示锁竞争...")
    lock1 = RedisDistributedLock(redis, "shared-resource", timeout=5)
    lock2 = RedisDistributedLock(redis, "shared-resource", timeout=5)

    result1 = await lock1.acquire()
    print(f"锁 1 获取结果: {result1}")

    result2 = await lock2.acquire()
    print(f"锁 2 获取结果: {result2}")  # 应该失败


if __name__ == "__main__":
    asyncio.run(demo_distributed_lock())
