"""L02 示例7: for 循环

学习目标:
- 掌握 for 循环的基本用法
- 使用 range() 生成数字序列
- 使用 enumerate() 同时获取索引和值
- 嵌套循环

【知识点边界】本文件仅使用 L01 + L02 的知识点：
- print, input, if/elif/else, for, while
- range(), enumerate()
"""

# 1. 遍历字符串（字符串是 L01 的知识点）
print("遍历字符串:")
text = "Python"
for char in text:
    print(char, end=" ")
print()

# 2. range()
print("\n1到5:")
for i in range(1, 6):
    print(i, end=" ")

# 3. enumerate() - 同时获取索引和值
print("\n\n带索引:")
text = "Hi"
for idx, char in enumerate(text):
    print(f"{idx}: {char}")

# 4. 嵌套循环
print("\n九九乘法表:")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i}×{j}={i * j}", end=" ")
    print()
