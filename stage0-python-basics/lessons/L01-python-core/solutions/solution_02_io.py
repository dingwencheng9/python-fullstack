"""L01 参考答案 2: 交互式输入输出

对应练习: exercises/02_io_practice.py
知识点: input()、int()、f-string 格式化

"""

# 1. 获取用户姓名
name = input("请输入你的姓名：")

# 2. 获取用户年龄
age_str = input("请输入你的年龄：")
age = int(age_str)  # 转换为整数

# 3. 输出问候语
print(f"你好，{name}！你今年 {age} 岁。")

# 4. 获取两个数字
num1 = int(input("请输入第一个数字："))
num2 = int(input("请输入第二个数字："))

# 5. 计算并输出结果
# 注意：此处假设 num2 不为 0，L02 将学习如何处理除数为零的情况
print(f"{num1} + {num2} = {num1 + num2}")
print(f"{num1} - {num2} = {num1 - num2}")
print(f"{num1} * {num2} = {num1 * num2}")
print(f"{num1} / {num2} = {num1 / num2}")
