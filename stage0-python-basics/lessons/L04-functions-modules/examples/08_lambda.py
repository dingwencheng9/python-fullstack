"""L04 示例8: lambda 表达式

演示 lambda 匿名函数的典型用途。
适合需要简短函数的场景，如 sorted()、map()、filter() 等。
"""

# ============ lambda 基础 ============

# 完整函数定义
def square_def(x: int) -> int:
    return x * x


# ✅ 教学演示：lambda 赋值（实际项目中推荐用 def）
square_lambda = lambda x: x * x  # noqa: E731

print("=== lambda 基础 ===")
print(f"square_def(5) = {square_def(5)}")
print(f"square_lambda(5) = {square_lambda(5)}")


# ============ lambda 配合 sorted ============

print("\n=== lambda 配合 sorted ===")

numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"原始列表: {numbers}")
print(f"默认排序: {sorted(numbers)}")

# 按绝对值排序
mixed = [-5, 3, -1, 2, -4]
print(f"\n混合数: {mixed}")
print(f"按绝对值排序: {sorted(mixed, key=lambda x: abs(x))}")

# 按字符串长度排序
words = ["apple", "hi", "banana", "a", "cherry"]
print(f"\n单词: {words}")
print(f"按长度排序: {sorted(words, key=lambda s: len(s))}")


# ============ lambda 配合 map ============

print("\n=== lambda 配合 map ===")

numbers = [1, 2, 3, 4, 5]

# 转换每个元素
doubled = list(map(lambda x: x * 2, numbers))
print(f"原列表: {numbers}")
print(f"翻倍: {doubled}")

# 转换为字符串
str_nums = list(map(lambda x: str(x), numbers))
print(f"转字符串: {str_nums}")


# ============ lambda 配合 filter ============

print("\n=== lambda 配合 filter ===")

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 筛选偶数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"原列表: {numbers}")
print(f"偶数: {evens}")

# 筛选大于 5 的数
gt_five = list(filter(lambda x: x > 5, numbers))
print(f"大于5: {gt_five}")


# ============ lambda 限制 ============

print("\n=== lambda 限制 ===")

# ✅ 教学演示：lambda 条件表达式和参数
abs_val = lambda x: x if x >= 0 else -x  # noqa: E731
add = lambda x, y: x + y  # noqa: E731
print(f"abs_val(-5) = {abs_val(-5)}")
print(f"add(3, 4) = {add(3, 4)}")

# ❌ 错误：lambda 不能包含 if/while/for 语句（只能是表达式）
# 下面这种写法是错误的：
# lambda x: if x > 0: return x  # 语法错误！


# ============ 实际使用场景 ============

print("\n=== 实际使用场景 ===")

# 场景1：按字典的某个字段排序
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
]

# 按年龄排序
sorted_users = sorted(users, key=lambda u: u["age"])
print("按年龄排序:")
for u in sorted_users:
    print(f"  {u['name']}: {u['age']}")

# 场景2：数据转换
prices = [100, 200, 300]
# 计算折后价（打9折）
discounted = list(map(lambda p: p * 0.9, prices))
print(f"\n原价: {prices}")
print(f"9折: {discounted}")


if __name__ == "__main__":
    print("\n=== lambda 总结 ===")
    print("lambda 适合场景:")
    print("  - sorted(key=lambda ...)")
    print("  - map(lambda ...)")
    print("  - filter(lambda ...)")
    print("\n避免场景:")
    print("  - 复杂逻辑（用 def）")
    print("  - 多行代码（用 def）")
    print("  - 需要多次复用的函数（用 def）")
