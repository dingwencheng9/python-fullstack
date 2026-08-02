"""
L10: 类型系统 - 类型收窄练习解答

使用 TypeGuard 和 isinstance 实现类型收窄。
"""

from typing import TypeGuard


def is_string_list(value: list[object]) -> TypeGuard[list[str]]:
    """验证列表是否全为字符串"""
    return all(isinstance(item, str) for item in value)


def is_dict_list(value: list[object]) -> TypeGuard[list[dict]]:
    """验证列表是否全为字典"""
    return all(isinstance(item, dict) for item in value)


def filter_strings(items: list[object]) -> list[str]:
    """过滤并返回字符串元素"""
    return [item for item in items if isinstance(item, str)]
