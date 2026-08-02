"""示例：包与模块的导入

演示如何导入包、子模块和包内的特定函数。
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

# ✅ 正确做法：使用 importlib 按物理路径加载
# 这种方式不会污染 sys.path，适合测试和动态加载场景
# ❌ 反模式：sys.path.insert 会污染全局导入路径，生产代码应使用：
# 1. 包安装（uv add）
# 2. 相对导入（包内使用）
# 3. importlib 按物理路径加载（测试场景）
examples_dir = Path(__file__).parent.resolve()
package_dir = examples_dir / "my_package"

my_package: ModuleType | None = None

if package_dir.exists():
    # 使用 spec_from_file_location（推荐方式）
    spec = importlib.util.spec_from_file_location("my_package", package_dir / "__init__.py")
    if spec and spec.loader:
        my_package = importlib.util.module_from_spec(spec)
        sys.modules["my_package"] = my_package
        spec.loader.exec_module(my_package)
else:
    print("⚠️  my_package 未找到，请确保在正确目录下运行")


# ============ 导入包 ============

if my_package is not None:
    # 方式 1：导入整个包
    print(f"包版本: {my_package.__version__}")
    print(f"包作者: {my_package.__author__}")

    # 方式 2：从包导入子模块
    from my_package import calculator

    result = calculator.add(10, 5)
    print(f"calculator.add(10, 5) = {result}")

    # 方式 3：从子模块导入特定函数
    from my_package.calculator import add, multiply

    print(f"add(3, 7) = {add(3, 7)}")
    print(f"multiply(4, 5) = {multiply(4, 5)}")

    # 方式 4：通过包的 __init__.py 直接导入函数
    # （因为 __init__.py 中已经导入了这些函数）
    print(f"直接导入: my_package.add(2, 3) = {my_package.add(2, 3)}")

    # ============ 导入子包 ============
    from my_package.subpackage import utils

    print(f"格式化日期: {utils.format_date(2026, 7, 1)}")
    print(f"格式化时间: {utils.format_time(14, 30, 45)}")


if __name__ == "__main__":
    print("\n=== 包导入总结 ===")
    print("1. import package              → package.module.func()")
    print("2. from package import module  → module.func()")
    print("3. from package.module import func → func()")
    print("4. from package import func    → func()（需要在 __init__.py 中导出）")
    print("")
    print("✅ 推荐使用 importlib 按物理路径加载，避免 sys.path 污染")
