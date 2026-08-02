"""Exercise 1: JWT Authentication"""

import jwt
from datetime import UTC
import secrets

SECRET_KEY = secrets.token_hex(32)


def create_token(user_id: str) -> str:
    """Create JWT token"""
    payload = {"sub": user_id, "exp": datetime.datetime.now(UTC) + datetime.timedelta(minutes=30)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None


def test():
    token = create_token("user123")
    payload = verify_token(token)
    assert payload["sub"] == "user123"
    print("PASS: JWT auth works")


if __name__ == "__main__":
    test()
