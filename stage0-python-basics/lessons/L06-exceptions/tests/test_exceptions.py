"""L08 Exceptions 测试用例"""

import pytest





class TestSafeDivide:
    """测试安全除法函数"""

    def test_divide_normal(self):
        """测试正常除法"""
        result = basic_handling.safe_divide(10, 2)  # noqa: F821
        assert result == 5.0

    def test_divide_by_zero(self):
        """测试除数为零"""
        result = basic_handling.safe_divide(10, 0)  # noqa: F821
        assert result is None

    def test_divide_negative(self):
        """测试负数除法"""
        result = basic_handling.safe_divide(-10, 2)  # noqa: F821
        assert result == -5.0

    def test_divide_decimal(self):
        """测试小数除法"""
        result = basic_handling.safe_divide(7, 3)  # noqa: F821
        assert result is not None
        assert abs(result - 2.333333) < 0.001


class TestSafeParseInt:
    """测试安全整数解析函数"""

    def test_parse_valid(self):
        """测试有效整数"""
        result = basic_handling.safe_parse_int("42")  # noqa: F821
        assert result == 42

    def test_parse_negative(self):
        """测试负数"""
        result = basic_handling.safe_parse_int("-10")  # noqa: F821
        assert result == -10

    def test_parse_invalid(self):
        """测试无效输入"""
        result = basic_handling.safe_parse_int("abc")  # noqa: F821
        assert result is None

    def test_parse_float_string(self):
        """测试浮点数字符串（会丢失小数部分）"""
        result = basic_handling.safe_parse_int("3.14")  # noqa: F821
        assert result is None  # int() 对 "3.14" 会抛出 ValueError


class TestSafeGetItem:
    """测试安全列表元素获取函数"""

    def test_getitem_normal(self):
        """测试正常索引"""
        items = ["apple", "banana", "cherry"]
        result = basic_handling.safe_getitem(items, 1)  # noqa: F821
        assert result == "banana"

    def test_getitem_first(self):
        """测试第一个元素"""
        items = ["apple", "banana", "cherry"]
        result = basic_handling.safe_getitem(items, 0)  # noqa: F821
        assert result == "apple"

    def test_getitem_out_of_range(self):
        """测试越界索引"""
        items = ["apple", "banana", "cherry"]
        result = basic_handling.safe_getitem(items, 10)  # noqa: F821
        assert result is None

    def test_getitem_negative(self):
        """测试负数索引"""
        items = ["apple", "banana", "cherry"]
        result = basic_handling.safe_getitem(items, -1)  # noqa: F821
        assert result == "cherry"


class TestProcessNumber:
    """测试 process_number 函数"""

    def test_process_valid(self):
        """测试有效输入"""
        result = multiple_exceptions.process_number("10", "2")  # noqa: F821
        assert result == 5.0

    def test_process_zero_divisor(self):
        """测试除数为零"""
        result = multiple_exceptions.process_number("10", "0")  # noqa: F821
        assert result is None

    def test_process_invalid_value(self):
        """测试无效数值"""
        result = multiple_exceptions.process_number("abc", "2")  # noqa: F821
        assert result is None

    def test_process_invalid_divisor(self):
        """测试无效除数"""
        result = multiple_exceptions.process_number("10", "xyz")  # noqa: F821
        assert result is None

    def test_process_type_error(self):
        """测试类型错误输入"""
        result = multiple_exceptions.process_number(None, "2")  # noqa: F821
        assert result is None


class TestValidateUserInput:
    """测试 validate_user_input 函数"""

    def test_validate_user_input_success(self):
        result = multiple_exceptions.validate_user_input(" alice ", "25")  # noqa: F821
        assert result == {"username": "alice", "age": "25"}

    def test_validate_user_input_blank_username(self):
        with pytest.raises(ValueError, match="用户名不能为空"):
            multiple_exceptions.validate_user_input("   ", "25")  # noqa: F821

    def test_validate_user_input_invalid_age(self):
        with pytest.raises(ValueError, match="年龄必须是有效数字"):
            multiple_exceptions.validate_user_input("alice", "abc")  # noqa: F821

    def test_validate_user_input_age_out_of_range(self):
        with pytest.raises(ValueError, match="年龄必须在 0-150 之间"):
            multiple_exceptions.validate_user_input("alice", "151")  # noqa: F821


class TestCustomExceptions:
    """测试自定义异常类"""

    def test_invalid_age_error(self):
        """测试 InvalidAgeError 异常"""
        InvalidAgeError = custom_exceptions.InvalidAgeError  # noqa: F821
        error = InvalidAgeError(200)
        assert isinstance(error, ValueError)
        assert "200" in str(error)

    def test_invalid_email_error(self):
        """测试 InvalidEmailError 异常"""
        InvalidEmailError = custom_exceptions.InvalidEmailError  # noqa: F821
        error = InvalidEmailError("invalid")
        assert isinstance(error, ValueError)
        assert "invalid" in str(error)

    def test_validate_age_valid(self):
        """测试有效年龄验证"""
        validate_age = custom_exceptions.validate_age  # noqa: F821
        assert validate_age(25) == 25

    def test_validate_age_invalid(self):
        """测试无效年龄验证"""
        validate_age = custom_exceptions.validate_age  # noqa: F821
        InvalidAgeError = custom_exceptions.InvalidAgeError  # noqa: F821
        with pytest.raises(InvalidAgeError):
            validate_age(-5)

    def test_validate_email_valid(self):
        """测试有效邮箱验证"""
        validate_email = custom_exceptions.validate_email  # noqa: F821
        assert validate_email("test@example.com") == "test@example.com"

    def test_validate_email_invalid(self):
        """测试无效邮箱验证"""
        validate_email = custom_exceptions.validate_email  # noqa: F821
        InvalidEmailError = custom_exceptions.InvalidEmailError  # noqa: F821
        with pytest.raises(InvalidEmailError):
            validate_email("invalid")

    def test_register_user_success(self):
        """测试成功注册"""
        register_user = custom_exceptions.register_user  # noqa: F821
        result = register_user("alice", 25, "alice@example.com")
        assert result["username"] == "alice"
        assert result["age"] == "25"
        assert result["email"] == "alice@example.com"

    def test_register_user_multiple_errors(self):
        """测试多个验证错误"""
        register_user = custom_exceptions.register_user  # noqa: F821
        with pytest.raises(ValueError) as exc_info:
            register_user("", -5, "invalid")
        # 应该同时收集多个错误信息，而不是遇到第一个错误就停止。
        error_message = str(exc_info.value)
        assert "用户名不能为空" in error_message
        assert "无效的年龄" in error_message
        assert "无效的邮箱" in error_message

    def test_top_level_exception_exports(self):
        """测试 solutions.__init__ 暴露自定义异常类"""
        assert solutions_pkg.InvalidAgeError is custom_exceptions.InvalidAgeError  # noqa: F821
        assert solutions_pkg.InvalidEmailError is custom_exceptions.InvalidEmailError  # noqa: F821
