"""L01 参考答案 3: 变量与类型基础

对应练习: exercises/03_type_basics.py
知识点: type()、id()、变量引用

"""

# ============================================================
# 演示基本数据类型
# ============================================================
print("=== 基本数据类型 ===\n")

# 整数
age: int = 25
print(f"整数: age = {age}, 类型 = {type(age)}")

# 浮点数
height: float = 1.75
print(f"浮点数: height = {height}, 类型 = {type(height)}")

# 字符串
name: str = "张三"
print(f"字符串: name = {name}, 类型 = {type(name)}")

# 布尔值
is_student: bool = True
print(f"布尔值: is_student = {is_student}, 类型 = {type(is_student)}")

# None 类型
middle_name: str | None = None
print(f"None: middle_name = {middle_name}, 类型 = {type(middle_name)}")

# ============================================================
# 演示类型操作（仅 + - * /）
# ============================================================
print("\n=== 类型操作 ===\n")

a, b = 10, 3
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")

print("\n📖 预告：L02 将学习整除(//)、取模(%)、幂(**)等运算符")

# ============================================================
# 演示变量命名规则
# ============================================================
print("\n=== 变量命名规则 ===\n")

# 合法的变量名
user_name = "Alice"  # 蛇形命名法（推荐）
user_age = 25  # 蛇形命名法（推荐）
private_val = "隐藏"  # 以下划线开头
MAX_COUNT = 100  # 常量（全大写）

print(f"user_name = {user_name}")
print(f"user_age = {user_age}")
print(f"private_val = {private_val}")
print(f"MAX_COUNT = {MAX_COUNT}")
