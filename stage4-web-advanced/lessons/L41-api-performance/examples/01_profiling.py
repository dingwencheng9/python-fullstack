"""示例 1: 性能分析"""

import cProfile
import pstats
from io import StringIO
import asyncio
import aiohttp


async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, "http://api.example.com/data") for _ in range(100)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    asyncio.run(main())

    profiler.disable()

    s = StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.print_stats(20)
    print(s.getvalue())
