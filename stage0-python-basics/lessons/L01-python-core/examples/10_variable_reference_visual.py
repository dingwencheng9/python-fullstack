"""L01 示例10: 变量引用模型可视化

用代码可视化"变量是标签，不是盒子"的概念。
对应 lesson.md 第 2.1 节，配合引用模型 Mermaid 图阅读效果最佳。

> ⚠️ **拓展内容**：本文件通过重新赋值场景展示字符串/整数的不可变性，
>   初学者可先跳过"字符串别名"场景（L03 才会系统学习 list/dict 等可变类型）。
>   核心理解：整数和字符串不可变，重新赋值不影响其他标签。

"""

print("=" * 60)
print("  变量引用模型 — 可视化演示")
print("=" * 60)

# ---------------------------------------------------------------
# 场景 1：字符串的不可变性 — 重新赋值不影响原对象
# ---------------------------------------------------------------
print("\n【场景 1】字符串不可变：重新赋值不影响其他标签")
print("-" * 40)

original = "hello"
alias = original  # alias 成为 original 的另一个标签

print(f"  original = {original!r}")
print("  alias    = original")
print(f"  original == alias: {original == alias}  ← 值相等")

original = "world"  # original 重新指向新对象

print("\n  执行 original = 'world' 后：")
print(f"  original = {original!r}  ← 标签换到新对象")
print(f"  alias    = {alias!r}     ← alias 不受影响（字符串不可变）")
print(f"  original == alias: {original == alias}  ← False")


# ---------------------------------------------------------------
# 场景 2：整数不可变 — 重新赋值不影响其他标签
# ---------------------------------------------------------------
print("\n【场景 2】整数不可变：重新赋值不影响其他标签")
print("-" * 40)

count = 100
backup = count  # backup 成为 count 的另一个标签

print(f"  count  = {count}")
print("  backup = count")
print(f"  count == backup: {count == backup}  ← 值相等")

count = count + 50  # 重新赋值：count 指向新对象 150

print("\n  执行 count = count + 50 后：")
print(f"  count  = {count}   ← 指向新对象")
print(f"  backup = {backup}  ← backup 不受影响")
print(f"  count == backup: {count == backup}  ← False：值不相等")


# ---------------------------------------------------------------
# 场景 3：用 == 验证值相等关系
# ---------------------------------------------------------------
print("\n【场景 3】== 验证三个变量值相等")
print("-" * 40)

a = 42
b = a
c = a

print("  a = 42, b = a, c = a")
print(f"  a == b: {a == b}")  # True
print(f"  b == c: {b == c}")  # True
print(f"  a == b == c: {a == b == c}  ← 三个变量值相等")


# ---------------------------------------------------------------
# 场景 4：None 的引用特殊性
# ---------------------------------------------------------------
print("\n【场景 4】None 是单例对象")
print("-" * 40)

x = None
y = None

print("  x = None, y = None")
print(f"  x == y: {x == y}  ← True：None 值相等")
print(f"  x is None: {x is None}  ← True：判断 None 的推荐方式（L02 将学到）")


# ---------------------------------------------------------------
# 总结
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("  总结：变量是标签，不是盒子")
print("=" * 60)
print("""
  ✅ 不可变对象（str, int, float, bool, None）：
     重新赋值 = 创建新对象 = 原标签不受影响

  ✅ 判断两个变量值是否相等：x == y

  📖 预告：L03 会学到 list/dict/set 等可变对象，
     它们的"原地修改"行为与字符串/整数不同。
""")
