"""L03 示例6: 列表推导式 vs 生成器表达式

学习目标:
- 理解推导式 [...] 与生成器表达式 (...) 的根本区别
- 量化对比内存占用差异

【知识点边界】本文件仅使用 L01 + L02 + L03 的知识点：
- print, for, range, if
- list, tuple, dict
- 列表推导式、生成器表达式
"""

# ============================================================
# 1. 基本语法对比
# ============================================================
print("=" * 50)
print("1. 基本语法对比")
print("=" * 50)

# 列表推导式 — 方括号，立即创建完整列表
list_comp = [x**2 for x in range(5)]
print("列表推导式 [x**2 for x in range(5)]")
print(f"  结果: {list_comp}")
print(f"  类型: {type(list_comp).__name__}")

# 生成器表达式 — 圆括号，不立即创建列表
gen_exp = (x**2 for x in range(5))
print("\n生成器表达式 (x**2 for x in range(5))")
print(f"  结果: {gen_exp}")
print(f"  类型: {type(gen_exp).__name__}")

# ============================================================
# 2. 行为差异：可重复迭代 vs 只能消费一次
# ============================================================
print("\n" + "=" * 50)
print("2. 行为差异：可重复迭代 vs 只能消费一次")
print("=" * 50)

# 列表 — 可重复迭代
print("列表（可重复迭代）:")
squares_list = [x**2 for x in range(3)]
print(f"  第一次遍历: {list(squares_list)}")
print(f"  第二次遍历: {list(squares_list)}")  # 仍可访问
print(f"  第三次遍历: {list(squares_list)}")  # 仍可访问

# 生成器 — 只能消费一次！
print("\n生成器（只能消费一次）:")
squares_gen = (x**2 for x in range(3))
print(f"  第一次遍历: {list(squares_gen)}")
print(f"  第二次遍历: {list(squares_gen)}")  # 空了！
print(f"  第三次遍历: {list(squares_gen)}")  # 仍然是空

# ============================================================
# 3. 何时用哪个？
# ============================================================
print("\n" + "=" * 50)
print("3. 何时用哪个？")
print("=" * 50)

# 需要随机访问/多次遍历 → 列表必需
squares = [x**2 for x in range(10)]
print(f"需要随机访问: squares[5] = {squares[5]}")
print(f"需要长度: len(squares) = {len(squares)}")

# 大数据量求和 → 生成器最优（不创建完整列表）
# 计算前 1000 个数的平方和（演示用小数据）
total_small = sum(x**2 for x in range(1000))
print(f"\n生成器求和 sum(x**2 for x in range(1000)) = {total_small}")
print("(生成器不创建完整列表，内存友好)")

# ============================================================
# 4. 断言验证
# ============================================================
print("\n" + "=" * 50)
print("4. 验证")
print("=" * 50)

# 验证类型
assert isinstance(list_comp, list)
assert not isinstance(gen_exp, list)
assert hasattr(gen_exp, "__next__")  # 生成器有 __next__

print("✅ 列表推导式类型正确: list")
print("✅ 生成器不是 list")
print("✅ 生成器有 __next__ 方法")

# ============================================================
# 5. 经验法则
# ============================================================
print("\n" + "=" * 50)
print("5. 经验法则")
print("=" * 50)
print("列表推导式 []:")
print("  - 数据量小（< 10000 个元素）")
print("  - 需要多次访问相同数据")
print("  - 简单直观，性能差异可忽略")

print("\n生成器表达式 ():")
print("  - 数据量大（> 10000 个元素）")
print("  - 只需遍历一次（如求和、筛选）")
print("  - 节省内存，避免一次性加载")

print("\n✅ 全部演示完成！")
