"""L03 示例2: 字典操作"""

# 1. 创建字典
person = {"name": "Alice", "age": 20, "city": "Beijing"}

# 2. 访问元素
print(f"姓名: {person['name']}")
print(f"年龄: {person.get('age')}")

# 3. 添加/修改
person["email"] = "alice@example.com"
person["age"] = 21

# 4. 删除
del person["city"]
email = person.pop("email")

# 5. 遍历
for key, value in person.items():
    print(f"{key}: {value}")

# 6. 字典推导式
squares = {x: x**2 for x in range(5)}
print(f"字典: {squares}")
