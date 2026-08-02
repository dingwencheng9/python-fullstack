"""L18 练习5 参考：工具链综合"""

from __future__ import annotations


def add(a: int, b: int) -> int:
    return a + b


def test_add() -> None:
    assert add(2, 3) == 5
