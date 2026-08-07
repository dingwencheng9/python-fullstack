"""P02 参考答案 4: 异步数据处理"""

import asyncio
import json
from pathlib import Path
from typing import AsyncIterator


async def async_read_file(filepath: Path) -> dict:
    """异步读取 JSON 文件"""
    # 在线程中执行同步 IO 操作
    loop = asyncio.get_event_loop()
    content = await loop.run_in_executor(
        None, filepath.read_text, "utf-8"
    )
    return json.loads(content)


async def async_process_files(
    filepaths: list[Path],
    max_concurrent: int = 5
) -> list[dict]:
    """并发处理多个文件"""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_one(fp: Path) -> dict:
        async with semaphore:
            return await async_read_file(fp)

    return await asyncio.gather(*[process_one(fp) for fp in filepaths])


class RateLimiter:
    """异步限流器"""
    def __init__(self, rate: float, per: float = 1.0) -> None:
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.last_update = asyncio.get_event_loop().time()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """获取令牌"""
        async with self._lock:
            while self.tokens < 1:
                self._refill()
                await asyncio.sleep(0.01)
            self.tokens -= 1

    def _refill(self) -> None:
        """重新填充令牌"""
        loop = asyncio.get_event_loop()
        now = loop.time()
        elapsed = now - self.last_update
        self.tokens = min(self.rate, self.tokens + elapsed * self.rate / self.per)
        self.last_update = now


async def stream_process(
    filepaths: list[Path],
    batch_size: int = 100
) -> AsyncIterator[dict]:
    """流式处理数据"""
    for fp in filepaths:
        data = await async_read_file(fp)
        # 处理字典或列表
        if isinstance(data, list):
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                yield {"file": fp.name, "batch": batch, "size": len(batch)}
        else:
            yield {"file": fp.name, "data": data}


async def fetch_with_timeout(coro, timeout: float) -> any:
    """带超时的异步操作"""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return None
