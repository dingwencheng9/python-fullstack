"""L17: 函数式编程 - itertools 高级用法"""

import itertools

# === Part 1: 组合迭代器 ===

# product - 笛卡尔积
print("product('AB', repeat=2):")
for p in itertools.product("AB", repeat=2):
    print(f"  {p}")

print("\nproduct([1,2], ['a','b']):")
for p in itertools.product([1, 2], ["a", "b"]):
    print(f"  {p}")

# permutations - 排列
print("\npermutations('ABC', 2):")
for p in itertools.permutations("ABC", 2):
    print(f"  {p}")

# combinations - 组合
print("\ncombinations('ABCD', 2):")
for c in itertools.combinations("ABCD", 2):
    print(f"  {c}")

# combinations_with_replacement - 带重复组合
print("\ncombinations_with_replacement('AB', 3):")
for c in itertools.combinations_with_replacement("AB", 3):
    print(f"  {c}")

# === Part 2: groupby 分组 ===

from itertools import groupby

data = [
    ("水果", "苹果"),
    ("水果", "香蕉"),
    ("蔬菜", "胡萝卜"),
    ("蔬菜", "菠菜"),
    ("水果", "橙子"),
]

# 按类别分组
print("\n按类别分组:")
for category, items in groupby(data, key=lambda x: x[0]):
    print(f"  {category}: {list(items)}")

# 排序后分组
data_sorted = sorted(data, key=lambda x: x[0])
print("\n排序后分组:")
for category, items in groupby(data_sorted, key=lambda x: x[0]):
    print(f"  {category}: {list(items)}")

# === Part 3: pairwise (Python 3.10+) ===

numbers = range(5)
print("\npairwise:", list(itertools.pairwise(numbers)))


# 自定义窗口大小
def windowed(iterable, size):
    """滑动窗口"""
    iters = itertools.tee(iterable, size)
    for i, it in enumerate(iters):
        for _ in range(i):
            next(it, None)
    return list(zip(*iters, strict=False))


print(f"windowed(3): {list(windowed(range(7), 3))}")

# === Part 4: zip_longest 填充zip ===

a = [1, 2, 3]
b = ["a", "b"]

# 注意: zip() 默认截断到最短，zip_longest 填充缺失值
print("\nzip:", list(zip(a, b, strict=False)))
print("zip_longest:", list(itertools.zip_longest(a, b, fillvalue="-")))

# === Part 5: count/cycle/repeat ===

print("\ncount(10, 2) 前5个:")
for i, num in enumerate(itertools.count(10, 2)):
    if i >= 5:
        break
    print(f"  {num}")

print("\ncycle('AB') 前6个:")
for i, char in enumerate(itertools.cycle("AB")):
    if i >= 6:
        break
    print(f"  {char}")

print("\nrepeat(5, 3):", list(itertools.repeat(5, 3)))

# === Part 6: islice 切片 ===

numbers = range(20)

print("\nislice(5):", list(itertools.islice(numbers, 5)))
print("islice(5, 10):", list(itertools.islice(numbers, 5, 10)))
print("islice(0, 20, 2):", list(itertools.islice(numbers, 0, 20, 2)))

# === Part 7: filterfalse / compress ===

print("\nfilter(lambda x: x%2, range(10)):", list(filter(lambda x: x % 2, range(10))))
print(
    "filterfalse(lambda x: x%2, range(10)):",
    list(itertools.filterfalse(lambda x: x % 2, range(10))),
)

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
selectors = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
print("compress:", list(itertools.compress(data, selectors)))

# === Part 8: accumulate 高级用法 ===


# 最大运行和
def max_running_sum(arr):
    """最大子数组和（Kadane算法）"""
    max_sum = float("-inf")
    current = 0
    for x in arr:
        current = max(0, current + x)
        max_sum = max(max_sum, current)
    return max_sum


arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f"\n最大子数组和: {max_running_sum(arr)}")

# 运行最大值
nums = [3, 1, 4, 1, 5, 9, 2, 6]
running_max = list(itertools.accumulate(nums, lambda a, b: max(a, b)))  # noqa: PLW0108
print(f"运行最大值: {running_max}")

# === Part 9: 实用工具函数 ===


def chunked(iterable, size):
    """分块"""
    it = iter(iterable)
    while chunk := list(itertools.islice(it, size)):
        yield chunk


data = range(10)
print(f"\nchunked(3): {list(chunked(data, 3))}")


def unique_justseen(iterable, key=None):
    """去除连续重复（保留第一个）"""
    return map(next, map(lambda x: x[1], groupby(iterable, key)))


data = [1, 1, 2, 2, 3, 1, 1]
print(f"unique_justseen: {list(unique_justseen(data))}")

words = ["foo", "Foo", "bar", "Bar", "bar"]
print(f"unique_justseen(lower): {list(unique_justseen(words, key=str.lower))}")

# === Part 10: 组合实现复杂功能 ===


# 找出列表中所有和为指定值的组合
def find_combinations(target: int, numbers: list[int]):
    """找出所有和为 target 的组合"""
    for r in range(1, len(numbers) + 1):
        for combo in itertools.combinations(numbers, r):
            if sum(combo) == target:
                yield combo


nums = [1, 2, 3, 4, 5, 6]
print(f"\n和为7的组合: {list(find_combinations(7, nums))}")


# 所有排列用于穷举
def all_permutations(chars: str, length: int):
    """生成所有指定长度的排列"""
    return itertools.permutations(chars, length)


print(f"\n'abc' 的2位排列: {list(all_permutations('abc', 2))}")

print("\n=== itertools 高级用法示例完成 ===")
