"""L11: 生成器与迭代器 - 基础示例"""

# === Part 1: 迭代器协议 ===


class Counter:
    """手动实现迭代器协议"""

    def __init__(self, max_val: int) -> None:
        self.max_val = max_val
        self.current = 0

    def __iter__(self) -> "Counter":
        """返回迭代器自身"""
        return self

    def __next__(self) -> int:
        """返回下一个值"""
        if self.current >= self.max_val:
            raise StopIteration
        self.current += 1
        return self.current


# 使用迭代器
counter = Counter(5)
for num in counter:
    print(num, end=" ")
print()  # 1 2 3 4 5

# 手动迭代
counter2 = Counter(3)
iterator = iter(counter2)
print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3

# === Part 2: 生成器函数 ===


def countdown(n: int):
    """倒计时生成器"""
    while n > 0:
        yield n
        n -= 1


for num in countdown(5):
    print(f"倒计时: {num}")

# === Part 3: 生成器表达式 ===

# 列表推导式 vs 生成器表达式
squares_list = [x**2 for x in range(5)]
squares_gen = (x**2 for x in range(5))

print(f"列表: {squares_list}")  # [0, 1, 4, 9, 16]
print(f"生成器: {squares_gen}")  # <generator object>

# 生成器惰性求值
gen = (x**2 for x in range(1000000))
print(f"生成器大小: {gen.__sizeof__()} bytes")  # 很小

# === Part 4: 嵌套循环展开 ===

# 传统写法：显式嵌套循环


def flatten(nested: list[list[int]]) -> list[int]:
    """扁平化嵌套列表（列表版）"""
    result = []
    for sublist in nested:
        for item in sublist:
            result.append(item)
    return result


def flatten_gen(nested: list[list[int]]):
    """扁平化嵌套列表（生成器版 - 使用显式嵌套循环）"""
    for sublist in nested:
        for item in sublist:
            yield item


nested = [[1, 2], [3, 4, 5], [6]]
print(f"列表版: {flatten(nested)}")
print(f"生成器版: {list(flatten_gen(nested))}")

# === Part 5: 生成器状态 ===


def stateful_generator():
    """带状态的生成器"""
    state = 0
    while True:
        state += 1
        yield state
        state *= 2


gen = stateful_generator()
print(next(gen))  # 1
print(next(gen))  # 3 (state=1, then state*=2=2, next yields 3)
print(next(gen))  # 5 (state=2, then state*=2=4, next yields 5)

# === Part 6: 生成器状态交互 ===

# 展示生成器的基本交互模式


def interactive_gen():
    """模拟双向交互的生成器"""
    total = 0
    while True:
        # 每次 yield 当前累加值
        yield total
        # 状态更新
        total += 1


gen = interactive_gen()
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2

# === Part 7: throw() 和 close() ===


def error_prone():
    """可能抛出异常的生成器"""
    try:
        yield 1
        yield 2
        raise ValueError("Test error")
        yield 3
    except ValueError:
        yield "Caught!"


gen = error_prone()
print(next(gen))  # 1
print(next(gen))  # 2
print(gen.throw(ValueError("Injected")))  # Caught!


# close() 示例
def infinite():
    i = 0
    while True:
        yield i
        i += 1


gen = infinite()
print(next(gen))  # 0
print(next(gen))  # 1
gen.close()  # 优雅关闭
try:
    next(gen)
except StopIteration:
    print("Generator closed")

print("\n=== 生成器基础示例完成 ===")
