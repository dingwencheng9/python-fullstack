"""L03 示例3: 集合和元组"""

# 1. 集合 - 去重
nums = [1, 2, 2, 3, 3, 3]
unique = set(nums)
print(f"去重: {unique}")

# 2. 集合运算
a = {1, 2, 3}
b = {2, 3, 4}
print(f"并集: {a | b}")
print(f"交集: {a & b}")
print(f"差集: {a - b}")

# 3. 元组 - 不可变
point = (10, 20)
x, y = point
print(f"坐标: ({x}, {y})")

# 4. 集合推导式
squares = {x**2 for x in range(5)}
print(f"集合: {squares}")
