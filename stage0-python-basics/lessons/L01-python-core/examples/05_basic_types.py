"""L01 示例5: 基本数据类型

覆盖 5 种基本类型：int / float / str / bool / None。

"""

# ===== 1. 整数 int =====
print("=== 1. 整数 int ===")
count = 42
negative = -10
zero = 0
big_number = 10**100  # Python 支持任意精度整数

print(f"count    = {count}")  # 42
print(f"negative = {negative}")  # -10
print(f"zero     = {zero}")  # 0
print(f"big_number = 10**100 = {big_number}")  # 1 后面跟 100 个零

# ===== 2. 浮点数 float =====
print("\n=== 2. 浮点数 float ===")
pi = 3.14159
temperature = 36.6
avogadro = 6.02e23  # 科学计数法：6.02 × 10²³
small = 1e-5  # 0.00001

print(f"pi         = {pi}")
print(f"temperature = {temperature}")
print(f"avogadro   = {avogadro}")
print(f"small      = {small}")

# ⚠️ 浮点数精度问题（二进制无法精确表示 0.1）
result = 0.1 + 0.2
print(f"\n0.1 + 0.2 = {result}")  # 输出：0.30000000000000004

# ===== 3. 字符串 str =====
print("\n=== 3. 字符串 str ===")
greeting = "Hello, World!"
single_quoted = "Python is fun"
multiline = """这是
一个多行
字符串"""

print(f"greeting     = {greeting}")
print(f"single_quoted = {single_quoted}")
print(f"multiline    = {multiline!r}")

# 转义字符
path = "C:\\Users\\Name"  # \\ 表示反斜杠本身
print(f"path = {path}")

# 原始字符串（r-string，原样输出）
raw_path = r"C:\Users\Name"
print(f"raw_path = {raw_path}")

# ===== 4. 布尔值 bool =====
print("\n=== 4. 布尔值 bool ===")
is_valid = True
is_empty = False

# 布尔值通常来自比较运算
result = 10 > 5  # True
is_equal = 3 == 3  # True（== 是相等比较）
is_different = 3 != 3  # False（!= 是不等比较）

print(f"is_valid      = {is_valid}")
print(f"is_empty      = {is_empty}")
print(f"10 > 5        = {result}")
print(f"3 == 3        = {is_equal}")
print(f"3 != 3        = {is_different}")

# ===== 5. None 类型 =====
print("\n=== 5. None 类型 ===")
nothing = None
print(f"nothing = {nothing}")

# ===== 6. type() 检查类型 =====
print("\n=== 6. type() 检查类型 ===")
num = 42
pi = 3.14
name = "Python"
flag = True
empty = None

print(f"type({num})    = {type(num)}")
print(f"type({pi})    = {type(pi)}")
print(f"type({name!r}) = {type(name)}")
print(f"type({flag})   = {type(flag)}")
print(f"type({empty})  = {type(empty)}")

# ===== 7. 类型判断回顾 =====
print("\n=== 7. 类型判断 ===")
print("💡 判断变量类型，用 type() 函数:")
num = 42
pi = 3.14
name = "Python"
flag = True
empty = None

print(f"type({num})    = {type(num)}")
print(f"type({pi})    = {type(pi)}")
print(f"type({name!r}) = {type(name)}")
print(f"type({flag})   = {type(flag)}")
print(f"type({empty})  = {type(empty)}")

print("\n💡 更精确的类型判断方法在 L03 数据结构中学习。")
