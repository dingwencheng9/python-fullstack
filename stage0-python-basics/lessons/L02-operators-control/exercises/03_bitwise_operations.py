"""L02 练习3: 位运算符应用

难度: ⭐⭐☆ (中等)
预计时间: 30 分钟
知识点: 位运算符（&, |, ^, <<, >>, ~）、权限管理、状态压缩

学习方式:
本练习是"演示型练习"——代码已经完整实现，
你需要运行它，观察输出，理解代码的工作原理。

任务描述:
练习位运算技巧，综合运用：
- 位运算符（&, |, ^, <<, >>, ~）
- 权限标志位管理
- 状态压缩存储

提示:
1. 判断奇偶: number & 1 (最低位为 1 则为奇数)
2. 权限检查: permissions & flag != 0
3. 添加权限: permissions | flag
"""

# ============================================================
# 演示：奇偶判断（位运算）
# ============================================================
print("=== 奇偶判断演示 ===\n")

print("测试用例 1: n=4")
n = 4
result = (n & 1) == 0
print(f"   {n} 是{'偶数' if result else '奇数'}")

print("\n测试用例 2: n=7")
n = 7
result = (n & 1) == 0
print(f"   {n} 是{'偶数' if result else '奇数'}")

print("\n测试用例 3: n=0")
n = 0
result = (n & 1) == 0
print(f"   {n} 是{'偶数' if result else '奇数'}")

print("\n测试用例 4: n=1")
n = 1
result = (n & 1) == 0
print(f"   {n} 是{'偶数' if result else '奇数'}")

print("\n测试用例 5: n=100")
n = 100
result = (n & 1) == 0
print(f"   {n} 是{'偶数' if result else '奇数'}")

# ============================================================
# 演示：数字交换（异或）
# ============================================================
print("\n=== 数字交换演示（异或）===\n")

print("测试用例 1: a=5, b=3")
a, b = 5, 3
temp_a, temp_b = a, b
temp_a = temp_a ^ temp_b
temp_b = temp_a ^ temp_b
temp_a = temp_a ^ temp_b
print(f"   swap({a}, {b}) = ({temp_a}, {temp_b})")

print("\n测试用例 2: a=10, b=20")
a, b = 10, 20
temp_a, temp_b = a, b
temp_a = temp_a ^ temp_b
temp_b = temp_a ^ temp_b
temp_a = temp_a ^ temp_b
print(f"   swap({a}, {b}) = ({temp_a}, {temp_b})")

print("\n测试用例 3: a=0, b=1")
a, b = 0, 1
temp_a, temp_b = a, b
temp_a = temp_a ^ temp_b
temp_b = temp_a ^ temp_b
temp_a = temp_a ^ temp_b
print(f"   swap({a}, {b}) = ({temp_a}, {temp_b})")

print("\n测试用例 4: a=100, b=100")
a, b = 100, 100
temp_a, temp_b = a, b
temp_a = temp_a ^ temp_b
temp_b = temp_a ^ temp_b
temp_a = temp_a ^ temp_b
print(f"   swap({a}, {b}) = ({temp_a}, {temp_b})")

# ============================================================
# 演示：权限管理
# ============================================================
print("\n=== 权限管理演示 ===\n")

# 权限标志位常量（使用 2 的幂次方）
PERMISSION_READ = 1 << 0    # 1   - 0001
PERMISSION_WRITE = 1 << 1   # 2   - 0010
PERMISSION_DELETE = 1 << 2   # 4   - 0100
PERMISSION_ADMIN = 1 << 3    # 8   - 1000

print("权限标志位:")
print(f"   READ   = {PERMISSION_READ} (二进制: {bin(PERMISSION_READ)})")
print(f"   WRITE  = {PERMISSION_WRITE} (二进制: {bin(PERMISSION_WRITE)})")
print(f"   DELETE = {PERMISSION_DELETE} (二进制: {bin(PERMISSION_DELETE)})")
print(f"   ADMIN  = {PERMISSION_ADMIN} (二进制: {bin(PERMISSION_ADMIN)})")

# 演示权限操作
perms = 0
print(f"\n初始权限: {perms} (二进制: {bin(perms)})")

# 授予读权限
perms = perms | PERMISSION_READ
print(f"授予读权限后: {perms} (二进制: {bin(perms)})")
print(f"   检查读权限 (perms & READ): {perms & PERMISSION_READ != 0}")

# 授予写权限
perms = perms | PERMISSION_WRITE
print(f"授予写权限后: {perms} (二进制: {bin(perms)})")

# 撤销读权限
perms = perms & (~PERMISSION_READ)
print(f"撤销读权限后: {perms} (二进制: {bin(perms)})")
print(f"   检查读权限: {perms & PERMISSION_READ != 0}")

# 授予管理员权限
perms = perms | PERMISSION_ADMIN
print(f"授予管理员权限后: {perms} (二进制: {bin(perms)})")

# ============================================================
# 演示：位运算原理
# ============================================================
print("\n=== 位运算原理演示 ===\n")

print("判断奇偶原理:")
print("   偶数二进制最低位是 0，奇数是 1")
print(f"   4 的二进制: {bin(4)}, 4 & 1 = {4 & 1} (0 表示偶数)")
print(f"   7 的二进制: {bin(7)}, 7 & 1 = {7 & 1} (1 表示奇数)")

print("\n异或交换原理:")
print("   a ^ b ^ a = b, a ^ b ^ b = a")
a, b = 5, 3
print(f"   交换前: a={a}, b={b}")
a_xor_b = a ^ b
print(f"   a = a ^ b = {a_xor_b}")
b_final = a_xor_b ^ b
print(f"   b = a ^ b = {a_xor_b} ^ {b} = {b_final}")
a_final = a_xor_b ^ a
print(f"   a = a ^ b = {a_xor_b} ^ {a} = {a_final}")

# ============================================================
# 思考题
# ============================================================
print("\n=== 思考题 ===")
print("1. 为什么可以用 a & 1 判断奇偶？")
print("2. 如何用位运算判断一个数是否是 2 的幂次方？")
print("3. permissions | flag 和 permissions & ~flag 的区别是什么？")
