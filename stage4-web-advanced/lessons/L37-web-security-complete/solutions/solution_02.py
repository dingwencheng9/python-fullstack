"""

from __future__ import annotations

练习 2: RBAC 权限控制系统 - Python 3.13 参考答案

本解决方案展示：
1. Python 3.13 PEP 695 泛型语法
2. match/case 模式匹配
3. asyncio.TaskGroup 并发权限检查
4. Free-threading 线程安全设计

【解题思路】

1. RBAC 核心概念：
   - 角色（Role）：用户的身份分类
   - 权限（Permission）：操作资源的能力
   - 映射（Mapping）：角色拥有哪些权限
   - 检查（Check）：验证用户是否有权限

2. 权限设计原则：
   - 最小权限原则：只授予必要权限
   - 角色继承：高级角色包含低级角色的权限
   - 显式拒绝：默认拒绝，显式授权

3. 依赖注入模式：
   - 使用 Depends 注入权限检查
   - 在路由级别声明所需权限
   - 统一的错误处理

4. 资源所有权：
   - 所有者有特殊权限
   - 管理员可以访问所有资源
   - 普通用户只能操作自己的资源

【关键知识点】

- RBAC 模型设计
- 枚举类型的使用
- FastAPI 依赖注入
- HTTP 403 Forbidden 状态码
- 权限检查装饰器模式
- Python 3.13 PEP 695 泛型语法
- match/case 模式匹配
- asyncio.TaskGroup 并发处理

作者：Python 3.13 全栈课程
"""

import asyncio
from enum import StrEnum
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

# ============================================================================
# 1. 定义角色和权限枚举
# ============================================================================


class UserRole(StrEnum):
    """用户角色"""

    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"


class Permission(StrEnum):
    """权限"""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


# ============================================================================
# 2. 定义 RBAC 权限映射表（Free-threading 线程安全说明）
# ============================================================================

# 🔒 Free-threading 线程安全说明:
# - 这是一个只读字典，初始化后不修改
# - Python 3.14 环境下读操作是线程安全的
# - 如果需要动态修改权限，应使用 asyncio.Lock
ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN},
    UserRole.MANAGER: {Permission.READ, Permission.WRITE, Permission.DELETE},
    UserRole.USER: {Permission.READ, Permission.WRITE},
    UserRole.GUEST: {Permission.READ},
}


# ============================================================================
# 3. 定义数据模型
# ============================================================================


class User(BaseModel):
    """用户模型"""

    username: str
    role: UserRole


class Resource(BaseModel):
    """资源模型"""

    id: int
    name: str
    content: str
    owner: str


# ============================================================================
# 4. 泛型权限检查器（Python 3.13 PEP 695 泛型）
# ============================================================================


class PermissionChecker[T]:
    """
    泛型权限检查器（Python 3.13 PEP 695 泛型语法）

    🚀 Python 3.13 PEP 695 特性:
    - 使用 class PermissionChecker[T]: 定义泛型类
    - 相比旧语法更简洁直观
    - 类型推断更准确

    泛型参数:
        T: 用户类型（User 或其子类）
    """

    def __init__(self, role_permissions: dict[UserRole, set[Permission]]) -> None:
        self.role_permissions = role_permissions

    def has_permission(self, user: T, permission: Permission) -> bool:
        """
        检查用户是否有指定权限（使用 match/case）

        🎯 Python 3.10+ match/case 模式匹配
        """
        # 获取用户权限
        user_permissions = self.role_permissions.get(user.role, set())

        # 使用 match/case 检查权限
        match permission in user_permissions:
            case True:
                return True
            case False:
                # 检查是否是 ADMIN 角色（管理员有所有权限）
                match user.role:
                    case UserRole.ADMIN:
                        return True
                    case _:
                        return False

    def check_resource_access(self, user: T, resource: Resource, required_permission: Permission) -> bool:
        """
        检查资源访问权限（使用 match/case）

        🎯 使用 match/case 实现复杂的访问控制逻辑
        """
        # 使用 match/case 检查访问权限
        match (user.role, resource.owner == user.username):
            case (UserRole.ADMIN, _):
                # 管理员可以访问所有资源
                return True
            case (_, True):
                # 资源所有者可以访问
                return True
            case (_, False):
                # 其他情况需要检查权限
                return self.has_permission(user, required_permission)


# 创建全局权限检查器
permission_checker: PermissionChecker[User] = PermissionChecker(ROLE_PERMISSIONS)


# ============================================================================
# 5. 模拟用户和资源数据库
# ============================================================================

# 🔒 Free-threading: 只读字典，线程安全
fake_users_db: dict[str, User] = {
    "admin": User(username="admin", role=UserRole.ADMIN),
    "manager": User(username="manager", role=UserRole.MANAGER),
    "user": User(username="user", role=UserRole.USER),
    "guest": User(username="guest", role=UserRole.GUEST),
}

fake_resources_db: dict[int, Resource] = {
    1: Resource(id=1, name="公开文档", content="这是公开内容", owner="admin"),
    2: Resource(id=2, name="内部文档", content="这是内部内容", owner="manager"),
    3: Resource(id=3, name="用户文档", content="这是用户内容", owner="user"),
}


# ============================================================================
# 6. 实现权限检查函数
# ============================================================================


def require_permission(required_permission: Permission):
    """权限检查依赖工厂"""

    async def permission_checker_dep(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if not permission_checker.has_permission(current_user, required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要 {required_permission.value} 权限",
            )
        return current_user

    return permission_checker_dep


# ============================================================================
# 7. 实现资源访问控制（使用 match/case）
# ============================================================================


def get_resource_or_403(resource_id: int, current_user: User) -> Resource:
    """
    获取资源并检查权限（使用 match/case）

    🎯 Python 3.10+ match/case 模式匹配
    """
    if resource_id not in fake_resources_db:
        raise HTTPException(status_code=404, detail="资源不存在")

    resource = fake_resources_db[resource_id]

    # 使用 match/case 检查访问权限
    match (current_user.role, resource.owner == current_user.username):
        case (UserRole.ADMIN, _):
            # 管理员可以访问所有资源
            return resource
        case (_, True):
            # 资源所有者可以访问
            return resource
        case (_, False):
            # 其他情况拒绝访问
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此资源",
            )


# ============================================================================
# 8. 批量权限检查（使用 asyncio.TaskGroup）
# ============================================================================


async def check_permissions_batch(user: User, permissions: list[Permission]) -> dict[Permission, bool]:
    """
    批量检查权限（使用 asyncio.TaskGroup 并发）

    🚀 Python 3.13 asyncio.TaskGroup:
    - 结构化并发，自动等待所有任务完成
    - 异常安全，任何任务失败会取消其他任务

    Args:
        user: 用户对象
        permissions: 权限列表

    Returns:
        权限检查结果字典
    """
    results: dict[Permission, bool] = {}

    async def check_single(perm: Permission) -> tuple[Permission, bool]:
        """检查单个权限"""
        # 模拟异步检查（实际可能查询数据库）
        await asyncio.sleep(0.01)
        has_perm = permission_checker.has_permission(user, perm)
        return (perm, has_perm)

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(check_single(perm)) for perm in permissions]

    # 收集结果
    for task in tasks:
        perm, has_perm = task.result()
        results[perm] = has_perm

    return results


# ============================================================================
# 9. 创建 FastAPI 应用和路由
# ============================================================================

app = FastAPI(title="RBAC 权限控制练习 - Python 3.13")


# 模拟获取当前用户
async def get_current_user(username: str = "guest") -> User:
    """获取当前用户（简化版）"""
    if username not in fake_users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    return fake_users_db[username]


@app.get("/resources/")
async def list_resources(
    current_user: Annotated[User, Depends(require_permission(Permission.READ))],
) -> list[Resource]:
    """列出所有资源（需要 READ 权限）"""
    # 管理员可以看到所有资源
    if permission_checker.has_permission(current_user, Permission.ADMIN):
        return list(fake_resources_db.values())

    # 普通用户只能看到自己的资源
    return [resource for resource in fake_resources_db.values() if resource.owner == current_user.username]


@app.post("/resources/", status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource: Resource,
    current_user: Annotated[User, Depends(require_permission(Permission.WRITE))],
) -> Resource:
    """创建资源（需要 WRITE 权限）"""
    # 自动设置所有者
    resource.owner = current_user.username

    # 保存资源
    fake_resources_db[resource.id] = resource

    return resource


@app.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: int,
    current_user: Annotated[User, Depends(require_permission(Permission.DELETE))],
) -> None:
    """删除资源（需要 DELETE 权限或是资源所有者）"""
    # 检查资源权限
    get_resource_or_403(resource_id, current_user)

    # 删除资源
    del fake_resources_db[resource_id]


@app.get("/admin/users/")
async def list_users(
    current_user: Annotated[User, Depends(require_permission(Permission.ADMIN))],
) -> list[User]:
    """列出所有用户（仅管理员）"""
    return list(fake_users_db.values())


@app.post("/users/{username}/permissions")
async def check_user_permissions(username: str, permissions: list[Permission]) -> dict[str, Any]:
    """
    批量检查用户权限（使用 asyncio.TaskGroup 并发）

    🚀 展示 Python 3.13 TaskGroup 并发检查
    """
    if username not in fake_users_db:
        raise HTTPException(status_code=404, detail="用户不存在")

    user = fake_users_db[username]
    results = await check_permissions_batch(user, permissions)

    return {
        "username": username,
        "role": user.role.value,
        "permissions": {perm.value: has_perm for perm, has_perm in results.items()},
    }


@app.get("/")
async def root() -> dict[str, Any]:
    """根端点"""
    return {
        "message": "RBAC 权限控制系统 (Python 3.13)",
        "roles": [role.value for role in UserRole],
        "permissions": [perm.value for perm in Permission],
        "features": [
            "PEP 695 泛型语法",
            "match/case 模式匹配",
            "asyncio.TaskGroup 并发",
            "Free-threading 线程安全",
        ],
    }


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    from core.settings import get_settings

    settings = get_settings()
    import uvicorn

    print("=" * 70)
    print("练习 2 参考答案: RBAC 权限控制系统 - Python 3.13")
    print("=" * 70)
    print("\n特性:")
    print("  ✅ PEP 695 泛型语法: class PermissionChecker[T]")
    print("  ✅ match/case: 复杂权限检查逻辑")
    print("  ✅ asyncio.TaskGroup: 批量权限检查")
    print("  ✅ Free-threading 线程安全设计")
    print("\n角色权限映射：")
    for role, perms in ROLE_PERMISSIONS.items():
        print(f"  {role.value:8} -> {', '.join(p.value for p in perms)}")
    print("\n测试用户：")
    for username, user in fake_users_db.items():
        print(f"  {username:8} (角色: {user.role.value})")
    print("\n测试步骤：")
    print("  1. 访问 http://localhost:8000/docs")
    print("  2. 测试不同用户的权限：")
    print("     - GET /resources/ (所有角色)")
    print("     - POST /resources/ (需要 WRITE)")
    print("     - DELETE /resources/1 (需要 DELETE)")
    print("     - GET /admin/users/ (仅 ADMIN)")
    print("     - POST /users/{username}/permissions (批量检查)")
    print("\n启动服务...\n")

    uvicorn.run(
        app,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
    )
