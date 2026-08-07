"""

from __future__ import annotations

FastAPI 契约优先开发 - Pydantic V2 强类型契约
===============================================

本模块展示 FastAPI + Pydantic V2 的契约优先设计：
- 请求/响应强类型定义
- 自动 API 文档生成
- Rust 核心验证性能（Pydantic V2）
- 完整的类型注解（mypy --strict）

架构设计：
---------
1. 契约定义（Pydantic Models）
2. API 路由（FastAPI Router）
3. 业务逻辑（Service Layer）
4. 自动文档（OpenAPI/Swagger）

对标：
-----
- Pydantic V2 性能（5-50x V1）
- 呼应 L08 高性能抽象（__slots__ + 描述符）

作者：Python 3.13 全栈课程
"""

from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, ConfigDict, Field

# ============================================================
# 契约定义：请求/响应模型
# ============================================================


class UserBase(BaseModel):
    """用户基础模型（共享字段）"""

    model_config = ConfigDict(
        str_strip_whitespace=True,  # 自动去除首尾空格
        validate_default=True,  # 验证默认值
    )

    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            pattern=r"^[a-zA-Z0-9_-]+$",
            description="用户名（3-50 字符，仅字母数字下划线）",
            examples=["alice", "bob_123"],
        ),
    ]

    email: Annotated[
        str,
        Field(
            pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
            description="邮箱地址",
            examples=["alice@example.com"],
        ),
    ]

    full_name: Annotated[
        str | None,
        Field(
            default=None,
            max_length=100,
            description="真实姓名（可选）",
            examples=["Alice Smith"],
        ),
    ]


class UserCreate(UserBase):
    """用户创建请求契约"""

    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
            description="密码（至少 8 位）",
            examples=["SecurePass123!"],
        ),
    ]


class UserResponse(UserBase):
    """用户响应契约"""

    id: Annotated[
        int,
        Field(
            gt=0,
            description="用户 ID",
            examples=[1, 42],
        ),
    ]

    is_active: Annotated[
        bool,
        Field(
            description="是否激活",
            examples=[True],
        ),
    ] = True

    created_at: Annotated[
        datetime,
        Field(
            description="创建时间",
            examples=["2026-06-07T10:00:00Z"],
        ),
    ]


class UserUpdate(BaseModel):
    """用户更新请求契约（部分字段）"""

    model_config = ConfigDict(str_strip_whitespace=True)

    email: Annotated[
        str | None,
        Field(
            default=None,
            pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        ),
    ]

    full_name: Annotated[str | None, Field(default=None, max_length=100)]

    is_active: Annotated[bool | None, Field(default=None)]


class ErrorResponse(BaseModel):
    """错误响应契约"""

    error: Annotated[
        str,
        Field(description="错误类型", examples=["ValidationError"]),
    ]

    message: Annotated[
        str,
        Field(description="错误消息", examples=["用户名已存在"]),
    ]

    details: Annotated[
        dict[str, str] | None,
        Field(
            default=None,
            description="详细错误信息",
            examples=[{"field": "username", "issue": "already_exists"}],
        ),
    ]


# ============================================================
# 模拟数据库（内存存储）
# ============================================================

# 模拟数据库
users_db: dict[int, UserResponse] = {
    1: UserResponse(
        id=1,
        username="alice",
        email="alice@example.com",
        full_name="Alice Smith",
        is_active=True,
        created_at=datetime.now(),
    ),
    2: UserResponse(
        id=2,
        username="bob",
        email="bob@example.com",
        full_name=None,
        is_active=True,
        created_at=datetime.now(),
    ),
}

next_user_id = 3


# ============================================================
# FastAPI 应用与路由
# ============================================================

app = FastAPI(
    title="契约优先 API",
    description="FastAPI + Pydantic V2 契约驱动开发示例",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)


@app.get(
    "/",
    summary="API 根路径",
    description="返回 API 欢迎消息",
)
async def root() -> dict[str, str]:
    """根路径"""
    return {"message": "FastAPI 契约优先 API", "docs": "/docs"}


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="创建用户",
    description="创建新用户，返回用户信息",
    responses={
        201: {"description": "用户创建成功"},
        400: {"model": ErrorResponse, "description": "验证失败"},
        409: {"model": ErrorResponse, "description": "用户名已存在"},
    },
)
async def create_user(user: UserCreate) -> UserResponse:
    """
    创建新用户

    **契约验证**:
    - username: 3-50 字符，仅字母数字下划线
    - email: 有效邮箱格式
    - password: 至少 8 位

    **自动验证**: Pydantic V2 Rust 核心验证（5-50x 性能）
    """
    global next_user_id

    # 检查用户名是否已存在
    for existing_user in users_db.values():
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "ConflictError",
                    "message": f"用户名 '{user.username}' 已存在",
                    "details": {"field": "username", "issue": "already_exists"},
                },
            )

    # 创建用户
    new_user = UserResponse(
        id=next_user_id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=True,
        created_at=datetime.now(),
    )

    users_db[next_user_id] = new_user
    next_user_id += 1

    return new_user


@app.get(
    "/users",
    response_model=list[UserResponse],
    summary="获取用户列表",
    description="获取所有用户（支持分页）",
)
async def list_users(
    skip: Annotated[int, Query(ge=0, description="跳过记录数")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="返回记录数")] = 10,
    is_active: Annotated[bool | None, Query(description="过滤激活状态")] = None,
) -> list[UserResponse]:
    """
    获取用户列表

    **查询参数契约**:
    - skip: >= 0（分页偏移）
    - limit: 1-100（分页大小）
    - is_active: 可选，过滤激活状态
    """
    users = list(users_db.values())

    # 过滤
    if is_active is not None:
        users = [u for u in users if u.is_active == is_active]

    # 分页
    return users[skip : skip + limit]


@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="获取用户详情",
    description="根据 ID 获取用户信息",
    responses={
        200: {"description": "用户信息"},
        404: {"model": ErrorResponse, "description": "用户不存在"},
    },
)
async def get_user(user_id: Annotated[int, Path(gt=0, description="用户 ID")]) -> UserResponse:
    """
    获取用户详情

    **路径参数契约**:
    - user_id: > 0
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFoundError",
                "message": f"用户 ID {user_id} 不存在",
            },
        )

    return users_db[user_id]


@app.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="更新用户",
    description="部分更新用户信息",
    responses={
        200: {"description": "更新成功"},
        404: {"model": ErrorResponse, "description": "用户不存在"},
    },
)
async def update_user(
    user_id: Annotated[int, Path(gt=0, description="用户 ID")],
    update_data: UserUpdate,
) -> UserResponse:
    """
    更新用户信息

    **契约特性**:
    - 部分更新（PATCH）
    - 仅更新提供的字段
    - 自动验证更新数据
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFoundError",
                "message": f"用户 ID {user_id} 不存在",
            },
        )

    user = users_db[user_id]

    # 更新字段（仅更新非 None 的字段）
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(user, field, value)

    return user


@app.delete(
    "/users/{user_id}",
    status_code=204,
    summary="删除用户",
    description="删除指定用户",
    responses={
        204: {"description": "删除成功"},
        404: {"model": ErrorResponse, "description": "用户不存在"},
    },
)
async def delete_user(user_id: Annotated[int, Path(gt=0, description="用户 ID")]) -> None:
    """删除用户"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFoundError",
                "message": f"用户 ID {user_id} 不存在",
            },
        )

    del users_db[user_id]


# ============================================================
# 运行说明
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("FastAPI 契约优先 API")
    print("=" * 80)
    print("\n启动服务器...")
    print("  - API 文档: http://localhost:8000/docs")
    print("  - ReDoc:    http://localhost:8000/redoc")
    print("\n按 Ctrl+C 停止\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
