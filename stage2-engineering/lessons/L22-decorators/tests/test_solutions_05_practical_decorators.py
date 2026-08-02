"""

from __future__ import annotations

测试 solution_05_practical_decorators.py - 实战应用
"""

import logging
import time

import pytest
from solutions.solution_05_practical_decorators import (
    PerformanceMonitor,
    TokenBucket,
    Transaction,
    transactional,
)


class TestPerformanceMonitor:
    """测试 PerformanceMonitor 类"""

    def test_monitor_basic(self):
        """测试基本性能监控"""
        monitor = PerformanceMonitor()

        @monitor.timer
        def task():
            time.sleep(0.01)
            return "done"

        result = task()
        assert result == "done"

        # 检查统计信息
        assert "task" in monitor.stats
        assert monitor.stats["task"]["calls"] == 1
        assert monitor.stats["task"]["total_time"] > 0

    def test_monitor_multiple_calls(self):
        """测试多次调用统计"""
        monitor = PerformanceMonitor()

        @monitor.timer
        def task():
            time.sleep(0.01)

        # 调用多次
        for _ in range(3):
            task()

        stats = monitor.stats["task"]
        assert stats["calls"] == 3
        assert stats["min_time"] > 0
        assert stats["max_time"] >= stats["min_time"]
        assert stats["total_time"] >= stats["min_time"] * 3

    def test_monitor_multiple_functions(self):
        """测试监控多个函数"""
        monitor = PerformanceMonitor()

        @monitor.timer
        def task1():
            time.sleep(0.01)

        @monitor.timer
        def task2():
            time.sleep(0.02)

        task1()
        task2()

        assert "task1" in monitor.stats
        assert "task2" in monitor.stats
        assert monitor.stats["task1"]["calls"] == 1
        assert monitor.stats["task2"]["calls"] == 1

    def test_monitor_reset(self):
        """测试重置统计"""
        monitor = PerformanceMonitor()

        @monitor.timer
        def task():
            pass

        task()
        assert len(monitor.stats) == 1

        monitor.reset()
        assert len(monitor.stats) == 0

    def test_monitor_report(self, capsys):
        """测试报告生成"""
        monitor = PerformanceMonitor()

        @monitor.timer
        def task():
            time.sleep(0.01)

        task()
        monitor.report()

        captured = capsys.readouterr()
        assert "性能监控报告" in captured.out
        assert "task" in captured.out
        assert "调用次数" in captured.out

    def test_monitor_with_args(self):
        """测试带参数的函数"""
        monitor = PerformanceMonitor()

        @monitor.timer
        def add(a, b):
            return a + b

        result = add(2, 3)
        assert result == 5
        assert monitor.stats["add"]["calls"] == 1

    def test_monitor_with_exception(self):
        """测试异常情况"""
        monitor = PerformanceMonitor()

        @monitor.timer
        def failing_func():
            raise ValueError("error")

        with pytest.raises(ValueError):
            failing_func()

        # 即使抛出异常，也应该记录统计
        assert "failing_func" in monitor.stats
        assert monitor.stats["failing_func"]["calls"] == 1


class TestTransaction:
    """测试 Transaction 类"""

    def test_transaction_basic(self):
        """测试基本事务操作"""
        tx = Transaction()
        assert not tx.in_transaction
        assert len(tx.operations) == 0

        tx.begin()
        assert tx.in_transaction
        assert len(tx.operations) == 0

        tx.add_operation("INSERT INTO users")
        assert len(tx.operations) == 1

        tx.commit()
        assert not tx.in_transaction

    def test_transaction_rollback(self):
        """测试事务回滚"""
        tx = Transaction()

        tx.begin()
        tx.add_operation("DELETE FROM users")
        assert len(tx.operations) == 1

        tx.rollback()
        assert not tx.in_transaction


class TestTransactional:
    """测试 transactional 装饰器"""

    def test_transactional_success(self, caplog):
        """测试成功场景"""
        tx = Transaction()

        @transactional
        def update_user():
            tx.add_operation("UPDATE users SET name='Alice'")
            return "success"

        with caplog.at_level(logging.INFO):
            result = update_user()

        assert result == "success"
        assert not tx.in_transaction
        assert "COMMIT" in caplog.text

    def test_transactional_failure(self, caplog):
        """测试失败场景"""
        tx = Transaction()

        @transactional
        def failing_update():
            tx.add_operation("UPDATE users")
            raise ValueError("database error")

        with caplog.at_level(logging.INFO):
            with pytest.raises(ValueError, match="database error"):
                failing_update()

        assert not tx.in_transaction
        assert "ROLLBACK" in caplog.text

    def test_transactional_with_args(self):
        """测试带参数的函数"""
        tx = Transaction()

        @transactional
        def transfer(from_acc, to_acc, amount):
            tx.add_operation(f"DEBIT {from_acc} {amount}")
            tx.add_operation(f"CREDIT {to_acc} {amount}")
            return amount

        result = transfer("Alice", "Bob", 100)
        assert result == 100

    def test_transactional_preserves_metadata(self):
        """测试元信息保留"""

        @transactional
        def documented_func():
            """This is a docstring"""

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "This is a docstring"


class TestTokenBucket:
    """测试 TokenBucket 限流器"""

    def test_token_bucket_basic(self):
        """测试基本限流功能"""

        @TokenBucket(capacity=3, refill_rate=10.0)
        def api_call():
            return "ok"

        # 初始容量为 3，可以连续调用 3 次
        assert api_call() == "ok"
        assert api_call() == "ok"
        assert api_call() == "ok"

    def test_token_bucket_rate_limit(self):
        """测试速率限制"""

        @TokenBucket(capacity=2, refill_rate=10.0)
        def api_call():
            return "ok"

        # 前两次成功
        api_call()
        api_call()

        # 第三次应该失败（令牌不足）
        with pytest.raises(RuntimeError, match="Rate limit exceeded"):
            api_call()

    def test_token_bucket_refill(self):
        """测试令牌补充"""

        @TokenBucket(capacity=1, refill_rate=10.0)
        def api_call():
            return "ok"

        # 第一次成功
        api_call()

        # 等待令牌补充（10 tokens/s = 0.1s per token）
        time.sleep(0.15)

        # 现在应该可以再次调用
        result = api_call()
        assert result == "ok"

    def test_token_bucket_with_args(self):
        """测试带参数的函数"""

        @TokenBucket(capacity=2, refill_rate=10.0)
        def get_data(endpoint):
            return f"data from {endpoint}"

        result1 = get_data("/api/users")
        result2 = get_data("/api/posts")

        assert result1 == "data from /api/users"
        assert result2 == "data from /api/posts"

        with pytest.raises(RuntimeError):
            get_data("/api/comments")

    def test_token_bucket_high_refill_rate(self):
        """测试高补充速率"""

        @TokenBucket(capacity=1, refill_rate=100.0)
        def fast_api():
            return "ok"

        # 高速率下，令牌快速补充
        for _ in range(5):
            fast_api()
            time.sleep(0.02)  # 等待补充

    def test_token_bucket_preserves_metadata(self):
        """测试元信息保留"""

        @TokenBucket(capacity=3, refill_rate=10.0)
        def documented_func():
            """API endpoint"""
            return "ok"

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "API endpoint"


class TestIntegration:
    """测试集成场景"""

    def test_monitor_with_transactional(self):
        """测试性能监控和事务组合"""
        monitor = PerformanceMonitor()
        tx = Transaction()

        @monitor.timer
        @transactional
        def update_data():
            tx.add_operation("UPDATE data")
            time.sleep(0.01)
            return "done"

        result = update_data()
        assert result == "done"
        assert "update_data" in monitor.stats

    def test_token_bucket_with_monitor(self):
        """测试限流和监控组合"""
        monitor = PerformanceMonitor()

        @TokenBucket(capacity=2, refill_rate=10.0)
        @monitor.timer
        def api_endpoint():
            return "response"

        # 前两次成功
        api_endpoint()
        api_endpoint()

        assert monitor.stats["api_endpoint"]["calls"] == 2

        # 第三次失败
        with pytest.raises(RuntimeError):
            api_endpoint()

        # 失败的调用不应该被监控统计
        # （因为在进入 timer 之前就被 TokenBucket 拦截了）


class TestEdgeCases:
    """测试边界情况"""

    def test_monitor_concurrent_calls(self):
        """测试并发调用（线程安全）"""
        import threading

        monitor = PerformanceMonitor()

        @monitor.timer
        def task():
            time.sleep(0.001)

        threads = [threading.Thread(target=task) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert monitor.stats["task"]["calls"] == 10

    def test_token_bucket_zero_capacity(self):
        """测试零容量"""

        @TokenBucket(capacity=0, refill_rate=10.0)
        def api_call():
            return "ok"

        # 零容量应该立即被限流
        with pytest.raises(RuntimeError):
            api_call()

    def test_transactional_nested(self):
        """测试嵌套事务（简化版）"""
        tx = Transaction()

        @transactional
        def outer():
            tx.add_operation("outer op")
            return "outer"

        # 注意：当前实现不支持真正的嵌套事务
        # 这里只是测试基本调用
        result = outer()
        assert result == "outer"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
