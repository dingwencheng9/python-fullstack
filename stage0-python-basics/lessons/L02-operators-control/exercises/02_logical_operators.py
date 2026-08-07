"""L02 练习2: 逻辑运算符与短路求值

难度: ⭐☆☆ (入门)
预计时间: 15 分钟
知识点: and/or/not 运算符、短路求值、条件判断

学习方式:
本练习是"演示型练习"——代码已经完整实现，
你需要运行它，观察输出，理解代码的工作原理。

任务描述:
练习安全的数据访问，综合运用：
- 逻辑运算符（and, or, not）
- 短路求值特性
- if/else 分支
"""

# ============================================================
# 演示：短路求值特性
# ============================================================
print("=== 短路求值演示 ===\n")

# and 短路：第一个为假，不计算第二个
print("1. and 短路求值:")
result = False and (1 / 0)  # 不会报错，因为第一个为 False
print(f"   False and (1/0) = {result}")

# or 短路：第一个为真，不计算第二个
print("\n2. or 短路求值:")
result = True or (1 / 0)  # 不会报错，因为第一个为 True
print(f"   True or (1/0) = {result}")

# ============================================================
# 演示：安全字典访问（不使用字典）
# ============================================================
print("\n=== 安全字典访问演示 ===\n")

print("测试用例 1: name='Alice', age=30")
data_name = 'Alice'
data_age = 30
key = 'name'
default = ''
# 手动模拟安全访问逻辑
if data_name is None:
    result = default
elif key == 'name':
    result = data_name
elif key == 'age':
    result = data_age
else:
    result = default
print(f"   访问 key='{key}': '{result}'")

print("\n测试用例 2: name='Bob', age 缺失")
data_name = 'Bob'
data_age = None
key = 'age'
default = 'N/A'
# 手动模拟安全访问逻辑
if data_name is None:
    result = default
elif key == 'name':
    result = data_name
elif key == 'age':
    result = data_age if data_age is not None else default
else:
    result = default
print(f"   访问 key='{key}': '{result}'")

print("\n测试用例 3: data=None, key='name'")
data_is_none = True
key = 'name'
default = 'Unknown'
if data_is_none:
    result = default
else:
    result = f"存在 {key}"
print(f"   访问 key='{key}': '{result}'")

# ============================================================
# 演示：年龄验证（不使用数据结构）
# ============================================================
print("\n=== 年龄验证演示 ===\n")

print("测试用例 1: age=25")
age = 25
if age is None:
    result = '年龄未提供'
elif age > 150:
    result = '年龄超出合理范围'
elif age <= 0:
    result = '年龄必须大于0'
else:
    result = '有效年龄: ' + str(age)
print(f"   {result}")

print("\n测试用例 2: age=0")
age = 0
if age is None:
    result = '年龄未提供'
elif age > 150:
    result = '年龄超出合理范围'
elif age <= 0:
    result = '年龄必须大于0'
else:
    result = '有效年龄: ' + str(age)
print(f"   {result}")

print("\n测试用例 3: age=None")
age = None
if age is None:
    result = '年龄未提供'
elif age > 150:
    result = '年龄超出合理范围'
elif age <= 0:
    result = '年龄必须大于0'
else:
    result = '有效年龄: ' + str(age)
print(f"   {result}")

print("\n测试用例 4: age=150")
age = 150
if age is None:
    result = '年龄未提供'
elif age > 150:
    result = '年龄超出合理范围'
elif age <= 0:
    result = '年龄必须大于0'
else:
    result = '有效年龄: ' + str(age)
print(f"   {result}")

# ============================================================
# 演示：用户状态判断（不使用元组）
# ============================================================
print("\n=== 用户状态判断演示 ===\n")

# 测试用例 1: 未登录
is_logged_in = False
is_premium = False
has_unsaved_changes = False
if not is_logged_in:
    result = '游客'
elif is_premium:
    if has_unsaved_changes:
        result = 'VIP 用户（有未保存更改）'
    else:
        result = 'VIP 用户'
elif has_unsaved_changes:
    result = '普通用户（有未保存更改）'
else:
    result = '普通用户'
print(f"测试 1: 未登录 → {result}")

# 测试用例 2: 普通用户
is_logged_in = True
is_premium = False
has_unsaved_changes = False
if not is_logged_in:
    result = '游客'
elif is_premium:
    if has_unsaved_changes:
        result = 'VIP 用户（有未保存更改）'
    else:
        result = 'VIP 用户'
elif has_unsaved_changes:
    result = '普通用户（有未保存更改）'
else:
    result = '普通用户'
print(f"测试 2: 登录普通用户 → {result}")

# 测试用例 3: VIP 用户
is_logged_in = True
is_premium = True
has_unsaved_changes = False
if not is_logged_in:
    result = '游客'
elif is_premium:
    if has_unsaved_changes:
        result = 'VIP 用户（有未保存更改）'
    else:
        result = 'VIP 用户'
elif has_unsaved_changes:
    result = '普通用户（有未保存更改）'
else:
    result = '普通用户'
print(f"测试 3: VIP 用户 → {result}")

# 测试用例 4: VIP 用户有未保存更改
is_logged_in = True
is_premium = True
has_unsaved_changes = True
if not is_logged_in:
    result = '游客'
elif is_premium:
    if has_unsaved_changes:
        result = 'VIP 用户（有未保存更改）'
    else:
        result = 'VIP 用户'
elif has_unsaved_changes:
    result = '普通用户（有未保存更改）'
else:
    result = '普通用户'
print(f"测试 4: VIP 用户有未保存更改 → {result}")

# 测试用例 5: 普通用户有未保存更改
is_logged_in = True
is_premium = False
has_unsaved_changes = True
if not is_logged_in:
    result = '游客'
elif is_premium:
    if has_unsaved_changes:
        result = 'VIP 用户（有未保存更改）'
    else:
        result = 'VIP 用户'
elif has_unsaved_changes:
    result = '普通用户（有未保存更改）'
else:
    result = '普通用户'
print(f"测试 5: 普通用户有未保存更改 → {result}")

# ============================================================
# 思考题
# ============================================================
print("\n=== 思考题 ===")
print("1. 为什么 False and (1/0) 不会报错？")
print("2. 为什么 None or 'default' 会返回 'default'？")
print("3. 短路求值在什么场景下特别有用？")
