#!/usr/bin/env python3
"""
L20: 装饰器深度探索 - 综合演示程序

演示装饰器的各种用法和实际应用场景

💡 注意: 运行本脚本时，您可能会看到装饰器在导入阶段就产生的输出
   （例如 "🆕 创建新实例"）。这是正常行为，因为：

   1. Python 模块在首次导入时会执行顶层代码
   2. 装饰器在定义时就会执行（@singleton 等会在导入时检查类）
   3. 这种"预执行"是装饰器设计的一部分，而非错误

   如果您只需要使用装饰器而不产生导入输出，可以：
   - 直接导入需要的装饰器函数，而非运行完整演示
   - 将演示代码封装在 if __name__ == "__main__": 块中
"""

from __future__ import annotations

from functools import wraps
import time

# ==================== 1. 基础装饰器演示 ====================


def section(title):
    """打印分节标题"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n{'=' * 60}")
            print(f"  {title}")
            print("=" * 60)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@section("1. 简单装饰器 - 计时器")
def demo_basic_timer():
    """演示基础计时装饰器"""

    def timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"⏱️  {func.__name__} 执行时间: {elapsed:.4f}s")
            return result

        return wrapper

    @timer
    def slow_operation():
        """模拟慢速操作"""
        time.sleep(0.1)
        return "完成"

    result = slow_operation()
    print(f"结果: {result}")


@section("2. 带参数的装饰器 - 重试机制")
def demo_retry_decorator():
    """演示重试装饰器"""

    def retry(max_attempts=3):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        print(f"❌ 尝试 {attempt}/{max_attempts} 失败: {e}")
                        if attempt == max_attempts:
                            raise
                        time.sleep(0.1)
                return None

            return wrapper

        return decorator

    call_count = 0

    @retry(max_attempts=3)
    def unreliable_api():
        """模拟不稳定的 API 调用"""
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("网络错误")
        return {"status": "success", "data": "重要数据"}

    result = unreliable_api()
    print(f"✅ 最终结果: {result}")


@section("3. 类装饰器 - 调用统计")
def demo_class_decorator():
    """演示使用类实现的装饰器"""

    class CallStats:
        def __init__(self, func):
            wraps(func)(self)
            self.func = func
            self.call_count = 0
            self.total_time = 0

        def __call__(self, *args, **kwargs):
            self.call_count += 1
            start = time.perf_counter()
            result = self.func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            self.total_time += elapsed
            print(
                f"📊 {self.func.__name__}: 调用 {self.call_count} 次, "
                f"平均 {self.total_time / self.call_count:.4f}s"
            )
            return result

        def stats(self):
            return {
                "calls": self.call_count,
                "total_time": self.total_time,
                "avg_time": self.total_time / self.call_count
                if self.call_count > 0
                else 0,
            }

    @CallStats
    def process_data(data):
        time.sleep(0.05)
        return data.upper()

    process_data("hello")
    process_data("world")
    process_data("python")

    stats = process_data.stats()
    print(f"\n统计信息: {stats}")


@section("4. 装饰器链 - HTML 格式化")
def demo_decorator_chain():
    """演示多个装饰器组合使用"""

    def bold(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return f"<b>{func(*args, **kwargs)}</b>"

        return wrapper

    def italic(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return f"<i>{func(*args, **kwargs)}</i>"

        return wrapper

    def underline(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return f"<u>{func(*args, **kwargs)}</u>"

        return wrapper

    @bold
    @italic
    @underline
    def format_text(text):
        return text

    result = format_text("重要提示")
    print(f"HTML 输出: {result}")
    print("装饰器应用顺序: underline → italic → bold")


@section("5. 实战应用 - 缓存装饰器")
def demo_cache_decorator():
    """演示缓存装饰器的实际应用"""

    from functools import lru_cache

    @lru_cache(maxsize=128)
    def fibonacci(n):
        """斐波那契数列（带缓存）"""
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    # 测试性能差异
    print("计算斐波那契数列 fibonacci(35)...")

    start = time.perf_counter()
    result = fibonacci(35)
    elapsed = time.perf_counter() - start

    print(f"结果: {result}")
    print(f"⚡ 执行时间: {elapsed:.6f}s")
    print(f"📦 缓存信息: {fibonacci.cache_info()}")

    # 第二次调用（从缓存返回）
    start = time.perf_counter()
    _ = fibonacci(35)  # 触发缓存调用
    elapsed2 = time.perf_counter() - start
    print(f"\n第二次调用（缓存命中）: {elapsed2:.6f}s")
    print(f"性能提升: {elapsed / elapsed2:.0f}x 倍")


@section("6. 单例模式")
def demo_singleton():
    """演示单例装饰器"""

    def singleton(cls):
        instances = {}

        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
                print(f"🆕 创建新实例: {cls.__name__}")
            else:
                print(f"♻️  返回已有实例: {cls.__name__}")
            return instances[cls]

        return get_instance

    @singleton
    class Database:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            print(f"   连接到 {host}:{port}")

    db1 = Database("localhost", 5432)
    db2 = Database("remotehost", 3306)  # 参数被忽略

    print(f"\ndb1 is db2: {db1 is db2}")
    print(f"db1 配置: {db1.host}:{db1.port}")


@section("7. 条件装饰器")
def demo_conditional_decorator():
    """演示条件装饰器"""

    import os

    def debug_mode(func=None, *, enabled=None):
        if enabled is None:
            enabled = os.getenv("DEBUG", "false").lower() == "true"

        def decorator(f):
            if enabled:

                @wraps(f)
                def wrapper(*args, **kwargs):
                    print(f"🐛 DEBUG: 调用 {f.__name__}({args}, {kwargs})")
                    result = f(*args, **kwargs)
                    print(f"🐛 DEBUG: 返回 {result}")
                    return result

                return wrapper
            return f

        if func is None:
            return decorator
        return decorator(func)

    @debug_mode(enabled=True)
    def calculate(a, b):
        return a + b

    @debug_mode(enabled=False)
    def simple_func():
        return "no debug"

    calculate(10, 20)
    print()
    result2 = simple_func()
    print(f"简单函数结果: {result2}")


@section("8. 装饰器最佳实践总结")
def demo_best_practices():
    """装饰器最佳实践总结"""

    print("""
    ✅ 装饰器最佳实践:

    1. 始终使用 @wraps(func)
       - 保留函数名、文档字符串等元信息

    2. 使用 *args, **kwargs 传递参数
       - 确保装饰器适用于任意函数签名

    3. 装饰器命名清晰
       - @timer, @cache, @retry 而非 @decorator1

    4. 提供详细的文档字符串
       - 说明装饰器的作用、参数、返回值

    5. 考虑装饰器的组合性
       - 确保多个装饰器可以组合使用

    6. 避免过度使用
       - 保持简单，不要为了装饰器而装饰器

    7. 测试装饰器
       - 编写单元测试验证功能

    8. 性能考量
       - 装饰器会增加调用开销，注意性能影响
    """)


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  L20: 装饰器深度探索 - 综合演示")
    print("=" * 60)
    print("\n本演示将展示装饰器的各种用法和实际应用\n")

    # 运行所有演示
    demo_basic_timer()
    demo_retry_decorator()
    demo_class_decorator()
    demo_decorator_chain()
    demo_cache_decorator()
    demo_singleton()
    demo_conditional_decorator()
    demo_best_practices()

    # 结束语
    print("\n" + "=" * 60)
    print("  演示完成")
    print("=" * 60)
    print("\n💡 建议:")
    print("  1. 尝试修改代码，观察不同的行为")
    print("  2. 完成 exercises/ 中的练习")
    print("  3. 查看 solutions/ 中的参考答案")
    print("  4. 阅读 lesson.md 了解更多细节")
    print("\n🚀 开始你的装饰器之旅吧！\n")


if __name__ == "__main__":
    main()
