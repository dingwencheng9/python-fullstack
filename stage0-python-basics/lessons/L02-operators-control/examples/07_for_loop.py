"""L02 示例7: for 循环"""

# 1. 遍历列表

fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(fruit)

# 2. range()
print("\n1到5:")
for i in range(1, 6):
    print(i, end=" ")

# 3. enumerate()
print("\n\n带索引:")
for idx, fruit in enumerate(fruits):
    print(f"{idx}: {fruit}")

# 4. 嵌套循环
print("\n九九乘法表:")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i}×{j}={i * j}", end=" ")
    print()
