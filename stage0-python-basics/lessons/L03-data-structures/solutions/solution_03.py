"""L03 练习3 参考答案"""


def sum_of_squares_list(n: int) -> int:
    """列表推导式实现"""
    return sum([x**2 for x in range(1, n + 1)])


def sum_of_squares_gen(n: int) -> int:
    """生成器表达式实现（省内存）"""
    return sum(x**2 for x in range(1, n + 1))


def count_long_words(words: list[str], min_length: int) -> int:
    """生成器表达式 + sum 统计长词"""
    return sum(1 for w in words if len(w) >= min_length)
