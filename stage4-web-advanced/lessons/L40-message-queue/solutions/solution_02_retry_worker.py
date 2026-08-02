"""练习 2 参考答案: 重试 Worker。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class Task:
    name: str
    payload: dict
    id: str = field(default_factory=lambda: str(uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    attempts: int = 0
    max_retries: int = 3


def backoff_seconds(attempt: int) -> int:
    return min(60, 2**attempt)


class Worker:
    def __init__(self, queue, handlers: dict) -> None:
        self.queue = queue
        self.handlers = handlers
        self.dead_letters: list[Task] = []

    def process_one(self) -> bool:
        task = self.queue.dequeue()
        if task is None:
            return False
        task.status = TaskStatus.RUNNING
        try:
            result = self.handlers[task.name](**task.payload)
            task.payload["result"] = result
            task.status = TaskStatus.SUCCESS
        except Exception as exc:
            task.attempts += 1
            if task.attempts <= task.max_retries:
                task.status = TaskStatus.RETRYING
                self.queue.enqueue(task)
            else:
                task.status = TaskStatus.FAILED
                task.payload["error"] = str(exc)
                self.dead_letters.append(task)
        return True
