"""L06 异常处理与防御代码 - 学员练习测试

测试 exercises/ 目录下学员编写的代码。
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
def basic_handling_module():
    """加载 exercises/01_basic_handling.py"""
    return _load_exercise_module("_test_basic_handling", EXERCISES_DIR / "01_basic_handling.py")


@pytest.fixture(scope="module")
def multiple_exceptions_module():
    """加载 exercises/02_multiple_exceptions.py"""
    return _load_exercise_module("_test_multiple", EXERCISES_DIR / "02_multiple_exceptions.py")


# ============================================================
# 01_basic_handling.py 测试
# ============================================================


class TestSafeDivide:
    """测试 safe_divide 函数"""

    def test_divide_normal(self, basic_handling_module) -> None:
        """测试正常除法"""
        func = getattr(basic_handling_module, "safe_divide", None)
        assert func is not None, "请定义 safe_divide 函数"
        assert func(10, 2) == 5.0

    def test_divide_by_zero(self, basic_handling_module) -> None:
        """测试除数为零"""
        func = getattr(basic_handling_module, "safe_divide", None)
        assert func is not None, "请定义 safe_divide 函数"
        assert func(10, 0) is None

    def test_divide_negative(self, basic_handling_module) -> None:
        """测试负数除法"""
        func = getattr(basic_handling_module, "safe_divide", None)
        assert func is not None, "请定义 safe_divide 函数"
        assert func(-10, 2) == -5.0

    def test_divide_decimal(self, basic_handling_module) -> None:
        """测试小数除法"""
        func = getattr(basic_handling_module, "safe_divide", None)
        assert func is not None, "请定义 safe_divide 函数"
        result = func(7, 3)
        assert result is not None
        assert abs(result - 2.333333) < 0.001


class TestSafeParseInt:
    """测试 safe_parse_int 函数"""

    def test_parse_valid(self, basic_handling_module) -> None:
        """测试有效整数"""
        func = getattr(basic_handling_module, "safe_parse_int", None)
        assert func is not None, "请定义 safe_parse_int 函数"
        assert func("42") == 42

    def test_parse_negative(self, basic_handling_module) -> None:
        """测试负数"""
        func = getattr(basic_handling_module, "safe_parse_int", None)
        assert func is not None, "请定义 safe_parse_int 函数"
        assert func("-10") == -10

    def test_parse_invalid(self, basic_handling_module) -> None:
        """测试无效输入"""
        func = getattr(basic_handling_module, "safe_parse_int", None)
        assert func is not None, "请定义 safe_parse_int 函数"
        assert func("abc") is None

    def test_parse_float_string(self, basic_handling_module) -> None:
        """测试浮点数字符串"""
        func = getattr(basic_handling_module, "safe_parse_int", None)
        assert func is not None, "请定义 safe_parse_int 函数"
        # int("3.14") 会抛出 ValueError
        assert func("3.14") is None


class TestSafeGetItem:
    """测试 safe_getitem 函数"""

    def test_getitem_normal(self, basic_handling_module) -> None:
        """测试正常索引"""
        func = getattr(basic_handling_module, "safe_getitem", None)
        assert func is not None, "请定义 safe_getitem 函数"
        items = ["apple", "banana", "cherry"]
        assert func(items, 1) == "banana"

    def test_getitem_first(self, basic_handling_module) -> None:
        """测试第一个元素"""
        func = getattr(basic_handling_module, "safe_getitem", None)
        assert func is not None, "请定义 safe_getitem 函数"
        items = ["apple", "banana", "cherry"]
        assert func(items, 0) == "apple"

    def test_getitem_out_of_range(self, basic_handling_module) -> None:
        """测试越界索引"""
        func = getattr(basic_handling_module, "safe_getitem", None)
        assert func is not None, "请定义 safe_getitem 函数"
        items = ["apple", "banana", "cherry"]
        assert func(items, 10) is None

    def test_getitem_negative(self, basic_handling_module) -> None:
        """测试负数索引"""
        func = getattr(basic_handling_module, "safe_getitem", None)
        assert func is not None, "请定义 safe_getitem 函数"
        items = ["apple", "banana", "cherry"]
        assert func(items, -1) == "cherry"


# ============================================================
# 03_custom_exceptions.py 测试
# ============================================================


@pytest.fixture(scope="module")
def custom_exceptions_module():
    """加载 exercises/03_custom_exceptions.py"""
    return _load_exercise_module("_test_custom", EXERCISES_DIR / "03_custom_exceptions.py")


class TestInvalidAgeError:
    """测试 InvalidAgeError 异常类"""

    def test_valid_age(self, custom_exceptions_module) -> None:
        """测试有效年龄"""
        func = getattr(custom_exceptions_module, "validate_age", None)
        assert func is not None, "请定义 validate_age 函数"
        assert func(25) == 25
        assert func(1) == 1
        assert func(150) == 150

    def test_invalid_age_negative(self, custom_exceptions_module) -> None:
        """测试负数年龄"""
        func = getattr(custom_exceptions_module, "validate_age", None)
        exc_class = getattr(custom_exceptions_module, "InvalidAgeError", None)
        assert func is not None, "请定义 validate_age 函数"
        assert exc_class is not None, "请定义 InvalidAgeError 类"
        with pytest.raises(exc_class) as exc_info:
            func(-5)
        assert exc_info.value.age == -5

    def test_invalid_age_zero(self, custom_exceptions_module) -> None:
        """测试零岁"""
        func = getattr(custom_exceptions_module, "validate_age", None)
        exc_class = getattr(custom_exceptions_module, "InvalidAgeError", None)
        with pytest.raises(exc_class):
            func(0)

    def test_invalid_age_too_old(self, custom_exceptions_module) -> None:
        """测试超出上限"""
        func = getattr(custom_exceptions_module, "validate_age", None)
        exc_class = getattr(custom_exceptions_module, "InvalidAgeError", None)
        with pytest.raises(exc_class):
            func(200)


class TestInvalidEmailError:
    """测试 InvalidEmailError 异常类"""

    def test_valid_email(self, custom_exceptions_module) -> None:
        """测试有效邮箱"""
        func = getattr(custom_exceptions_module, "validate_email", None)
        assert func is not None, "请定义 validate_email 函数"
        assert func("user@example.com") == "user@example.com"

    def test_invalid_email_no_at(self, custom_exceptions_module) -> None:
        """测试无效邮箱：无 @"""
        func = getattr(custom_exceptions_module, "validate_email", None)
        exc_class = getattr(custom_exceptions_module, "InvalidEmailError", None)
        with pytest.raises(exc_class):
            func("invalid-email")

    def test_invalid_email_empty(self, custom_exceptions_module) -> None:
        """测试空邮箱"""
        func = getattr(custom_exceptions_module, "validate_email", None)
        exc_class = getattr(custom_exceptions_module, "InvalidEmailError", None)
        with pytest.raises(exc_class):
            func("")


class TestValidateUser:
    """测试 validate_user 函数"""

    def test_valid_user(self, custom_exceptions_module) -> None:
        """测试有效用户"""
        func = getattr(custom_exceptions_module, "validate_user", None)
        assert func is not None, "请定义 validate_user 函数"
        result = func("alice", 25, "alice@example.com")
        assert result["username"] == "alice"
        assert result["age"] == "25"
        assert result["email"] == "alice@example.com"

    def test_username_normalized(self, custom_exceptions_module) -> None:
        """测试用户名规范化"""
        func = getattr(custom_exceptions_module, "validate_user", None)
        result = func("  bob  ", 30, "bob@example.com")
        assert result["username"] == "bob"


class TestRegisterUser:
    """测试 register_user 函数（收集多个错误）"""

    def test_valid_user(self, custom_exceptions_module) -> None:
        """测试有效用户"""
        func = getattr(custom_exceptions_module, "register_user", None)
        assert func is not None, "请定义 register_user 函数"
        result = func("alice", 25, "alice@example.com")
        assert result["username"] == "alice"

    def test_collects_multiple_errors(self, custom_exceptions_module) -> None:
        """测试收集多个错误"""
        func = getattr(custom_exceptions_module, "register_user", None)
        with pytest.raises(ValueError) as exc_info:
            func("", -5, "not-an-email")
        # 应该包含多个错误信息
        error_msg = str(exc_info.value)
        assert "用户名" in error_msg or "username" in error_msg.lower()
