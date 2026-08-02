"""

from __future__ import annotations

练习 1: 创建 RESTful API - 参考答案

【解题思路】
1. 数据模型设计：
   - UserCreate: 用于接收客户端数据（不含id）
   - UserResponse: 用于返回数据（含id）
   - 使用 Pydantic 的 Field 和 EmailStr 进行验证

2. CRUD 实现策略：
   - CREATE: 生成新ID，保存到字典，返回201
   - READ: 从字典查找，不存在抛出404
   - UPDATE: 先检查存在性，再更新，返回更新后的数据
   - DELETE: 先检查存在性，删除后返回204
   - LIST: 使用切片实现分页

3. HTTP 状态码：
   - 200: GET/PUT 成功
   - 201: POST 创建成功
   - 204: DELETE 成功（无内容）
   - 404: 资源不存在
   - 422: 数据验证失败（Pydantic自动处理）

4. 类型安全：
   - 使用 Annotated 和 Query 进行参数验证
   - 使用 response_model 确保返回类型一致

【关键知识点】
- FastAPI 路由装饰器的 response_model 和 status_code 参数
- Pydantic 的 Field、EmailStr 验证
- HTTPException 的使用
- 异步端点的定义（async def）
- 分页查询的实现（skip/limit）
"""

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="用户管理 API")


# ============================================================================
# PEP 695 泛型工具函数（Python 3.12+，课程基线 3.13）
# ============================================================================


def paginate[T](items: list[T], skip: int, limit: int) -> list[T]:
    """
    通用分页函数（PEP 695 泛型语法）

    使用 PEP 695 的 [T] 语法声明类型参数，替代旧式 TypeVar：
    - 旧式: T = TypeVar('T'); def paginate(items: list[T], ...) -> list[T]
    - 新式: def paginate[T](items: list[T], ...) -> list[T]

    优势：
    - 更简洁（无需单独声明 TypeVar）
    - 更清晰（类型参数直接在函数签名中）
    - 作用域更明确（T 只在函数内有效）

    线程安全考量（python3.13t / python3.14t free-threading 构建下）：
    - 纯函数，无共享状态，线程安全
    - 切片操作是原子的，返回新列表
    """
    return items[skip : skip + limit]


# ============================================================================
# 数据模型
# ============================================================================


class UserCreate(BaseModel):
    """创建用户模型"""

    name: str = Field(..., min_length=1, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    age: int = Field(..., ge=0, le=150, description="年龄")


class UserResponse(BaseModel):
    """用户响应模型"""

    id: int
    name: str
    email: str
    age: int


# ============================================================================
# 模拟数据库
# ============================================================================

# 线程安全考量（python3.13t / python3.14t free-threading 构建下）：
# users 和 next_id 是全局可变状态，在无 GIL (Free-Threading) 环境下不安全
# 问题：
# 1. 多线程同时执行 create_user() 可能导致 next_id 竞态条件（两个请求获得相同 ID）
# 2. 多线程同时修改 users 字典可能导致数据损坏
# 生产环境解决方案：
# 1. 使用真实数据库（PostgreSQL、MySQL）- 数据库提供 ACID 保证
# 2. 使用 threading.Lock 保护临界区（性能开销大）
# 3. 使用进程隔离（每个进程独立状态，通过数据库共享）
users: dict[int, UserCreate] = {}
next_id: int = 1


# ============================================================================
# CRUD 端点
# ============================================================================


@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserResponse:
    """创建用户"""
    global next_id

    user_id = next_id
    next_id += 1

    users[user_id] = user

    return UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        age=user.age,
    )


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    """获取单个用户"""
    if user_id not in users:
        raise HTTPException(status_code=404, detail="用户不存在")

    user = users[user_id]
    return UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        age=user.age,
    )


@app.get("/users/", response_model=list[UserResponse])
async def list_users(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> list[UserResponse]:
    """列出所有用户（分页）"""
    all_users = list(users.items())

    # 使用 PEP 695 泛型函数进行分页
    paginated = paginate(all_users, skip, limit)

    return [
        UserResponse(
            id=user_id,
            name=user.name,
            email=user.email,
            age=user.age,
        )
        for user_id, user in paginated
    ]


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate) -> UserResponse:
    """更新用户"""
    if user_id not in users:
        raise HTTPException(status_code=404, detail="用户不存在")

    users[user_id] = user

    return UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        age=user.age,
    )


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int) -> None:
    """删除用户"""
    if user_id not in users:
        raise HTTPException(status_code=404, detail="用户不存在")

    del users[user_id]


# ============================================================================
# 测试辅助函数
# ============================================================================


def reset_database() -> None:
    """重置数据库（用于测试）"""
    global next_id
    users.clear()
    next_id = 1


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    from core.settings import get_settings

    settings = get_settings()
    import uvicorn

    print("=" * 70)
    print("练习 1 参考答案: 用户管理 API")
    print("=" * 70)
    print("\n实现功能：")
    print("  ✅ POST /users/ - 创建用户")
    print("  ✅ GET /users/{user_id} - 获取用户")
    print("  ✅ GET /users/ - 列出用户（分页）")
    print("  ✅ PUT /users/{user_id} - 更新用户")
    print("  ✅ DELETE /users/{user_id} - 删除用户")
    print("\n测试命令:")
    print("  pytest tests/test_exercises.py::test_exercise_01 -v")
    print("\n启动服务:")
    print("  uvicorn solutions.01_create_api:app --reload")
    print("  访问文档: http://localhost:8000/docs\n")

    uvicorn.run(
        app,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
    )
