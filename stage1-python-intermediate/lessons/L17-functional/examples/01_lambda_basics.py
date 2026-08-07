"""L17: 函数式编程 - lambda 表达式基础"""

# === Part 1: lambda 基础 ===

# 语法: lambda 参数: 表达式
square = lambda x: x**2
add = lambda x, y: x + y
greet = lambda name: f"Hello, {name}!"

print(f"平方: {square(5)}")  # 25
print(f"加法: {add(3, 4)}")  # 7
print(f"问候: {greet('Alice')}")  # Hello, Alice!

# === Part 2: lambda 与高阶函数 ===

numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# sorted 默认升序
print(f"升序: {sorted(numbers)}")

# 使用 lambda 自定义排序
print(f"降序: {sorted(numbers, key=lambda x: -x)}")

# 按字符串长度排序
words = ["apple", "pie", "banana", "cat"]
print(f"按长度: {sorted(words, key=lambda w: len(w))}")  # noqa: PLW0108

# max 使用 key
people = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35}]
oldest = max(people, key=lambda p: p["age"])
print(f"最年长: {oldest['name']} ({oldest['age']}岁)")

# === Part 3: lambda 限制 ===

# lambda 只能包含单个表达式
# 条件表达式
abs_val = lambda x: x if x >= 0 else -x
print(f"绝对值: {abs_val(-5)}")


# 多操作需要用函数
def complex_operation(x: int) -> int:
    """复杂操作用普通函数"""
    temp = x * 2
    return temp + 10


# === Part 4: 闭包与 lambda ===


def make_multiplier(n: int):
    """工厂函数"""
    return lambda x: x * n


double = make_multiplier(2)
triple = make_multiplier(3)
print(f"double(10) = {double(10)}")
print(f"triple(10) = {triple(10)}")

# === Part 5: lambda 作为返回值 ===


def classifier(threshold: int):
    """返回分类器"""
    return lambda x: "大" if x >= threshold else "小"


big_small = classifier(50)
print(f"30 -> {big_small(30)}")
print(f"100 -> {big_small(100)}")

# === Part 6: lambda 在数据结构中的应用 ===

from dataclasses import dataclass


@dataclass
class Item:
    name: str
    price: float
    quantity: int

    def total(self) -> float:
        return self.price * self.quantity


items = [
    Item("苹果", 3.5, 10),
    Item("香蕉", 2.0, 5),
    Item("橙子", 4.0, 8),
]

# 按总价排序
sorted_items = sorted(items, key=lambda item: item.total())
print("按总价排序:")
for item in sorted_items:
    print(f"  {item.name}: ¥{item.total():.2f}")

# 计算总价
total = sum(map(lambda item: item.total(), items))
print(f"总计: ¥{total:.2f}")

print("\n=== lambda 基础示例完成 ===")
