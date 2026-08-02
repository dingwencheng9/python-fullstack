"""示例 1: WebSocket 连接管理器"""

from fastapi import WebSocket, WebSocketDisconnect
from dataclasses import dataclass, field


@dataclass
class ConnectionManager:
    """WebSocket 连接管理器"""

    active_connections: dict[str, set[WebSocket]] = field(default_factory=dict)

    async def connect(self, websocket: WebSocket, channel: str = "default"):
        """连接"""
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        self.active_connections[channel].add(websocket)

    def disconnect(self, websocket: WebSocket, channel: str = "default"):
        """断开连接"""
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)

    async def broadcast(self, channel: str, message: str):
        """广播消息"""
        if channel in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[channel]:
                try:
                    await connection.send_text(message)
                except Exception:
                    disconnected.add(connection)
            # 清理断开连接
            for conn in disconnected:
                self.disconnect(conn, channel)

    @property
    def connection_count(self) -> int:
        """连接数"""
        return sum(len(conns) for conns in self.active_connections.values())


manager = ConnectionManager()


async def websocket_handler(websocket: WebSocket, channel: str = "default"):
    """WebSocket 处理器"""
    await manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            # 处理消息并广播
            await manager.broadcast(channel, f"echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
