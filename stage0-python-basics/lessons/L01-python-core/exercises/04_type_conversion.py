"""L01 练习4: 类型转换挑战

难度: ⭐☆☆ (入门)
预计时间: 15 分钟
知识点: int(), float(), str(), bool() 类型转换

学习方式:
本练习是"演示型练习"——代码已经完整实现，
你需要运行它，观察输出，理解代码的工作原理。

任务描述:
1. 运行这个文件，观察不同类型之间的转换
2. 理解什么时候需要类型转换
3. 观察特殊值的转换结果（如空字符串、0 等）

关键概念:
- int() 可以将数字字符串转为整数
- float() 可以将数字字符串转为浮点数
- str() 可以将任何值转为字符串
- bool() 可以将任何值转为布尔值
- 非零数字和非空字符串在布尔上下文中为 True
"""

# ============================================================
# 演示：字符串转数字
# ============================================================

print("--- 字符串转数字 ---")

# 字符串到整数
num_str = "42"
num_int = int(num_str)
print(f"int('{num_str}') = {num_int}")
print(f"  type: {type(num_int)}")

# 字符串到浮点数
pi_str = "3.14159"
pi_float = float(pi_str)
print(f"\nfloat('{pi_str}') = {pi_float}")
print(f"  type: {type(pi_float)}")

# 从整数到浮点数
age = 25
age_float = float(age)
print(f"\nfloat({age}) = {age_float}")
print(f"  type: {type(age_float)}")

# ============================================================
# 演示：数字转字符串
# ============================================================

print("\n--- 数字转字符串 ---")

price = 99.9
price_str = str(price)
print(f"str({price}) = '{price_str}'")
print(f"  type: {type(price_str)}")

# 字符串可以拼接，数字不能直接与字符串拼接
count = 5
message = "商品数量: " + str(count)
print(f"  拼接结果: {message}")

# ============================================================
# 演示：布尔转换规则
# ============================================================

print("\n--- 布尔转换规则 ---")

# 假值（转换为 False）
print("假值 (bool 为 False):")
print(f"  bool(0) = {bool(0)}")
print(f"  bool(0.0) = {bool(0.0)}")
print(f"  bool('') = {bool('')}")  # 空字符串
print(f"  bool(None) = {bool(None)}")

# 真值（转换为 True）
print("\n真值 (bool 为 True):")
print(f"  bool(1) = {bool(1)}")
print(f"  bool(-1) = {bool(-1)}")
print(f"  bool(0.1) = {bool(0.1)}")
print(f"  bool('hello') = {bool('hello')}")  # 非空字符串

# ============================================================
# 演示：实用场景（静态示例）
# ============================================================

print("\n--- 实用场景 ---")

# 场景1: 类型转换在计算中的应用
base_price = 99.9
tax_rate = 0.08
tax = base_price * tax_rate
total = base_price + tax
print(f"原价: {base_price}, 税率: {tax_rate:.0%}, 税额: {tax:.2f}, 总价: {total:.2f}")

# 场景2: 字符串拼接数字
count = 5
message = "商品数量: " + str(count)
print(f"  {message}")

# 场景3: 布尔判断
score = 85.5
passed = score >= 60
print(f"分数: {score}, 是否及格: {passed}")
print(f"类型: {type(passed)}")

# ============================================================
# 交互式演示（取消注释后需要手动输入）
# ============================================================
# 如果你想尝试交互式输入，取消下面代码的注释:
#
# num1 = float(input("输入第一个数字: "))
# num2 = float(input("输入第二个数字: "))
# result = num1 + num2
# print(f"结果: {num1} + {num2} = {result}")
#
# score = float(input("\n输入你的分数: "))
# passed = score >= 60
# print(f"是否及格: {passed}")

# ============================================================
# 思考题
# ============================================================
# 1. int("3.14") 会怎样？为什么？
# 2. bool("False") 是 True 还是 False？
# 3. 为什么需要类型转换？
