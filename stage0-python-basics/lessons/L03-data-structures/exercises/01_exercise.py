"""L03 练习1: 数据处理

难度: ⭐☆☆ (入门)
预计时间: 15 分钟
知识点: 列表推导式、字典操作、字符串处理

学习方式:
本练习是"演示型练习"——代码已经完整实现，
你需要运行它，观察输出，理解代码的工作原理。

任务描述:
练习数据筛选和统计，综合运用：
- 列表推导式
- 字典操作
- 字符串处理

提示:
1. 筛选正数: 使用列表推导式 [x for x in nums if x > 0]
2. 词频统计: 使用 split() 分词，用字典统计频次
3. 注意边界情况（空列表、空字符串）
"""

# ============================================================
# 演示：筛选正数
# ============================================================
print("=== 筛选正数演示 ===\n")

test_cases = [
    ([1, -2, 3, -4, 5], [1, 3, 5]),
    ([], []),
    ([-1, -2, -3], []),
    ([0, 1, 2], [1, 2]),
]

for nums, expected in test_cases:
    # 使用列表推导式筛选正数
    result = [x for x in nums if x > 0]
    status = '✓' if result == expected else '✗'
    print(f"{status} [x for x in {nums} if x > 0] = {result}")

# ============================================================
# 演示：词频统计
# ============================================================
print("\n=== 词频统计演示 ===\n")

text_tests = [
    'hello world hello',
    '',
    'python',
    'one two three one two',
]

for text in text_tests:
    # 使用字典统计词频
    word_freq: dict = {}
    for word in text.split():
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    print(f"  '{text}' → {word_freq}")

# ============================================================
# 演示：列表推导式的高级用法
# ============================================================
print("\n=== 列表推导式高级用法演示 ===\n")

# 带条件判断
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = [x * 2 for x in numbers if x % 2 == 0]
print(f"偶数翻倍: {result}")

# 嵌套列表扁平化
nested = [[1, 2, 3], [4, 5], [6]]
flat = [item for sublist in nested for item in sublist]
print(f"扁平化: {flat}")

# 字典推导式
words = ['apple', 'banana', 'cherry', 'date']
word_lengths = {word: len(word) for word in words}
print(f"单词长度: {word_lengths}")

# ============================================================
# 思考题
# ============================================================
print("\n=== 思考题 ===")
print("1. [x for x in nums if x > 0] 和 [x for x in nums if x >= 1] 有什么区别？")
print("2. 如何用列表推导式实现矩阵转置？")
print("3. 字典推导式和列表推导式的主要区别是什么？")
