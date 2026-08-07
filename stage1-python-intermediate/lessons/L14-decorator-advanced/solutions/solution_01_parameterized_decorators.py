"""L14 练习 1 参考答案: 带参装饰器

参考实现:
1. rate_limit - 速率限制装饰器
2. deprecated - 废弃警告装饰器
3. memoize - 带过期时间的记忆化装饰器
"""

from functools import wraps
from typing import Callable, TypeVar, ParamSpec
import time
import warnings

P = ParamSpec('P')
R = TypeVar('R')


# ============================================================
# 练习 1.1: 速率限制装饰器
# ============================================================

def rate_limit(calls: int = 10, period: float = 60):
    """速率限制装饰器工厂

    限制函数在指定时间周期内的调用次数。

    Args:
        calls: 时间周期内的最大调用次数
        period: 时间周期（秒）

    Returns:
        装饰器

    Example:
        @rate_limit(calls=5, period=60)
        def api_call():
            return "OK"

        # 60 秒内最多调用 5 次
    """
    call_times: list[float] = []

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal call_times
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

            # 记录当前调用
            call_times.append(now)
            return func(*args, **kwargs)

        # 暴露查询接口
        wrapper.calls_remaining = lambda: calls - len(call_times)
        wrapper._call_times = lambda: list(call_times)
        return wrapper

    return decorator


# ============================================================
# 练习 1.2: 废弃警告装饰器
# ============================================================

def deprecated(reason: str = ""):
    """废弃警告装饰器工厂

    标记函数为已废弃，并输出警告信息。

    Args:
        reason: 废弃原因，推荐替代方案

    Returns:
        装饰器

    Example:
        @deprecated(reason="使用 new_function instead")
        def old_function():
            pass

        # 调用时会输出警告
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # 输出废弃警告
            warning_msg = f"{func.__module__}.{func.__qualname__} 已废弃"
            if reason:
                warning_msg += f": {reason}"
            warnings.warn(warning_msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        # 标记为废弃（用于代码检查工具）
        wrapper.__deprecated__ = True
        wrapper.__deprecation_reason__ = reason
        return wrapper

    return decorator


# ============================================================
# 练习 1.3: 带过期时间的记忆化装饰器
# ============================================================

def memoize(ttl: int = 300):
    """带过期时间的记忆化缓存装饰器工厂

    缓存函数调用结果，支持 TTL 过期。

    Args:
        ttl: 缓存有效期（秒），0 表示永不过期

    Returns:
        装饰器

    Example:
        @memoize(ttl=60)
        def expensive_computation(n):
            return n * n

        # 60 秒内的相同调用直接返回缓存结果
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache: dict[tuple, tuple[R, float]] = {}

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # 创建缓存键
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            # 检查缓存是否存在且未过期
            if key in cache:
                result, timestamp = cache[key]
                if ttl == 0 or now - timestamp < ttl:
                    return result
                # 缓存过期，删除
                del cache[key]

            # 计算并缓存结果
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result

        # 暴露缓存管理接口
        wrapper.cache_clear = lambda: cache.clear()
        wrapper.cache_info = lambda: {
            "size": len(cache),
            "ttl": ttl,
            "keys": len(cache)
        }
        return wrapper

    return decorator


# ============================================================
# 测试验证
# ============================================================

if __name__ == "__main__":
    import time

    print("=== 速率限制测试 ===")

    @rate_limit(calls=3, period=5)
    def limited_api():
        return "API 响应"

    for i in range(5):
        try:
            result = limited_api()
            remaining = limited_api.calls_remaining()
            print(f"  第 {i+1} 次成功，剩余调用: {remaining}")
        except RuntimeError as e:
            print(f"  第 {i+1} 次失败: {e}")

    print("\n=== 废弃警告测试 ===")

    @deprecated(reason="使用 new_calc 替代")
    def old_calc(x):
        return x * 2

    result = old_calc(10)
    print(f"  结果: {result}")

    print("\n=== 记忆化缓存测试 ===")

    @memoize(ttl=1)
    def fibonacci(n):
        print(f"  [计算] fibonacci({n})")
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print(f"  fibonacci(10) = {fibonacci(10)}")
    print(f"  fibonacci(10) = {fibonacci(10)}")  # 缓存命中
    print("  等待 2 秒...")
    time.sleep(2)
    print(f"  fibonacci(10) = {fibonacci(10)}")  # 缓存过期

    print("\n所有测试通过!")
