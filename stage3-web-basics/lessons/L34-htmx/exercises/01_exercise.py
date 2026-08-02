"""L34 HTMX 练习题

构建 HTMX 评论系统。

功能要求：
1. 发表顶级评论
2. 回复已有评论（嵌套显示）
3. 评论实时更新（使用 SSE）
4. 表单验证与错误提示
5. 删除评论（带确认）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


# ============================================================
# TODO 1: 实现评论数据模型
# ============================================================


@dataclass
class Comment:
    """评论数据模型"""

    content: str
    parent_id: int | None = None
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)
    replies: list[Comment] = field(default_factory=list)


# ============================================================
# TODO 2: 实现评论仓库类
# ============================================================


class CommentRepository:
    """评论仓库"""

    def __init__(self) -> None:
        self.comments: list[Comment] = []
        self._next_id = 1

    def create(self, content: str, parent_id: int | None = None) -> Comment:
        """创建评论"""
        # TODO: 实现创建评论逻辑
        raise NotImplementedError("请实现 create 方法")

    def get_all(self) -> list[Comment]:
        """获取所有顶级评论"""
        # TODO: 实现获取评论逻辑
        raise NotImplementedError("请实现 get_all 方法")

    def get(self, comment_id: int) -> Comment | None:
        """获取单个评论"""
        # TODO: 实现获取单个评论逻辑
        raise NotImplementedError("请实现 get 方法")

    def delete(self, comment_id: int) -> bool:
        """删除评论"""
        # TODO: 实现删除评论逻辑
        raise NotImplementedError("请实现 delete 方法")


# ============================================================
# TODO 3: 实现 FastAPI 应用
# ============================================================

app = FastAPI(title="HTMX 评论系统", version="1.0.0")

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static", check_dir=False), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

comment_repo = CommentRepository()


def is_htmx(request: Request) -> bool:
    """检测是否为 HTMX 请求"""
    return "HX-Request" in request.headers


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """首页"""
    # TODO: 返回评论列表页面
    raise NotImplementedError("请实现 home 路由")


@app.post("/comments", response_class=HTMLResponse)
async def create_comment(request: Request, content: Annotated[str, Form()]) -> HTMLResponse:
    """创建评论"""
    # TODO: 实现评论创建逻辑
    raise NotImplementedError("请实现 create_comment 路由")


@app.delete("/comments/{comment_id}", response_class=HTMLResponse)
async def delete_comment(request: Request, comment_id: int) -> HTMLResponse:
    """删除评论"""
    # TODO: 实现评论删除逻辑
    raise NotImplementedError("请实现 delete_comment 路由")


@app.get("/comments/stream")
async def comments_stream():
    """SSE 流：推送评论更新"""
    # TODO: 实现 SSE 实时更新
    raise NotImplementedError("请实现 comments_stream 路由")


# ============================================================
# 启动
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("HTMX 评论系统练习")
    print("=" * 60)
    print("访问 http://localhost:8000")
    print()
    print("功能：")
    print("  1. 发表顶级评论")
    print("  2. 回复评论（嵌套显示）")
    print("  3. 评论实时更新（SSE）")
    print("  4. 删除评论")
    print("=" * 60)

    uvicorn.run("01_exercise:app", host="0.0.0.0", port=8000, reload=True)
