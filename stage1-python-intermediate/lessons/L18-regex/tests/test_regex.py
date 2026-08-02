"""L16 正则表达式测试。"""

from __future__ import annotations

import pytest


@pytest.fixture(scope="module", autouse=True)
def _inject_solutions(solutions, request) -> None:
    """从 ``solutions`` fixture 动态获取子模块并注入模块命名空间。

    取代原先顶层的 ``importlib.import_module("solutions.01_validation")``，
    避免依赖 sys.path 注入。测试体保持原样，运行时通过模块全局名 ``validation``
    / ``extraction`` 解析。
    """
    request.module.__dict__["validation"] = solutions.solution_01_validation
    request.module.__dict__["extraction"] = solutions.solution_02_extraction


@pytest.mark.parametrize(
    ("email", "expected"),
    [
        ("user@example.com", True),
        ("user.name+tag@sub.example.co.uk", True),
        ("invalid", False),
        ("@example.com", False),
        ("user@", False),
        ("", False),
    ],
)
def test_validate_email(email: str, expected: bool) -> None:
    assert validation.validate_email(email) is expected


@pytest.mark.parametrize(
    ("phone", "expected"),
    [
        ("13800138000", True),
        ("12345", False),
        ("", False),
        ("abc", False),
    ],
)
def test_validate_phone(phone: str, expected: bool) -> None:
    assert validation.validate_phone(phone) is expected


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://example.com", True),
        ("http://sub.example.co.uk:8080/path?q=1", True),
        ("ftp://example.com", False),
        ("https://localhost", False),
    ],
)
def test_validate_url(url: str, expected: bool) -> None:
    assert validation.validate_url(url) is expected


def test_extract_dates_iso_format() -> None:
    text = "Meeting on 2026-06-11 and 2026-07-15."
    assert extraction.extract_dates(text) == ["2026-06-11", "2026-07-15"]


def test_extract_dates_empty() -> None:
    """边界：无日期文本。"""
    assert extraction.extract_dates("no dates here") == []


def test_extract_prices_currency() -> None:
    text = "Apple $1.99, Banana $0.50, Cherry $12.34"
    assert extraction.extract_prices(text) == [1.99, 0.50, 12.34]


def test_extract_html_tags() -> None:
    text = '<div class="card"><span>Hi</span><br></div>'
    assert extraction.extract_html_tags(text) == ["div", "span", "br"]


def test_validate_email_raises_on_non_string() -> None:
    """异常路径：非字符串输入。"""
    with pytest.raises(TypeError):
        validation.validate_email(None)  # type: ignore[arg-type]


def test_extract_prices_raises_on_non_string() -> None:
    """异常路径：非字符串输入。"""
    with pytest.raises(TypeError):
        extraction.extract_prices(None)  # type: ignore[arg-type]
