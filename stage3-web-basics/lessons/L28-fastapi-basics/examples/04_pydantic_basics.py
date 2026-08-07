"""示例 2：Pydantic 请求与响应模型。"""

from __future__ import annotations

from typing import Annotated, Literal

from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="L28 Pydantic Models",
    description="演示请求模型、响应模型、Field 验证和联合类型。",
    version="1.0.0",
    openapi_tags=[{"name": "商品", "description": "商品模型示例"}],
)


class ItemCreate(BaseModel):
    """创建商品的请求体。"""

    name: Annotated[str, Field(min_length=1, max_length=60, description="商品名称")]
    price: Annotated[float, Field(ge=0, description="商品价格，允许免费商品")]
    category: Annotated[Literal["book", "tool", "course"], Field(description="商品分类")]
    description: Annotated[str | None, Field(default=None, max_length=200)] = None


class ItemResponse(BaseModel):
    """商品响应体。"""

    id: int
    name: str
    price: float
    category: str
    description: str | None = None
    is_free: bool


@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["商品"],
    summary="创建商品",
)
def create_item(item: ItemCreate) -> ItemResponse:
    """根据请求模型创建一个演示商品。"""
    return ItemResponse(
        id=1,
        name=item.name,
        price=item.price,
        category=item.category,
        description=item.description,
        is_free=item.price == 0,
    )


def main() -> None:
    """启动开发服务器。"""
    import uvicorn

    uvicorn.run("02_pydantic_models:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
