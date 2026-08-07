"""L12 练习3: 异步生成器"""

import asyncio
from typing import AsyncIterator


async def async_count(n: int) -> AsyncIterator[int]:
    """异步计数器"""
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i


async def async_filter(predicate, async_iter) -> AsyncIterator:
    """异步过滤器"""
    async for item in async_iter:
        if asyncio.iscoroutinefunction(predicate):
            if await predicate(item):
                yield item
        elif predicate(item):
            yield item


async def async_map(transform, async_iter) -> AsyncIterator:
    """异步映射器"""
    async for item in async_iter:
        if asyncio.iscoroutinefunction(transform):
            yield await transform(item)
        else:
            yield transform(item)


async def async_batch_processor(items, batch_size: int = 3) -> AsyncIterator[list]:
    """异步批量处理器"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        await asyncio.sleep(0.01)
        yield batch


async def async_pipeline(source, *stages) -> AsyncIterator:
    """异步管道"""
    async for item in source:
        result = item
        for stage in stages:
            if asyncio.iscoroutinefunction(stage):
                result = await stage(result)
            else:
                result = stage(result)
        yield result


async def main():
    print("异步计数器:")
    result = [x async for x in async_count(5)]
    print(f"  {result}")

    print("\n异步过滤 (偶数):")
    result = [x async for x in async_filter(lambda x: x % 2 == 0, async_count(6))]
    print(f"  {result}")

    print("\n异步映射 (乘以2):")
    result = [x async for x in async_map(lambda x: x * 2, async_count(5))]
    print(f"  {result}")

    print("\n异步批量处理:")
    async for batch in async_batch_processor(range(10), 3):
        print(f"  {batch}")

    print("\n异步管道 (过滤 -> 乘以10):")
    result = [x async for x in async_pipeline(
        async_count(10),
        lambda x: x % 2 == 0,
        lambda x: x * 10
    )]
    print(f"  {result}")


if __name__ == "__main__":
    asyncio.run(main())
