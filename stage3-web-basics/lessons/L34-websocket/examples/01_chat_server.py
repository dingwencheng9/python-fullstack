"""L33 WebSocket 聊天室服务器"""

from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ChatRoom:
    """聊天室管理器"""

    def __init__(self) -> None:
        self.rooms: dict[str, set[WebSocket]] = {}

    async def join(self, room: str, ws: WebSocket) -> None:
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(ws)
        await self.broadcast(room, f"新成员加入 ({len(self.rooms[room])} 人在线)")

    async def leave(self, room: str, ws: WebSocket) -> None:
        self.rooms[room].discard(ws)
        if not self.rooms[room]:
            del self.rooms[room]
        else:
            await self.broadcast(room, "成员离开")

    async def broadcast(self, room: str, message: str) -> None:
        if room in self.rooms:
            for ws in self.rooms[room].copy():
                try:
                    await ws.send_text(message)
                except WebSocketDisconnect:
                    self.rooms[room].discard(ws)


chat = ChatRoom()


@app.websocket("/ws/chat/{room}")
async def chat_websocket(websocket: WebSocket, room: str) -> None:
    await websocket.accept()
    await chat.join(room, websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            await chat.broadcast(room, msg)
    except WebSocketDisconnect:
        await chat.leave(room, websocket)


@app.websocket("/ws/echo")
async def echo_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"回声: {data}")
    except WebSocketDisconnect:
        print("客户端断开连接")
