"""练习3参考答案: 自定义异常类"""

# ruff: noqa: N999


class InvalidAgeError(ValueError):
    """年龄验证错误"""

    def __init__(self, age: int) -> None:
        self.age = age
        super().__init__(f"无效的年龄: {age}，年龄必须在 1-150 之间")


class InvalidEmailError(ValueError):
    """邮箱验证错误"""

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"无效的邮箱地址: {email}")


def validate_age(age: int) -> int:
    """验证年龄 (1-150)"""
    if age < 1 or age > 150:
        raise InvalidAgeError(age)
    return age


def validate_email(email: str) -> str:
    """验证邮箱格式"""
    if not email:
        raise InvalidEmailError("邮箱不能为空")

    if "@" not in email:
        raise InvalidEmailError(email)

    local, domain = email.split("@", 1)
    if not local or not domain:
        raise InvalidEmailError(email)

    if "." not in domain:
        raise InvalidEmailError(email)

    return email


def validate_user(username: str, age: int, email: str) -> dict[str, str]:
    """验证用户信息，抛出相应的异常"""
    normalized_username = username.strip()
    if not normalized_username:
        raise ValueError("用户名不能为空")

    validate_age(age)
    validate_email(email)

    return {"username": normalized_username, "age": str(age), "email": email}


def register_user(username: str, age: int, email: str) -> dict[str, str]:
    """注册用户，收集所有验证错误"""
    errors: list[str] = []

    normalized_username = username.strip()
    if not normalized_username:
        errors.append("用户名不能为空")

    try:
        validate_age(age)
    except InvalidAgeError as e:
        errors.append(str(e))

    try:
        validate_email(email)
    except InvalidEmailError as e:
        errors.append(str(e))

    if errors:
        raise ValueError("; ".join(errors))

    return {"username": normalized_username, "age": str(age), "email": email}


# 测试代码
if __name__ == "__main__":
    # 测试 validate_age
    try:
        validate_age(25)
        print("年龄 25 验证通过")
    except InvalidAgeError as e:
        print(f"年龄验证失败: {e}")

    try:
        validate_age(-5)
    except InvalidAgeError as e:
        print(f"年龄验证失败: {e}")  # 预期: 年龄必须在 1-150 之间

    # 测试 register_user（收集多个错误）
    try:
        result = register_user("", -5, "invalid")
        print(f"register_user 结果: {result}")
    except ValueError as e:
        print(f"register_user 失败: {e}")
