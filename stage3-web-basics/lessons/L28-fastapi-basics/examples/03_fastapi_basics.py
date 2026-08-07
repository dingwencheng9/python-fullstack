"""示例 1：最小 FastAPI 应用。"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="L27 Hello API",
    description="最小 FastAPI 应用：路由、健康检查和自动文档。",
    version="1.0.0",
    openapi_tags=[{"name": "基础", "description": "入门级路由示例"}],
)


@app.get("/", tags=["基础"], summary="欢迎页")
def read_root() -> dict[str, str]:
    """返回服务欢迎信息。"""
    return {"message": "Hello FastAPI", "docs": "/docs"}


@app.get("/health", tags=["基础"], summary="健康检查")
def health_check() -> dict[str, str]:
    """返回健康状态，常用于部署探针。"""
    return {"status": "ok"}


def main() -> None:
    """启动开发服务器。"""
    import uvicorn

    uvicorn.run("03_fastapi_basics:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
