# examples/02_cache_decorator.py
"""
缓存装饰器演示 - 使用 Python 装饰器简化缓存逻辑

本模块演示如何创建可复用的缓存装饰器。
"""

from __future__ import annotations

import asyncio
import hashlib
import json
from functools import wraps
from typing import Any, Callable, TypeVar
T = TypeVar("T")


# ==================== 模拟缓存 ====================


class MockCache:
    """模拟缓存（内存版）"""

    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        """获取缓存"""
        if key in self._store:
            value, expiry = self._store[key]
            if expiry > asyncio.get_event_loop().time():
                return value
            del self._store[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """设置缓存"""
        expiry = asyncio.get_event_loop().time() + ttl
        self._store[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """删除缓存"""
        self._store.pop(key, None)

    def clear(self) -> None:
        """清空缓存"""
        self._store.clear()


# 全局缓存实例
cache = MockCache()


# ==================== 缓存装饰器 ====================


def cache_result(
    ttl: int = 300,
    key_prefix: str = "",
    include_args: bool = True,
):
    """
    缓存函数结果的装饰器

    Args:
        ttl: 缓存过期时间（秒）
        key_prefix: 缓存键前缀
        include_args: 是否将函数参数包含在缓存键中
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            # 生成缓存键
            cache_key = _generate_cache_key(func, args, kwargs, key_prefix, include_args)

            # 尝试获取缓存
            cached = cache.get(cache_key)
            if cached is not None:
                print(f"  [缓存命中] {func.__name__} -> {cache_key}")
                return cached

            # 执行函数
            print(f"  [缓存未命中] {func.__name__} -> 执行函数")
            result = func(*args, **kwargs)

            # 缓存结果
            if result is not None:
                cache.set(cache_key, result, ttl)

            return result

        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            # 生成缓存键
            cache_key = _generate_cache_key(func, args, kwargs, key_prefix, include_args)

            # 尝试获取缓存
            cached = cache.get(cache_key)
            if cached is not None:
                print(f"  [缓存命中] {func.__name__} -> {cache_key}")
                return cached

            # 执行函数
            print(f"  [缓存未命中] {func.__name__} -> 执行函数")
            result = await func(*args, **kwargs)

            # 缓存结果
            if result is not None:
                cache.set(cache_key, result, ttl)

            return result

        # 根据函数类型返回合适的装饰器
        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


def _generate_cache_key(
    func: Callable, args: tuple, kwargs: dict, key_prefix: str, include_args: bool
) -> str:
    """生成缓存键"""
    parts = [key_prefix or func.__module__, func.__name__]

    if include_args and (args or kwargs):
        # 序列化参数
        arg_str = json.dumps(
            {"args": args[1:], "kwargs": kwargs},  # 跳过 self
            sort_keys=True,
            default=str,
        )
        arg_hash = hashlib.md5(arg_str.encode()).hexdigest()[:8]
        parts.append(arg_hash)

    return ":".join(parts)


# ==================== 使用示例 ====================


@cache_result(ttl=60, key_prefix="user")
async def get_user(user_id: int) -> dict:
    """获取用户信息"""
    await asyncio.sleep(0.1)  # 模拟数据库查询
    return {"id": user_id, "username": f"user_{user_id}", "email": f"user{user_id}@example.com"}


@cache_result(ttl=300, key_prefix="product")
def get_product(product_id: int, category: str = "all") -> dict:
    """获取产品信息"""
    import time

    time.sleep(0.1)  # 模拟数据库查询
    return {"id": product_id, "name": f"Product {product_id}", "category": category, "price": 99.99}


@cache_result(ttl=180, key_prefix="search")
async def search_products(query: str, page: int = 1, page_size: int = 20) -> dict:
    """搜索产品"""
    await asyncio.sleep(0.15)  # 模拟搜索延迟
    return {
        "query": query,
        "page": page,
        "page_size": page_size,
        "total": 100,
        "items": [{"id": i, "name": f"Item {i}"} for i in range(page_size)],
    }


# ==================== 演示 ====================


async def demo_basic_cache():
    """演示基础缓存"""
    print("\n" + "=" * 60)
    print("基础缓存装饰器演示")
    print("=" * 60)

    # 清空缓存
    cache.clear()

    # 首次调用 - 缓存未命中
    print("\n[1] 首次获取用户（应执行查询）")
    user = await get_user(1)
    print(f"    结果: {user}")

    # 再次调用 - 缓存命中
    print("\n[2] 再次获取同一用户（应命中缓存）")
    user = await get_user(1)
    print(f"    结果: {user}")


async def demo_different_args():
    """演示不同参数生成不同缓存"""
    print("\n" + "=" * 60)
    print("不同参数生成不同缓存")
    print("=" * 60)

    cache.clear()

    # 同一函数，不同参数
    print("\n[1] 获取产品 (id=1, category=electronics)")
    p1 = get_product(1, category="electronics")
    print(f"    结果: {p1}")

    print("\n[2] 获取产品 (id=1, category=clothing)")
    p2 = get_product(1, category="clothing")
    print(f"    结果: {p2}")

    print("\n[3] 再次获取产品 (id=1, category=electronics)")
    p3 = get_product(1, category="electronics")
    print(f"    结果: {p3}")


async def demo_search_cache():
    """演示搜索缓存"""
    print("\n" + "=" * 60)
    print("搜索缓存演示")
    print("=" * 60)

    cache.clear()

    # 分页搜索
    print("\n[1] 搜索 'laptop' (第1页)")
    result1 = await search_products("laptop", page=1)
    print(f"    找到 {result1['total']} 条结果")

    print("\n[2] 搜索 'laptop' (第2页)")
    result2 = await search_products("laptop", page=2)
    print(f"    找到 {result2['total']} 条结果")

    print("\n[3] 再次搜索 'laptop' (第1页) - 应命中缓存")
    result3 = await search_products("laptop", page=1)
    print(f"    找到 {result3['total']} 条结果")


async def main():
    """主函数"""
    await demo_basic_cache()
    await demo_different_args()
    await demo_search_cache()

    print("\n" + "=" * 60)
    print("装饰器缓存演示完成！")
    print("=" * 60)
    print("\n关键点:")
    print("  1. 装饰器自动处理缓存逻辑")
    print("  2. 不同参数生成不同的缓存键")
    print("  3. 支持同步和异步函数")
    print("  4. 可配置 TTL、前缀等参数")


if __name__ == "__main__":
    asyncio.run(main())
