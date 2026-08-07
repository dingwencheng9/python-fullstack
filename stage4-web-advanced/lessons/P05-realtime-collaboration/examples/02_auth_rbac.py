"""P05 示例 2: JWT 认证与 RBAC"""

from __future__ import annotations

import time
import hashlib
import hmac
import base64
import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional

# ============ 用户角色 ============

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    VIEWER = "viewer"

# 权限等级 (数字越大权限越高)
ROLE_LEVELS = {
    UserRole.VIEWER: 1,
    UserRole.MEMBER: 2,
    UserRole.MANAGER: 3,
    UserRole.ADMIN: 4,
}

# ============ JWT 实现 ============

class JWTToken:
    """简化的 JWT 实现 - 参考 L38"""

    def __init__(self, secret_key: str = "taskcollab-secret-key"):
        self.secret = secret_key

    def encode(self, payload: dict, expires_in: int = 1800) -> str:
        """创建 JWT token"""
        header = {"alg": "HS256", "typ": "JWT"}
        payload["exp"] = time.time() + expires_in
        payload["iat"] = time.time()

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
            expected_sig = hmac.new(
                self.secret.encode(),
                f"{header_b64}.{payload_b64}".encode(),
                hashlib.sha256
            ).digest()
            expected_b64 = base64.urlsafe_b64encode(expected_sig).rstrip(b"=").decode()

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


# ============ 密码哈希 ============

class PasswordHasher:
    """简化的密码哈希 - 实际使用 bcrypt"""

    def hash(self, password: str) -> str:
        """哈希密码"""
        # 实际应使用 bcrypt
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return self.hash(plain_password) == hashed_password


# ============ 权限检查 ============

class PermissionChecker:
    """权限检查 - 参考 L37 RBAC"""

    @staticmethod
    def can_access(user_role: UserRole, required_role: UserRole) -> bool:
        """检查用户是否有权限访问"""
        if user_role == UserRole.ADMIN:
            return True
        return user_role == required_role

    @staticmethod
    def has_minimum_role(user_role: UserRole, minimum_role: UserRole) -> bool:
        """检查用户是否有最低角色权限"""
        return ROLE_LEVELS.get(user_role, 0) >= ROLE_LEVELS.get(minimum_role, 0)

    @staticmethod
    def get_allowed_actions(role: UserRole) -> list[str]:
        """获取角色允许的操作"""
        base_actions = ["read"]
        if role in [UserRole.MEMBER, UserRole.MANAGER, UserRole.ADMIN]:
            base_actions.extend(["create", "update"])
        if role in [UserRole.MANAGER, UserRole.ADMIN]:
            base_actions.extend(["delete", "manage_team"])
        if role == UserRole.ADMIN:
            base_actions.extend(["admin", "system_config"])
        return base_actions


# ============ 演示 ============

def demonstrate_auth():
    """演示认证授权"""
    print("=" * 60)
    print("JWT 认证与 RBAC 权限模型")
    print("=" * 60)

    jwt = JWTToken()
    hasher = PasswordHasher()
    checker = PermissionChecker()

    # 1. 创建用户并哈希密码
    print("\n1️⃣ 用户认证")
    user = {
        "id": 1,
        "email": "alice@example.com",
        "username": "alice",
        "role": UserRole.MEMBER.value,
    }
    hashed_password = hasher.hash("secure_password_123")
    print(f"  用户: {user['email']}")
    print(f"  密码哈希: {hashed_password[:20]}...")

    # 2. 验证密码
    assert hasher.verify("secure_password_123", hashed_password)
    print("  ✓ 密码验证成功")

    # 3. 创建 JWT Token
    print("\n2️⃣ JWT Token")
    token_payload = {
        "sub": user["id"],
        "email": user["email"],
        "role": user["role"],
    }
    token = jwt.encode(token_payload, expires_in=1800)
    print(f"  Token: {token[:50]}...")
    print(f"  有效期: 30 分钟")

    # 4. 解析 Token
    decoded = jwt.decode(token)
    print(f"  ✓ 解析成功: 用户 {decoded['sub']}, 角色 {decoded['role']}")

    # 5. 权限检查
    print("\n3️⃣ RBAC 权限检查")
    for role in [UserRole.VIEWER, UserRole.MEMBER, UserRole.MANAGER, UserRole.ADMIN]:
        actions = checker.get_allowed_actions(role)
        print(f"  {role.value:10}: {', '.join(actions)}")

    # 6. 权限验证示例
    print("\n4️⃣ 权限验证")
    scenarios = [
        (UserRole.MEMBER, UserRole.MEMBER, True, "成员可以更新自己的任务"),
        (UserRole.VIEWER, UserRole.MEMBER, False, "查看者不能更新任务"),
        (UserRole.ADMIN, UserRole.ADMIN, True, "管理员可以做任何事"),
        (UserRole.MANAGER, UserRole.VIEWER, True, "经理可以查看任务"),
    ]
    for user_role, required, expected, desc in scenarios:
        result = checker.can_access(user_role, required)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {user_role.value} -> {required.value}: {result} ({desc})")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_auth()
