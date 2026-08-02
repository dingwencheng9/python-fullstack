"""

from __future__ import annotations

测试 solution_04_advanced_decorators.py - 装饰器进阶
"""

import pytest
from solutions.solution_04_advanced_decorators import (
    bold,
    compose,
    conditional_decorator,
    italic,
    underline,
)


class TestDecoratorChain:
    """测试装饰器链"""

    def test_bold_decorator(self):
        """测试 bold 装饰器"""

        @bold
        def greet(name):
            return f"Hello, {name}!"

        result = greet("Alice")
        assert result == "<b>Hello, Alice!</b>"

    def test_italic_decorator(self):
        """测试 italic 装饰器"""

        @italic
        def greet(name):
            return f"Hello, {name}!"

        result = greet("Bob")
        assert result == "<i>Hello, Bob!</i>"

    def test_underline_decorator(self):
        """测试 underline 装饰器"""

        @underline
        def greet(name):
            return f"Hello, {name}!"

        result = greet("Charlie")
        assert result == "<u>Hello, Charlie!</u>"

    def test_decorator_chain_order(self):
        """测试装饰器链顺序"""

        @bold
        @italic
        @underline
        def greet(name):
            return f"Hello, {name}!"

        result = greet("Dave")
        # 装饰器从下到上应用：underline -> italic -> bold
        assert result == "<b><i><u>Hello, Dave!</u></i></b>"

    def test_different_chain_order(self):
        """测试不同的装饰器链顺序"""

        @underline
        @bold
        @italic
        def greet(name):
            return f"Hello, {name}!"

        result = greet("Eve")
        # 顺序：italic -> bold -> underline
        assert result == "<u><b><i>Hello, Eve!</i></b></u>"

    def test_single_decorator(self):
        """测试单个装饰器"""

        @bold
        def msg():
            return "Important"

        assert msg() == "<b>Important</b>"

    def test_empty_string(self):
        """测试空字符串"""

        @bold
        @italic
        def empty():
            return ""

        assert empty() == "<b><i></i></b>"


class TestConditionalDecorator:
    """测试条件装饰器"""

    def test_condition_true(self, capsys):
        """测试条件为 True"""

        @conditional_decorator(True)
        def func():
            return "result"

        result = func()
        assert result == "result"

        captured = capsys.readouterr()
        # 条件为 True，应该有日志输出
        assert "Calling func" in captured.out
        assert "returned 'result'" in captured.out

    def test_condition_false(self, capsys):
        """测试条件为 False"""

        @conditional_decorator(False)
        def func():
            return "result"

        result = func()
        assert result == "result"

        captured = capsys.readouterr()
        # 条件为 False，不应该有日志输出
        assert "Calling func" not in captured.out

    def test_condition_with_args(self, capsys):
        """测试带参数的函数"""

        @conditional_decorator(True)
        def add(a, b):
            return a + b

        result = add(2, 3)
        assert result == 5

        captured = capsys.readouterr()
        assert "Calling add" in captured.out

    def test_multiple_functions_different_conditions(self, capsys):
        """测试多个函数不同条件"""

        @conditional_decorator(True)
        def logged_func():
            return "logged"

        @conditional_decorator(False)
        def silent_func():
            return "silent"

        result1 = logged_func()
        result2 = silent_func()

        assert result1 == "logged"
        assert result2 == "silent"

        captured = capsys.readouterr()
        assert "logged_func" in captured.out
        assert "silent_func" not in captured.out

    def test_condition_preserves_metadata(self):
        """测试元信息保留"""

        @conditional_decorator(True)
        def documented_func():
            """This is a docstring"""
            return "ok"

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "This is a docstring"

    def test_condition_with_exception(self, capsys):
        """测试异常情况"""

        @conditional_decorator(True)
        def failing_func():
            raise ValueError("test error")

        with pytest.raises(ValueError, match="test error"):
            failing_func()

        # 应该记录异常（根据实现）
        captured = capsys.readouterr()
        assert "Calling failing_func" in captured.out


class TestCompose:
    """测试装饰器组合器"""

    def test_compose_basic(self):
        """测试基本组合功能"""

        @compose(bold, italic)
        def greet(name):
            return f"Hello, {name}!"

        result = greet("Alice")
        assert result == "<b><i>Hello, Alice!</i></b>"

    def test_compose_three_decorators(self):
        """测试三个装饰器组合"""

        @compose(bold, italic, underline)
        def greet(name):
            return f"Hello, {name}!"

        result = greet("Bob")
        assert result == "<b><i><u>Hello, Bob!</u></i></b>"

    def test_compose_single_decorator(self):
        """测试单个装饰器"""

        @compose(bold)
        def msg():
            return "Important"

        assert msg() == "<b>Important</b>"

    def test_compose_order_matters(self):
        """测试组合顺序的重要性"""

        @compose(underline, italic, bold)
        def greet(name):
            return f"Hello, {name}!"

        result = greet("Charlie")
        # 顺序：bold -> italic -> underline
        assert result == "<u><i><b>Hello, Charlie!</b></i></u>"

    def test_compose_with_args(self):
        """测试带参数的函数"""

        @compose(bold, italic)
        def add(a, b):
            return str(a + b)

        result = add(2, 3)
        assert result == "<b><i>5</i></b>"

    def test_compose_empty_decorators(self):
        """测试空装饰器列表"""

        @compose()
        def func():
            return "unchanged"

        # 没有装饰器，返回原值
        assert func() == "unchanged"


class TestDecoratorCombinations:
    """测试装饰器组合场景"""

    def test_compose_with_conditional(self, capsys):
        """测试 compose 和 conditional_decorator 组合"""

        @compose(bold, italic)
        @conditional_decorator(True)
        def func():
            return "result"

        result = func()
        assert result == "<b><i>result</i></b>"

        captured = capsys.readouterr()
        assert "Calling func" in captured.out

    def test_conditional_before_formatting(self, capsys):
        """测试条件装饰在格式化之前"""

        @conditional_decorator(True)
        @bold
        @italic
        def func():
            return "result"

        result = func()
        assert result == "<b><i>result</i></b>"

        captured = capsys.readouterr()
        assert "Calling func" in captured.out

    def test_multiple_compose_calls(self):
        """测试多次使用 compose"""

        @compose(bold)
        @compose(italic)
        def func():
            return "result"

        result = func()
        assert result == "<b><i>result</i></b>"


class TestEdgeCases:
    """测试边界情况"""

    def test_decorator_with_none_result(self):
        """测试返回 None 的函数"""

        @bold
        def func():
            return None

        result = func()
        assert result == "<b>None</b>"

    def test_decorator_with_number_result(self):
        """测试返回数字的函数"""

        @italic
        def get_number():
            return 42

        result = get_number()
        assert result == "<i>42</i>"

    def test_decorator_with_complex_string(self):
        """测试复杂字符串"""

        @bold
        def get_html():
            return "<div>content</div>"

        result = get_html()
        assert result == "<b><div>content</div></b>"

    def test_conditional_with_boolean_result(self):
        """测试返回布尔值的函数"""

        @conditional_decorator(True)
        def is_valid():
            return True

        result = is_valid()
        assert result is True


class TestMetadataPreservation:
    """测试元信息保留"""

    def test_bold_preserves_name(self):
        """测试 bold 保留函数名"""

        @bold
        def my_func():
            pass

        assert my_func.__name__ == "my_func"

    def test_compose_preserves_metadata(self):
        """测试 compose 保留元信息"""

        @compose(bold, italic)
        def documented_func():
            """Important function"""

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "Important function"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
