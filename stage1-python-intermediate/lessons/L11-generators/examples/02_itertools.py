"""L11: 生成器与迭代器 - itertools 示例"""

import itertools

# === Part 1: 无限迭代器 ===

# count - 无限计数
print("count(10):")
for i, num in enumerate(itertools.count(10)):
    if i >= 5:
        break
    print(num, end=" ")
print()  # 10 11 12 13 14

# cycle - 无限循环
print("\ncycle('ABC'):")
for i, char in enumerate(itertools.cycle("ABC")):
    if i >= 7:
        break
    print(char, end=" ")
print()  # A B C A B C A

# repeat - 重复值
print("\nrepeat(5, 3):")
for num in itertools.repeat(5, 3):
    print(num, end=" ")
print()  # 5 5 5

# === Part 2: 有限迭代器 ===

# accumulate - 累加
numbers = [1, 2, 3, 4, 5]
print("\naccumulate:", list(itertools.accumulate(numbers)))  # [1, 3, 6, 10, 15]
print("accumulate with mul:", list(itertools.accumulate(numbers, lambda a, b: a * b)))  # [1, 2, 6, 24, 120]

# chain - 连接多个可迭代对象
print("\nchain:", list(itertools.chain([1, 2], [3, 4], [5])))

# chain.from_iterable - 扁平化
nested = [[1, 2], [3, 4], [5]]
print("chain.from_iterable:", list(itertools.chain.from_iterable(nested)))

# compress - 按选择器筛选
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
selectors = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
print("compress:", list(itertools.compress(data, selectors)))  # [1, 3, 5, 7, 9]

# dropwhile / takewhile
print("\ndropwhile(<3):", list(itertools.dropwhile(lambda x: x < 3, numbers)))
print("takewhile(<3):", list(itertools.takewhile(lambda x: x < 3, numbers)))

# filterfalse - 保留不满足条件的
print("filterfalse(odd):", list(itertools.filterfalse(lambda x: x % 2, numbers)))  # [2, 4]

# islice - 切片
print("islice(2, 7, 2):", list(itertools.islice(numbers, 2, 7, 2)))  # [3, 5, 7]

# === Part 3: 组合迭代器 ===

# product - 笛卡尔积
print("\nproduct('AB', repeat=2):", list(itertools.product("AB", repeat=2)))  # [('A','A'), ('A','B'), ('B','A'), ('B','B')]
print("product([1,2], ['a','b']):", list(itertools.product([1, 2], ["a", "b"])))

# permutations - 排列
print("\npermutations('ABC', 2):")
for p in itertools.permutations("ABC", 2):
    print(p, end=" ")
print()

# combinations - 组合
print("\ncombinations('ABCD', 2):")
for c in itertools.combinations("ABCD", 2):
    print(c, end=" ")
print()

# combinations_with_replacement - 带重复组合
print("\ncombinations_with_replacement('AB', 2):")
for c in itertools.combinations_with_replacement("AB", 2):
    print(c, end=" ")
print()

# === Part 4: 实用工具函数 ===

# groupby - 分组
data = [("a", 1), ("a", 2), ("b", 1), ("b", 3), ("c", 5)]
print("\ngroupby:")
for key, group in itertools.groupby(data, lambda x: x[0]):
    print(f"  {key}: {list(group)}")

# pairwise (Python 3.10+)
print("\npairwise:", list(itertools.pairwise(range(5))))  # [(0,1), (1,2), (2,3), (3,4)]

# zip_longest - 填充zip
a = [1, 2, 3]
b = ["a", "b"]
print("\nzip_longest:", list(itertools.zip_longest(a, b, fillvalue="-")))
# [(1,'a'), (2,'b'), (3,'-')]

# === Part 5: 组合使用 ===


# 生成菲波那契数列前20项
def fibonacci():
    """无限菲波那契生成器"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print("\n菲波那契数列前15项:")
for i, fib in enumerate(itertools.islice(fibonacci(), 15)):
    print(fib, end=" ")
print()


# 生成杨辉三角
def pascal_triangle():
    """杨辉三角"""
    row = [1]
    while True:
        yield row
        row = [x + y for x, y in zip([0] + row, row + [0], strict=True)]


print("\n杨辉三角前8行:")
for i, row in enumerate(itertools.islice(pascal_triangle(), 8)):
    print("  " * (7 - i) + " ".join([str(x) for x in row]))


# 寻找第一个满足条件的元素
def first(predicate, iterable):
    """找到第一个满足条件的元素"""
    return next(itertools.filterfalse(lambda x: not predicate(x), iterable))


numbers = range(100)
result = first(lambda x: x % 17 == 0 and x % 23 == 0, numbers)
print(f"\n第一个能被17和23整除的数: {result}")

print("\n=== itertools 示例完成 ===")
