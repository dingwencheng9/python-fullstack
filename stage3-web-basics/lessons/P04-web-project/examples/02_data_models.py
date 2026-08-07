"""L35 综合项目 - Exercise 2: 数据模型设计

任务：定义 User 和 Task 数据模型
"""

# === models/user.py ===
from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from models.task import Task


class User(Base):
    """用户模型"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))

    # 关系
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


# === models/task.py ===
from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from models.user import User


class Task(Base):
    """任务模型"""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(default=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # 关系
    owner: Mapped["User"] = relationship("User", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, completed={self.completed})>"


# === models/__init__.py ===
from models.task import Task
from models.user import User

__all__ = ["Task", "User"]
