"""示例：模块的导入方式

演示 Python 中各种导入模块的方式。
"""

# ============ 各种导入方式 ============

# 方式 1：导入整个模块（推荐）
import math

result = math.sqrt(16)  # 需要使用模块名前缀
print(f"sqrt(16) = {result}")

# 方式 2：从模块导入特定内容（推荐）
from math import sqrt, pi  # noqa: E402

result = sqrt(25)  # 直接使用函数名
print(f"sqrt(25) = {result}")
print(f"pi = {pi}")

# 方式 3：从模块导入多个内容
from math import ceil, floor, pow  # noqa: E402

print(f"ceil(3.2) = {ceil(3.2)}")  # 4
print(f"floor(3.8) = {floor(3.8)}")  # 3
print(f"pow(2, 3) = {pow(2, 3)}")  # 8.0

# 方式 4：使用别名（避免命名冲突或简化长名称）
import math as m  # noqa: E402

result = m.sqrt(9)
print(f"m.sqrt(9) = {result}")

# 方式 5：从模块导入并重命名
from math import sqrt as square_root  # noqa: E402

print(f"square_root(16) = {square_root(16)}")

# 方式 6：导入所有内容（不推荐，可能覆盖同名变量）
# from math import *  # 危险：可能与自己的变量冲突


if __name__ == "__main__":
    print("\n=== 导入方式总结 ===")
    print("1. import module           → module.func()")
    print("2. from module import func → func()")
    print("3. import module as m      → m.func()")
    print("4. from module import func as f → f()")
    print("\n推荐：方式 1 和 2，避免 from module import *")
