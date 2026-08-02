"""L15: 函数式编程 - 生成器与函数式"""

import itertools

# === Part 1: 生成器表达式（惰性求值）===

numbers = [1, 2, 3, 4, 5]

# 列表推导式：立即计算
squares_list = [x**2 for x in numbers]
print(f"列表推导式: {squares_list}")

# 生成器表达式：惰性计算
squares_gen = (x**2 for x in numbers)
print(f"生成器表达式: {squares_gen}")  # <generator object>

# 惰性求值优势
import sys

big_range = range(10_000_000)
list_size = sys.getsizeof([x for x in big_range])  # noqa: C416 (教学演示：展示列表与生成器的内存差异)
gen_size = sys.getsizeof(x for x in big_range)
print(f"\n列表大小: {list_size} bytes")
print(f"生成器大小: {gen_size} bytes")

# === Part 2: 生成器管道 ===


def read_numbers():
    """模拟数据源"""
    yield from [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]


def filter_odds(numbers):
    """过滤奇数"""
    yield from (n for n in numbers if n % 2 == 0)


def square(numbers):
    """平方"""
    yield from (n**2 for n in numbers)


def running_sum(numbers):
    """累加"""
    total = 0
    for n in numbers:
        total += n
        yield total


# 链式处理
result = list(running_sum(square(filter_odds(read_numbers()))))
print(f"\n生成器管道: {result}")

# === Part 3: itertools 函数式工具 ===

# takewhile - 取满足条件的连续元素
numbers = [1, 2, 3, 10, 20, 30]
small = list(itertools.takewhile(lambda x: x < 10, numbers))
print(f"\ntakewhile(<10): {small}")

# dropwhile - 跳过满足条件的连续元素
large = list(itertools.dropwhile(lambda x: x < 10, numbers))
print(f"dropwhile(<10): {large}")

# compress - 按选择器筛选
data = ["a", "b", "c", "d", "e"]
selectors = [1, 0, 1, 0, 1]
filtered = list(itertools.compress(data, selectors))
print(f"compress: {filtered}")

# === Part 4: accumulate 累加器 ===

from operator import mul

# 累加
nums = [1, 2, 3, 4, 5]
print(f"\naccumulate: {list(itertools.accumulate(nums))}")
print(f"accumulate(mul): {list(itertools.accumulate(nums, mul))}")


# 找出最大运行和
def max_subarray_sum(arr):
    """找出最大子数组和（动态规划）"""

    def max_sum(acc, x):
        current_max = max(acc[1] + x, x)
        return (max(acc[0], current_max), current_max)

    best, _ = list(itertools.accumulate(arr, max_sum, initial=(float("-inf"), 0)))[-1]
    return best


arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f"最大子数组和: {max_subarray_sum(arr)}")

# === Part 5: 无限迭代器与生成器 ===


def fibonacci():
    """无限菲波那契生成器"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# 取前20个
first_20 = list(itertools.islice(fibonacci(), 20))
print(f"\n前20个斐波那契数: {first_20}")


# 找出第一个大于1000的
def first_where(predicate, iterable):
    """找出第一个满足条件的元素"""
    return next(x for x in iterable if predicate(x))


fib_over_1000 = first_where(lambda x: x > 1000, fibonacci())
print(f"第一个大于1000的斐波那契数: {fib_over_1000}")

# === Part 6: 分组与归约 ===

from itertools import groupby

# 按长度分组
words = ["apple", "ant", "banana", "bat", "cat", "car"]
sorted_words = sorted(words, key=len)
groups = {k: list(v) for k, v in groupby(sorted_words, key=len)}
print(f"\n按长度分组: {groups}")

# === Part 7: 生成器 vs 列表的内存效率 ===


def process_large_data(limit: int):
    """处理大数据"""

    def data_generator():
        for i in range(limit):
            yield i * 2

    return data_generator


# 使用生成器处理大数据集
gen = process_large_data(1000000)()
count = sum(1 for _ in gen)
print(f"\n处理了 {count} 个元素（生成器）")

# === Part 8: 惰性链式操作 ===


class LazyList:
    """惰性列表"""

    def __init__(self, source):
        self._source = source
        self._pipeline = []

    def map(self, func):
        self._pipeline.append(("map", func))
        return self

    def filter(self, pred):
        self._pipeline.append(("filter", pred))
        return self

    def __iter__(self):
        iterator = iter(self._source)
        for op, func in self._pipeline:
            iterator = map(func, iterator) if op == "map" else filter(func, iterator)
        return iter(iterator)

    def __len__(self):
        return sum(1 for _ in self)


# 使用惰性列表
data = LazyList(range(1000))
result = data.map(lambda x: x * 2).filter(lambda x: x % 3 == 0).filter(lambda x: x > 100)
count = sum(1 for _ in result)
print(f"\n惰性列表处理: {count} 个元素满足条件")

print("\n=== 生成器与函数式示例完成 ===")
