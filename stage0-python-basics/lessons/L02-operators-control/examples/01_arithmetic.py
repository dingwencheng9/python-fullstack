"""L02 示例1: 算术运算符"""

# 1. 基本运算

a, b = 10, 3

print("=== 基本算术 ===")
print(f"{a} + {b} = {a + b}")  # 加法: 13
print(f"{a} - {b} = {a - b}")  # 减法: 7
print(f"{a} * {b} = {a * b}")  # 乘法: 30
print(f"{a} / {b} = {a / b}")  # 除法: 3.333...

# 2. 特殊运算
print("\n=== 特殊运算 ===")
print(f"{a} // {b} = {a // b}")  # 整除: 3
print(f"{a} % {b} = {a % b}")  # 取模: 1
print(f"{a} ** {b} = {a**b}")  # 幂运算: 1000

# 3. 实用案例：判断奇偶
num = 7
if num % 2 == 0:
    print(f"\n{num} 是偶数")
else:
    print(f"\n{num} 是奇数")
