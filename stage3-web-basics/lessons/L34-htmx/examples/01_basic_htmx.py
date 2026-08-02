"""L34: 基础 HTMX 示例 - FastAPI + Jinja2 + HTMX 模板渲染

本示例展示如何使用 FastAPI 的 Jinja2Templates 配合 HTMX，
实现无需复杂前端框架的全栈交互应用。

运行方式：
    cd examples
    uv run python 01_basic_htmx.py

然后访问 http://localhost:8000
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


# ============================================================
# 配置
# ============================================================

app = FastAPI(title="HTMX 基础示例", version="1.0.0")

BASE_DIR = Path(__file__).parent

# 静态文件（HTMX 库）
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Jinja2 模板
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ============================================================
# 数据模型
# ============================================================


class Message:
    """简单消息模型"""

    def __init__(self, id: int, content: str) -> None:
        self.id = id
        self.content = content


# 内存存储
messages: list[Message] = [
    Message(1, "欢迎使用 HTMX + FastAPI！"),
    Message(2, "无需复杂前端框架即可实现交互式应用"),
]
_next_id = 3


# ============================================================
# 辅助函数
# ============================================================


def is_htmx(request: Request) -> bool:
    """检测是否为 HTMX 请求"""
    return "HX-Request" in request.headers


# ============================================================
# 路由
# ============================================================


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """首页"""
    return templates.TemplateResponse(request, "home.html", {"messages": messages})


@app.get("/messages", response_class=HTMLResponse)
async def list_messages(request: Request) -> HTMLResponse:
    """获取消息列表（HTMX 局部更新用）"""
    return templates.TemplateResponse(request, "message_list.html", {"messages": messages})


@app.post("/messages", response_class=HTMLResponse)
async def create_message(request: Request, content: Annotated[str, Form()]) -> HTMLResponse:
    """创建新消息"""
    global _next_id

    if not content.strip():
        if is_htmx(request):
            return HTMLResponse(content='<div class="error">消息内容不能为空</div>', status_code=422)

    msg = Message(id=_next_id, content=content.strip())
    messages.append(msg)
    _next_id += 1

    if is_htmx(request):
        # HTMX 请求：返回新消息片段
        return templates.TemplateResponse(request, "message_item.html", {"message": msg})

    # 普通请求：重定向
    response = HTMLResponse(content="", status_code=303)
    response.headers["Location"] = "/"
    return response


@app.delete("/messages/{message_id}", response_class=HTMLResponse)
async def delete_message(request: Request, message_id: int) -> HTMLResponse:
    """删除消息"""
    global messages

    original_len = len(messages)
    messages = [m for m in messages if m.id != message_id]

    if len(messages) == original_len:
        return HTMLResponse(content='<div class="error">消息不存在</div>', status_code=404)

    if is_htmx(request):
        # HTMX 请求：返回空响应，触发移除
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
    # 确保静态文件和模板目录存在
    static_dir = BASE_DIR / "static"
    static_dir.mkdir(exist_ok=True)

    templates_dir = BASE_DIR / "templates"
    templates_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("HTMX 基础示例")
    print("=" * 60)
    print("访问 http://localhost:8000")
    print()
    print("功能演示：")
    print("  1. 表单提交 - 异步添加消息（无需刷新页面）")
    print("  2. 删除消息 - 点击删除按钮移除消息")
    print("  3. HTMX 请求 - 带 HX-Request 头的异步请求")
    print()
    print("提示：请确保 static/htmx.min.js 存在")
    print("      下载: curl -o static/htmx.min.js https://unpkg.com/htmx.org@latest/dist/htmx.min.js")
    print("=" * 60)

    uvicorn.run("01_basic_htmx:app", host="0.0.0.0", port=8000, reload=True)
