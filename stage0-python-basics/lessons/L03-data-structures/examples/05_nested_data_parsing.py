"""L03 示例5: 嵌套数据解析（模拟 API 响应）

学习目标:
- 防御性 .get() 链式访问
- 字典合并运算 | (Python 3.9+)
"""

# ============================================================
# 1. 模拟真实 API 响应
# ============================================================
print("=" * 50)
print("1. 真实 API 响应解析")
print("=" * 50)

api_response: dict = {
    "status": "success",
    "code": 200,
    "data": {
        "user": {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "addresses": [
                {"type": "home", "city": "Beijing", "zip": "100000"},
                {"type": "work", "city": "Shanghai", "zip": "200000"},
            ],
        },
    },
}

# ============================================================
# 2. ❌ 危险方式 vs ✅ 防御方式
# ============================================================
print("\n--- 危险 vs 防御 ---")

# ❌ 直接访问 — 嵌套深时容易 KeyError
# 用浅层数据演示：如果 key 不存在会怎样
user: dict = {"name": "Alice"}
if "name" in user:
    print(f"✅ 直接访问成功: {user['name']}")
else:
    print("❌ 直接访问失败: 缺少 'name' 键")

# ✅ 链式 .get() — 永不崩溃
safe: str = api_response.get("data", {}).get("user", {}).get("account", {}).get("balance", "0.00")
print(f"✅ 防御访问成功: {safe}")

# ============================================================
# 3. 提取嵌套字段（REPL 风格，逐行演示）
# ============================================================
print("\n--- 提取嵌套字段 ---")

# 提取用户名
name: str = api_response.get("data", {}).get("user", {}).get("name", "Unknown")
print(f"用户名: {name}")

# 提取第一个地址城市
addresses: list[dict] = api_response.get("data", {}).get("user", {}).get("addresses", [])
if addresses:
    city: str = addresses[0].get("city", "Unknown")
else:
    city = "No Address"
print(f"第一地址城市: {city}")

# 空响应不崩溃
empty_response: dict = {}
name_empty: str = empty_response.get("data", {}).get("user", {}).get("name", "Unknown")
print(f"空响应用户名: {name_empty}")

# ============================================================
# 4. 字典合并运算 | (Python 3.9+)
# ============================================================
print("\n--- 字典合并 ---")

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

assert merged == {"timeout": 60, "retries": 3, "debug": True}
assert defaults == {"timeout": 30, "retries": 3, "debug": False}  # 原字典不变
print(f"✅ 合并结果: {merged}")
print(f"✅ defaults 未被修改: {defaults}")

print("\n🎉 全部演示完成！")
