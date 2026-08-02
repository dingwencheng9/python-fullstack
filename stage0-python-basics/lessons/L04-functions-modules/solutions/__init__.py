"""L04 函数与模块 - 参考解答

本模块提供 L04 课程练习题的参考解答。
"""

# 导出所有子模块的公开函数和类
from .calculator import (
    add,
    subtract,
    multiply,
    divide,
)
from .validators import (
    validate_email,
    validate_phone,
    validate_username,
)

__all__ = [
    "add",
    "divide",
    "multiply",
    "subtract",
    "validate_email",
    "validate_phone",
    "validate_username",
]
