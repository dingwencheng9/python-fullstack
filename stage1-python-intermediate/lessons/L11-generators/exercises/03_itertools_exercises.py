"""
L11: 生成器与迭代器 - itertools 练习

使用 itertools 实现高效的数据处理。
"""

import itertools


def first_n(iterable, n: int):
    """取前n个元素"""
    return list(itertools.islice(iterable, n))


def take_while(predicate, iterable):
    """取满足条件的连续元素"""
    return list(itertools.takewhile(predicate, iterable))


def group_by_key(items: list, key_func):
    """按键分组"""
    result = {}
    for key, group in itertools.groupby(sorted(items, key=key_func), key=key_func):
        result[key] = list(group)
    return result


def sliding_window(items: list, size: int):
    """滑动窗口。"""
    if size <= 0:
        raise ValueError("size 必须为正整数")
    iterators = itertools.tee(items, size)
    for offset, iterator in enumerate(iterators):
        for _ in range(offset):
            next(iterator, None)
    return list(zip(*iterators, strict=False))


def powerset(iterable):
    """生成所有子集。"""
    items = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(items, size) for size in range(len(items) + 1))


# === 验证 ===

if __name__ == "__main__":
    # 测试 first_n
    assert first_n(range(100), 5) == [0, 1, 2, 3, 4]

    # 测试 take_while
    assert take_while(lambda x: x < 5, [1, 2, 3, 6, 7, 8]) == [1, 2, 3]

    # 测试 group_by_key
    items = [("a", 1), ("b", 2), ("a", 3), ("b", 4)]
    grouped = group_by_key(items, lambda x: x[0])
    assert grouped["a"] == [("a", 1), ("a", 3)]
    assert grouped["b"] == [("b", 2), ("b", 4)]

    # 测试 sliding_window
    assert sliding_window([1, 2, 3, 4, 5], 3) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    # 测试 powerset
    result = list(powerset([1, 2, 3]))
    assert len(result) == 8  # 2^3
    assert () in result  # 空集
    assert (1, 2) in result

    print("✅ 所有测试通过！")
