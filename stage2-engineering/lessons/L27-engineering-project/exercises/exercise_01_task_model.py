"""练习 1: 完善任务模型

根据 lesson.md 中的要求，实现 Task 类的以下方法：
- is_overdue() - 检查任务是否已过期
- days_until_due() - 计算距离截止日期的天数
- to_dict() - 序列化为字典
- from_dict() - 从字典反序列化
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
        # TODO: 实现过期检查逻辑
        # 提示: 比较 datetime.now() 和 self.due_date
        raise NotImplementedError("请实现 is_overdue 方法")

    def days_until_due(self) -> int | None:
        """计算距离截止日期的天数

        Returns:
            距离截止日期的天数（负数表示已过期），无截止日期返回 None
        """
        # TODO: 实现天数计算
        # 提示: 使用 (self.due_date - datetime.now()).days
        raise NotImplementedError("请实现 days_until_due 方法")

    def to_dict(self) -> dict:
        """序列化为字典

        Returns:
            包含任务所有字段的字典
        """
        # TODO: 实现序列化
        # 提示: 将枚举值转换为字符串，datetime 转换为 ISO 格式
        raise NotImplementedError("请实现 to_dict 方法")

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        """从字典反序列化

        Args:
            data: 包含任务数据的字典

        Returns:
            Task 实例
        """
        # TODO: 实现反序列化
        # 提示: 从字符串恢复枚举值和 datetime
        raise NotImplementedError("请实现 from_dict 类方法")
