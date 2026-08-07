"""L05 练习 1: pdb 基础

使用 pdb 调试以下代码，找到问题所在。
"""


def calculate_average(numbers):
    """计算平均值"""
    # TODO: 这个函数有个问题，请使用 pdb 调试找到它
    total = 0
    for num in numbers:
        total += num
    count = len(numbers)

    # 这里忘记检查除以零的情况
    return total / count


def find_middle_element(items):
    """返回列表中间的元素"""
    # TODO: 使用 pdb 调试找到问题
    length = len(items)
    middle_index = length // 2
    return items[middle_index]


if __name__ == "__main__":
    # 测试 1: 空列表
    print("测试 1: 空列表")
    result = calculate_average([])
    print(f"平均值: {result}")

    # 测试 2: 偶数长度的列表
    print("\n测试 2: 偶数长度列表")
    data = [1, 2, 3, 4]
    middle = find_middle_element(data)
    print(f"中间元素: {middle}")  # 预期是什么？实际是什么？

    # 调试步骤:
    # 1. 运行: uv run python exercises/01_pdb_practice.py
    # 2. 在 pdb 中使用 'n' 单步执行
    # 3. 使用 'p variable_name' 查看变量值
    # 4. 使用 'l' 查看当前代码上下文
    # 5. 找到问题后，修复代码
