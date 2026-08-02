"""L17 示例 1: pytest 基础模式"""


# AAA 模式

from __future__ import annotations


def test_answer():
    """Arrange-Act-Assert 基础示例"""
    # Arrange
    expected = 42
    # Act
    result = 40 + 2
    # Assert
    assert result == expected


def test_string_operations():
    assert "hello".upper() == "HELLO"
    assert "  spaced  ".strip() == "spaced"


def test_float_comparison():
    import pytest

    assert pytest.approx(0.3, rel=1e-9) == 0.1 + 0.2


def test_exception():
    import pytest

    with pytest.raises(ValueError, match="invalid"):
        int("not_a_number")
