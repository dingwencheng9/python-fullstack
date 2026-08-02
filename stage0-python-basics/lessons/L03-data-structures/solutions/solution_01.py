"""L03 练习 1 参考答案：列表推导式与字典操作。

演示如何使用列表推导式和字典进行数据处理。
"""


def filter_positive(nums: list[int]) -> list[int]:
    """筛选正数。

    Args:
        nums: 整数列表

    Returns:
        只包含正数的新列表

    Example:
        >>> filter_positive([1, -2, 3, -4, 5])
        [1, 3, 5]
    """
    return [x for x in nums if x > 0]


def word_count(text: str) -> dict[str, int]:
    """词频统计。

    Args:
        text: 输入文本

    Returns:
        单词到出现次数的映射

    Example:
        >>> word_count("hello world hello")
        {'hello': 2, 'world': 1}
    """
    words: list[str] = text.lower().split()
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


if __name__ == "__main__":
    print(filter_positive([1, -2, 3, -4, 5]))
    print(word_count("hello world hello"))
