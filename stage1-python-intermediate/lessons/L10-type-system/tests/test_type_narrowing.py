"""
L10: 类型系统 - TypeGuard 类型收窄测试
"""

import pytest

type_narrowing = None  # type: ignore[assignment]


@pytest.fixture(autouse=True)
def _inject_type_narrowing(solutions, request) -> None:
    """注入 type_narrowing 模块（solution_01_type_narrowing）到测试命名空间。"""
    try:
        request.module.__dict__["type_narrowing"] = getattr(solutions, "solution_01_type_narrowing")
    except (AttributeError, ImportError) as e:
        pytest.fail(f"无法导入 solution_01_type_narrowing: {e}")


def test_is_string_list_true():
    """测试全为字符串的列表"""
    data = ["a", "b", "c"]
    assert type_narrowing.is_string_list(data) is True


def test_is_string_list_false():
    """测试包含非字符串的列表"""
    data = ["a", 1, "c"]
    assert type_narrowing.is_string_list(data) is False


def test_is_string_list_empty():
    """测试空列表"""
    data: list[object] = []
    assert type_narrowing.is_string_list(data) is True


def test_filter_strings():
    """测试字符串过滤"""
    data: list[object] = ["a", 1, "b", 2, "c"]
    result = type_narrowing.filter_strings(data)
    assert result == ["a", "b", "c"]
