"""练习 1 参考答案：线程安全的生产者消费者容器。"""

from __future__ import annotations

import threading


class ProducerConsumer:
    """用 Lock 保护共享列表和递增序号。"""

    def __init__(self, max_items: int) -> None:
        if max_items < 0:
            msg = "max_items 必须大于或等于 0"
            raise ValueError(msg)
        self.max_items = max_items
        self._items: list[int] = []
        self._next_value = 0
        self._lock = threading.Lock()

    def produce(self, count: int) -> None:
        """生产 count 个整数，最多保留 max_items 个。"""
        if count < 0:
            msg = "count 必须大于或等于 0"
            raise ValueError(msg)

        with self._lock:
            remaining = self.max_items - len(self._items)
            amount = min(count, remaining)
            new_items = list(range(self._next_value, self._next_value + amount))
            self._items.extend(new_items)
            self._next_value += amount

    def consume_all(self) -> list[int]:
        """取出全部数据，并清空内部缓冲区。"""
        with self._lock:
            items = list(self._items)
            self._items.clear()
            return items

    def reset(self) -> None:
        """重置内部状态，便于测试或重复演示。"""
        with self._lock:
            self._items.clear()
            self._next_value = 0
