"""集合去重与运算示例。

演示集合的创建、去重、成员检测和集合运算（交集、并集、差集）。
"""

# 创建集合
print("=== 集合创建 ===")
numbers: set[int] = {1, 2, 3, 4, 5}
print(f"整数集合: {numbers}")

unique_chars: set[str] = set("hello")
print(f"字符串转集合: {unique_chars}")

# 自动去重
print("\n=== 自动去重 ===")
duplicates: list[int] = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique: set[int] = set(duplicates)
print(f"原列表: {duplicates}")
print(f"去重后: {unique}")

# 成员检测（O(1) 时间复杂度）
print("\n=== 成员检测 ===")
has_three: bool = 3 in unique
has_ten: bool = 10 in unique
print(f"3 是否在集合中: {has_three}")
print(f"10 是否在集合中: {has_ten}")

# 添加和删除
print("\n=== 添加和删除 ===")
numbers.add(6)
print(f"add(6) 后: {numbers}")

numbers.remove(1)
print(f"remove(1) 后: {numbers}")

numbers.discard(10)  # 安全删除，键不存在不报错
print(f"discard(10) 后: {numbers} (键不存在，不报错)")

# 集合运算
print("\n=== 集合运算 ===")
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

# 实际应用：找出两个用户的共同兴趣
print("\n=== 实际应用：共同兴趣 ===")
user_a_tags: set[str] = {"Python", "AI", "Web", "Database"}
user_b_tags: set[str] = {"AI", "Database", "Cloud", "DevOps"}

common_tags: set[str] = user_a_tags & user_b_tags
print(f"用户 A 兴趣: {user_a_tags}")
print(f"用户 B 兴趣: {user_b_tags}")
print(f"共同兴趣: {common_tags}")
