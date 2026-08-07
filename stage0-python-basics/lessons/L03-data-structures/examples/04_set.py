"""L03 示例4: 集合去重与运算

学习目标:
- 掌握集合的创建、去重、成员检测
- 理解集合运算（交集、并集、差集、对称差集）

【知识点边界】本文件仅使用 L01 + L02 + L03 的知识点：
- print, for, range, if
- set
- 集合操作、集合推导式
"""


# ============================================================
# 1. 创建集合
# ============================================================
print("=" * 50)
print("1. 集合创建")
print("=" * 50)

# 空集合（注意不是 {}，那是字典）
numbers: set[int] = {1, 2, 3, 4, 5}
print(f"整数集合: {numbers}")

unique_chars: set[str] = set("hello")
print(f"字符串转集合: {unique_chars}")


# ============================================================
# 2. 自动去重
# ============================================================
print("\n" + "=" * 50)
print("2. 自动去重")
print("=" * 50)

duplicates: list[int] = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique: set[int] = set(duplicates)
print(f"原列表: {duplicates}")
print(f"去重后: {unique}")


# ============================================================
# 3. 成员检测（O(1) 时间复杂度）
# ============================================================
print("\n" + "=" * 50)
print("3. 成员检测")
print("=" * 50)

has_three: bool = 3 in unique
has_ten: bool = 10 in unique
print(f"3 是否在集合中: {has_three}")
print(f"10 是否在集合中: {has_ten}")


# ============================================================
# 4. 添加和删除
# ============================================================
print("\n" + "=" * 50)
print("4. 添加和删除")
print("=" * 50)

numbers.add(6)
print(f"add(6) 后: {numbers}")

numbers.remove(1)
print(f"remove(1) 后: {numbers}")

numbers.discard(10)  # 安全删除，键不存在不报错
print(f"discard(10) 后: {numbers} (键不存在，不报错)")


# ============================================================
# 5. 集合运算
# ============================================================
print("\n" + "=" * 50)
print("5. 集合运算")
print("=" * 50)

a: set[int] = {1, 2, 3, 4}
b: set[int] = {3, 4, 5, 6}

print(f"集合 A: {a}")
print(f"集合 B: {b}")

# 交集（intersection）
intersection: set[int] = a & b
print(f"交集 A & B: {intersection}")

# 并集（union）
union: set[int] = a | b
print(f"并集 A | B: {union}")

# 差集（difference）
diff: set[int] = a - b
print(f"差集 A - B: {diff}")

# 对称差集（symmetric difference）
sym_diff: set[int] = a ^ b
print(f"对称差集 A ^ B: {sym_diff}")


# ============================================================
# 6. 实际应用：共同兴趣
# ============================================================
print("\n" + "=" * 50)
print("6. 实际应用：共同兴趣")
print("=" * 50)

user_a_tags: set[str] = {"Python", "AI", "Web", "Database"}
user_b_tags: set[str] = {"AI", "Database", "Cloud", "DevOps"}

common_tags: set[str] = user_a_tags & user_b_tags
print(f"用户 A 兴趣: {user_a_tags}")
print(f"用户 B 兴趣: {user_b_tags}")
print(f"共同兴趣: {common_tags}")


# ============================================================
# 7. 集合推导式
# ============================================================
print("\n" + "=" * 50)
print("7. 集合推导式")
print("=" * 50)

squares = {x**2 for x in range(5)}
print(f"集合推导式: {squares}")

# 从列表提取唯一值
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x**2 for x in numbers}
print(f"原列表: {numbers}")
print(f"唯一平方数: {unique_squares}")

# 带条件过滤
even_unique = {x for x in range(10) if x % 2 == 0}
print(f"0-9 中的偶数集合: {even_unique}")


print("\n✅ 全部演示完成！")
