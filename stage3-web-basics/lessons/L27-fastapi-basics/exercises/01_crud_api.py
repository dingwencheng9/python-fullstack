"""练习 1：实现内存版 CRUD API。"""

from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="L28 练习：CRUD API", version="0.1.0")


class ItemCreate(BaseModel):
    """创建商品的请求模型。"""

    name: Annotated[str, Field(min_length=1, max_length=80)]
    price: Annotated[float, Field(ge=0)]


class ItemResponse(BaseModel):
    """商品响应模型。"""

    id: int
    name: str
    price: float


# TODO: 使用 dict[int, ItemResponse] 保存数据。
# TODO: 实现 reset_storage()，方便测试时隔离状态。
# TODO: 实现以下端点：
# 1. POST /items，创建商品，状态码 201，返回 ItemResponse。
# 2. GET /items，返回 list[ItemResponse]。
# 3. GET /items/{item_id}，不存在时返回 404。
# 4. PUT /items/{item_id}，完整更新商品。
# 5. DELETE /items/{item_id}，删除成功返回 204。


def reset_storage() -> None:
    """重置内存存储。"""
    raise NotImplementedError("请实现 reset_storage")
