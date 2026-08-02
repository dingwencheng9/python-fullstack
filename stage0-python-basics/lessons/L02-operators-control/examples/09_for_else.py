"""L02 示例9: for-else 和 while-else 循环子句

本文件演示 Python 中循环的 else 子句：
- for-else: 循环正常结束时执行 else
- while-else: 条件为假时执行 else

【知识点边界】本文件仅使用 L01 + L02 的知识点：
- print, input, if/elif/else, for, while
- break, continue, range
"""

# ============================================================
# 1. for-else 模式：查找数字
# ============================================================
print("=" * 50)
print("1. for-else: 查找数字")
print("=" * 50)

numbers = [1, 3, 5, 7, 9]
target = 5
found = False

print(f"列表: {numbers}")
print(f"查找: {target}")
print("-" * 50)

for num in numbers:
    if num == target:
        print(f"找到 {target} ！")
        found = True
        break
else:
    # 只有循环正常结束（未执行 break）时才执行这里
    print(f"{target} 不在列表中")

print("-" * 50)

# 再测一次：查找一个不存在的数字
target = 4
found = False

print(f"\n查找: {target}")
for num in numbers:
    if num == target:
        print(f"找到 {target} ！")
        found = True
        break
else:
    print(f"{target} 不在列表中")

# ============================================================
# 2. for-else 模式：判断质数
# ============================================================
print("\n" + "=" * 50)
print("2. for-else: 判断质数")
print("=" * 50)

test_numbers = [2, 3, 4, 5, 15, 17, 18, 19, 20]

for n in test_numbers:
    if n < 2:
        print(f"{n}: 不是质数（< 2）")
        continue

    is_prime = True
    # 检查从 2 到 sqrt(n) 的所有可能因子
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            print(f"{n}: 不是质数（{i} × {n // i} = {n}）")
            is_prime = True
            break
    else:
        print(f"{n}: 是质数！")

# ============================================================
# 3. for-else 模式：检查所有人是否及格
# ============================================================
print("\n" + "=" * 50)
print("3. for-else: 检查所有人是否及格")
print("=" * 50)

scores = [85, 92, 78, 95, 88]
threshold = 60

print(f"分数列表: {scores}")
print(f"及格线: {threshold}")
print("-" * 50)

for score in scores:
    if score < threshold:
        print(f"有人不及格: {score}")
        break
else:
    print("全部及格！")

# 另一个场景：有不及格的
scores2 = [85, 55, 78, 95, 88]
print(f"\n分数列表: {scores2}")
for score in scores2:
    if score < threshold:
        print(f"有人不及格: {score}")
        break
else:
    print("全部及格！")

# ============================================================
# 4. while-else 模式：有限次尝试
# ============================================================
print("\n" + "=" * 50)
print("4. while-else: 有限次尝试")
print("=" * 50)

password = "python123"
attempts = 3

print(f"正确密码: {password}")
print(f"最大尝试次数: {attempts}")

# 模拟三次猜测（不实际调用 input）
guesses = ["wrong1", "wrong2", "python123"]
attempt = 0

while attempt < attempts:
    guess = guesses[attempt]
    print(f"  尝试 {attempt + 1}: {guess}")
    if guess == password:
        print("  → 密码正确！")
        break
    attempt += 1
else:
    print(f"账户已被锁定（{attempts} 次机会用完）")
