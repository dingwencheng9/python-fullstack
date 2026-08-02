"""L15: 函数式编程 - 柯里化"""

from functools import wraps

# === Part 1: 基础柯里化 ===


# 普通函数
def add(x: int, y: int, z: int) -> int:
    return x + y + z


print(f"普通调用: add(1, 2, 3) = {add(1, 2, 3)}")


# 柯里化版本
def curried_add(x: int):
    def inner(y: int):
        def innermost(z: int) -> int:
            return x + y + z

        return innermost

    return inner


print(f"柯里化调用: curried_add(1)(2)(3) = {curried_add(1)(2)(3)}")

# === Part 2: 使用 lambda 实现柯里化 ===

curried_mul = lambda x: lambda y: lambda z: x * y * z

double = curried_mul(2)(1)
triple = curried_mul(3)(1)
quadruple = curried_mul(4)(1)

print(f"\ndouble(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")
print(f"quadruple(5) = {quadruple(5)}")
print(f"double(triple(5)) = {double(triple(5))}")

# === Part 3: 自动柯里化装饰器 ===


def curry(func):
    """自动柯里化装饰器。"""
    arity = func.__code__.co_argcount

    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) + len(kwargs) >= arity:
            return func(*args, **kwargs)

        def collect_more(*more_args, **more_kwargs):
            return wrapper(*(args + more_args), **{**kwargs, **more_kwargs})

        return collect_more

    return wrapper


@curry
def add_three(a: int, b: int, c: int) -> int:
    return a + b + c


@curry
def power(base: float, exponent: float) -> float:
    return base**exponent


print("\n自动柯里化:")
print(f"add_three(1)(2)(3) = {add_three(1)(2)(3)}")
print(f"add_three(1, 2)(3) = {add_three(1, 2)(3)}")
print(f"add_three(1)(2, 3) = {add_three(1)(2, 3)}")
print(f"add_three(1, 2, 3) = {add_three(1, 2, 3)}")

print(f"\npower(2)(8) = {power(2)(8)}")
print(f"power(2, 8) = {power(2, 8)}")

# === Part 4: 柯里化应用场景 ===

from functools import partial


# URL 构建器
def build_url(scheme: str, host: str, path: str, query: str = "") -> str:
    url = f"{scheme}://{host}{path}"
    if query:
        url += f"?{query}"
    return url


# 创建特定网站的 URL 构建器
make_github_url = partial(build_url, "https", "github.com")
make_api_url = partial(build_url, "https", "api.example.com")

# 创建特定路径的构建器
user_profile = partial(make_api_url, path="/users")
user_posts = partial(make_api_url, path="/posts")

print("\nURL 构建器:")
print(f"GitHub: {make_github_url('/user/repo')}")
print(f"API: {user_profile(query='id=123&format=json')}")
print(f"Posts: {user_posts(query='id=456')}")

# === Part 5: 柯里化与函数组合 ===


def compose(f, g):
    """函数组合"""
    return lambda x: f(g(x))


def curry2(func):
    """二元函数柯里化"""

    @wraps(func)
    def wrapper(x):
        def inner(y):
            return func(x, y)

        return inner

    return wrapper


@curry2
def divide(x: float, y: float) -> float:
    return x / y


half = divide(2)  # divide(2, y)
reciprocal = divide(1)  # divide(1, y)

print("\n柯里化除法:")
print(f"half(10) = {half(10)}")
print(f"reciprocal(5) = {reciprocal(5)}")
print(f"half(reciprocal(8)) = {half(reciprocal(8))}")

# === Part 6: 多参数柯里化 ===

from typing import TypeVar
from collections.abc import Callable

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


def curry_n(func: Callable) -> Callable:
    """通用柯里化函数。"""
    arity = func.__code__.co_argcount

    def curried(*args):
        if len(args) >= arity:
            return func(*args)

        def next_arg(*more_args):
            return curried(*(args + more_args))

        return next_arg

    return curried


@curry_n
def add_four(a: int, b: int, c: int, d: int) -> int:
    return a + b + c + d


print("\n通用柯里化:")
print(f"add_four(1)(2)(3)(4) = {add_four(1)(2)(3)(4)}")
print(f"add_four(1, 2)(3, 4) = {add_four(1, 2)(3, 4)}")
print(f"add_four(1, 2, 3)(4) = {add_four(1, 2, 3)(4)}")

print("\n=== 柯里化示例完成 ===")
