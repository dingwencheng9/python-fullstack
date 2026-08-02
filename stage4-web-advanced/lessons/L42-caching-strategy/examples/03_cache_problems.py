# examples/03_cache_problems.py
"""
缓存问题处理演示 - 缓存穿透、击穿、雪崩

本模块演示三种常见缓存问题的原因和解决方案。
"""

from __future__ import annotations

import asyncio
import random
from typing import Any
# ==================== 模拟组件 ====================


class MockDatabase:
    """模拟数据库"""

    def __init__(self):
        self._data: dict[int, dict] = {
            1: {"id": 1, "name": "Product A"},
            2: {"id": 2, "name": "Product B"},
            3: {"id": 3, "name": "Product C"},
        }

    async def query(self, item_id: int) -> dict | None:
        """查询数据"""
        await asyncio.sleep(0.05)  # 模拟 DB 延迟
        return self._data.get(item_id)


class MockCache:
    """模拟缓存"""

    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Any | None:
        if key in self._store:
            value, expiry = self._store[key]
            if expiry > asyncio.get_event_loop().time():
                self._hits += 1
                return value
            del self._store[key]
        self._misses += 1
        return None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        expiry = asyncio.get_event_loop().time() + ttl
        self._store[key] = (value, expiry)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def get_stats(self) -> dict:
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0
        return {"hits": self._hits, "misses": self._misses, "hit_rate": f"{hit_rate:.1%}"}


# ==================== 问题 1: 缓存穿透 ====================


class CachePenetration:
    """
    缓存穿透：查询不存在的数据，每次都穿透到数据库

    原因：
    - 查询不存在的数据（如恶意攻击）
    - 缓存和数据库都没有这条数据
    - 每次请求都会查询数据库

    解决方案：
    - 空值缓存：缓存 NULL 值，短 TTL
    - 布隆过滤器：快速判断数据是否存在
    """

    def __init__(self, cache: MockCache, db: MockDatabase):
        self.cache = cache
        self.db = db
        self._null_cache_ttl = 60  # 空值缓存 TTL

    async def get_without_protection(self, item_id: int) -> dict | None:
        """无保护的查询（会穿透）"""
        cache_key = f"item:{item_id}"

        # 查缓存
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        # 查数据库
        item = await self.db.query(item_id)

        if item:
            self.cache.set(cache_key, item, ttl=3600)
        else:
            # 问题：这里没有缓存空值，导致每次都查 DB
            pass

        return item

    async def get_with_null_cache(self, item_id: int) -> dict | None:
        """使用空值缓存防止穿透"""
        cache_key = f"item:{item_id}"

        # 查缓存
        cached = self.cache.get(cache_key)
        if cached:
            # 检查是否是空值标记
            if cached.get("_null"):
                return None
            return cached

        # 查数据库
        item = await self.db.query(item_id)

        if item:
            self.cache.set(cache_key, item, ttl=3600)
        else:
            # 解决方案：缓存空值，短 TTL
            self.cache.set(cache_key, {"_null": True}, ttl=self._null_cache_ttl)

        return item


async def demo_cache_penetration():
    """演示缓存穿透问题"""
    print("\n" + "=" * 60)
    print("问题 1: 缓存穿透")
    print("=" * 60)

    cache = MockCache()
    db = MockDatabase()

    penetration = CachePenetration(cache, db)

    # 查询存在的数据
    print("\n[1] 查询存在的数据 (id=1)")
    result = await penetration.get_without_protection(1)
    print(f"    结果: {result}")
    print(f"    缓存状态: {cache.get_stats()}")

    # 查询不存在的数据（无保护）
    print("\n[2] 查询不存在的数据 (id=999) - 无保护")
    print("    模拟多次查询，观察数据库压力...")
    for i in range(5):
        result = await penetration.get_without_protection(999)
        print(f"    第{i + 1}次: 查询数据库 -> {result}")

    print(f"    缓存命中率: {cache.get_stats()['hit_rate']} (每次都穿透)")

    # 使用空值缓存
    cache.clear()
    print("\n[3] 查询不存在的数据 (id=999) - 使用空值缓存")
    for i in range(5):
        result = await penetration.get_with_null_cache(999)
        print(f"    第{i + 1}次: {result} (第2次后命中空值缓存)")

    print(f"    缓存命中率: {cache.get_stats()['hit_rate']}")


# ==================== 问题 2: 缓存击穿 ====================


class CacheBreaker:
    """
    缓存击穿：热点 key 过期时，大量并发请求同时穿透到数据库

    原因：
    - 热点数据缓存过期
    - 大量请求同时发现缓存不存在
    - 同时去数据库查询，造成数据库压力

    解决方案：
    - 互斥锁：只有一个请求去查数据库
    - 永不过期：热点数据使用主动更新策略
    """

    def __init__(self, cache: MockCache, db: MockDatabase):
        self.cache = cache
        self.db = db
        self._locks: dict[str, asyncio.Lock] = {}

    async def get_lock(self, key: str) -> asyncio.Lock:
        """获取指定 key 的锁"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    async def get_without_protection(self, item_id: int) -> dict | None:
        """无保护的查询（会击穿）"""
        cache_key = f"item:{item_id}"

        cached = self.cache.get(cache_key)
        if cached:
            return cached

        # 问题：多个协程同时执行到这里，都去查数据库
        print(f"      [查询DB] item_id={item_id}")
        item = await self.db.query(item_id)

        if item:
            self.cache.set(cache_key, item, ttl=1)  # 短 TTL，易过期

        return item

    async def get_with_mutex(self, item_id: int) -> dict | None:
        """使用互斥锁防止击穿"""
        cache_key = f"item:{item_id}"

        # 第一层检查
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        # 获取锁
        lock = await self.get_lock(cache_key)

        async with lock:
            # 双重检查（获取锁后再次检查）
            cached = self.cache.get(cache_key)
            if cached:
                return cached

            # 只有获取锁的协程去查数据库
            print(f"      [查询DB] item_id={item_id}")
            item = await self.db.query(item_id)

            if item:
                self.cache.set(cache_key, item, ttl=3600)

            return item


async def demo_cache_breaker():
    """演示缓存击穿问题"""
    print("\n" + "=" * 60)
    print("问题 2: 缓存击穿")
    print("=" * 60)

    cache = MockCache()
    db = MockDatabase()

    breaker = CacheBreaker(cache, db)

    # 预热缓存
    await breaker.get_without_protection(1)
    print("[0] 缓存已预热，1秒后过期...")

    # 等待缓存过期
    await asyncio.sleep(1.1)

    # 无保护：多个并发请求
    print("\n[1] 无保护：10 个并发请求同时查询 (缓存已过期)")
    print("    观察有多少请求查询了数据库:")

    async def concurrent_query():
        return await breaker.get_without_protection(1)

    results = await asyncio.gather(*[concurrent_query() for _ in range(10)])

    # 使用互斥锁
    cache.clear()
    await breaker.get_without_protection(2)
    await asyncio.sleep(1.1)

    print("\n[2] 使用互斥锁：10 个并发请求同时查询")
    print("    观察有多少请求查询了数据库:")

    async def concurrent_query_with_mutex():
        return await breaker.get_with_mutex(2)

    results = await asyncio.gather(*[concurrent_query_with_mutex() for _ in range(10)])
    print(f"    完成 {len(results)} 个并发请求")


# ==================== 问题 3: 缓存雪崩 ====================


class CacheAvalanche:
    """
    缓存雪崩：大量缓存同时过期，导致大量请求穿透到数据库

    原因：
    - 大量缓存设置相同的 TTL
    - 同时过期
    - 大量请求同时击穿缓存

    解决方案：
    - 随机 TTL：在基础 TTL 上添加随机偏移
    - 分级过期：不同级别缓存不同过期时间
    - 热点永不过期：热点数据主动续期
    """

    def __init__(self, cache: MockCache, db: MockDatabase):
        self.cache = cache
        self.db = db

    def generate_ttl(self, base_ttl: int, variance: float = 0.2) -> int:
        """生成带随机性的 TTL"""
        offset = base_ttl * variance
        return int(base_ttl + random.uniform(-offset, offset))

    async def get_with_fixed_ttl(self, item_id: int, ttl: int = 3600) -> dict | None:
        """固定 TTL（易雪崩）"""
        cache_key = f"item:{item_id}"

        cached = self.cache.get(cache_key)
        if cached:
            return cached

        item = await self.db.query(item_id)
        if item:
            self.cache.set(cache_key, item, ttl=ttl)

        return item

    async def get_with_random_ttl(self, item_id: int, base_ttl: int = 3600) -> dict | None:
        """随机 TTL（防止雪崩）"""
        cache_key = f"item:{item_id}"

        cached = self.cache.get(cache_key)
        if cached:
            return cached

        item = await self.db.query(item_id)
        if item:
            # 添加随机 TTL
            actual_ttl = self.generate_ttl(base_ttl, variance=0.3)
            self.cache.set(cache_key, item, ttl=actual_ttl)

        return item


async def demo_cache_avalanche():
    """演示缓存雪崩问题"""
    print("\n" + "=" * 60)
    print("问题 3: 缓存雪崩")
    print("=" * 60)

    cache = MockCache()
    db = MockDatabase()

    avalanche = CacheAvalanche(cache, db)

    # 批量预热 20 个缓存
    print("\n[1] 批量预热 20 个缓存（固定 TTL=1秒）")
    for i in range(1, 21):
        await avalanche.get_with_fixed_ttl(i, ttl=1)
    print("    所有缓存将在同一时刻过期...")

    # 等待过期
    print("\n[2] 等待 1.1 秒后...")
    await asyncio.sleep(1.1)

    # 模拟雪崩：同时查询
    print("\n[3] 模拟雪崩：同时查询 20 个缓存")
    print("    所有请求同时穿透到数据库:")

    async def query_item(i):
        return await avalanche.get_with_fixed_ttl(i)

    results = await asyncio.gather(*[query_item(i) for i in range(1, 21)])

    # 使用随机 TTL
    cache.clear()
    print("\n[4] 使用随机 TTL：同时查询 20 个缓存")
    print("    缓存过期时间错开，减轻数据库压力:")

    for i in range(1, 21):
        await avalanche.get_with_random_ttl(i, base_ttl=1)
    await asyncio.sleep(1.1)

    results = await asyncio.gather(*[avalanche.get_with_random_ttl(i) for i in range(1, 21)])
    print(f"    模拟雪崩，完成 {len(results)} 个请求")


# ==================== 演示 ====================


async def main():
    """主函数"""
    await demo_cache_penetration()
    await demo_cache_breaker()
    await demo_cache_avalanche()

    print("\n" + "=" * 60)
    print("缓存问题处理演示完成！")
    print("=" * 60)
    print("\n问题总结:")
    print("  1. 缓存穿透 → 空值缓存 + 布隆过滤器")
    print("  2. 缓存击穿 → 互斥锁 + 永不过期")
    print("  3. 缓存雪崩 → 随机 TTL + 分级过期")


if __name__ == "__main__":
    asyncio.run(main())
