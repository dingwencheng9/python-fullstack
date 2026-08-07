"""L18 练习 1 参考答案：邮箱、手机号和 URL 校验。"""

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
        msg = f"{field_name} 必须是字符串"
        raise TypeError(msg)


def validate_email(email: str) -> bool:
    """验证邮箱格式。"""
    _ensure_string(email, "email")
    return bool(EMAIL_PATTERN.fullmatch(email))


def validate_phone(phone: str) -> bool:
    """验证中国大陆手机号。"""
    _ensure_string(phone, "phone")
    return bool(PHONE_PATTERN.fullmatch(phone))


def validate_url(url: str) -> bool:
    """验证简单 HTTP/HTTPS URL。"""
    _ensure_string(url, "url")
    return bool(URL_PATTERN.fullmatch(url))
