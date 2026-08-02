"""字典操作与安全访问示例。

演示字典的创建、访问、修改、删除，以及 .get() 安全访问的重要性。
"""

# 创建字典
print("=== 字典创建 ===")
user: dict[str, str | int] = {
    "name": "Alice",
    "age": 25,
    "city": "Beijing",
}
print(f"用户信息: {user}")

# 访问值（两种方式对比）
print("\n=== 访问值 ===")
name: str | int = user["name"]
print(f"直接访问 user['name']: {name}")

# 使用 .get() 提供默认值（推荐）
age: str | int = user.get("age", 0)
print(f"user.get('age', 0): {age}")

score: str | int = user.get("score", 0)
print(f"user.get('score', 0): {score} (键不存在，返回默认值)")

# 修改和新增
print("\n=== 修改和新增 ===")
user["age"] = 26
print(f"修改年龄后: {user}")

user["email"] = "alice@example.com"
print(f"新增邮箱后: {user}")

# 删除键值对
print("\n=== 删除键值对 ===")
removed_city: str | int = user.pop("city")
print(f"删除的城市: {removed_city}")
print(f"删除后: {user}")

# 遍历字典
print("\n=== 遍历字典 ===")
print("遍历键:")
for key in user.keys():
    print(f"  {key}")

print("\n遍历值:")
for value in user.values():
    print(f"  {value}")

print("\n遍历键值对:")
for key, value in user.items():
    print(f"  {key}: {value}")

# .get() vs 直接访问的安全性对比
print("\n=== 安全性对比 ===")
config: dict[str, str] = {"host": "localhost", "port": "8000"}

# ❌ 危险：键不存在会崩溃
print("直接访问不存在的键会报错:")
print("timeout = config['timeout']  # KeyError: 'timeout'")

# ✅ 安全：提供默认值
timeout: str = config.get("timeout", "30")
print(f"使用 .get() 安全访问: timeout = {timeout}")
