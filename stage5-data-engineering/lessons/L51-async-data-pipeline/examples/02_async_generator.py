"""L51 示例: 异步生成器管道。"""

from __future__ import annotations

import asyncio


async def numbers(n: int) -> list[int]:
    return list(range(n))


async def squared(nums: list[int]) -> list[int]:
    return [x * x for x in nums]


async def pipeline(n: int) -> list[int]:
    return await squared(await numbers(n))


if __name__ == "__main__":
    print(asyncio.run(pipeline(5)))
