"""Bag 类参考答案 - 演示容器魔法方法"""


class Bag:
    """可迭代容器类（实现 Sized、Container、Iterable 协议）"""

    def __init__(self) -> None:
        self._items: list[str] = []
        self._counts: dict[str, int] = {}

    def add(self, item: str) -> None:
        """添加物品"""
        self._items.append(item)
        self._counts[item] = self._counts.get(item, 0) + 1

    def remove(self, item: str) -> bool:
        """移除物品"""
        if item not in self._counts or self._counts[item] == 0:
            return False
        self._counts[item] -= 1
        self._items.remove(item)
        return True

    def count(self, item: str) -> int:
        """获取物品数量"""
        return self._counts.get(item, 0)

    def __len__(self) -> int:
        """len(bag) 返回物品总数"""
        return len(self._items)

    def __contains__(self, item: str) -> bool:
        """item in bag"""
        return self.count(item) > 0

    def __iter__(self) -> "BagIterator":
        """for item in bag"""
        return BagIterator(self._items.copy())

    def __repr__(self) -> str:
        return f"Bag({self._items})"


class BagIterator:
    """Bag 的迭代器"""

    def __init__(self, items: list[str]) -> None:
        self._items = items
        self._index = 0

    def __iter__(self) -> "BagIterator":
        return self

    def __next__(self) -> str:
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item
