"""L17 示例 3: 参数化测试"""

from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    "text,expected",
    [
        ("hello", 5),
        ("", 0),
        ("python", 6),
        ("a b", 3),
    ],
)
def test_str_length(text, expected):
    assert len(text) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
        (100, -50, 50),
    ],
)
def test_add(a, b, expected):
    assert a + b == expected


@pytest.mark.parametrize(
    "value,exc_msg",
    [
        ("abc", "invalid"),
        ("", "invalid"),
    ],
)
def test_parse_errors(value, exc_msg):
    import pytest

    with pytest.raises(ValueError, match=exc_msg):
        int(value)
