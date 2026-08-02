"""L03 示例1: 列表操作"""

# 1. 创建列表
nums = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "orange"]

# 2. 访问元素
print(f"第一个: {fruits[0]}")
print(f"最后一个: {fruits[-1]}")

# 3. 切片
print(f"前两个: {fruits[:2]}")
print(f"后两个: {fruits[-2:]}")

# 4. 增加元素
fruits.append("grape")
fruits.insert(1, "kiwi")

# 5. 删除元素
fruits.remove("banana")
last = fruits.pop()

# 6. 列表推导式
squares = [x**2 for x in range(5)]
print(f"平方: {squares}")

evens = [x for x in range(10) if x % 2 == 0]
print(f"偶数: {evens}")
