# solutions/solution_01_cache_design.py
"""
练习 1 参考答案: 多级缓存系统实现
"""

from __future__ import annotations

import asyncio
import time
from typing import Any
# ==================== 数据源 ====================


class DataSource:
    """模拟数据库"""

    def __init__(self):
        self._data = {
            1: {"id": 1, "name": "Product A", "price": 99.99},
            2: {"id": 2, "name": "Product B", "price": 149.99},
            3: {"id": 3, "name": "Product C", "price": 199.99},
        }

    async def get(self, item_id: int) -> dict | None:
        """模拟数据库查询，100ms 延迟"""
        await asyncio.sleep(0.1)
        return self._data.get(item_id)


# ==================== L1 本地缓存 ====================


class L1Cache:
    """L1 本地缓存"""

    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        """从本地缓存获取"""
        if key in self._store:
            value, expiry = self._store[key]
            if expiry > time.time():
                return value
            del self._store[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        """设置本地缓存"""
        expiry = time.time() + ttl
        self._store[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """删除本地缓存"""
        self._store.pop(key, None)


# ==================== L2 分布式缓存 ====================


class L2Cache:
    """L2 分布式缓存"""

    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}

    async def get(self, key: str) -> Any | None:
        """从分布式缓存获取"""
        if key in self._store:
            value, expiry = self._store[key]
            if expiry > time.time():
                return value
            del self._store[key]
        return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """设置分布式缓存"""
        expiry = time.time() + ttl
        self._store[key] = (value, expiry)

    async def delete(self, key: str) -> None:
        """删除分布式缓存"""
        self._store.pop(key, None)


# ==================== 多级缓存管理器 ====================


class MultiLevelCache:
    """多级缓存管理器"""

    def __init__(self, l1: L1Cache, l2: L2Cache, source: DataSource):
        self.l1 = l1
        self.l2 = l2
        self.source = source
        self._lock = asyncio.Lock()

    def _make_key(self, item_id: int) -> str:
        return f"item:{item_id}"

    async def get(self, item_id: int) -> dict | None:
        """多级缓存查询"""
        cache_key = self._make_key(item_id)

        # 1. 查 L1
        cached = self.l1.get(cache_key)
        if cached is not None:
            print(f"  L1 命中! key={cache_key}")
            return cached

        print("  L1 未命中")

        # 2. 查 L2
        cached = await self.l2.get(cache_key)
        if cached is not None:
            print("  L2 命中! 回填 L1...")
            self.l1.set(cache_key, cached, ttl=60)
            return cached

        print("  L2 未命中")

        # 3. 查数据源
        print("  从数据源加载...")
        item = await self.source.get(item_id)

        if item is not None:
            # 4. 回填 L2 和 L1
            print("  回填 L2 和 L1...")
            await self.l2.set(cache_key, item, ttl=300)
            self.l1.set(cache_key, item, ttl=60)

        return item

    async def invalidate(self, item_id: int) -> None:
        """失效缓存"""
        cache_key = self._make_key(item_id)
        self.l1.delete(cache_key)
        await self.l2.delete(cache_key)
        print(f"  已删除 L1 和 L2: {cache_key}")


# ==================== 测试代码 ====================


async def test_multi_level_cache():
    """测试多级缓存"""
    print("\n" + "=" * 60)
    print("多级缓存测试")
    print("=" * 60)

    # 初始化组件
    l1 = L1Cache()
    l2 = L2Cache()
    source = DataSource()
    cache = MultiLevelCache(l1, l2, source)

    # 测试 1: 首次查询
    print("\n[1] 首次查询 id=1")
    result = await cache.get(1)
    print(f"    结果: {result}")

    # 测试 2: 再次查询（L1 命中）
    print("\n[2] 再次查询 id=1 (L1 应命中)")
    result = await cache.get(1)
    print(f"    结果: {result}")

    # 测试 3: 删除缓存
    print("\n[3] 删除 id=1 的缓存")
    await cache.invalidate(1)

    # 测试 4: 查询（缓存已删除）
    print("\n[4] 查询 id=1 (缓存已删除，应重新加载)")
    result = await cache.get(1)
    print(f"    结果: {result}")

    # 测试 5: 并发查询
    print("\n[5] 并发查询 id=2 (5 个请求)")
    results = await asyncio.gather(*[cache.get(2) for _ in range(5)])
    print(f"    所有结果一致: {len(set(str(r) for r in results)) == 1}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_multi_level_cache())
