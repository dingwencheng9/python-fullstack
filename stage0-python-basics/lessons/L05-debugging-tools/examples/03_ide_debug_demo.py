"""L05 示例 3: IDE 调试示例（模拟）

演示在 IDE 中调试时的常见场景。
此文件用于展示调试技巧，不包含实际断点。

运行方式: uv run python examples/03_ide_debug_demo.py
"""


def find_max(numbers):
    """查找列表中的最大值"""
    if not numbers:
        raise ValueError("列表不能为空")

    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num

    return max_val


def find_min_max(numbers):
    """同时查找最大值和最小值"""
    if not numbers:
        raise ValueError("列表不能为空")

    min_val = numbers[0]
    max_val = numbers[0]

    for num in numbers:
        if num < min_val:
            min_val = num
        if num > max_val:
            max_val = num

    return min_val, max_val


def normalize_numbers(numbers):
    """将数字列表归一化到 0-1 范围"""
    if not numbers:
        return []

    min_val, max_val = find_min_max(numbers)
    range_val = max_val - min_val

    if range_val == 0:
        return [0.0] * len(numbers)

    normalized = []
    for num in numbers:
        normalized.append((num - min_val) / range_val)

    return normalized


if __name__ == "__main__":
    # 测试数据
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    print("归一化示例:")
    print(f"原始数据: {data}")
    print(f"最大值: {find_max(data)}")
    print(f"归一化结果: {normalize_numbers(data)}")

    # 调试技巧:
    # 1. 在函数入口设置断点，检查输入参数
    # 2. 在循环内设置条件断点，特定值时暂停
    # 3. 使用 "Watch" 监视 normalized 列表的变化
    # 4. 使用 "Call Stack" 查看函数调用链
