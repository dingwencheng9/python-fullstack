"""L37 示例：密码哈希。"""

from __future__ import annotations

import hashlib
import secrets


def hash_password(password: str) -> tuple[str, str]:
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return salt, hashed.hex()


def verify_password(password: str, salt: str, hashed: str) -> bool:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex() == hashed


if __name__ == "__main__":
    s, h = hash_password("hello")
    print("OK" if verify_password("hello", s, h) else "FAIL")
