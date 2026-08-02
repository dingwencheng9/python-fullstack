"""参考答案 4: 循环与循环控制"""


def find_first_negative(numbers) -> int:
    """查找第一个负数。

    Args:
        numbers: 整数列表

    Returns:
        第一个负数，如果不存在返回 None

    Examples:
        >>> find_first_negative([1, 2, -3, 4, 5])
        -3
        >>> find_first_negative([1, 2, 3])
        None
    """
    # 使用循环 else 子句实现
    for num in numbers:
        if num < 0:
            return num
    return None


def sum_until_negative(numbers) -> int:
    """累加直到遇到负数。

    Args:
        numbers: 整数列表

    Returns:
        从头开始累加，直到遇到负数为止的和（不包含负数）

    Examples:
        >>> sum_until_negative([1, 2, 3, 4, 5])
        15
        >>> sum_until_negative([1, 2, -3, 4, 5])
        3
        >>> sum_until_negative([-1, 2, 3])
        0
    """
    # 使用 break 实现
    total = 0
    for num in numbers:
        if num < 0:
            break
        total += num
    return total


def skip_zeros(numbers) -> list:
    """跳过列表中的零，返回非零元素的平方。

    Args:
        numbers: 整数列表

    Returns:
        非零元素的平方列表

    Examples:
        >>> skip_zeros([1, 0, 2, 0, 3])
        [1, 4, 9]
        >>> skip_zeros([0, 0, 1])
        [1]
        >>> skip_zeros([0, 0, 0])
        []
    """
    # 使用 continue 跳过零
    result = []
    for num in numbers:
        if num == 0:
            continue
        result.append(num**2)
    return result


def countdown(start: int) -> list:
    """生成倒计时序列。

    Args:
        start: 起始数字

    Returns:
        从 start 到 1 的倒计时列表

    Examples:
        >>> countdown(5)
        [5, 4, 3, 2, 1]
        >>> countdown(1)
        [1]
        >>> countdown(0)
        []
    """
    # 使用 while 循环实现
    result = []
    while start > 0:
        result.append(start)
        start -= 1
    return result


def fibonacci(n: int) -> list:
    """生成前 n 个斐波那契数。

    Args:
        n: 数量

    Returns:
        前 n 个斐波那契数列表

    Examples:
        >>> fibonacci(7)
        [1, 1, 2, 3, 5, 8, 13]
        >>> fibonacci(1)
        [1]
        >>> fibonacci(0)
        []
    """
    # 循环实现斐波那契数列
    # 1, 1, 2, 3, 5, 8, 13, 21, ...
    if n <= 0:
        return []
    if n == 1:
        return [1]

    result = [1, 1]
    while len(result) < n:
        result.append(result[-1] + result[-2])
    return result


if __name__ == "__main__":
    print("=== 查找第一个负数测试 ===")
    tests = [
        ([1, 2, -3, 4, 5], -3),
        ([1, 2, 3], None),
        ([], None),
        ([-5, 1, 2], -5),
    ]
    for numbers, expected in tests:
        result = find_first_negative(numbers)
        status = "✓" if result == expected else "✗"
        print(f"{status} find_first_negative({numbers}) = {result}")

    print("\n=== 累加到负数测试 ===")
    tests = [
        ([1, 2, 3, 4, 5], 15),
        ([1, 2, -3, 4, 5], 3),
        ([-1, 2, 3], 0),
        ([], 0),
    ]
    for numbers, expected in tests:
        result = sum_until_negative(numbers)
        status = "✓" if result == expected else "✗"
        print(f"{status} sum_until_negative({numbers}) = {result}")

    print("\n=== 跳过零测试 ===")
    tests = [
        ([1, 0, 2, 0, 3], [1, 4, 9]),
        ([0, 0, 1], [1]),
        ([0, 0, 0], []),
        ([1, 2, 3], [1, 4, 9]),
    ]
    for numbers, expected in tests:
        result = skip_zeros(numbers)
        status = "✓" if result == expected else "✗"
        print(f"{status} skip_zeros({numbers}) = {result}")

    print("\n=== 倒计时测试 ===")
    tests = [(5, [5, 4, 3, 2, 1]), (1, [1]), (0, [])]
    for n, expected in tests:
        result = countdown(n)
        status = "✓" if result == expected else "✗"
        print(f"{status} countdown({n}) = {result}")

    print("\n=== 斐波那契数列测试 ===")
    tests = [(7, [1, 1, 2, 3, 5, 8, 13]), (1, [1]), (0, [])]
    for n, expected in tests:
        result = fibonacci(n)
        status = "✓" if result == expected else "✗"
        print(f"{status} fibonacci({n}) = {result}")
