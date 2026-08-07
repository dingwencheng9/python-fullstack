"""L14 练习 2 参考答案: 装饰器组合与执行顺序

参考实现:
1. log - 日志装饰器
2. timer - 计时装饰器
3. retry - 重试装饰器
4. cache - 缓存装饰器
"""

from functools import wraps
from typing import Callable, TypeVar, ParamSpec
import time

P = ParamSpec('P')
R = TypeVar('R')


# ============================================================
# 练习 2.1: 日志装饰器
# ============================================================

def log(level: str = "INFO"):
    """日志装饰器工厂

    记录函数调用信息。

    Args:
        level: 日志级别

    Returns:
        装饰器
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"[{level}] 调用 {func.__name__}({args}, {kwargs})")
            result = func(*args, **kwargs)
            print(f"[{level}] {func.__name__} 返回: {result!r}")
            return result
        return wrapper
    return decorator


# ============================================================
# 练习 2.2: 计时装饰器
# ============================================================

def timer(unit: str = "s"):
    """计时装饰器工厂

    测量函数执行时间。

    Args:
        unit: 时间单位 ("s", "ms", "us")

    Returns:
        装饰器
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start

            # 根据单位转换
            factors = {"s": 1, "ms": 1000, "us": 1_000_000}
            factor = factors.get(unit, 1)
            print(f"[计时] {func.__name__}: {elapsed * factor:.4f}{unit}")
            return result
        return wrapper
    return decorator


# ============================================================
# 练习 2.3: 重试装饰器
# ============================================================

def retry(max_attempts: int = 3, delay: float = 0.1):
    """重试装饰器工厂

    自动重试失败的操作。

    Args:
        max_attempts: 最大重试次数
        delay: 重试间隔（秒）

    Returns:
        装饰器
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"[重试] 第 {attempt} 次失败，{delay}s 后重试...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


# ============================================================
# 练习 2.4: 缓存装饰器
# ============================================================

def cache():
    """缓存装饰器（无参数）"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache_store: dict = {}

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # 创建缓存键
            key = (args, tuple(sorted(kwargs.items())))

            # 检查缓存
            if key in cache_store:
                print(f"[缓存命中] {func.__name__}")
                return cache_store[key]

            # 计算并缓存
            result = func(*args, **kwargs)
            cache_store[key] = result
            return result

        # 暴露缓存管理接口
        wrapper.cache_clear = lambda: cache_store.clear()
        wrapper.cache_info = lambda: {"size": len(cache_store)}
        return wrapper

    return decorator


# ============================================================
# 测试验证
# ============================================================

if __name__ == "__main__":
    import random

    print("=== 日志装饰器测试 ===")

    @log("INFO")
    def add(a, b):
        return a + b

    result = add(1, 2)
    print(f"  结果: {result}")

    print("\n=== 计时装饰器测试 ===")

    @timer(unit="ms")
    def slow_task():
        time.sleep(0.1)
        return "完成"

    result = slow_task()
    print(f"  结果: {result}")

    print("\n=== 装饰器组合测试 ===")

    @log("DEBUG")
    @timer(unit="ms")
    def combined_task(n):
        """同时记录日志和计时"""
        time.sleep(0.05)
        return n * 2

    result = combined_task(5)
    print(f"  最终结果: {result}")

    print("\n=== 执行顺序说明 ===")
    print("""
    @log
    @timer
    def func(): pass

    等价于: func = log(timer(func))

    执行顺序:
    1. func = timer(func) 返回 wrapped
    2. func = log(wrapped) 返回 logged_wrapped
    3. 调用 logged_wrapped
       -> 进入 log wrapper
       -> 进入 timer wrapper
       -> 执行原始 func
       <- 返回 timer wrapper
       <- 返回 log wrapper
    """)

    print("\n=== 重试装饰器测试 ===")

    attempt_count = 0

    @retry(max_attempts=3, delay=0.1)
    def unreliable_operation():
        global attempt_count
        attempt_count += 1
        if random.random() < 0.7:
            raise ConnectionError("网络错误")
        return "成功"

    try:
        result = unreliable_operation()
        print(f"  结果: {result}")
    except ConnectionError as e:
        print(f"  最终失败: {e}")

    print(f"  总尝试次数: {attempt_count}")

    print("\n=== 重试 + 缓存组合测试 ===")

    api_call_count = 0

    @cache()
    @retry(max_attempts=2, delay=0.1)
    def cached_api(endpoint):
        """带重试的缓存 API 调用"""
        global api_call_count
        api_call_count += 1
        if random.random() < 0.5:
            raise ConnectionError("连接失败")
        return f"数据来自 {endpoint}"

    # 第一次调用（可能重试）
    try:
        result = cached_api("/users")
        print(f"  第1次: {result}")
    except ConnectionError as e:
        print(f"  第1次失败: {e}")

    # 第二次调用相同参数（使用缓存，不会计数）
    try:
        result = cached_api("/users")
        print(f"  第2次（缓存）: {result}")
    except ConnectionError as e:
        print(f"  第2次失败: {e}")

    print(f"  实际 API 调用次数: {api_call_count}")

    print("\n所有测试通过!")
