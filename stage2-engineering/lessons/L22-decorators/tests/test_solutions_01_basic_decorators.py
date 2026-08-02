"""L20 装饰器测试 - solution_01_basic_decorators"""

from __future__ import annotations

import time

import pytest


class TestTimer:
    """测试 timer 装饰器"""

    def test_timer_basic(self, capsys, solutions):
        """测试基本计时功能"""
        timer = solutions.solution_01_basic_decorators.timer

        @timer
        def quick_func():
            time.sleep(0.01)
            return "done"

        result = quick_func()
        assert result == "done"

        captured = capsys.readouterr()
        assert "quick_func took" in captured.out
        assert "s" in captured.out

    def test_timer_with_args(self, capsys, solutions):
        """测试带参数的函数计时"""
        timer = solutions.solution_01_basic_decorators.timer

        @timer
        def add(a, b):
            return a + b

        result = add(2, 3)
        assert result == 5

        captured = capsys.readouterr()
        assert "add took" in captured.out

    def test_timer_preserves_metadata(self, solutions):
        """测试元信息保留"""
        timer = solutions.solution_01_basic_decorators.timer

        @timer
        def documented_func():
            """This is a docstring"""

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "This is a docstring"


class TestLogCalls:
    """测试 log_calls 装饰器"""

    def test_log_calls_basic(self, capsys, solutions):
        """测试基本日志记录"""
        log_calls = solutions.solution_01_basic_decorators.log_calls

        @log_calls
        def greet(name):
            return f"Hello, {name}"

        result = greet("Alice")
        assert result == "Hello, Alice"

        captured = capsys.readouterr()
        assert "Calling greet('Alice')" in captured.out
        assert "greet returned 'Hello, Alice'" in captured.out

    def test_log_calls_with_kwargs(self, capsys, solutions):
        """测试带关键字参数的日志"""
        log_calls = solutions.solution_01_basic_decorators.log_calls

        @log_calls
        def create_user(name, age=0):
            return {"name": name, "age": age}

        result = create_user("Bob", age=25)
        assert result == {"name": "Bob", "age": 25}

        captured = capsys.readouterr()
        assert "Calling create_user" in captured.out
        assert "Bob" in captured.out
        assert "age=25" in captured.out

    def test_log_calls_exception(self, capsys, solutions):
        """测试异常情况的日志"""
        log_calls = solutions.solution_01_basic_decorators.log_calls

        @log_calls
        def failing_func():
            raise ValueError("test error")

        with pytest.raises(ValueError, match="test error"):
            failing_func()

        captured = capsys.readouterr()
        assert "Calling failing_func" in captured.out
        assert "raised ValueError" in captured.out


class TestCountCalls:
    """测试 count_calls 装饰器"""

    def test_count_calls_basic(self, capsys, solutions):
        """测试基本计数功能"""
        count_calls = solutions.solution_01_basic_decorators.count_calls

        @count_calls
        def func():
            return "ok"

        assert func.calls == 0

        func()
        assert func.calls == 1

        func()
        assert func.calls == 2

        captured = capsys.readouterr()
        assert "func has been called 1 times" in captured.out
        assert "func has been called 2 times" in captured.out

    def test_count_calls_reset(self, capsys, solutions):
        """测试 reset 功能"""
        count_calls = solutions.solution_01_basic_decorators.count_calls

        @count_calls
        def func():
            return "ok"

        # 调用几次
        func()
        func()
        assert func.calls == 2

        # 重置
        func.reset()
        assert func.calls == 0

        # 重置后重新计数
        func()
        captured = capsys.readouterr()
        assert "func has been called 1 times" in captured.out
        assert func.calls == 1

    def test_count_calls_multiple_functions(self, solutions):
        """测试多个函数独立计数"""
        count_calls = solutions.solution_01_basic_decorators.count_calls

        @count_calls
        def func1():
            return "1"

        @count_calls
        def func2():
            return "2"

        func1()
        func1()
        func2()

        assert func1.calls == 2
        assert func2.calls == 1


class TestValidateTypes:
    """测试 validate_types 装饰器"""

    def test_validate_types_success(self, solutions):
        """测试类型验证成功"""
        validate_types = solutions.solution_01_basic_decorators.validate_types

        @validate_types(int, int)
        def add(a, b):
            return a + b

        result = add(2, 3)
        assert result == 5

    def test_validate_types_failure(self, solutions):
        """测试类型验证失败"""
        validate_types = solutions.solution_01_basic_decorators.validate_types

        @validate_types(int, int)
        def add(a, b):
            return a + b

        with pytest.raises(TypeError, match="Argument 0 must be int"):
            add("2", 3)

        with pytest.raises(TypeError, match="Argument 1 must be int"):
            add(2, "3")

    def test_validate_types_mixed(self, solutions):
        """测试混合类型验证"""
        validate_types = solutions.solution_01_basic_decorators.validate_types

        @validate_types(str, int)
        def repeat_string(s, n):
            return s * n

        result = repeat_string("hi", 3)
        assert result == "hihihi"

        with pytest.raises(TypeError):
            repeat_string(123, 3)


class TestSimpleCache:
    """测试 simple_cache 装饰器"""

    def test_cache_basic(self, solutions):
        """测试基本缓存功能"""
        simple_cache = solutions.solution_01_basic_decorators.simple_cache
        call_count = 0

        @simple_cache
        def expensive_func(n):
            nonlocal call_count
            call_count += 1
            return n * 2

        # 第一次调用
        result1 = expensive_func(5)
        assert result1 == 10
        assert call_count == 1

        # 第二次调用（应该从缓存返回）
        result2 = expensive_func(5)
        assert result2 == 10
        assert call_count == 1  # 没有增加

        # 不同参数
        result3 = expensive_func(10)
        assert result3 == 20
        assert call_count == 2

    def test_cache_info(self, solutions):
        """测试缓存统计信息"""
        simple_cache = solutions.solution_01_basic_decorators.simple_cache

        @simple_cache
        def func(n):
            return n * 2

        func(1)
        func(1)  # 缓存命中
        func(2)
        func(2)  # 缓存命中

        info = func.cache_info()
        assert info["hits"] == 2
        assert info["misses"] == 2

    def test_cache_clear(self, solutions):
        """测试清除缓存"""
        simple_cache = solutions.solution_01_basic_decorators.simple_cache
        call_count = 0

        @simple_cache
        def func(n):
            nonlocal call_count
            call_count += 1
            return n * 2

        func(1)
        assert call_count == 1

        func(1)  # 缓存命中
        assert call_count == 1

        func.cache_clear()

        func(1)  # 缓存已清除，需要重新计算
        assert call_count == 2

    def test_cache_with_kwargs(self, solutions):
        """测试带关键字参数的缓存"""
        simple_cache = solutions.solution_01_basic_decorators.simple_cache

        @simple_cache
        def func(a, b=10):
            return a + b

        func(5, b=10)  # 第一次调用，缓存未命中
        func(5, b=10)  # 第二次调用，缓存命中
        func(5, b=20)  # 不同参数，缓存未命中

        info = func.cache_info()
        assert info["hits"] == 1  # 第二次调用命中
        assert info["misses"] == 2  # 第一次和第三次未命中


class TestRepeat:
    """测试 repeat 装饰器"""

    def test_repeat_basic(self, solutions):
        """测试基本重复功能"""
        repeat = solutions.solution_01_basic_decorators.repeat

        @repeat(3)
        def get_value():
            return 42

        result = get_value()
        assert result == [42, 42, 42]

    def test_repeat_with_args(self, solutions):
        """测试带参数的重复"""
        repeat = solutions.solution_01_basic_decorators.repeat

        @repeat(2)
        def add(a, b):
            return a + b

        result = add(2, 3)
        assert result == [5, 5]

    def test_repeat_invalid_times(self, solutions):
        """测试无效的重复次数"""
        repeat = solutions.solution_01_basic_decorators.repeat

        with pytest.raises(ValueError, match="times must be > 0"):

            @repeat(0)
            def func():
                pass

        with pytest.raises(ValueError, match="times must be > 0"):

            @repeat(-1)
            def func():
                pass

    def test_repeat_side_effects(self, solutions):
        """测试有副作用的函数重复"""
        repeat = solutions.solution_01_basic_decorators.repeat
        counter = []

        @repeat(3)
        def append_value():
            counter.append(1)
            return len(counter)

        result = append_value()
        assert result == [1, 2, 3]
        assert counter == [1, 1, 1]


class TestDecoratorComposition:
    """测试装饰器组合"""

    def test_timer_and_log_calls(self, capsys, solutions):
        """测试 timer 和 log_calls 组合"""
        timer = solutions.solution_01_basic_decorators.timer
        log_calls = solutions.solution_01_basic_decorators.log_calls

        @timer
        @log_calls
        def func(x):
            return x * 2

        result = func(5)
        assert result == 10

        captured = capsys.readouterr()
        assert "Calling func" in captured.out
        assert "func took" in captured.out

    def test_cache_and_count_calls(self, solutions):
        """测试 cache 和 count_calls 组合"""
        count_calls = solutions.solution_01_basic_decorators.count_calls
        simple_cache = solutions.solution_01_basic_decorators.simple_cache

        @count_calls
        @simple_cache
        def func(n):
            return n * 2

        func(1)
        func(1)  # 缓存命中
        func(2)

        # count_calls 计数所有调用（包括缓存命中）
        assert func.calls == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
