"""L02 示例6: while 循环和控制语句"""

# 1. 基本 while

count = 0
while count < 3:
    print(f"count: {count}")
    count += 1

# 2. break - 提前退出
print("\nbreak 示例:")
i = 0
while True:
    if i >= 3:
        break
    print(i)
    i += 1

# 3. continue - 跳过本次
print("\ncontinue 示例:")
for i in range(5):
    if i == 2:
        continue
    print(i)

# 4. while-else
print("\nwhile-else:")
n = 0
while n < 3:
    print(n)
    n += 1
print("循环结束")
