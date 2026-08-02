"""练习 1 参考答案: 完善任务模型

这是 exercises/exercise_01_task_model.py 的参考实现。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """任务状态枚举"""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(Enum):
    """优先级枚举"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    """任务数据模型"""

    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)
    due_date: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def is_overdue(self) -> bool:
        """检查任务是否已过期

        Returns:
            如果任务有截止日期且已过期返回 True，否则返回 False
        """
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date

    def days_until_due(self) -> int | None:
        """计算距离截止日期的天数

        Returns:
            距离截止日期的天数（负数表示已过期），无截止日期返回 None
        """
        if self.due_date is None:
            return None
        delta = self.due_date - datetime.now()
        return delta.days

    def to_dict(self) -> dict:
        """序列化为字典

        Returns:
            包含任务所有字段的字典
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "tags": self.tags.copy(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        """从字典反序列化

        Args:
            data: 包含任务数据的字典

        Returns:
            Task 实例
        """
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=TaskStatus(data.get("status", "todo")),
            priority=Priority(data.get("priority", "medium")),
            tags=data.get("tags", []).copy(),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now(),
        )
