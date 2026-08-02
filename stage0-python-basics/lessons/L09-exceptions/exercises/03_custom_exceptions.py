"""L08 练习3: 自定义异常类

难度: ⭐⭐☆ (中等)
预计时间: 25 分钟
知识点: 自定义异常类、异常继承、raise 语句、异常信息

任务要求:
1. 定义 InvalidAgeError 异常类（继承自 ValueError）
2. 定义 InvalidEmailError 异常类（继承自 ValueError）
3. 实现 validate_user 函数，使用这些异常
4. 实现 register_user 函数，收集多个错误

提示:
1. 异常类应该有有意义的错误消息
2. raise InvalidAgeError(f"年龄 {age} 无效")
3. register_user 应该能够收集并报告多个错误
"""


class InvalidAgeError(ValueError):
    """年龄验证错误"""


class InvalidEmailError(ValueError):
    """邮箱验证错误"""


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

    local_part, domain_part = email.split("@", 1)
    if not local_part or not domain_part:
        raise InvalidEmailError(email)

    if "." not in domain_part:
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
    except InvalidAgeError as exc:
        errors.append(str(exc))

    try:
        validate_email(email)
    except InvalidEmailError as exc:
        errors.append(str(exc))

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
    result = register_user("", -5, "invalid")
    print(f"register_user 结果: {result}")
