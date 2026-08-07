"""L34: CRUD 操作示例 - 任务管理器

本示例展示完整的 HTMX + FastAPI CRUD 操作，
包括列表展示、创建、编辑、删除任务。

运行方式：
    cd examples
    mkdir -p templates
    # 创建模板文件（见下方）
    uv run python 02_crud_operations.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn


# ============================================================
# 配置
# ============================================================

app = FastAPI(title="HTMX CRUD 示例", version="1.0.0")

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ============================================================
# 数据模型
# ============================================================


class Task(BaseModel):
    """任务模型"""

    id: int | None = None
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = False


class TaskRepository:
    """任务仓库（内存实现）"""

    def __init__(self) -> None:
        self.tasks: dict[int, Task] = {}
        self._next_id = 1

    def create(self, title: str) -> Task:
        task = Task(id=self._next_id, title=title)
        self.tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_all(self) -> list[Task]:
        return list(self.tasks.values())

    def get(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def update(self, task_id: int, title: str | None = None, completed: bool | None = None) -> Task | None:
        if task_id not in self.tasks:
            return None
        task = self.tasks[task_id]
        if title is not None:
            task.title = title
        if completed is not None:
            task.completed = completed
        return task

    def delete(self, task_id: int) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False


task_repo = TaskRepository()
# 添加示例任务
task_repo.create("学习 HTMX 基础")
task_repo.create("完成 FastAPI CRUD 示例")
task_repo.create("实现表单验证")


# ============================================================
# 辅助函数
# ============================================================


def is_htmx(request: Request) -> bool:
    return "HX-Request" in request.headers


# ============================================================
# 路由
# ============================================================


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "crud/home.html", {"tasks": task_repo.get_all()})


@app.get("/tasks", response_class=HTMLResponse)
async def list_tasks(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "crud/task_list.html", {"tasks": task_repo.get_all()})


@app.post("/tasks", response_class=HTMLResponse)
async def create_task(request: Request, title: Annotated[str, Form()]) -> HTMLResponse:
    if not title.strip():
        return HTMLResponse(content='<div class="error">标题不能为空</div>', status_code=422)

    task = task_repo.create(title.strip())

    if is_htmx(request):
        return templates.TemplateResponse(request, "crud/task_item.html", {"task": task})

    response = HTMLResponse(content="", status_code=303)
    response.headers["Location"] = "/"
    return response


@app.put("/tasks/{task_id}", response_class=HTMLResponse)
async def update_task(
    request: Request,
    task_id: int,
    title: Annotated[str, Form()],
    completed: Annotated[bool, Form()] = False,
) -> HTMLResponse:
    task = task_repo.get(task_id)
    if not task:
        return HTMLResponse(content='<div class="error">任务不存在</div>', status_code=404)

    task = task_repo.update(task_id, title=title, completed=completed)

    if is_htmx(request):
        return templates.TemplateResponse(request, "crud/task_item.html", {"task": task})

    response = HTMLResponse(content="", status_code=303)
    response.headers["Location"] = "/"
    return response


@app.post("/tasks/{task_id}/toggle", response_class=HTMLResponse)
async def toggle_task(request: Request, task_id: int) -> HTMLResponse:
    task = task_repo.get(task_id)
    if not task:
        return HTMLResponse(content='<div class="error">任务不存在</div>', status_code=404)

    task = task_repo.update(task_id, completed=not task.completed)

    if is_htmx(request):
        return templates.TemplateResponse(request, "crud/task_item.html", {"task": task})

    return HTMLResponse(content="", status_code=303)


@app.delete("/tasks/{task_id}", response_class=HTMLResponse)
async def delete_task(request: Request, task_id: int) -> HTMLResponse:
    if not task_repo.delete(task_id):
        return HTMLResponse(content='<div class="error">任务不存在</div>', status_code=404)

    if is_htmx(request):
        response = HTMLResponse(content="")
        response.headers["HX-Reswap"] = "none"
        return response

    response = HTMLResponse(content="", status_code=303)
    response.headers["Location"] = "/"
    return response


@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
async def edit_task_form(request: Request, task_id: int) -> HTMLResponse:
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return templates.TemplateResponse(request, "crud/task_edit.html", {"task": task})


if __name__ == "__main__":
    print("=" * 60)
    print("HTMX CRUD 示例")
    print("=" * 60)
    print("访问 http://localhost:8000")
    print()
    print("功能：")
    print("  1. 创建任务 - 使用 HTMX 无刷新添加")
    print("  2. 切换完成状态 - 点击复选框")
    print("  3. 编辑任务 - 点击编辑按钮")
    print("  4. 删除任务 - 点击删除按钮")
    print("=" * 60)

    uvicorn.run("02_crud_operations:app", host="0.0.0.0", port=8000, reload=True)
