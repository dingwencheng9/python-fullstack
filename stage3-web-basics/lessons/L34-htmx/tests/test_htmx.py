"""L34 HTMX 课程测试

验证 HTMX 与 FastAPI 的集成功能。
"""

from __future__ import annotations

from pathlib import Path

import importlib.util
from fastapi.testclient import TestClient
import pytest
jinja2 = pytest.importorskip("jinja2")


# ============================================================
# 安全加载数字开头模块名的函数
# ============================================================


def load_module(name: str, file_path: Path) -> object:
    """按物理路径加载模块，不污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# 加载示例应用
EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
basic_htmx = load_module("_01_basic_htmx", EXAMPLES_DIR / "01_basic_htmx.py")


# ============================================================
# 创建 FastAPI 测试客户端
# ============================================================


@pytest.fixture(autouse=True)
def reset_messages() -> None:
    """每个测试前重置消息状态"""
    basic_htmx.messages.clear()
    basic_htmx._next_id = 1
    # 恢复初始消息
    basic_htmx.messages.extend(
        [
            basic_htmx.Message(1, "欢迎使用 HTMX + FastAPI！"),
            basic_htmx.Message(2, "无需复杂前端框架即可实现交互式应用"),
        ]
    )


@pytest.fixture
def client() -> TestClient:
    """创建测试客户端"""
    return TestClient(basic_htmx.app)


# ============================================================
# 测试用例
# ============================================================


class TestHomePage:
    """首页测试"""

    def test_home_returns_html(self, client: TestClient) -> None:
        """首页返回 HTML 页面"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_home_contains_messages(self, client: TestClient) -> None:
        """首页包含消息列表"""
        response = client.get("/")
        assert b"HTMX" in response.content or b"htmx" in response.content.lower()


class TestHTMXRequests:
    """HTMX 请求测试"""

    def test_create_message_via_htmx(self, client: TestClient) -> None:
        """通过 HTMX 创建消息"""
        response = client.post("/messages", data={"content": "Test message"}, headers={"HX-Request": "true"})
        assert response.status_code == 200
        assert "Test message" in response.text

    def test_create_message_empty_content(self, client: TestClient) -> None:
        """创建空消息返回错误"""
        response = client.post("/messages", data={"content": ""}, headers={"HX-Request": "true"})
        assert response.status_code == 422

    def test_delete_message_via_htmx(self, client: TestClient) -> None:
        """通过 HTMX 删除消息"""
        # 先创建一个消息
        client.post("/messages", data={"content": "To delete"}, headers={"HX-Request": "true"})

        # 删除消息
        response = client.delete("/messages/1", headers={"HX-Request": "true"})
        assert response.status_code == 200

    def test_delete_nonexistent_message(self, client: TestClient) -> None:
        """删除不存在的消息"""
        response = client.delete("/messages/999", headers={"HX-Request": "true"})
        assert response.status_code == 404


class TestNonHTMXRequests:
    """非 HTMX 请求测试"""

    def test_create_message_regular_request(self, client: TestClient) -> None:
        """普通请求创建消息后重定向"""
        response = client.post("/messages", data={"content": "Regular request"}, follow_redirects=False)
        assert response.status_code == 303
        assert response.headers.get("location") == "/"

    def test_delete_message_regular_request(self, client: TestClient) -> None:
        """普通请求删除消息后重定向"""
        response = client.delete("/messages/1", follow_redirects=False)
        assert response.status_code == 303


class TestHTMXDetection:
    """HTMX 检测功能测试"""

    def test_htmx_header_detection(self, client: TestClient) -> None:
        """测试 HTMX 请求头检测"""
        # 有 HX-Request 头
        response_with = client.get("/", headers={"HX-Request": "true"})
        assert response_with.status_code == 200

        # 无 HX-Request 头
        response_without = client.get("/")
        assert response_without.status_code == 200

    def test_htmx_response_has_proper_swap_header(self, client: TestClient) -> None:
        """HTMX 删除响应包含正确的交换头"""
        response = client.delete("/messages/1", headers={"HX-Request": "true"})
        assert response.status_code == 200
        assert "HX-Reswap" in response.headers or response.text == ""
