"""

from __future__ import annotations

练习 2: RBAC 权限控制系统

任务：
实现基于角色的访问控制（RBAC）系统。

学习目标：
- 理解 RBAC 的核心概念（用户、角色、权限）
- 实现角色与权限的映射
- 使用装饰器保护端点
- 实现动态权限检查

预计时间: 60 分钟
难度: ⭐⭐⭐⭐☆
"""

from typing import Annotated

from fastapi import Depends, FastAPI

# ============================================================================
# TODO 1: 定义角色和权限枚举
# ============================================================================

# TODO: 创建角色枚举
# class UserRole(str, Enum):
#     ADMIN = "admin"
#     MANAGER = "manager"
#     USER = "user"
#     GUEST = "guest"


# TODO: 创建权限枚举
# class Permission(str, Enum):
#     READ = "read"
#     WRITE = "write"
#     DELETE = "delete"
#     ADMIN = "admin"


# ============================================================================
# TODO 2: 定义 RBAC 权限映射表
# ============================================================================

# TODO: 创建角色到权限的映射
# ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
#     UserRole.ADMIN: {...},
#     UserRole.MANAGER: {...},
#     UserRole.USER: {...},
#     UserRole.GUEST: {...},
# }


# ============================================================================
# TODO 3: 定义数据模型
# ============================================================================

# TODO: 创建用户模型（包含角色）
# class User(BaseModel):
#     username: str
#     role: UserRole


# TODO: 创建资源模型
# class Resource(BaseModel):
#     id: int
#     name: str
#     content: str
#     owner: str


# ============================================================================
# TODO 4: 模拟用户和资源数据库
# ============================================================================

# TODO: 创建模拟用户数据库
# fake_users_db: dict[str, User] = {
#     "admin": User(username="admin", role=UserRole.ADMIN),
#     "manager": User(username="manager", role=UserRole.MANAGER),
#     "user": User(username="user", role=UserRole.USER),
#     "guest": User(username="guest", role=UserRole.GUEST),
# }


# TODO: 创建模拟资源数据库
# fake_resources_db: dict[int, Resource] = {
#     1: Resource(id=1, name="公开文档", content="...", owner="admin"),
#     2: Resource(id=2, name="内部文档", content="...", owner="manager"),
# }


# ============================================================================
# TODO 5: 实现权限检查函数
# ============================================================================


def has_permission(user: User, permission: Permission) -> bool:
    """检查用户是否有指定权限"""
    # TODO: 根据用户角色检查权限


def check_permission(required_permission: Permission):
    """权限检查依赖（装饰器模式）"""
    # TODO:
    # 1. 创建依赖函数
    # 2. 获取当前用户
    # 3. 检查权限
    # 4. 返回用户或抛出 403 异常


# ============================================================================
# TODO 6: 实现资源访问控制
# ============================================================================


def check_resource_owner(resource_id: int, current_user: User):
    """检查资源所有权"""
    # TODO:
    # 1. 获取资源
    # 2. 检查是否是所有者或管理员
    # 3. 返回资源或抛出异常


# ============================================================================
# TODO 7: 创建 FastAPI 应用和路由
# ============================================================================

app = FastAPI(title="RBAC 权限控制练习")


# 模拟获取当前用户（简化版，实际应结合 JWT）
async def get_current_user(username: str = "guest") -> User:
    """获取当前用户（简化版）"""
    # TODO: 从数据库获取用户


@app.get("/resources/")
async def list_resources(
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Resource]:
    """列出所有资源（需要 READ 权限）"""
    # TODO:
    # 1. 检查 READ 权限
    # 2. 返回资源列表


@app.post("/resources/")
async def create_resource(
    resource: Resource,
    current_user: Annotated[User, Depends(get_current_user)],
) -> Resource:
    """创建资源（需要 WRITE 权限）"""
    # TODO:
    # 1. 检查 WRITE 权限
    # 2. 创建资源
    # 3. 返回资源


@app.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """删除资源（需要 DELETE 权限或是资源所有者）"""
    # TODO:
    # 1. 检查 DELETE 权限或资源所有权
    # 2. 删除资源
    # 3. 返回成功消息


@app.get("/admin/users/")
async def list_users(
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[User]:
    """列出所有用户（仅管理员）"""
    # TODO:
    # 1. 检查 ADMIN 权限
    # 2. 返回用户列表


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 2: RBAC 权限控制系统")
    print("=" * 70)
    print("\n任务：")
    print("  1. 定义角色和权限枚举")
    print("  2. 创建 RBAC 权限映射表")
    print("  3. 实现权限检查函数")
    print("  4. 实现资源访问控制")
    print("  5. 保护 API 端点")
    print("\n测试方法：")
    print("  1. 启动服务: uvicorn exercises.02_rbac:app --reload")
    print("  2. 测试不同角色的访问权限")
    print("  3. 验证权限检查是否正确")
    print("\n角色权限：")
    print("  - ADMIN: 所有权限")
    print("  - MANAGER: READ, WRITE, DELETE")
    print("  - USER: READ, WRITE")
    print("  - GUEST: READ")
    print()
