"""L14 示例 1: 带参装饰器基础

演示三层嵌套结构的装饰器工厂模式。

运行方式: python examples/01_parameterized_decorators.py
"""

from functools import wraps
import time


# ============================================================
# 1.1 无参装饰器 vs 带参装饰器
# ============================================================

def simple_timer(func):
    """无参装饰器：功能固定"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"耗时: {time.time() - start:.4f}s")
        return result
    return wrapper


def timer(unit: str = "s"):
    """带参装饰器：可以配置行为

    Args:
        unit: 时间单位，"s" 表示秒，"ms" 表示毫秒
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            if unit == "ms":
                print(f"耗时: {elapsed * 1000:.4f}ms")
            else:
                print(f"耗时: {elapsed:.4f}s")
            return result
        return wrapper
    return decorator


# ============================================================
# 1.2 重试装饰器
# ============================================================

def retry(max_attempts: int = 3, delay: float = 1):
    """重试装饰器工厂

    Args:
        max_attempts: 最大重试次数
        delay: 重试间隔（秒）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"第 {attempt} 次失败，{delay}s 后重试...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


# ============================================================
# 1.3 缓存装饰器（简化版）
# ============================================================

def cache(max_size: int = 128):
    """缓存装饰器工厂

    Args:
        max_size: 缓存最大条目数
    """
    def decorator(func):
        cache_store: dict = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = (args, tuple(sorted(kwargs.items())))

            # 检查缓存
            if key in cache_store:
                print(f"[缓存命中] {func.__name__}")
                return cache_store[key]

            # 执行函数
            result = func(*args, **kwargs)

            # 存入缓存（简单的 FIFO）
            if len(cache_store) >= max_size:
                cache_store.pop(next(iter(cache_store)))
            cache_store[key] = result

            return result

        # 暴露缓存管理接口
        wrapper.cache_clear = lambda: cache_store.clear()
        wrapper.cache_info = lambda: {"size": len(cache_store), "max_size": max_size}

        return wrapper
    return decorator


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    # 测试带参装饰器
    @timer(unit="ms")
    def slow_function():
        time.sleep(0.1)
        return "done"

    @timer()
    def fast_function():
        return "instant"

    print("=== 带参装饰器测试 ===")
    slow_function()
    fast_function()

    # 测试重试装饰器
    @retry(max_attempts=3, delay=0.1)
    def maybe_fail():
        import random
        if random.random() < 0.7:
            raise ValueError("Random failure")
        return "Success!"

    print("\n=== 重试装饰器测试 ===")
    try:
        result = maybe_fail()
        print(f"结果: {result}")
    except ValueError as e:
        print(f"最终失败: {e}")

    # 测试缓存装饰器
    @cache(max_size=10)
    def expensive_computation(n: int) -> int:
        print(f"[计算中] n={n}")
        return n * n * n

    print("\n=== 缓存装饰器测试 ===")
    expensive_computation(5)
    expensive_computation(5)  # 缓存命中
    expensive_computation(5)  # 缓存命中
    expensive_computation(6)
    print(f"缓存状态: {expensive_computation.cache_info()}")
