"""示例5: 自定义异常类"""


# ============ 自定义异常类定义 ============


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


# ============ 使用自定义异常的验证函数 ============


def validate_age(age: int) -> int:
    """验证年龄是否合法 (1-150)"""
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
    if not local or not domain or "." not in domain:
        raise InvalidEmailError(email)
    return email


# ============ 测试 ============
print("=== 自定义异常类示例 ===\n")

# 测试年龄验证
print("1. validate_age:")
try:
    result = validate_age(25)
    print(f"   validate_age(25) = {result}")  # 25
except InvalidAgeError as e:
    print(f"   ❌ {e}")

try:
    validate_age(-5)
except InvalidAgeError as e:
    print(f"   ✓ 捕获 InvalidAgeError: {e}")  # 捕获成功

# 测试邮箱验证
print("\n2. validate_email:")
try:
    result = validate_email("user@example.com")
    print(f"   validate_email('user@example.com') = {result}")
except InvalidEmailError as e:
    print(f"   ❌ {e}")

try:
    validate_email("invalid-email")
except InvalidEmailError as e:
    print(f"   ✓ 捕获 InvalidEmailError: {e}")  # 捕获成功
