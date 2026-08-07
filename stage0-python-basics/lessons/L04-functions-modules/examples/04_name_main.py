"""示例：__name__ 与入口点

演示 __name__ 变量的作用和 if __name__ == "__main__" 模式。
"""


def factorial(n: int) -> int:
    """计算阶乘"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """计算斐波那契数列第 n 项"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def run_tests() -> None:
    """运行测试用例"""
    print("运行测试...")
    assert factorial(5) == 120, "factorial(5) 应该等于 120"
    assert factorial(0) == 1, "factorial(0) 应该等于 1"
    assert factorial(1) == 1, "factorial(1) 应该等于 1"

    assert fibonacci(0) == 0, "fibonacci(0) 应该等于 0"
    assert fibonacci(1) == 1, "fibonacci(1) 应该等于 1"
    assert fibonacci(6) == 8, "fibonacci(6) 应该等于 8"
    print("✓ 所有测试通过!")


# ============ 入口点模式 ============
# 当模块被直接运行时，__name__ == "__main__"
# 当模块被导入时，__name__ == "module_name"

if __name__ == "__main__":
    print(f"当前模块名称: {__name__}")
    print("模块被直接运行，执行测试代码\n")

    # 运行测试
    run_tests()

    # 运行示例计算
    print("\n示例计算:")
    print(f"factorial(10) = {factorial(10)}")
    print(f"fibonacci(10) = {fibonacci(10)}")
else:
    print(f"模块被导入: {__name__}")
    print("提示：直接运行此文件查看完整测试输出")
