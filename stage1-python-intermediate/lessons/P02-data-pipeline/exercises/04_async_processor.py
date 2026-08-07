"""P02 练习 4: 异步数据处理

课程编号: P02
所属课程: Stage 1 - Python 进阶
练习编号: 04
难度: ⭐⭐⭐⭐
知识点: async/await + gather + Semaphore

任务：
1. 实现 async_read_file 异步读取
2. 实现 async_process_files 并发处理
3. 实现 RateLimiter 限流器
4. 实现带超时的异步处理

运行方式:
    python exercises/04_async_processor.py

预期行为：
    async def main():
        results = await async_process_files(["a.json", "b.json", "c.json"])
        assert len(results) == 3
"""

import asyncio
from pathlib import Path
from typing import AsyncIterator
import json


# ============================================================
# 1. async_read_file
# ============================================================

# TODO: 实现异步文件读取
async def async_read_file(filepath: Path) -> dict:
    """异步读取 JSON 文件

    预期行为:
        # 创建测试文件
        test_file = Path("test.json")
        test_file.write_text('{"name": "test"}')

        # 异步读取
        result = await async_read_file(test_file)
        assert result == {"name": "test"}

        # 清理
        test_file.unlink()
    """
    # TODO: 实现异步文件读取
    # 提示: 使用 asyncio.to_thread 在线程中执行同步 IO
    # 或者直接使用 await asyncio.sleep(0) 模拟异步
    pass


# ============================================================
# 2. async_process_files
# ============================================================

# TODO: 实现并发文件处理
async def async_process_files(
    filepaths: list[Path],
    max_concurrent: int = 5
) -> list[dict]:
    """并发处理多个文件

    参数:
        filepaths: 文件路径列表
        max_concurrent: 最大并发数

    预期行为:
        results = await async_process_files([fp1, fp2, fp3], max_concurrent=2)
        assert len(results) == 3
    """
    # TODO: 实现并发处理逻辑
    # 提示: 使用 asyncio.Semaphore 限制并发数
    # 使用 asyncio.gather 并发执行任务
    pass


# ============================================================
# 3. RateLimiter 限流器
# ============================================================

# TODO: 实现限流器
class RateLimiter:
    """异步限流器

    使用令牌桶算法：
    - rate: 每段时间的最大调用次数
    - per: 时间段（秒）
    """
    def __init__(self, rate: float, per: float = 1.0) -> None:
        self.rate = rate
        self.per = per
        self.tokens = rate
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """获取令牌（等待直到可用）

        预期行为:
            limiter = RateLimiter(rate=2, per=1.0)
            await limiter.acquire()  # 获取令牌
            await limiter.acquire()  # 获取令牌
            # 第三次可能需要等待
        """
        # TODO: 实现令牌获取逻辑
        # 1. 获取锁
        # 2. 如果没有令牌，等待补充
        # 3. 消耗一个令牌
        # 4. 释放锁
        pass


# ============================================================
# 4. 流式处理
# ============================================================

# TODO: 实现流式处理
async def stream_process(
    filepaths: list[Path],
    batch_size: int = 100
) -> AsyncIterator[dict]:
    """流式处理数据

    预期行为:
        async for batch in stream_process([fp], batch_size=2):
            print(batch)
    """
    # TODO: 实现流式处理逻辑
    # 提示: 使用 async for 和 yield
    pass


# ============================================================
# 5. 带超时的异步处理
# ============================================================

async def fetch_with_timeout(coro, timeout: float) -> any:
    """带超时的异步操作

    预期行为:
        result = await fetch_with_timeout(asyncio.sleep(0.1), timeout=1.0)
        assert result is True  # 正常完成

        result = await fetch_with_timeout(asyncio.sleep(2), timeout=0.5)
        assert result is None  # 超时返回 None
    """
    # TODO: 实现超时控制
    # 提示: 使用 asyncio.wait_for
    pass


# ============================================================
# 测试
# ============================================================

import tempfile
import os

def create_temp_json_files(count: int) -> list[Path]:
    """创建临时 JSON 文件"""
    files = []
    for i in range(count):
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            json.dump({"id": i, "name": f"user_{i}"}, f)
            files.append(Path(f.name))
    return files


def cleanup_temp_files(files: list[Path]) -> None:
    """清理临时文件"""
    for f in files:
        if f.exists():
            f.unlink()


async def test_async_read_file():
    """测试异步文件读取"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    ) as f:
        json.dump({"name": "test", "value": 123}, f)
        filepath = Path(f.name)

    try:
        result = await async_read_file(filepath)
        assert result == {"name": "test", "value": 123}
        print("✓ async_read_file 测试通过")
    finally:
        filepath.unlink()


async def test_async_process_files():
    """测试并发文件处理"""
    files = create_temp_json_files(3)

    try:
        results = await async_process_files(files, max_concurrent=2)
        assert len(results) == 3
        print("✓ async_process_files 测试通过")
    finally:
        cleanup_temp_files(files)


async def test_rate_limiter():
    """测试限流器"""
    limiter = RateLimiter(rate=2, per=1.0)

    import time
    start = time.perf_counter()
    await limiter.acquire()
    await limiter.acquire()
    elapsed = time.perf_counter() - start

    # 前两次调用应该很快
    assert elapsed < 0.1, f"前两次应该快速完成: {elapsed}"
    print("✓ RateLimiter 测试通过")


async def test_stream_process():
    """测试流式处理"""
    files = create_temp_json_files(2)

    try:
        batches = []
        async for batch in stream_process(files, batch_size=2):
            batches.append(batch)

        # 至少应该有一个批次
        assert len(batches) >= 1
        print("✓ stream_process 测试通过")
    finally:
        cleanup_temp_files(files)


async def test_fetch_with_timeout():
    """测试超时控制"""
    # 正常完成
    result = await fetch_with_timeout(asyncio.sleep(0.1), timeout=1.0)
    assert result is True

    # 超时情况
    result = await fetch_with_timeout(asyncio.sleep(2), timeout=0.1)
    assert result is None
    print("✓ fetch_with_timeout 测试通过")


async def main():
    """运行所有测试"""
    print("=" * 50)
    print("P02 练习 4: 异步数据处理")
    print("=" * 50)

    try:
        await test_async_read_file()
        await test_async_process_files()
        await test_rate_limiter()
        await test_stream_process()
        await test_fetch_with_timeout()
        print("\n🎉 所有测试通过!")
    except (AssertionError, NotImplementedError) as e:
        print(f"\n❌ 测试失败: {e}")
        print("请实现 TODO 部分")


if __name__ == "__main__":
    asyncio.run(main())
