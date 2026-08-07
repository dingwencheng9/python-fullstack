"""L28 FastAPI 基础测试。"""

from __future__ import annotations

import importlib

import pytest

pytest.importorskip("fastapi", reason="fastapi 未安装")

from fastapi.testclient import TestClient

crud_module = importlib.import_module("solutions.solution_01")
query_module = importlib.import_module("solutions.solution_02")


@pytest.fixture
def client() -> TestClient:
    """共享 TestClient。"""
    if hasattr(crud_module, "reset_storage"):
        crud_module.reset_storage()
    return TestClient(crud_module.app)


def test_create_item(client: TestClient) -> None:
    response = client.post("/items", json={"name": "test", "price": 10.0})
    assert response.status_code == 201
    assert response.json()["name"] == "test"


def test_list_items_returns_array(client: TestClient) -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.parametrize(
    ("price", "expected_status"),
    [
        (-1, 422),
        (0, 201),
        (999999, 201),
    ],
)
def test_create_item_price_validation(
    client: TestClient,
    price: float,
    expected_status: int,
) -> None:
    response = client.post("/items", json={"name": "x", "price": price})
    assert response.status_code == expected_status


def test_get_nonexistent_item_returns_404(client: TestClient) -> None:
    """异常路径。"""
    response = client.get("/items/99999")
    assert response.status_code == 404


def test_update_item(client: TestClient) -> None:
    """完整 CRUD：先创建再更新。"""
    created = client.post("/items", json={"name": "orig", "price": 1.0}).json()
    response = client.put(
        f"/items/{created['id']}",
        json={"name": "updated", "price": 2.0},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "updated"


def test_delete_item(client: TestClient) -> None:
    created = client.post("/items", json={"name": "doomed", "price": 5.0}).json()
    response = client.delete(f"/items/{created['id']}")
    assert response.status_code == 204


def test_query_filter_by_category() -> None:
    query_client = TestClient(query_module.app)
    response = query_client.get("/products", params={"category": "book"})
    assert response.status_code == 200
    assert all(item["category"] == "book" for item in response.json())


def test_query_filter_rejects_invalid_price_range() -> None:
    query_client = TestClient(query_module.app)
    response = query_client.get("/products", params={"min_price": 100, "max_price": 10})
    assert response.status_code == 400
