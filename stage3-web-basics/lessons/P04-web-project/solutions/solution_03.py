"""L35 综合项目 - Solution 3: API 端点实现"""

from __future__ import annotations

from fastapi import APIRouter, status
from pydantic import BaseModel

# 简化版 API 端点示例


class UserCreate(BaseModel):
    """用户创建请求"""

    username: str
    email: str
    password: str


class TaskCreate(BaseModel):
    """任务创建请求"""

    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    """任务更新请求"""

    title: str | None = None
    description: str | None = None
    completed: bool | None = None


# 模拟的 API 路由
users_router = APIRouter(prefix="/users", tags=["用户"])
tasks_router = APIRouter(prefix="/tasks", tags=["任务"])


@users_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate) -> dict:
    """创建新用户"""
    return {
        "id": 1,
        "username": user_in.username,
        "email": user_in.email,
        "is_active": True,
    }


@tasks_router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate) -> dict:
    """创建新任务"""
    return {
        "id": 1,
        "title": task_in.title,
        "description": task_in.description,
        "completed": False,
        "user_id": 1,
    }


@tasks_router.get("/")
def list_tasks(skip: int = 0, limit: int = 100) -> list[dict]:
    """获取任务列表"""
    return [
        {
            "id": 1,
            "title": "示例任务",
            "description": "这是示例任务",
            "completed": False,
            "user_id": 1,
        }
    ]
