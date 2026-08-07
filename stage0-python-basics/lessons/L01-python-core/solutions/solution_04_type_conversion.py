"""L01 参考答案 4: 类型转换挑战

对应练习: exercises/04_type_conversion.py
知识点: int()、float()、str()、bool() 类型转换

"""

# ============================================================
# 字符串与其他类型转换
# ============================================================
print("=== 字符串转数字 ===\n")

# 字符串转整数
num_str = "42"
num = int(num_str)
print(f"int('{num_str}') = {num}")

# 字符串转浮点数
price_str = "19.99"
price = float(price_str)
print(f"float('{price_str}') = {price}")

# ============================================================
# 数字转字符串
# ============================================================
print("\n=== 数字转字符串 ===\n")

age = 25
age_str = str(age)
print(f"str({age}) = '{age_str}'")

pi = 3.14159
pi_str = str(pi)
print(f"str({pi}) = '{pi_str}'")

# ============================================================
# 浮点数转整数（截断）
# ============================================================
print("\n=== 浮点数转整数 ===\n")

pi = 3.14159
pi_int = int(pi)
print(f"int({pi}) = {pi_int}（截断小数）")

# ============================================================
# 布尔转换
# ============================================================
print("\n=== 布尔转换 ===\n")

print(f"bool(1) = {bool(1)}")
print(f"bool(0) = {bool(0)}")
print(f"bool(-1) = {bool(-1)}")
print(f"bool('hello') = {bool('hello')}")
print(f"bool('') = {bool('')}")
print(f"int(True) = {int(True)}")
print(f"int(False) = {int(False)}")

# ============================================================
# 类型检查（使用 isinstance）
# ⚠️ L01 边界: isinstance() 是 L06 的知识点，这里仅作提前预览
# ============================================================
print("\n=== 类型检查 ===\n")

x = 42
y = "hello"
z = 3.14

print(f"isinstance({x}, int) = {isinstance(x, int)}")
print(f"isinstance('{y}', str) = {isinstance(y, str)}")
print(f"isinstance({z}, float) = {isinstance(z, float)}")
print(f"isinstance({x}, (int, float)) = {isinstance(x, (int, float))}")

print("\n📖 预告：")
print("  - L02 将学习 is 与 == 的区别")
print("  - L03 将学习 list、dict、set 等数据结构")
