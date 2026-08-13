"""P02 示例 3: 装饰器链

演示 L14 装饰器进阶的核心概念：
- functools.wraps 保留元数据
- 装饰器工厂模式
- 装饰器链叠加顺序
- 常见装饰器实现

运行方式:
    python examples/03_decorator_chain.py
"""

import functools
import inspect
import logging
import time
import re
from typing import Callable, TypeVar, ParamSpec
from pathlib import Path

P = ParamSpec("P")
R = TypeVar("R")

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ============================================================
# 1. 基础装饰器
# ============================================================

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """日志装饰器 - 记录函数调用"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.debug(f"调用 {func.__name__}(args={args}, kwargs={kwargs})")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug(f"{func.__name__} 返回 {result} (耗时 {elapsed:.4f}s)")
        return result
    return wrapper


def log_calls_simple(func: Callable[P, R]) -> Callable[P, R]:
    """简化版日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"[LOG] 调用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


# ============================================================
# 2. 装饰器工厂
# ============================================================

def retry(max_attempts: int = 3, delay: float = 0.1):
    """重试装饰器工厂

    用法：
        @retry(max_attempts=5, delay=1.0)
        def unreliable_function():
            ...
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(f"{func.__name__} 失败 ({attempt}/{max_attempts}): {e}")
                        time.sleep(delay)
            raise last_exception  # type: ignore
        return wrapper
    return decorator


def validate(**schemas):
    """参数验证装饰器工厂

    用法：
        @validate(name=str, age=int)
        def create_user(name: str, age: int):
            ...
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # 合并位置参数和关键字参数
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for param_name, param_type in schemas.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not isinstance(value, param_type):
                        raise TypeError(
                            f"{func.__name__} 的参数 {param_name} "
                            f"类型错误: 期望 {param_type.__name__}, 实际 {type(value).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def pattern_match(param_name: str, pattern: str):
    r"""正则匹配验证装饰器工厂

    用法：
        @pattern_match("email", r"^[\w.-]+@[\w.-]+\.\w+$")
        def send_email(email: str):
            ...
    """
    compiled = re.compile(pattern)

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            if param_name in bound.arguments:
                value = str(bound.arguments[param_name])
                if not compiled.match(value):
                    raise ValueError(
                        f"{param_name} 不匹配模式: {pattern}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def timeout(seconds: float):
    """超时装饰器工厂

    用法：
        @timeout(5.0)
        def long_running_task():
            ...
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError(f"{func.__name__} 执行超时 ({seconds}s)")

            # 设置超时信号
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(seconds))

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
            return result
        return wrapper
    return decorator


def memoize(func: Callable[P, R]) -> Callable[P, R]:
    """记忆化装饰器 - 缓存结果

    用法：
        @memoize
        def expensive_computation(x):
            ...
    """
    cache: dict = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper


# ============================================================
# 3. 缓存装饰器
# ============================================================

def rate_limit(calls_per_second: float):
    """速率限制装饰器工厂

    用法：
        @rate_limit(10)  # 每秒最多 10 次调用
        def api_call():
            ...
    """
    min_interval = 1.0 / calls_per_second
    last_call = [0.0]

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            elapsed = time.perf_counter() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.perf_counter()
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================
# 4. 装饰器链组合
# ============================================================

@log_calls_simple
@retry(max_attempts=3, delay=0.1)
@validate(name=str, age=int)
def create_user(name: str, age: int) -> dict:
    """组合多个装饰器"""
    return {"name": name, "age": age, "id": hash(name) % 10000}


@log_calls_simple
@retry(max_attempts=2)
@pattern_match("email", r"^[\w.-]+@[\w.-]+\.\w+$")
def register_email(email: str) -> bool:
    """邮箱注册（带正则验证）"""
    print(f"  注册邮箱: {email}")
    return True


# ============================================================
# 5. 类装饰器
# ============================================================

def singleton(cls: type) -> type:
    """单例模式装饰器"""
    instances: dict = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class DatabaseConnection:
    """单例数据库连接"""
    def __init__(self, host: str = "localhost") -> None:
        self.host = host
        self.connected = True

    def query(self, sql: str) -> list:
        print(f"  执行查询: {sql}")
        return []


# ============================================================
# 6. 装饰器优先级
# ============================================================

def demonstrate_decorator_order():
    """演示装饰器应用顺序

    装饰器从下往上应用：
        @d1
        @d2
        def func():
            ...

    等价于：
        func = d1(d2(func))
    """
    print("\n=== 装饰器应用顺序 ===")

    execution_order: list = []

    def trace(name: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                execution_order.append(f"进入 {name}")
                result = func(*args, **kwargs)
                execution_order.append(f"退出 {name}")
                return result
            return wrapper
        return decorator

    @trace("A")
    @trace("B")
    @trace("C")
    def my_function():
        execution_order.append("执行 my_function")

    my_function()

    print("执行顺序:")
    for step in execution_order:
        print(f"  {step}")
    print("结论: 进入顺序 C→B→A, 退出顺序 A→B→C (栈式)")


# ============================================================
# 演示函数
# ============================================================

def demonstrate_basic_decorators():
    """演示基础装饰器"""
    print("\n=== 基础装饰器 ===")

    @log_calls_simple
    def add(a: int, b: int) -> int:
        return a + b

    result = add(1, 2)
    print(f"结果: {result}")


def demonstrate_retry():
    """演示重试装饰器"""
    print("\n=== 重试装饰器 ===")

    attempts = [0]

    @retry(max_attempts=3, delay=0.1)
    def flaky_function():
        attempts[0] += 1
        if attempts[0] < 3:
            raise ValueError(f"尝试 {attempts[0]} 失败")
        return "成功!"

    result = flaky_function()
    print(f"最终结果: {result}")
    print(f"尝试次数: {attempts[0]}")


def demonstrate_validate():
    """演示验证装饰器"""
    print("\n=== 参数验证装饰器 ===")

    try:
        user = create_user(name="Alice", age=25)
        print(f"创建用户成功: {user}")
    except TypeError as e:
        print(f"验证失败: {e}")

    try:
        user = create_user(name="Bob", age="invalid")  # type: ignore
    except TypeError as e:
        print(f"验证失败: {e}")


def demonstrate_pattern_match():
    """演示正则验证"""
    print("\n=== 正则验证装饰器 ===")

    emails = [
        "alice@example.com",
        "invalid-email",
        "bob@test.co.uk",
    ]

    for email in emails:
        try:
            register_email(email)
            print(f"  ✓ {email} 有效")
        except ValueError as e:
            print(f"  ✗ {email}: {e}")


def demonstrate_memoize():
    """演示记忆化"""
    print("\n=== 记忆化装饰器 ===")

    call_count = [0]

    @memoize
    def fibonacci(n: int) -> int:
        call_count[0] += 1
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    for i in range(1, 8):
        call_count[0] = 0
        result = fibonacci(i)
        print(f"fibonacci({i}) = {result}, 调用次数: {call_count[0]}")


def demonstrate_singleton():
    """演示单例装饰器"""
    print("\n=== 单例装饰器 ===")

    db1 = DatabaseConnection("production")
    db2 = DatabaseConnection("staging")

    print(f"db1.host: {db1.host}")
    print(f"db2.host: {db2.host}")
    print(f"db1 is db2: {db1 is db2}")
    print("结论: 两次实例化返回同一对象")


# ============================================================
# 主函数
# ============================================================

def main() -> None:
    """主函数"""
    print("=" * 60)
    print("P02 示例 3: 装饰器链")
    print("=" * 60)

    demonstrate_decorator_order()
    demonstrate_basic_decorators()
    demonstrate_retry()
    demonstrate_validate()
    demonstrate_pattern_match()
    demonstrate_memoize()
    demonstrate_singleton()

    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
