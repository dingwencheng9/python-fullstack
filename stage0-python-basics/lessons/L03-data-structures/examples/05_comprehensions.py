"""L03 示例5: 推导式与生成器表达式

学习目标:
- 掌握列表推导式、字典推导式、集合推导式
- 理解生成器表达式的惰性求值特性

【知识点边界】本文件仅使用 L01 + L02 + L03 的知识点：
- print, for, range, if
- list, dict, set, tuple
- 列表推导式、字典推导式、集合推导式、生成器表达式
"""

# ============================================================
# 1. 列表推导式
# ============================================================
print("=" * 50)
print("1. 列表推导式")
print("=" * 50)

# 基础列表推导式
squares = [x**2 for x in range(10)]
print(f"平方数列表: {squares}")

# 带条件过滤的推导式
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(f"偶数的平方: {even_squares}")

# 嵌套推导式：展平矩阵
matrix = [[1, 2], [3, 4], [5, 6]]
flattened = [num for row in matrix for num in row]
print(f"原矩阵: {matrix}")
print(f"展平后: {flattened}")

# 字符串处理
words = ["hello", "world", "python"]
upper_words = [word.upper() for word in words]
print(f"原字符串列表: {words}")
print(f"转大写后: {upper_words}")

# ============================================================
# 2. 字典推导式
# ============================================================
print("\n" + "=" * 50)
print("2. 字典推导式")
print("=" * 50)

# 数字 → 平方的字典
squares_dict = {x: x**2 for x in range(5)}
print(f"数字→平方: {squares_dict}")

# 字符串 → 长度的字典
words2 = ["apple", "banana", "cherry"]
word_lengths = {word: len(word) for word in words2}
print(f"单词→长度: {word_lengths}")

# 交换键值对
swapped = {v: k for k, v in word_lengths.items()}
print(f"交换键值: {swapped}")

# ============================================================
# 3. 集合推导式
# ============================================================
print("\n" + "=" * 50)
print("3. 集合推导式")
print("=" * 50)

# 从列表提取唯一值
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x**2 for x in numbers}
print(f"原列表: {numbers}")
print(f"唯一平方数: {unique_squares}")

# 带条件过滤
even_unique = {x for x in range(10) if x % 2 == 0}
print(f"0-9 中的偶数集合: {even_unique}")

# ============================================================
# 4. 元组不是推导式 — 用生成器 + tuple()
# ============================================================
print("\n" + "=" * 50)
print("4. 元组：生成器表达式")
print("=" * 50)

# ❌ 错误写法
wrong = (x**2 for x in range(5))  # 这是生成器，不是元组！
print(f"(x**2 for x in range(5)) 的类型: {type(wrong).__name__}")

# ✅ 正确写法：用 tuple() 包装
correct = tuple(x**2 for x in range(5))
print(f"tuple(x**2 for x in range(5)) 的类型: {type(correct).__name__}")
print(f"结果: {correct}")

# ============================================================
# 5. 生成器表达式 vs 列表推导式
# ============================================================
print("\n" + "=" * 50)
print("5. 生成器表达式 vs 列表推导式")
print("=" * 50)

print("【列表推导式】立即创建完整列表:")
list_result = [x**2 for x in range(100)]
print(f"  len([x**2 for x in range(100)]) = {len(list_result)}")
print(f"  [x**2 for x in range(100)][:5] = {list_result[:5]}")

print("\n【生成器表达式】惰性求值，不创建列表:")
gen_result = (x**2 for x in range(100))
print(f"  type((x**2 for x in range(100))) = {type(gen_result).__name__}")
print("  生成器是迭代器，需要用 list() 或循环才能取值")

# 生成器逐个产出元素
print("\n用 next() 逐个获取:")
gen_small = (x**2 for x in range(5))
print(f"  next(gen): {next(gen_small)}")
print(f"  next(gen): {next(gen_small)}")
print(f"  next(gen): {next(gen_small)}")

# ============================================================
# 6. 实际应用场景
# ============================================================
print("\n" + "=" * 50)
print("6. 实际应用场景")
print("=" * 50)

# 筛选偶数
nums = range(1, 21)
even_nums = [n for n in nums if n % 2 == 0]
print(f"1-20 中的偶数: {even_nums}")

# 提取字典中的某些字段
users = [
    {"name": "Alice", "age": 25, "city": "Beijing"},
    {"name": "Bob", "age": 30, "city": "Shanghai"},
    {"name": "Charlie", "age": 35, "city": "Beijing"},
]
names = [user["name"] for user in users]
print(f"所有用户名: {names}")

beijing_users = [user["name"] for user in users if user["city"] == "Beijing"]
print(f"北京用户: {beijing_users}")

# 求和（生成器更高效）
total = sum(x**2 for x in range(1000))
print(f"\n前 1000 个数的平方和: {total}")

print("\n✅ 全部演示完成！")
