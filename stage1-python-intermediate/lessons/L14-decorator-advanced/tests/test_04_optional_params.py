"""L14 练习 4 测试: 可选参数装饰器

测试同时支持有参和无参调用的装饰器。
"""

import pytest
import time


class TestOptionalLogDecorator:
    """可选参数日志装饰器测试"""

    def test_log_without_parentheses(self, capsys):
        """@log 方式调用（无括号）"""
        from solutions import optional_log as log

        @log
        def my_func():
            return "result"

        result = my_func()

        assert result == "result"
        captured = capsys.readouterr()
        assert "INFO" in captured.out  # 默认级别
        assert "my_func" in captured.out

    def test_log_with_empty_parentheses(self, capsys):
        """@log() 方式调用（空括号）"""
        from solutions import optional_log as log

        @log()
        def my_func():
            return "result"

        result = my_func()

        assert result == "result"
        captured = capsys.readouterr()
        assert "INFO" in captured.out

    def test_log_with_level_parameter(self, capsys):
        """@log(level="DEBUG") 方式调用"""
        from solutions import optional_log as log

        @log(level="DEBUG")
        def my_func():
            return "result"

        result = my_func()

        assert result == "result"
        captured = capsys.readouterr()
        assert "DEBUG" in captured.out


class TestOptionalTimedDecorator:
    """可选参数计时装饰器测试"""

    def test_timed_without_parentheses(self):
        """@timed 方式调用"""
        from solutions import timed

        @timed
        def my_func():
            time.sleep(0.01)
            return "result"

        result = my_func()

        assert result == "result"
        # 默认 verbose=False，不输出任何内容
        # 可以验证 last_elapsed 属性
        assert hasattr(my_func, 'last_elapsed')

    def test_timed_with_unit_parameter(self, capsys):
        """@timed(unit="ms") 方式调用"""
        from solutions import timed

        @timed(unit="ms")
        def my_func():
            time.sleep(0.01)
            return "result"

        result = my_func()

        assert result == "result"
        captured = capsys.readouterr()
        # 只有 verbose=True 时才输出
        assert "ms" not in captured.out  # 默认 verbose=False

    def test_timed_with_verbose(self, capsys):
        """@timed(unit="ms", verbose=True) 方式调用"""
        from solutions import timed

        @timed(unit="ms", verbose=True)
        def my_func():
            time.sleep(0.01)
            return "result"

        result = my_func()

        assert result == "result"
        captured = capsys.readouterr()
        assert "计时" in captured.out


class TestWhenDecorator:
    """条件装饰器测试"""

    def test_when_condition_true(self):
        """条件为 True 时执行函数"""
        from solutions import when

        @when(lambda: True)
        def my_func():
            return "executed"

        result = my_func()
        assert result == "executed"

    def test_when_condition_false_skip(self):
        """条件为 False 且 action="skip" 时跳过"""
        from solutions import when

        @when(lambda: False, action="skip")
        def my_func():
            return "executed"

        result = my_func()
        assert result is None

    def test_when_condition_false_error(self):
        """条件为 False 且 action="error" 时抛出异常"""
        from solutions import when

        @when(lambda: False, action="error")
        def my_func():
            return "executed"

        with pytest.raises(RuntimeError, match="条件不满足"):
            my_func()


class TestDebugTimedDecorator:
    """组合装饰器测试"""

    def test_debug_timed_combined(self, capsys):
        """组合日志和计时"""
        from solutions import debug_timed

        @debug_timed(level="INFO", unit="ms")
        def my_func():
            time.sleep(0.01)
            return 42

        result = my_func()

        assert result == 42
        captured = capsys.readouterr()
        assert "INFO" in captured.out
        assert "ms" in captured.out
        assert "my_func" in captured.out

    def test_debug_timed_without_args(self, capsys):
        """组合装饰器无参调用"""
        from solutions import debug_timed

        @debug_timed
        def my_func():
            return "done"

        result = my_func()

        assert result == "done"
        captured = capsys.readouterr()
        assert "DEBUG" in captured.out  # 默认级别


class TestOptionalDecoratorEdgeCases:
    """可选参数装饰器边界情况测试"""

    def test_preserve_function_metadata(self):
        """装饰器应该保留函数元信息"""
        from solutions import optional_log as log

        @log(level="DEBUG")
        def my_function(x, y):
            """My docstring"""
            return x + y

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring"

    def test_multiple_decorators_same_type(self):
        """多个同类型装饰器应该正常工作"""
        from solutions import optional_log as log

        @log(level="INFO")
        @log(level="WARNING")
        def my_func():
            return "result"

        result = my_func()
        assert result == "result"

    def test_decorator_with_kwargs(self):
        """装饰器应该正确处理关键字参数"""
        from solutions import optional_log as log

        @log(level="INFO")
        def my_func(a, b, c=10):
            return a + b + c

        result = my_func(1, 2, c=3)
        assert result == 6
