"""L33 WebSocket 客户端示例"""

from __future__ import annotations

import asyncio
import sys

import websockets


async def echo_client() -> None:
    """连接回声服务"""
    async with websockets.connect("ws://localhost:8000/ws/echo") as ws:
        await ws.send("Hello WebSocket!")
        response = await ws.recv()
        print(f"服务端回声: {response}")


async def chat_client(room: str = "general") -> None:
    """连接聊天室"""
    async with websockets.connect(f"ws://localhost:8000/ws/chat/{room}") as ws:
        print(f"已连接到聊天室 {room}，输入消息 (Ctrl+C 退出)")

        async def receive() -> None:
            async for msg in ws:
                print(f"\n[消息]: {msg}")

        async def send() -> None:
            loop = asyncio.get_event_loop()
            while True:
                msg = await loop.run_in_executor(None, sys.stdin.readline)
                if msg.strip():
                    await ws.send(msg.strip())

        await asyncio.gather(receive(), send())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "chat":
        asyncio.run(chat_client())
    else:
        asyncio.run(echo_client())
