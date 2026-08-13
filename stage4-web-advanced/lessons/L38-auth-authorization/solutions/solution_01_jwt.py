"""Solution: JWT Authentication with RBAC"""

import jwt
import datetime
from datetime import UTC
import secrets

from dataclasses import dataclass
from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


@dataclass
class TokenPayload:
    sub: str  # user id
    roles: list[str]
    exp: datetime.datetime
    iat: datetime.datetime


class JWTAuth:
    def __init__(self, secret_key: str | None = None):
        self.secret = secret_key or secrets.token_hex(32)
        self.algorithm = "HS256"
        self.access_token_expire = 30  # minutes
        self.refresh_token_expire = 7 * 24 * 60  # 7 days

    def create_access_token(self, user_id: str, roles: list[str]) -> str:
        """Create JWT access token."""
        now = datetime.datetime.now(UTC)
        payload = {
            "sub": user_id,
            "roles": roles,
            "type": "access",
            "iat": now,
            "exp": now + datetime.timedelta(minutes=self.access_token_expire),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token."""
        now = datetime.datetime.now(UTC)
        payload = {
            "sub": user_id,
            "type": "refresh",
            "iat": now,
            "exp": now + datetime.timedelta(minutes=self.refresh_token_expire),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict[str, object] | None:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:  # jose.jwt 使用 JWTError 而非 InvalidTokenError
            return None

    def refresh_access_token(self, refresh_token: str) -> str | None:
        """Get new access token using refresh token."""
        payload = self.verify_token(refresh_token)
        if payload and payload.get("type") == "refresh":
            return self.create_access_token(payload["sub"], ["user"])
        return None


class RBAC:
    """Role-Based Access Control."""

    PERMISSIONS = {
        Role.ADMIN: ["read", "write", "delete", "admin"],
        Role.USER: ["read", "write"],
        Role.GUEST: ["read"],
    }

    @classmethod
    def has_permission(cls, roles: list[str], permission: str) -> bool:
        """Check if any role has the permission."""
        for role_name in roles:
            try:
                role = Role(role_name)
                if permission in cls.PERMISSIONS.get(role, []):
                    return True
            except ValueError:
                continue
        return False


if __name__ == "__main__":
    auth = JWTAuth()

    # Create tokens
    access = auth.create_access_token("user123", ["user"])
    refresh = auth.create_refresh_token("user123")

    # Verify
    payload = auth.verify_token(access)
    print(f"Verified: {payload}")

    # Refresh
    new_access = auth.refresh_access_token(refresh)
    print(f"New access token: {new_access[:50]}...")

    # RBAC test
    print(f"Has admin permission: {RBAC.has_permission(['user'], 'admin')}")
    print(f"Has read permission: {RBAC.has_permission(['user'], 'read')}")
