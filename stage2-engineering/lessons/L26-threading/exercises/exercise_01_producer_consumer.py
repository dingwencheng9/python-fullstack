"""练习 1：实现线程安全的生产者消费者容器。"""

from __future__ import annotations

import threading


class ProducerConsumer:
    """待实现：用 Lock 保护共享列表。"""

    def __init__(self, max_items: int) -> None:
        self.max_items = max_items
        self._items: list[int] = []
        self._next_value = 0
        self._lock = threading.Lock()

    def produce(self, count: int) -> None:
        """生产 count 个整数，最多保存 max_items 个。"""
        # TODO: 在锁内追加数据，并保证多线程调用时不会超过 max_items。
        raise NotImplementedError

    def consume_all(self) -> list[int]:
        """取出当前全部数据，并清空内部缓冲区。"""
        # TODO: 返回数据副本并清空缓冲区。
        raise NotImplementedError

    def reset(self) -> None:
        """重置内部状态，便于重复练习。"""
        # TODO: 清空数据并把下一个值重置为 0。
        raise NotImplementedError
