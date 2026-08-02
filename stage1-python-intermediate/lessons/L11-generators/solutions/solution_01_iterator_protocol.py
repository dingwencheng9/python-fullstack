"""
L11: 生成器与迭代器 - 迭代器协议练习解答

实现自定义迭代器。
"""

from collections.abc import Iterator


class FibonacciIterator:
    """斐波那契数列迭代器"""

    def __init__(self, limit: int):
        self.limit = limit
        self.current = 0
        self.next_val = 1
        self.count = 0

    def __iter__(self) -> "FibonacciIterator":
        return self

    def __next__(self) -> int:
        if self.count >= self.limit:
            raise StopIteration
        result = self.current
        self.current, self.next_val = self.next_val, self.current + self.next_val
        self.count += 1
        return result


class Range:
    """自定义 Range 实现"""

    def __init__(self, start: int, stop: int, step: int = 1):
        self.start = start
        self.stop = stop
        self.step = step
        self._current = start

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if (self.step > 0 and self._current >= self.stop) or (self.step < 0 and self._current <= self.stop):
            raise StopIteration
        result = self._current
        self._current += self.step
        return result


class Counter:
    """计数器迭代器"""

    def __init__(self, max_val: int, start: int = 0):
        self.current = start
        self.max_val = max_val

    def __iter__(self) -> "Counter":
        return self

    def __next__(self) -> int:
        if self.current >= self.max_val:
            raise StopIteration
        self.current += 1
        return self.current
