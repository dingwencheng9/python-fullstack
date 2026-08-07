"""

from __future__ import annotations

练习 1: SSE 流式输出实现

任务：
实现基于 Server-Sent Events (SSE) 的实时数据流系统。

学习目标：
- 理解 SSE 协议和规范
- 实现 SSE 端点和事件流
- 处理客户端连接管理
- 实现心跳和重连机制

预计时间: 60 分钟
难度: ⭐⭐⭐⭐☆
"""

import asyncio
from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request

# ============================================================================
# TODO 1: 理解 SSE 协议
# ============================================================================

"""
SSE (Server-Sent Events) 协议规范：

1. Content-Type: text/event-stream
2. Cache-Control: no-cache
3. Connection: keep-alive

事件格式：
data: <message>\n\n

带ID和类型：
id: <event_id>
event: <event_type>
data: <message>
\n\n

重试间隔：
retry: <milliseconds>\n\n
"""


# ============================================================================
# TODO 2: 实现 SSE 事件类
# ============================================================================

# TODO: 创建 SSE 事件类
# class SSEEvent:
#     def __init__(
#         self,
#         data: str,
#         event: str | None = None,
#         id: str | None = None,
#         retry: int | None = None
#     ):
#         pass
#
#     def format(self) -> str:
#         """格式化为 SSE 协议格式"""
#         pass


# ============================================================================
# TODO 3: 实现连接管理器
# ============================================================================

# TODO: 创建连接管理器
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: dict[str, asyncio.Queue] = {}
#
#     async def connect(self, client_id: str) -> asyncio.Queue:
#         """添加新连接"""
#         pass
#
#     def disconnect(self, client_id: str) -> None:
#         """移除连接"""
#         pass
#
#     async def broadcast(self, message: str) -> None:
#         """广播消息到所有客户端"""
#         pass
#
#     async def send_to_client(self, client_id: str, message: str) -> None:
#         """发送消息到特定客户端"""
#         pass


# ============================================================================
# TODO 4: 实现 SSE 流生成器
# ============================================================================


async def sse_generator(queue: asyncio.Queue, heartbeat_interval: int = 30) -> AsyncGenerator[str]:
    """SSE 事件流生成器"""
    # TODO:
    # 1. 从队列读取消息
    # 2. 格式化为 SSE 事件
    # 3. 发送心跳（防止连接超时）
    # 4. 处理关闭信号


# ============================================================================
# TODO 5: 创建 FastAPI 应用和 SSE 端点
# ============================================================================

app = FastAPI(title="SSE 流式输出练习")

# TODO: 创建全局连接管理器
# manager = ConnectionManager()


@app.get("/")
async def root():
    """根端点"""
    return {
        "message": "SSE 流式输出系统",
        "endpoints": {
            "/stream": "SSE 事件流",
            "/send": "发送消息",
            "/broadcast": "广播消息",
        },
    }


@app.get("/stream")
async def stream_events(request: Request, client_id: str = "default"):
    """SSE 事件流端点"""
    # TODO:
    # 1. 创建客户端队列
    # 2. 注册连接
    # 3. 返回 StreamingResponse
    # 4. 设置正确的 headers
    # 5. 处理断开连接


@app.post("/send/{client_id}")
async def send_message(client_id: str, message: str):
    """发送消息到特定客户端"""
    # TODO:
    # 1. 验证客户端存在
    # 2. 发送消息
    # 3. 返回结果


@app.post("/broadcast")
async def broadcast_message(message: str):
    """广播消息到所有客户端"""
    # TODO:
    # 1. 调用 manager.broadcast
    # 2. 返回发送统计


# ============================================================================
# TODO 6: 实现客户端示例（测试用）
# ============================================================================


async def sse_client_example():
    """SSE 客户端示例"""

    # TODO:
    # 1. 创建 httpx.AsyncClient
    # 2. 连接到 /stream
    # 3. 逐行读取事件
    # 4. 解析 SSE 事件
    # 5. 处理断线重连


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 1: SSE 流式输出实现")
    print("=" * 70)
    print("\n任务：")
    print("  1. 实现 SSE 事件类")
    print("  2. 创建连接管理器")
    print("  3. 实现 SSE 流生成器")
    print("  4. 创建 SSE 端点")
    print("  5. 实现消息发送和广播")
    print("  6. 测试客户端连接")
    print("\n测试方法：")
    print("  1. 启动服务: uvicorn exercises.01_sse_streaming:app --reload")
    print("  2. 浏览器访问: http://localhost:8000/stream?client_id=test1")
    print("  3. 发送消息: curl -X POST http://localhost:8000/send/test1?message=Hello")
    print("  4. 广播消息: curl -X POST http://localhost:8000/broadcast?message=Broadcast")
    print("\nSSE 协议要点：")
    print("  - Content-Type: text/event-stream")
    print("  - 每个事件以双换行符结束 (\\n\\n)")
    print("  - 支持事件ID和类型")
    print("  - 客户端自动重连")
    print()
