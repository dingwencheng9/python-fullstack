"""P02 示例 5: 异步数据处理

演示 L16 并发编程入门的核心概念：
- async/await 语法
- asyncio.gather 并发执行
- asyncio.create_task 任务创建
- AsyncIterator 流式处理
- Semaphore 限流

运行方式:
    python examples/05_async_processing.py
"""

import asyncio
import json
from pathlib import Path
from typing import AsyncIterator
import time


# ============================================================
# 1. 基础异步函数
# ============================================================

async def fetch_data(source: str) -> dict:
    """模拟异步数据获取"""
    # 模拟 I/O 延迟
    await asyncio.sleep(0.1)
    return {"source": source, "data": f"data_from_{source}"}


async def process_item(item: str) -> str:
    """模拟异步数据处理"""
    await asyncio.sleep(0.05)
    return item.upper()


# ============================================================
# 2. 并发执行
# ============================================================

async def concurrent_fetch(sources: list[str]) -> list[dict]:
    """并发获取多个数据源"""
    tasks = [fetch_data(source) for source in sources]
    results = await asyncio.gather(*tasks)
    return results


async def concurrent_process(items: list[str]) -> list[str]:
    """并发处理多个项目"""
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)


# ============================================================
# 3. 异步上下文管理器
# ============================================================

class AsyncFileReader:
    """异步文件读取器"""

    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
        self._file = None

    async def __aenter__(self) -> "AsyncFileReader":
        """进入异步上下文"""
        await asyncio.sleep(0)  # 模拟异步打开
        self._file = open(self.filepath, "r", encoding="utf-8")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出异步上下文"""
        if self._file:
            self._file.close()

    async def read(self) -> str:
        """异步读取文件"""
        await asyncio.sleep(0)
        if self._file:
            return self._file.read()
        return ""

    async def read_json(self) -> dict:
        """异步读取 JSON"""
        content = await self.read()
        return json.loads(content)


class AsyncFileWriter:
    """异步文件写入器"""

    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    async def __aenter__(self) -> "AsyncFileWriter":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    async def write(self, content: str) -> None:
        """异步写入文件"""
        await asyncio.sleep(0)  # 模拟异步写入
        self.filepath.write_text(content, encoding="utf-8")


# ============================================================
# 4. 异步迭代器
# ============================================================

async def async_range(start: int, stop: int) -> AsyncIterator[int]:
    """异步生成器：模拟异步 range"""
    for i in range(start, stop):
        await asyncio.sleep(0.01)  # 模拟异步操作
        yield i


async def async_file_lines(filepath: Path) -> AsyncIterator[str]:
    """异步逐行读取文件"""
    async with AsyncFileReader(filepath) as reader:
        content = await reader.read()
        for line in content.split("\n"):
            if line.strip():
                yield line


# ============================================================
# 5. 流式处理
# ============================================================

async def stream_process(
    items: list[dict],
    batch_size: int = 2
) -> AsyncIterator[list[dict]]:
    """流式处理数据批次"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        await asyncio.sleep(0.05)  # 模拟处理延迟
        yield batch


async def paginated_fetch(
    page_size: int = 10,
    max_pages: int = 5
) -> AsyncIterator[list[dict]]:
    """分页获取数据"""
    for page in range(max_pages):
        # 模拟 API 调用
        await asyncio.sleep(0.1)
        page_data = [
            {"page": page + 1, "index": page * page_size + i}
            for i in range(page_size)
        ]
        yield page_data


# ============================================================
# 6. 限流器
# ============================================================

class AsyncRateLimiter:
    """异步限流器"""

    def __init__(self, rate: float, per: float = 1.0) -> None:
        """限流器

        Args:
            rate: 每段时间内的最大调用次数
            per: 时间段（秒）
        """
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """获取令牌（等待直到可用）"""
        async with self._lock:
            while self.tokens < 1:
                await self._refill()
                await asyncio.sleep(0.01)
            self.tokens -= 1

    async def _refill(self) -> None:
        """重新填充令牌"""
        now = time.monotonic()
        elapsed = now - self.last_update
        self.tokens = min(self.rate, self.tokens + elapsed * self.rate / self.per)
        self.last_update = now


class SemaphoreLimiter:
    """信号量限流器"""

    def __init__(self, max_concurrent: int) -> None:
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def __aenter__(self) -> "SemaphoreLimiter":
        await self._semaphore.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self._semaphore.release()


# ============================================================
# 7. 超时控制
# ============================================================

async def fetch_with_timeout(coro, timeout: float) -> any:
    """带超时的异步操作"""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return None


async def resilient_fetch(source: str, retries: int = 3) -> dict | None:
    """带重试的异步获取"""
    for attempt in range(retries):
        try:
            return await asyncio.wait_for(
                fetch_data(source),
                timeout=1.0
            )
        except asyncio.TimeoutError:
            if attempt == retries - 1:
                return None
            await asyncio.sleep(0.5 * (attempt + 1))


# ============================================================
# 8. 异步生成器管道
# ============================================================

async def async_generator_pipeline(
    items: AsyncIterator[dict],
    *processors: callable
) -> AsyncIterator[dict]:
    """异步生成器管道"""
    async for item in items:
        for processor in processors:
            item = processor(item)
        yield item


def sync_processor(item: dict) -> dict:
    """同步处理器（在异步上下文中调用）"""
    item["processed"] = True
    return item


# ============================================================
# 演示函数
# ============================================================

async def demonstrate_basic_async():
    """演示基础异步"""
    print("\n=== 基础异步 ===")

    result = await fetch_data("api.example.com")
    print(f"获取结果: {result}")


async def demonstrate_concurrent():
    """演示并发执行"""
    print("\n=== 并发执行 ===")

    sources = ["api1", "api2", "api3", "api4", "api5"]

    # 顺序执行
    start = time.perf_counter()
    sequential_results = []
    for source in sources:
        result = await fetch_data(source)
        sequential_results.append(result)
    sequential_time = time.perf_counter() - start

    # 并发执行
    start = time.perf_counter()
    concurrent_results = await concurrent_fetch(sources)
    concurrent_time = time.perf_counter() - start

    print(f"顺序执行: {sequential_time:.3f}s, 获取 {len(sequential_results)} 条")
    print(f"并发执行: {concurrent_time:.3f}s, 获取 {len(concurrent_results)} 条")
    print(f"加速比: {sequential_time / concurrent_time:.1f}x")


async def demonstrate_async_context():
    """演示异步上下文管理器"""
    print("\n=== 异步上下文管理器 ===")

    # 创建测试文件
    test_file = Path(__file__).parent / "temp_test.json"
    test_file.write_text('{"name": "test", "value": 123}', encoding="utf-8")

    async with AsyncFileReader(test_file) as reader:
        data = await reader.read_json()
        print(f"JSON 数据: {data}")

    # 清理
    test_file.unlink()


async def demonstrate_async_iterator():
    """演示异步迭代器"""
    print("\n=== 异步迭代器 ===")

    print("async_range(1, 6):")
    async for i in async_range(1, 6):
        print(f"  {i}", end=" ")
    print()


async def demonstrate_stream():
    """演示流式处理"""
    print("\n=== 流式处理 ===")

    data = [{"id": i} for i in range(7)]
    print(f"输入数据: {len(data)} 条")

    batch_num = 0
    async for batch in stream_process(data, batch_size=3):
        batch_num += 1
        print(f"  批次 {batch_num}: {len(batch)} 条")


async def demonstrate_rate_limiter():
    """演示限流器"""
    print("\n=== 限流器 ===")

    limiter = AsyncRateLimiter(rate=2, per=1.0)

    start = time.perf_counter()
    for _ in range(5):
        await limiter.acquire()
        print(f"  获取令牌: {time.perf_counter() - start:.3f}s")
    total_time = time.perf_counter() - start

    print(f"5 次调用（限流 2/s）总耗时: {total_time:.2f}s")


async def demonstrate_semaphore():
    """演示信号量"""
    print("\n=== 信号量限流 ===")

    async def bounded_task(task_id: int) -> str:
        async with SemaphoreLimiter(max_concurrent=2):
            print(f"  任务 {task_id} 开始")
            await asyncio.sleep(0.1)
            print(f"  任务 {task_id} 完成")
            return f"task_{task_id}"

    start = time.perf_counter()
    results = await asyncio.gather(*[bounded_task(i) for i in range(4)])
    total_time = time.perf_counter() - start

    print(f"4 个任务（最多 2 并发）总耗时: {total_time:.3f}s")
    print(f"结果: {results}")


async def demonstrate_timeout():
    """演示超时控制"""
    print("\n=== 超时控制 ===")

    # 正常情况
    result = await fetch_with_timeout(fetch_data("fast"), timeout=1.0)
    print(f"快速请求: {result}")

    # 超时情况
    async def slow_fetch():
        await asyncio.sleep(2)
        return {"data": "slow"}

    result = await fetch_with_timeout(slow_fetch(), timeout=0.5)
    print(f"慢速请求（超时）: {result}")


async def demonstrate_resilient():
    """演示弹性获取"""
    print("\n=== 弹性获取 ===")

    # 模拟偶尔失败的 API
    call_count = [0]

    async def flaky_fetch():
        call_count[0] += 1
        if call_count[0] < 2:
            raise asyncio.TimeoutError("模拟超时")
        return {"data": "success", "attempts": call_count[0]}

    result = await asyncio.wait_for(flaky_fetch(), timeout=2.0)
    print(f"最终结果: {result}")


# ============================================================
# 主函数
# ============================================================

async def main() -> None:
    """主函数"""
    print("=" * 60)
    print("P02 示例 5: 异步数据处理")
    print("=" * 60)

    await demonstrate_basic_async()
    await demonstrate_concurrent()
    await demonstrate_async_context()
    await demonstrate_async_iterator()
    await demonstrate_stream()
    await demonstrate_rate_limiter()
    await demonstrate_semaphore()
    await demonstrate_timeout()
    await demonstrate_resilient()

    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
