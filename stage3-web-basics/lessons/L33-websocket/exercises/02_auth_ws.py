"""

from __future__ import annotations

练习 2: 带鉴权的 WebSocket 端点

使用 L33 的 JWT 验证函数，创建一个需要 token 的 WebSocket 端点：

@app.websocket("/ws/protected")
async def protected_ws(websocket: WebSocket, token: str = Query(...)):
    ...

要求:
1. 从 query string 获取 token 参数
2. 使用 verify_jwt(token) 验证（参考 L33 实现）
3. 验证失败时返回 4001 错误
4. 验证成功后再 accept()
"""
