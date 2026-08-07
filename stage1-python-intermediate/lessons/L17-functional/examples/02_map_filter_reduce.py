"""L17: 函数式编程 - map, filter, reduce"""

from functools import reduce
from operator import add, mul

# === Part 1: map - 转换 ===

numbers = [1, 2, 3, 4, 5]

# 使用 map + lambda
squared = list(map(lambda x: x**2, numbers))
print(f"平方: {squared}")


# 使用 map + 普通函数
def to_upper(s: str) -> str:
    return s.upper()


names = ["alice", "bob", "charlie"]
upper_names = list(map(to_upper, names))
print(f"大写: {upper_names}")

# 多个可迭代对象
a = [1, 2, 3]
b = [4, 5, 6]
sums = list(map(lambda x, y: x + y, a, b))
print(f"对应相加: {sums}")

# === Part 2: filter - 过滤 ===

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 保留偶数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数: {evens}")

# 保留长度大于 3 的字符串
words = ["cat", "elephant", "dog", "hippopotamus"]
long_words = list(filter(lambda w: len(w) > 3, words))
print(f"长词: {long_words}")

# 保留正数
mixed = [-2, -1, 0, 1, 2, 3]
positives = list(filter(lambda x: x > 0, mixed))
print(f"正数: {positives}")

# === Part 3: reduce - 聚合 ===

numbers = [1, 2, 3, 4, 5]

# 求和
total = reduce(lambda acc, x: acc + x, numbers, 0)
print(f"求和: {total}")

# 求积
product = reduce(lambda acc, x: acc * x, numbers, 1)
print(f"求积: {product}")

# 找最大值
max_val = reduce(lambda acc, x: acc if acc > x else x, numbers)
print(f"最大值: {max_val}")

# 连接字符串
words = ["Hello", " ", "World", "!"]
sentence = reduce(lambda acc, w: acc + w, words, "")
print(f"连接: {sentence}")

# === Part 4: 使用 operator 模块 ===

# 更高效的写法
total = reduce(add, numbers, 0)
product = reduce(mul, numbers, 1)
print(f"\n使用 operator: sum={total}, product={product}")

# === Part 5: 组合使用 ===

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 找出偶数的平方和
result = reduce(lambda acc, x: acc + x**2, filter(lambda x: x % 2 == 0, numbers), 0)
print(f"\n偶数平方和: {result}")

# 等价的命令式写法
total = 0
for n in numbers:
    if n % 2 == 0:
        total += n**2
print(f"命令式验证: {total}")

# === Part 6: 链式调用 ===


# 字符串处理 pipeline
strip = lambda s: s.strip()
lower = lambda s: s.lower()
remove_special = lambda s: "".join(c for c in s if c.isalnum() or c == " ")

text = "  Hello, World!  "
sanitized = lower(strip(remove_special(text)))
print(f"\n清理后: '{sanitized}'")

# 使用 reduce 组合
from functools import reduce


def compose(*functions):
    """函数组合"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


sanitize = compose(lower, strip, remove_special)
print(f"组合后: '{sanitize(text)}'")

# === Part 7: 列表推导式 vs map/filter ===

numbers = [1, 2, 3, 4, 5]

# 列表推导式
squares = [x**2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]
even_squares = [x**2 for x in numbers if x % 2 == 0]

# map/filter
squares_mf = list(map(lambda x: x**2, numbers))
evens_mf = list(filter(lambda x: x % 2 == 0, numbers))
even_squares_mf = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))

print(f"\n列表推导式: squares={squares}, evens={evens}, even_squares={even_squares}")
print(f"map/filter:  squares={squares_mf}, evens={evens_mf}, even_squares={even_squares_mf}")

print("\n=== map/filter/reduce 示例完成 ===")
