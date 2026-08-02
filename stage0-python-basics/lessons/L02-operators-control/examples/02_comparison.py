"""L02 示例2: 比较运算符"""

a, b = 10, 5

print("=== 相等比较 ===")
print(f"{a} == {b}: {a == b}")  # False
print(f"{a} != {b}: {a != b}")  # True

print("\n=== 大小比较 ===")
print(f"{a} > {b}: {a > b}")  # True
print(f"{a} < {b}: {a < b}")  # False
print(f"{a} >= {b}: {a >= b}")  # True
print(f"{a} <= {b}: {a <= b}")  # False

# 实用案例：成绩等级
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "D"

print(f"\n分数 {score} 等级: {grade}")
