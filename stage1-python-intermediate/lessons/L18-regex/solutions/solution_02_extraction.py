"""L16 练习 2 参考答案：日期、价格和 HTML 标签提取。"""

from __future__ import annotations

import re

DATE_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
PRICE_PATTERN = re.compile(r"(?<=\$)\d+(?:\.\d{2})?")
HTML_TAG_PATTERN = re.compile(r"<([A-Za-z][A-Za-z0-9-]*)(?:\s[^>]*)?>")


def _ensure_string(value: str, field_name: str) -> None:
    """确保输入是字符串。"""
    if not isinstance(value, str):
        msg = f"{field_name} 必须是字符串"
        raise TypeError(msg)


def extract_dates(text: str) -> list[str]:
    """提取 ISO 日期（YYYY-MM-DD）。"""
    _ensure_string(text, "text")
    return DATE_PATTERN.findall(text)


def extract_prices(text: str) -> list[float]:
    """提取美元价格并转换为 float。"""
    _ensure_string(text, "text")
    return [float(value) for value in PRICE_PATTERN.findall(text)]


def extract_html_tags(text: str) -> list[str]:
    """提取简单 HTML 起始标签名。"""
    _ensure_string(text, "text")
    return HTML_TAG_PATTERN.findall(text)
