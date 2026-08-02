"""
L10: 类型系统 - Protocol 练习

使用 Protocol 定义结构化类型。
"""

from typing import Protocol


class Sized(Protocol):
    """支持大小操作的协议"""

    def __len__(self) -> int: ...


class Comparable(Protocol):
    """可比较协议"""

    def __lt__(self, other) -> bool: ...
    def __gt__(self, other) -> bool: ...


def total_size(items: list[Sized]) -> int:
    """计算所有元素的总大小"""
    return sum(len(item) for item in items)


def find_max[T: Comparable](items: list[T]) -> T | None:
    """找最大值"""
    if not items:
        return None
    max_val = items[0]
    for item in items[1:]:
        max_val = max(max_val, item)
    return max_val


# === 验证 ===

if __name__ == "__main__":
    # 测试 Sized
    assert total_size(["hello", "world"]) == 10
    assert total_size([[1], [2], [3]]) == 3

    # 测试 Comparable
    assert find_max([3, 1, 4, 1, 5]) == 5
    assert find_max([]) is None

    print("✅ 所有测试通过！")
