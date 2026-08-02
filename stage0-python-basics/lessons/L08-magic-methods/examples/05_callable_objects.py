"""示例5: 可调用对象 __call__"""


class Counter:
    """演示 __call__ 使对象像函数一样可调用"""

    def __init__(self) -> None:
        self._count = 0

    def __call__(self) -> int:
        """使实例可调用"""
        self._count += 1
        return self._count

    @property
    def count(self) -> int:
        return self._count

    def reset(self) -> None:
        self._count = 0


# 演示
counter = Counter()

print(f"计数器初始值: {counter()}")
print(f"计数器当前值: {counter()}")
print(f"计数器当前值: {counter()}")
print(f"总调用次数: {counter.count}")

counter.reset()
print(f"重置后: {counter()}")
