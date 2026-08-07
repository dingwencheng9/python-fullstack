"""L02 练习6: 综合练习 - 运算符与控制流

难度: ⭐⭐⭐ (进阶)
预计时间: 40 分钟
知识点: 算术运算符、逻辑运算符、循环、条件语句综合应用

学习方式:
本练习是"演示型练习"——代码已经完整实现，
你需要运行它，观察输出，理解代码的工作原理。

任务描述:
综合练习：本练习整合了运算符与控制流的核心知识点，
包括 FizzBuzz、素数判断、数字统计等经典问题。

提示:
1. FizzBuzz: 先判断 15 的倍数，再判断 3 和 5
2. 素数判断: 只需检查到 sqrt(n) 即可
3. 注意边界条件 (如 n <= 1)
"""

# ============================================================
# 演示：FizzBuzz 游戏
# ============================================================
print("=== FizzBuzz 游戏演示 ===\n")
print("规则:")
print("   - 3 的倍数 → 'Fizz'")
print("   - 5 的倍数 → 'Buzz'")
print("   - 3 和 5 的倍数 → 'FizzBuzz'")
print("   - 其他 → 数字本身\n")
print("FizzBuzz(1-15) 结果:")
print("   ", end="")

# 使用字符串拼接代替列表收集结果
result_str = ""
for i in range(1, 16):
    if result_str:
        result_str += ", "
    if i % 15 == 0:
        result_str += 'FizzBuzz'
    elif i % 3 == 0:
        result_str += 'Fizz'
    elif i % 5 == 0:
        result_str += 'Buzz'
    else:
        result_str += str(i)
print(result_str)

# ============================================================
# 演示：素数判断
# ============================================================
print("\n=== 素数判断演示 ===\n")

print("判断 1-20 是否为素数:")
for i in range(1, 21):
    # 手动模拟 is_prime 逻辑
    if i <= 1:
        result = False
    elif i <= 3:
        result = True
    elif i % 2 == 0 or i % 3 == 0:
        result = False
    else:
        result = True
        j = 5
        while j * j <= i:
            if i % j == 0 or i % (j + 2) == 0:
                result = False
                break
            j += 6
    status = '素数' if result else ''
    print(f"   {i:2}: {status}")

# ============================================================
# 演示：简易计算器
# ============================================================
print("\n=== 简易计算器演示 ===\n")

print("测试 1: 10 + 3 = ?")
a, b, op = 10, 3, '+'
if op == '+':
    result = a + b
elif op == '-':
    result = a - b
elif op == '*':
    result = a * b
elif op == '/':
    if b == 0:
        result = None
    else:
        result = a / b
else:
    result = None
print(f"   10 + 3 = {result}")

print("\n测试 2: 10 - 3 = ?")
a, b, op = 10, 3, '-'
if op == '+':
    result = a + b
elif op == '-':
    result = a - b
elif op == '*':
    result = a * b
elif op == '/':
    if b == 0:
        result = None
    else:
        result = a / b
else:
    result = None
print(f"   10 - 3 = {result}")

print("\n测试 3: 10 * 3 = ?")
a, b, op = 10, 3, '*'
if op == '+':
    result = a + b
elif op == '-':
    result = a - b
elif op == '*':
    result = a * b
elif op == '/':
    if b == 0:
        result = None
    else:
        result = a / b
else:
    result = None
print(f"   10 * 3 = {result}")

print("\n测试 4: 10 / 3 = ?")
a, b, op = 10, 3, '/'
if op == '+':
    result = a + b
elif op == '-':
    result = a - b
elif op == '*':
    result = a * b
elif op == '/':
    if b == 0:
        result = None
    else:
        result = a / b
else:
    result = None
print(f"   10 / 3 = {result}")

print("\n测试 5: 10 / 0 = ?")
a, b, op = 10, 0, '/'
if op == '+':
    result = a + b
elif op == '-':
    result = a - b
elif op == '*':
    result = a * b
elif op == '/':
    if b == 0:
        result = None
    else:
        result = a / b
else:
    result = None
print(f"   10 / 0 = {result}")

print("\n测试 6: 2 ** 3 = ?")
a, b, op = 2, 3, '**'
if op == '+':
    result = a + b
elif op == '-':
    result = a - b
elif op == '*':
    result = a * b
elif op == '/':
    if b == 0:
        result = None
    else:
        result = a / b
else:
    result = None
print(f"   2 ** 3 = {result}")

# ============================================================
# 演示：价格计算
# ============================================================
print("\n=== 价格计算演示 ===\n")

print("测试 1: 单价 100, 数量 2, 无折扣无税")
price, qty, discount, tax = 100, 2, 0, 0
subtotal = price * qty
discount_amount = subtotal * (discount / 100)
after_discount = subtotal - discount_amount
tax_amount = after_discount * (tax / 100)
result = round(after_discount + tax_amount, 2)
print(f"   (100×2, -0%, +0%) = {result}")

print("\n测试 2: 单价 100, 数量 2, 10%折扣无税")
price, qty, discount, tax = 100, 2, 10, 0
subtotal = price * qty
discount_amount = subtotal * (discount / 100)
after_discount = subtotal - discount_amount
tax_amount = after_discount * (tax / 100)
result = round(after_discount + tax_amount, 2)
print(f"   (100×2, -10%, +0%) = {result}")

print("\n测试 3: 单价 100, 数量 2, 无折扣 13%税")
price, qty, discount, tax = 100, 2, 0, 13
subtotal = price * qty
discount_amount = subtotal * (discount / 100)
after_discount = subtotal - discount_amount
tax_amount = after_discount * (tax / 100)
result = round(after_discount + tax_amount, 2)
print(f"   (100×2, -0%, +13%) = {result}")

# ============================================================
# 思考题
# ============================================================
print("\n=== 思考题 ===")
print("1. 为什么 FizzBuzz 的判断顺序是 15 → 3 → 5？")
print("2. 素数判断为什么只需检查到 sqrt(n)？")
print("3. 折扣和税费计算的顺序重要吗？")
