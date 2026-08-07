"""L14 练习 4 参考答案: 可选参数装饰器

参考实现:
1. log - 可选参数日志装饰器
2. timed - 可选参数计时装饰器
3. when - 条件装饰器
4. debug_timed - 组合装饰器
"""

from functools import wraps
from typing import Callable, Optional, TypeVar, ParamSpec
import time

P = ParamSpec('P')
R = TypeVar('R')


# ============================================================
# 练习 4.1: 可选参数日志装饰器
# ============================================================

def log(
    func: Optional[Callable[P, R]] = None,
    *,
    level: str = "INFO"
) -> Callable:
    """可选参数的日志装饰器

    支持三种调用方式:
        @log                    # 使用默认级别
        @log()                  # 显式无参
        @log(level="DEBUG")    # 自定义级别

    Args:
        func: 被装饰的函数（无参调用时）
        level: 日志级别

    Returns:
        装饰后的函数或装饰器
    """
    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"[{level}] 调用 {f.__name__}({args}, {kwargs})")
            result = f(*args, **kwargs)
            print(f"[{level}] {f.__name__} 返回: {result!r}")
            return result
        return wrapper

    if func is None:
        # @log(param=...) 方式
        return decorator
    else:
        # @log 方式
        return decorator(func)


# ============================================================
# 练习 4.2: 可选参数计时装饰器
# ============================================================

def timed(
    func: Optional[Callable[P, R]] = None,
    *,
    unit: str = "s",
    verbose: bool = False
) -> Callable:
    """可选参数的计时装饰器

    支持多种配置方式。

    Args:
        func: 被装饰的函数
        unit: 时间单位 ("s", "ms", "us")
        verbose: 是否输出详细信息

    Example:
        @timed
        @timed(unit="ms")
        @timed(unit="ms", verbose=True)
    """
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
# 练习 4.3: 条件装饰器
# ============================================================

def when(
    condition: Optional[Callable[..., bool]] = None,
    *,
    action: str = "skip"
) -> Callable:
    """条件装饰器工厂

    根据条件决定是否执行被装饰的函数。

    Args:
        condition: 条件函数，返回 True 时执行函数
        action: 条件为 False 时的行为 ("skip", "warn", "error")

    Example:
        @when(lambda: settings.DEBUG)
        def debug_tool():
            pass

        @when(lambda x: x > 0, action="error")
        def positive_only(x):
            pass
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # 执行条件判断
            if condition is not None:
                try:
                    should_execute = condition(*args, **kwargs)
                except TypeError:
                    # 条件函数不接受这些参数
                    should_execute = condition()
            else:
                should_execute = True

            if not should_execute:
                if action == "skip":
                    return None  # type: ignore[return-value]
                elif action == "warn":
                    import warnings
                    warnings.warn(f"{func.__name__} 被跳过")
                    return None  # type: ignore[return-value]
                elif action == "error":
                    raise RuntimeError(f"{func.__name__} 条件不满足")

            return func(*args, **kwargs)
        return wrapper

    if condition is not None and callable(condition) and not isinstance(condition, type):
        # 检查是否是 lambda 或普通函数（而非类型）
        # 简单判断：如果有 __name__ 属性且不是类，则是函数
        if hasattr(condition, '__name__') and not condition.__name__.startswith('<'):
            # 可能是 @when(condition) 方式
            return decorator(condition)

    return decorator


# ============================================================
# 练习 4.4: 组合装饰器（可选挑战）
# ============================================================

def debug_timed(
    func: Optional[Callable[P, R]] = None,
    *,
    level: str = "DEBUG",
    unit: str = "ms"
) -> Callable:
    """组合日志和计时的装饰器

    同时实现日志记录和性能测量。
    """
    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            print(f"[{level}] 调用 {f.__name__}({args}, {kwargs})")

            result = f(*args, **kwargs)

            elapsed = time.perf_counter() - start
            factors = {"s": 1, "ms": 1000, "us": 1_000_000}
            factor = factors.get(unit, 1)
            print(f"[{level}] {f.__name__} 耗时: {elapsed * factor:.4f}{unit}, 返回: {result!r}")
            return result
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


# ============================================================
# 测试验证
# ============================================================

if __name__ == "__main__":
    print("=== 可选参数日志装饰器测试 ===")

    @log
    def func1():
        return "默认级别"

    @log()
    def func2():
        return "显式无参"

    @log(level="WARNING")
    def func3():
        return "WARNING 级别"

    func1()
    func2()
    func3()

    print("\n=== 可选参数计时装饰器测试 ===")

    @timed
    def task1():
        time.sleep(0.01)
        return "默认"

    @timed(unit="ms")
    def task2():
        time.sleep(0.01)
        return "毫秒"

    @timed(unit="ms", verbose=True)
    def task3():
        time.sleep(0.01)
        return "详细"

    task1()
    task2()
    task3()

    print("\n=== 条件装饰器测试 ===")

    debug_mode = True

    @when(lambda: debug_mode)
    def debug_info():
        return "调试信息"

    @when(lambda: not debug_mode)
    def production_code():
        return "生产环境代码"

    print(f"  debug_mode={debug_mode}: {debug_info()}")

    debug_mode = False
    print(f"  debug_mode={debug_mode}: {production_code()}")

    print("\n=== 组合装饰器测试 ===")

    @debug_timed(level="INFO", unit="ms")
    def complex_operation(n):
        time.sleep(0.05)
        return sum(range(n))

    result = complex_operation(100000)
    print(f"  结果: {result:,}")

    print("\n所有测试通过!")
