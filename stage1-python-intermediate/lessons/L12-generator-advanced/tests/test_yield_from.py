"""L12 生成器进阶 - yield from 测试

使用根 conftest.py 提供的 solutions fixture，避免 sys.path 污染。
"""

import pytest


class TestFlatten:
    def test_flatten_simple(self, solutions):
        flatten = getattr(solutions, "flatten")
        data = [[1, 2], [3, 4], [5, [6, 7]]]
        result = list(flatten(data))
        assert result == [1, 2, 3, 4, 5, 6, 7]

    def test_flatten_deep(self, solutions):
        flatten = getattr(solutions, "flatten")
        data = [1, [2, [3, [4, [5]]]]]
        result = list(flatten(data))
        assert result == [1, 2, 3, 4, 5]


class TestTraverseTree:
    def test_simple_tree(self, solutions):
        traverse_tree = getattr(solutions, "traverse_tree")
        tree = {"val": 1, "left": {"val": 2}, "right": {"val": 3}}
        result = list(traverse_tree(tree))
        assert result == [1, 2, 3]


class TestMergeSorted:
    def test_two_lists(self, solutions):
        merge_sorted = getattr(solutions, "merge_sorted")
        result = list(merge_sorted([1, 3, 5], [2, 4, 6]))
        assert result == [1, 2, 3, 4, 5, 6]


class TestChainIterables:
    def test_chain(self, solutions):
        chain_iterables = getattr(solutions, "chain_iterables")
        result = list(chain_iterables([1, 2], "ab", (3, 4)))
        assert result == [1, 2, "a", "b", 3, 4]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
