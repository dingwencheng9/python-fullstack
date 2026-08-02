"""示例4: 容器和迭代器魔法方法"""

from __future__ import annotations


class Stack:
    """演示 __len__, __contains__, __iter__"""

    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        self._items.append(item)

    def pop(self) -> str | None:
        if not self._items:
            return None
        return self._items.pop()

    def __len__(self) -> int:
        """len(stack)"""
        return len(self._items)

    def __contains__(self, item: str) -> bool:
        """item in stack"""
        return item in self._items

    def __iter__(self) -> StackIterator:
        """for item in stack"""
        return StackIterator(self._items.copy())

    def __repr__(self) -> str:
        return f"Stack({self._items})"


class StackIterator:
    """Stack 的迭代器"""

    def __init__(self, items: list[str]) -> None:
        self._items = items
        self._index = 0

    def __iter__(self) -> StackIterator:
        return self

    def __next__(self) -> str:
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item


# 演示
stack = Stack()
stack.push("apple")
stack.push("banana")
stack.push("cherry")

print(f"栈长度: {len(stack)}")  # 3
print(f"'banana' in stack: {'banana' in stack}")  # True
print("迭代栈:")
for item in stack:
    print(f"  - {item}")

print(f"栈内容: {stack}")
