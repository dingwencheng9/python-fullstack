"""L01 示例3: 输入与输出 - input() 和 print() 函数

演示如何接收用户输入并输出结果。

"""

print("===== Python 输入输出示例 =====\n")

# 示例 1: 基本输入输出
print("--- 示例 1: 基本输入输出 ---")
# input() 会阻塞等待用户输入，输入后回车确认
name = input("请输入你的名字: ")  # 等用户输入
print(f"你好, {name}!")
print()

# 示例 2: 多次输入
print("--- 示例 2: 多次输入 ---")
first_name = input("请输入你的名: ")
last_name = input("请输入你的姓: ")
# 字符串可以直接用 + 拼接
print(f"你好, {last_name}{first_name}!")
print()

# 示例 3: f-string 组合多变量
print("--- 示例 3: f-string 格式化 ---")
city = input("请输入你的城市: ")
hobby = input("请输入你的爱好: ")
print(f"你来自 {city}，喜欢 {hobby}。")
print()

# 示例 4: 输入数字（input 返回字符串，需要 int 转换）
print("--- 示例 4: 输入数字 ---")
age_str = input("请输入你的年龄: ")
age = int(age_str)  # 字符串 → 整数
next_year = age + 1
print(f"明年你将 {next_year} 岁")
print()

# 示例 5: 一行完成输入和转换
print("--- 示例 5: 一行转换 ---")
birth_year = int(input("请输入你的出生年份: "))
current_year = 2026
calculated_age = current_year - birth_year
print(f"你大约 {calculated_age} 岁")
print()

# 示例 6: print() 的高级用法
print("--- 示例 6: print() 高级用法 ---")

# 多个参数，默认用空格分隔
print("Apple", "Banana", "Cherry")

# 自定义分隔符
print("Apple", "Banana", "Cherry", sep=", ")

# 自定义结束符（end 参数控制末尾字符，默认是换行）
print("Hello", end=" ")
print("World")  # 接着上一行输出，不换行

# 同时使用多个参数
print("A", "B", "C", sep=" | ", end=" <-- 结束\n")
print()

# 示例 7: 综合应用 - 个人信息登记
print("--- 示例 7: 综合应用 ---")
print("=== 个人信息登记 ===")
name = input("姓名: ")
age = int(input("年龄: "))  # 直接在 input 外层套 int()
city = input("城市: ")
hobby = input("爱好: ")

print("\n=== 登记结果 ===")
print(f"姓名: {name}")
print(f"年龄: {age} 岁")
print(f"城市: {city}")
print(f"爱好: {hobby}")
print("\n登记完成！ ✅")
