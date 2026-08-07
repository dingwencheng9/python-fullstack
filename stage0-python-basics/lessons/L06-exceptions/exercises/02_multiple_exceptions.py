"""L06 练习2: 多个异常类型

难度: ⭐⭐☆ (中等)
预计时间: 20 分钟
知识点: 多个 except 子句、异常类型区分、异常链

任务要求:
1. 实现 process_number 函数，处理 ValueError、TypeError、ZeroDivisionError
2. 实现 validate_user_input 函数，处理多种验证错误

提示:
1. 使用多个 except 子句处理不同类型错误
2. 区分不同类型的错误，返回不同结果
3. except (ValueError, TypeError): 可捕获多种异常
"""


def process_number(value: str, divisor: str) -> float | None:
    """处理数字字符串的除法运算

    捕获:
    - ValueError: 无法转换为数字
    - ZeroDivisionError: 除数为零
    - TypeError: 类型错误
    """
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
    """验证用户输入

    返回:
        {"username": xxx, "age": xxx} 或抛出异常

    捕获:
    - ValueError: 各种验证错误
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
    print(f"process_number('10', '2') = {process_number('10', '2')}")  # 预期: 5.0
    print(f"process_number('10', '0') = {process_number('10', '0')}")  # 预期: None
    print(f"process_number('abc', '2') = {process_number('abc', '2')}")  # 预期: None

    # 测试 validate_user_input
    try:
        result = validate_user_input("alice", "25")
        print(f"validate_user_input 成功: {result}")
    except Exception as e:
        print(f"validate_user_input 失败: {e}")
