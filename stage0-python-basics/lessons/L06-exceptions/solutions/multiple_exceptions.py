"""练习2参考答案: 多个异常类型"""

# ruff: noqa: N999


def process_number(value: str, divisor: str) -> float | None:
    """处理数字字符串的除法运算"""
    try:
        x = float(value)
        y = float(divisor)
        return x / y
    except ValueError:
        print("错误: 无法将输入转换为数字")
        return None
    except ZeroDivisionError:
        print("错误: 除数不能为零")
        return None
    except TypeError:
        print("错误: 输入类型错误")
        return None


def validate_user_input(username: str, age: str) -> dict[str, str]:
    """验证用户输入。

    Args:
        username: 用户名，不能为空或纯空白。
        age: 年龄字符串，必须可解析为 0-150 的整数。

    Returns:
        规范化后的用户数据。

    Raises:
        ValueError: 用户名为空、年龄不是整数或年龄超出范围。
    """
    normalized_username = username.strip()
    if not normalized_username:
        raise ValueError("用户名不能为空")

    try:
        age_int = int(age)
    except ValueError:
        raise ValueError("年龄必须是有效数字") from None

    if age_int < 0 or age_int > 150:
        raise ValueError("年龄必须在 0-150 之间")

    return {"username": normalized_username, "age": str(age_int)}


# 测试代码
if __name__ == "__main__":
    # 测试 process_number
    print(f"process_number('10', '2') = {process_number('10', '2')}")  # 5.0
    print(f"process_number('10', '0') = {process_number('10', '0')}")  # None
    print(f"process_number('abc', '2') = {process_number('abc', '2')}")  # None

    # 测试 validate_user_input
    try:
        result = validate_user_input("alice", "25")
        print(f"validate_user_input 成功: {result}")
    except Exception as e:
        print(f"validate_user_input 失败: {e}")
