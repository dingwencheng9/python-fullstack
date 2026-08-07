"""L02 示例9: for-else 和 while-else 循环子句

本文件演示 Python 中循环的 else 子句：
- for-else: 循环正常结束时执行 else
- while-else: 条件为假时执行 else

【知识点边界】本文件仅使用 L01 + L02 的知识点：
- print, input, if/elif/else, for, while
- break, continue, range
- 注意：不使用任何列表/字典/集合
"""

# ============================================================
# 1. for-else 模式：查找字符
# ============================================================
print("=" * 50)
print("1. for-else: 查找字符")
print("=" * 50)

text = "Hello"
target = "l"
found = False

print(f"字符串: '{text}'")
print(f"查找: '{target}'")
print("-" * 50)

for char in text:
    if char == target:
        print(f"找到 '{target}' ！")
        found = True
        break
else:
    print(f"'{target}' 不在字符串中")

print("-" * 50)

# 再测一次：查找一个不存在的字符
target = "X"

print(f"\n查找: '{target}'")
for char in text:
    if char == target:
        print(f"找到 '{target}' ！")
        break
else:
    print(f"'{target}' 不在字符串中")

# ============================================================
# 2. for-else 模式：判断质数
# ============================================================
print("\n" + "=" * 50)
print("2. for-else: 判断质数")
print("=" * 50)

# 使用 range 遍历 2-20 的数字（不使用列表）
for n in range(2, 21):
    if n < 2:
        print(f"{n}: 不是质数（< 2）")
        continue

    # 逐个检查因子
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            print(f"{n}: 不是质数（{i} × {n // i} = {n}）")
            break
    else:
        print(f"{n}: 是质数！")

# ============================================================
# 3. for-else 模式：密码验证
# ============================================================
print("\n" + "=" * 50)
print("3. for-else: 密码验证")
print("=" * 50)

correct_password = "python"
attempt_limit = 3

print(f"正确密码: '{correct_password}'")
print(f"最大尝试次数: {attempt_limit}")
print("-" * 50)

# 直接列举猜测（不使用列表存储）
passwords = "wrong1 wrong2 python"
p_index = 0
p_count = 0

while p_count < attempt_limit:
    # 找到空格位置
    space_pos = -1
    temp = p_index
    while temp < len(passwords) and passwords[temp] != " ":
        temp += 1
    if temp < len(passwords):
        space_pos = temp

    if space_pos == -1:
        guess = passwords[p_index:]
        p_index = len(passwords)
    else:
        guess = passwords[p_index:space_pos]
        p_index = space_pos + 1

    print(f"  尝试 {p_count + 1}: '{guess}'")
    if guess == correct_password:
        print("  → 密码正确！")
        break
    p_count += 1
else:
    print(f"账户已被锁定（{attempt_limit} 次机会用完）")

# ============================================================
# 4. while-else 模式：数字游戏
# ============================================================
print("\n" + "=" * 50)
print("4. while-else: 猜数字")
print("=" * 50)

target = 7
max_attempts = 5

print(f"目标数字: {target}")
print(f"最大尝试次数: {max_attempts}")

# 直接列举猜测数字（不使用列表）
guess_numbers = "3 5 8 7"
g_index = 0
g_count = 0
current_guess = 0

while g_count < max_attempts:
    # 解析下一个数字
    if g_index >= len(guess_numbers):
        break

    # 找到空格
    space_pos = -1
    temp = g_index
    while temp < len(guess_numbers) and guess_numbers[temp] != " ":
        temp += 1
    if temp < len(guess_numbers):
        space_pos = temp

    if space_pos == -1:
        num_str = guess_numbers[g_index:]
        g_index = len(guess_numbers)
    else:
        num_str = guess_numbers[g_index:space_pos]
        g_index = space_pos + 1

    # 转换字符串为数字
    current_guess = 0
    for digit in num_str:
        current_guess = current_guess * 10 + (ord(digit) - ord("0"))

    print(f"  尝试 {g_count + 1}: {current_guess}")
    if current_guess == target:
        print("  → 猜对了！")
        break
    g_count += 1
else:
    print(f"很遗憾，没有在 {max_attempts} 次内猜中")
