"""基于角色的访问控制（RBAC）模块。

from __future__ import annotations

提供 Principal 解析、角色验证和路由权限依赖。
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from fastapi import Depends, HTTPException, Request

Role = Literal["viewer", "editor", "admin"]


@dataclass(frozen=True)
class Principal:
    """请求主体，包含用户身份和权限信息。"""

    user_id: str
    role: Role
    workspace_id: str


def get_principal(request: Request) -> Principal:
    """从请求头解析 Principal。

    头部：
        X-User-Id: 用户 ID，默认 "anonymous"
        X-Role: 用户角色，默认 "viewer"
        X-Workspace-Id: 工作空间 ID，默认 "default"

    Raises:
        HTTPException(403): 如果角色无效
    """
    user_id = request.headers.get("X-User-Id", "anonymous")
    role_value = request.headers.get("X-Role", "viewer")
    workspace_id = request.headers.get("X-Workspace-Id", "default")

    # 验证角色有效性
    valid_roles: set[Role] = {"viewer", "editor", "admin"}
    if role_value not in valid_roles:
        raise HTTPException(
            status_code=403,
            detail=f"无效角色: {role_value}",
        )

    return Principal(
        user_id=user_id,
        role=role_value,
        workspace_id=workspace_id,
    )


def require_role(*allowed_roles: Role) -> Callable[[Principal], Principal]:
    """创建角色验证依赖。

    Args:
        *allowed_roles: 允许访问的角色列表

    Returns:
        可注入的 FastAPI 依赖函数

    Raises:
        HTTPException(403): 如果 Principal 的角色不在允许列表中
    """

    def dependency(principal: Principal = Depends(get_principal)) -> Principal:  # noqa: B008
        if principal.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"需要 {' 或 '.join(allowed_roles)} 权限",
            )
        return principal

    return dependency
