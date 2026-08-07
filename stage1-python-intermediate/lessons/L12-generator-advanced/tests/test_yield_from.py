"""L12 生成器进阶 - yield from 测试"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "solutions"))

from solution_01_yield_from import flatten, traverse_tree, merge_sorted, chain_iterables


class TestFlatten:
    def test_flatten_simple(self):
        data = [[1, 2], [3, 4], [5, [6, 7]]]
        result = list(flatten(data))
        assert result == [1, 2, 3, 4, 5, 6, 7]

    def test_flatten_deep(self):
        data = [1, [2, [3, [4, [5]]]]]
        result = list(flatten(data))
        assert result == [1, 2, 3, 4, 5]


class TestTraverseTree:
    def test_simple_tree(self):
        tree = {"val": 1, "left": {"val": 2}, "right": {"val": 3}}
        result = list(traverse_tree(tree))
        assert result == [1, 2, 3]


class TestMergeSorted:
    def test_two_lists(self):
        result = list(merge_sorted([1, 3, 5], [2, 4, 6]))
        assert result == [1, 2, 3, 4, 5, 6]


class TestChainIterables:
    def test_chain(self):
        result = list(chain_iterables([1, 2], "ab", (3, 4)))
        assert result == [1, 2, "a", "b", 3, 4]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
