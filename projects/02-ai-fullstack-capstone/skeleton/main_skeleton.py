"""

from __future__ import annotations

【骨架代码】FastAPI 应用入口

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from fastapi import FastAPI

# TODO: 导入配置和路由
# from .config import config
# from .routes import health, documents, chat


def create_app() -> FastAPI:
    """创建 FastAPI 应用

    步骤：
    1. 创建 FastAPI 实例，设置标题和描述
    2. 注册路由（health, documents, chat）
    3. 挂载静态文件目录（static）
    4. 添加首页路由返回 index.html
    """
    # TODO: 1. 创建 FastAPI 应用
    # ← 你的代码写在这里

    # TODO: 2. 注册路由
    # app.include_router(...)
    # ← 你的代码写在这里

    # TODO: 3. 挂载静态文件
    # static_dir = Path(__file__).parent / "static"
    # app.mount("/static", StaticFiles(directory=static_dir), name="static")
    # ← 你的代码写在这里

    # TODO: 4. 添加首页路由 GET /
    # @app.get("/", response_class=HTMLResponse)
    # async def read_index():
    #     index_path = Path(__file__).parent / "templates" / "index.html"
    #     return HTMLResponse(index_path.read_text(encoding="utf-8"))
    # ← 你的代码写在这里

    return app


app = create_app()


if __name__ == "__main__":
    pass

    # TODO: 运行 uvicorn 服务器，使用配置中的 host 和 port
    # uvicorn.run(...)
    # ← 你的代码写在这里
