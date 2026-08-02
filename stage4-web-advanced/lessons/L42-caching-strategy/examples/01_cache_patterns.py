# examples/01_cache_patterns.py
"""
缓存策略模式演示 - Cache-Aside、Read-Through、Write-Through

本模块演示三种最常用的缓存策略模式。
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime

# ==================== 数据模型 ====================


@dataclass
class User:
    """用户模型"""

    id: int
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)


# ==================== 模拟数据库 ====================


class MockDatabase:
    """模拟数据库"""

    def __init__(self):
        self._users: dict[int, dict] = {}

    async def get_user(self, user_id: int) -> dict | None:
        """从数据库获取用户"""
        await asyncio.sleep(0.01)  # 模拟 DB 延迟
        return self._users.get(user_id)

    async def create_user(self, user_id: int, username: str, email: str) -> dict:
        """创建用户"""
        await asyncio.sleep(0.01)
        user = {"id": user_id, "username": username, "email": email}
        self._users[user_id] = user
        return user

    async def update_user(self, user_id: int, **kwargs) -> dict | None:
        """更新用户"""
        await asyncio.sleep(0.01)
        if user_id in self._users:
            self._users[user_id].update(kwargs)
            return self._users[user_id]
        return None


# ==================== 模拟缓存 ====================


class MockCache:
    """模拟缓存"""

    def __init__(self):
        self._store: dict[str, tuple[dict, float]] = {}  # key -> (value, expiry)

    async def get(self, key: str) -> dict | None:
        """获取缓存"""
        if key in self._store:
            value, expiry = self._store[key]
            if expiry > asyncio.get_event_loop().time():
                return value
            del self._store[key]
        return None

    async def set(self, key: str, value: dict, ttl: int = 300) -> None:
        """设置缓存"""
        expiry = asyncio.get_event_loop().time() + ttl
        self._store[key] = (value, expiry)

    async def delete(self, key: str) -> None:
        """删除缓存"""
        self._store.pop(key, None)

    async def clear(self) -> None:
        """清空缓存"""
        self._store.clear()


# ==================== 缓存策略实现 ====================


class CacheAside:
    """
    旁路缓存模式（Cache-Aside）

    读流程：
    1. 先查缓存
    2. 缓存命中则返回
    3. 缓存未命中，查数据库
    4. 写入缓存，返回数据

    写流程：
    1. 先更新数据库
    2. 删除缓存（而不是更新）

    优点：实现简单，一致性好
    缺点：首次访问较慢
    """

    def __init__(self, cache: MockCache, db: MockDatabase):
        self.cache = cache
        self.db = db

    def _make_key(self, prefix: str, id: int) -> str:
        return f"{prefix}:{id}"

    async def get_user(self, user_id: int) -> dict | None:
        """读取用户"""
        cache_key = self._make_key("user", user_id)

        # 1. 先查缓存
        cached = await self.cache.get(cache_key)
        if cached:
            print(f"  [Cache-Aside] 缓存命中: user:{user_id}")
            return cached

        # 2. 缓存未命中，查数据库
        print("  [Cache-Aside] 缓存未命中，查询数据库...")
        user = await self.db.get_user(user_id)

        if user:
            # 3. 写入缓存
            await self.cache.set(cache_key, user, ttl=3600)
            print("  [Cache-Aside] 已写入缓存")

        return user

    async def update_user(self, user_id: int, **kwargs) -> dict | None:
        """更新用户"""
        cache_key = self._make_key("user", user_id)

        # 1. 更新数据库
        user = await self.db.update_user(user_id, **kwargs)

        # 2. 删除缓存（而不是更新）
        await self.cache.delete(cache_key)
        print(f"  [Cache-Aside] 已删除缓存: user:{user_id}")

        return user


class ReadThrough:
    """
    穿透读取模式（Read-Through）

    读流程：
    1. 先查缓存
    2. 缓存命中则返回
    3. 缓存未命中，自动调用 factory 加载数据
    4. 写入缓存，返回数据

    优点：调用方代码简洁
    缺点：缓存逻辑与业务逻辑耦合
    """

    def __init__(self, cache: MockCache, db: MockDatabase):
        self.cache = cache
        self.db = db

    async def get_user(self, user_id: int, ttl: int = 3600) -> dict | None:
        """读取用户，自动处理缓存"""
        cache_key = f"user:{user_id}"

        # 尝试获取缓存
        cached = await self.cache.get(cache_key)
        if cached:
            print(f"  [Read-Through] 缓存命中: user:{user_id}")
            return cached

        # 缓存未命中，自动加载
        print("  [Read-Through] 缓存未命中，自动加载数据...")

        # 定义数据加载器
        async def loader() -> dict | None:
            return await self.db.get_user(user_id)

        # 执行加载
        user = await loader()

        if user:
            await self.cache.set(cache_key, user, ttl=ttl)
            print("  [Read-Through] 已写入缓存")

        return user


class WriteThrough:
    """
    穿透写入模式（Write-Through）

    写流程：
    1. 先更新数据库
    2. 同步更新缓存

    优点：缓存始终是最新值
    缺点：写入延迟较高
    """

    def __init__(self, cache: MockCache, db: MockDatabase):
        self.cache = cache
        self.db = db

    async def update_user(self, user_id: int, **kwargs) -> dict | None:
        """更新用户，同时更新缓存"""
        cache_key = f"user:{user_id}"

        # 1. 更新数据库
        user = await self.db.update_user(user_id, **kwargs)

        if user:
            # 2. 同步更新缓存
            await self.cache.set(cache_key, user, ttl=3600)
            print("  [Write-Through] 已同步更新缓存")

        return user


# ==================== 演示 ====================


async def demo_cache_aside():
    """演示 Cache-Aside 模式"""
    print("\n" + "=" * 60)
    print("Cache-Aside 模式演示")
    print("=" * 60)

    cache = MockCache()
    db = MockDatabase()

    # 准备数据
    await db.create_user(1, "alice", "alice@example.com")

    strategy = CacheAside(cache, db)

    # 首次读取 - 缓存未命中
    print("\n[1] 首次读取用户")
    user = await strategy.get_user(1)
    print(f"    结果: {user}")

    # 再次读取 - 缓存命中
    print("\n[2] 再次读取用户（应命中缓存）")
    user = await strategy.get_user(1)
    print(f"    结果: {user}")

    # 更新用户
    print("\n[3] 更新用户")
    await strategy.update_user(1, username="alice_updated")
    print("    更新后缓存已删除")

    # 读取 - 缓存未命中（因为刚删除）
    print("\n[4] 更新后读取（缓存未命中）")
    user = await strategy.get_user(1)
    print(f"    结果: {user}")


async def demo_read_through():
    """演示 Read-Through 模式"""
    print("\n" + "=" * 60)
    print("Read-Through 模式演示")
    print("=" * 60)

    cache = MockCache()
    db = MockDatabase()

    # 准备数据
    await db.create_user(2, "bob", "bob@example.com")

    strategy = ReadThrough(cache, db)

    # 读取 - 缓存未命中
    print("\n[1] 首次读取用户")
    user = await strategy.get_user(2)
    print(f"    结果: {user}")

    # 再次读取 - 缓存命中
    print("\n[2] 再次读取用户（应命中缓存）")
    user = await strategy.get_user(2)
    print(f"    结果: {user}")


async def demo_write_through():
    """演示 Write-Through 模式"""
    print("\n" + "=" * 60)
    print("Write-Through 模式演示")
    print("=" * 60)

    cache = MockCache()
    db = MockDatabase()

    # 准备数据
    await db.create_user(3, "charlie", "charlie@example.com")

    strategy = WriteThrough(cache, db)

    # 预热缓存
    cache.set("user:3", await db.get_user(3), ttl=3600)
    print("[0] 预热缓存完成")

    # 更新用户
    print("\n[1] 更新用户")
    await strategy.update_user(3, username="charlie_updated")

    # 读取 - 缓存中已是最新值
    print("\n[2] 读取用户（缓存已是最新值）")
    cached = await cache.get("user:3")
    print(f"    缓存值: {cached}")


async def main():
    """主函数"""
    await demo_cache_aside()
    await demo_read_through()
    await demo_write_through()

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
