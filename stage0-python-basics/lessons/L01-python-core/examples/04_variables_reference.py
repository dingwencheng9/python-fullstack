"""L01 示例4: 变量与引用

Python 的变量是"对象的标签"，不是"装值的盒子"。
同一个对象可以有多个标签（变量名）。

"""

# ===== 1. 变量是引用 =====
print("=== 1. 变量是引用 ===")
name = "Alice"  # 创建字符串对象，name 指向它
print(f"name = {name}")
print(f"id(name) = {id(name)}")

# ===== 2. 多个变量指向同一对象 =====
print("\n=== 2. 字符串别名（引用同一对象）===")
original = "hello"
alias = original  # alias 也指向同一个字符串对象
print(f"original = {original!r}")
print(f"alias = original  →  alias = {alias!r}")
print(f"id(original) = {id(original)}")
print(f"id(alias)   = {id(alias)}")
print(f"original is alias: {original is alias}")  # True：指向同一对象
print(f"original == alias: {original == alias}")  # True：值相等

# ===== 3. 重新赋值创建新对象 =====
print("\n=== 3. 重新赋值创建新对象 ===")
a = "hello"
b = a  # b 指向 a 指向的对象
print("a = 'hello', b = a 后:")
print(f"a = {a}")
print(f"b = {b}")
a = "world"  # 重新赋值，a 指向新对象，b 不受影响
print("a = 'world' 后:")
print(f"a = {a}  （指向新对象）")
print(f"b = {b}  （仍指向原来的 'hello'）")
print(f"a is b: {a is b}")  # False
print()
print("💡 预告：L03 会学到 list/dict/set 等可变对象，它们的修改行为与字符串/整数不同。")
