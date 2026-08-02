"""示例：__all__ 控制导出

演示 __all__ 如何控制 from module import * 的行为。

学习目标：
1. 理解 __all__ 的作用
2. 掌握 public vs private 命名约定
3. 了解 import * 的潜在问题
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

# ✅ 正确做法：使用 importlib 按物理路径加载
# ❌ 反模式：sys.path.insert 会污染全局导入路径
# 仅用于演示目的
examples_dir = Path(__file__).parent.resolve()
module_file = examples_dir / "my_module.py"

my_module: ModuleType | None = None

if module_file.exists():
    # 使用 spec_from_file_location 加载模块
    spec = importlib.util.spec_from_file_location("my_module", module_file)
    if spec and spec.loader:
        my_module = importlib.util.module_from_spec(spec)
        sys.modules["my_module"] = my_module
        spec.loader.exec_module(my_module)
else:
    print("⚠️  my_module.py 未找到，请确保在正确目录下运行")


# ============ 正常导入（__all__ 不影响） ============
if my_module is not None:
    print("=== 正常导入：import my_module ===")
    print(f"my_module.public_function(1, 2) = {my_module.public_function(1, 2)}")
    print(f"my_module.another_public(5) = {my_module.another_public(5)}")  # 私有函数也可访问
    print(f"my_module._private_helper() = {my_module._private_helper()}")  # 私有函数仍可显式访问
    print(f"my_module.CONSTANT_VALUE = {my_module.CONSTANT_VALUE}")

    # ============ __all__ 的定义 ============
    print("\n=== 模块的 __all__ 定义 ===")
    print(f"my_module.__all__ = {my_module.__all__}")
    print("\n说明：__all__ 定义了 from module import * 时导出的内容")

    # ============ 使用 importlib 检查模块属性 ============
    print("\n=== 检查模块属性 ===")

    # 检查 reload 后 __all__ 是否生效
    importlib.reload(my_module)
    print(f"reload 后 __all__ = {my_module.__all__}")

    # ============ from import * 的效果 ============
    print("\n=== from my_module import * ===")
    print("⚠️ 注意：在 Python 交互式环境中执行")
    print("from my_module import * 会根据 __all__ 决定导入内容")
    print("\n预期行为：")
    print("  ✓ public_function 会被导入（在 __all__ 中）")
    print("  ✓ PublicClass 会被导入（在 __all__ 中）")
    print("  ✓ CONSTANT_VALUE 会被导入（在 __all__ 中）")
    print("  ✗ another_public 不会被 import * 导入（公共命名，但不在 __all__ 中）")
    print("  ✗ _private_helper 不会被导入（不在 __all__ 中）")
    print("  ✗ _internal_value 不会被导入（不在 __all__ 中）")

    # 演示：手动检查 __all__ 内容
    print("\n=== 验证 __all__ 控制导出 ===")
    for name in dir(my_module):
        if not name.startswith("_") or name in my_module.__all__:
            if name in my_module.__all__:
                print(f"  ✓ {name} - 会被 import * 导入")
            else:
                print(f"    {name} - 公共属性但不在 __all__ 中")

    print("\n✅ 推荐使用 importlib 按物理路径加载，避免 sys.path 污染")
