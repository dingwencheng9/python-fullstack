"""L33 练习 2: 带鉴权的 WebSocket 端点 — 参考答案"""

from __future__ import annotations

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect

app = FastAPI()


def verify_jwt(token: str) -> bool:
    """JWT 验证（简化版，完整实现见 L33）"""
    return token == "valid_token" or token.startswith("ey")  # JWT 开头


@app.websocket("/ws/protected")
async def protected_ws(websocket: WebSocket, token: str = Query(...)):
    if not token or not verify_jwt(token):
        await websocket.close(code=4001, reason="鉴权失败")
        return
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"安全回声: {data}")
    except WebSocketDisconnect:
        pass
