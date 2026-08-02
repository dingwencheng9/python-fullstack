"""
L15: 函数式编程 - 函数式管道练习解答

使用 map/filter/reduce 实现数据处理。
"""

from functools import reduce


def process_data(data: list[int]) -> int:
    """过滤偶数 -> 平方 -> 求和（支持空列表）"""
    return reduce(
        lambda acc, x: acc + x,
        map(lambda x: x**2, filter(lambda x: x % 2 == 0, data)),
        0,  # initial=0，空列表时返回 0
    )


def transform_strings(strings: list[str]) -> list[str]:
    """过滤空字符串 -> 转大写 -> 排序"""
    return sorted(map(str.upper, filter(bool, strings)))


def compose(*functions):
    """函数组合: f ∘ g"""

    def composed(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result

    return composed


def pipe(*functions):
    """管道组合: f | g"""

    def piped(x):
        result = x
        for func in functions:
            result = func(result)
        return result

    return piped
