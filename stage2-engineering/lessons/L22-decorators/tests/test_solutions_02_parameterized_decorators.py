"""

from __future__ import annotations

测试 solution_02_parameterized_decorators.py - 带参数装饰器
"""

import time
import warnings

import pytest
from solutions.solution_02_parameterized_decorators import (
    deprecated,
    rate_limit,
    retry,
    singleton,
    validate_input,
    with_logging,
)


class TestRetry:
    """测试 retry 装饰器"""

    def test_retry_success_first_try(self):
        """测试第一次就成功"""
        call_count = 0

        @retry(max_attempts=3)
        def func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = func()
        assert result == "success"
        assert call_count == 1

    def test_retry_success_after_failures(self):
        """测试重试后成功"""
        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("not yet")
            return "success"

        result = func()
        assert result == "success"
        assert call_count == 3

    def test_retry_all_attempts_fail(self):
        """测试所有重试都失败"""
        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def func():
            nonlocal call_count
            call_count += 1
            raise ValueError("always fails")

        with pytest.raises(ValueError, match="always fails"):
            func()

        assert call_count == 3

    def test_retry_with_args(self):
        """测试带参数的函数重试"""
        call_count = 0

        @retry(max_attempts=2, delay=0.01)
        def divide(a, b):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ZeroDivisionError("retry")
            return a / b

        result = divide(10, 2)
        assert result == 5.0
        assert call_count == 2


class TestRateLimit:
    """测试 rate_limit 装饰器"""

    def test_rate_limit_basic(self):
        """测试基本限流功能"""

        @rate_limit(calls=2, period=1.0)
        def func():
            return "ok"

        # 前两次调用应该成功
        result1 = func()
        result2 = func()
        assert result1 == "ok"
        assert result2 == "ok"

        # 第三次调用应该被限流
        with pytest.raises(RuntimeError, match="Rate limit exceeded"):
            func()

    def test_rate_limit_reset_after_period(self):
        """测试时间窗口重置"""

        @rate_limit(calls=1, period=0.1)
        def func():
            return "ok"

        # 第一次调用成功
        func()

        # 立即第二次调用失败
        with pytest.raises(RuntimeError):
            func()

        # 等待时间窗口过期
        time.sleep(0.15)

        # 现在应该可以再次调用
        result = func()
        assert result == "ok"


class TestDeprecated:
    """测试 deprecated 装饰器"""

    def test_deprecated_warning(self):
        """测试弃用警告"""

        @deprecated
        def old_func():
            return "old"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_func()

            assert result == "old"
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "old_func is deprecated" in str(w[0].message)

    def test_deprecated_custom_message(self):
        """测试自定义弃用消息"""

        @deprecated("Use new_func instead")
        def old_func():
            return "old"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            old_func()

            assert len(w) == 1
            assert "Use new_func instead" in str(w[0].message)


class TestSingleton:
    """测试 singleton 装饰器"""

    def test_singleton_basic(self):
        """测试单例模式基本功能"""

        @singleton
        class Database:
            def __init__(self):
                self.connection = "connected"

        db1 = Database()
        db2 = Database()

        assert db1 is db2
        assert db1.connection == "connected"

    def test_singleton_different_classes(self):
        """测试不同类的单例独立"""

        @singleton
        class ClassA:
            pass

        @singleton
        class ClassB:
            pass

        a1 = ClassA()
        a2 = ClassA()
        b1 = ClassB()
        b2 = ClassB()

        assert a1 is a2
        assert b1 is b2
        assert a1 is not b1


class TestValidateInput:
    """测试 validate_input 装饰器"""

    def test_validate_input_success(self):
        """测试验证成功"""

        @validate_input(lambda x: x > 0, "x must be positive")
        def sqrt(x):
            return x**0.5

        result = sqrt(4)
        assert result == 2.0

    def test_validate_input_failure(self):
        """测试验证失败"""

        @validate_input(lambda x: x > 0, "x must be positive")
        def sqrt(x):
            return x**0.5

        with pytest.raises(ValueError, match="x must be positive"):
            sqrt(-1)

    def test_validate_input_multiple_args(self):
        """测试多参数验证"""

        @validate_input(lambda x, y: x < y, "x must be less than y")
        def range_check(x, y):
            return y - x

        result = range_check(1, 5)
        assert result == 4

        with pytest.raises(ValueError, match="x must be less than y"):
            range_check(5, 1)


class TestWithLogging:
    """测试 with_logging 装饰器"""

    def test_with_logging_basic(self, capsys):
        """测试基本日志功能"""

        @with_logging
        def func(x):
            return x * 2

        result = func(5)
        assert result == 10

        captured = capsys.readouterr()
        assert "Executing: func" in captured.out

    def test_with_logging_with_level(self, capsys):
        """测试指定日志级别"""

        @with_logging(level="INFO")
        def func():
            return "ok"

        result = func()
        assert result == "ok"

    def test_with_logging_exception(self, capsys):
        """测试异常日志"""

        @with_logging
        def failing_func():
            raise ValueError("test error")

        with pytest.raises(ValueError):
            failing_func()

        captured = capsys.readouterr()
        assert "Executing: failing_func" in captured.out


class TestDecoratorComposition:
    """测试装饰器组合"""

    def test_retry_with_logging(self, capsys):
        """测试 retry 和 with_logging 组合"""
        call_count = 0

        @with_logging
        @retry(max_attempts=2, delay=0.01)
        def func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("retry")
            return "ok"

        result = func()
        assert result == "ok"
        assert call_count == 2

    def test_deprecated_singleton(self):
        """测试 deprecated 和 singleton 组合"""

        @deprecated
        @singleton
        class OldDatabase:
            pass

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            db1 = OldDatabase()
            db2 = OldDatabase()

            # singleton 正常工作
            assert db1 is db2
            # deprecated 警告正常触发
            assert len(w) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
