"""L02 示例4: 赋值运算符。

学习目标:
- 掌握普通赋值和增强赋值
- 理解变量重新绑定与就地更新的区别
- 使用海象运算符 := 简化条件中的赋值
"""

print("=" * 50)
print("1. 普通赋值")
print("=" * 50)

x = 10
name = "Alice"
is_active = True

print(f"x = {x}")
print(f"name = {name}")
print(f"is_active = {is_active}")

print("\n" + "=" * 50)
print("2. 多变量赋值")
print("=" * 50)

a, b, c = 1, 2, 3
print(f"a={a}, b={b}, c={c}")

# 交换变量不需要临时变量
left = "左"
right = "右"
left, right = right, left
print(f"交换后: left={left}, right={right}")

print("\n" + "=" * 50)
print("3. 增强赋值")
print("=" * 50)

count = 10
print(f"初始 count = {count}")

count += 5
print(f"count += 5  -> {count}")

count -= 3
print(f"count -= 3  -> {count}")

count *= 2
print(f"count *= 2  -> {count}")

count //= 4
print(f"count //= 4 -> {count}")

count %= 3
print(f"count %= 3  -> {count}")

print("\n" + "=" * 50)
print("4. 可变对象的增强赋值")
print("=" * 50)

items = ["Python"]
alias = items
items += ["FastAPI"]

print(f"items = {items}")
print(f"alias = {alias}")
print("列表是可变对象，items += [...] 会原地扩展列表")

print("\n" + "=" * 50)
print("5. 海象运算符 :=")
print("=" * 50)

text = "Python"
if (length := len(text)) > 5:
    print(f"{text} 长度为 {length}，超过 5")
else:
    print(f"{text} 长度为 {length}，不超过 5")

# 常见用途：在条件判断中复用计算结果
numbers = [3, 5, 8, 13]
if (total := sum(numbers)) > 20:
    print(f"总和 {total} 大于 20")

print("\n🎉 赋值运算符示例完成！")
