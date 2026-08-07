"""P02 参考答案 3: 装饰器链实现验证器"""

import functools
import inspect
import time
import signal
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def log(func: Callable[P, R]) -> Callable[P, R]:
    """日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"[LOG] 调用 {func.__name__}, 参数: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} 返回: {result}")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 0.1):
    """重试装饰器工厂"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"[RETRY] {func.__name__} 失败: {e}, 重试...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def validate(**schemas):
    """参数验证装饰器工厂"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for param_name, expected_type in schemas.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{func.__name__} 的参数 {param_name} "
                            f"类型错误: 期望 {expected_type.__name__}, "
                            f"实际 {type(value).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def timeout(seconds: float):
    """超时装饰器工厂"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            def timeout_handler(signum, frame):
                raise TimeoutError(f"{func.__name__} 执行超时 ({seconds}s)")

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(seconds))

            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        return wrapper
    return decorator
