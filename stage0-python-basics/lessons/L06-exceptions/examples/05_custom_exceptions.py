"""示例5: 自定义异常类"""


class ValidationError(Exception):
    """验证错误基类"""

    def __init__(self, message: str, field: str | None = None) -> None:
        self.field = field
        super().__init__(message)


class EmailValidationError(ValidationError):
    """邮箱验证错误"""

    def __init__(self, email: str) -> None:
        super().__init__(f"无效的邮箱地址: {email}", field="email")


class PasswordValidationError(ValidationError):
    """密码验证错误"""

    def __init__(self, reason: str) -> None:
        super().__init__(reason, field="password")


def validate_email(email: str) -> str:
    """验证邮箱格式"""
    if "@" not in email:
        raise EmailValidationError(email)
    if "." not in email.rsplit("@", maxsplit=1)[-1]:
        raise EmailValidationError(email)
    return email


def validate_password(password: str) -> str:
    """验证密码强度"""
    if len(password) < 8:
        raise PasswordValidationError("密码至少需要8个字符")
    if not any(c.isdigit() for c in password):
        raise PasswordValidationError("密码必须包含数字")
    if not any(c.isupper() for c in password):
        raise PasswordValidationError("密码必须包含大写字母")
    return password


def register_user(email: str, password: str) -> dict[str, str]:
    """用户注册"""
    errors: list[str] = []
    user_data: dict[str, str] = {}

    try:
        user_data["email"] = validate_email(email)
    except EmailValidationError as e:
        errors.append(str(e))

    try:
        user_data["password"] = validate_password(password)
    except PasswordValidationError as e:
        errors.append(str(e))

    if errors:
        raise ValidationError("; ".join(errors))

    return user_data


# 测试
try:
    user = register_user("alice@example.com", "Pass1234")
    print(f"注册成功: {user}")
except ValidationError as e:
    print(f"注册失败: {e}")


try:
    user = register_user("invalid-email", "weak")
    print(f"注册成功: {user}")
except ValidationError as e:
    print(f"注册失败: {e}")
