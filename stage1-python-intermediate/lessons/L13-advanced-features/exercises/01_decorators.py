"""
L13: 进阶特性 - 装饰器练习

实现各种装饰器。
"""

from functools import wraps
from inspect import signature


def log_calls(func):
    """日志装饰器：记录函数调用。"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 返回: {result}")
        return result

    return wrapper


def retry(times: int = 3):
    """重试装饰器工厂。"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
            raise last_error

        return wrapper

    return decorator


def memoize(func):
    """记忆化装饰器。"""
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


def validate_args(**validators):
    """参数验证装饰器工厂。"""

    def decorator(func):
        sig = signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            for name, validator in validators.items():
                if name in bound.arguments and not validator(bound.arguments[name]):
                    raise ValueError(f"参数 {name} 验证失败")
            return func(*args, **kwargs)

        return wrapper

    return decorator


# === 验证 ===

if __name__ == "__main__":
    # 测试日志
    @log_calls
    def add(a, b):
        return a + b

    assert add(1, 2) == 3

    # 测试记忆化
    @memoize
    def fib(n):
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    assert fib(10) == 55

    # 测试重试
    attempts = [0]

    @retry(times=3)
    def flaky():
        attempts[0] += 1
        if attempts[0] < 2:
            raise ValueError("Fail")
        return "Success"

    assert flaky() == "Success"

    # 测试参数验证
    @validate_args(x=lambda value: value > 0)
    def positive(x):
        return x

    assert positive(1) == 1

    print("✅ 所有测试通过！")
