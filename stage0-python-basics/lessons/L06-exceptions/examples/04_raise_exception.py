"""示例4: 异常的传递与 raise"""


def validate_age(age: int) -> int:
    """验证年龄"""
    if age < 0:
        raise ValueError("年龄不能为负数")
    if age > 150:
        raise ValueError("年龄超出合理范围")
    return age


def get_age_category(age: int) -> str:
    """获取年龄类别"""
    age = validate_age(age)
    if age < 18:
        return "未成年"
    if age < 65:
        return "成年人"
    return "老年人"


def safe_get_age_category(age: int) -> str | None:
    """安全的年龄类别获取"""
    try:
        return get_age_category(age)
    except ValueError as e:
        print(f"验证失败: {e}")
        return None


# 测试
print(safe_get_age_category(25))  # 成年人
print(safe_get_age_category(-5))  # 验证失败: 年龄不能为负数
print(safe_get_age_category(200))  # 验证失败: 年龄超出合理范围


def divide_with_raise(a: float, b: float) -> float:
    """除法，异常时抛出自定义错误"""
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b


try:
    result = divide_with_raise(10, 0)
except ZeroDivisionError as e:
    print(f"捕获异常: {e}")
