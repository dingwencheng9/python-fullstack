# exercises/exercise_01_cache_design.py
"""
练习 1: 缓存设计实践

本练习要求你实现一个完整的多级缓存系统。
"""

from __future__ import annotations

import asyncio
from typing import Any
# ==================== 练习题目 ====================

"""
## 练习要求

实现一个 L1/L2 两级缓存系统：

### 架构

```
请求 → L1 (本地缓存) → L2 (分布式缓存) → 数据源
```

### 要求

1. **L1 本地缓存**:
   - 使用 dict 模拟内存缓存
   - TTL 支持（简化版可不实现）

2. **L2 分布式缓存**:
   - 使用 dict 模拟 Redis
   - 支持 TTL

3. **多级查找逻辑**:
   - 先查 L1，命中则返回
   - L1 未命中，查 L2
   - L2 命中，回填 L1
   - L2 也未命中，查数据源

4. **数据回填**:
   - 查询到数据后，回填到 L2
   - 同时回填到 L1

5. **缓存失效**:
   - 同时删除 L1 和 L2

### 示例输出

```
=== 多级缓存演示 ===
[1] 首次查询 id=1
  L1 未命中
  L2 未命中
  从数据源加载
  回填 L2 和 L1
  结果: {'id': 1, 'name': 'Product A'}

[2] 再次查询 id=1
  L1 命中！
  结果: {'id': 1, 'name': 'Product A'}

[3] 删除 id=1
  已删除 L1 和 L2

[4] 查询 id=1 (缓存已删除)
  L1 未命中
  L2 未命中
  从数据源加载
  结果: {'id': 1, 'name': 'Product A'}
```
"""


# ==================== 数据源（无需修改） ====================


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


# ==================== L1 本地缓存（需要实现） ====================


class L1Cache:
    """L1 本地缓存"""

    def __init__(self):
        # TODO: 实现本地缓存存储
        pass

    def get(self, key: str) -> Any | None:
        """从本地缓存获取"""
        # TODO: 实现获取逻辑
        pass

    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        """设置本地缓存"""
        # TODO: 实现设置逻辑
        pass

    def delete(self, key: str) -> None:
        """删除本地缓存"""
        # TODO: 实现删除逻辑
        pass


# ==================== L2 分布式缓存（需要实现） ====================


class L2Cache:
    """L2 分布式缓存"""

    def __init__(self):
        # TODO: 实现分布式缓存存储
        pass

    async def get(self, key: str) -> Any | None:
        """从分布式缓存获取"""
        # TODO: 实现获取逻辑（可以是异步）
        pass

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """设置分布式缓存"""
        # TODO: 实现设置逻辑
        pass

    async def delete(self, key: str) -> None:
        """删除分布式缓存"""
        # TODO: 实现删除逻辑
        pass


# ==================== 多级缓存管理器（需要实现） ====================


class MultiLevelCache:
    """
    多级缓存管理器

    负责协调 L1 和 L2 缓存，提供统一接口。
    """

    def __init__(self, l1: L1Cache, l2: L2Cache, source: DataSource):
        self.l1 = l1
        self.l2 = l2
        self.source = source

    async def get(self, item_id: int) -> dict | None:
        """
        多级缓存查询

        流程：
        1. 先查 L1
        2. L1 命中则返回
        3. L1 未命中，查 L2
        4. L2 命中，回填 L1，返回
        5. L2 也未命中，查数据源
        6. 回填 L2 和 L1，返回
        """
        # TODO: 实现多级查找逻辑
        pass

    async def invalidate(self, item_id: int) -> None:
        """
        失效缓存

        同时删除 L1 和 L2 中的缓存。
        """
        # TODO: 实现失效逻辑
        pass


# ==================== 测试代码（无需修改） ====================


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


# ==================== 验收标准 ====================

"""
验收标准：

1. [ ] L1Cache.get() 能正确获取缓存值
2. [ ] L1Cache.set() 能正确设置缓存值
3. [ ] L1Cache.delete() 能正确删除缓存值
4. [ ] L2Cache 异步方法能正常工作
5. [ ] MultiLevelCache.get() 实现正确的多级查找逻辑
6. [ ] MultiLevelCache.invalidate() 能同时删除 L1 和 L2
7. [ ] L2 命中时能回填 L1
8. [ ] 数据源查询后能回填 L1 和 L2
9. [ ] 并发查询不会导致数据不一致
"""
