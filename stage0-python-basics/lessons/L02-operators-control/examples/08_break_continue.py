"""L02 示例8: break 和 continue。

学习目标:
- 使用 break 提前结束循环
- 使用 continue 跳过本轮循环
- 理解二者在搜索、过滤和输入校验中的常见用法

【知识点边界】本文件仅使用 L01 + L02 的知识点：
- print, input, if/elif/else, for, while
- break, continue, range
"""

print("=" * 50)
print("1. break: 找到目标后提前退出")
print("=" * 50)

# 使用字符串演示（字符串是 L01 的知识点）
text = "Py3.8"  # 查找第一个数字
found_digit = False

for char in text:
    if char.isdigit():
        found_digit = True
        print(f"第一个数字: '{char}'")
        break

if not found_digit:
    print("没有找到数字")

print("\n" + "=" * 50)
print("2. continue: 跳过不需要的数据")
print("=" * 50)

# 使用 range() 演示：跳过某些数字
print("打印 1-5，但跳过 3:")
for i in range(1, 6):
    if i == 3:
        continue
    print(f"  {i}")

print("\n" + "=" * 50)
print("3. break + continue 组合")
print("=" * 50)

# 使用字符串演示：处理到某个字符为止
text = "Hello_World"
print("处理有效字符（遇到下划线停止）:")
for char in text:
    if char == "_":
        print("  遇到下划线，退出循环")
        break
    print(f"  处理: {char}")

print("\n" + "=" * 50)
print("4. while 中的 break")
print("=" * 50)

count = 0
while True:
    count += 1
    if count == 3:
        print("count 到达 3，退出循环")
        break
    print(f"  count = {count}")

print("\n💡 经验法则")
print("- break: 已经得到答案，不需要继续循环")
print("- continue: 当前数据不合格，跳过本轮处理")

print("\n🎉 break/continue 示例完成！")
