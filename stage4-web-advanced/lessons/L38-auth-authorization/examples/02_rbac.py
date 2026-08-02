"""Example 2: RBAC Implementation"""

from enum import Enum
from functools import wraps
from dataclasses import dataclass, field


class Role(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE_USERS = "manage_users"
    VIEW_ADMIN = "view_admin"


# Role-Permission mapping
ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.ADMIN: {p for p in Permission},
    Role.MODERATOR: {Permission.READ, Permission.WRITE, Permission.DELETE},
    Role.USER: {Permission.READ, Permission.WRITE},
    Role.GUEST: {Permission.READ},
}


@dataclass
class User:
    id: str
    name: str
    roles: list[Role] = field(default_factory=list)

    def has_permission(self, permission: Permission) -> bool:
        """Check if user has a specific permission."""
        for role in self.roles:
            if permission in ROLE_PERMISSIONS.get(role, set()):
                return True
        return False

    def has_any_role(self, *roles: Role) -> bool:
        """Check if user has any of the specified roles."""
        return any(role in self.roles for role in roles)


def require_permission(permission: Permission):
    """Decorator to require a permission."""

    def decorator(func):
        @wraps(func)
        async def wrapper(user: User, *args, **kwargs):
            if not user.has_permission(permission):
                raise PermissionError(f"Permission denied: {permission}")
            return await func(user, *args, **kwargs)

        return wrapper

    return decorator


# Usage example
async def delete_post(user: User, post_id: str):
    """Delete a post (requires DELETE permission)."""

    @require_permission(Permission.DELETE)
    async def _delete(user: User, post_id: str):
        # Actual delete logic
        return {"deleted": post_id}

    return await _delete(user, post_id)


if __name__ == "__main__":
    admin = User(id="1", name="Admin", roles=[Role.ADMIN])
    user = User(id="2", name="User", roles=[Role.USER])

    print(f"Admin can delete: {admin.has_permission(Permission.DELETE)}")
    print(f"User can delete: {user.has_permission(Permission.DELETE)}")
    print(f"User can read: {user.has_permission(Permission.READ)}")
