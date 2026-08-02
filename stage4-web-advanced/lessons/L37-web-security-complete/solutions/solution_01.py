"""

from __future__ import annotations

练习 1: JWT 认证系统实现 - Python 3.13 参考答案

本解决方案展示：
1. Python 3.13 PEP 695 泛型语法
2. match/case 模式匹配
3. asyncio.TaskGroup 并发验证
4. Free-threading 线程安全设计

【解题思路】

1. JWT 认证流程：
   - 用户提交用户名和密码
   - 服务器验证凭据
   - 生成 JWT 令牌（包含用户信息和过期时间）
   - 客户端在后续请求中携带令牌
   - 服务器验证令牌并提取用户信息

2. 密码安全：
   - 使用 bcrypt 算法哈希密码
   - 永远不存储明文密码
   - 使用 passlib 提供的安全上下文

3. 依赖注入模式：
   - OAuth2PasswordBearer 自动提取令牌
   - get_current_user 依赖验证令牌
   - 保护端点只需添加 Depends(get_current_user)

4. 错误处理：
   - 认证失败返回 401 状态码
   - 设置 WWW-Authenticate 头
   - 提供清晰的错误信息

【关键知识点】

- JWT 令牌结构（Header.Payload.Signature）
- OAuth2 密码流程
- bcrypt 密码哈希
- FastAPI 依赖注入系统
- 异常处理和 HTTP 状态码
- Python 3.13 PEP 695 泛型语法
- match/case 模式匹配
- asyncio.TaskGroup 并发处理

作者：Python 3.13 全栈课程
"""

import asyncio
import os
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

# ============================================================================
# 1. 配置 JWT 和密码加密
# ============================================================================

# ✅ 从环境变量读取密钥（生产环境必须设置）
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 密码验证scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ============================================================================
# 2. 定义数据模型
# ============================================================================


class User(BaseModel):
    """用户模型"""

    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False


class UserInDB(User):
    """数据库中的用户模型（包含哈希密码）"""

    hashed_password: str


class Token(BaseModel):
    """令牌模型"""

    access_token: str
    token_type: str


# ============================================================================
# 3. 模拟用户数据库（Free-threading 线程安全说明）
# ============================================================================

# 🔒 Free-threading 线程安全说明:
# - 这是一个只读字典，初始化后不修改
# - Python 3.14 环境下读操作是线程安全的
# - 如果需要写操作，应使用 asyncio.Lock 或 threading.Lock
fake_users_db: dict[str, UserInDB] = {
    "alice": UserInDB(
        username="alice",
        email="alice@example.com",
        full_name="Alice Wonderland",
        disabled=False,
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    ),
    "bob": UserInDB(
        username="bob",
        email="bob@example.com",
        full_name="Bob Builder",
        disabled=False,
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    ),
}


# ============================================================================
# 4. 泛型 Token 管理器（Python 3.13 PEP 695 泛型）
# ============================================================================


class TokenManager[T]:
    """
    泛型 Token 管理器（Python 3.13 PEP 695 泛型语法）

    🚀 Python 3.13 PEP 695 特性:
    - 使用 class TokenManager[T]: 定义泛型类
    - 相比旧语法 Generic[T] 更简洁直观
    - 类型推断更准确

    泛型参数:
        T: Token payload 的数据类型
    """

    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, data: T, expires_delta: timedelta | None = None) -> str:
        """
        创建 JWT Token

        Args:
            data: Token payload 数据
            expires_delta: 过期时间增量

        Returns:
            编码后的 JWT Token
        """
        # 将 payload 转换为字典
        if isinstance(data, dict):
            to_encode = data.copy()
        else:
            # 假设是 Pydantic model 或 dataclass
            to_encode = data.model_dump() if hasattr(data, "model_dump") else data.__dict__

        # 设置过期时间（使用 UTC 时区）
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict[str, Any] | None:
        """
        解码 JWT Token（使用 match/case 错误处理）

        🎯 Python 3.10+ match/case 模式匹配

        Args:
            token: JWT Token 字符串

        Returns:
            解码后的 payload，失败返回 None
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            # 使用 match/case 处理不同的 JWT 错误
            error_type = type(e).__name__

            match error_type:
                case "ExpiredSignatureError":
                    print(f"Token 已过期: {e}")
                    return None
                case "JWTClaimsError":
                    print(f"Token claims 错误: {e}")
                    return None
                case "InvalidTokenError":
                    print(f"Token 无效: {e}")
                    return None
                case _:
                    print(f"未知 JWT 错误: {e}")
                    return None


# 创建全局 Token 管理器
token_manager: TokenManager[dict[str, Any]] = TokenManager(SECRET_KEY, ALGORITHM)


# ============================================================================
# 5. 实现密码处理函数
# ============================================================================


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)


# ============================================================================
# 6. 实现用户验证函数（使用 match/case）
# ============================================================================


def get_user(username: str) -> UserInDB | None:
    """从数据库获取用户"""
    if username in fake_users_db:
        return fake_users_db[username]
    return None


def authenticate_user(username: str, password: str) -> UserInDB | None:
    """
    验证用户凭据（使用 match/case 处理验证结果）

    🎯 Python 3.10+ match/case 模式匹配
    """
    user = get_user(username)

    # 使用 match/case 处理用户查询结果
    match user:
        case None:
            # 用户不存在
            return None
        case UserInDB() if user.disabled:
            # 用户已禁用
            return None
        case UserInDB():
            # 验证密码
            if verify_password(password, user.hashed_password):
                return user
            return None
        case _:
            # 未知情况
            return None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    获取当前用户（依赖注入，使用 match/case 处理 Token 验证）

    🎯 使用 match/case 优雅处理 Token 验证结果
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 解码 Token
    payload = token_manager.decode_token(token)

    # 使用 match/case 处理解码结果
    match payload:
        case None:
            # Token 无效
            raise credentials_exception
        case {"sub": str(username)} if username:
            # Token 有效且包含用户名
            user = get_user(username)
            if user is None:
                raise credentials_exception
            return user
        case _:
            # Payload 格式错误
            raise credentials_exception


# ============================================================================
# 7. 批量验证 Token（使用 asyncio.TaskGroup）
# ============================================================================


async def verify_tokens_batch(tokens: list[str]) -> list[User | None]:
    """
    批量验证 Token（使用 asyncio.TaskGroup 并发）

    🚀 Python 3.13 asyncio.TaskGroup:
    - 结构化并发，自动等待所有任务完成
    - 异常安全，任何任务失败会取消其他任务
    - 相比手动 gather，代码更清晰

    Args:
        tokens: Token 列表

    Returns:
        验证结果列表（User 或 None）
    """
    results: list[User | None] = []

    async def verify_single(token: str) -> User | None:
        """验证单个 Token"""
        try:
            return await get_current_user(token)
        except HTTPException:
            return None

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(verify_single(token)) for token in tokens]

    # 收集结果
    for task in tasks:
        results.append(task.result())

    return results


# ============================================================================
# 8. 创建 FastAPI 应用和路由
# ============================================================================

app = FastAPI(title="JWT 认证练习 - Python 3.13")


@app.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """用户登录"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token_manager.create_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """获取当前用户信息（需要认证）"""
    return current_user


@app.post("/users/verify-batch")
async def verify_batch(tokens: list[str]) -> dict[str, Any]:
    """
    批量验证 Token（使用 asyncio.TaskGroup 并发）

    🚀 展示 Python 3.13 TaskGroup 并发验证
    """
    users = await verify_tokens_batch(tokens)

    return {
        "total": len(tokens),
        "valid": sum(1 for u in users if u is not None),
        "invalid": sum(1 for u in users if u is None),
        "users": [u.username if u else None for u in users],
    }


@app.get("/")
async def root() -> dict[str, Any]:
    """公开端点（无需认证）"""
    return {
        "message": "JWT 认证系统 (Python 3.13)",
        "docs": "/docs",
        "features": [
            "PEP 695 泛型语法",
            "match/case 模式匹配",
            "asyncio.TaskGroup 并发",
            "Free-threading 线程安全",
        ],
    }


# ============================================================================
# 测试辅助函数
# ============================================================================


def print_test_credentials():
    """打印测试凭据"""
    print("\n测试凭据：")
    print("  用户名: alice")
    print("  密码: secret123")
    print("  用户名: bob")
    print("  密码: secret123")


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    from core.settings import get_settings

    settings = get_settings()
    import uvicorn

    print("=" * 70)
    print("练习 1 参考答案: JWT 认证系统 - Python 3.13")
    print("=" * 70)
    print("\n特性:")
    print("  ✅ PEP 695 泛型语法: class TokenManager[T]")
    print("  ✅ match/case: 优雅的错误处理")
    print("  ✅ asyncio.TaskGroup: 批量验证 Token")
    print("  ✅ Free-threading 线程安全设计")
    print_test_credentials()
    print("\n测试步骤：")
    print("  1. 访问 http://localhost:8000/docs")
    print("  2. 点击 /token 端点的 'Try it out'")
    print("  3. 输入用户名和密码")
    print("  4. 复制返回的 access_token")
    print("  5. 点击页面右上角的 'Authorize' 按钮")
    print("  6. 输入 token，点击 'Authorize'")
    print("  7. 测试 /users/me 端点")
    print("  8. 测试 /users/verify-batch 端点（批量验证）")
    print("\n启动服务...\n")

    uvicorn.run(
        app,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
    )
