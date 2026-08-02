"""

from __future__ import annotations

L20 练习 1: 装饰器基础

学习目标：
- 实现简单的函数装饰器
- 理解 @wraps 的作用
- 正确处理函数参数

难度：★★☆☆☆
预计时间：30-45 分钟
"""

from collections.abc import Callable
from functools import wraps
import sys
import time

# ==================== 任务 1: 计时装饰器 ====================


def timer(func: Callable) -> Callable:
    """测量函数执行时间并返回原函数结果。"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result

    return wrapper


# ==================== 任务 2: 日志装饰器 ====================


def log_calls(func: Callable) -> Callable:
    """打印函数调用、返回值和异常信息。"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(arg) for arg in args]
        kwargs_repr = [f"{key}={value!r}" for key, value in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            print(f"{func.__name__} raised {type(exc).__name__}: {exc}")
            raise
        print(f"{func.__name__} returned {result!r}")
        return result

    return wrapper


# ==================== 任务 3: 调用计数装饰器 ====================


def count_calls(func: Callable) -> Callable:
    """统计函数调用次数，并提供 reset 方法。"""
    state = {"count": 0}

    @wraps(func)
    def wrapper(*args, **kwargs):
        state["count"] += 1
        wrapper.calls = state["count"]
        print(f"{func.__name__} has been called {state['count']} times")
        return func(*args, **kwargs)

    def reset() -> None:
        state["count"] = 0
        wrapper.calls = 0

    wrapper.calls = 0
    wrapper.reset = reset
    return wrapper


# ==================== 任务 4: 参数验证装饰器 ====================


def validate_types(*expected_types):
    """验证位置参数类型。"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for index, (arg, expected_type) in enumerate(
                zip(args, expected_types, strict=False)
            ):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Argument {index} must be {expected_type.__name__}, got {type(arg).__name__}"
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator


# ==================== 任务 5: 结果缓存装饰器（简单版）====================


def simple_cache(func: Callable) -> Callable:
    """简单结果缓存装饰器。"""
    cache = {}
    hits = 0
    misses = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal hits, misses
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            hits += 1
            return cache[key]
        misses += 1
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    def cache_info() -> dict[str, int]:
        return {"hits": hits, "misses": misses}

    def cache_clear() -> None:
        nonlocal hits, misses
        cache.clear()
        hits = 0
        misses = 0

    wrapper.cache_info = cache_info
    wrapper.cache_clear = cache_clear
    return wrapper


# ==================== 任务 6: 重复执行装饰器 ====================


def repeat(times: int):
    """重复执行函数并返回每次结果。"""
    if times <= 0:
        raise ValueError("times must be > 0")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]

        return wrapper

    return decorator


# ==================== 测试代码 ====================


def test_timer():
    """测试计时装饰器"""
    print("\n测试 1: 计时装饰器")
    print("=" * 50)

    @timer
    def slow_function():
        """慢速函数"""
        time.sleep(0.1)
        return "done"

    result = slow_function()
    assert result == "done", "函数返回值错误"
    assert slow_function.__name__ == "slow_function", "函数名未保留"
    assert slow_function.__doc__ == "慢速函数", "文档字符串未保留"
    print("✅ 计时装饰器测试通过")


def test_log_calls():
    """测试日志装饰器"""
    print("\n测试 2: 日志装饰器")
    print("=" * 50)

    @log_calls
    def add(a, b):
        """加法函数"""
        return a + b

    @log_calls
    def divide(a, b):
        """除法函数"""
        return a / b

    result = add(3, 5)
    assert result == 8, "函数返回值错误"

    try:
        divide(10, 0)
        raise AssertionError("应该抛出异常")
    except ZeroDivisionError:
        pass  # 预期的异常

    print("✅ 日志装饰器测试通过")


def test_count_calls():
    """测试调用计数装饰器"""
    print("\n测试 3: 调用计数装饰器")
    print("=" * 50)

    @count_calls
    def greet(name):
        return f"Hello, {name}!"

    greet("Alice")
    greet("Bob")
    greet("Charlie")

    assert greet.calls == 3, f"调用次数错误: 期望 3, 实际 {greet.calls}"

    greet.reset()
    assert greet.calls == 0, "reset() 未正确清零"

    greet("Dave")
    assert greet.calls == 1, "reset() 后计数错误"

    print("✅ 调用计数装饰器测试通过")


def test_validate_types():
    """测试参数验证装饰器"""
    print("\n测试 4: 参数验证装饰器")
    print("=" * 50)

    @validate_types(int, int)
    def add(a, b):
        return a + b

    # 正确的类型
    result = add(3, 5)
    assert result == 8, "函数返回值错误"

    # 错误的类型
    try:
        add("3", 5)
        raise AssertionError("应该抛出 TypeError")
    except TypeError as e:
        assert "Argument 0" in str(e), "错误信息不正确"

    try:
        add(3, "5")
        raise AssertionError("应该抛出 TypeError")
    except TypeError as e:
        assert "Argument 1" in str(e), "错误信息不正确"

    print("✅ 参数验证装饰器测试通过")


def test_simple_cache():
    """测试简单缓存装饰器"""
    print("\n测试 5: 简单缓存装饰器")
    print("=" * 50)

    call_count = 0

    @simple_cache
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        time.sleep(0.01)
        return x * 2

    # 第一次调用
    result1 = expensive_function(5)
    assert result1 == 10, "函数返回值错误"
    assert call_count == 1, "函数应该被调用一次"

    # 第二次调用（应该从缓存返回）
    result2 = expensive_function(5)
    assert result2 == 10, "缓存返回值错误"
    assert call_count == 1, "函数不应该被再次调用"

    # 不同参数
    result3 = expensive_function(10)
    assert result3 == 20, "函数返回值错误"
    assert call_count == 2, "新参数应该触发调用"

    # 检查缓存信息
    info = expensive_function.cache_info()
    assert info["hits"] == 1, f"缓存命中次数错误: {info}"
    assert info["misses"] == 2, f"缓存未命中次数错误: {info}"

    # 清空缓存
    expensive_function.cache_clear()
    expensive_function(5)
    assert call_count == 3, "清空缓存后应该重新调用"

    print("✅ 简单缓存装饰器测试通过")


def test_repeat():
    """测试重复执行装饰器"""
    print("\n测试 6: 重复执行装饰器")
    print("=" * 50)

    counter = 0

    @repeat(3)
    def increment():
        nonlocal counter
        counter += 1
        return counter

    results = increment()
    assert results == [1, 2, 3], f"返回值错误: {results}"
    assert len(results) == 3, "执行次数不正确"

    # 测试异常情况
    try:

        @repeat(0)
        def invalid_function():
            pass

        invalid_function()
        raise AssertionError("times <= 0 应该抛出 ValueError")
    except ValueError:
        pass  # 预期的异常

    print("✅ 重复执行装饰器测试通过")


def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("L20 练习 1: 装饰器基础")
    print("=" * 50)

    try:
        test_timer()
        test_log_calls()
        test_count_calls()
        test_validate_types()
        test_simple_cache()
        test_repeat()

        print("\n" + "=" * 50)
        print("🎉 所有测试通过！")
        print("=" * 50)
        print("\n✅ 完成情况:")
        print("  ✅ 任务 1: 计时装饰器")
        print("  ✅ 任务 2: 日志装饰器")
        print("  ✅ 任务 3: 调用计数装饰器")
        print("  ✅ 任务 4: 参数验证装饰器")
        print("  ✅ 任务 5: 简单缓存装饰器")
        print("  ✅ 任务 6: 重复执行装饰器")
        print("\n🎓 恭喜！你已经掌握了装饰器的基础用法。")
        print("💡 下一步：尝试 exercise_02_parameterized_decorators.py")

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        print("💡 提示: 请检查你的实现，确保符合所有要求")
        return False
    except Exception as e:
        print(f"\n❌ 发生错误: {type(e).__name__}: {e}")
        print("💡 提示: 请检查你的代码是否有语法错误或逻辑错误")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
