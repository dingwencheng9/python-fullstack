"""L02 示例5: if/elif/else"""

# 1. 基本 if

age = 18
if age >= 18:
    print("成年人")

# 2. if-else
score = 75
if score >= 60:
    print("及格")
else:
    print("不及格")

# 3. if-elif-else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "D"
print(f"成绩: {grade}")

# 4. 嵌套 if
num = 10
if num > 0:
    if num % 2 == 0:
        print("正偶数")
    else:
        print("正奇数")
