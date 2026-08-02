"""
L11: 生成器与迭代器 - 迭代器练习

手动实现迭代器协议。
"""


class Counter:
    """计数器迭代器"""

    def __init__(self, max_val: int) -> None:
        self.max_val = max_val
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current >= self.max_val:
            raise StopIteration
        self.current += 1
        return self.current


class Fibonacci:
    """斐波那契数列迭代器"""

    def __init__(self, count: int) -> None:
        self.count = count
        self.a = 0
        self.b = 1
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.n >= self.count:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.n += 1
        return value


class Range:
    """范围迭代器"""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.start = start
        self.stop = stop
        self.step = step
        self.current = start

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.step == 0:
            raise ValueError("step 不能为 0")
        if (self.step > 0 and self.current >= self.stop) or (self.step < 0 and self.current <= self.stop):
            raise StopIteration
        value = self.current
        self.current += self.step
        return value


# === 验证 ===

if __name__ == "__main__":
    # 测试计数器
    counter = Counter(5)
    assert list(counter) == [1, 2, 3, 4, 5]

    # 测试斐波那契
    fib = Fibonacci(10)
    assert list(fib) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    # 测试范围
    r = Range(0, 10, 2)
    assert list(r) == [0, 2, 4, 6, 8]

    print("✅ 所有测试通过！")
