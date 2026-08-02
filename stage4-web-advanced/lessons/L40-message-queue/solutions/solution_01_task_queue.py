"""练习 1 参考答案: 任务队列。"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Task:
    name: str
    payload: dict
    id: str = field(default_factory=lambda: str(uuid4()))


class Queue:
    def __init__(self) -> None:
        self.queue: deque[Task] = deque()
        self.results: dict[str, Task] = {}

    def enqueue(self, task: Task) -> str:
        self.queue.append(task)
        self.results[task.id] = task
        return task.id

    def dequeue(self) -> Task | None:
        return self.queue.popleft() if self.queue else None

    def get_result(self, task_id: str) -> Task | None:
        return self.results.get(task_id)
