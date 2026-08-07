"""L02 练习1: 算术运算符与条件语句

难度: ⭐☆☆ (入门)
预计时间: 15 分钟
知识点: 算术运算符、比较运算符、if/elif/else 多分支

学习方式:
本练习是"演示型练习"——代码已经完整实现，
你需要运行它，观察输出，理解代码的工作原理。

任务描述:
练习 BMI（身体质量指数）计算器，综合运用：
- 算术运算符（/, **）
- 比较运算符（<, >, <=, >=）
- if/elif/else 多分支

提示:
1. BMI 公式: 体重(kg) / 身高(m)^2
2. 使用 if/elif/else 判断 BMI 范围
3. 注意浮点数计算精度
"""

# ============================================================
# 演示：BMI 计算器
# ============================================================
print("=== BMI 计算器演示 ===\n")

print("测试用例 1: 体重 70kg, 身高 1.75m")
weight, height = 70, 1.75
bmi = weight / (height ** 2)
if bmi < 18.5:
    level = '偏瘦'
elif bmi < 24:
    level = '正常'
elif bmi < 28:
    level = '偏胖'
else:
    level = '肥胖'
print(f"  BMI={bmi:.2f} → {level}")

print("\n测试用例 2: 体重 50kg, 身高 1.6m")
weight, height = 50, 1.6
bmi = weight / (height ** 2)
if bmi < 18.5:
    level = '偏瘦'
elif bmi < 24:
    level = '正常'
elif bmi < 28:
    level = '偏胖'
else:
    level = '肥胖'
print(f"  BMI={bmi:.2f} → {level}")

print("\n测试用例 3: 体重 90kg, 身高 1.7m")
weight, height = 90, 1.7
bmi = weight / (height ** 2)
if bmi < 18.5:
    level = '偏瘦'
elif bmi < 24:
    level = '正常'
elif bmi < 28:
    level = '偏胖'
else:
    level = '肥胖'
print(f"  BMI={bmi:.2f} → {level}")

print("\n测试用例 4: 体重 45kg, 身高 1.8m")
weight, height = 45, 1.8
bmi = weight / (height ** 2)
if bmi < 18.5:
    level = '偏瘦'
elif bmi < 24:
    level = '正常'
elif bmi < 28:
    level = '偏胖'
else:
    level = '肥胖'
print(f"  BMI={bmi:.2f} → {level}")

# ============================================================
# 演示：成绩等级计算
# ============================================================
print("\n=== 成绩等级计算演示 ===\n")

print("测试用例 1: 分数 95")
score = 95
if score >= 90:
    grade = 'S'
elif score >= 80:
    grade = 'A'
elif score >= 70:
    grade = 'B'
elif score >= 60:
    grade = 'C'
else:
    grade = 'D'
print(f"  等级: {grade}")

print("\n测试用例 2: 分数 88")
score = 88
if score >= 90:
    grade = 'S'
elif score >= 80:
    grade = 'A'
elif score >= 70:
    grade = 'B'
elif score >= 60:
    grade = 'C'
else:
    grade = 'D'
print(f"  等级: {grade}")

print("\n测试用例 3: 分数 75")
score = 75
if score >= 90:
    grade = 'S'
elif score >= 80:
    grade = 'A'
elif score >= 70:
    grade = 'B'
elif score >= 60:
    grade = 'C'
else:
    grade = 'D'
print(f"  等级: {grade}")

print("\n测试用例 4: 分数 65")
score = 65
if score >= 90:
    grade = 'S'
elif score >= 80:
    grade = 'A'
elif score >= 70:
    grade = 'B'
elif score >= 60:
    grade = 'C'
else:
    grade = 'D'
print(f"  等级: {grade}")

print("\n测试用例 5: 分数 45")
score = 45
if score >= 90:
    grade = 'S'
elif score >= 80:
    grade = 'A'
elif score >= 70:
    grade = 'B'
elif score >= 60:
    grade = 'C'
else:
    grade = 'D'
print(f"  等级: {grade}")

# ============================================================
# 思考题
# ============================================================
print("\n=== 思考题 ===")
print("1. BMI < 18.5 表示偏瘦，这个阈值是如何得出的？")
print("2. 如果身高是 1.75m，体重是 70kg，BMI 是多少？")
print("3. grade = 'S' 对应的分数范围是多少？")
