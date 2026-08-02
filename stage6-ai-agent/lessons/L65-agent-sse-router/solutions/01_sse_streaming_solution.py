"""

from __future__ import annotations

练习 1: SSE 流式输出实现 - 参考答案

本解决方案展示：
1. Python 3.13 PEP 695 泛型语法
2. asyncio.TaskGroup 结构化并发
3. SSE 协议完整实现
4. Free-threading 线程安全考量

作者：Python 3.13 全栈课程
"""

import asyncio
import json
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

# ============================================================================
# 1. SSE 事件类（使用 PEP 695 泛型）
# ============================================================================


@dataclass
class SSEEvent[T]:
    """
    SSE 事件类（Python 3.13 PEP 695 泛型语法）

    泛型参数:
        T: 事件数据类型
    """

    data: T
    event: str | None = None
    id: str | None = None
    retry: int | None = None

    def format(self) -> str:
        """
        格式化为 SSE 协议格式

        SSE 协议规范:
        - 每个字段一行
        - data 字段可以多行
        - 事件以双换行符结束 (\\n\\n)
        """
        lines: list[str] = []

        if self.id is not None:
            lines.append(f"id: {self.id}")

        if self.event is not None:
            lines.append(f"event: {self.event}")

        if self.retry is not None:
            lines.append(f"retry: {self.retry}")

        # data 字段（支持 JSON 序列化）
        if isinstance(self.data, str):
            data_str = self.data
        else:
            data_str = json.dumps(self.data, ensure_ascii=False)

        lines.append(f"data: {data_str}")

        # SSE 事件必须以双换行符结束
        return "\n".join(lines) + "\n\n"


# ============================================================================
# 2. 连接管理器（Python 3.13 Free-threading 线程安全设计）
# ============================================================================


class ConnectionManager[T]:
    """
    连接管理器（Python 3.13 PEP 695 泛型）

    🔒 Free-threading 线程安全说明:
    - asyncio.Queue 在 asyncio event loop 内是线程安全的
    - Python 3.14 (Free-threading) 环境下，多个 OS 线程可以并发执行
    - 使用 asyncio.Queue 管理连接，避免 GIL 争用

    泛型参数:
        T: 消息数据类型
    """

    def __init__(self) -> None:
        # 🔒 dict 在 Python 3.14 中仍需要外部同步（dict 本身不是线程安全的）
        # 但在 asyncio 单线程事件循环中是安全的
        self.active_connections: dict[str, asyncio.Queue[T]] = {}
        self._connection_count = 0

    async def connect(self, client_id: str) -> asyncio.Queue[T]:
        """
        添加新连接

        Args:
            client_id: 客户端唯一标识

        Returns:
            为该客户端创建的消息队列
        """
        queue: asyncio.Queue[T] = asyncio.Queue()
        self.active_connections[client_id] = queue
        self._connection_count += 1
        return queue

    def disconnect(self, client_id: str) -> None:
        """
        移除连接

        Args:
            client_id: 客户端唯一标识
        """
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def broadcast(self, message: T) -> int:
        """
        广播消息到所有客户端（使用 asyncio.TaskGroup）

        🚀 Python 3.13 asyncio.TaskGroup:
        - 结构化并发，自动等待所有任务完成
        - 异常安全，任何任务失败会取消其他任务
        - 相比手动 gather，代码更清晰

        Args:
            message: 要广播的消息

        Returns:
            成功发送的客户端数量
        """
        if not self.active_connections:
            return 0

        sent_count = 0

        async with asyncio.TaskGroup() as tg:
            for _client_id, queue in self.active_connections.items():
                # 创建并发任务
                tg.create_task(queue.put(message))
                sent_count += 1

        return sent_count

    async def send_to_client(self, client_id: str, message: T) -> bool:
        """
        发送消息到特定客户端

        Args:
            client_id: 客户端唯一标识
            message: 要发送的消息

        Returns:
            是否发送成功
        """
        queue = self.active_connections.get(client_id)
        if queue is None:
            return False

        await queue.put(message)
        return True


# ============================================================================
# 3. SSE 流生成器（使用 PEP 695 泛型和 asyncio.TaskGroup）
# ============================================================================


async def sse_generator[T](
    queue: asyncio.Queue[T],
    heartbeat_interval: int = 30,
) -> AsyncGenerator[str]:
    """
    SSE 事件流生成器（Python 3.13 PEP 695 泛型语法）

    功能:
    1. 从队列读取消息
    2. 格式化为 SSE 事件
    3. 发送心跳（防止连接超时）
    4. 处理关闭信号
    5. 优雅处理客户端断开（CancelledError）

    Args:
        queue: 消息队列
        heartbeat_interval: 心跳间隔（秒）

    Yields:
        格式化的 SSE 事件字符串

    Raises:
        asyncio.CancelledError: 客户端断开或服务器关闭
    """
    last_heartbeat = datetime.now(UTC)

    try:
        while True:
            # 使用超时避免永久阻塞
            try:
                message = await asyncio.wait_for(queue.get(), timeout=1.0)

                # 处理关闭信号
                if message == "__CLOSE__":
                    break

                # 格式化并发送事件
                event = SSEEvent(data=message, event="message")
                yield event.format()

            except TimeoutError:
                # 检查是否需要发送心跳
                now = datetime.now(UTC)
                if (now - last_heartbeat).total_seconds() >= heartbeat_interval:
                    # 发送心跳事件
                    heartbeat = SSEEvent(
                        data={"type": "heartbeat", "timestamp": now.isoformat()},
                        event="heartbeat",
                    )
                    yield heartbeat.format()
                    last_heartbeat = now

    except asyncio.CancelledError:
        # 客户端断开或服务器关闭 → 优雅退出
        # 尝试发送最终的关闭事件（如果客户端仍然连接）
        try:
            close_event = SSEEvent(
                data={"type": "close", "reason": "client_disconnected"},
                event="close",
            )
            yield close_event.format()
        except Exception:
            # 客户端已完全断开，发送失败是正常的
            pass
        raise  # 必须重新抛出，让 asyncio 正确清理任务

    finally:
        # 生成器清理（队列会被 GC 自动回收）
        pass


# ============================================================================
# 4. FastAPI 应用和 SSE 端点
# ============================================================================

app = FastAPI(title="SSE 流式输出系统 - Python 3.13")

# 全局连接管理器（泛型实例化）
manager: ConnectionManager[dict[str, Any]] = ConnectionManager()


@app.get("/")
async def root() -> dict[str, Any]:
    """根端点"""
    return {
        "message": "SSE 流式输出系统 (Python 3.13)",
        "features": [
            "PEP 695 泛型语法",
            "asyncio.TaskGroup 结构化并发",
            "Free-threading 线程安全设计",
        ],
        "endpoints": {
            "/stream": "SSE 事件流",
            "/send/{client_id}": "发送消息到客户端",
            "/broadcast": "广播消息",
        },
    }


@app.get("/stream")
async def stream_events(request: Request, client_id: str = "default") -> StreamingResponse:
    """
    SSE 事件流端点

    Args:
        request: FastAPI Request 对象
        client_id: 客户端唯一标识

    Returns:
        StreamingResponse 包含 SSE 流
    """
    # 1. 创建客户端队列
    queue = await manager.connect(client_id)

    # 2. 发送连接成功消息
    await queue.put(
        {
            "type": "connection",
            "status": "connected",
            "client_id": client_id,
            "timestamp": datetime.now(UTC).isoformat(),
        }
    )

    # 3. 创建 SSE 生成器
    async def event_stream() -> AsyncGenerator[str]:
        try:
            async for event in sse_generator(queue, heartbeat_interval=30):
                # 检查客户端是否断开连接
                if await request.is_disconnected():
                    break
                yield event
        finally:
            # 清理连接
            manager.disconnect(client_id)

    # 4. 返回 StreamingResponse（正确的 SSE headers）
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 Nginx 缓冲
        },
    )


@app.post("/send/{client_id}")
async def send_message(client_id: str, message: str) -> dict[str, Any]:
    """
    发送消息到特定客户端

    Args:
        client_id: 客户端唯一标识
        message: 消息内容

    Returns:
        发送结果
    """
    success = await manager.send_to_client(
        client_id,
        {"type": "message", "content": message, "timestamp": datetime.now(UTC).isoformat()},
    )

    if success:
        return {"status": "sent", "client_id": client_id, "message": message}
    return {"status": "failed", "error": "Client not connected"}


@app.post("/broadcast")
async def broadcast_message(message: str) -> dict[str, Any]:
    """
    广播消息到所有客户端（使用 asyncio.TaskGroup）

    🚀 Python 3.13 asyncio.TaskGroup:
    - manager.broadcast() 内部使用 TaskGroup 并发发送
    - 结构化并发，自动等待所有任务完成

    Args:
        message: 消息内容

    Returns:
        广播统计
    """
    sent_count = await manager.broadcast({"type": "broadcast", "content": message, "timestamp": datetime.now(UTC).isoformat()})

    return {
        "status": "broadcasted",
        "message": message,
        "recipients": sent_count,
        "timestamp": datetime.now(UTC).isoformat(),
    }


# ============================================================================
# 5. 客户端示例（测试用）
# ============================================================================


async def sse_client_example() -> None:
    """
    SSE 客户端示例

    演示如何连接和接收 SSE 事件
    """
    import httpx

    async with httpx.AsyncClient() as client:
        client_id = "test_client"
        url = f"http://localhost:8000/stream?client_id={client_id}"

        print(f"连接到 SSE 端点: {url}")

        async with client.stream("GET", url) as response:
            print(f"连接状态: {response.status_code}")

            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    data = line[5:].strip()
                    print(f"收到数据: {data}")

                elif line.startswith("event:"):
                    event_type = line[6:].strip()
                    print(f"事件类型: {event_type}")

                elif line == "":
                    # 事件结束（双换行符）
                    print("---")


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    from core.settings import get_settings

    settings = get_settings()
    import uvicorn

    print("=" * 70)
    print("SSE 流式输出系统 - Python 3.13 参考答案")
    print("=" * 70)
    print("\n特性:")
    print("  ✅ PEP 695 泛型语法: def func[T](), class Name[T]")
    print("  ✅ asyncio.TaskGroup: 结构化并发")
    print("  ✅ Free-threading 线程安全设计")
    print("  ✅ SSE 协议完整实现")
    print("\n启动服务:")
    print("  uvicorn solutions.01_sse_streaming_solution:app --reload")
    print("\n测试端点:")
    print("  1. 浏览器: http://localhost:8000/stream?client_id=test1")
    print("  2. 发送消息: curl -X POST 'http://localhost:8000/send/test1?message=Hello'")
    print("  3. 广播: curl -X POST 'http://localhost:8000/broadcast?message=Broadcast'")
    print()

    uvicorn.run(
        app,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
    )
