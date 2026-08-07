"""L12 示例3: 异步生成器

本示例演示异步生成器的用法和异步数据处理管道。
"""

import asyncio
from typing import AsyncIterator


async def async_count(n: int) -> AsyncIterator[int]:
    """异步计数器"""
    for i in range(n):
        await asyncio.sleep(0.1)  # 模拟异步操作
        yield i


async def async_fetch_page(url: str) -> str:
    """模拟异步获取页面"""
    await asyncio.sleep(0.1)
    return f"Content from {url}"


async def async_url_generator() -> AsyncIterator[str]:
    """异步 URL 生成器"""
    urls = ["a.com", "b.com", "c.com", "d.com", "e.com"]
    for url in urls:
        await asyncio.sleep(0.05)
        yield url


async def async_batch_processor(
    items: list,
    batch_size: int = 3
) -> AsyncIterator[list]:
    """异步批量处理器"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        await asyncio.sleep(0.1)  # 模拟处理延迟
        yield batch


async def async_file_reader(filename: str, chunk_size: int = 1024) -> AsyncIterator[bytes]:
    """异步文件读取器"""
    import io
    # 模拟文件内容
    content = f"这是 {filename} 的内容。\n" * 100
    buffer = io.BytesIO(content.encode())

    while True:
        chunk = buffer.read(chunk_size)
        if not chunk:
            break
        yield chunk


async def async_filter(predicate, async_iter):
    """异步过滤器"""
    async for item in async_iter:
        if await predicate(item) if asyncio.iscoroutinefunction(predicate) else predicate(item):
            yield item


async def async_map(transform, async_iter):
    """异步映射器"""
    async for item in async_iter:
        result = transform(item) if not asyncio.iscoroutinefunction(transform) else await transform(item)
        yield result


async def async_pipeline(source, *stages):
    """异步管道"""
    async for item in source:
        result = item
        for stage in stages:
            result = stage(result) if not asyncio.iscoroutinefunction(stage) else await stage(result)
        yield result


async def fetch_all_pages():
    """顺序获取所有页面"""
    pages = []
    async for url in async_url_generator():
        page = await async_fetch_page(url)
        pages.append(page)
    return pages


async def fetch_all_pages_concurrent():
    """并发获取所有页面"""
    urls = ["a.com", "b.com", "c.com", "d.com", "e.com"]
    tasks = [async_fetch_page(url) for url in urls]
    return await asyncio.gather(*tasks)


async def process_in_batches():
    """演示批量处理"""
    items = list(range(10))
    print(f"待处理项目: {items}")

    batch_num = 0
    async for batch in async_batch_processor(items, batch_size=3):
        batch_num += 1
        print(f"批次 {batch_num}: {batch}")


async def generator_comparison():
    """普通生成器 vs 异步生成器对比"""
    def sync_range(n):
        for i in range(n):
            yield i

    async def async_range(n):
        for i in range(n):
            await asyncio.sleep(0.01)
            yield i

    print("普通生成器:")
    for i in sync_range(3):
        print(f"  Sync: {i}")

    print("\n异步生成器:")
    async for i in async_range(3):
        print(f"  Async: {i}")


if __name__ == "__main__":
    print("=" * 60)
    print("1. 异步计数器")
    print("=" * 60)

    async def test_counter():
        count = 0
        async for i in async_count(5):
            count += 1
            print(f"计数: {i}")
        print(f"总计: {count} 项")

    asyncio.run(test_counter())

    print("\n" + "=" * 60)
    print("2. 顺序获取页面")
    print("=" * 60)

    async def test_fetch_sequential():
        pages = await fetch_all_pages()
        for page in pages:
            print(f"  {page}")

    asyncio.run(test_fetch_sequential())

    print("\n" + "=" * 60)
    print("3. 并发获取页面")
    print("=" * 60)

    async def test_fetch_concurrent():
        pages = await fetch_all_pages_concurrent()
        for page in pages:
            print(f"  {page}")

    asyncio.run(test_fetch_concurrent())

    print("\n" + "=" * 60)
    print("4. 批量处理")
    print("=" * 60)

    asyncio.run(process_in_batches())

    print("\n" + "=" * 60)
    print("5. 生成器对比")
    print("=" * 60)

    asyncio.run(generator_comparison())
