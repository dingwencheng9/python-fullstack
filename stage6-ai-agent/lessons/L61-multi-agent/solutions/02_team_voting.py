"""L54 练习2 参考：多 Agent 投票"""

from __future__ import annotations

from collections import Counter


def majority_vote(answers: list[str]) -> str:
    """
    取多数投票结果

    Args:
        answers: 字符串列表，表示各个投票者的投票结果

    Returns:
        str: 出现次数最多的投票结果。在平票情况下，返回第一个遇到的最多元素。

    Raises:
        ValueError: 当输入列表为空时抛出
    """
    if not answers:
        raise ValueError("输入列表不能为空")

    # 使用Counter统计每个答案的出现次数
    counter = Counter(answers)

    # 获取出现次数最多的答案
    # 在平票情况下，返回第一个遇到的最多元素
    return counter.most_common(1)[0][0]
