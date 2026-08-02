"""L17 pytest-complete 测试 — 验证测试框架本身的功能。"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


def test_import_pytest():
    """pytest 可导入。"""
    import pytest

    assert hasattr(pytest, "fixture")
    assert hasattr(pytest, "mark")
    assert hasattr(pytest, "raises")


def test_aaa_pattern():
    """验证 AAA 模式测试。"""
    result = 2 + 2
    assert result == 4


def test_pytest_raises():
    """测试 pytest.raises。"""
    with pytest.raises(ValueError):
        int("not_a_number")


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (10, -5, 5),
    ],
)
def test_parametrize_basic(a, b, expected):
    """参数化基础测试。"""
    assert a + b == expected


@pytest.fixture
def sample_dict():
    """示例 fixture。"""
    return {"key": "value", "number": 42}


def test_fixture_usage(sample_dict):
    """测试 fixture 注入。"""
    assert sample_dict["key"] == "value"
    assert sample_dict["number"] == 42


def test_fixture_scope_isolation(sample_dict):
    """每个测试函数获得独立的 fixture 实例。"""
    sample_dict["modified"] = True
    assert "modified" in sample_dict


def test_mock_http_call():
    """测试 mock HTTP 请求。"""
    pytest.importorskip("requests", reason="需要 requests 库")
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = mock_get("https://api.example.com").json()
        assert result["status"] == "ok"


def test_monkeypatch_env(monkeypatch):
    """测试 monkeypatch 修改环境变量。"""
    monkeypatch.setenv("TEST_MODE", "true")
    assert os.environ["TEST_MODE"] == "true"


def test_temp_dir_fixture():
    """测试 TemporaryDirectory 可用。"""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir) / "test.txt"
        p.write_text("data")
        assert p.read_text() == "data"


def test_float_precision():
    """测试 pytest.approx 处理浮点精度。"""
    assert pytest.approx(0.3, rel=1e-9) == 0.1 + 0.2
    assert pytest.approx(0.33333, abs=1e-4) == 1.0 / 3.0


def test_error_message_match():
    """测试异常消息匹配。"""
    with pytest.raises(ValueError, match="invalid"):
        raise ValueError("invalid literal for int()")


def test_calculator_add(solutions):
    """测试 Calculator add 方法。"""
    calc = solutions.solution_02_parametrize_calc.Calculator()
    assert calc.add(2, 3) == 5


def test_calculator_divide(solutions):
    """测试 Calculator divide 方法。"""
    calc = solutions.solution_02_parametrize_calc.Calculator()
    assert calc.divide(10, 2) == 5.0


def test_calculator_divide_by_zero(solutions):
    """测试 Calculator 除零异常。"""
    calc = solutions.solution_02_parametrize_calc.Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, 0)
