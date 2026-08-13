"""L07 OOP基础 - 自定义异常测试

测试 exercises/04_custom_exceptions.py 中定义的自定义异常类。
"""

import importlib.util
from pathlib import Path

import pytest


EXERCISES_DIR = Path(__file__).resolve().parent.parent / "exercises"


def _load_exercise_module(name: str, file_path: Path):
    """按物理路径加载模块，不污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def custom_exceptions_module():
    """加载 exercises/04_custom_exceptions.py"""
    return _load_exercise_module("_test_custom", EXERCISES_DIR / "04_custom_exceptions.py")


class TestCustomExceptions:
    """测试自定义异常类"""

    def test_invalid_age_error(self, custom_exceptions_module) -> None:
        """测试 InvalidAgeError 异常"""
        cls = getattr(custom_exceptions_module, "InvalidAgeError", None)
        assert cls is not None, "请定义 InvalidAgeError 异常类"

        error = cls(200)
        assert isinstance(error, ValueError)
        assert "200" in str(error)

    def test_invalid_email_error(self, custom_exceptions_module) -> None:
        """测试 InvalidEmailError 异常"""
        cls = getattr(custom_exceptions_module, "InvalidEmailError", None)
        assert cls is not None, "请定义 InvalidEmailError 异常类"

        error = cls("invalid")
        assert isinstance(error, ValueError)
        assert "invalid" in str(error)

    def test_validate_age_valid(self, custom_exceptions_module) -> None:
        """测试有效年龄验证"""
        func = getattr(custom_exceptions_module, "validate_age", None)
        assert func is not None, "请定义 validate_age 函数"
        assert func(25) == 25

    def test_validate_age_invalid(self, custom_exceptions_module) -> None:
        """测试无效年龄验证"""
        cls = getattr(custom_exceptions_module, "InvalidAgeError", None)
        func = getattr(custom_exceptions_module, "validate_age", None)
        assert cls is not None and func is not None

        with pytest.raises(cls):
            func(-5)

    def test_validate_email_valid(self, custom_exceptions_module) -> None:
        """测试有效邮箱验证"""
        func = getattr(custom_exceptions_module, "validate_email", None)
        assert func is not None, "请定义 validate_email 函数"
        assert func("test@example.com") == "test@example.com"

    def test_validate_email_invalid(self, custom_exceptions_module) -> None:
        """测试无效邮箱验证"""
        cls = getattr(custom_exceptions_module, "InvalidEmailError", None)
        func = getattr(custom_exceptions_module, "validate_email", None)
        assert cls is not None and func is not None

        with pytest.raises(cls):
            func("invalid")

    def test_register_user_success(self, custom_exceptions_module) -> None:
        """测试成功注册"""
        func = getattr(custom_exceptions_module, "register_user", None)
        assert func is not None, "请定义 register_user 函数"

        result = func("alice", 25, "alice@example.com")
        assert result["username"] == "alice"
        assert result["age"] == "25"
        assert result["email"] == "alice@example.com"

    def test_register_user_multiple_errors(self, custom_exceptions_module) -> None:
        """测试多个验证错误"""
        func = getattr(custom_exceptions_module, "register_user", None)
        assert func is not None, "请定义 register_user 函数"

        with pytest.raises(ValueError) as exc_info:
            func("", -5, "invalid")

        error_message = str(exc_info.value)
        assert "用户名不能为空" in error_message or "empty" in error_message.lower()
