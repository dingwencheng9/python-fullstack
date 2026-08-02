"""测试文件：L04 函数与模块

验证 solutions 模块中的函数实现是否正确。
"""


class TestCalculator:
    """计算器模块测试"""

    def test_add(self, solutions) -> None:
        """测试加法"""
        from solutions import add

        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_subtract(self, solutions) -> None:
        """测试减法"""
        from solutions import subtract

        assert subtract(5, 3) == 2
        assert subtract(1, 1) == 0
        assert subtract(0, 5) == -5

    def test_multiply(self, solutions) -> None:
        """测试乘法"""
        from solutions import multiply

        assert multiply(3, 4) == 12
        assert multiply(0, 100) == 0
        assert multiply(-2, 3) == -6

    def test_divide(self, solutions) -> None:
        """测试除法"""
        from solutions import divide

        assert divide(10, 2) == 5.0
        assert divide(7, 2) == 3.5
        assert divide(10, 0) is None


class TestValidators:
    """验证器模块测试"""

    def test_validate_email_valid(self, solutions) -> None:
        """测试有效的邮箱"""
        from solutions import validate_email

        assert validate_email("user@example.com") is True
        assert validate_email("test.user@domain.co.uk") is True

    def test_validate_email_invalid(self, solutions) -> None:
        """测试无效的邮箱"""
        from solutions import validate_email

        assert validate_email("invalid-email") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False

    def test_validate_phone_valid(self, solutions) -> None:
        """测试有效的手机号"""
        from solutions import validate_phone

        assert validate_phone("13812345678") is True
        assert validate_phone("15912345678") is True

    def test_validate_phone_invalid(self, solutions) -> None:
        """测试无效的手机号"""
        from solutions import validate_phone

        assert validate_phone("1234567890") is False
        assert validate_phone("10012345678") is False

    def test_validate_username_valid(self, solutions) -> None:
        """测试有效的用户名"""
        from solutions import validate_username

        assert validate_username("alice123") is True
        assert validate_username("user_name") is True

    def test_validate_username_invalid(self, solutions) -> None:
        """测试无效的用户名"""
        from solutions import validate_username

        assert validate_username("ab") is False  # 太短
        assert validate_username("user-name") is False  # 包含连字符
