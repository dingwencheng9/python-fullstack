"""L14 示例 4: 可选参数的装饰器

同时支持无参和有参调用模式的装饰器。

运行方式: python examples/04_optional_params.py
"""

from functools import wraps
from typing import Callable, Optional, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')


# ============================================================
# 4.1 可选参数装饰器基础
# ============================================================

def debug(func: Optional[Callable[P, R]] = None, *, prefix: str = "DEBUG") -> Callable:
    """可选参数的装饰器

    使用方式:
        @debug                    # 无参调用
        @debug()                 # 显式无参
        @debug(prefix="INFO")    # 有参调用

    Args:
        func: 被装饰的函数（当无参调用时）
        prefix: 日志前缀
    """
    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"[{prefix}] 调用 {f.__name__}({args}, {kwargs})")
            return f(*args, **kwargs)
        return wrapper

    # 关键逻辑：区分调用方式
    if func is None:
        # @debug() 或 @debug(prefix="INFO")
        return decorator
    else:
        # @debug（无括号）
        return decorator(func)


# ============================================================
# 4.2 复杂可选参数装饰器
# ============================================================

def rate_limit(
    func: Optional[Callable[P, R]] = None,
    *,
    calls: int = 10,
    period: float = 60
) -> Callable:
    """速率限制装饰器

    Args:
        func: 被装饰的函数（当无参调用时）
        calls: 时间周期内的最大调用次数
        period: 时间周期（秒）
    """
    import time
    call_times: list[float] = []

    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            now = time.time()

            # 清理过期的调用记录
            while call_times and now - call_times[0] > period:
                call_times.pop(0)

            # 检查是否超过限制
            if len(call_times) >= calls:
                wait_time = period - (now - call_times[0])
                raise RuntimeError(
                    f"速率限制: 超过 {calls} 次调用/ {period}s, "
                    f"需等待 {wait_time:.2f}s"
                )

            call_times.append(now)
            return f(*args, **kwargs)

        wrapper.calls_remaining = lambda: calls - len(call_times)
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


# ============================================================
# 4.3 可选参数 + 多功能装饰器
# ============================================================

def timed(
    func: Optional[Callable[P, R]] = None,
    *,
    unit: str = "s",
    verbose: bool = False
) -> Callable:
    """计时装饰器，支持多种配置

    Args:
        func: 被装饰的函数（当无参调用时）
        unit: 时间单位 ("s", "ms", "us")
        verbose: 是否输出详细信息
    """
    import time

    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            result = f(*args, **kwargs)
            elapsed = time.perf_counter() - start

            # 根据单位转换
            factors = {"s": 1, "ms": 1000, "us": 1_000_000}
            factor = factors.get(unit, 1)
            elapsed_display = elapsed * factor

            if verbose:
                print(f"[计时] {f.__name__}: {elapsed_display:.4f}{unit}")
            return result

        wrapper.last_elapsed = 0.0
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


# ============================================================
# 4.4 状态累积装饰器
# ============================================================

def memoize(func: Optional[Callable[P, R]] = None, *, ttl: int = 300):
    """记忆化缓存装饰器

    Args:
        func: 被装饰的函数（当无参调用时）
        ttl: 缓存有效期（秒），0 表示永久
    """
    import time

    cache: dict = {}

    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            # 检查缓存
            if key in cache:
                result, timestamp = cache[key]
                if ttl == 0 or now - timestamp < ttl:
                    return result
                del cache[key]

            # 计算并缓存
            result = f(*args, **kwargs)
            cache[key] = (result, now)
            return result

        wrapper.cache_clear = lambda: cache.clear()
        wrapper.cache_size = lambda: len(cache)
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("=== 可选参数装饰器 ===")
    print("""
    装饰器的三种调用方式:
    1. @decorator          -> decorator(func)
    2. @decorator()        -> decorator()(func)
    3. @decorator(param=1) -> decorator(param=1)(func)
    """)

    print("=== 三种调用方式测试 ===")

    @debug
    def func1():
        return "无参调用"

    @debug()
    def func2():
        return "显式无参"

    @debug(prefix="INFO")
    def func3():
        return "有参调用"

    func1()
    func2()
    func3()

    print("\n=== 速率限制装饰器 ===")

    @rate_limit(calls=3, period=5)
    def api_call():
        return "API 响应"

    for i in range(3):
        try:
            api_call()
            print(f"  第 {i+1} 次调用成功，剩余: {api_call.calls_remaining()}")
        except RuntimeError as e:
            print(f"  {e}")

    print("\n=== 计时装饰器 ===")

    import time

    @timed
    def fast():
        time.sleep(0.01)
        return "快速"

    @timed(unit="ms", verbose=True)
    def slow():
        time.sleep(0.1)
        return "慢速"

    fast()
    slow()

    print("\n=== 记忆化缓存装饰器 ===")

    @memoize(ttl=1)
    def compute(x):
        print(f"  [计算中] x={x}")
        return x * x

    print(compute(5))  # 计算
    print(compute(5))  # 缓存命中
    print(compute(6))  # 新计算
    print(f"缓存大小: {compute.cache_size()}")

    print("\n=== 组合使用 ===")

    @debug(prefix="INFO")
    @timed(unit="ms", verbose=True)
    @memoize
    def complex_computation(n: int) -> int:
        time.sleep(0.05)
        return sum(range(n))

    print(complex_computation(1000000))
    print(complex_computation(1000000))  # 缓存命中

    print("""
    ┌─────────────────────────────────────────────────────────┐
    │ 可选参数装饰器的关键实现                                 │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │ def decorator(func=None, *, key_param):                 │
    │     def inner(f):                                       │
    │         @wraps(f)                                       │
    │         def wrapper(...):                               │
    │             ...                                         │
    │         return wrapper                                  │
    │                                                         │
    │     if func is None:                                    │
    │         return inner  # @decorator(param=...)           │
    │     else:                                               │
    │         return inner(func)  # @decorator                │
    │                                                         │
    │ 关键点:                                                 │
    │   - func 参数放在第一位                                 │
    │   - 其他参数使用 * 强制关键字参数                        │
    │   - 检查 func is None 区分调用方式                      │
    └─────────────────────────────────────────────────────────┘
    """)
