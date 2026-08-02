"""

from __future__ import annotations

练习 3: 并发控制 - 参考答案

===============================================================================
解题思路: asyncio.gather, Semaphore, Lock 控制异步并发
===============================================================================
"""

import asyncio
import time


async def download_file(file_id: int, delay: float = 0.5) -> dict[str, object]:
    """模拟下载文件"""
    print(f"开始下载文件 {file_id}")
    await asyncio.sleep(delay)
    print(f"完成下载文件 {file_id}")
    return {"file_id": file_id, "size": file_id * 100}


async def download_all_parallel(file_ids: list[int]) -> list[dict[str, object]]:
    """并发下载所有文件"""
    tasks = [download_file(fid) for fid in file_ids]
    results = await asyncio.gather(*tasks)
    return results


class RateLimiter:
    """速率限制器"""

    def __init__(self, max_concurrent: int = 3):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch(self, url: str) -> str:
        """限流获取数据"""
        async with self.semaphore:
            print(f"获取 {url}")
            await asyncio.sleep(0.5)
            print(f"完成 {url}")
            return f"Data from {url}"


class Counter:
    """线程安全计数器"""

    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        """原子递增"""
        async with self.lock:
            current = self.value
            await asyncio.sleep(0.001)  # 模拟处理时间
            self.value = current + 1


async def test_gather():
    """测试并发下载"""
    print("测试 1: asyncio.gather()")
    start = time.time()
    await download_all_parallel([1, 2, 3])
    elapsed = time.time() - start
    print(f"✅ 下载完成，耗时 {elapsed:.2f}秒\n")


async def test_rate_limiter():
    """测试速率限制"""
    print("测试 2: Semaphore 限流")
    limiter = RateLimiter(max_concurrent=2)
    urls = [f"http://api.example.com/{i}" for i in range(5)]
    await asyncio.gather(*[limiter.fetch(url) for url in urls])
    print("✅ 限流测试通过\n")


async def test_lock():
    """测试锁"""
    print("测试 3: Lock 保护共享资源")
    counter = Counter()
    await asyncio.gather(*[counter.increment() for _ in range(100)])
    assert counter.value == 100
    print(f"✅ 计数器值: {counter.value}\n")


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("练习 3: 并发控制")
    print("=" * 60)
    print()

    await test_gather()
    await test_rate_limiter()
    await test_lock()

    print("=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
