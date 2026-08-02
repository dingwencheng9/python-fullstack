"""示例：RBAC 权限系统实战

演示面向对象在实际系统中的应用：用户角色权限管理。
这是企业级应用中常见的 RBAC (Role-Based Access Control) 模型。
"""

# ============ RBAC 权限系统 ============
print("=" * 60)
print("RBAC 权限系统实战")
print("=" * 60)


class User:
    """用户基类 — RBAC 系统核心

    在 RBAC 系统中，用户被分配角色，角色决定权限。
    """

    ROLE_ADMIN: str = "admin"
    ROLE_MANAGER: str = "manager"
    ROLE_EMPLOYEE: str = "employee"

    def __init__(self, username: str, role: str = "employee") -> None:
        """初始化用户

        Args:
            username: 用户名
            role: 角色，默认普通员工
        """
        self.username = username
        self._role = role

    @property
    def role(self) -> str:
        """获取角色（只读）"""
        return self._role

    def has_permission(self, action: str) -> bool:
        """检查用户是否有执行某操作的权限

        Args:
            action: 操作名称，如 "read", "write", "delete"

        Returns:
            是否有权限
        """
        permissions = self._get_permissions()
        return action in permissions

    def _get_permissions(self) -> set[str]:
        """获取权限集合 — 子类可重写

        Returns:
            权限集合
        """
        return {"read"}


class Admin(User):
    """管理员 — 最高权限

    管理员拥有所有基础权限，并可以动态授权。
    """

    def __init__(self, username: str) -> None:
        super().__init__(username, self.ROLE_ADMIN)
        self.__granted_permissions: set[str] = set()

    def _get_permissions(self) -> set[str]:
        """管理员拥有所有基础权限 + 自定义权限"""
        return {"read", "write", "delete", "admin"} | self.__granted_permissions

    def grant_permission(self, action: str) -> None:
        """授予权限

        Args:
            action: 要授予的权限
        """
        self.__granted_permissions.add(action)
        print(f"[权限变更] {self.username} 授予 {action}")

    def revoke_permission(self, action: str) -> None:
        """撤销权限

        Args:
            action: 要撤销的权限
        """
        self.__granted_permissions.discard(action)
        print(f"[权限变更] {self.username} 撤销 {action}")

    def list_permissions(self) -> set[str]:
        """列出所有权限"""
        return self._get_permissions()


class Manager(User):
    """经理 — 中级权限

    经理拥有读写和审批权限。
    """

    def __init__(self, username: str, department: str) -> None:
        super().__init__(username, self.ROLE_MANAGER)
        self._department = department

    @property
    def department(self) -> str:
        """获取部门"""
        return self._department

    def _get_permissions(self) -> set[str]:
        """经理权限：读写 + 审批"""
        return {"read", "write", "approve"}


class Employee(User):
    """普通员工 — 基础权限

    员工只有读取权限。
    """

    def _get_permissions(self) -> set[str]:
        """员工只有读取权限"""
        return {"read"}


# ============ 系统演示 ============
print("\n=== 1. 创建不同角色的用户 ===")

admin = Admin("root")
manager = Manager("alice", "Engineering")
employee = Employee("bob")

print(f"创建用户: username={admin.username}, role={admin.role}")
print(f"创建用户: username={manager.username}, role={manager.role}, dept={manager.department}")
print(f"创建用户: username={employee.username}, role={employee.role}")

print("\n=== 2. 权限检查演示 ===")

actions = ["read", "write", "delete", "approve", "admin"]
users = [admin, manager, employee]

print(f"{'用户':<12} {'read':<8} {'write':<8} {'delete':<8} {'approve':<10} {'admin':<8}")
print("-" * 60)

for user in users:
    row = f"{user.username:<12}"
    for action in actions:
        status = "✅" if user.has_permission(action) else "❌"
        row += f" {status:<7}"
    print(row)

print("\n=== 3. 管理员动态授权 ===")

print(f"root 当前权限: {admin.list_permissions()}")
print(f"root 是否有 audit 权限: {admin.has_permission('audit')}")

admin.grant_permission("audit")
print(f"授权后 root 是否有 audit 权限: {admin.has_permission('audit')}")
print(f"授权后 root 权限: {admin.list_permissions()}")

admin.revoke_permission("audit")
print(f"撤销后 root 是否有 audit 权限: {admin.has_permission('audit')}")

print("\n=== 4. 多态演示：批量权限检查 ===")


def check_permission(user: User, action: str) -> str:
    """统一的权限检查接口"""
    return f"{user.username}: {action} {'允许' if user.has_permission(action) else '拒绝'}"


all_users: list[User] = [admin, manager, employee]

print(f"\n{'delete' + ' 操作权限检查':^60}")
print("-" * 60)
for user in all_users:
    print(check_permission(user, "delete"))


# ============ 进阶：组合模式（注入 User） ============
print("\n=== 5. 组合模式：资源操作类 ===")


class ProtectedResource:
    """受保护的资源操作类"""

    def __init__(self, user: User) -> None:
        """接收一个 User 实例

        Args:
            user: 拥有权限的用户
        """
        self._user = user

    def read_data(self, resource_id: str) -> str:
        """读取数据"""
        if not self._user.has_permission("read"):
            # raise PermissionError: 需要 'read' 权限  # L08 将学到
            pass
        return f"读取资源 {resource_id} 成功"

    def write_data(self, resource_id: str, data: str) -> str:
        """写入数据"""
        if not self._user.has_permission("write"):
            # raise PermissionError: 需要 'write' 权限  # L08 将学到
            pass
        return f"写入资源 {resource_id}: {data}"

    def delete_data(self, resource_id: str) -> str:
        """删除数据"""
        if not self._user.has_permission("delete"):
            # raise PermissionError: 需要 'delete' 权限  # L08 将学到
            pass
        return f"删除资源 {resource_id} 成功"


print("普通员工尝试操作:")
emp_resource = ProtectedResource(employee)

result = emp_resource.read_data("doc-001")
print(f"  读取: {result}")  # ✅ 普通员工有读取权限

result = emp_resource.delete_data("doc-001")  # ❌ 无权限，但 raise 已注释（L08 将学到如何捕获）
print(f"  删除: {result}")  # ⚠️ raise 注释后不再抛异常

print("\n管理员尝试操作:")
admin_resource = ProtectedResource(admin)

result = admin_resource.delete_data("doc-001")
print(f"  删除: {result}")  # ✅ 管理员有删除权限


# ============ 总结 ============
print("\n" + "=" * 60)
print("RBAC 系统设计总结")
print("=" * 60)
print("1. User 基类定义统一的权限检查接口")
print("2. Admin/Manager/Employee 继承 User，实现不同权限级别")
print("3. _get_permissions() 方法被子类重写，实现权限差异化")
print("4. has_permission() 方法支持运行时权限检查")
print("5. 多态让我们可以用统一的接口操作不同角色")
print("6. @property 实现只读属性，保护数据一致性")
print("\n这是企业级权限管理的核心模式！")
