"""L04 练习1: 函数基础

难度: ⭐⭐☆ (中等)
预计时间: 25 分钟
知识点: 函数定义、递归、参数传递、异常处理

任务描述:
完成以下函数实现，包括阶乘、斐波那契数列等经典算法。

提示:
1. 递归函数要有终止条件
2. 注意参数验证（如负数检查）
3. 使用 raise ValueError 抛出异常
"""


def factorial(n: int) -> int:
    """计算阶乘

    Args:
        n: 非负整数

    Returns:
        n! 的值

    Raises:
        ValueError: 当 n 为负数时
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """计算斐波那契数列第 n 项

    Args:
        n: 非负整数（从 0 开始计数）

    Returns:
        斐波那契数列第 n 项

    Raises:
        ValueError: 当 n 为负数时
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def find_max(numbers: list[int]) -> int | None:
    """查找列表中的最大值

    Args:
        numbers: 整数列表

    Returns:
        最大值，如果列表为空则返回 None
    """
    if not numbers:
        return None
    return max(numbers)


def filter_even(numbers: list[int]) -> list[int]:
    """过滤出列表中的偶数

    Args:
        numbers: 整数列表

    Returns:
        只包含偶数的新列表
    """
    return [n for n in numbers if n % 2 == 0]


if __name__ == "__main__":
    # 测试函数
    print("=== 函数练习测试 ===")
    print(f"5! = {factorial(5)}")
    print(f"前 10 个斐波那契数: {[fibonacci(i) for i in range(10)]}")
    print(f"最大值: {find_max([3, 1, 4, 1, 5, 9, 2, 6])}")
    print(f"空列表最大值: {find_max([])}")
    print(f"过滤偶数: {filter_even([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])}")
