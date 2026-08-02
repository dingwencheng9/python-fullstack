"""示例1: 基础异常处理"""


def divide(a: float, b: float) -> float:
    """除法运算"""
    return a / b


def safe_divide(a: float, b: float) -> float | None:
    """带异常处理的除法"""
    try:
        return a / b
    except ZeroDivisionError:
        print("错误: 除数不能为零")
        return None


# 正常情况
print(f"10 / 2 = {divide(10, 2)}")

# 异常情况
result = safe_divide(10, 0)
print(f"10 / 0 = {result}")
