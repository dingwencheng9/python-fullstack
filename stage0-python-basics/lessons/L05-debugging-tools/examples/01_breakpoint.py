"""L05 示例 1: breakpoint() 内置函数

演示 Python 3.7+ 的 breakpoint() 内置函数及其配置。
运行方式: uv run python examples/01_breakpoint.py
"""


def factorial(n):
    """计算阶乘"""
    if n < 0:
        raise ValueError("负数没有阶乘")
    if n <= 1:
        return 1

    breakpoint()  # 使用 breakpoint() 而不是 pdb.set_trace()

    result = 1
    for i in range(2, n + 1):
        result *= i

    return result


def calculate_combination(n, r):
    """计算组合数 C(n, r) = n! / (r! * (n-r)!)"""
    breakpoint()

    # 计算 n! / r!
    numerator = factorial(n) // factorial(r)
    # 计算 (n-r)!
    denominator = factorial(n - r)

    return numerator // denominator


if __name__ == "__main__":
    # 测试数据
    print("计算组合数 C(5, 2):")

    # breakpoint() 会调用 sys.breakpointhook()
    # 可以通过环境变量 PYTHONBREAKPOINT 配置:
    # - PYTHONBREAKPOINT=pdb.set_trace (默认)
    # - PYTHONBREAKPOINT=ipdb.set_trace (需要安装 ipdb)
    # - PYTHONBREAKPOINT= (禁用断点)

    result = calculate_combination(5, 2)
    print(f"C(5, 2) = {result}")
    print("预期结果: 10")

    # 在命令行禁用断点运行:
    # PYTHONBREAKPOINT= uv run python examples/01_breakpoint.py
