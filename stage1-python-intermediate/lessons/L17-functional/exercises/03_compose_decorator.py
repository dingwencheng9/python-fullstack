"""
L17: 函数式编程 - 组合装饰器练习

使用函数式编程思想实现装饰器组合。
"""

from functools import wraps
from typing import TypeVar, Any
from collections.abc import Callable


T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


def add_logging(func: F) -> F:
    """添加日志记录"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数 {func.__name__} 返回: {result}")
        return result

    return wrapper  # type: ignore[return-value]


def add_retry(max_attempts: int = 3):
    """添加重试机制"""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"重试 {attempt + 1}/{max_attempts}")

        return wrapper  # type: ignore[return-value]

    return decorator


def memoize(func: F) -> F:
    """添加缓存"""
    cache: dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper  # type: ignore[return-value]


def compose_decorators(*decorators):
    """将多个装饰器组合成一个。

    与函数组合一致，``compose_decorators(a, b)(func)`` 等价于
    ``a(b(func))``。
    """

    def composed(func: F) -> F:
        result = func
        for decorator in reversed(decorators):
            result = decorator(result)
        return result  # type: ignore[return-value]

    return composed


def pipe_decorators(*decorators):
    """将多个装饰器用管道方式组合。

    ``pipe_decorators(a, b)(func)`` 先应用 ``a``，再应用 ``b``。
    """

    def piped(func: F) -> F:
        result = func
        for decorator in decorators:
            result = decorator(result)
        return result  # type: ignore[return-value]

    return piped


# === 验证 ===

if __name__ == "__main__":
    # 测试基本装饰器
    @add_logging
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    result = greet("World")
    assert result == "Hello, World!"

    # 测试重试装饰器
    retry_state = {"attempts": 0}

    @add_retry(max_attempts=3)
    def flaky_function():
        retry_state["attempts"] += 1
        if retry_state["attempts"] < 3:
            raise ValueError("临时错误")
        return "成功"

    assert flaky_function() == "成功"

    # 测试缓存装饰器
    cache_state = {"call_count": 0}

    @memoize
    def expensive_computation(x: int) -> int:
        cache_state["call_count"] += 1
        return x * 2

    assert expensive_computation(5) == 10
    assert expensive_computation(5) == 10  # 应该使用缓存
    assert cache_state["call_count"] == 1  # 只计算了一次

    @compose_decorators(add_logging, add_retry(max_attempts=2))
    def composed_function():
        return "composed"

    assert composed_function() == "composed"

    @pipe_decorators(add_retry(max_attempts=2), add_logging)
    def piped_function():
        return "piped"

    assert piped_function() == "piped"

    print("✅ 所有测试通过！")
