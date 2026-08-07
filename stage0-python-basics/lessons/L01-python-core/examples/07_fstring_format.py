"""L01 示例7: f-string 字符串格式化

f-string（格式化字符串字面量）是 Python 3.6+ 推荐的字符串格式化方式，
简洁、高效、可读性强。Python 3.13 中 f-string 性能进一步提升。

"""

# ===== 1. 基本 f-string =====
print("=== 1. 基本 f-string ===")

name = "Alice"
age = 25

message = f"我是 {name}，今年 {age} 岁"
print(message)

# ===== 2. 表达式 =====
print("\n=== 2. 表达式 ===")

print(f"明年我 {age + 1} 岁")
print(f"10 年后我 {age + 10} 岁")
print(f"姓名长度: {len(name)}")
print(f"姓名大写: {name.upper()}")

# ===== 3. 格式化数字 =====
print("\n=== 3. 格式化数字 ===")

pi = 3.14159265359
price = 99.5

print(f"π = {pi:.2f}")  # 保留 2 位小数
print(f"π = {pi:.4f}")  # 保留 4 位小数
print(f"价格: ¥{price:.2f}")

# ===== 4. 对齐和填充 =====
print("\n=== 4. 对齐和填充 ===")

text = "Python"

print(f"|{text:>10}|")  # 右对齐，宽度 10
print(f"|{text:<10}|")  # 左对齐，宽度 10
print(f"|{text:^10}|")  # 居中，宽度 10
print(f"|{text:*^10}|")  # 居中，用 * 填充

# ===== 5. 千位分隔符 =====
print("\n=== 5. 千位分隔符 ===")

big_num = 1000000
print(f"数字: {big_num:,}")  # 1,000,000
print(f"数字: {big_num:_}")  # 1_000_000

# ===== 6. 百分比 =====
print("\n=== 6. 百分比 ===")

ratio = 0.856
print(f"比例: {ratio:.1%}")  # 85.6%
print(f"比例: {ratio:.2%}")  # 85.60%

# ===== 7. Python 3.8+ 调试模式 =====
print("\n=== 7. 调试模式（=）===")

x = 100
y = 200

# = 符号会同时显示变量名和值，方便调试
print(f"{x=}")
print(f"{y=}")
print(f"{x + y=}")
print(f"{x * y=}")
print(f"{x / y=:.4f}")

# ===== 8. 多行 f-string =====
print("\n=== 8. 多行 f-string ===")

name = "Bob"
age = 30
city = "北京"

info = f"""
姓名: {name}
年龄: {age}
城市: {city}
"""
print(info)

# ===== 9. f-string vs 其他格式化方式对比 =====
print("=== 9. f-string vs 其他方式 ===")

name = "Alice"
age = 25

# ✅ 推荐：f-string（清晰、高效）
print(f"f-string: 我是 {name}，今年 {age} 岁")

# ❌ 不推荐：字符串拼接（冗长、易错）
print("字符串拼接: 我是 " + name + "，今年 " + str(age) + " 岁")

# ❌ 不推荐：% 格式化（老旧，已废弃）
# 注意：% 格式化需要元组来传递多个值
# name, age = "Alice", 25  # 这在 L02 会学到
# print("% 格式化: 我是 %s，今年 %d 岁" % (name, age))
print("% 格式化示例: '我是 %s，今年 %d 岁' % ('Alice', 25)")
print("（%s 表示字符串，%d 表示整数，元组在 L02 才学）")

# ❌ 不推荐：.format()（冗长）
print(".format(): 我是 {}，今年 {} 岁".format(name, age))  # noqa: US032
