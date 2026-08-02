"""示例模块：演示 __all__ 的作用"""

# 定义公开 API（会被 from module import * 导入）
__all__ = ["CONSTANT_VALUE", "greet_user", "public_function"]


# 私有函数（不会被 import * 导入）
def _private_helper() -> str:
    """私有辅助函数，不对外公开"""
    return "This is private"


def public_function(x: int, y: int) -> int:
    """公开函数，返回两数之和"""
    return x + y


def greet_user(name: str) -> str:
    """公开函数，返回问候语"""
    return f"Hello, {name}!"


def another_public(x: int) -> int:
    """另一个公开函数，但不在 __all__ 中"""
    return x * 2


CONSTANT_VALUE = 42
