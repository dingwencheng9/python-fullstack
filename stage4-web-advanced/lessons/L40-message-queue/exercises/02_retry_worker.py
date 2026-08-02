"""练习 2: 实现失败重试。

from __future__ import annotations

任务：实现 ``Worker`` 类，要求支持以下行为。

构造：``Worker(queue, handlers)``
- ``queue``：消息队列（提供 ``dequeue() -> Task | None`` 与 ``enqueue(task)``）
- ``handlers``：任务名 → 处理函数 的字典（处理函数接收 ``**task.payload``）

实例属性：
- ``self.dead_letters: list[Task]``：达到最大重试仍失败的任务收集到死信队列

方法 ``process_one(self) -> bool``：
- 从队列取一个任务
- 队列为空 → 返回 ``False``
- 否则将任务标记为 ``RUNNING`` 后调用 handler：
  - 成功：``status = SUCCESS``，把结果写到 ``task.payload["result"]``
  - 失败（捕获 ``Exception``）：
    - ``task.attempts += 1``
    - 若 ``task.attempts <= task.max_retries``：``status = RETRYING`` 并重新入队
    - 否则：``status = FAILED``，错误写入 ``task.payload["error"]``，追加到 ``dead_letters``
- 不论成功失败，只要消费了一个任务都返回 ``True``

参考答案：solutions/solution_02_retry_worker.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from solution_01_basic_queue import Task


class Worker:
    """请补全 process_one。"""

    def __init__(self, queue: object, handlers: dict[str, Callable[..., object]]) -> None:
        self.queue = queue
        self.handlers = handlers
        self.dead_letters: list[Task] = []

    def process_one(self) -> bool:
        raise NotImplementedError("请在练习中实现 process_one")
