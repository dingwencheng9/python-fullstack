"""计算器模块 - 参考解答"""


def add(a: float, b: float) -> float:
    """加法"""
    return a + b


def subtract(a: float, b: float) -> float:
    """减法"""
    return a - b


def multiply(a: float, b: float) -> float:
    """乘法"""
    return a * b


def divide(a: float, b: float) -> float | None:
    """除法（除数为0时返回None）"""
    if b == 0:
        return None
    return a / b


if __name__ == "__main__":
    # 测试代码
    print("=== 计算器测试 ===")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")
    print(f"20 / 4 = {divide(20, 4)}")
    print(f"10 / 0 = {divide(10, 0)}")
