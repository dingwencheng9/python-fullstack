"""
L10: 类型系统 - 泛型约束练习解答

使用泛型约束实现类型安全的容器。
"""


class Container[T]:
    """泛型容器"""

    def __init__(self, value: T):
        self._value = value

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value


N = int | float


class NumberBox[N: (int, float)]:
    """数字容器，支持加减运算"""

    def __init__(self, value: N):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected number, got {type(value).__name__}")
        self._value = value

    def get(self) -> N:
        return self._value

    def add(self, other: N) -> "NumberBox[N]":
        return NumberBox(self._value + other)

    def multiply(self, other: N) -> "NumberBox[N]":
        return NumberBox(self._value * other)


def merge_containers[T](a: Container[T], b: Container[T]) -> list[T]:
    """合并两个同类型容器"""
    return [a.get(), b.get()]
