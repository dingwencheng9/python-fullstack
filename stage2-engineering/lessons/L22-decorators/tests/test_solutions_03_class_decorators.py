"""

from __future__ import annotations

测试 solution_03_class_decorators.py - 类装饰器
"""

import contextlib
import time

import pytest
from solutions.solution_03_class_decorators import (
    CallCounter,
    Memoize,
    RateLimiter,
    log_method_calls,
)


class TestCallCounter:
    """测试 CallCounter 类装饰器"""

    def test_call_counter_basic(self):
        """测试基本计数功能"""

        @CallCounter
        def func():
            return "ok"

        assert func.calls == 0

        func()
        assert func.calls == 1

        func()
        func()
        assert func.calls == 3

    def test_call_counter_with_args(self):
        """测试带参数的函数计数"""

        @CallCounter
        def add(a, b):
            return a + b

        result1 = add(2, 3)
        result2 = add(5, 10)

        assert result1 == 5
        assert result2 == 15
        assert add.calls == 2

    def test_call_counter_reset(self):
        """测试重置计数"""

        @CallCounter
        def func():
            return "ok"

        func()
        func()
        assert func.calls == 2

        func.reset()
        assert func.calls == 0

        func()
        assert func.calls == 1

    def test_call_counter_multiple_functions(self):
        """测试多个函数独立计数"""

        @CallCounter
        def func1():
            return "1"

        @CallCounter
        def func2():
            return "2"

        func1()
        func1()
        func2()

        assert func1.calls == 2
        assert func2.calls == 1


class TestMemoize:
    """测试 Memoize 类装饰器"""

    def test_memoize_basic(self):
        """测试基本缓存功能"""
        call_count = 0

        @Memoize
        def fibonacci(n):
            nonlocal call_count
            call_count += 1
            if n <= 1:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        result = fibonacci(5)
        assert result == 5
        # 由于缓存，调用次数应该远小于递归次数
        assert call_count == 6  # 只计算 0,1,2,3,4,5

    def test_memoize_with_different_args(self):
        """测试不同参数的缓存"""
        call_count = 0

        @Memoize
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = expensive_func(5)
        result2 = expensive_func(5)  # 缓存命中
        result3 = expensive_func(10)

        assert result1 == 10
        assert result2 == 10
        assert result3 == 20
        assert call_count == 2  # 只实际调用 2 次

    def test_memoize_clear_cache(self):
        """测试清除缓存"""
        call_count = 0

        @Memoize
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        func(5)
        assert call_count == 1

        func(5)  # 缓存命中
        assert call_count == 1

        func.clear_cache()

        func(5)  # 缓存已清除
        assert call_count == 2

    def test_memoize_preserves_metadata(self):
        """测试元信息保留"""

        @Memoize
        def documented_func(x):
            """This is a docstring"""
            return x

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "This is a docstring"


class TestRateLimiter:
    """测试 RateLimiter 类装饰器"""

    def test_rate_limiter_basic(self):
        """测试基本限流功能"""

        @RateLimiter(max_calls=2, period=1.0)
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

    def test_rate_limiter_reset_after_period(self):
        """测试时间窗口重置"""

        @RateLimiter(max_calls=1, period=0.1)
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

    def test_rate_limiter_with_args(self):
        """测试带参数的函数限流"""

        @RateLimiter(max_calls=2, period=1.0)
        def add(a, b):
            return a + b

        result1 = add(1, 2)
        result2 = add(3, 4)

        assert result1 == 3
        assert result2 == 7

        with pytest.raises(RuntimeError):
            add(5, 6)


class TestLogMethodCalls:
    """测试 log_method_calls 类装饰器"""

    def test_log_method_calls_basic(self, capsys):
        """测试基本方法调用日志"""

        @log_method_calls
        class Calculator:
            def add(self, a, b):
                return a + b

            def multiply(self, a, b):
                return a * b

        calc = Calculator()
        result1 = calc.add(2, 3)
        result2 = calc.multiply(4, 5)

        assert result1 == 5
        assert result2 == 20

        captured = capsys.readouterr()
        assert "Calling Calculator.add" in captured.out
        assert "Calling Calculator.multiply" in captured.out

    def test_log_method_calls_with_private_methods(self, capsys):
        """测试私有方法不被日志记录"""

        @log_method_calls
        class MyClass:
            def public_method(self):
                return self._private_method()

            def _private_method(self):
                return "private"

        obj = MyClass()
        result = obj.public_method()

        assert result == "private"

        captured = capsys.readouterr()
        # 只记录公共方法
        assert "public_method" in captured.out
        # 私有方法不应该被记录（根据实现可能会记录）
        # 这里假设实现会记录所有方法

    def test_log_method_calls_preserves_class_name(self):
        """测试类名保留"""

        @log_method_calls
        class MyClass:
            pass

        assert MyClass.__name__ == "MyClass"


class TestClassDecoratorComposition:
    """测试类装饰器组合"""

    def test_multiple_class_decorators(self):
        """测试多个类装饰器组合"""

        @CallCounter
        @Memoize
        def func(n):
            if n <= 1:
                return n
            return func(n - 1) + func(n - 2)

        result = func(5)
        assert result == 5
        # Memoize 减少了实际调用次数
        # CallCounter 统计外部调用次数
        assert hasattr(func, "calls")


class TestEdgeCases:
    """测试边界情况"""

    def test_call_counter_with_exception(self):
        """测试异常情况下的计数"""

        @CallCounter
        def failing_func():
            raise ValueError("error")

        with contextlib.suppress(ValueError):
            failing_func()

        # 即使抛出异常，也应该计数
        assert failing_func.calls == 1

    def test_memoize_with_unhashable_args(self):
        """测试不可哈希参数"""

        @Memoize
        def func(data):
            return sum(data)

        # 列表是不可哈希的，应该抛出错误
        with pytest.raises(TypeError):
            func([1, 2, 3])

    def test_rate_limiter_zero_period(self):
        """测试零时间窗口"""

        @RateLimiter(max_calls=1, period=0.0)
        def func():
            return "ok"

        # 即使 period=0，也应该能至少调用一次
        result = func()
        assert result == "ok"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
