"""L14 练习 4: 可选参数装饰器 [模板型练习]

难度: ⭐⭐⭐⭐☆（中高级）
模式: 模板型 - 根据需求描述实现完整功能

任务要求:
1. 实现同时支持有参和无参调用的装饰器
2. 实现日志级别可配置的装饰器
3. 实现带条件的装饰器

参考示例: examples/04_optional_params.py
"""

from functools import wraps
from typing import Callable, Optional, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')


# ============================================================
# 练习 4.1: 可选参数日志装饰器
# ============================================================

def log(func: Optional[Callable[P, R]] = None, *, level: str = "INFO") -> Callable:
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
    # TODO: 实现可选参数装饰器
    # 提示:
    # 1. 检查 func is None 来区分调用方式
    # 2. func is None -> @log(param=...) 方式，返回装饰器
    # 3. func is not None -> @log 方式，直接装饰
    pass


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
    # TODO: 实现可选参数计时装饰器
    # 提示:
    # 1. 记录开始时间
    # 2. 调用原函数
    # 3. 计算耗时并根据配置决定是否输出
    # 4. 根据单位转换显示
    pass


# ============================================================
# 练习 4.3: 条件装饰器
# ============================================================

def when(
    condition: Optional[Callable[..., bool]] = None,
    *,
    action: str = "skip"
):
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
    # TODO: 实现条件装饰器
    # 提示:
    # 1. 处理不同的 action 值
    # 2. 支持传入额外参数的条件函数
    # 3. 正确处理有参和无参两种调用方式
    pass


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
    # TODO: 实现组合装饰器
    # 提示:
    # 1. 结合 log 和 timed 的逻辑
    # 2. 可以分别定义辅助函数
    # 3. 确保日志包含耗时信息
    pass


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    import time

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

    print("""
    ┌─────────────────────────────────────────────────────────┐
    │ 可选参数装饰器的核心模式                                 │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │ def decorator(                                           │
    │     func: Optional[Callable] = None,  # 位置参数       │
    │     *,                                   # 强制关键字   │
    │     param1: str = "default",            # 关键字参数   │
    │     param2: int = 0                                     │
    │ ) -> Callable:                                           │
    │                                                         │
    │     def inner(f: Callable) -> Callable:                 │
    │         @wraps(f)                                       │
    │         def wrapper(*args, **kwargs):                   │
    │             # 装饰逻辑                                  │
    │             return f(*args, **kwargs)                   │
    │         return wrapper                                  │
    │                                                         │
    │     if func is None:                                    │
    │         # @decorator(param=...)                         │
    │         return inner                                    │
    │     else:                                               │
    │         # @decorator                                    │
    │         return inner(func)                              │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """)

    print("\n测试完成！")
