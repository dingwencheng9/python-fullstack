"""

from __future__ import annotations

L20 练习 2 参考答案 - 带参数的装饰器

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
import warnings


def retry(max_attempts=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        print(f"Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        raise
            return None

        return wrapper

    return decorator


def timeout(seconds: float):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            if elapsed > seconds:
                raise TimeoutError(
                    f"Function took {elapsed:.2f}s, limit was {seconds}s"
                )
            return result

        return wrapper

    return decorator


def rate_limit(calls: int = 5, period: float = 1.0):
    """限流装饰器 - 限制函数在指定时间窗口内的调用次数"""
    call_times = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            nonlocal call_times

            # 移除过期的调用记录
            call_times = [t for t in call_times if now - t < period]

            # 检查是否超过限制
            if len(call_times) >= calls:
                raise RuntimeError(f"Rate limit exceeded: {calls} calls per {period}s")

            # 记录本次调用
            call_times.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecated(message: str | None = None):
    """弃用警告装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warning_msg = message if message else f"{func.__name__} is deprecated"
            warnings.warn(warning_msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    # 支持 @deprecated 和 @deprecated("message") 两种用法
    if callable(message):
        func = message
        message = None
        return decorator(func)
    return decorator


def singleton(cls):
    """单例装饰器 - 确保类只有一个实例"""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def validate_input(condition: Callable, error_msg: str = "Invalid input"):
    """输入验证装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not condition(*args, **kwargs):
                raise ValueError(error_msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def with_logging(func=None, *, level: str = "DEBUG"):
    """日志装饰器"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Executing: {f.__name__}")
            try:
                return f(*args, **kwargs)
            except Exception as e:
                print(f"[{level}] Exception in {f.__name__}: {e}")
                raise

        return wrapper

    # 支持 @with_logging 和 @with_logging(level="INFO") 两种用法
    if func is None:
        return decorator
    return decorator(func)


def cache_with_ttl(ttl=60.0):
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                result, expire_time = cache[key]
                if time.time() < expire_time:
                    return result
                del cache[key]
            result = func(*args, **kwargs)
            cache[key] = (result, time.time() + ttl)
            return result

        return wrapper

    return decorator


def require_permission(*permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if user is None:
                raise PermissionError("Not authenticated")
            if not any(perm in user.permissions for perm in permissions):
                raise PermissionError(f"Required: {permissions}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def debug(func=None, *, prefix="DEBUG"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f"{prefix}: {f.__name__}({args}) -> ", end="")
            result = f(*args, **kwargs)
            print(result)
            return result

        return wrapper

    if func is None:
        return decorator
    return decorator(func)
