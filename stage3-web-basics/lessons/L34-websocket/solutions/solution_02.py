"""L33 练习 1: 房间管理增强 — 参考答案

from __future__ import annotations

不依赖 FastAPI，使用 send_text 接口约定。
"""

from __future__ import annotations

from typing import Any


class DisconnectError(Exception):
    """模拟连接断开"""


class ChatRoom:
    """聊天室管理器，不依赖 FastAPI"""

    def __init__(self) -> None:
        self.rooms: dict[str, set[Any]] = {}

    async def join(self, room: str, ws: Any) -> None:
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(ws)

    async def leave(self, room: str, ws: Any) -> None:
        self.rooms[room].discard(ws)
        if not self.rooms[room]:
            del self.rooms[room]

    async def broadcast(self, room: str, message: str) -> None:
        if room not in self.rooms:
            return
        for ws in list(self.rooms[room]):
            try:
                await ws.send_text(message)
            except DisconnectError:
                self.rooms[room].discard(ws)
        if not self.rooms[room]:
            del self.rooms[room]

    def get_online_count(self, room: str) -> int:
        return len(self.rooms.get(room, set()))

    def list_rooms(self) -> list[str]:
        return list(self.rooms.keys())
