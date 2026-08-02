"""L15: 函数式编程 - 偏函数"""

from functools import partial

# === Part 1: partial 基础 ===


def power(base: float, exponent: float) -> float:
    """幂函数"""
    return base**exponent


# 部分参数绑定
square = partial(power, exponent=2)
cube = partial(power, exponent=3)
sqrt = partial(power, exponent=0.5)

print(f"square(5) = {square(5)}")
print(f"cube(2) = {cube(2)}")
print(f"sqrt(16) = {sqrt(16)}")

# === Part 2: 位置参数绑定 ===


def greet(greeting: str, name: str, punctuation: str) -> str:
    """格式化问候"""
    return f"{greeting}, {name}{punctuation}"


# 固定第一个参数
formal_greet = partial(greet, "Hello")
# 固定前两个参数
casual_greet = partial(greet, "Hey", "there")

print(formal_greet("Alice", "!"))
print(casual_greet("!"))
print(casual_greet(", how are you?"))

# === Part 3: 关键字参数绑定 ===


def configure(host: str, port: int, ssl: bool = False, timeout: int = 30) -> dict:
    """配置连接参数"""
    return {
        "host": host,
        "port": port,
        "ssl": ssl,
        "timeout": timeout,
    }


# 生产环境配置
prod_config = partial(configure, ssl=True, timeout=60)
# 开发环境配置
dev_config = partial(configure, "localhost")

print(f"\n生产配置: {prod_config('api.example.com', 443)}")
print(f"开发配置: {dev_config(3306)}")

# === Part 4: 数据处理偏函数 ===


def filter_data(data: list, condition, transform):
    """数据处理"""
    return [transform(x) for x in data if condition(x)]


# 固定处理函数
process_numbers = partial(filter_data, condition=lambda x: x > 0, transform=lambda x: x**2)

numbers = [-2, -1, 0, 1, 2, 3, 4, 5]
print(f"\n正数平方: {process_numbers(numbers)}")

# 固定条件
filter_positive = partial(filter_data, condition=lambda x: x > 0)
print(f"正数: {filter_positive(numbers, transform=lambda x: x)}")

# === Part 5: 回调模式 ===


def on_result(callback, success, data):
    """结果回调"""
    if success:
        return callback(data)
    return None


# 固定成功处理
handle_success = partial(on_result, success=True)


def format_result(data: dict) -> str:
    return f"{data['name']}: {data['value']}"


process = partial(handle_success, callback=format_result)

result = process(data={"name": "Score", "value": 95})
print(f"\n处理结果: {result}")

# === Part 6: 偏函数链 ===


def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b


def subtract(a: int, b: int) -> int:
    return a - b


# 创建操作函数
add_5 = partial(add, 5)
multiply_3 = partial(multiply, 3)
subtract_2 = partial(subtract, b=2)

# 链式调用
# (x + 5) * 3 - 2
result = subtract_2(multiply_3(add_5(10)))
print(f"\n链式偏函数: (10 + 5) * 3 - 2 = {result}")

# === Part 7: 类方法偏函数 ===


class StringProcessor:
    def __init__(self):
        self.data: list[str] = []

    def process(self, text: str, upper: bool = False, strip: bool = True) -> str:
        if strip:
            text = text.strip()
        if upper:
            text = text.upper()
        return text


processor = StringProcessor()

# 固定参数
upper_process = partial(processor.process, upper=True)
strip_process = partial(processor.process, strip=True)
clean_upper = partial(processor.process, upper=True, strip=True)

text = "  Hello, World!  "
print(f"\n原文: '{text}'")
print(f"大写: '{upper_process(text, strip=False)}'")
print(f"去空格: '{strip_process(text, upper=False)}'")
print(f"清理+大写: '{clean_upper(text)}'")

print("\n=== 偏函数示例完成 ===")
