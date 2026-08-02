"""Capstone API 路由测试。"""

from __future__ import annotations

import pytest

pytest.importorskip("fastapi", reason="需要 fastapi")
pytest.importorskip("langgraph", reason="需要 langgraph（uv pip install langgraph）")

from fastapi.testclient import TestClient

from app.main import app
from app.routes.documents import _rag_cache

client = TestClient(app)


def setup_function() -> None:
    """清理 workspace RAG 存储，避免测试间污染。"""
    _rag_cache.cache.clear()


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_ready():
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.json()["status"] == "ready"


def test_document_ingest():
    res = client.post(
        "/documents",
        json={
            "title": "FastAPI",
            "content": "FastAPI 是现代 Python Web 框架",
        },
        headers={
            "X-User-Id": "test-editor",
            "X-Role": "editor",
            "X-Workspace-Id": "default",
        },
    )
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    assert res.json()["chunks"] >= 1
    assert res.json()["workspace_id"] == "default"


def test_document_stats():
    # 使用 editor 角色上传文档
    client.post(
        "/documents",
        json={"title": "Doc", "content": "内容"},
        headers={
            "X-User-Id": "test-editor",
            "X-Role": "editor",
            "X-Workspace-Id": "default",
        },
    )
    # 使用 admin 角色读取统计
    res = client.get(
        "/documents/stats",
        headers={
            "X-User-Id": "test-admin",
            "X-Role": "admin",
            "X-Workspace-Id": "default",
        },
    )
    assert res.status_code == 200
    assert "documents" in res.json()
    assert "chunks" in res.json()
    assert res.json()["workspace_id"] == "default"


def test_viewer_cannot_read_stats():
    """测试 viewer 角色不能读取统计信息。"""
    res = client.get(
        "/documents/stats",
        headers={
            "X-User-Id": "test-viewer",
            "X-Role": "viewer",
            "X-Workspace-Id": "default",
        },
    )
    # viewer 角色应该被禁止读取统计
    assert res.status_code == 403
    # 新的标准化错误响应格式
    assert res.json()["success"] is False
    assert "admin" in res.json()["error"]["message"]


def test_chat_no_docs_still_answers():
    res = client.post("/chat", json={"question": "什么是不存在的问题？"})
    assert res.status_code == 200
    assert "answer" in res.json()


def test_chat_with_document():
    # 使用 editor 角色在 default 工作空间上传文档
    client.post(
        "/documents",
        json={
            "title": "LangGraph",
            "content": "LangGraph 使用状态机构建 Agent。",
        },
        headers={
            "X-User-Id": "test-editor",
            "X-Role": "editor",
            "X-Workspace-Id": "default",
        },
    )
    # 使用 viewer 角色在同一工作空间聊天
    res = client.post(
        "/chat",
        json={"question": "LangGraph Agent"},
        headers={
            "X-User-Id": "test-viewer",
            "X-Role": "viewer",
            "X-Workspace-Id": "default",
        },
    )
    assert res.status_code == 200
    assert "LangGraph" in res.json()["answer"]
    assert res.json()["workspace_id"] == "default"


def test_workspace_isolation_for_chat():
    """测试工作空间隔离：alpha 工作空间的内容不应出现在 beta 工作空间的聊天中。"""
    # 在 alpha 工作空间上传 LangGraph 文档
    client.post(
        "/documents",
        json={
            "title": "LangGraph",
            "content": "LangGraph 使用状态机构建 Agent。",
        },
        headers={
            "X-User-Id": "test-editor",
            "X-Role": "editor",
            "X-Workspace-Id": "alpha",
        },
    )

    # 在 beta 工作空间聊天，不应包含 LangGraph 内容
    beta_res = client.post(
        "/chat",
        json={"question": "LangGraph Agent"},
        headers={
            "X-User-Id": "test-viewer",
            "X-Role": "viewer",
            "X-Workspace-Id": "beta",
        },
    )
    assert beta_res.status_code == 200
    assert "LangGraph" not in beta_res.json()["answer"]
    assert beta_res.json()["workspace_id"] == "beta"

    # 在 alpha 工作空间聊天，应该包含 LangGraph 内容
    alpha_res = client.post(
        "/chat",
        json={"question": "LangGraph Agent"},
        headers={
            "X-User-Id": "test-viewer",
            "X-Role": "viewer",
            "X-Workspace-Id": "alpha",
        },
    )
    assert alpha_res.status_code == 200
    assert "LangGraph" in alpha_res.json()["answer"]
    assert alpha_res.json()["workspace_id"] == "alpha"


def test_home_page():
    res = client.get("/")
    assert res.status_code == 200
    assert "AI Knowledge Assistant" in res.text


def test_sse_stream():
    with client.stream("GET", "/chat/stream?question=FastAPI") as res:
        assert res.status_code == 200
        body = "".join(res.iter_text())
        assert "data:" in body
        assert "[DONE]" in body


def test_viewer_cannot_upload_document():
    """测试 viewer 角色不能上传文档。"""
    res = client.post(
        "/documents",
        json={
            "title": "Test Document",
            "content": "Test content",
        },
        headers={
            "X-User-Id": "test-user",
            "X-Role": "viewer",
            "X-Workspace-Id": "default",
        },
    )
    # viewer 角色应该被禁止上传文档
    assert res.status_code == 403


def test_invalid_role_returns_403():
    """测试无效角色返回 403。"""
    res = client.get(
        "/documents/stats",
        headers={
            "X-User-Id": "test-user",
            "X-Role": "invalid-role",
            "X-Workspace-Id": "default",
        },
    )
    # 无效角色应该返回 403
    assert res.status_code == 403
