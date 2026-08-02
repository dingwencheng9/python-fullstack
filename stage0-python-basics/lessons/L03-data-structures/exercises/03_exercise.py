"""L03 练习3: 生成器表达式性能优化

难度: ⭐⭐☆ (中等)
预计时间: 25 分钟
知识点: 列表推导式 vs 生成器表达式、内存优化、惰性计算


任务描述:
TODO: 用生成器表达式优化大数据处理

提示:
1. 列表推导式 [x for x] 会创建完整列表
2. 生成器表达式 (x for x) 惰性计算，节省内存
3. sum((x**2 for x in range(n))) 不需要中间列表
"""


def sum_of_squares_list(n: int) -> int:
    """用列表推导式计算 1^2 + 2^2 + ... + n^2

    列表推导式会在内存中创建中间列表。
    """
    return sum([x ** 2 for x in range(1, n + 1)])


def sum_of_squares_gen(n: int) -> int:
    """用生成器表达式计算 1^2 + 2^2 + ... + n^2

    生成器表达式是惰性求值，适合大数据场景以节省内存。
    """
    return sum(x ** 2 for x in range(1, n + 1))


def count_long_words(words: list[str], min_length: int) -> int:
    """
    统计长度大于等于 min_length 的单词数量。

    要求:
    1. 用生成器表达式 + sum() 实现
    2. 不创建中间列表
    3. 必须带类型注解
    """
    return sum(1 for w in words if len(w) >= min_length)


if __name__ == "__main__":
    # 测试结果一致性
    assert sum_of_squares_list(10) == sum_of_squares_gen(10) == 385
    print("✅ 求和测试通过")

    # 测试词数统计
    words: list[str] = ["hello", "hi", "world", "a", "Python", "ok"]
    assert count_long_words(words, 5) == 3  # "hello", "world", "Python" — 3 个
    print("✅ 词数测试通过")
