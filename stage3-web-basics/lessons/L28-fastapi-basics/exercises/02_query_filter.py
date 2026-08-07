"""练习 2：实现查询过滤 API。"""

from __future__ import annotations

from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="L28 练习：查询过滤", version="0.1.0")


class Product(BaseModel):
    """商品数据模型。"""

    id: int
    name: str
    category: Literal["book", "tool", "course"]
    price: float
    is_active: bool = True


# TODO: 准备一组内存商品数据。
# TODO: 实现 GET /products。
# 要求支持：
# - q: str | None，按名称关键字过滤。
# - category: Literal["book", "tool", "course"] | None，按分类过滤。
# - min_price: float | None，价格下限，Query(ge=0)。
# - max_price: float | None，价格上限，Query(ge=0)。
# - active_only: bool，默认 True。
# - skip: int，默认 0，Query(ge=0)。
# - limit: int，默认 10，Query(ge=1, le=50)。


@app.get("/products", response_model=list[Product], tags=["商品"])
def list_products(
    q: str | None = None,
    category: Literal["book", "tool", "course"] | None = None,
    min_price: Annotated[float | None, Query(ge=0)] = None,
    max_price: Annotated[float | None, Query(ge=0)] = None,
    active_only: bool = True,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> list[Product]:
    """按查询参数过滤商品。"""
    raise NotImplementedError("请实现查询过滤逻辑")
