"""L02 示例8: break 和 continue。

学习目标:
- 使用 break 提前结束循环
- 使用 continue 跳过本轮循环
- 理解二者在搜索、过滤和输入校验中的常见用法
"""

print("=" * 50)
print("1. break: 找到目标后提前退出")
print("=" * 50)

numbers = [3, 7, 11, 14, 19, 22]
first_even = None

for number in numbers:
    if number % 2 == 0:
        first_even = number
        break

print(f"第一个偶数: {first_even}")

print("\n" + "=" * 50)
print("2. continue: 跳过不需要的数据")
print("=" * 50)

values = [10, 0, 5, 0, 2]
reciprocals = []

for value in values:
    if value == 0:
        continue
    reciprocals.append(1 / value)

print(f"跳过 0 后的倒数: {reciprocals}")

print("\n" + "=" * 50)
print("3. break + continue 组合")
print("=" * 50)

records = ["", "alice", "bob", "STOP", "carol"]
valid_names = []

for record in records:
    if not record:
        continue  # 跳过空字符串
    if record == "STOP":
        break  # 遇到停止标记后结束循环
    valid_names.append(record.title())

print(f"有效姓名: {valid_names}")

print("\n" + "=" * 50)
print("4. while 中的 break")
print("=" * 50)

count = 0
while True:
    count += 1
    if count == 3:
        print("count 到达 3，退出循环")
        break

print("\n💡 经验法则")
print("- break: 已经得到答案，不需要继续循环")
print("- continue: 当前数据不合格，跳过本轮处理")
print("\n🎉 break/continue 示例完成！")
