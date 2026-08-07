"""L03 示例3: 字典操作与安全访问

学习目标:
- 掌握字典的创建、访问、修改、删除
- 理解 .get() 安全访问的重要性
- 防御性嵌套数据解析
- 字典合并运算符 | (Python 3.9+)

【知识点边界】本文件仅使用 L01 + L02 + L03 的知识点：
- print, for, range, if
- list, dict
- 字典操作、安全访问、遍历
"""

from typing import Any


# ============================================================
# 1. 创建字典
# ============================================================
print("=" * 50)
print("1. 字典创建")
print("=" * 50)

user: dict[str, str | int] = {
    "name": "Alice",
    "age": 25,
    "city": "Beijing",
}
print(f"用户信息: {user}")

# 使用 dict() 构造
person = dict(name="Bob", age=30)
print(f"dict() 构造: {person}")


# ============================================================
# 2. 访问值（直接访问 vs 安全访问）
# ============================================================
print("\n" + "=" * 50)
print("2. 访问值：直接访问 vs 安全访问")
print("=" * 50)

# 直接访问（键不存在会报错）
name: str | int = user["name"]
print(f"直接访问 user['name']: {name}")

# 使用 .get() 提供默认值（推荐）
age: str | int = user.get("age", 0)
print(f"user.get('age', 0): {age}")

# 访问不存在的键（返回默认值，不报错）
score: str | int = user.get("score", 0)
print(f"user.get('score', 0): {score} (键不存在，返回默认值)")


# ============================================================
# 3. 修改和新增
# ============================================================
print("\n" + "=" * 50)
print("3. 修改和新增")
print("=" * 50)

user["age"] = 26
print(f"修改年龄后: {user}")

user["email"] = "alice@example.com"
print(f"新增邮箱后: {user}")


# ============================================================
# 4. 删除键值对
# ============================================================
print("\n" + "=" * 50)
print("4. 删除键值对")
print("=" * 50)

removed_city: str | int = user.pop("city")
print(f"删除的城市: {removed_city}")
print(f"删除后: {user}")


# ============================================================
# 5. 遍历字典
# ============================================================
print("\n" + "=" * 50)
print("5. 遍历字典")
print("=" * 50)

print("遍历键:")
for key in user.keys():
    print(f"  {key}")

print("\n遍历值:")
for value in user.values():
    print(f"  {value}")

print("\n遍历键值对:")
for key, value in user.items():
    print(f"  {key}: {value}")


# ============================================================
# 6. 安全性对比
# ============================================================
print("\n" + "=" * 50)
print("6. 安全性对比")
print("=" * 50)

config: dict[str, str] = {"host": "localhost", "port": "8000"}

# ❌ 危险：键不存在会崩溃
print("直接访问不存在的键会报错:")
print("timeout = config['timeout']  # KeyError: 'timeout'")

# ✅ 安全：提供默认值
timeout: str | None = config.get("timeout", "30")
print(f"使用 .get() 安全访问: timeout = {timeout}")


# ============================================================
# 7. 嵌套数据解析（模拟 API 响应）
# ============================================================
print("\n" + "=" * 50)
print("7. 嵌套数据解析（防御性访问）")
print("=" * 50)

api_response: dict[str, Any] = {
    "status": "success",
    "code": 200,
    "data": {
        "user": {
            "id": 1,
            "name": "Alice",
            "addresses": [
                {"type": "home", "city": "Beijing"},
            ],
        },
    },
}

# 提取用户名（防御性链式访问）
name: str = api_response.get("data", {}).get("user", {}).get("name", "Unknown")
print(f"用户名: {name}")

# 提取第一个地址城市
addresses: list[dict[str, str]] = api_response.get("data", {}).get("user", {}).get("addresses", [])
if addresses:
    city: str = addresses[0].get("city", "Unknown")
else:
    city = "No Address"
print(f"第一地址城市: {city}")

# 空响应不崩溃
empty_response: dict[str, Any] = {}
name_empty: str = empty_response.get("data", {}).get("user", {}).get("name", "Unknown")
print(f"空响应用户名: {name_empty}")


# ============================================================
# 8. 字典合并运算 | (Python 3.9+)
# ============================================================
print("\n" + "=" * 50)
print("8. 字典合并运算 |")
print("=" * 50)

defaults: dict[str, int | bool] = {
    "timeout": 30,
    "retries": 3,
    "debug": False,
}

user_config: dict[str, int | bool] = {
    "timeout": 60,
    "debug": True,
}

# | 运算符 — 返回新字典，不修改原字典
merged: dict[str, int | bool] = defaults | user_config

print(f"✅ 合并结果: {merged}")
print(f"✅ defaults 未被修改: {defaults}")


# ============================================================
# 9. 字典推导式
# ============================================================
print("\n" + "=" * 50)
print("9. 字典推导式")
print("=" * 50)

# 数字 → 平方的字典
squares_dict = {x: x**2 for x in range(5)}
print(f"数字→平方: {squares_dict}")

# 字符串 → 长度的字典
words = ["apple", "banana", "cherry"]
word_lengths = {word: len(word) for word in words}
print(f"单词→长度: {word_lengths}")

# 交换键值对
swapped = {v: k for k, v in word_lengths.items()}
print(f"交换键值: {swapped}")


print("\n✅ 全部演示完成！")
