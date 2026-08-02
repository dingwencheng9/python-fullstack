"""L20 练习 6: 实战应用.

学习目标：
- 构建实用装饰器库
- 实现性能监控、事务管理和令牌桶限流
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
import logging
import sys
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """统计函数调用次数和耗时的性能监控器。"""

    def __init__(self) -> None:
        self.stats: dict[str, dict[str, float | int | list[float]]] = {}

    def timer(self, func: Callable) -> Callable:
        """记录被装饰函数的耗时统计。"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                func_stats = self.stats.setdefault(
                    func.__name__,
                    {
                        "calls": 0,
                        "total_time": 0.0,
                        "min_time": float("inf"),
                        "max_time": 0.0,
                        "times": [],
                    },
                )
                func_stats["calls"] += 1
                func_stats["total_time"] += elapsed
                func_stats["min_time"] = min(func_stats["min_time"], elapsed)
                func_stats["max_time"] = max(func_stats["max_time"], elapsed)
                func_stats["times"].append(elapsed)

        return wrapper

    def report(self) -> None:
        """打印性能报告。"""
        print("\n" + "=" * 70)
        print(" 性能监控报告")
        print("=" * 70)
        if not self.stats:
            print("暂无性能数据")
            return
        for name, stats in sorted(self.stats.items()):
            avg = stats["total_time"] / stats["calls"]
            print(f"函数: {name}")
            print(f"  调用次数: {stats['calls']}")
            print(f"  总时间: {stats['total_time']:.6f}s")
            print(f"  平均时间: {avg:.6f}s")
            print(f"  最小时间: {stats['min_time']:.6f}s")
            print(f"  最大时间: {stats['max_time']:.6f}s")
        print("=" * 70)

    def reset(self) -> None:
        """清空统计数据。"""
        self.stats.clear()


class Transaction:
    """模拟事务管理器。"""

    def __init__(self) -> None:
        self.in_transaction = False
        self.operations: list[str] = []

    def begin(self) -> None:
        self.in_transaction = True
        self.operations = []
        logger.info("BEGIN TRANSACTION")

    def commit(self) -> None:
        self.in_transaction = False
        logger.info("COMMIT: %s operations", len(self.operations))

    def rollback(self) -> None:
        self.in_transaction = False
        logger.warning("ROLLBACK: %s operations", len(self.operations))

    def add_operation(self, op: str) -> None:
        self.operations.append(op)


transaction = Transaction()


def transactional(func: Callable) -> Callable:
    """自动 begin/commit/rollback 的事务装饰器。"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        transaction.begin()
        try:
            result = func(*args, **kwargs)
        except Exception:
            transaction.rollback()
            raise
        transaction.commit()
        return result

    return wrapper


class TokenBucket:
    """令牌桶限流装饰器。"""

    def __init__(self, capacity: int, refill_rate: float) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        if refill_rate <= 0:
            raise ValueError("refill_rate must be > 0")
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def _consume(self) -> bool:
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def __call__(self, func: Callable) -> Callable:
        """装饰函数；令牌不足时拒绝请求。"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self._consume():
                raise RuntimeError(
                    f"Rate limit exceeded: {self.capacity} calls per second"
                )
            return func(*args, **kwargs)

        return wrapper


def test_performance_monitor() -> None:
    print("\n测试 1: 性能监控装饰器")
    monitor = PerformanceMonitor()

    @monitor.timer
    def task1():
        time.sleep(0.01)

    @monitor.timer
    def task2():
        time.sleep(0.02)

    for _ in range(3):
        task1()
    for _ in range(2):
        task2()
    assert monitor.stats["task1"]["calls"] == 3
    assert monitor.stats["task2"]["calls"] == 2
    monitor.report()
    monitor.reset()
    assert monitor.stats == {}
    print("✅ 性能监控装饰器测试通过")


def test_transactional() -> None:
    print("\n测试 2: 事务管理装饰器")

    @transactional
    def transfer_money(from_acc, to_acc, amount):
        transaction.add_operation(f"Debit {from_acc}: {amount}")
        transaction.add_operation(f"Credit {to_acc}: {amount}")
        if amount > 10000:
            raise ValueError("Amount too large")
        return True

    assert transfer_money("Alice", "Bob", 100) is True
    assert transaction.in_transaction is False
    try:
        transfer_money("Alice", "Bob", 20000)
        raise AssertionError("应该抛出异常")
    except ValueError:
        pass
    assert transaction.in_transaction is False
    print("✅ 事务管理装饰器测试通过")


def test_token_bucket() -> None:
    print("\n测试 3: API 限流装饰器")

    @TokenBucket(capacity=3, refill_rate=10.0)
    def api_call(endpoint):
        return f"Response from {endpoint}"

    for i in range(3):
        assert "Response" in api_call(f"/api/{i}")
    try:
        api_call("/api/too-much")
        raise AssertionError("令牌耗尽后应该拒绝请求")
    except RuntimeError:
        pass
    print("✅ API 限流装饰器测试通过")


def main() -> bool:
    print("\n" + "=" * 50)
    print("L20 练习 6: 实战应用")
    print("=" * 50)
    try:
        test_performance_monitor()
        test_transactional()
        test_token_bucket()
    except AssertionError as exc:
        print(f"\n❌ 测试失败: {exc}")
        return False
    except Exception as exc:
        print(f"\n❌ 发生错误: {type(exc).__name__}: {exc}")
        return False

    print("\n🎉 所有测试通过！")
    print("🏆 恭喜！你已经完成 L20 所有练习！")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
