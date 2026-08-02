"""

from __future__ import annotations

测试 Python 3.13 装饰器特性

验证 PEP 695 泛型、Free-threading 考量、现代类型提示等特性
"""

from threading import Thread
import time

from examples.python313_decorators import (
    ThreadSafeCounter,
    cache_generic,
    calculate_profit,
    fast_operation,
    fetch_data,
    fibonacci,
    optional_cache,
    precise_timer,
    process_task,
    slow_operation,
    validate_return,
)
import pytest


class TestPEP695Generics:
    """测试 PEP 695 新泛型语法"""

    def test_cache_generic_basic(self):
        """测试泛型缓存装饰器基本功能"""

        @cache_generic
        def multiply(a: int, b: int) -> int:
            return a * b

        # 第一次调用
        result1 = multiply(3, 4)
        assert result1 == 12

        # 验证缓存生效
        assert (3, 4) in multiply.cache
        assert multiply.cache[(3, 4)] == 12

        # 第二次调用应从缓存返回
        result2 = multiply(3, 4)
        assert result2 == 12

    def test_cache_generic_clear(self):
        """测试缓存清除功能"""

        @cache_generic
        def add(a: int, b: int) -> int:
            return a + b

        add(1, 2)
        assert len(add.cache) == 1

        add.cache_clear()
        assert len(add.cache) == 0

    def test_fibonacci_with_cache(self):
        """测试斐波那契函数的泛型缓存"""
        result = fibonacci(10)
        assert result == 55

        # 验证缓存中有多个值
        assert len(fibonacci.cache) > 0

    def test_validate_return_success(self):
        """测试返回值验证装饰器 - 成功情况"""
        profit = calculate_profit(100, 50)
        assert profit == 50

    def test_validate_return_failure(self):
        """测试返回值验证装饰器 - 失败情况"""
        with pytest.raises(ValueError, match="结果必须为正数"):
            calculate_profit(50, 100)

    def test_validate_return_custom(self):
        """测试自定义返回值验证"""

        @validate_return(lambda x: len(x) > 0, "列表不能为空")
        def get_items() -> list[int]:
            return []

        with pytest.raises(ValueError, match="列表不能为空"):
            get_items()


class TestFreeThreadingSafety:
    """测试 Free-threading 线程安全考量"""

    def test_thread_safe_counter_basic(self):
        """测试线程安全计数器基本功能"""

        @ThreadSafeCounter
        def simple_func() -> str:
            return "ok"

        assert simple_func.count == 0

        simple_func()
        assert simple_func.count == 1

        simple_func()
        assert simple_func.count == 2

    def test_thread_safe_counter_reset(self):
        """测试计数器重置功能"""

        @ThreadSafeCounter
        def func() -> None:
            pass

        func()
        func()
        assert func.count == 2

        func.reset()
        assert func.count == 0

    def test_thread_safe_counter_concurrent(self):
        """测试计数器在并发环境下的线程安全性"""

        @ThreadSafeCounter
        def concurrent_func() -> None:
            time.sleep(0.001)  # 模拟一些工作

        # 创建多个线程并发调用
        threads = []
        num_threads = 10
        calls_per_thread = 5

        def worker():
            for _ in range(calls_per_thread):
                concurrent_func()

        for _ in range(num_threads):
            t = Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # 验证计数正确（无竞态条件）
        expected = num_threads * calls_per_thread
        assert concurrent_func.count == expected

    def test_process_task_function(self, capsys):
        """测试预定义的 process_task 函数"""
        # 重置计数器
        process_task.reset()

        result = process_task(42)
        assert result == "Task 42 completed"

        captured = capsys.readouterr()
        assert "🔒 [线程安全]" in captured.out
        assert "process_task" in captured.out


class TestPreciseTiming:
    """测试高精度计时装饰器"""

    def test_precise_timer_decorator(self, capsys):
        """测试纳秒级精度计时"""

        @precise_timer
        def quick_func() -> int:
            return 42

        result = quick_func()
        assert result == 42

        captured = capsys.readouterr()
        assert "⏱️" in captured.out
        assert "quick_func" in captured.out
        # 应该显示纳秒或微秒级的时间
        assert any(unit in captured.out for unit in ["ns", "μs", "ms", "s"])

    def test_precise_timer_with_sleep(self, capsys):
        """测试计时器对较长操作的测量"""

        @precise_timer
        def slow_func() -> None:
            time.sleep(0.01)

        slow_func()

        captured = capsys.readouterr()
        assert "ms" in captured.out or "s" in captured.out

    def test_fast_operation_timing(self, capsys):
        """测试预定义的快速操作"""
        result = fast_operation()
        assert result == sum(range(100))

        captured = capsys.readouterr()
        assert "fast_operation" in captured.out

    def test_slow_operation_timing(self, capsys):
        """测试预定义的慢速操作"""
        slow_operation()

        captured = capsys.readouterr()
        assert "slow_operation" in captured.out
        assert "ms" in captured.out or "s" in captured.out


class TestModernTyping:
    """测试现代类型提示和可选缓存"""

    def test_optional_cache_basic(self):
        """测试可选 TTL 缓存的基本功能"""
        call_count = 0

        @optional_cache(ttl=1.0)
        def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # 第一次调用
        result1 = expensive_func(5)
        assert result1 == 10
        assert call_count == 1

        # 第二次调用（从缓存返回）
        result2 = expensive_func(5)
        assert result2 == 10
        assert call_count == 1  # 没有增加

    def test_optional_cache_ttl_expiration(self):
        """测试缓存过期"""
        call_count = 0

        @optional_cache(ttl=0.1)
        def func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        func(5)
        assert call_count == 1

        # 等待缓存过期
        time.sleep(0.15)

        func(5)
        assert call_count == 2  # 重新计算

    def test_optional_cache_no_ttl(self):
        """测试无 TTL 限制的缓存"""

        @optional_cache(ttl=None)
        def func(x: int) -> int:
            return x**2

        result1 = func(3)
        assert result1 == 9

        result2 = func(3)
        assert result2 == 9

    def test_optional_cache_clear(self):
        """测试缓存清除"""

        @optional_cache(ttl=10.0)
        def func(x: int) -> int:
            return x + 1

        func(1)
        func(2)

        # 清除缓存
        func.cache_clear()

        # 验证缓存已清空（需要重新计算）
        call_count = 0

        @optional_cache(ttl=10.0)
        def counted_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x + 1

        counted_func(1)
        counted_func.cache_clear()
        counted_func(1)

        assert call_count == 2

    def test_fetch_data_function(self):
        """测试预定义的 fetch_data 函数"""
        data = fetch_data(1001)

        assert isinstance(data, dict)
        assert data["id"] == 1001
        assert "name" in data
        assert "score" in data

        # 验证类型提示：返回值应该是 dict[str, int | str]
        assert isinstance(data["id"], int)
        assert isinstance(data["name"], str)
        assert isinstance(data["score"], int)


class TestTypeAnnotations:
    """测试类型注解的正确性"""

    def test_union_type_with_pipe(self):
        """验证使用管道符 | 的联合类型"""

        @optional_cache(ttl=None)
        def get_value(key: str) -> int | str | None:
            if key == "age":
                return 25
            if key == "name":
                return "Alice"
            return None

        assert get_value("age") == 25
        assert get_value("name") == "Alice"
        assert get_value("unknown") is None

    def test_builtin_generics(self):
        """验证内置泛型的使用"""

        @cache_generic
        def process_tuple(items: tuple[int, ...]) -> dict[str, int]:
            return {"sum": sum(items), "count": len(items)}

        # 使用元组（可哈希）而非列表
        result = process_tuple((1, 2, 3, 4, 5))
        assert result == {"sum": 15, "count": 5}


class TestIntegration:
    """集成测试"""

    def test_decorator_composition(self):
        """测试装饰器组合"""

        @precise_timer
        @cache_generic
        def complex_calculation(n: int) -> int:
            time.sleep(0.01)
            return n**2

        # 第一次调用（慢）
        result1 = complex_calculation(10)
        assert result1 == 100

        # 第二次调用（快，从缓存返回）
        result2 = complex_calculation(10)
        assert result2 == 100

    def test_all_decorators_preserve_metadata(self):
        """验证所有装饰器都保留了函数元信息"""

        @cache_generic
        def func1():
            """Docstring 1"""

        @precise_timer
        def func2():
            """Docstring 2"""

        @optional_cache(ttl=1.0)
        def func3():
            """Docstring 3"""

        assert func1.__doc__ == "Docstring 1"
        assert func2.__doc__ == "Docstring 2"
        assert func3.__doc__ == "Docstring 3"

        assert func1.__name__ == "func1"
        assert func2.__name__ == "func2"
        assert func3.__name__ == "func3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
