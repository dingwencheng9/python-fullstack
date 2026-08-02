"""数据验证工具模块 - 参考解答"""

import re


def validate_email(email: str) -> bool:
    """验证邮箱格式

    Args:
        email: 待验证的邮箱地址

    Returns:
        邮箱格式是否有效
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """验证手机号（中国大陆）

    Args:
        phone: 待验证的手机号

    Returns:
        手机号格式是否有效
    """
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone))


def validate_username(username: str) -> bool:
    """验证用户名（3-20位字母数字下划线）

    Args:
        username: 待验证的用户名

    Returns:
        用户名格式是否有效
    """
    pattern = r"^[a-zA-Z0-9_]{3,20}$"
    return bool(re.match(pattern, username))


if __name__ == "__main__":
    # 测试代码
    print("=== 验证器测试 ===")
    print(f"user@example.com: {validate_email('user@example.com')}")
    print(f"invalid-email: {validate_email('invalid-email')}")
    print(f"13812345678: {validate_phone('13812345678')}")
    print(f"1234567890: {validate_phone('1234567890')}")
    print(f"alice123: {validate_username('alice123')}")
    print(f"ab: {validate_username('ab')}")
