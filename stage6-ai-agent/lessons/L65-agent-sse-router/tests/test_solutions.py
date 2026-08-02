"""

from __future__ import annotations

L34 Agent SSE Router 完整测试套件

测试维度:
1. solutions/ 模块导入和功能测试
2. FastAPI SSE 流式响应测试
3. Agent 路由边界和异常路径测试
4. Checkpoint 错误处理测试
"""

from __future__ import annotations

import asyncio
import importlib
from typing import TYPE_CHECKING

import pytest

pytest.importorskip("fastapi", reason="需要 FastAPI（uv sync --extra web）")

from fastapi.testclient import TestClient

# sys.path 注入由同目录 conftest.py 统一管理，严禁在此污染

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from pathlib import Path
    from types import ModuleType
    from typing import Any


@pytest.fixture(scope="module")
def sol01() -> ModuleType:
    """加载 SSE 流式输出参考实现。"""
    return importlib.import_module("solutions.01_sse_streaming_solution")


@pytest.fixture(scope="module")
def sol02() -> ModuleType:
    """加载 Agent 路由参考实现。"""
    return importlib.import_module("solutions.02_agent_router_solution")


@pytest.fixture(scope="module")
def sol03() -> ModuleType:
    """加载 Checkpoint 参考实现。"""
    return importlib.import_module("solutions.03_checkpoint_solution")


@pytest.fixture
def sse_client(sol01: ModuleType, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """创建 SSE 应用测试客户端，并让测试流可自动结束。"""

    class FiniteConnectionManager:
        def __init__(self) -> None:
            self.active_connections: dict[str, asyncio.Queue[dict[str, str] | str]] = {}

        async def connect(self, client_id: str) -> asyncio.Queue[dict[str, str] | str]:
            queue: asyncio.Queue[dict[str, str] | str] = asyncio.Queue()
            self.active_connections[client_id] = queue
            await queue.put({"type": "connection", "status": "connected", "client_id": client_id})
            await queue.put("__CLOSE__")
            return queue

        def disconnect(self, client_id: str) -> None:
            self.active_connections.pop(client_id, None)

        async def send_to_client(self, client_id: str, message: dict[str, str]) -> bool:
            queue = self.active_connections.get(client_id)
            if queue is None:
                return False
            await queue.put(message)
            return True

        async def broadcast(self, message: dict[str, str]) -> int:
            for queue in self.active_connections.values():
                await queue.put(message)
            return len(self.active_connections)

    monkeypatch.setattr(sol01, "manager", FiniteConnectionManager())
    return TestClient(sol01.app)


@pytest.fixture
def agent_client(sol02: ModuleType, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """创建使用 mock Agent Router 的测试客户端，避免慢速或外部依赖。"""

    class MockRouter:
        async def route(self, user_input: str) -> AsyncGenerator[dict[str, Any]]:
            yield {"type": "routing", "selected_agent": "general"}
            yield {"type": "token", "content": f"mock:{user_input}"}
            yield {"type": "complete", "content": "done"}

    monkeypatch.setattr(sol02, "router", MockRouter())
    return TestClient(sol02.app)


@pytest.mark.parametrize(
    ("module_name", "expected_attr"),
    [
        ("solutions.01_sse_streaming_solution", "sse_generator"),
        ("solutions.02_agent_router_solution", "AgentRouter"),
        ("solutions.03_checkpoint_solution", "CheckpointManager"),
    ],
)
def test_import_solution_modules(module_name: str, expected_attr: str) -> None:
    """测试三个参考实现模块都可以从仓库根目录导入。"""
    module = importlib.import_module(module_name)

    assert hasattr(module, expected_attr)


@pytest.mark.parametrize(
    ("payload", "event", "expected"),
    [
        ({"type": "test", "content": "hello"}, "message", "event: message"),
        ("plain text", "notice", "data: plain text"),
    ],
)
def test_sse_event_formats_supported_payloads(
    sol01: ModuleType,
    payload: dict[str, str] | str,
    event: str,
    expected: str,
) -> None:
    """测试 SSE 事件支持 JSON 和纯文本载荷。"""
    sse_event = sol01.SSEEvent(data=payload, event=event, id="evt-1")

    formatted = sse_event.format()

    assert "id: evt-1" in formatted
    assert expected in formatted
    assert formatted.endswith("\n\n")


@pytest.mark.asyncio
async def test_sse_generator_closes_on_close_signal(sol01: ModuleType) -> None:
    """测试 SSE 生成器收到关闭信号后正常结束。"""
    queue: asyncio.Queue[dict[str, str] | str] = asyncio.Queue()
    await queue.put({"type": "message", "content": "hello"})
    await queue.put("__CLOSE__")

    events: list[str] = []
    async for event in sol01.sse_generator(queue, heartbeat_interval=30):
        events.append(event)

    assert len(events) == 1
    assert "event: message" in events[0]
    assert "hello" in events[0]


def test_sse_stream_endpoint_returns_event_stream_headers(sse_client: TestClient) -> None:
    """测试 SSE 路由返回流式响应头。"""
    response = sse_client.get("/stream", params={"client_id": "header-client"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.headers["cache-control"] == "no-cache"
    assert "data:" in response.text
    assert "connected" in response.text


@pytest.mark.parametrize(
    ("client_id", "message", "expected_status"),
    [
        ("missing-session", "hello", "failed"),
        ("", "hello", "failed"),
    ],
)
def test_send_message_reports_invalid_session_id(
    sse_client: TestClient,
    client_id: str,
    message: str,
    expected_status: str,
) -> None:
    """测试无效 session_id 不会误报发送成功。"""
    response = sse_client.post(f"/send/{client_id}", params={"message": message})

    assert response.status_code in {200, 404}
    if response.status_code == 200:
        assert response.json()["status"] == expected_status


def test_chat_stream_uses_mock_router(agent_client: TestClient) -> None:
    """测试 Agent 对话端点输出 SSE 流式响应。"""
    response = agent_client.post("/chat", json={"message": "你好"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert "data:" in response.text
    assert "mock:你好" in response.text


@pytest.mark.parametrize(
    ("message", "expected_agent"),
    [
        ("", "general"),
        ("x" * 5000, "general"),
        ("帮我写 Python 算法", "code"),
        ("分析 pandas 数据报表", "data"),
    ],
)
def test_intent_classifier_handles_boundary_queries(
    sol02: ModuleType,
    message: str,
    expected_agent: str,
) -> None:
    """测试空 query、超长 query 和典型 query 的路由边界。"""
    classifier = sol02.IntentClassifier()

    agent_type = classifier.classify(message)

    assert agent_type.value == expected_agent


def test_chat_rejects_malformed_input(agent_client: TestClient) -> None:
    """测试 malformed input 触发 FastAPI 校验错误。"""
    response = agent_client.post("/chat", json={"user_id": "u-1"})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_base_agent_requires_generate_response(sol02: ModuleType) -> None:
    """测试未实现响应生成的 Agent 会抛出异常。"""
    agent = sol02.BaseAgent(sol02.AgentType.GENERAL, "system")

    with pytest.raises(NotImplementedError, match="子类必须实现"):
        await agent._generate_response("hello")


@pytest.mark.asyncio
async def test_connection_manager_operations(sol01: ModuleType) -> None:
    """测试连接管理器的连接、发送和断开流程。"""
    manager = sol01.ConnectionManager[str]()

    queue = await manager.connect("client1")
    success = await manager.send_to_client("client1", "test message")
    message = await asyncio.wait_for(queue.get(), timeout=1.0)
    missing_success = await manager.send_to_client("missing", "test")
    manager.disconnect("client1")

    assert success is True
    assert message == "test message"
    assert missing_success is False
    assert "client1" not in manager.active_connections


@pytest.mark.asyncio
async def test_checkpoint_manager_save_load_with_tmp_path(
    sol03: ModuleType,
    tmp_path: Path,
) -> None:
    """测试 Checkpoint 管理器使用临时目录保存和加载会话。"""
    manager = sol03.CheckpointManager(storage_dir=str(tmp_path))
    conversation = sol03.Conversation(
        conversation_id="conv-1",
        user_id="user-1",
    )
    conversation.add_message(sol03.Message(role="user", content="Hello"))

    checkpoint_id = await manager.save_checkpoint(conversation)
    loaded = await manager.load_checkpoint("conv-1")

    assert checkpoint_id and isinstance(checkpoint_id, str)
    assert loaded is not None
    assert loaded.conversation.conversation_id == "conv-1"


def test_checkpoint_api_returns_404_for_invalid_session(sol03: ModuleType) -> None:
    """测试无效会话 ID 会返回明确的 404 错误。"""
    client = TestClient(sol03.app)

    response = client.get("/conversations/not-exists")

    assert response.status_code == 404
    assert response.json()["detail"] == "会话不存在"
