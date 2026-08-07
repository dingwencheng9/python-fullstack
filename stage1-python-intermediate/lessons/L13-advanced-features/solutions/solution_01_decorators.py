"""
L13: 高级特性 - 装饰器练习解答

实现各种装饰器。
"""

from functools import wraps
from time import perf_counter
from typing import TypeVar, Any
from collections.abc import Callable


F = TypeVar("F", bound=Callable[..., Any])


def timer(func: F) -> F:
    """计时装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"{func.__name__} 耗时: {elapsed:.4f}秒")
        return result

    return wrapper  # type: ignore[return-value]


def retry(max_attempts: int = 3, delay: float = 0):
    """重试装饰器"""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"重试 {attempt + 1}/{max_attempts}")
            raise last_exception

        return wrapper  # type: ignore[return-value]

    return decorator


def validate_args(**validators):
    """参数验证装饰器"""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = func.__code__.co_varnames[: func.__code__.co_argcount]
            bound = dict(zip(sig, args, strict=True))
            bound.update(kwargs)
            for name, validator in validators.items():
                if name in bound:
                    if not validator(bound[name]):
                        raise ValueError(f"参数 {name} 验证失败")
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def memoize(func: F) -> F:
    """缓存装饰器"""
    cache: dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper  # type: ignore[return-value]


def count_calls(func: F) -> F:
    """调用计数装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return func(*args, **kwargs)

    wrapper.call_count = 0  # type: ignore
    return wrapper  # type: ignore[return-value]


def log_calls(func: F) -> F:
    """日志记录装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 返回: {result}")
        return result

    return wrapper  # type: ignore[return-value]
