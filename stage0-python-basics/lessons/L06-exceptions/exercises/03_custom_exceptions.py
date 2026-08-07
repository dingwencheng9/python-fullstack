"""L06 练习3: 自定义异常类 [演示型练习]

难度: ⭐⭐⭐☆☆ (中等进阶)
预计时间: 25 分钟
知识点: 自定义异常类、异常继承、异常链

前置知识:
本练习需要先理解异常处理基础（练习1和练习2）。
自定义异常是构建可维护错误处理系统的核心技能。

模式说明:
本练习采用"演示型"模式 - 提供完整实现供学习理解。
学员可以通过阅读代码、运行 if __name__ == '__main__' 测试块来验证行为。
"""


# ============ 练习 1: 创建自定义异常类 ============


class InvalidAgeError(ValueError):
    """年龄验证错误

    当年龄不在合法范围 (1-150) 时抛出。
    """

    def __init__(self, age: int) -> None:
        self.age = age
        super().__init__(f"无效的年龄: {age}，年龄必须在 1-150 之间")


class InvalidEmailError(ValueError):
    """邮箱验证错误

    当邮箱格式无效时抛出。
    """

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"无效的邮箱地址: {email}")


# ============ 练习 2: 验证函数 ============


def validate_age(age: int) -> int:
    """验证年龄是否合法 (1-150)

    Args:
        age: 年龄值

    Returns:
        验证通过的年龄

    Raises:
        InvalidAgeError: 当年龄不在 1-150 之间时
    """
    if age < 1 or age > 150:
        raise InvalidAgeError(age)
    return age


def validate_email(email: str) -> str:
    """验证邮箱格式

    Args:
        email: 邮箱地址

    Returns:
        验证通过的邮箱

    Raises:
        InvalidEmailError: 当邮箱格式无效时
    """
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


# ============ 练习 3: 组合验证 ============


def validate_user(username: str, age: int, email: str) -> dict[str, str]:
    """验证用户信息

    Args:
        username: 用户名
        age: 年龄
        email: 邮箱

    Returns:
        验证通过的用户信息字典

    Raises:
        ValueError: 用户名为空时
        InvalidAgeError: 年龄无效时
        InvalidEmailError: 邮箱无效时
    """
    normalized_username = username.strip()
    if not normalized_username:
        raise ValueError("用户名不能为空")

    validate_age(age)
    validate_email(email)

    return {"username": normalized_username, "age": str(age), "email": email}


# ============ 练习 4: 收集多个错误 ============
# 进阶挑战：注册时收集所有错误，一次性报告


def register_user(username: str, age: int, email: str) -> dict[str, str]:
    """注册用户，收集所有验证错误

    与 validate_user 不同，这个函数会尝试执行所有验证，
    收集所有错误后一次性报告，而不是遇到第一个错误就停止。

    Args:
        username: 用户名
        age: 年龄
        email: 邮箱

    Returns:
        验证通过的用户信息字典

    Raises:
        ValueError: 包含所有错误信息的汇总消息
    """
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


# ============ 测试代码 ============
if __name__ == "__main__":
    print("=== 自定义异常练习 ===\n")

    # 测试 1: validate_age
    print("1. validate_age:")
    try:
        result = validate_age(25)
        print(f"   validate_age(25) = {result}")
    except InvalidAgeError as e:
        print(f"   ❌ 年龄验证失败: {e}")

    try:
        validate_age(-5)
    except InvalidAgeError as e:
        print(f"   ✓ 捕获 InvalidAgeError: {e}")

    # 测试 2: validate_email
    print("\n2. validate_email:")
    try:
        result = validate_email("user@example.com")
        print(f"   validate_email('user@example.com') = {result}")
    except InvalidEmailError as e:
        print(f"   ❌ 邮箱验证失败: {e}")

    try:
        validate_email("invalid-email")
    except InvalidEmailError as e:
        print(f"   ✓ 捕获 InvalidEmailError: {e}")

    # 测试 3: validate_user
    print("\n3. validate_user:")
    try:
        result = validate_user("alice", 25, "alice@example.com")
        print(f"   ✓ 验证通过: {result}")
    except Exception as e:
        print(f"   ❌ 验证失败: {e}")

    # 测试 4: register_user（收集多个错误）
    print("\n4. register_user（收集多个错误）:")
    try:
        result = register_user("", -5, "not-an-email")
        print(f"   ❌ 不应该到这里: {result}")
    except ValueError as e:
        print(f"   ✓ 收集到多个错误: {e}")
