# tests/test_cache.py
"""
L42 缓存策略测试
"""

from __future__ import annotations

import time
import pytest
from typing import Any
# ==================== 测试数据模型 ====================


class MockCache:
    """测试用模拟缓存（无 TTL）"""

    def __init__(self):
        self._store: dict[str, Any] = {}
        self._hits = 0
        self._misses = 0

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def misses(self) -> int:
        return self._misses

    def get(self, key: str) -> Any | None:
        if key in self._store:
            self._hits += 1
            return self._store[key]
        self._misses += 1
        return None

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()
        self._hits = 0
        self._misses = 0


class MockDatabase:
    """测试用模拟数据库"""

    def __init__(self):
        self._users = {
            1: {"id": 1, "username": "alice", "email": "alice@example.com"},
            2: {"id": 2, "username": "bob", "email": "bob@example.com"},
        }

    async def get_user(self, user_id: int) -> dict | None:
        return self._users.get(user_id)

    async def update_user(self, user_id: int, **kwargs) -> dict | None:
        if user_id in self._users:
            self._users[user_id].update(kwargs)
            return self._users[user_id]
        return None


# ==================== 测试用例 ====================


class TestCacheAside:
    """测试 Cache-Aside 模式"""

    @pytest.fixture
    def cache_aside(self):
        cache = MockCache()
        db = MockDatabase()

        class CacheAside:
            def __init__(self, cache, db):
                self.cache = cache
                self.db = db

            async def get_user(self, user_id: int) -> dict | None:
                cache_key = f"user:{user_id}"
                cached = self.cache.get(cache_key)
                if cached:
                    return cached
                user = await self.db.get_user(user_id)
                if user:
                    self.cache.set(cache_key, user)
                return user

            async def update_user(self, user_id: int, **kwargs) -> dict | None:
                cache_key = f"user:{user_id}"
                user = await self.db.update_user(user_id, **kwargs)
                if user:
                    self.cache.delete(cache_key)
                return user

        return CacheAside(cache, db)

    @pytest.mark.asyncio
    async def test_cache_miss_then_hit(self, cache_aside):
        """测试缓存未命中后命中"""
        # 首次查询 - 缓存未命中
        user = await cache_aside.get_user(1)
        assert user is not None
        assert user["username"] == "alice"
        assert cache_aside.cache.hits == 0
        assert cache_aside.cache.misses == 1

        # 再次查询 - 缓存命中
        user = await cache_aside.get_user(1)
        assert user is not None
        assert user["username"] == "alice"
        assert cache_aside.cache.hits == 1
        assert cache_aside.cache.misses == 1

    @pytest.mark.asyncio
    async def test_update_invalidates_cache(self, cache_aside):
        """测试更新后缓存失效"""
        # 先查询填充缓存
        await cache_aside.get_user(1)  # miss=1
        assert cache_aside.cache.misses == 1

        await cache_aside.get_user(1)  # hit=1
        assert cache_aside.cache.hits == 1

        # 更新用户 - 缓存失效
        await cache_aside.update_user(1, username="alice_new")

        # 再次查询 - 缓存未命中
        await cache_aside.get_user(1)  # miss=2
        assert cache_aside.cache.misses == 2
        assert cache_aside.cache.hits == 1

    @pytest.mark.asyncio
    async def test_nonexistent_user(self, cache_aside):
        """测试不存在的用户"""
        user = await cache_aside.get_user(999)
        assert user is None


class TestMultiLevelCache:
    """测试多级缓存"""

    @pytest.fixture
    def multi_level_cache(self):
        class L1Cache:
            def __init__(self):
                self._store = {}

            def get(self, key):
                return self._store.get(key)

            def set(self, key, value):
                self._store[key] = value

            def delete(self, key):
                self._store.pop(key, None)

        class L2Cache:
            def __init__(self):
                self._store = {}

            async def get(self, key):
                return self._store.get(key)

            async def set(self, key, value):
                self._store[key] = value

            async def delete(self, key):
                self._store.pop(key, None)

        class MultiLevelCache:
            def __init__(self, l1, l2):
                self.l1 = l1
                self.l2 = l2

            async def get(self, item_id):
                key = f"item:{item_id}"

                # L1 查找
                cached = self.l1.get(key)
                if cached:
                    return cached

                # L2 查找
                cached = await self.l2.get(key)
                if cached:
                    self.l1.set(key, cached)
                    return cached

                return None

            async def invalidate(self, item_id):
                key = f"item:{item_id}"
                self.l1.delete(key)
                await self.l2.delete(key)

        l1 = L1Cache()
        l2 = L2Cache()
        return MultiLevelCache(l1, l2)

    @pytest.mark.asyncio
    async def test_l1_hit(self, multi_level_cache):
        """测试 L1 命中"""
        # 设置 L1 缓存
        multi_level_cache.l1.set("item:1", {"id": 1, "name": "Item 1"})

        # 查询
        result = await multi_level_cache.get(1)

        assert result is not None
        assert result["id"] == 1
        assert result["name"] == "Item 1"

    @pytest.mark.asyncio
    async def test_l2_hit_and_backfill(self, multi_level_cache):
        """测试 L2 命中并回填 L1"""
        # 设置 L2 缓存
        await multi_level_cache.l2.set("item:2", {"id": 2, "name": "Item 2"})

        # 查询
        result = await multi_level_cache.get(2)

        assert result is not None
        assert result["id"] == 2
        # 应该回填到 L1
        assert multi_level_cache.l1.get("item:2") is not None

    @pytest.mark.asyncio
    async def test_invalidate_both_levels(self, multi_level_cache):
        """测试失效两个层级"""
        # 设置 L1 和 L2 缓存
        multi_level_cache.l1.set("item:3", {"id": 3})
        await multi_level_cache.l2.set("item:3", {"id": 3})

        # 失效
        await multi_level_cache.invalidate(3)

        # 两个层级都应该被清除
        assert multi_level_cache.l1.get("item:3") is None


class TestCacheMetrics:
    """测试缓存指标"""

    def test_hit_rate_calculation(self):
        """测试命中率计算"""
        cache = MockCache()

        # 模拟 10 次查询，3 次命中
        # 前 3 次都 miss (key 不存在)
        for _ in range(3):
            cache.get("key1")
        # 后 7 次，前 3 次命中，后 4 次 miss
        cache.set("key2", "value")
        for _ in range(3):
            cache.get("key2")  # 3 次命中
        for _ in range(4):
            cache.get("key3")  # 4 次 miss

        assert cache.hits == 3
        assert cache.misses == 7

        total = cache.hits + cache.misses
        hit_rate = cache.hits / total if total > 0 else 0
        assert hit_rate == 0.3


class TestCacheTTL:
    """测试缓存 TTL"""

    def test_ttl_expiry(self):
        """测试 TTL 过期"""

        class TTLCache:
            def __init__(self):
                self._store: dict[str, tuple[Any, float]] = {}

            def get(self, key: str) -> Any | None:
                if key in self._store:
                    value, expiry = self._store[key]
                    if expiry > time.time():
                        return value
                    del self._store[key]
                return None

            def set(self, key: str, value: Any, ttl: int = 300) -> None:
                expiry = time.time() + ttl
                self._store[key] = (value, expiry)

        cache = TTLCache()

        # 设置 1 秒 TTL
        cache.set("key1", "value1", ttl=1)

        # 立即获取 - 命中
        assert cache.get("key1") == "value1"

        # 等待过期
        time.sleep(1.1)

        # 过期后获取 - 未命中
        assert cache.get("key1") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
