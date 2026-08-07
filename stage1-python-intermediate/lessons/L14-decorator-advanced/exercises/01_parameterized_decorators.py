"""L14 练习 1: 带参装饰器 [模板型练习]

难度: ⭐⭐⭐☆☆（中级）
模式: 模板型 - 根据需求描述实现完整功能

任务要求:
1. 实现速率限制装饰器 @rate_limit
2. 实现废弃警告装饰器 @deprecated
3. 实现带过期时间的记忆化装饰器 @memoize

参考示例: examples/01_parameterized_decorators.py
"""

from functools import wraps
from typing import Callable, TypeVar, ParamSpec
import time

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
    # TODO: 实现速率限制装饰器
    # 提示:
    # 1. 使用列表记录每次调用时间
    # 2. 检查当前时间与最早调用时间的差值
    # 3. 超过限制时抛出 RuntimeError
    pass


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
        @deprecated(reason="Use new_function instead")
        def old_function():
            pass

        # 调用时会输出警告
    """
    # TODO: 实现废弃警告装饰器
    # 提示:
    # 1. 输出 DeprecationWarning 或 UserWarning
    # 2. 保留原函数元信息
    # 3. 可以记录废弃信息用于审计
    pass


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
    # TODO: 实现带过期时间的记忆化装饰器
    # 提示:
    # 1. 使用字典缓存 (key -> (value, timestamp))
    # 2. 创建缓存键时考虑 args 和 kwargs
    # 3. 检查缓存是否过期
    # 4. 暴露 cache_clear() 方法
    pass


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("=== 速率限制测试 ===")

    @rate_limit(calls=3, period=5)
    def limited_api():
        return "API 响应"

    # 测试应该在 5 秒内最多成功 3 次
    for i in range(5):
        try:
            result = limited_api()
            print(f"  第 {i+1} 次成功: {result}")
        except RuntimeError as e:
            print(f"  第 {i+1} 次失败: {e}")

    print("\n=== 废弃警告测试 ===")

    @deprecated(reason="使用 new_calc 替代")
    def old_calc(x):
        return x * 2

    # 应该输出警告信息
    result = old_calc(10)
    print(f"  结果: {result}")

    print("\n=== 记忆化缓存测试 ===")

    @memoize(ttl=1)
    def fibonacci(n):
        """斐波那契数列（用于测试缓存）"""
        print(f"  [计算] fibonacci({n})")
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    # 第一次调用
    print(f"  fibonacci(10) = {fibonacci(10)}")
    # 第二次调用（应该使用缓存）
    print(f"  fibonacci(10) = {fibonacci(10)}")
    # 缓存过期后
    print("  等待 2 秒...")
    time.sleep(2)
    print(f"  fibonacci(10) = {fibonacci(10)}")

    print("\n测试完成！")
