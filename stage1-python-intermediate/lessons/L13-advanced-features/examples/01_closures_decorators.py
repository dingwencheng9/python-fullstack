"""L13: 进阶特性 - 闭包与装饰器"""

from functools import wraps

# === Part 1: 闭包基础 ===


def outer(x: int):
    """外层函数"""

    def inner(y: int) -> int:
        # inner 可以访问 outer 的变量 x
        return x + y

    return inner


add_5 = outer(5)
print(f"add_5(3) = {add_5(3)}")  # 8
print(f"add_5(10) = {add_5(10)}")  # 15

# === Part 2: nonlocal 关键字 ===


def counter():
    """计数器闭包"""
    count = 0

    def increment(delta: int = 1) -> int:
        nonlocal count  # 声明 count 不是局部变量
        count += delta
        return count

    return increment


cnt = counter()
print(f"计数器: {cnt()}")  # 1
print(f"计数器: {cnt()}")  # 2
print(f"计数器: {cnt(5)}")  # 7

# === Part 3: 装饰器基础 ===


def simple_decorator(func):
    """简单装饰器"""

    @wraps(func)  # 保留原函数元数据
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__} 前")
        result = func(*args, **kwargs)
        print(f"调用 {func.__name__} 后")
        return result

    return wrapper


@simple_decorator
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"


print(greet("Alice"))

# === Part 4: 带参数的装饰器 ===


def repeat(times: int):
    """重复调用的装饰器工厂"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results

        return wrapper

    return decorator


@repeat(3)
def say_hello():
    return "Hello!"


print(say_hello())  # ['Hello!', 'Hello!', 'Hello!']

# === Part 5: 装饰器栈 ===


def debug(func):
    """调试装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"DEBUG: 调用 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"DEBUG: {func.__name__} 返回 {result}")
        return result

    return wrapper


def validate_args(func):
    """参数验证装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if args and args[0] < 0:
            raise ValueError("第一个参数不能为负数")
        return func(*args, **kwargs)

    return wrapper


@debug
@validate_args
def safe_divide(a: float, b: float) -> float:
    """安全除法"""
    return a / b


print(safe_divide(10, 2))
# DEBUG: 调用 safe_divide
# DEBUG: safe_divide 返回 5.0

# === Part 6: 装饰器参数传递 ===


def log_with(level: str):
    """带日志级别的装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level.upper()}] {func.__name__} 被调用")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@log_with("INFO")
def process_data(data: str) -> str:
    return data.upper()


@log_with("WARNING")
def risky_operation(x: int) -> int:
    if x > 100:
        raise ValueError("值太大")
    return x * 2


print(process_data("hello"))
print(risky_operation(50))

print("\n=== 闭包与装饰器示例完成 ===")
