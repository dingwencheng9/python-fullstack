"""L01 示例6: 类型注解

类型注解（Type Hints）是 Python 3.5+ 引入的特性，用于标注预期类型。
本课重点：函数签名（参数和返回值）的类型注解。

> 💡 提示：局部变量通常依赖类型推导，过度标注会增加冗余。
> 函数签名是类型注解的主要用武之地。

"""

# ===== 1. 函数签名类型注解（重点！）=====
print("=== 1. 函数签名类型注解（推荐）===")

# ✅ 推荐：函数参数和返回值加类型注解
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> str:
    return f"Hello, {name}!"

def calculate_area(width: float, height: float) -> float:
    return width * height

print(f"add(1, 2) = {add(1, 2)}")
print(f"greet('Alice') = {greet('Alice')}")
print(f"calculate_area(3.0, 4.0) = {calculate_area(3.0, 4.0)}")

# ===== 2. 局部变量类型注解（可选，仅作文档用途）=====
print("\n=== 2. 局部变量类型注解（可选）===")

# 局部变量可以不标注，Python 会自动推导
name = "Alice"  # Python 推导出 str
age = 25        # Python 推导出 int

# 如果希望显式标注（仅用于文档目的），可以这样：
name_explicit: str = "Bob"  # 这与 name = "Bob" 效果相同

print(f"name = {name}, age = {age}")
print(f"name_explicit: str = {name_explicit}")

# ===== 3. 类型注解不影响运行 =====
print("\n=== 3. 类型注解不影响运行 ===")

# 故意写错类型，Python 不会报错
name_wrong: str = 123  # 注解说 str，实际是 int
print(f"类型注解 name: str = 123，但 Python 不报错: {name_wrong}")
print(f"type(name_wrong) = {type(name_wrong)}")

# ===== 4. 组合类型 str | int =====
print("\n=== 4. 组合类型（联合类型）===")

# 函数参数可以是字符串或整数
def process_id(user_id: str | int) -> str:
    return f"User ID: {user_id}"

print(f"process_id('U001') = {process_id('U001')}")
print(f"process_id(1001) = {process_id(1001)}")

# ===== 5. 为什么要用类型注解？=====
print("\n=== 5. 类型注解的作用 ===")
print("1. 函数签名：参数和返回值是最重要的标注点")
print("2. IDE 提供更好的代码补全（如 VS Code）")
print("3. 他人阅读代码时快速理解函数意图")
print("4. mypy 等工具可在运行前发现类型错误")

# ===== 6. None 类型注解 =====
print("\n=== 6. None 类型注解 ===")

def no_return() -> None:
    """这个函数不返回任何值"""
    print("Hello from no_return!")

result = no_return()
print(f"no_return() 返回: {result}")  # None
