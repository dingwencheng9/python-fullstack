"""L05 示例 0: pdb 基础用法

演示如何使用 pdb.set_trace() 设置断点进行调试。
运行方式: uv run python examples/00_pdb_basics.py
"""

import pdb


def calculate_sum(numbers):
    """计算数字列表的总和"""
    total = 0
    pdb.set_trace()  # 断点：程序在这里暂停

    for num in numbers:
        total += num

    return total


def calculate_average(numbers):
    """计算数字列表的平均值"""
    pdb.set_trace()  # 断点

    total = calculate_sum(numbers)
    count = len(numbers)

    if count == 0:
        return 0

    return total / count


if __name__ == "__main__":
    # 测试数据
    data = [10, 20, 30, 40, 50]

    print("计算列表平均值:")
    print(f"数据: {data}")

    # 使用 pdb 调试时，可以使用以下命令:
    # n (next) - 执行下一行
    # s (step) - 进入函数
    # c (continue) - 继续执行到下一个断点
    # p variable - 打印变量值
    # l (list) - 查看当前代码上下文
    # q (quit) - 退出调试器

    result = calculate_average(data)
    print(f"平均值: {result}")
