"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L11: 生成器与迭代器 - itertools 练习测试
"""


def test_first_n():
    """测试返回前 n 个元素"""
    result = itertools_exercises.first_n(5, range(100))
    assert result == [0, 1, 2, 3, 4]


def test_first_n_more_than_available():
    """测试 n 大于可用元素"""
    result = itertools_exercises.first_n(10, range(5))
    assert result == [0, 1, 2, 3, 4]


def test_running_total():
    """测试累积和"""
    result = itertools_exercises.running_total([1, 2, 3, 4])
    assert result == [1, 3, 6, 10]


def test_running_total_empty():
    """测试空列表"""
    result = itertools_exercises.running_total([])
    assert result == []


def test_group_consecutive():
    """测试连续元素分组"""
    result = itertools_exercises.group_consecutive([1, 1, 2, 2, 2, 3])
    assert result == {1: [1, 1], 2: [2, 2, 2], 3: [3]}


def test_all_combinations():
    """测试组合"""
    result = itertools_exercises.all_combinations([1, 2, 3], 2)
    assert result == [(1, 2), (1, 3), (2, 3)]


def test_all_permutations():
    """测试排列"""
    result = itertools_exercises.all_permutations([1, 2, 3], 2)
    assert result == [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]


def test_interleave():
    """测试交替合并"""
    result = itertools_exercises.interleave([1, 4], [2, 5], [3, 6])
    assert result == [1, 2, 3, 4, 5, 6]


def test_interleave_uneven():
    """测试不均匀长度的交替合并"""
    result = itertools_exercises.interleave([1, 2], [3])
    assert result == [1, 3, 2]
