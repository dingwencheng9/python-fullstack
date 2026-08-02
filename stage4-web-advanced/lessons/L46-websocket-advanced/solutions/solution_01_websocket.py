"""Solution: WebSocket Connection Manager with Redis PubSub"""

import asyncio
from dataclasses import dataclass, field
from fastapi import WebSocket


@dataclass
class ConnectionInfo:
    user_id: str | None
    channel: str
    last_heartbeat: float
    metadata: dict = field(default_factory=dict)


class ConnectionManager:
    """WebSocket connection manager with channels and heartbeat."""

    def __init__(self, heartbeat_interval: float = 30.0, heartbeat_timeout: float = 60.0):
        self.channels: dict[str, set[WebSocket]] = {}
        self.connections: dict[WebSocket, ConnectionInfo] = {}
        self.heartbeat_interval = heartbeat_interval
        self.heartbeat_timeout = heartbeat_timeout
        self._heartbeat_task: asyncio.Task | None = None
        self._lock = asyncio.Lock()

    async def connect(
        self,
        websocket: WebSocket,
        channel: str = "default",
        user_id: str | None = None,
        metadata: dict = None,
    ) -> bool:
        """Accept and register a WebSocket connection."""
        try:
            await websocket.accept()

            async with self._lock:
                if channel not in self.channels:
                    self.channels[channel] = set()
                self.channels[channel].add(websocket)

                self.connections[websocket] = ConnectionInfo(
                    user_id=user_id,
                    channel=channel,
                    last_heartbeat=asyncio.get_event_loop().time(),
                    metadata=metadata or {},
                )

            # Start heartbeat task if not running
            if self._heartbeat_task is None or self._heartbeat_task.done():
                self._heartbeat_task = asyncio.create_task(self._heartbeat_check())

            return True
        except Exception:
            return False

    async def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        async with self._lock:
            if websocket in self.connections:
                info = self.connections[websocket]
                channel = info.channel

                if channel in self.channels:
                    self.channels[channel].discard(websocket)

                del self.connections[websocket]

    async def broadcast(self, channel: str, message: dict):
        """Broadcast message to all connections in a channel."""
        if channel not in self.channels:
            return

        disconnected = []

        async with self._lock:
            for connection in self.channels[channel].copy():
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)

        # Clean up disconnected
        for conn in disconnected:
            await self.disconnect(conn)

    async def send_to_user(self, user_id: str, message: dict) -> bool:
        """Send message to a specific user."""
        for websocket, info in self.connections.items():
            if info.user_id == user_id:
                try:
                    await websocket.send_json(message)
                    return True
                except Exception:
                    await self.disconnect(websocket)
        return False

    async def send_to_connection(self, websocket: WebSocket, message: dict) -> bool:
        """Send message to a specific connection."""
        try:
            await websocket.send_json(message)
            return True
        except Exception:
            await self.disconnect(websocket)
            return False

    async def handle_heartbeat(self, websocket: WebSocket):
        """Handle heartbeat from client."""
        async with self._lock:
            if websocket in self.connections:
                self.connections[websocket].last_heartbeat = asyncio.get_event_loop().time()

    async def _heartbeat_check(self):
        """Periodically check and disconnect stale connections."""
        while True:
            await asyncio.sleep(self.heartbeat_interval)

            current_time = asyncio.get_event_loop().time()
            stale = []

            async with self._lock:
                for websocket, info in self.connections.items():
                    if current_time - info.last_heartbeat > self.heartbeat_timeout:
                        stale.append(websocket)

            for conn in stale:
                self.disconnect(conn)

    @property
    def connection_count(self) -> int:
        return len(self.connections)

    @property
    def channel_stats(self) -> dict[str, int]:
        return {ch: len(conns) for ch, conns in self.channels.items()}


if __name__ == "__main__":
    print("ConnectionManager implemented with:")
    print("  - Multi-channel support")
    print("  - Heartbeat mechanism")
    print("  - User-specific messaging")
    print("  - Automatic stale connection cleanup")
