"""L14 练习 2: 装饰器组合与执行顺序 [模板型练习]

难度: ⭐⭐⭐☆☆（中级）
模式: 模板型 - 根据需求描述实现完整功能

任务要求:
1. 组合多个装饰器并理解执行顺序
2. 实现日志 + 计时组合装饰器
3. 实现重试 + 缓存组合装饰器

参考示例: examples/02_decorator_chaining.py
"""

from functools import wraps
import time
import random


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
    # TODO: 实现日志装饰器
    # 提示:
    # 1. 记录调用时间、函数名、参数
    # 2. 记录返回值（如果有）
    # 3. 使用合适的日志格式
    pass


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
    # TODO: 实现计时装饰器
    # 提示:
    # 1. 记录开始和结束时间
    # 2. 根据单位转换显示
    # 3. 返回原始函数返回值
    pass


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
    # TODO: 实现重试装饰器
    # 提示:
    # 1. 捕获异常
    # 2. 等待后重试
    # 3. 最后仍失败则抛出异常
    pass


# ============================================================
# 练习 2.4: 缓存装饰器
# ============================================================

def cache():
    """缓存装饰器（无参数）"""
    # TODO: 实现缓存装饰器
    # 提示:
    # 1. 简单的函数结果缓存
    # 2. 使用 (args, kwargs) 作为键
    pass


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
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

    @retry(max_attempts=3, delay=0.1)
    def unreliable_operation():
        if random.random() < 0.7:
            raise ConnectionError("网络错误")
        return "成功"

    try:
        result = unreliable_operation()
        print(f"  结果: {result}")
    except ConnectionError as e:
        print(f"  最终失败: {e}")

    print("\n=== 重试 + 缓存组合测试 ===")

    call_count = 0

    @cache()
    @retry(max_attempts=2, delay=0.1)
    def cached_api(endpoint):
        """带重试的缓存 API 调用"""
        global call_count
        call_count += 1
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

    print(f"  实际 API 调用次数: {call_count}")

    print("\n测试完成！")
