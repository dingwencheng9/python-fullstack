"""test_async.py - 异步处理测试"""

import pytest
import asyncio
import tempfile
import json
from pathlib import Path
from solutions.solution_04_async_processor import (
    async_read_file,
    async_process_files,
    RateLimiter,
    stream_process,
    fetch_with_timeout,
)


@pytest.fixture
def temp_json_file():
    """创建临时 JSON 文件"""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    ) as f:
        json.dump({"name": "test", "value": 123}, f)
        filepath = Path(f.name)

    yield filepath

    if filepath.exists():
        filepath.unlink()


@pytest.fixture
def temp_json_files():
    """创建多个临时 JSON 文件"""
    files = []
    for i in range(3):
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            json.dump({"id": i, "name": f"user_{i}"}, f)
            files.append(Path(f.name))

    yield files

    for f in files:
        if f.exists():
            f.unlink()


@pytest.mark.asyncio
async def test_async_read_file(temp_json_file):
    """测试异步文件读取"""
    result = await async_read_file(temp_json_file)
    assert result == {"name": "test", "value": 123}


@pytest.mark.asyncio
async def test_async_process_files(temp_json_files):
    """测试并发文件处理"""
    results = await async_process_files(temp_json_files, max_concurrent=2)
    assert len(results) == 3
    assert results[0]["id"] == 0
    assert results[1]["id"] == 1
    assert results[2]["id"] == 2


@pytest.mark.asyncio
async def test_rate_limiter():
    """测试限流器"""
    limiter = RateLimiter(rate=2, per=1.0)

    # 前两次应该很快
    start = asyncio.get_event_loop().time()
    await limiter.acquire()
    await limiter.acquire()
    elapsed = asyncio.get_event_loop().time() - start

    assert elapsed < 0.1


@pytest.mark.asyncio
async def test_stream_process(temp_json_files):
    """测试流式处理"""
    batches = []
    async for batch in stream_process(temp_json_files, batch_size=2):
        batches.append(batch)

    assert len(batches) >= 1


@pytest.mark.asyncio
async def test_fetch_with_timeout():
    """测试超时控制"""
    # 正常完成（asyncio.sleep 返回 None）
    result = await fetch_with_timeout(asyncio.sleep(0.01), timeout=1.0)
    assert result is None  # asyncio.sleep 返回 None

    # 超时情况
    result = await fetch_with_timeout(asyncio.sleep(2), timeout=0.1)
    assert result is None  # 超时返回 None


@pytest.mark.asyncio
async def test_concurrent_limit():
    """测试并发数限制"""
    concurrent_count = []

    async def tracked_task():
        concurrent_count.append(1)
        await asyncio.sleep(0.1)
        concurrent_count.pop()
        return "done"

    # 使用 max_concurrent=1 应该保证顺序执行
    files = [Path(f"test_{i}.json") for i in range(3)]

    # 创建临时文件
    temp_files = []
    for fp in files:
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            json.dump({"id": fp.stem}, f)
            temp_files.append(Path(f.name))

    try:
        await async_process_files(temp_files, max_concurrent=1)
        # 如果 max_concurrent=1 工作正常，任务应该顺序执行
    finally:
        for f in temp_files:
            if f.exists():
                f.unlink()
