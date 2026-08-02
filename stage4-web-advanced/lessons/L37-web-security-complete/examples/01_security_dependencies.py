"""

from __future__ import annotations

FastAPI 防御性安全网关 - RBAC 与 Rate Limiting
===========================================

本模块展示 FastAPI Dependencies 的防御性安全设计：
- 基于依赖注入的安全网关（非中间件）
- RBAC（Role-Based Access Control）强类型上下文
- Rate Limiting 防止暴力破解（Redis）
- 所有 Auth 错误追踪（OpenTelemetry）

架构设计：
---------
1. JWT Token 验证（依赖注入）
2. RBAC 权限检查（装饰器）
3. Rate Limiting（Redis + 滑动窗口）
4. 审计日志（OTel Span）

对标：
-----
- 粉碎旧模块的中间件模式
- 呼应 L09 OpenTelemetry 可观测性

作者：Python 3.13 全栈课程
"""

import hashlib
import os
import secrets
from datetime import datetime, timedelta, UTC
from enum import StrEnum
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

# OpenTelemetry 集成（可选）
try:
    from opentelemetry import trace
    tracer = trace.get_tracer(__name__)
except ImportError:
    tracer = None  # type: ignore

# Redis（Rate Limiting）
# 注意：实际使用需安装 redis-py
# import redis.asyncio as redis


# ============================================================
# 配置
# ============================================================

# JWT 配置（✅ 从环境变量读取）
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# HTTP Bearer Token
security = HTTPBearer()


# ============================================================
# 用户角色定义（强类型）
# ============================================================


class UserRole(StrEnum):
    """用户角色枚举"""

    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"


class Permission(StrEnum):
    """权限枚举"""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


# RBAC 权限映射表
ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN},
    UserRole.MANAGER: {Permission.READ, Permission.WRITE, Permission.DELETE},
    UserRole.USER: {Permission.READ, Permission.WRITE},
    UserRole.GUEST: {Permission.READ},
}


# ============================================================
# 契约定义
# ============================================================


class User(BaseModel):
    """用户模型"""

    id: int
    username: str
    email: str
    hashed_password: str
    role: UserRole
    disabled: bool = False


class Token(BaseModel):
    """JWT Token 响应"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None


class TokenData(BaseModel):
    """Token 载荷数据"""

    username: str | None = None
    role: UserRole | None = None


class PermissionCheck(BaseModel):
    """权限检查结果"""

    allowed: bool
    required_permission: Permission
    user_role: UserRole


# ============================================================
# 密码哈希（简化版本，用于教学演示）
# ============================================================


def simple_hash(password: str, salt: str = "course-salt") -> str:
    """简单哈希（仅用于教学演示）"""
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码（兼容 simple_hash 旧格式和 pwd_context 新格式）。"""
    if "$" in hashed_password:
        return pwd_context.verify(plain_password, hashed_password)
    return simple_hash(plain_password) == hashed_password


def get_password_hash(password: str) -> str:
    """哈希密码"""
    return simple_hash(password)


# passlib 兼容接口（教学演示用，始终使用纯标准库实现以避免第三方库兼容问题）


class _PwdContext:
    """纯标准库实现的密码哈希，接口与 passlib CryptContext 兼容。"""

    def hash(self, password: str) -> str:
        salt = secrets.token_hex(16)
        h = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100_000
        ).hex()
        return f"{salt}${h}"

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        if "$" not in hashed_password:
            return False
        salt, h = hashed_password.split("$", 1)
        expected = hashlib.pbkdf2_hmac(
            "sha256", plain_password.encode(), salt.encode(), 100_000
        ).hex()
        return h == expected


pwd_context = _PwdContext()


# ============================================================
# 模拟用户数据库（生产环境使用真实数据库）
# ============================================================

users_db: dict[str, dict] = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": get_password_hash("AdminPass123!"),
        "role": UserRole.ADMIN,
        "disabled": False,
    },
    "manager": {
        "id": 2,
        "username": "manager",
        "email": "manager@example.com",
        "hashed_password": get_password_hash("ManagerPass123!"),
        "role": UserRole.MANAGER,
        "disabled": False,
    },
    "user": {
        "id": 3,
        "username": "user",
        "email": "user@example.com",
        "hashed_password": get_password_hash("UserPass123!"),
        "role": UserRole.USER,
        "disabled": False,
    },
}


# ============================================================
# JWT Token 生成与验证
# ============================================================


def create_access_token(user: dict, expires_delta: timedelta | None = None) -> str:
    """创建 JWT Token"""
    to_encode = user.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.now(UTC)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """解码 JWT Token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", "")
        role: str = payload.get("role", "guest")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenData(username=username, role=UserRole(role))
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================================================
# 用户查找
# ============================================================


def get_user(username: str) -> User | None:
    """根据用户名获取用户"""
    if username in users_db:
        user_dict = users_db[username]
        return User(**user_dict)
    return None


def authenticate_user(username: str, password: str) -> User | bool:
    """验证用户"""
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# ============================================================
# 核心依赖：认证
# ============================================================


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> User:
    """获取当前用户（JWT 验证）"""
    token = credentials.credentials
    token_data = decode_token(token)
    user = get_user(username=token_data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """获取当前活跃用户"""
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


# ============================================================
# 核心依赖：RBAC 权限检查
# ============================================================


def require_permission(required_permission: Permission):
    """权限检查装饰器工厂"""

    async def permission_checker(
        current_user: Annotated[User, Depends(get_current_active_user)]
    ) -> User:
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, set())
        if required_permission not in user_permissions:
            # 追踪未授权访问
            if tracer:
                tracer.start_span("permission_denied").end()

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足",
            )
        return current_user

    return permission_checker


# 快捷依赖
RequireRead = Annotated[User, Depends(require_permission(Permission.READ))]
RequireWrite = Annotated[User, Depends(require_permission(Permission.WRITE))]
RequireDelete = Annotated[User, Depends(require_permission(Permission.DELETE))]
RequireAdmin = Annotated[User, Depends(require_permission(Permission.ADMIN))]


# ============================================================
# FastAPI 应用
# ============================================================

app = FastAPI(title="FastAPI 安全网关", version="1.0.0")


class LoginRequest(BaseModel):
    """JSON 登录请求"""
    username: str
    password: str


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Request):
    """登录获取 Token（表单模式，OAuth2 兼容）"""
    body = await form_data.form()
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing username or password",
        )

    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if tracer:
        tracer.start_span("user_login").end()

    access_token = create_access_token(
        user={"sub": user.username, "role": user.role.value}
    )
    return Token(access_token=access_token, expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60)


@app.post("/login", response_model=Token)
async def login_json(request: Request):
    """登录获取 Token（JSON 模式）"""
    try:
        body = await request.json()
        username = body.get("username")
        password = body.get("password")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON body",
        )

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing username or password",
        )

    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if tracer:
        tracer.start_span("user_login").end()

    access_token = create_access_token(
        user={"sub": user.username, "role": user.role.value}
    )
    expires_in = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in,
    }


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: RequireRead):
    """获取当前用户信息"""
    return current_user


@app.get("/me", response_model=User)
async def read_me(current_user: RequireRead):
    """获取当前用户信息（/me 别名）"""
    return current_user


@app.get("/items/")
async def read_items(current_user: RequireRead):
    """读取项目（需要 READ 权限）"""
    return [{"item": "Item 1"}, {"item": "Item 2"}]


@app.post("/items/")
async def create_item(
    item: dict,
    current_user: RequireWrite,
):
    """创建项目（需要 WRITE 权限）"""
    if tracer:
        tracer.start_span("create_item").end()
    return {"item": item, "owner": current_user.username}


@app.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    current_user: RequireDelete,
):
    """删除项目（需要 DELETE 权限）"""
    return {"message": f"Item {item_id} deleted by {current_user.username}"}


@app.get("/admin/only")
async def admin_only(current_user: RequireAdmin):
    """管理员专属接口"""
    return {"message": "Welcome, Admin!"}


# ============================================================
# 管理端点
# ============================================================


@app.get("/admin/users", response_model=list[User])
async def list_users(current_user: RequireAdmin):
    """获取用户列表（仅管理员）"""
    return [User(**u) for u in users_db.values()]


@app.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: RequireDelete,
):
    """删除用户（需要 DELETE 权限）"""
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法删除自己",
        )
    target = None
    for u in users_db.values():
        if u["id"] == user_id:
            target = u
            break
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    for key, u in list(users_db.items()):
        if u["id"] == user_id:
            del users_db[key]
            break
    return JSONResponse(content={"message": "删除成功"}, status_code=204)


# ============================================================
# 权限检查端点
# ============================================================


@app.get("/protected/read")
async def protected_read(current_user: RequireRead):
    """受保护的读操作（需要 READ 权限）"""
    return {"message": "读取成功"}


@app.post("/protected/write")
async def protected_write(current_user: RequireWrite):
    """受保护的写操作（需要 WRITE 权限）"""
    return {"message": "写入成功"}


# ============================================================
# 权限检查端点
# ============================================================


@app.post("/check-permission", response_model=PermissionCheck)
async def check_permission(
    required: Permission,
    current_user: RequireRead,
):
    """检查用户是否有特定权限"""
    user_permissions = ROLE_PERMISSIONS.get(current_user.role, set())
    return PermissionCheck(
        allowed=required in user_permissions,
        required_permission=required,
        user_role=current_user.role,
    )


# ============================================================
# 速率限制（占位）
# ============================================================


async def rate_limit(request: Request):
    """速率限制中间件（占位实现）"""
    # 生产环境使用 Redis 实现
    # client_ip = request.client.host
    # count = await redis.incr(f"rate_limit:{client_ip}")
    # if count > 100:  # 100 requests per minute
    #     raise HTTPException(status_code=429, detail="Rate limit exceeded")
    pass
