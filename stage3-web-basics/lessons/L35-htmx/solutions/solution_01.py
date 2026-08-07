"""L34 HTMX 练习题参考解答

构建 HTMX 评论系统。
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
# 评论数据模型
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
# 评论仓库类
# ============================================================


class CommentRepository:
    """评论仓库"""

    def __init__(self) -> None:
        self.comments: list[Comment] = []
        self._next_id = 1

    def create(self, content: str, parent_id: int | None = None) -> Comment:
        """创建评论"""
        comment = Comment(id=self._next_id, content=content, parent_id=parent_id)
        self._next_id += 1

        if parent_id is None:
            self.comments.append(comment)
        else:
            parent = self._find_comment(parent_id)
            if parent:
                parent.replies.append(comment)

        return comment

    def get_all(self) -> list[Comment]:
        """获取所有顶级评论"""
        return [c for c in self.comments if c.parent_id is None]

    def get(self, comment_id: int) -> Comment | None:
        """获取单个评论"""
        return self._find_comment(comment_id)

    def delete(self, comment_id: int) -> bool:
        """删除评论"""
        # 先检查是否是顶级评论
        for i, comment in enumerate(self.comments):
            if comment.id == comment_id:
                del self.comments[i]
                return True

        # 检查是否是回复
        for comment in self.comments:
            for i, reply in enumerate(comment.replies):
                if reply.id == comment_id:
                    del comment.replies[i]
                    return True

        return False

    def _find_comment(self, comment_id: int) -> Comment | None:
        """递归查找评论"""
        for comment in self.comments:
            if comment.id == comment_id:
                return comment
            for reply in comment.replies:
                if reply.id == comment_id:
                    return reply
        return None


# ============================================================
# FastAPI 应用
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
    return templates.TemplateResponse(request, "comments/home.html", {"comments": comment_repo.get_all()})


@app.post("/comments", response_class=HTMLResponse)
async def create_comment(
    request: Request,
    content: Annotated[str, Form()],
    parent_id: Annotated[int | None, Form()] = None,
) -> HTMLResponse:
    """创建评论"""
    if not content.strip():
        return HTMLResponse(content='<div class="error">评论内容不能为空</div>', status_code=422)

    comment = comment_repo.create(content.strip(), parent_id)

    if is_htmx(request):
        return templates.TemplateResponse(request, "comments/comment_item.html", {"comment": comment})

    response = HTMLResponse(content="", status_code=303)
    response.headers["Location"] = "/"
    return response


@app.delete("/comments/{comment_id}", response_class=HTMLResponse)
async def delete_comment(request: Request, comment_id: int) -> HTMLResponse:
    """删除评论"""
    if not comment_repo.delete(comment_id):
        return HTMLResponse(content='<div class="error">评论不存在</div>', status_code=404)

    if is_htmx(request):
        response = HTMLResponse(content="")
        response.headers["HX-Reswap"] = "none"
        return response

    response = HTMLResponse(content="", status_code=303)
    response.headers["Location"] = "/"
    return response


# ============================================================
# 启动
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("HTMX 评论系统参考解答")
    print("=" * 60)
    print("访问 http://localhost:8000")
    uvicorn.run("01_solution:app", host="0.0.0.0", port=8000, reload=True)
