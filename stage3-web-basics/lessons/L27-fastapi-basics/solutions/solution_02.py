"""练习 2 参考答案：查询参数过滤。"""

from __future__ import annotations

from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel

app = FastAPI(
    title="L28 Solution：Query Filter",
    description="演示路径之外的查询参数、默认值与验证。",
    version="1.0.0",
    openapi_tags=[{"name": "商品", "description": "商品查询过滤"}],
)


class Product(BaseModel):
    """商品数据模型。"""

    id: int
    name: str
    category: Literal["book", "tool", "course"]
    price: float
    is_active: bool = True


_PRODUCTS: tuple[Product, ...] = (
    Product(id=1, name="Python 入门书", category="book", price=59.0, is_active=True),
    Product(id=2, name="FastAPI 实战课", category="course", price=199.0, is_active=True),
    Product(id=3, name="调试工具包", category="tool", price=29.0, is_active=True),
    Product(id=4, name="旧版 Web 课程", category="course", price=99.0, is_active=False),
    Product(id=5, name="SQL 查询手册", category="book", price=45.0, is_active=True),
)


def _filter_by_keyword(products: list[Product], keyword: str | None) -> list[Product]:
    """按名称关键字过滤。"""
    if keyword is None:
        return products
    normalized = keyword.casefold()
    return [product for product in products if normalized in product.name.casefold()]


def _filter_by_price(
    products: list[Product],
    min_price: float | None,
    max_price: float | None,
) -> list[Product]:
    """按价格区间过滤。"""
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price 不能大于 max_price",
        )
    result = products
    if min_price is not None:
        result = [product for product in result if product.price >= min_price]
    if max_price is not None:
        result = [product for product in result if product.price <= max_price]
    return result


@app.get(
    "/products",
    response_model=list[Product],
    tags=["商品"],
    summary="查询商品",
)
def list_products(
    q: str | None = None,
    category: Literal["book", "tool", "course"] | None = None,
    min_price: Annotated[float | None, Query(ge=0)] = None,
    max_price: Annotated[float | None, Query(ge=0)] = None,
    active_only: bool = True,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> list[Product]:
    """按多个查询参数组合过滤商品。"""
    products = list(_PRODUCTS)
    if active_only:
        products = [product for product in products if product.is_active]
    if category is not None:
        products = [product for product in products if product.category == category]
    products = _filter_by_keyword(products, q)
    products = _filter_by_price(products, min_price, max_price)
    return products[skip : skip + limit]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("solutions.02_query_filter:app", host="127.0.0.1", port=8001, reload=True)
