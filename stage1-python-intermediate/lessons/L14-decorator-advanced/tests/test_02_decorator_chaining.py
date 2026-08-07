"""L14 练习 2 测试: 装饰器组合与执行顺序

测试日志、计时、重试、缓存装饰器及其组合。
"""

import pytest
import time
from unittest.mock import patch


class TestLogDecorator:
    """日志装饰器测试"""

    def test_log_records_function_call(self, capsys):
        """日志装饰器应该记录函数调用"""
        from solutions import log

        @log("INFO")
        def add(a, b):
            return a + b

        result = add(1, 2)

        assert result == 3
        captured = capsys.readouterr()
        assert "INFO" in captured.out
        assert "add" in captured.out

    def test_log_accepts_level_parameter(self, capsys):
        """日志装饰器应该接受级别参数"""
        from solutions import log

        @log("WARNING")
        def my_func():
            return "done"

        my_func()

        captured = capsys.readouterr()
        assert "WARNING" in captured.out


class TestTimerDecorator:
    """计时装饰器测试"""

    def test_timer_measures_elapsed_time(self, capsys):
        """计时装饰器应该测量执行时间"""
        from solutions import timer

        @timer(unit="ms")
        def slow_func():
            time.sleep(0.05)
            return "done"

        result = slow_func()

        assert result == "done"
        captured = capsys.readouterr()
        assert "计时" in captured.out
        assert "ms" in captured.out

    def test_timer_different_units(self, capsys):
        """计时装饰器应该支持不同时间单位"""
        from solutions import timer

        @timer(unit="s")
        def short_func():
            return "done"

        short_func()

        captured = capsys.readouterr()
        assert "s" in captured.out


class TestRetryDecorator:
    """重试装饰器测试"""

    def test_retry_succeeds_on_eventual_success(self):
        """最终成功时应该返回结果"""
        from solutions import retry

        attempt = 0

        @retry(max_attempts=3, delay=0.01)
        def unreliable_func():
            nonlocal attempt
            attempt += 1
            if attempt < 2:
                raise ValueError("Temporary error")
            return "success"

        result = unreliable_func()
        assert result == "success"
        assert attempt == 2

    def test_retry_fails_after_max_attempts(self):
        """超过最大重试次数后应该抛出异常"""
        from solutions import retry

        @retry(max_attempts=2, delay=0.01)
        def always_fails():
            raise ValueError("Always fails")

        with pytest.raises(ValueError):
            always_fails()


class TestCacheDecorator:
    """缓存装饰器测试"""

    def test_cache_stores_results(self):
        """缓存装饰器应该存储结果"""
        from solutions import cache

        call_count = 0

        @cache()
        def cached_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # 第一次调用
        result1 = cached_func(5)
        assert result1 == 10
        assert call_count == 1

        # 第二次相同参数（使用缓存）
        result2 = cached_func(5)
        assert result2 == 10
        assert call_count == 1  # 没有增加

    def test_cache_different_args(self):
        """不同参数应该分别缓存"""
        from solutions import cache

        call_count = 0

        @cache()
        def cached_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        cached_func(5)
        cached_func(10)

        assert call_count == 2


class TestDecoratorChaining:
    """装饰器链测试"""

    def test_decorators_execute_in_correct_order(self, capsys):
        """装饰器应该按正确顺序执行"""
        from solutions import log, timer

        execution_order = []

        def tracker_decorator(name):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    execution_order.append(f"enter_{name}")
                    result = func(*args, **kwargs)
                    execution_order.append(f"exit_{name}")
                    return result
                return wrapper
            return decorator

        # 模拟装饰器执行顺序
        log_decorator = tracker_decorator("log")
        timer_decorator = tracker_decorator("timer")

        # @log 在外层，@timer 在内层
        # 等价于: func = log(timer(func))
        # 执行顺序: timer -> log

        def test_func():
            execution_order.append("func")

        wrapped = log_decorator(timer_decorator(test_func))
        wrapped()

        # 期望顺序: enter_log -> enter_timer -> func -> exit_timer -> exit_log
        assert execution_order == [
            "enter_log", "enter_timer", "func", "exit_timer", "exit_log"
        ]


class TestDecoratorChainingReal:
    """真实装饰器链测试"""

    def test_log_and_timer_combined(self, capsys):
        """日志和计时装饰器组合"""
        from solutions import log, timer

        @log("INFO")
        @timer(unit="ms")
        def combined_func():
            time.sleep(0.01)
            return 42

        result = combined_func()

        assert result == 42
        captured = capsys.readouterr()
        assert "INFO" in captured.out
        assert "计时" in captured.out
