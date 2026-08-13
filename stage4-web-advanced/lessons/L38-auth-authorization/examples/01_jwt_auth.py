"""示例 1: JWT 认证实现"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from datetime import UTC, datetime, timedelta
import secrets

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    roles: list[str] = []


def create_token(user: User) -> str:
    """创建 JWT Token"""
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user.username, "roles": user.roles, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """验证 JWT Token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期")
    except jwt.JWTError:  # jose.jwt 使用 JWTError
        raise HTTPException(status_code=401, detail="无效的 Token")


@app.post("/login")
async def login(username: str, password: str) -> Token:
    """登录"""
    # 实际应该验证密码
    user = User(username=username, roles=["user"])
    token = create_token(user)
    return Token(access_token=token, token_type="bearer")


@app.get("/protected")
async def protected(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """受保护的接口"""
    payload = verify_token(credentials.credentials)
    return {"user": payload["sub"], "roles": payload["roles"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
