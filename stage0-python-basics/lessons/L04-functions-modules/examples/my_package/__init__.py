"""my_package - 数学工具包

这是一个示例包，演示 Python 包的组织结构。
"""

from __future__ import annotations

__version__ = "1.0.0"
__author__ = "Course Author"

# 导出列表（用于 from my_package import *）
__all__ = ["add", "subtract", "multiply", "divide", "validate_email", "validate_phone"]

# 从子模块导入常用功能，方便直接访问
from .calculator import add, subtract, multiply, divide  # noqa: F401
from .validators import validate_email, validate_phone  # noqa: F401
