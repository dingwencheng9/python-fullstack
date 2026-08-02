"""L05 练习 1 参考解答: pdb 基础"""



def calculate_average(numbers):
    """计算平均值 - 已修复"""
    if not numbers:
        raise ValueError("列表不能为空，无法计算平均值")

    total = 0
    for num in numbers:
        total += num
    count = len(numbers)
    return total / count


def find_middle_element(items):
    """返回列表中间的元素 - 已修复

    对于偶数长度的列表，返回中间两个元素之一是合理的行为
    但为了更明确，这里返回靠左的中间元素
    """
    if not items:
        raise ValueError("列表不能为空")

    length = len(items)
    middle_index = length // 2
    return items[middle_index]


if __name__ == "__main__":
    print("测试修复后的代码:")
    print("-" * 50)

    # 测试 1: 空列表
    print("\n测试 1: 空列表")
    try:
        result = calculate_average([])
        print(f"平均值: {result}")
    except ValueError as e:
        print(f"已处理的错误: {e}")

    # 测试 2: 偶数长度列表
    print("\n测试 2: 偶数长度列表")
    data = [1, 2, 3, 4]
    middle = find_middle_element(data)
    print(f"中间元素 (索引 {len(data)//2}): {middle}")
    print("说明: 对于 [1,2,3,4]，索引 2 位置的值是 3")
