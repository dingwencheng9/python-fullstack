"""P05 练习 2: Redis 缓存与 Celery 任务"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Optional, Any
from enum import Enum

# ============ 缓存实现 ============

class CacheLevel(str, Enum):
    L1_LOCAL = "l1_local"  # 本地 LRU 缓存
    L2_REDIS = "l2_redis"  # Redis 分布式缓存

@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    sets: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

stats = CacheStats()

# 简化的 L1 本地缓存
class L1Cache:
    """L1 本地 LRU 缓存"""

    def __init__(self, max_size: int = 1000):
        self._cache: dict[str, tuple[Any, float]] = {}  # key -> (value, expiry)
        self.max_size = max_size

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key in self._cache:
            value, expiry = self._cache[key]
            if expiry > time.time():
                stats.hits += 1
                return value
            else:
                del self._cache[key]
        stats.misses += 1
        return None

    def set(self, key: str, value: Any, ttl: int = 300):
        """设置缓存值"""
        # LRU: 如果满了，删除最老的
        if len(self._cache) >= self.max_size and key not in self._cache:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]

        self._cache[key] = (value, time.time() + ttl)
        stats.sets += 1

    def delete(self, key: str):
        """删除缓存"""
        self._cache.pop(key, None)

l1_cache = L1Cache()

# ============ 练习题目 ============

def exercise_01_l1_cache():
    """练习 1: 实现 L1 本地缓存"""
    # TODO: 使用 L1Cache 实现任务数据缓存

    # 学员应实现:
    # task_data = {"id": 1, "title": "完成报告", "status": "pending", "assignee": "alice"}
    # l1_cache.set("task:1", task_data, ttl=300)
    # result = l1_cache.get("task:1")
    # assert result == task_data

    print("练习 1: L1 本地缓存")
    print("- 使用 l1_cache.set(key, value, ttl)")
    print("- 使用 l1_cache.get(key) 获取值")
    print(f"- 当前缓存大小: {len(l1_cache._cache)}")


def exercise_02_cache_invalidation():
    """练习 2: 缓存失效策略"""
    # TODO: 实现缓存失效

    async def test_invalidation():
        # 1. 设置缓存
        # l1_cache.set("task:1", {"id": 1, "title": "New Task"})

        # 2. 任务更新时删除缓存
        async def update_task(task_id: int, updates: dict):
            # 模拟数据库更新
            await asyncio.sleep(0.1)

            # 删除旧缓存
            # l1_cache.delete(f"task:{task_id}")

            # 返回更新后的数据
            return {"id": task_id, **updates}

        # 3. 下次获取时重新加载
        # l1_cache.set("task:1", await update_task(1, {"title": "Updated Task"}))

        print("练习 2: 缓存失效策略")
        print("- 更新时删除缓存: l1_cache.delete(key)")
        print("- 读取时重新加载")

    asyncio.run(test_invalidation())


def exercise_03_cache_pattern():
    """练习 3: 缓存模式 (Cache-Aside)"""
    # TODO: 实现 Cache-Aside 模式

    async def get_user_with_cache(user_id: int):
        """Cache-Aside 模式: 先查缓存，缓存未命中再查数据库"""
        # 学员应实现:
        # cache_key = f"user:{user_id}"
        #
        # # 1. 先查缓存
        # cached = l1_cache.get(cache_key)
        # if cached:
        #     return cached
        #
        # # 2. 缓存未命中，查数据库
        # user = await db.fetch_one("SELECT * FROM users WHERE id = ?", user_id)
        #
        # # 3. 写入缓存
        # l1_cache.set(cache_key, user, ttl=600)
        #
        # return user
        return {"id": user_id, "name": "Alice"}

    async def test_cache_aside():
        # 第一次调用 (缓存未命中)
        # result1 = await get_user_with_cache(1)
        # print(f"Cache misses: {stats.misses}")

        # 第二次调用 (缓存命中)
        # result2 = await get_user_with_cache(1)
        # print(f"Cache hits: {stats.hits}")
        # print(f"Hit rate: {stats.hit_rate:.1%}")

        print("练习 3: Cache-Aside 模式")
        print("- 先查缓存，未命中查数据库")
        print("- 回填缓存供下次使用")

    asyncio.run(test_cache_aside())


def exercise_04_celery_task():
    """练习 4: Celery 异步任务"""
    # TODO: 实现 Celery 任务定义

    # 以下是 Celery 任务的结构定义
    # 实际使用需要安装 celery: pip install celery

    def define_celery_task():
        """定义 Celery 任务"""
        # from celery import Celery
        # app = Celery('tasks', broker='redis://localhost:6379')
        #
        # @app.task
        # def send_notification(user_id: int, message: str):
        #     '''发送通知任务'''
        #     # 实际发送逻辑
        #     print(f"Sending to user {user_id}: {message}")
        #     return {"status": "sent", "user_id": user_id}
        #
        # @app.task(bind=True, max_retries=3)
        # def process_data(self, data: dict):
        #     '''带重试的任务'''
        #     try:
        #         return process(data)
        #     except Exception as exc:
        #         raise self.retry(exc=exc, countdown=2 ** self.request.retries)

        print("练习 4: Celery 任务定义")
        print("- 使用 @app.task 装饰器")
        print("- bind=True 时第一个参数是 self")
        print("- max_retries=3 设置最大重试次数")


def exercise_05_task_chain():
    """练习 5: 任务链"""
    # TODO: 实现任务链和任务组

    def define_task_chain():
        """定义任务链"""
        # from celery import chain, group
        #
        # # 任务链: 依次执行
        # workflow = chain(
        #     task1.s(),
        #     task2.s(),
        #     task3.s()
        # )
        # result = workflow.apply_async()
        #
        # # 任务组: 并行执行
        # parallel_work = group(
        #     send_email.s(recipient) for recipient in recipients
        # )
        # result = parallel_work.apply_async()

        print("练习 5: 任务链")
        print("- chain(): 顺序执行")
        print("- group(): 并行执行")
        print("- chord(): 全部完成后汇总")


def exercise_06_cache_warming():
    """练习 6: 缓存预热"""
    # TODO: 实现缓存预热

    async def warm_cache():
        """预热缓存: 系统启动时加载热点数据"""
        # 热点任务列表
        hot_tasks = [1, 2, 3, 4, 5]

        for task_id in hot_tasks:
            # 从数据库加载
            # task = await db.fetch_one("SELECT * FROM tasks WHERE id = ?", task_id)

            # 写入缓存，TTL 长一些
            # l1_cache.set(f"task:{task_id}", task, ttl=3600)

            print(f"预热缓存: task:{task_id}")

        print("练习 6: 缓存预热")
        print("- 系统启动时加载热点数据")
        print("- 设置较长 TTL")


# ============ 运行测试 ============

if __name__ == "__main__":
    print("=" * 60)
    print("P05 练习 2: Redis 缓存与 Celery 任务")
    print("=" * 60)

    exercise_01_l1_cache()
    print()

    exercise_02_cache_invalidation()
    print()

    exercise_03_cache_pattern()
    print()

    exercise_04_celery_task()
    print()

    exercise_05_task_chain()
    print()

    exercise_06_cache_warming()
    print()

    print("=" * 60)
    print("所有练习完成！")
    print("=" * 60)
