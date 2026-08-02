"""Solution: API Performance Analysis and Optimization"""

import time
import functools
import asyncio
from typing import TypeVar, Callable
from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class QueryStats:
    query: str
    count: int
    total_duration: float
    avg_duration: float


class QueryAnalyzer:
    """Analyze and detect N+1 query problems."""

    def __init__(self):
        self.queries: list[dict[str, float]] = []

    def record(self, query: str, duration: float):
        self.queries.append({"query": query, "duration": duration})

    def get_stats(self) -> list[QueryStats]:
        """Get statistics for each unique query."""
        stats_map: dict[str, list[float]] = {}

        for q in self.queries:
            query = q["query"]
            if query not in stats_map:
                stats_map[query] = []
            stats_map[query].append(q["duration"])

        return [
            QueryStats(
                query=query,
                count=len(durations),
                total_duration=sum(durations),
                avg_duration=sum(durations) / len(durations),
            )
            for query, durations in stats_map.items()
        ]

    def detect_n_plus_one(self) -> list[str]:
        """Detect queries that are executed multiple times."""
        stats = self.get_stats()
        return [s.query for s in stats if s.count > 1]

    def print_report(self):
        """Print performance report."""
        stats = self.get_stats()
        print(f"{'Query':<50} {'Count':>6} {'Avg (ms)':>10} {'Total (ms)':>12}")
        print("-" * 80)

        for s in sorted(stats, key=lambda x: -x.total_duration):
            print(f"{s.query:<50} {s.count:>6} {s.avg_duration * 1000:>10.2f} {s.total_duration * 1000:>12.2f}")

        n_plus_one = self.detect_n_plus_one()
        if n_plus_one:
            print(f"\n⚠️  N+1 detected: {len(n_plus_one)} queries executed multiple times")


def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure function execution time."""

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  {func.__name__}: {elapsed:.2f}ms")
        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  {func.__name__}: {elapsed:.2f}ms")
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


if __name__ == "__main__":
    analyzer = QueryAnalyzer()

    # Simulate queries
    for i in range(5):
        analyzer.record("SELECT * FROM users", 0.01)
    analyzer.record("SELECT * FROM posts", 0.02)

    analyzer.print_report()
    n_plus_one = analyzer.detect_n_plus_one()
    print(f"\nN+1 problems: {n_plus_one}")
