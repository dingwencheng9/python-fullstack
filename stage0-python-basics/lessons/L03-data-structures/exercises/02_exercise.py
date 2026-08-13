"""L03 练习2: JSON 响应解析

难度: ⭐⭐☆ (中等)
预计时间: 20 分钟
知识点: 字典访问、嵌套数据结构、默认值处理

学习方式:
本练习是"演示型练习"——代码已经完整实现，
你需要运行它，观察输出，理解代码的工作原理。

任务描述:
练习从 API 响应中提取数据，综合运用：
- 字典的安全访问（get 方法）
- 嵌套字典的遍历
- 默认值处理

提示:
1. 使用 'key' in dict 检查键是否存在
2. 使用 dict.get(key, default) 提供默认值
3. 注意嵌套结构的访问路径
"""

# ============================================================
# 演示：安全获取嵌套字典值
# ============================================================
print("=== 安全获取嵌套字典值演示 ===\n")

# 测试用例：模拟 API 响应
test_responses = [
    {'user': {'name': 'Alice', 'age': 25}},
    {'user': {}},
    {},
    {'user': {'name': 'Bob'}},
]

print("从嵌套字典中获取用户名:")
for response in test_responses:
    # 安全获取用户名的逻辑
    if 'user' in response:
        user = response['user']
        if isinstance(user, dict) and 'name' in user:
            user_name = user['name']
        else:
            user_name = 'Unknown'
    else:
        user_name = 'Unknown'
    print(f"  {response} → '{user_name}'")

# ============================================================
# 演示：分页响应处理
# ============================================================
print("\n=== 分页响应处理演示 ===\n")

pagination_tests = [
    {'pagination': {'total': 100, 'page': 1}},
    {'pagination': {}},
    {},
    {'pagination': {'total': 42}},
]

print("从分页响应中获取总数:")
for response in pagination_tests:
    # 安全获取总数的逻辑
    if 'pagination' in response:
        pagination = response['pagination']
        if isinstance(pagination, dict):
            total = pagination.get('total', 0)
        else:
            total = 0
    else:
        total = 0
    print(f"  {response} → total={total}")

# ============================================================
# 演示：配置合并
# ============================================================
print("\n=== 配置合并演示 ===\n")

defaults = {'timeout': 30, 'retries': 3, 'debug': False}
print(f"默认配置: {defaults}")

user_configs = [
    {'timeout': 60},
    {'debug': True},
    {},
    {'retries': 5, 'verbose': True},
]

print("\n用户配置合并:")
for user_config in user_configs:
    # 合并配置的逻辑
    result = defaults.copy()
    for key, value in user_config.items():
        result[key] = value
    print(f"  用户: {user_config}")
    print(f"  合并后: {result}")

# ============================================================
# 演示：字典的常用操作
# ============================================================
print("\n=== 字典常用操作演示 ===\n")

person = {'name': 'Alice', 'age': 30, 'city': 'Beijing'}

print(f"原始字典: {person}")
print(f"  获取 'name': {person.get('name')}")
print(f"  获取 'email'（不存在）: {person.get('email', 'N/A')}")
print(f"  所有键: {list(person.keys())}")
print(f"  所有值: {list(person.values())}")
print(f"  所有项: {list(person.items())}")
print("  更新: person.update({'age': 31})")
person.update({'age': 31})
print(f"  更新后: {person}")

# ============================================================
# 思考题
# ============================================================
print("\n=== 思考题 ===")
print("1. dict.get('key') 和 dict['key'] 有什么区别？")
print("2. 如何安全地获取嵌套字典中的值而不会抛出异常？")
print("3. 字典的 copy() 和直接赋值有什么区别？")
