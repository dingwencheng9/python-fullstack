"""L03 练习1: 数据处理

难度: ⭐☆☆ (入门)
预计时间: 15 分钟
知识点: 列表推导式、字典操作、字符串处理


任务描述:
TODO: 实现数据筛选和统计

提示:
1. filter_positive: 使用列表推导式 [x for x in nums if x > 0]
2. word_count: 使用 split() 分词，用字典统计频次
3. 注意边界情况（空列表、空字符串）
"""


def filter_positive(nums: list[int]) -> list[int]:
    """筛选正数。"""
    return [x for x in nums if x > 0]


def word_count(text: str) -> dict[str, int]:
    """词频统计。"""
    words = text.lower().split()
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


if __name__ == "__main__":
    print(filter_positive([1, -2, 3, -4, 5]))
    print(word_count("hello world hello"))
