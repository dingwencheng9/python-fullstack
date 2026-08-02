"""L02 示例3: 逻辑运算符"""

# 1. and (与)

print("=== and 运算 ===")
print(f"True and True: {True and True}")  # True
print(f"True and False: {True and False}")  # False

# 2. or (或)
print("\n=== or 运算 ===")
print(f"True or False: {True or False}")  # True
print(f"False or False: {False or False}")  # False

# 3. not (非)
print("\n=== not 运算 ===")
print(f"not True: {not True}")  # False
print(f"not False: {not False}")  # True

# 4. 实用案例：权限检查
age = 20
has_id = True

if age >= 18 and has_id:
    print("\n✅ 允许进入")
else:
    print("\n❌ 拒绝进入")
