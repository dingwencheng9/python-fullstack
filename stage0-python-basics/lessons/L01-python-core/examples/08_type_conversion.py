"""L01 示例8: 类型转换

Python 是强类型语言，不同类型不能直接运算，需要显式转换。
提供转换函数：int() / float() / str() / bool()。

"""

# ===== 1. 字符串 → 整数/浮点数 =====
print("=== 1. 字符串 → 数字 ===")

age_str = "25"
age_int = int(age_str)
print(f"int('{age_str}') = {age_int}   type = {type(age_int)}")

price_str = "19.99"
price_float = float(price_str)
print(f"float('{price_str}') = {price_float}   type = {type(price_float)}")

# ===== 2. 数字 → 字符串 =====
print("\n=== 2. 数字 → 字符串 ===")

count = 100
count_str = str(count)
print(f"str({count}) = '{count_str}'   type = {type(count_str)}")

pi = 3.14159
pi_str = str(pi)
print(f"str({pi}) = '{pi_str}'   type = {type(pi_str)}")

# ===== 3. 布尔转换 =====
print("\n=== 3. 布尔转换 ===")
print(f"bool(0)       = {bool(0)}")  # False
print(f"bool(1)       = {bool(1)}")  # True
print(f"bool('')      = {bool('')}")  # False（空字符串）
print(f"bool('hello') = {bool('hello')}")  # True
print(f"bool(None)    = {bool(None)}")  # False

# ===== 4. 整数 ↔ 浮点数 =====
print("\n=== 4. 整数 ↔ 浮点数 ===")
print(f"float(10) = {float(10)}")
print(f"int(3.99) = {int(3.99)}")  # 浮点数 → 整数会截断小数部分

# ===== 5. 实用案例：用户输入 =====
print("\n=== 5. 用户输入与类型转换 ===")
# input() 返回的是字符串
# 如果需要数字，必须做类型转换
user_input = "18"  # 模拟用户输入
age = int(user_input)  # 字符串 → 整数
print(f"用户输入: '{user_input}'   type = {type(user_input)}")
print(f"转换后: {age}   type = {type(age)}")
print(f"5 年后: {age + 5} 岁")
