"""Task Tracker CLI - 任务追踪工具

综合运用 Stage 2 工程化内容的示例代码：
- pytest 完整实战：单元测试、Mock、Fixture、参数化测试
- 现代化工具链：uv + Ruff + mypy + 类型注解
- 异步编程：使用 asyncio.TaskGroup 并发处理任务
- 装饰器：日志、缓存、权限检查装饰器
- CI/CD：GitHub Actions 自动化流水线
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
    """优先级枚举，支持比较操作"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    def __lt__(self, other: object) -> bool:
        """支持优先级比较：高 > 中 > 低"""
        if not isinstance(other, Priority):
            return NotImplemented
        order = {Priority.HIGH: 3, Priority.MEDIUM: 2, Priority.LOW: 1}
        return order[self] < order[other]

    def __gt__(self, other: object) -> bool:
        """支持 > 比较"""
        if not isinstance(other, Priority):
            return NotImplemented
        return other.__lt__(self)

    def __le__(self, other: object) -> bool:
        """支持 <= 比较"""
        if not isinstance(other, Priority):
            return NotImplemented
        return self == other or self.__lt__(other)

    def __ge__(self, other: object) -> bool:
        """支持 >= 比较"""
        if not isinstance(other, Priority):
            return NotImplemented
        return self == other or self.__gt__(other)


@dataclass(frozen=True)
class Task:
    """任务数据模型（不可变）"""

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
        """检查任务是否已过期"""
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date

    def days_until_due(self) -> int | None:
        """计算距离截止日期的天数"""
        if self.due_date is None:
            return None
        delta = self.due_date - datetime.now()
        return delta.days

    def to_dict(self) -> dict:
        """序列化为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "tags": self.tags,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        """从字典反序列化"""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=TaskStatus(data["status"]),
            priority=Priority(data["priority"]),
            tags=data.get("tags", []),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
