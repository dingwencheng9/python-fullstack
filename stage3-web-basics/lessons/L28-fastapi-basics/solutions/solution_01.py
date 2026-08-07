"""练习 1 参考答案：内存版 CRUD API。"""

from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="L28 Solution：CRUD API",
    description="使用内存 dict 实现完整 CRUD，便于理解 FastAPI 路由与状态码。",
    version="1.0.0",
    openapi_tags=[{"name": "商品", "description": "商品 CRUD 操作"}],
)


class ItemCreate(BaseModel):
    """创建或更新商品的请求模型。"""

    name: Annotated[str, Field(min_length=1, max_length=80, description="商品名称")]
    price: Annotated[float, Field(ge=0, description="商品价格，允许为 0")]


class ItemResponse(BaseModel):
    """商品响应模型。"""

    id: int
    name: str
    price: float


_items: dict[int, ItemResponse] = {}
_next_id_state = {"value": 1}


def reset_storage() -> None:
    """清空内存存储，保证测试之间互不影响。"""
    _items.clear()
    _next_id_state["value"] = 1


def _get_item_or_404(item_id: int) -> ItemResponse:
    """读取商品；不存在时抛出 404。"""
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"商品 {item_id} 不存在",
        )
    return item


@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["商品"],
    summary="创建商品",
)
def create_item(item: ItemCreate) -> ItemResponse:
    """创建商品并返回带 id 的响应。"""
    item_id = _next_id_state["value"]
    created = ItemResponse(id=item_id, name=item.name, price=item.price)
    _items[item_id] = created
    _next_id_state["value"] = item_id + 1
    return created


@app.get(
    "/items",
    response_model=list[ItemResponse],
    tags=["商品"],
    summary="列出商品",
)
def list_items() -> list[ItemResponse]:
    """按创建顺序返回所有商品。"""
    return list(_items.values())


@app.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    tags=["商品"],
    summary="读取商品",
)
def get_item(item_id: int) -> ItemResponse:
    """按 id 读取单个商品。"""
    return _get_item_or_404(item_id)


@app.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    tags=["商品"],
    summary="更新商品",
)
def update_item(item_id: int, item: ItemCreate) -> ItemResponse:
    """完整更新商品。"""
    _get_item_or_404(item_id)
    updated = ItemResponse(id=item_id, name=item.name, price=item.price)
    _items[item_id] = updated
    return updated


@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["商品"],
    summary="删除商品",
)
def delete_item(item_id: int) -> Response:
    """删除商品，成功时返回 204 空响应。"""
    _get_item_or_404(item_id)
    del _items[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("solutions.01_crud_api:app", host="127.0.0.1", port=8000, reload=True)
