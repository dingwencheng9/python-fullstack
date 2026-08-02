"""L10: 类型系统 - Callable 类型与泛型 Callable"""

from collections.abc import Callable
from typing import TypeVar

# === Part 1: Callable 类型签名 ===


# 基本 Callable 类型
def apply_func(func: Callable[[int, int], int], a: int, b: int) -> int:
    """应用二元函数"""
    return func(a, b)


def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b


print(apply_func(add, 3, 4))  # 7
print(apply_func(multiply, 3, 4))  # 12


# 无参数的 Callable
def on_ready(callback: Callable[[], None]) -> None:
    """模拟就绪回调"""
    print("Ready!")
    callback()


def say_hello() -> None:
    print("Hello!")


on_ready(say_hello)

# === Part 2: 泛型 Callable ===

T = TypeVar("T")
U = TypeVar("U")


def transform_list(items: list[T], func: Callable[[T], U]) -> list[U]:
    """使用函数转换列表"""
    return [func(item) for item in items]


numbers = [1, 2, 3, 4, 5]
print(transform_list(numbers, str))  # ['1', '2', '3', '4', '5']
print(transform_list(numbers, lambda x: x * 2))  # [2, 4, 6, 8, 10]


# 泛型回调
def execute_with_retry[T](func: Callable[[], T], max_retries: int = 3) -> T:
    """带重试的执行"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed, retrying...")
    raise RuntimeError("Should not reach here")


# 测试
counter = [0]


def might_fail() -> str:
    counter[0] += 1
    if counter[0] < 3:
        raise ValueError("Not ready yet")
    return "Success!"


print(execute_with_retry(might_fail))  # Success!

# === Part 3: 可变参数 Callable ===


def log_calls(func: Callable[..., int]) -> Callable[..., int]:
    """记录调用的装饰器"""

    def wrapper(*args, **kwargs) -> int:
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result

    return wrapper


@log_calls
def complex_calc(a: int, b: int, factor: int = 1) -> int:
    return (a + b) * factor


print(complex_calc(3, 4))
print(complex_calc(3, 4, factor=2))

# === Part 4: 回调模式 ===

from typing import Protocol


class AsyncCallback(Protocol[T]):
    """异步回调协议"""

    def __call__(self, result: T | None, error: Exception | None) -> None: ...


def async_fetch(url: str, on_complete: AsyncCallback[bytes]) -> None:
    """模拟异步获取"""
    import time

    time.sleep(0.1)  # 模拟网络延迟
    try:
        if "error" in url:
            raise ConnectionError("Network error")
        # 模拟成功
        on_complete(b"fake data", None)
    except Exception as e:
        on_complete(None, e)


def handle_response(result: bytes | None, error: Exception | None) -> None:
    if error:
        print(f"Error: {error}")
    else:
        print(f"Got {len(result)} bytes")


async_fetch("https://example.com", handle_response)
async_fetch("https://error.example", handle_response)

# === Part 5: 工厂函数模式 ===


def create_adder(n: int) -> Callable[[int], int]:
    """创建加法器"""

    def adder(x: int) -> int:
        return x + n

    return adder


add_5 = create_adder(5)
add_10 = create_adder(10)

print(add_5(3))  # 8
print(add_10(3))  # 13


# 使用泛型 Callable 类型
def compose[T, U, V](f: Callable[[T], U], g: Callable[[U], V]) -> Callable[[T], V]:
    """组合两个函数"""

    def composed(x: T) -> V:
        return g(f(x))

    return composed


def double(x: int) -> int:
    return x * 2


def to_str(x: int) -> str:
    return str(x)


double_then_str = compose(double, to_str)
print(double_then_str(5))  # "10"

print("\n=== Callable 类型示例完成 ===")
