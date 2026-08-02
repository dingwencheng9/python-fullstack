"""

from __future__ import annotations

Python 3.13 装饰器特性演示

本模块展示 Python 3.13 的新特性在装饰器中的应用：
1. PEP 695: 新泛型语法 (type parameters)
2. Free-threading 考量 (PEP 703)
3. 改进的错误提示
4. 性能优化

作者: Python 3.13 全栈课程
日期: 2026-06-08
Python版本: 3.13+
"""

from collections.abc import Callable
import functools
from threading import Lock
import time

# ============================================
# PEP 695: 新泛型语法演示
# ============================================


def cache_generic[T](func: Callable[..., T]) -> Callable[..., T]:
    """
    使用 PEP 695 语法的泛型缓存装饰器

    Python 3.13+ 新特性：
    - 使用 [T] 声明类型参数，无需从 typing 导入 TypeVar
    - 类型推断更精确，IDE 支持更好

    Args:
        func: 被装饰的函数，返回类型为 T

    Returns:
        包装后的函数，保持相同的返回类型 T
    """
    cache: dict[tuple, T] = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> T:
        # 简化缓存键（只使用 args，避免不可哈希类型问题）
        key = args
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    wrapper.cache = cache
    wrapper.cache_clear = cache.clear
    return wrapper


@cache_generic
def fibonacci(n: int) -> int:
    """斐波那契数列（泛型缓存版本）"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def validate_return[T, R](
    validator: Callable[[R], bool], error_msg: str = "返回值验证失败"
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """
    使用 PEP 695 的返回值验证装饰器

    Python 3.13 特性：
    - [T, R] 声明多个类型参数
    - 类型推断自动传播
    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> R:
            result = func(*args, **kwargs)
            if not validator(result):
                raise ValueError(f"{error_msg}: {result}")
            return result

        return wrapper

    return decorator


@validate_return(lambda x: x > 0, "结果必须为正数")
def calculate_profit(revenue: int, cost: int) -> int:
    """计算利润（带返回值验证）"""
    return revenue - cost


# ============================================
# Free-threading (PEP 703) 考量演示
# ============================================


class ThreadSafeCounter:
    """
    线程安全的计数装饰器

    Free-threading（PEP 703/779）考量：
    - 在标准 Python 3.13 / 3.14 构建中，GIL 仍然存在，Lock 是必需的
    - 在 free-threading 构建（python3.13t / python3.14t）中，这个 Lock 变得更加关键
    - Free-threading 模式下，不加锁的 self.count += 1 会产生竞态条件

    性能说明：
    - GIL 模式：Lock 开销小，因为 GIL 已经序列化了大部分操作
    - Free-threading 模式：Lock 开销更大，但可以真正并行执行多个线程
    """

    def __init__(self, func: Callable) -> None:
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0
        # 线程安全：在 Python 3.14 下这个锁是必需的
        self._lock = Lock()

    def __call__(self, *args, **kwargs):
        # 使用锁保护计数器，确保 Free-threading 模式下的安全性
        with self._lock:
            self.count += 1
            current_count = self.count

        print(f"🔒 [线程安全] {self.func.__name__} 调用次数: {current_count}")
        return self.func(*args, **kwargs)

    def reset(self) -> None:
        """重置计数器（线程安全）"""
        with self._lock:
            self.count = 0


@ThreadSafeCounter
def process_task(task_id: int) -> str:
    """处理任务（可在多线程环境中安全调用）"""
    return f"Task {task_id} completed"


# ============================================
# 改进的性能计时装饰器（Python 3.13 优化版）
# ============================================


def precise_timer(func: Callable) -> Callable:
    """
    高精度计时装饰器

    Python 3.13 优化：
    - 使用 time.perf_counter_ns() 获取纳秒级精度
    - 避免浮点运算的精度损失
    - 在 Python 3.13 中，perf_counter 的实现进一步优化
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_ns = time.perf_counter_ns()
        result = func(*args, **kwargs)
        elapsed_ns = time.perf_counter_ns() - start_ns

        # 根据耗时选择合适的单位
        if elapsed_ns < 1000:
            print(f"⏱️  {func.__name__} 耗时: {elapsed_ns}ns")
        elif elapsed_ns < 1_000_000:
            print(f"⏱️  {func.__name__} 耗时: {elapsed_ns / 1000:.2f}μs")
        elif elapsed_ns < 1_000_000_000:
            print(f"⏱️  {func.__name__} 耗时: {elapsed_ns / 1_000_000:.2f}ms")
        else:
            print(f"⏱️  {func.__name__} 耗时: {elapsed_ns / 1_000_000_000:.4f}s")

        return result

    return wrapper


@precise_timer
def fast_operation() -> int:
    """快速操作（纳秒级）"""
    return sum(range(100))


@precise_timer
def slow_operation() -> None:
    """慢速操作（毫秒级）"""
    time.sleep(0.01)


# ============================================
# 现代类型提示：使用内置泛型和管道符
# ============================================


def optional_cache[T](
    ttl: float | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    可选 TTL 的缓存装饰器

    Python 3.13 类型提示最佳实践：
    - 使用 float | None 而非 Optional[float]
    - 使用内置 dict 而非 typing.Dict
    - 使用 PEP 695 泛型语法
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: dict[tuple, tuple[T, float]] = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            if key in cache:
                value, expire_time = cache[key]
                if ttl is None or now < expire_time:
                    return value
                del cache[key]

            result = func(*args, **kwargs)
            expire = now + ttl if ttl is not None else float("inf")
            cache[key] = (result, expire)
            return result

        wrapper.cache_clear = cache.clear
        return wrapper

    return decorator


@optional_cache(ttl=5.0)
def fetch_data(user_id: int) -> dict[str, int | str]:
    """获取用户数据（5秒缓存）"""
    return {"id": user_id, "name": f"User_{user_id}", "score": 100}


# ============================================
# 演示函数
# ============================================


def demo_pep695_generics() -> None:
    """演示 PEP 695 泛型语法"""
    print("\n" + "=" * 60)
    print("1. PEP 695: 新泛型语法")
    print("=" * 60)

    # 测试泛型缓存
    result1 = fibonacci(10)
    print(f"fibonacci(10) = {result1}")

    result2 = fibonacci(10)  # 从缓存返回
    print(f"fibonacci(10) [cached] = {result2}")

    # 测试返回值验证
    try:
        profit = calculate_profit(100, 50)
        print(f"✅ 利润计算成功: {profit}")
    except ValueError as e:
        print(f"❌ 验证失败: {e}")

    try:
        loss = calculate_profit(50, 100)
        print(f"利润: {loss}")
    except ValueError as e:
        print(f"❌ 验证失败: {e}")


def demo_free_threading() -> None:
    """演示 Free-threading 考量"""
    print("\n" + "=" * 60)
    print("2. Free-threading (PEP 703) 线程安全")
    print("=" * 60)
    print("💡 提示: 使用 python3.13t 运行以体验无 GIL 模式\n")

    # 单线程测试
    process_task(1)
    process_task(2)
    process_task(3)

    print(f"\n总调用次数: {process_task.count}")

    # 多线程测试演示（需要 import threading）
    print("\n💡 在生产环境中，应使用 threading 模块进行并发测试")
    print("   例如: with ThreadPoolExecutor() as executor:")
    print("         executor.map(process_task, range(100))")


def demo_precise_timing() -> None:
    """演示高精度计时"""
    print("\n" + "=" * 60)
    print("3. 纳秒级精度计时 (Python 3.13 优化)")
    print("=" * 60)

    fast_operation()
    slow_operation()


def demo_modern_typing() -> None:
    """演示现代类型提示"""
    print("\n" + "=" * 60)
    print("4. 现代类型提示：内置泛型 + 管道符")
    print("=" * 60)

    data1 = fetch_data(1001)
    print(f"获取数据: {data1}")

    data2 = fetch_data(1001)  # 从缓存返回
    print(f"获取数据 [cached]: {data2}")

    # 等待 6 秒后缓存过期
    print("\n💡 5秒后缓存将过期，重新获取数据")


def main() -> None:
    """主函数"""
    print("\n" + "=" * 60)
    print("  Python 3.13 装饰器特性演示")
    print("=" * 60)
    print("\n🚀 本演示展示 Python 3.13 的新特性")
    print("   运行环境要求: Python 3.13+\n")

    demo_pep695_generics()
    demo_free_threading()
    demo_precise_timing()
    demo_modern_typing()

    print("\n" + "=" * 60)
    print("  演示完成")
    print("=" * 60)
    print("\n✨ Python 3.13 关键特性:")
    print("  1. PEP 695: 简化的泛型语法 [T]")
    print("  2. PEP 703: Free-threading (实验性)")
    print("  3. 改进的 REPL 和错误提示")
    print("  4. 性能优化（JIT 编译器实验）")
    print("\n💡 要启用 Free-threading:")
    print("  $ python3.13t script.py    # 使用 freethreaded 构建（PEP 703 试验性）")
    print("  $ python3.14t script.py    # 使用 freethreaded 构建（PEP 779 官方支持）")
    print()


if __name__ == "__main__":
    main()
