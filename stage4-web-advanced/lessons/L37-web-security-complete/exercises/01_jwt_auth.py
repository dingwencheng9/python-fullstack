"""

from __future__ import annotations

练习 1: JWT 认证系统实现

任务：
实现一个完整的基于 JWT 的用户认证系统。

学习目标：
- 理解 JWT 令牌的生成和验证
- 掌握密码加密存储
- 实现用户登录和注册流程
- 使用 FastAPI 依赖注入保护路由

预计时间: 60 分钟
难度: ⭐⭐⭐☆☆
"""

import os
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# ============================================================================
# TODO 1: 配置 JWT 和密码加密
# ============================================================================

# ⚠️ 生产环境必须从环境变量读取密钥
# 演示时使用 secrets.token_hex() 动态生成（仅内存有效，重启丢失）
import secrets

SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# TODO: 创建密码加密上下文（使用 bcrypt）
# pwd_context = CryptContext(...)


# TODO: 创建 OAuth2 密码验证scheme
# oauth2_scheme = OAuth2PasswordBearer(...)


# ============================================================================
# TODO 2: 定义数据模型
# ============================================================================

# TODO: 创建 User 模型
# class User(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None
#     disabled: bool = False


# TODO: 创建 UserInDB 模型（包含哈希密码）
# class UserInDB(User):
#     hashed_password: str


# TODO: 创建 Token 模型
# class Token(BaseModel):
#     access_token: str
#     token_type: str


# ============================================================================
# TODO 3: 模拟用户数据库
# ============================================================================

# TODO: 创建模拟用户数据库（字典）
# fake_users_db: dict[str, UserInDB] = {
#     "alice": UserInDB(...),
#     "bob": UserInDB(...),
# }


# ============================================================================
# TODO 4: 实现密码处理函数
# ============================================================================


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    # TODO: 使用 pwd_context 验证密码


def get_password_hash(password: str) -> str:
    """哈希密码"""
    # TODO: 使用 pwd_context 哈希密码


# ============================================================================
# TODO 5: 实现 JWT 令牌函数
# ============================================================================


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """创建访问令牌"""
    # TODO: 实现 JWT 令牌生成
    # 1. 复制 data
    # 2. 设置过期时间
    # 3. 使用 jwt.encode 生成令牌


# ============================================================================
# TODO 6: 实现用户验证函数
# ============================================================================


def get_user(username: str) -> UserInDB | None:
    """从数据库获取用户"""
    # TODO: 从 fake_users_db 获取用户


def authenticate_user(username: str, password: str) -> UserInDB | None:
    """验证用户凭据"""
    # TODO:
    # 1. 获取用户
    # 2. 验证密码
    # 3. 返回用户或 None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """获取当前用户（依赖注入）"""
    HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # TODO:
    # 1. 解码 JWT 令牌
    # 2. 提取 username
    # 3. 获取用户
    # 4. 返回用户或抛出异常


# ============================================================================
# TODO 7: 创建 FastAPI 应用和路由
# ============================================================================

app = FastAPI(title="JWT 认证练习")


@app.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """用户登录"""
    # TODO:
    # 1. 验证用户凭据
    # 2. 创建访问令牌
    # 3. 返回令牌


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """获取当前用户信息（需要认证）"""
    # TODO: 返回当前用户


@app.get("/")
async def root() -> dict:
    """公开端点（无需认证）"""
    return {"message": "JWT 认证系统", "docs": "/docs"}


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 1: JWT 认证系统")
    print("=" * 70)
    print("\n任务：")
    print("  1. 配置 JWT 和密码加密")
    print("  2. 定义数据模型（User, UserInDB, Token）")
    print("  3. 实现密码处理函数")
    print("  4. 实现 JWT 令牌函数")
    print("  5. 实现用户验证函数")
    print("  6. 实现登录和获取用户信息端点")
    print("\n测试方法：")
    print("  1. 启动服务: uvicorn exercises.01_jwt_auth:app --reload")
    print("  2. 访问文档: http://localhost:8000/docs")
    print("  3. 测试登录: POST /token (username=alice, password=secret123)")
    print("  4. 测试获取用户: GET /users/me (需要 Bearer token)")
    print("\n提示：")
    print("  - 使用 python-jose 处理 JWT")
    print("  - 使用 passlib[bcrypt] 加密密码")
    print("  - 依赖注入保护需要认证的路由")
    print()
