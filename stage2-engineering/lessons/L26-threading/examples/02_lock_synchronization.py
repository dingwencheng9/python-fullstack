"""示例 2：Lock / RLock / Condition 同步原语。"""

from __future__ import annotations

import threading
import time
from collections import deque


class SafeCounter:
    """使用 Lock 保护共享计数器。"""

    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:
            self._value += 1

    @property
    def value(self) -> int:
        with self._lock:
            return self._value


class Account:
    """使用 RLock 允许同一线程重入锁。"""

    def __init__(self, balance: int) -> None:
        self._balance = balance
        self._lock = threading.RLock()

    def deposit(self, amount: int) -> None:
        with self._lock:
            self._balance += amount

    def transfer_bonus(self, amount: int) -> None:
        with self._lock:
            self.deposit(amount)

    @property
    def balance(self) -> int:
        with self._lock:
            return self._balance


class ConditionBuffer:
    """使用 Condition 协调生产者和消费者。"""

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._items: deque[int] = deque()
        self._condition = threading.Condition()

    def put(self, item: int) -> None:
        with self._condition:
            while len(self._items) >= self._capacity:
                self._condition.wait()
            self._items.append(item)
            self._condition.notify()

    def get(self) -> int:
        with self._condition:
            while not self._items:
                self._condition.wait()
            item = self._items.popleft()
            self._condition.notify()
            return item


def demo_lock() -> None:
    """演示 Lock 消除竞态。"""
    counter = SafeCounter()
    threads = [threading.Thread(target=counter.increment) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Lock counter = {counter.value}")


def demo_rlock() -> None:
    """演示 RLock 支持同一线程重复获得锁。"""
    account = Account(balance=100)
    account.transfer_bonus(20)
    print(f"RLock balance = {account.balance}")


def demo_condition() -> None:
    """演示 Condition 的等待和通知。"""
    buffer = ConditionBuffer(capacity=2)
    consumed: list[int] = []

    def producer() -> None:
        for item in range(5):
            buffer.put(item)
            print(f"生产 {item}")
            time.sleep(0.02)

    def consumer() -> None:
        for _ in range(5):
            item = buffer.get()
            consumed.append(item)
            print(f"消费 {item}")

    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    consumer_thread.join()
    print(f"Condition consumed = {consumed}")


def main() -> None:
    """运行同步原语示例。"""
    demo_lock()
    demo_rlock()
    demo_condition()


if __name__ == "__main__":
    main()
