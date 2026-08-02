"""L01 示例6: 类型注解

类型注解（Type Hints）是 Python 3.5+ 引入的特性，用于标注变量的预期类型。
注解不影响代码运行，仅作为文档和工具提示。

"""

# ===== 1. 基本类型注解 =====
print("=== 1. 基本类型注解 ===")

name: str = "Alice"
age: int = 25
height: float = 1.75
is_active: bool = True

print(f"name      : {name}   (str)")
print(f"age       : {age}    (int)")
print(f"height    : {height} (float)")
print(f"is_active : {is_active} (bool)")

# ===== 2. 类型注解不影响运行 =====
print("\n=== 2. 类型注解不影响运行 ===")

# 故意写错类型，Python 不会报错
name: str = 123  # 注解说 str，实际是 int
print(f"类型注解 name: str = 123，但 Python 不报错: {name}")
print(f"type(name) = {type(name)}")

# ===== 3. None 类型注解 =====
print("\n=== 3. None 类型注解 ===")

empty_value: None = None
print(f"empty_value: None = {empty_value}")

# ===== 4. 组合类型 str | int =====
print("\n=== 4. 组合类型（联合类型）===")

# 变量可以是字符串或整数
user_id: str | int = "U001"
print(f"user_id (str | int) = {user_id}   type = {type(user_id)}")

user_id = 1001
print(f"user_id (str | int) = {user_id}   type = {type(user_id)}")

# ===== 5. 为什么要用类型注解？=====
print("\n=== 5. 类型注解的作用 ===")
print("1. IDE 提供更好的代码补全（如 VS Code）")
print("2. 他人阅读代码时快速理解变量意图")
print("3. mypy 等工具可在运行前发现类型错误")
print("4. 代码即文档，无需额外注释")

# ===== 6. 变量引用与类型的关系 =====
print("\n=== 6. 变量是引用，类型随对象变化 ===")

data: int | str = 42
print(f"data = {data}   type = {type(data)}")

data = "hello"
print(f"data = {data!r}   type = {type(data)}")
