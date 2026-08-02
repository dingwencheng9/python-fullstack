"""数据验证模块"""

import re


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """验证手机号（中国大陆）"""
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone))


def validate_username(username: str) -> bool:
    """验证用户名（3-20位字母数字下划线）"""
    pattern = r"^[a-zA-Z0-9_]{3,20}$"
    return bool(re.match(pattern, username))
