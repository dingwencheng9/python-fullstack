"""
L10: 类型系统 - 类型收窄练习

使用类型守卫和类型守卫函数实现类型安全的代码。
"""

from typing import TypeGuard


def is_string_list(value: list[object]) -> TypeGuard[list[str]]:
    """类型守卫：检查列表是否全是字符串"""
    return all(isinstance(item, str) for item in value)


def is_even(n: int) -> bool:
    """检查是否为偶数"""
    return n % 2 == 0


def is_positive(n: int) -> bool:
    """检查是否为正数"""
    return n > 0


def filter_even(numbers: list[int]) -> list[int]:
    """过滤偶数"""
    return [n for n in numbers if is_even(n)]


def process_mixed(items: list[int | str]) -> tuple[list[int], list[str]]:
    """分离整数和字符串"""
    ints = []
    strs = []
    for item in items:
        if isinstance(item, int):
            ints.append(item)
        else:
            strs.append(item)
    return ints, strs


# === 验证 ===

if __name__ == "__main__":
    # 测试类型守卫
    assert is_string_list(["a", "b", "c"]) is True
    assert is_string_list(["a", 1, "c"]) is False

    # 测试过滤
    assert filter_even([1, 2, 3, 4, 5, 6]) == [2, 4, 6]

    # 测试分离
    ints, strs = process_mixed([1, "a", 2, "b", 3])
    assert ints == [1, 2, 3]
    assert strs == ["a", "b"]

    print("✅ 所有测试通过！")
