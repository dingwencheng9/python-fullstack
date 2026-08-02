"""L16 练习 2：日期、价格和 HTML 标签提取。"""

from __future__ import annotations

import re

DATE_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
PRICE_PATTERN = re.compile(r"(?<=\$)\d+(?:\.\d{2})?")
HTML_TAG_PATTERN = re.compile(r"<([A-Za-z][A-Za-z0-9-]*)(?:\s[^>]*)?>")


def _ensure_string(value: str, field_name: str) -> None:
    """确保输入是字符串。"""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} 必须是字符串")


def extract_dates(text: str) -> list[str]:
    """提取 ISO 日期（YYYY-MM-DD）。

    📝 练习要求：
    - 提取符合 ISO 8601 格式的日期（YYYY-MM-DD）
    - 非字符串输入应抛出 TypeError
    - 返回所有匹配的日期列表

    💡 实现提示：
    - 使用 re.findall() 查找所有匹配
    - 日期模式：\\d{4}-\\d{2}-\\d{2}
    - \\d{4} 表示 4 位数字（年份）
    - \\d{2} 表示 2 位数字（月份和日期）

    ✅ 测试用例：
    - extract_dates("今天是 2024-01-15，明天是 2024-01-16")
      → ["2024-01-15", "2024-01-16"]
    - extract_dates("没有日期") → []
    """
    _ensure_string(text, "text")
    return DATE_PATTERN.findall(text)


def extract_prices(text: str) -> list[float]:
    """提取美元价格并转换为 float。

    📝 练习要求：
    - 提取美元价格（格式：$数字.数字）
    - 将提取的价格转换为 float 类型
    - 非字符串输入应抛出 TypeError
    - 返回所有匹配的价格列表

    💡 实现提示：
    - 使用 re.findall() 查找所有匹配
    - 价格模式：\\$\\d+\\.\\d{2}
    - 注意：$ 和 . 在正则中是特殊字符，需要转义
    - 提取后需要去掉 $ 符号并转换为 float

    ✅ 测试用例：
    - extract_prices("Apple $1.99, Banana $0.59") → [1.99, 0.59]
    - extract_prices("Free!") → []
    - extract_prices("Total: $123.45") → [123.45]
    """
    _ensure_string(text, "text")
    return [float(value) for value in PRICE_PATTERN.findall(text)]


def extract_html_tags(text: str) -> list[str]:
    """提取简单 HTML 起始标签名。

    📝 练习要求：
    - 提取 HTML 起始标签的名称（如 div, span, p）
    - 只提取标签名，不包括 < > 符号
    - 非字符串输入应抛出 TypeError
    - 返回所有匹配的标签名列表

    💡 实现提示：
    - 使用 re.findall() 查找所有匹配
    - 标签模式：``r"<([A-Za-z][A-Za-z0-9-]*)(?:\\s[^>]*)?>"``
    - 使用捕获组 () 只提取标签名部分
    - 本练习只提取起始标签，支持简单属性和自闭合标签名

    ✅ 测试用例：
    - extract_html_tags("<div><span>Hi</span></div>")
      → ["div", "span"]（只提取起始标签）
    - extract_html_tags('<div class="card"><br></div>') → ["div", "br"]
    - extract_html_tags("No tags") → []
    """
    _ensure_string(text, "text")
    return HTML_TAG_PATTERN.findall(text)


if __name__ == "__main__":
    print("=" * 60)
    print("📝 L16 正则表达式练习 - 数据提取")
    print("=" * 60)
    assert extract_dates("会议在 2024-01-15 和 2024-01-16") == [
        "2024-01-15",
        "2024-01-16",
    ]
    assert extract_dates("没有日期") == []

    assert extract_prices("Apple $1.99, Banana $0.59") == [1.99, 0.59]
    assert extract_prices("Free!") == []

    assert extract_html_tags('<div class="card"><span>Hi</span><br></div>') == [
        "div",
        "span",
        "br",
    ]

    print("✅ 所有测试通过！")
    print("=" * 60)
