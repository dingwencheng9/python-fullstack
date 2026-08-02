"""Exercise 1: WebSocket Manager"""

import asyncio
from dataclasses import dataclass, field
from fastapi import WebSocket


@dataclass
class ConnectionManager:
    """WebSocket connection manager"""

    channels: dict[str, set[WebSocket]] = field(default_factory=dict)

    async def connect(self, websocket: WebSocket, channel: str = "default"):
        await websocket.accept()
        if channel not in self.channels:
            self.channels[channel] = set()
        self.channels[channel].add(websocket)

    def disconnect(self, websocket: WebSocket, channel: str = "default"):
        if channel in self.channels:
            self.channels[channel].discard(websocket)

    @property
    def count(self) -> int:
        return sum(len(c) for c in self.channels.values())


async def test():
    # Just verify class is defined
    manager = ConnectionManager()
    print(f"PASS: Connection manager defined, count={manager.count}")


if __name__ == "__main__":
    asyncio.run(test())
