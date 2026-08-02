"""L40 示例 1: 内存任务队列。"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Task:
    name: str
    payload: dict
    id: str = field(default_factory=lambda: str(uuid4()))
    status: TaskStatus = TaskStatus.PENDING


class InMemoryQueue:
    def __init__(self) -> None:
        self.queue: deque[Task] = deque()
        self.results: dict[str, Task] = {}

    def enqueue(self, task: Task) -> str:
        self.queue.append(task)
        self.results[task.id] = task
        return task.id

    def dequeue(self) -> Task | None:
        return self.queue.popleft() if self.queue else None


if __name__ == "__main__":
    q = InMemoryQueue()
    task_id = q.enqueue(Task("send_email", {"to": "alice@example.com"}))
    print("queued", task_id)
    print("dequeue", q.dequeue())
