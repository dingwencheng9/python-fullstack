"""L17: 函数式编程 - 函数组合"""

from functools import wraps, partial, reduce

# === Part 1: compose - 函数组合 ===


def compose(f, g):
    """返回组合函数 f ∘ g"""
    return lambda x: f(g(x))


# 示例
add_one = lambda x: x + 1
double = lambda x: x * 2
square = lambda x: x**2

# double(add_one(5)) = 12
add_then_double = compose(double, add_one)
print(f"add_then_double(5) = {add_then_double(5)}")

# square(double(5)) = 100
double_then_square = compose(square, double)
print(f"double_then_square(5) = {double_then_square(5)}")

# === Part 2: 多函数组合 ===


def compose_all(*functions):
    """组合多个函数（从右到左）"""
    return reduce(compose, functions, lambda x: x)


# 示例：字符串处理 pipeline
strip = lambda s: s.strip()
lower = lambda s: s.lower()
remove_special = lambda s: "".join(c for c in s if c.isalnum() or c == " ")

sanitize = compose_all(lower, strip, remove_special)
text = "  Hello, World!  "
print(f"sanitize('{text}') = '{sanitize(text)}'")

# === Part 3: pipe - 管道（左到右） ===


def pipe(*functions):
    """左到右组合函数"""
    return reduce(lambda f, g: lambda x: g(f(x)), functions, lambda x: x)


# 示例
add = lambda x: x + 1
multiply = lambda x: x * 2
subtract = lambda x: x - 3

pipeline = pipe(add, multiply, subtract)
# pipe(add, multiply, subtract)(5) = subtract(multiply(add(5)))
# = subtract(multiply(6)) = subtract(12) = 9
print(f"pipe(add, multiply, subtract)(5) = {pipeline(5)}")

# === Part 4: 使用 functools.partial ===


def power(base: float, exponent: float) -> float:
    return base**exponent


# 平方：固定 exponent=2
square = partial(power, exponent=2)
print(f"square(5) = {square(5)}")

# 立方：固定 exponent=3
cube = partial(power, exponent=3)
print(f"cube(5) = {cube(5)}")

# 平方根
sqrt = partial(power, exponent=0.5)
print(f"sqrt(16) = {sqrt(16)}")

# === Part 5: partial 应用场景 ===


# 格式化函数
def format_message(template: str, name: str, value: int = 0) -> str:
    return template.format(name=name, value=value)


# 固定模板
greet = partial(format_message, "Hello, {name}!")
report = partial(format_message, "{name} 的得分: {value}")

print(greet(name="Alice"))
print(report(name="Bob", value=95))

# === Part 6: 装饰器组合 ===


def logger(func):
    """日志装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用 {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


def validator(func):
    """验证装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[VALIDATE] 检查参数")
        return func(*args, **kwargs)

    return wrapper


def cache(func):
    """缓存装饰器"""
    cache_store = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache_store:
            cache_store[key] = func(*args, **kwargs)
            print("[CACHE] 缓存新值")
        else:
            print("[CACHE] 使用缓存")
        return cache_store[key]

    return wrapper


# 组合装饰器
@logger
@validator
@cache
def expensive_calc(n: int) -> int:
    print("[CALC] 执行计算...")
    return n**2


print("\n装饰器组合示例:")
expensive_calc(5)
expensive_calc(5)  # 使用缓存
expensive_calc(6)

# === Part 7: 条件函数组合 ===


def conditional(condition, true_fn, false_fn):
    """条件函数"""
    return lambda x: true_fn(x) if condition(x) else false_fn(x)


is_even = lambda x: x % 2 == 0
double_or_triple = conditional(is_even, lambda x: x * 2, lambda x: x * 3)

numbers = [1, 2, 3, 4, 5]
results = [double_or_triple(n) for n in numbers]
print(f"\n条件函数: {numbers} -> {results}")
# 1*3=3, 2*2=4, 3*3=9, 4*2=8, 5*3=15

print("\n=== 函数组合示例完成 ===")
