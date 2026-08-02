"""L41 示例: 任务状态查询。"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


@dataclass
class TaskResult:
    task_id: str
    status: Status
    result: str = ""


def query_task(task_id: str) -> TaskResult:
    results = {"t1": TaskResult("t1", Status.DONE, "ok")}
    return results.get(task_id, TaskResult(task_id, Status.PENDING))


if __name__ == "__main__":
    print(query_task("t1"))
