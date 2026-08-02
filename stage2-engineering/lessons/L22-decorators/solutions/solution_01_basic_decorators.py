"""

from __future__ import annotations

L20 练习 1 参考答案

解题思路：
本练习的完整实现展示了以下核心概念和技术要点：

1. **问题分析**：
   - 理解练习要求和核心目标
   - 识别关键技术点和实现难点
   - 确定合适的数据结构和算法

2. **实现策略**：
   - 采用模块化设计，每个函数/类职责单一
   - 使用 Python 3.13 类型提示增强代码可读性
   - 遵循 PEP 8 编码规范和最佳实践

3. **关键技术点**：
   - 正确使用语言特性（类型系统/异步/装饰器等）
   - 处理边界条件和异常情况
   - 编写清晰的文档字符串和注释

4. **测试验证**：
   - 覆盖正常流程和异常情况
   - 使用 pytest 进行单元测试
   - 确保代码质量和可维护性

学习建议：
- 先理解问题需求，再查看实现代码
- 对比自己的实现，找出差距和改进点
- 运行代码并修改参数，观察行为变化
- 尝试扩展功能，加深理解
"""

from collections.abc import Callable
from functools import wraps
import time


def timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result

    return wrapper


def log_calls(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        try:
            result = func(*args, **kwargs)
            print(f"{func.__name__} returned {result!r}")
            return result
        except Exception as e:
            print(f"{func.__name__} raised {type(e).__name__}: {e}")
            raise

    return wrapper


def count_calls(func: Callable) -> Callable:
    # 使用可变容器存储状态，以便 reset 函数可以正确修改
    state = {"count": 0}

    @wraps(func)
    def wrapper(*args, **kwargs):
        state["count"] += 1
        print(f"{func.__name__} has been called {state['count']} times")
        result = func(*args, **kwargs)
        wrapper.calls = state["count"]
        return result

    wrapper.calls = 0

    def reset():
        """重置调用计数器"""
        state["count"] = 0
        wrapper.calls = 0

    wrapper.reset = reset
    return wrapper


def validate_types(*expected_types):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i, (arg, expected_type) in enumerate(
                zip(args, expected_types, strict=False)
            ):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Argument {i} must be {expected_type.__name__}, got {type(arg).__name__}"
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def simple_cache(func: Callable) -> Callable:
    cache = {}
    hits = 0
    misses = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal hits, misses
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            hits += 1
            return cache[key]
        misses += 1
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    wrapper.cache_info = lambda: {"hits": hits, "misses": misses}
    wrapper.cache_clear = cache.clear
    return wrapper


def repeat(times: int):
    if times <= 0:
        raise ValueError("times must be > 0")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]

        return wrapper

    return decorator
