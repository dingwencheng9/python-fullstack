"""
L11: 生成器与迭代器 - 生成器练习解答

实现各种生成器函数。
"""

from collections.abc import Iterator


def fibonacci(n: int) -> Iterator[int]:
    """生成前 n 个斐波那契数"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def flatten(nested: list) -> Iterator:
    """展平嵌套列表"""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def chunked(data: list, size: int) -> Iterator[list]:
    """将数据分块"""
    for i in range(0, len(data), size):
        yield data[i : i + size]


def prime_numbers(limit: int) -> Iterator[int]:
    """生成小于 limit 的所有素数"""
    sieve = list(range(limit))
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit, i):
                sieve[j] = 0
    for i in range(limit):
        if sieve[i]:
            yield sieve[i]


def pairwise(iterable: list) -> Iterator[tuple]:
    """返回相邻元素对"""
    it = iter(iterable)
    a = next(it, None)
    for b in it:
        yield (a, b)
        a = b


def sliding_window(data: list, size: int) -> Iterator[list]:
    """滑动窗口"""
    for i in range(len(data) - size + 1):
        yield data[i : i + size]
