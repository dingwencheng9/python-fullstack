"""参考答案 4: 循环与循环控制

对应练习: exercises/04_loops.py
知识点: for/while 循环、break/continue、循环 else 子句

本参考答案为演示型练习的完整实现版本。
"""


def find_first_negative(numbers):
    """查找第一个负数。

    Args:
        numbers: 整数列表

    Returns:
        第一个负数，如果不存在返回 None
    """
    for n in numbers:
        if n < 0:
            return n
    return None


def sum_until_negative(numbers):
    """累加直到遇到负数。

    Args:
        numbers: 整数列表

    Returns:
        从头开始累加，直到遇到负数为止的和（不包含负数）
    """
    total = 0
    for n in numbers:
        if n < 0:
            break
        total += n
    return total


def skip_zeros(numbers):
    """跳过列表中的零，返回非零元素的平方。

    Args:
        numbers: 整数列表

    Returns:
        非零元素的平方列表
    """
    result = []
    for n in numbers:
        if n == 0:
            continue
        result.append(n * n)
    return result


def countdown(start):
    """生成倒计时序列。

    Args:
        start: 起始数字

    Returns:
        从 start 到 1 的倒计时列表
    """
    result = []
    while start > 0:
        result.append(start)
        start -= 1
    return result


def fibonacci(n):
    """生成前 n 个斐波那契数。

    Args:
        n: 数量

    Returns:
        前 n 个斐波那契数列表
    """
    if n <= 0:
        return []
    if n == 1:
        return [1]
    result = [1, 1]
    while len(result) < n:
        result.append(result[-1] + result[-2])
    return result


if __name__ == '__main__':
    print('=== 查找第一个负数测试 ===')
    tests = [([1, 2, -3, 4, 5], -3), ([1, 2, 3], None), ([], None), ([-5, 1, 2], -5)]
    for numbers, expected in tests:
        result = find_first_negative(numbers)
        status = '✓' if result == expected else '✗'
        print(f'{status} find_first_negative({numbers}) = {result}')

    print('\n=== 累加到负数测试 ===')
    tests = [([1, 2, 3, 4, 5], 15), ([1, 2, -3, 4, 5], 3), ([-1, 2, 3], 0), ([], 0)]
    for numbers, expected in tests:
        result = sum_until_negative(numbers)
        status = '✓' if result == expected else '✗'
        print(f'{status} sum_until_negative({numbers}) = {result}')

    print('\n=== 跳过零测试 ===')
    tests = [([1, 0, 2, 0, 3], [1, 4, 9]), ([0, 0, 1], [1]), ([0, 0, 0], []), ([1, 2, 3], [1, 4, 9])]
    for numbers, expected in tests:
        result = skip_zeros(numbers)
        status = '✓' if result == expected else '✗'
        print(f'{status} skip_zeros({numbers}) = {result}')

    print('\n=== 倒计时测试 ===')
    tests = [(5, [5, 4, 3, 2, 1]), (1, [1]), (0, [])]
    for n, expected in tests:
        result = countdown(n)
        status = '✓' if result == expected else '✗'
        print(f'{status} countdown({n}) = {result}')

    print('\n=== 斐波那契数列测试 ===')
    tests = [(7, [1, 1, 2, 3, 5, 8, 13]), (1, [1]), (0, [])]
    for n, expected in tests:
        result = fibonacci(n)
        status = '✓' if result == expected else '✗'
        print(f'{status} fibonacci({n}) = {result}')
