"""L40 消息队列基础测试。"""

from __future__ import annotations

import pytest
from solutions.solution_01_task_queue import Queue, Task
from solutions.solution_02_retry_worker import (
    Task as RetryTask,
)
from solutions.solution_02_retry_worker import (
    TaskStatus,
    Worker,
    backoff_seconds,
)


def test_queue_enqueue_dequeue():
    q = Queue()
    task = Task("email", {"to": "a@example.com"})
    task_id = q.enqueue(task)
    assert q.get_result(task_id) == task
    assert q.dequeue() == task
    assert q.dequeue() is None


def test_queue_multiple_tasks_order():
    q = Queue()
    t1 = Task("a", {})
    t2 = Task("b", {})
    q.enqueue(t1)
    q.enqueue(t2)
    assert q.dequeue() == t1
    assert q.dequeue() == t2


def test_worker_success():
    q = Queue()
    task = RetryTask("add", {"a": 2, "b": 3})
    q.enqueue(task)
    worker = Worker(q, {"add": lambda a, b: a + b})
    assert worker.process_one() is True
    assert task.status == TaskStatus.SUCCESS
    assert task.payload["result"] == 5


def test_worker_empty_queue():
    q = Queue()
    worker = Worker(q, {})
    assert worker.process_one() is False


def test_worker_retries_on_failure():
    q = Queue()
    task = RetryTask("fail", {}, max_retries=2)
    q.enqueue(task)
    worker = Worker(q, {"fail": lambda: (_ for _ in ()).throw(RuntimeError("boom"))})
    assert worker.process_one() is True
    assert task.status == TaskStatus.RETRYING
    assert task.attempts == 1
    assert q.dequeue() == task


def test_worker_dead_letter_after_retries():
    q = Queue()
    task = RetryTask("fail", {}, max_retries=0)
    q.enqueue(task)
    worker = Worker(q, {"fail": lambda: (_ for _ in ()).throw(RuntimeError("boom"))})
    worker.process_one()
    assert task.status == TaskStatus.FAILED
    assert len(worker.dead_letters) == 1


@pytest.mark.parametrize("attempt,expected", [(1, 2), (2, 4), (3, 8), (10, 60)])
def test_backoff_seconds(attempt, expected):
    assert backoff_seconds(attempt) == expected
