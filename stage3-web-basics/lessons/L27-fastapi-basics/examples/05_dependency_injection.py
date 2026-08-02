"""示例 3：Depends 依赖注入。"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel

app = FastAPI(
    title="L28 Dependency Injection",
    description="演示普通依赖、子依赖和请求级设置对象。",
    version="1.0.0",
    openapi_tags=[{"name": "依赖", "description": "Depends 示例"}],
)


class PageParams(BaseModel):
    """分页参数对象。"""

    skip: int
    limit: int


class CurrentUser(BaseModel):
    """当前用户对象。"""

    username: str
    role: str


def get_page_params(
    skip: Annotated[int, Query(ge=0, description="跳过数量")] = 0,
    limit: Annotated[int, Query(ge=1, le=50, description="每页数量")] = 10,
) -> PageParams:
    """把查询参数组合为分页对象。"""
    return PageParams(skip=skip, limit=limit)


def get_api_token(x_api_token: Annotated[str | None, Header()] = None) -> str:
    """读取并校验演示用 API Token。"""
    if x_api_token != "dev-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少或无效的 X-Api-Token",
        )
    return x_api_token


def get_current_user(token: Annotated[str, Depends(get_api_token)]) -> CurrentUser:
    """子依赖：基于 Token 解析当前用户。"""
    return CurrentUser(username="alice", role="admin" if token else "guest")


@app.get("/items", tags=["依赖"], summary="分页查询")
def list_items(page: Annotated[PageParams, Depends(get_page_params)]) -> dict[str, object]:
    """使用依赖注入复用分页参数。"""
    return {"pagination": page.model_dump(), "items": []}


@app.get("/me", tags=["依赖"], summary="当前用户")
def read_me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    """使用子依赖完成认证与用户解析。"""
    return user


def main() -> None:
    """启动开发服务器。"""
    import uvicorn

    uvicorn.run("03_dependency_injection:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
