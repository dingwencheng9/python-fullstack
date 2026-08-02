"""Set 类参考答案 - 对应 exercises/02_set_class.py。"""

from collections.abc import Iterator
from typing import override


class Set:
    """简化版集合类，演示容器协议。"""

    def __init__(self) -> None:
        self._items: list[str] = []

    def add(self, item: str) -> None:
        """添加元素；重复元素不会被再次加入。"""
        if item not in self._items:
            self._items.append(item)

    def remove(self, item: str) -> bool:
        """移除元素，返回是否成功。"""
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    @override
    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item: str) -> bool:
        return item in self._items

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._items)

    @override
    def __repr__(self) -> str:
        return f"Set({self._items!r})"
