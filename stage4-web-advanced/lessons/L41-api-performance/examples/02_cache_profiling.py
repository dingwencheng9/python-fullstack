"""Example 2: Performance Profiling with cProfile"""

import cProfile
import pstats
from io import StringIO
import asyncio
import time
from functools import lru_cache


# Simulated expensive operations
@lru_cache(maxsize=1000)
def expensive_computation(n: int) -> int:
    """Expensive CPU-bound computation."""
    result = 0
    for i in range(n * 1000):
        result += i**2
    return result % 1000000


async def async_database_query(user_id: int) -> dict:
    """Simulated async database query."""
    await asyncio.sleep(0.01)  # Simulate I/O
    return {"id": user_id, "name": f"User {user_id}"}


async def get_user_posts(user_id: int) -> list:
    """Get all posts for a user (N+1 problem example)."""
    # Get user
    user = await async_database_query(user_id)

    # Get posts (simulated)
    posts = []
    for i in range(10):
        await asyncio.sleep(0.001)
        posts.append({"post_id": i, "user_id": user_id})

    return {"user": user, "posts": posts}


def profile_async():
    """Profile async function."""
    profiler = cProfile.Profile()
    profiler.enable()

    # Run async code
    asyncio.run(get_user_posts(1))

    profiler.disable()

    # Print stats
    s = StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.print_stats(20)
    print(s.getvalue())


if __name__ == "__main__":
    # Profile the function
    profile_async()

    # Test caching benefit
    start = time.perf_counter()
    for i in range(1000):
        expensive_computation(10)
    elapsed = time.perf_counter() - start
    print(f"Cached 1000 calls: {elapsed * 1000:.2f}ms")
