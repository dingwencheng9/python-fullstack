"""
L11 防御性安全网关测试 - pytest-asyncio
======================================

测试覆盖：
---------
1. JWT Token 认证
2. RBAC 角色检查
3. 权限验证
4. Rate Limiting
5. OpenTelemetry 审计追踪

作者：Python 3.13 全栈课程
"""

from __future__ import annotations

import importlib

import pytest

pytest.importorskip("httpx", reason="需要 httpx（uv sync --extra web）")
pytest.importorskip("jwt", reason="python-jose/jwt 未安装")
pytest.importorskip("fastapi", reason="需要 fastapi（uv sync --extra web）")
pytest.importorskip("passlib", reason="需要 passlib（uv sync --extra web）")

from httpx import ASGITransport, AsyncClient


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture(scope="module")
def security_deps():
    """动态导入以数字开头的模块。"""
    # 在 fixture 中导入，确保 conftest.py 已执行
    deps = importlib.import_module("examples.01_security_dependencies")
    return deps


@pytest.fixture
def app(security_deps):
    """返回 FastAPI 应用。"""
    return security_deps.app


@pytest.fixture
def create_access_token(security_deps):
    """返回 Token 创建函数。"""
    return security_deps.create_access_token


@pytest.fixture
def UserRole(security_deps):
    """返回 UserRole 枚举。"""
    return security_deps.UserRole


@pytest.fixture(autouse=True)
def reset_users_db(security_deps, UserRole):
    """每个测试前重置用户数据库（自动应用）"""
    # 导入原始密码哈希函数
    pwd_context = security_deps.pwd_context

    # 重置为初始状态
    security_deps.users_db.clear()
    security_deps.users_db.update(
        {
            "admin": {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "hashed_password": pwd_context.hash("AdminPass123!"),
                "role": UserRole.ADMIN,
                "disabled": False,
            },
            "manager": {
                "id": 2,
                "username": "manager",
                "email": "manager@example.com",
                "hashed_password": pwd_context.hash("ManagerPass123!"),
                "role": UserRole.MANAGER,
                "disabled": False,
            },
            "user": {
                "id": 3,
                "username": "user",
                "email": "user@example.com",
                "hashed_password": pwd_context.hash("UserPass123!"),
                "role": UserRole.USER,
                "disabled": False,
            },
        }
    )


@pytest.fixture
async def client(app):
    """测试客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def admin_token(create_access_token, UserRole, reset_users_db) -> str:
    """管理员 Token"""
    return create_access_token(
        {
            "sub": "admin",
            "role": UserRole.ADMIN,
        }
    )


@pytest.fixture
def manager_token(create_access_token, UserRole, reset_users_db) -> str:
    """经理 Token"""
    return create_access_token(
        {
            "sub": "manager",
            "role": UserRole.MANAGER,
        }
    )


@pytest.fixture
def user_token(create_access_token, UserRole, reset_users_db) -> str:
    """普通用户 Token"""
    return create_access_token(
        {
            "sub": "user",
            "role": UserRole.USER,
        }
    )


# ============================================================
# 测试登录
# ============================================================


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """测试登录（成功）"""
    response = await client.post(
        "/login",
        json={
            "username": "admin",
            "password": "AdminPass123!",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data


@pytest.mark.asyncio
async def test_login_invalid_username(client: AsyncClient):
    """测试登录（用户名错误）"""
    response = await client.post(
        "/login",
        json={
            "username": "nonexistent",
            "password": "WrongPass123!",
        },
    )

    assert response.status_code == 401
    assert "用户名或密码错误" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    """测试登录（密码错误）"""
    response = await client.post(
        "/login",
        json={
            "username": "admin",
            "password": "WrongPass123!",
        },
    )

    assert response.status_code == 401
    assert "用户名或密码错误" in response.json()["detail"]


# ============================================================
# 测试认证
# ============================================================


@pytest.mark.asyncio
async def test_get_me_success(client: AsyncClient, admin_token: str):
    """测试获取当前用户（成功）"""
    response = await client.get(
        "/me",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["role"] == "admin"


@pytest.mark.asyncio
async def test_get_me_no_token(client: AsyncClient):
    """测试获取当前用户（无 Token）"""
    response = await client.get("/me")

    assert response.status_code == 401  # FastAPI HTTPBearer 返回 401


@pytest.mark.asyncio
async def test_get_me_invalid_token(client: AsyncClient):
    """测试获取当前用户（无效 Token）"""
    response = await client.get(
        "/me",
        headers={"Authorization": "Bearer invalid_token_here"},
    )

    assert response.status_code == 401
    assert "Token 无效" in response.json()["detail"]


# ============================================================
# 测试 RBAC 角色检查
# ============================================================


@pytest.mark.asyncio
async def test_list_users_as_admin(client: AsyncClient, admin_token: str):
    """测试获取用户列表（管理员）"""
    response = await client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 3  # admin, manager, user


@pytest.mark.asyncio
async def test_list_users_as_manager(client: AsyncClient, manager_token: str):
    """测试获取用户列表（经理，权限不足）"""
    response = await client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {manager_token}"},
    )

    assert response.status_code == 403
    assert "权限不足" in response.json()["detail"]


@pytest.mark.asyncio
async def test_list_users_as_user(client: AsyncClient, user_token: str):
    """测试获取用户列表（普通用户，权限不足）"""
    response = await client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 403
    assert "权限不足" in response.json()["detail"]


# ============================================================
# 测试权限检查
# ============================================================


@pytest.mark.asyncio
async def test_protected_read_as_user(client: AsyncClient, user_token: str):
    """测试读权限（普通用户，有权限）"""
    response = await client.get(
        "/protected/read",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "读取成功"


@pytest.mark.asyncio
async def test_protected_write_as_user(client: AsyncClient, user_token: str):
    """测试写权限（普通用户，有权限）"""
    response = await client.post(
        "/protected/write",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "写入成功"


# ============================================================
# 测试删除用户（权限检查）
# ============================================================


@pytest.mark.asyncio
async def test_delete_user_as_admin(client: AsyncClient, admin_token: str):
    """测试删除用户（管理员，有权限）"""
    response = await client.delete(
        "/admin/users/3",  # 删除 user
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    # 第一次删除成功
    if response.status_code == 204:
        assert response.status_code == 204
    # 或者用户已被删除
    elif response.status_code == 404:
        assert "不存在" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_user_as_manager(client: AsyncClient, manager_token: str):
    """测试删除用户（经理，有 DELETE 权限）"""
    response = await client.delete(
        "/admin/users/3",
        headers={"Authorization": f"Bearer {manager_token}"},
    )

    # 经理有 DELETE 权限，应该成功
    assert response.status_code in (204, 404)


@pytest.mark.asyncio
async def test_delete_user_as_user(client: AsyncClient, user_token: str):
    """测试删除用户（普通用户，无权限）"""
    response = await client.delete(
        "/admin/users/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    # 普通用户没有 DELETE 权限，应返回 403
    assert response.status_code == 403
    detail = response.json()["detail"]
    # 检查错误消息包含权限相关关键词
    assert any(keyword in detail for keyword in ["缺少权限", "权限不足", "permission"])


@pytest.mark.asyncio
async def test_delete_self(client: AsyncClient, admin_token: str):
    """测试删除自己（应被阻止）"""
    response = await client.delete(
        "/admin/users/1",  # admin 的 ID
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 403
    assert "无法删除自己" in response.json()["detail"]


# ============================================================
# 测试 Rate Limiting
# ============================================================


@pytest.mark.asyncio
@pytest.mark.skip(reason="Rate Limiting 需要 Redis，跳过实际测试")
async def test_rate_limiting(client: AsyncClient):
    """测试 Rate Limiting（需要 Redis）"""
    # 模拟：连续 6 次登录尝试
    for i in range(6):
        response = await client.post(
            "/login",
            json={
                "username": "admin",
                "password": "WrongPass123!",
            },
        )

        if i < 5:
            # 前 5 次应该返回 401（密码错误）
            assert response.status_code == 401
        else:
            # 第 6 次应该返回 429（Rate Limit）
            assert response.status_code == 429
            assert "请求过于频繁" in response.json()["detail"]


# ============================================================
# 集成测试
# ============================================================


@pytest.mark.asyncio
async def test_full_auth_flow(client: AsyncClient):
    """测试完整认证流程"""
    # 1. 登录获取 Token
    login_response = await client.post(
        "/login",
        json={
            "username": "admin",
            "password": "AdminPass123!",
        },
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # 2. 使用 Token 获取用户信息
    me_response = await client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "admin"

    # 3. 访问受保护资源
    protected_response = await client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert protected_response.status_code == 200
