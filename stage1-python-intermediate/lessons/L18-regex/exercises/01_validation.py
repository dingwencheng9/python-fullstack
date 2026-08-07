"""L18 练习 1：邮箱、手机号和 URL 校验。"""

from __future__ import annotations

import re

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^1[3-9]\d{9}$")
URL_PATTERN = re.compile(
    r"^https?://"
    r"(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}"
    r"(?::\d{2,5})?"
    r"(?:/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?$"
)


def _ensure_string(value: str, field_name: str) -> None:
    """确保输入是字符串。"""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} 必须是字符串")


def validate_email(email: str) -> bool:
    """验证邮箱格式。

    📝 练习要求：
    - 必须是字符串，否则抛出 TypeError
    - 用户名支持字母、数字、点、下划线、百分号、加号、横线
    - 域名支持多级域名
    - 顶级域名至少 2 个字母

    💡 实现提示：
    - 使用 re.fullmatch() 进行完整匹配
    - 正则模式参考：r'^[用户名部分]@[域名部分]$'
    - 用户名：[a-zA-Z0-9._%+-]+
    - 域名：[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}

    ✅ 测试用例：
    - validate_email("user@example.com") → True
    - validate_email("invalid.email") → False
    - validate_email("user@sub.domain.com") → True
    """
    _ensure_string(email, "email")
    return bool(EMAIL_PATTERN.fullmatch(email))


def validate_phone(phone: str) -> bool:
    """验证中国大陆手机号。

    📝 练习要求：
    - 必须是字符串，否则抛出 TypeError
    - 11 位数字
    - 以 1 开头，第二位为 3-9

    💡 实现提示：
    - 使用 re.fullmatch() 进行完整匹配
    - 正则模式参考：r'^1[3-9]\\d{9}$'
    - \\d 表示数字，{9} 表示重复 9 次

    ✅ 测试用例：
    - validate_phone("13812345678") → True
    - validate_phone("12345678901") → False（第二位不是3-9）
    - validate_phone("138123456789") → False（超过11位）
    """
    _ensure_string(phone, "phone")
    return bool(PHONE_PATTERN.fullmatch(phone))


def validate_url(url: str) -> bool:
    """验证简单 HTTP/HTTPS URL。

    📝 练习要求：
    - 必须是字符串，否则抛出 TypeError
    - 支持 http 和 https
    - 域名至少包含一个点
    - 可选端口和路径

    💡 实现提示：
    - 使用 re.fullmatch() 进行完整匹配
    - URL 结构：协议://域名[:端口][/路径]
    - 协议：https?（? 表示 s 可选）
    - 域名：[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}
    - 端口：(:\\d+)?（可选）
    - 路径：(/.*)?（可选）

    ✅ 测试用例：
    - validate_url("https://example.com") → True
    - validate_url("http://sub.example.com:8080/path") → True
    - validate_url("ftp://example.com") → False（协议不支持）
    """
    _ensure_string(url, "url")
    return bool(URL_PATTERN.fullmatch(url))


if __name__ == "__main__":
    print("=" * 60)
    print("📝 L18 正则表达式练习 - 数据验证")
    print("=" * 60)
    assert validate_email("user@example.com") is True
    assert validate_email("invalid.email") is False
    assert validate_email("user@sub.domain.com") is True

    assert validate_phone("13812345678") is True
    assert validate_phone("12345678901") is False
    assert validate_phone("138123456789") is False

    assert validate_url("https://example.com") is True
    assert validate_url("http://sub.example.com:8080/path") is True
    assert validate_url("ftp://example.com") is False

    print("✅ 所有测试通过！")
    print("=" * 60)
