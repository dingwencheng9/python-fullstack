"""
L15: 函数式编程 - 组合装饰器练习解答

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
    """将多个装饰器组合成一个（从右到左应用）"""

    def composed(func: F) -> F:
        result = func
        for decorator in reversed(decorators):
            result = decorator(result)
        return result  # type: ignore[return-value]

    return composed


def pipe_decorators(*decorators):
    """将多个装饰器用管道方式组合（从左到右应用）"""

    def piped(func: F) -> F:
        result = func
        for decorator in decorators:
            result = decorator(result)
        return result  # type: ignore[return-value]

    return piped
