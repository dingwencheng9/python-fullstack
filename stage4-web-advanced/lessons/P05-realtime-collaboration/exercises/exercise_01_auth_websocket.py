"""P05 练习 1: 认证与 WebSocket 整合"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

# ============ 数据模型 ============

class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

@dataclass
class User:
    id: int
    email: str
    username: str
    role: UserRole
    hashed_password: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "role": self.role.value,
        }

# ============ JWT 实现 ============

import base64
import hashlib
import hmac
import json
import time

class JWTToken:
    """简化的 JWT 实现 - 实际使用 python-jose"""

    def __init__(self, secret_key: str = "your-secret-key"):
        self.secret = secret_key

    def encode(self, payload: dict, expires_in: int = 3600) -> str:
        """创建 JWT token"""
        header = {"alg": "HS256", "typ": "JWT"}

        payload["exp"] = time.time() + expires_in
        payload["iat"] = time.time()

        # Base64URL 编码
        def b64encode(data: dict) -> str:
            json_str = json.dumps(data, separators=(",", ":"))
            return base64.urlsafe_b64encode(json_str.encode()).rstrip(b"=").decode()

        header_b64 = b64encode(header)
        payload_b64 = b64encode(payload)
        signature = hmac.new(
            self.secret.encode(),
            f"{header_b64}.{payload_b64}".encode(),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b"=").decode()

        return f"{header_b64}.{payload_b64}.{signature_b64}"

    def decode(self, token: str) -> Optional[dict]:
        """验证并解析 JWT token"""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None

            header_b64, payload_b64, signature_b64 = parts

            # 验证签名
            expected_signature = hmac.new(
                self.secret.encode(),
                f"{header_b64}.{payload_b64}".encode(),
                hashlib.sha256
            ).digest()
            expected_b64 = base64.urlsafe_b64encode(expected_signature).rstrip(b"=").decode()

            if not hmac.compare_digest(signature_b64, expected_b64):
                return None

            # 解析 payload
            payload_str = base64.urlsafe_b64decode(payload_b64 + "==")
            payload = json.loads(payload_str)

            # 检查过期
            if payload.get("exp", 0) < time.time():
                return None

            return payload
        except Exception:
            return None

jwt_token = JWTToken()

# ============ WebSocket 连接管理 ============

@dataclass
class WebSocketMessage:
    type: str
    data: dict = field(default_factory=dict)

class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        # user_id -> WebSocket
        self.connections: dict[int, list[asyncio.Queue]] = {}

    def subscribe(self, user_id: int, queue: asyncio.Queue):
        """订阅用户消息"""
        if user_id not in self.connections:
            self.connections[user_id] = []
        self.connections[user_id].append(queue)

    def unsubscribe(self, user_id: int, queue: asyncio.Queue):
        """取消订阅"""
        if user_id in self.connections:
            try:
                self.connections[user_id].remove(queue)
                if not self.connections[user_id]:
                    del self.connections[user_id]
            except ValueError:
                pass

    async def broadcast_to_user(self, user_id: int, message: dict):
        """向用户广播消息"""
        if user_id in self.connections:
            for queue in self.connections[user_id]:
                await queue.put(message)

manager = ConnectionManager()

# ============ 练习题目 ============

def exercise_01_create_token():
    """练习 1: 创建 JWT Token"""
    # TODO: 使用 JWTToken 创建一个包含 user_id 和 role 的 token
    # token 应该包含: {"sub": user_id, "role": role.value}
    # 过期时间: 30 分钟

    user = User(
        id=1,
        email="alice@example.com",
        username="alice",
        role=UserRole.MEMBER,
        hashed_password="xxx"
    )

    # 你的代码:
    # token = ...
    # assert token is not None
    # assert "." in token

    print("练习 1: 创建 JWT Token")
    print("- 实现 create_token(user) 函数")
    print("- 返回包含 user_id 和 role 的 token")


def exercise_02_verify_token():
    """练习 2: 验证 JWT Token"""
    # TODO: 验证 token 并返回 payload
    # 如果 token 无效或过期，返回 None

    valid_token = jwt_token.encode({"sub": 1, "role": "member"})
    invalid_token = "invalid.token.here"

    # 你的代码:
    # payload = jwt_token.decode(valid_token)
    # assert payload is not None
    # assert payload["sub"] == 1

    print("练习 2: 验证 JWT Token")
    print("- 实现 verify_token(token) 函数")
    print("- 返回 payload 或 None")


def exercise_03_websocket_subscription():
    """练习 3: WebSocket 订阅管理"""
    # TODO: 实现用户订阅和消息广播

    async def test_subscription():
        user_id = 1
        queue = asyncio.Queue()

        # 订阅
        # manager.subscribe(user_id, queue)

        # 发送消息
        # await manager.broadcast_to_user(user_id, {"type": "message", "content": "hello"})

        # 接收消息
        # msg = await asyncio.wait_for(queue.get(), timeout=1)
        # assert msg["content"] == "hello"

        print("练习 3: WebSocket 订阅管理")
        print("- 实现 subscribe(user_id, queue)")
        print("- 实现 broadcast_to_user(user_id, message)")

    asyncio.run(test_subscription())


def exercise_04_authenticated_websocket():
    """练习 4: 带认证的 WebSocket"""
    # TODO: 实现带 JWT 认证的 WebSocket 连接

    async def test_auth_flow():
        # 1. 用户登录获取 token
        token = jwt_token.encode({"sub": 1, "role": "member"})

        # 2. WebSocket 连接时验证 token
        def verify_ws_token(token: str) -> Optional[dict]:
            # 你的代码:
            # return jwt_token.decode(token)
            pass

        payload = verify_ws_token(token)
        # assert payload is not None
        # assert payload["sub"] == 1

        print("练习 4: 带认证的 WebSocket")
        print("- 实现 verify_ws_token(token) 函数")
        print("- 连接时验证 token 并返回用户信息")

    asyncio.run(test_auth_flow())


def exercise_05_permission_check():
    """练习 5: 权限检查"""
    # TODO: 实现基于角色的权限检查

    def check_permission(user_role: UserRole, required_role: UserRole) -> bool:
        # 权限等级: ADMIN > MEMBER > VIEWER
        # ADMIN 可以做任何事
        # MEMBER 可以做 MEMBER 和 VIEWER 的事
        # VIEWER 只能做 VIEWER 的事

        # 你的代码:
        # if user_role == UserRole.ADMIN:
        #     return True
        # return user_role == required_role
        pass

    print("练习 5: 权限检查")
    print("- 实现 check_permission(user_role, required_role)")
    print("- 返回 True 或 False")


# ============ 运行测试 ============

if __name__ == "__main__":
    print("=" * 60)
    print("P05 练习 1: 认证与 WebSocket 整合")
    print("=" * 60)

    exercise_01_create_token()
    print()

    exercise_02_verify_token()
    print()

    exercise_03_websocket_subscription()
    print()

    exercise_04_authenticated_websocket()
    print()

    exercise_05_permission_check()
    print()

    print("=" * 60)
    print("所有练习完成！")
    print("=" * 60)
