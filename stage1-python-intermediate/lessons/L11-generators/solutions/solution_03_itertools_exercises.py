"""
L11: 生成器与迭代器 - itertools 练习解答

使用 itertools 模块实现高效迭代。
"""

from itertools import (
    accumulate,
    groupby,
    combinations,
    permutations,
    islice,
    zip_longest,
)


def first_n(n: int, iterable) -> list:
    """返回可迭代对象的前 n 个元素"""
    return list(islice(iterable, n))


def running_total(numbers: list) -> list:
    """计算累积和"""
    return list(accumulate(numbers))


def chunk_iterable(iterable, size: int):
    """将可迭代对象分块"""
    [iter(iterable)] * size
    return list(zip(*[iter(iterable)] * size, strict=True))


def group_consecutive(items: list) -> dict:
    """将连续相同元素分组"""
    result = {}
    for key, group in groupby(items):
        result[key] = list(group)
    return result


def all_combinations(items: list, r: int) -> list:
    """返回所有 r 元素组合"""
    return list(combinations(items, r))


def all_permutations(items: list, r: int) -> list:
    """返回所有 r 元素排列"""
    return list(permutations(items, r))


def interleave(*iterables) -> list:
    """交替合并多个可迭代对象"""
    sentinel = object()
    result = []
    for items in zip_longest(*iterables, fillvalue=sentinel):
        for item in items:
            if item is not sentinel:
                result.append(item)
    return result
