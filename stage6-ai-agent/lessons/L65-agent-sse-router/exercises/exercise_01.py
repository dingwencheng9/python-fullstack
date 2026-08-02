"""
L64: Agent SSE 路由器 - 练习题

本练习将实现一个基于 SSE (Server-Sent Events) 的 Agent 路由器。

练习要求：
1. 实现 SSE 事件流处理
2. 实现多路复用路由
3. 实现背压控制
"""

import asyncio
from collections.abc import AsyncGenerator, Callable
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """SSE 事件类型"""

    TOKEN = "token"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    DONE = "done"


@dataclass
class SSEEvent:
    """SSE 事件"""

    event_type: EventType
    data: dict
    event_id: str = None


class SSERouter:
    """
    SSE 路由器

    负责将来自多个 Agent 的 SSE 事件流路由到对应的客户端。
    """

    def __init__(self):
        self.routes: dict[str, asyncio.Queue] = {}
        self._running = False

    async def register_route(self, route_id: str) -> None:
        """注册路由"""
        if route_id not in self.routes:
            self.routes[route_id] = asyncio.Queue(maxsize=100)

    async def unregister_route(self, route_id: str) -> None:
        """注销路由"""
        if route_id in self.routes:
            await self.routes[route_id].put(None)  # 发送结束信号
            del self.routes[route_id]

    async def send_event(self, route_id: str, event: SSEEvent) -> None:
        """发送事件"""
        if route_id in self.routes:
            try:
                self.routes[route_id].put_nowait(event)
            except asyncio.QueueFull:
                # 背压控制：队列满时丢弃旧事件
                try:
                    self.routes[route_id].get_nowait()
                    self.routes[route_id].put_nowait(event)
                except asyncio.QueueEmpty:
                    pass

    async def stream_events(self, route_id: str) -> AsyncGenerator[SSEEvent]:
        """流式获取事件"""
        if route_id not in self.routes:
            return

        queue = self.routes[route_id]

        while self._running:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=30.0)
                if event is None:
                    break
                yield event
            except TimeoutError:
                # 发送心跳
                yield SSEEvent(EventType.DONE, {"heartbeat": True})

    async def start(self) -> None:
        """启动路由器"""
        self._running = True

    async def stop(self) -> None:
        """停止路由器"""
        self._running = False
        for route_id in list(self.routes.keys()):
            await self.unregister_route(route_id)


# 练习：实现多路复用路由器
class MultiplexingRouter(SSERouter):
    """
    多路复用路由器

    支持将多个 Agent 的输出合并到一个 SSE 流中。
    """

    async def multiplex(self, agent_streams: list[tuple[str, AsyncGenerator[SSEEvent]]]) -> AsyncGenerator[tuple[str, SSEEvent]]:
        """
        多路复用多个 Agent 流

        Args:
            agent_streams: [(route_id, stream), ...] 的列表

        Yields:
            (route_id, event) 元组
        """
        # TODO: 实现多路复用逻辑
        # 提示：使用 asyncio.gather 或 asyncio.create_task


# 练习：实现背压控制
class BackpressureRouter(SSERouter):
    """
    带背压控制的路由器

    当客户端处理速度慢于服务端发送速度时，
    自动降低发送速率或暂停发送。
    """

    async def send_with_backpressure(self, route_id: str, event: SSEEvent, client_ready: Callable[[], bool]) -> bool:
        """
        带背压控制的事件发送

        Args:
            route_id: 路由 ID
            event: SSE 事件
            client_ready: 回调函数，判断客户端是否准备好接收

        Returns:
            True 如果发送成功，False 如果被背压暂停
        """
        # TODO: 实现背压控制逻辑


# 测试代码
async def test_router():
    """测试路由器"""
    router = SSERouter()
    await router.start()

    # 注册路由
    await router.register_route("agent-1")

    # 创建事件流任务
    async def generate_events():
        for i in range(10):
            event = SSEEvent(EventType.TOKEN, {"content": f"Token {i}"}, event_id=f"evt-{i}")
            await router.send_event("agent-1", event)
            await asyncio.sleep(0.01)

    # 启动事件生成
    task = asyncio.create_task(generate_events())

    # 消费事件
    count = 0
    async for event in router.stream_events("agent-1"):
        print(f"Received: {event.event_type.value} - {event.data}")
        count += 1
        if count >= 10:
            break

    await task
    await router.stop()

    print(f"Test completed: {count} events received")


if __name__ == "__main__":
    asyncio.run(test_router())
