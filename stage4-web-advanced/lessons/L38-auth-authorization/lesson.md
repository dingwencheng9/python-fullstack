# L38: 认证与授权

> **课程编号**: L38
> **所属阶段**: Stage 4 - Web 开发进阶
> **预计时长**: 6-8 小时
> **难度**: ⭐⭐⭐⭐☆（高级）
> **前置课程**: L27, L37
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ **认证机制**：理解 JWT、Session、OAuth2 三种认证方案的原理和适用场景
2. ✅ **JWT 完整实现**：掌握 JWT 签发、验证、刷新、黑名单机制
3. ✅ **RBAC 权限模型**：设计并实现基于角色的权限访问控制系统
4. ✅ **密码安全**：使用 bcrypt/argon2 进行安全的密码存储和验证
5. ✅ **认证中间件**：在 FastAPI 中实现认证中间件和依赖注入
6. ✅ **OAuth2 流程**：理解授权码流程并实现第三方登录
7. ✅ **实战项目**：构建完整的用户认证系统

---

## 📚 课程导读

### 为什么要学习认证授权？

现代 Web 应用几乎都需要用户系统：

```
┌─────────────────────────────────────────────────────┐
│  认证（Authentication）    授权（Authorization）     │
│  ───────────────────     ─────────────────────     │
│  你是谁？                 你能做什么？             │
│  用户名/密码验证           角色/权限检查            │
│  JWT Token 签发           RBAC 权限模型            │
└─────────────────────────────────────────────────────┘
```

**无认证的代价**：
- ❌ 任何人都能访问和修改数据
- ❌ 无法区分用户身份
- ❌ 无法实现个性化功能

**认证授权的价值**：
- ✅ 用户隐私和数据安全
- ✅ 个性化用户体验
- ✅ 权限分级管理
- ✅ 审计追溯

---

## Part 1: 认证与授权基础

### 1.1 核心概念辨析

**认证（Authentication）** 是验证"你是谁"——确认用户身份。

**授权（Authorization）** 是验证"你能做什么"——决定用户权限。

```python
# 认证：验证用户名密码
def login(username: str, password: str) -> bool:
    """验证用户身份"""
    user = db.get_user(username)
    return verify_password(password, user.hash)

# 授权：检查用户权限
def can_delete(user: User, resource: Resource) -> bool:
    """检查用户是否有权删除资源"""
    return user.role == "admin" or resource.owner_id == user.id
```

### 1.2 常见认证方案对比

| 方案 | 适用场景 | 优点 | 缺点 | 推荐指数 |
|------|----------|------|------|----------|
| **Session** | 传统 Web 应用 | 服务端可控、易失效 | 分布式麻烦、占用服务端内存 | ⭐⭐ |
| **JWT** | SPA/移动 API | 无状态、可扩展 | 注销困难、Payload 可解码 | ⭐⭐⭐⭐ |
| **OAuth2** | 第三方登录 | 标准化、安全 | 复杂度高 | ⭐⭐⭐⭐ |
| **API Key** | 服务间通信 | 简单 | 无用户概念 | ⭐⭐ |

### 1.3 Token vs Session 对比

```
Session 认证流程：
┌────────┐     1.登录      ┌────────┐
│ Client │ ──────────────→ │ Server │
└────────┘                └────┬────┘
     │                          │
     │  2.创建Session           │ 3.Session存入Redis
     │  返回SessionID ←─────────┘
     │                          │
     │  4.请求带上SessionID     │
     │ ───────────────────────→│
     │                          │ 5.验证Session
     │  6.返回数据              │
     │ ←───────────────────────│
```

```
JWT 认证流程：
┌────────┐     1.登录      ┌────────┐
│ Client │ ──────────────→ │ Server │
└────────┘                └────┬────┘
     │                          │
     │  2.签发JWT               │
     │  返回Token ←──────────────│
     │                          │
     │  3.请求带上JWT           │
     │ ───────────────────────→│
     │                          │ 4.验签JWT（无状态）
     │  5.返回数据              │
     │ ←───────────────────────│
```

### 1.4 认证方案选择决策树

```
需要选择认证方案？
│
├─ 是否需要第三方登录（GitHub、Google）？
│   └─ 是 → OAuth2 + JWT
│
├─ 是 SPA/移动 App 吗？
│   └─ 是 → JWT
│
├─ 是微服务架构吗？
│   └─ 是 → JWT（无状态）
│
└─ 传统单体 Web 应用？
    └─ 是 → Session + Redis
```

---

## Part 2: JWT 深度实现

### 2.1 JWT 结构详解

JWT 由三部分组成，用 `.` 分隔：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
│──────────────────────────────││──────────────────────────────││──────────────────────────────│
         Header                       Payload                        Signature
```

**Header（头部）**：
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload（负载）**：
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

**Signature（签名）**：
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

### 2.2 JWT 完整实现

```python
import jwt
import datetime
import secrets
import hashlib
from typing import Optional
from pydantic import BaseModel

class TokenPayload(BaseModel):
    """Token Payload 模型"""
    sub: str                    # 用户 ID
    name: str                   # 用户名
    roles: list[str]           # 角色列表
    type: str                  # token 类型
    exp: datetime.datetime     # 过期时间
    iat: datetime.datetime     # 签发时间

class JWTAuth:
    """JWT 认证完整实现"""

    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: str = "HS256",
        access_token_expire: int = 30,      # 分钟
        refresh_token_expire: int = 7,       # 天
    ):
        self.secret = secret_key or secrets.token_hex(32)
        self.algorithm = algorithm
        self.access_expire = access_token_expire
        self.refresh_expire = refresh_token_expire
        self._blacklist: set[str] = set()  # Token 黑名单

    def create_access_token(
        self,
        user_id: str,
        username: str,
        roles: list[str]
    ) -> str:
        """创建访问令牌"""
        now = datetime.datetime.utcnow()
        payload = {
            "sub": user_id,
            "name": username,
            "roles": roles,
            "type": "access",
            "iat": now,
            "exp": now + datetime.timedelta(minutes=self.access_expire),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """创建刷新令牌"""
        now = datetime.datetime.utcnow()
        payload = {
            "sub": user_id,
            "type": "refresh",
            "iat": now,
            "exp": now + datetime.timedelta(days=self.refresh_expire),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def create_tokens(
        self,
        user_id: str,
        username: str,
        roles: list[str]
    ) -> dict[str, str]:
        """同时创建 access 和 refresh token"""
        return {
            "access_token": self.create_access_token(user_id, username, roles),
            "refresh_token": self.create_refresh_token(user_id),
            "token_type": "bearer",
        }

    def verify_token(self, token: str) -> Optional[dict]:
        """验证令牌（不区分类型）"""
        # 检查是否在黑名单
        if token in self._blacklist:
            return None

        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None  # 令牌已过期
        except jwt.InvalidTokenError:
            return None  # 无效令牌

    def verify_access_token(self, token: str) -> Optional[dict]:
        """验证访问令牌"""
        payload = self.verify_token(token)
        if payload and payload.get("type") == "access":
            return payload
        return None

    def verify_refresh_token(self, token: str) -> Optional[dict]:
        """验证刷新令牌"""
        payload = self.verify_token(token)
        if payload and payload.get("type") == "refresh":
            return payload
        return None

    def refresh_access_token(self, refresh_token: str) -> Optional[dict]:
        """用刷新令牌获取新的访问令牌"""
        payload = self.verify_refresh_token(refresh_token)
        if payload:
            # 注意：这里应该从数据库获取用户的最新信息
            # 简化版本直接使用 refresh token 中的信息
            return {
                "access_token": self.create_access_token(
                    payload["sub"],
                    payload.get("name", "Unknown"),
                    payload.get("roles", ["user"])
                ),
                "token_type": "bearer",
            }
        return None

    def revoke_token(self, token: str) -> None:
        """将令牌加入黑名单（登出时调用）"""
        self._blacklist.add(token)

    def get_token_from_header(self, authorization: Optional[str]) -> Optional[str]:
        """从 Authorization Header 中提取 Token"""
        if not authorization:
            return None
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        return parts[1]
```

### 2.3 JWT 安全最佳实践

```python
class JWTSecurity:
    """JWT 安全配置"""

    # ❌ 不安全：使用简单密钥
    UNSAFE_SECRET = "password123"

    # ✅ 安全：使用足够长的随机密钥
    SAFE_SECRET = secrets.token_hex(32)  # 64 字符

    # ❌ 不安全：Token 永不过期
    UNSAFE_CONFIG = {"exp": None}

    # ✅ 安全：设置合理过期时间
    SAFE_CONFIG = {
        "access_expire": 15,    # 15 分钟
        "refresh_expire": 7,   # 7 天
    }

    # ❌ 不安全：敏感信息放 Payload
    UNSAFE_PAYLOAD = {
        "password": "secret123",
        "credit_card": "4111111111111111",
    }

    # ✅ 安全：只放必要信息
    SAFE_PAYLOAD = {
        "sub": "user_id",
        "roles": ["admin"],
    }
```

### 2.4 JWT 常见攻击与防御

| 攻击类型 | 描述 | 防御措施 |
|----------|------|----------|
| **Token 伪造** | 攻击者伪造 Token | 使用强密钥、验证签名 |
| **Token 盗取** | XSS 窃取存储的 Token | HttpOnly Cookie、CSRF Token |
| **Token 重放** | 复用旧 Token | 短期过期、使用 nonce |
| **密钥泄露** | 服务器密钥被获取 | 定期轮换、使用 KMS |

---

## Part 3: 密码安全

### 3.1 密码哈希算法对比

| 算法 | 安全性 | 速度 | 推荐度 |
|------|--------|------|--------|
| **bcrypt** | 高 | 中等 | ⭐⭐⭐⭐⭐ |
| **argon2** | 最高 | 较慢 | ⭐⭐⭐⭐⭐ |
| **scrypt** | 高 | 慢 | ⭐⭐⭐⭐ |
| **PBKDF2** | 中高 | 中等 | ⭐⭐⭐ |
| **SHA-256** | 低 | 快 | ❌ 不推荐 |

### 3.2 bcrypt 完整实现

```python
import bcrypt
from typing import Optional

class PasswordManager:
    """密码管理器"""

    @staticmethod
    def hash_password(password: str, rounds: int = 12) -> str:
        """
        对密码进行哈希处理

        Args:
            password: 明文密码
            rounds: 工作因子（4-31，越大越慢越安全）
                   建议值：12-14（需要 0.1-0.4 秒）

        Returns:
            哈希后的密码字符串
        """
        # 将密码转换为字节
        password_bytes = password.encode('utf-8')

        # 生成盐值并哈希
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)

        # 返回字符串形式
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        验证密码是否正确

        Args:
            password: 待验证的明文密码
            hashed: 数据库中存储的哈希值

        Returns:
            密码是否匹配
        """
        try:
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False

    @staticmethod
    def needs_rehash(hashed: str, current_rounds: int = 12) -> bool:
        """
        检查是否需要重新哈希（密钥轮换时使用）

        Args:
            hashed: 当前哈希值
            current_rounds: 当前配置的工作因子

        Returns:
            是否需要重新哈希
        """
        return bcrypt.gensalt().startswith(b'2b$') or '$' not in hashed
```

### 3.3 argon2 完整实现（推荐）

```python
import argon2
from argon2 import PasswordHasher

class Argon2PasswordManager:
    """Argon2 密码管理器（推荐）"""

    def __init__(self):
        # Argon2id 推荐配置
        self.ph = PasswordHasher(
            time_cost=3,          # 迭代次数
            memory_cost=65536,    # 内存消耗（64MB）
            parallelism=4,         # 并行度
            hash_len=32,          # 哈希长度
            salt_len=16,         # 盐值长度
        )

    def hash_password(self, password: str) -> str:
        """哈希密码"""
        return self.ph.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        """验证密码"""
        try:
            return self.ph.verify(hashed, password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def check_needs_rehash(self, hashed: str) -> bool:
        """检查是否需要重新哈希"""
        try:
            return self.ph.check_needs_rehash(hashed)
        except Exception:
            return True
```

### 3.4 密码策略验证

```python
import re
from dataclasses import dataclass

@dataclass
class PasswordPolicy:
    """密码策略配置"""
    min_length: int = 8
    max_length: int = 128
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digit: bool = True
    require_special: bool = True
    special_chars: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"

class PasswordValidator:
    """密码强度验证器"""

    def __init__(self, policy: PasswordPolicy):
        self.policy = policy

    def validate(self, password: str) -> tuple[bool, list[str]]:
        """
        验证密码强度

        Returns:
            (是否通过, 错误信息列表)
        """
        errors = []

        # 长度检查
        if len(password) < self.policy.min_length:
            errors.append(f"密码长度至少 {self.policy.min_length} 个字符")
        if len(password) > self.policy.max_length:
            errors.append(f"密码长度不能超过 {self.policy.max_length} 个字符")

        # 复杂度检查
        if self.policy.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("密码必须包含大写字母")

        if self.policy.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("密码必须包含小写字母")

        if self.policy.require_digit and not re.search(r'\d', password):
            errors.append("密码必须包含数字")

        if self.policy.require_special:
            special_pattern = f"[{re.escape(self.policy.special_chars)}]"
            if not re.search(special_pattern, password):
                errors.append(f"密码必须包含特殊字符 ({self.policy.special_chars})")

        return len(errors) == 0, errors

# 使用示例
policy = PasswordPolicy(
    min_length=8,
    require_uppercase=True,
    require_digit=True,
    require_special=True
)
validator = PasswordValidator(policy)

is_valid, errors = validator.validate("MyPass123!")
print(f"有效: {is_valid}")
print(f"错误: {errors}")
```

---

## Part 4: RBAC 权限模型

### 4.1 RBAC 核心概念

```
┌─────────────────────────────────────────────────────────────┐
│                        RBAC 模型                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐     ┌─────────┐     ┌─────────────┐       │
│   │   User  │────→│   Role  │←────│  Permission  │       │
│   └─────────┘     └─────────┘     └─────────────┘       │
│        │                │                   │                 │
│        │                │                   │                 │
│        ↓                ↓                   ↓                 │
│   用户角色映射      角色权限映射        具体权限              │
│   user_id,role_id   role_id,perm_id    resource+action    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**核心关系**：
- User ↔ Role: 多对多（一个用户可以有多个角色）
- Role ↔ Permission: 多对多（一个角色可以有多个权限）

### 4.2 RBAC 完整实现

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from functools import wraps

class PermissionAction(Enum):
    """权限动作"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

@dataclass
class Permission:
    """权限定义"""
    resource: str      # 资源名称
    action: PermissionAction  # 操作类型

    def __str__(self) -> str:
        return f"{self.resource}:{self.action.value}"

    @classmethod
    def from_string(cls, s: str) -> "Permission":
        """从字符串解析权限"""
        resource, action = s.split(":")
        return cls(resource, PermissionAction(action))

class Role(str, Enum):
    """系统角色"""
    ADMIN = "admin"      # 管理员：所有权限
    MODERATOR = "moderator"  # 版主：部分管理权限
    USER = "user"        # 普通用户：基本操作
    GUEST = "guest"      # 访客：只读权限

@dataclass
class User:
    """用户模型"""
    id: str
    username: str
    password_hash: str
    roles: list[str] = field(default_factory=list)
    is_active: bool = True

class RBACSystem:
    """RBAC 权限控制系统"""

    # 角色权限定义（简化版）
    ROLE_PERMISSIONS: dict[str, list[Permission]] = {
        Role.ADMIN.value: [
            Permission("*", PermissionAction.ADMIN),  # 所有权限
        ],
        Role.MODERATOR.value: [
            Permission("article", PermissionAction.READ),
            Permission("article", PermissionAction.WRITE),
            Permission("comment", PermissionAction.DELETE),
            Permission("user", PermissionAction.READ),
        ],
        Role.USER.value: [
            Permission("article", PermissionAction.READ),
            Permission("article", PermissionAction.WRITE),
            Permission("comment", PermissionAction.READ),
            Permission("comment", PermissionAction.WRITE),
            Permission("comment", PermissionAction.DELETE),
        ],
        Role.GUEST.value: [
            Permission("article", PermissionAction.READ),
            Permission("comment", PermissionAction.READ),
        ],
    }

    @classmethod
    def get_role_permissions(cls, role: str) -> list[Permission]:
        """获取角色的所有权限"""
        return cls.ROLE_PERMISSIONS.get(role, [])

    @classmethod
    def get_user_permissions(cls, user: User) -> set[str]:
        """获取用户的所有权限（合并所有角色）"""
        permissions = set()
        for role in user.roles:
            for perm in cls.get_role_permissions(role):
                permissions.add(str(perm))
        return permissions

    @classmethod
    def has_permission(
        cls,
        user: User,
        resource: str,
        action: PermissionAction
    ) -> bool:
        """检查用户是否拥有指定权限"""
        if not user.is_active:
            return False

        for role in user.roles:
            perms = cls.get_role_permissions(role)
            for perm in perms:
                # 管理员权限（*）
                if perm.resource == "*" and perm.action == PermissionAction.ADMIN:
                    return True
                # 资源匹配
                if perm.resource == resource and perm.action == action:
                    return True
                # 通配符资源
                if perm.resource == "*" and perm.action == action:
                    return True

        return False

    @classmethod
    def require_permission(
        cls,
        resource: str,
        action: PermissionAction
    ):
        """权限检查装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(user: User, *args, **kwargs):
                if not cls.has_permission(user, resource, action):
                    raise PermissionError(
                        f"权限不足：需要 {action.value} {resource}"
                    )
                return func(user, *args, **kwargs)
            return wrapper
        return decorator
```

### 4.3 数据库 RBAC 实现

```python
from typing import Optional
import sqlite3
from contextlib import contextmanager

@dataclass
class DBRole:
    id: int
    name: str
    description: str

@dataclass
class DBPermission:
    id: int
    resource: str
    action: str

@dataclass
class DBUser:
    id: int
    username: str
    password_hash: str
    is_active: bool

class DatabaseRBAC:
    """数据库版 RBAC 实现"""

    def __init__(self, db_path: str = "rbac.db"):
        self.db_path = db_path
        self._init_database()

    @contextmanager
    def _get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_database(self):
        """初始化数据库表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 用户表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1
                )
            """)

            # 角色表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT
                )
            """)

            # 权限表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS permissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resource TEXT NOT NULL,
                    action TEXT NOT NULL,
                    UNIQUE(resource, action)
                )
            """)

            # 用户角色关联表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_roles (
                    user_id INTEGER,
                    role_id INTEGER,
                    PRIMARY KEY (user_id, role_id),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (role_id) REFERENCES roles(id)
                )
            """)

            # 角色权限关联表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS role_permissions (
                    role_id INTEGER,
                    permission_id INTEGER,
                    PRIMARY KEY (role_id, permission_id),
                    FOREIGN KEY (role_id) REFERENCES roles(id),
                    FOREIGN KEY (permission_id) REFERENCES permissions(id)
                )
            """)

    def assign_role(self, user_id: int, role_name: str):
        """为用户分配角色"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO roles (name) VALUES (?)
            """, (role_name,))
            cursor.execute("""
                INSERT OR IGNORE INTO user_roles
                SELECT ?, id FROM roles WHERE name = ?
            """, (user_id, role_name))

    def check_permission(
        self,
        user_id: int,
        resource: str,
        action: str
    ) -> bool:
        """检查用户权限"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM user_roles ur
                JOIN roles r ON ur.role_id = r.id
                JOIN role_permissions rp ON r.id = rp.role_id
                JOIN permissions p ON rp.permission_id = p.id
                WHERE ur.user_id = ?
                  AND (p.resource = ? OR p.resource = '*')
                  AND (p.action = ? OR p.action = 'admin')
            """, (user_id, resource, action))
            return cursor.fetchone()[0] > 0
```

### 4.4 FastAPI 权限依赖

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

security = HTTPBearer()

class AuthDeps:
    """认证依赖"""

    def __init__(self, jwt_auth: JWTAuth, rbac: DatabaseRBAC):
        self.jwt_auth = jwt_auth
        self.rbac = rbac

    async def get_current_user(
        self,
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
    ) -> User:
        """获取当前用户（需要登录）"""
        token = credentials.credentials
        payload = self.jwt_auth.verify_access_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效或已过期的 Token"
            )

        # 从数据库获取用户
        user = self._get_user_by_id(payload["sub"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在"
            )

        return user

    def require_role(self, *roles: str):
        """角色检查依赖工厂"""
        async def role_checker(
            user: Annotated[User, Depends(self.get_current_user)]
        ) -> User:
            if not any(role in user.roles for role in roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"需要角色之一: {', '.join(roles)}"
                )
            return user
        return role_checker

    def require_permission(self, resource: str, action: str):
        """权限检查依赖工厂"""
        async def permission_checker(
            user: Annotated[User, Depends(self.get_current_user)]
        ) -> User:
            if not self.rbac.check_permission(user.id, resource, action):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"需要 {action}:{resource} 权限"
                )
            return user
        return permission_checker


# 使用示例
auth = AuthDeps(jwt_auth, rbac)

@app.get("/users")
async def list_users(
    user: Annotated[User, Depends(auth.require_role("admin", "moderator"))]
):
    """列出所有用户（需要 admin 或 moderator 角色）"""
    return {"users": [...]}

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    user: Annotated[User, Depends(auth.require_permission("user", "delete"))]
):
    """删除用户（需要 user:delete 权限）"""
    ...
```

---

## Part 5: OAuth2 授权码流程

### 5.1 OAuth2 四种授权模式

| 模式 | 适用场景 | 安全性 | 复杂度 |
|------|----------|--------|--------|
| **Authorization Code** | 服务端渲染 Web 应用 | ⭐⭐⭐⭐⭐ | 中 |
| **PKCE** | SPA/移动 App | ⭐⭐⭐⭐⭐ | 中 |
| **Client Credentials** | 服务间通信 | ⭐⭐⭐⭐ | 低 |
| **Refresh Token** | Token 续期 | ⭐⭐⭐⭐ | 低 |

### 5.2 Authorization Code 流程详解

```
┌─────────┐                    ┌──────────┐                    ┌──────────┐
│   User  │                    │  Client   │                    │   Auth  │
│  Browser│                    │   App     │                    │  Server │
└────┬────┘                    └─────┬─────┘                    └────┬────┘
     │                              │                               │
     │  1.点击"用GitHub登录"         │                               │
     │─────────────────────────────→│                               │
     │                              │                               │
     │  2.重定向到授权页面           │                               │
     │←─────────────────────────────│                               │
     │  ?client_id=xxx&redirect_uri=│                               │
     │   xxx&scope=read:user       │                               │
     │─────────────────────────────→│                               │
     │                              │                               │
     │  3.用户授权                  │                               │
     │─────────────────────────────→│                               │
     │                              │                               │
     │  4.回调携带授权码             │                               │
     │←─────────────────────────────│                               │
     │  ?code=authorization_code     │                               │
     │                              │                               │
     │                              │  5.用授权码换Token             │
     │                              │─────────────────────────────→│
     │                              │                               │
     │                              │  6.返回Access Token           │
     │                              │←─────────────────────────────│
     │                              │                               │
     │                              │  7.用Token获取用户信息         │
     │                              │─────────────────────────────→│
     │                              │                               │
     │                              │  8.返回用户信息               │
     │                              │←─────────────────────────────│
     │                              │                               │
     │  9.登录成功                  │                               │
     │←─────────────────────────────│                               │
```

### 5.3 OAuth2 完整实现

```python
import httpx
import secrets
from urllib.parse import urlencode
from typing import Optional
from dataclasses import dataclass

@dataclass
class OAuth2Config:
    """OAuth2 配置"""
    client_id: str
    client_secret: str
    authorize_url: str
    token_url: str
    redirect_uri: str
    scope: str

@dataclass
class OAuth2Token:
    """OAuth2 Token 响应"""
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str]
    scope: str

class OAuth2Provider:
    """OAuth2 提供者基类"""

    def __init__(self, config: OAuth2Config):
        self.config = config
        self._state: dict[str, str] = {}  # state -> original_url

    def get_authorize_url(self, state: Optional[str] = None) -> tuple[str, str]:
        """
        获取授权 URL

        Returns:
            (授权 URL, state)
        """
        # 生成 state 防止 CSRF
        if not state:
            state = secrets.token_urlsafe(32)

        # 保存 state
        self._state[state] = self.config.redirect_uri

        params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "response_type": "code",
            "scope": self.config.scope,
            "state": state,
        }
        return f"{self.config.authorize_url}?{urlencode(params)}", state

    async def exchange_code(self, code: str, state: str) -> Optional[OAuth2Token]:
        """
        用授权码换取 Token

        Args:
            code: 授权码
            state: 状态参数

        Returns:
            Token 响应或 None
        """
        # 验证 state
        if state not in self._state:
            return None
        del self._state[state]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config.token_url,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self.config.client_id,
                    "client_secret": self.config.client_secret,
                    "code": code,
                    "redirect_uri": self.config.redirect_uri,
                }
            )

            if response.status_code != 200:
                return None

            data = response.json()
            return OAuth2Token(
                access_token=data["access_token"],
                token_type=data.get("token_type", "Bearer"),
                expires_in=data.get("expires_in", 3600),
                refresh_token=data.get("refresh_token"),
                scope=data.get("scope", ""),
            )

    async def get_user_info(self, token: OAuth2Token) -> dict:
        """
        获取用户信息（需要子类实现）

        Args:
            token: OAuth2 Token

        Returns:
            用户信息字典
        """
        raise NotImplementedError


class GitHubOAuth2(OAuth2Provider):
    """GitHub OAuth2 实现"""

    USER_INFO_URL = "https://api.github.com/user"

    def __init__(self, client_id: str, client_secret: str):
        super().__init__(OAuth2Config(
            client_id=client_id,
            client_secret=client_secret,
            authorize_url="https://github.com/login/oauth/authorize",
            token_url="https://github.com/login/oauth/access_token",
            redirect_uri="http://localhost:8000/auth/github/callback",
            scope="read:user user:email",
        ))

    async def get_user_info(self, token: OAuth2Token) -> dict:
        """获取 GitHub 用户信息"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.USER_INFO_URL,
                headers={
                    "Authorization": f"token {token.access_token}",
                    "Accept": "application/json",
                }
            )

            if response.status_code != 200:
                return {}

            return response.json()


# FastAPI OAuth2 路由
from fastapi import APIRouter, Query, HTTPException
from starlette.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["认证"])

github_oauth = GitHubOAuth2(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

@router.get("/github/login")
async def github_login():
    """GitHub OAuth2 登录入口"""
    url, state = github_oauth.get_authorize_url()
    return RedirectResponse(url)

@router.get("/github/callback")
async def github_callback(
    code: str = Query(...),
    state: str = Query(...)
):
    """GitHub OAuth2 回调"""
    token = await github_oauth.exchange_code(code, state)
    if not token:
        raise HTTPException(status_code=400, detail="授权失败")

    # 获取用户信息
    user_info = await github_oauth.get_user_info(token)

    # 创建或更新本地用户
    user = await create_or_update_user(
        provider="github",
        provider_id=str(user_info["id"]),
        username=user_info.get("login"),
        email=user_info.get("email"),
    )

    # 签发本地 JWT
    jwt_tokens = jwt_auth.create_tokens(
        user_id=str(user.id),
        username=user.username,
        roles=["user"]
    )

    return jwt_tokens
```

---

## Part 6: 实战项目 - 用户认证系统

### 6.1 项目结构

```
auth_project/
├── main.py                      # FastAPI 应用入口
├── auth/
│   ├── __init__.py
│   ├── jwt_auth.py             # JWT 认证模块
│   ├── password.py              # 密码管理模块
│   ├── rbac.py                  # RBAC 权限模块
│   ├── oauth2.py               # OAuth2 模块
│   └── dependencies.py          # FastAPI 依赖
├── models/
│   ├── __init__.py
│   ├── user.py                 # 用户模型
│   └── token.py                # Token 模型
├── schemas/
│   ├── __init__.py
│   ├── user.py                 # Pydantic schemas
│   └── auth.py                 # 认证 schemas
├── routers/
│   ├── __init__.py
│   ├── auth.py                 # 认证路由
│   └── users.py                # 用户路由
├── database/
│   ├── __init__.py
│   └── connection.py           # 数据库连接
└── tests/
    ├── __init__.py
    ├── test_auth.py
    └── test_rbac.py
```

### 6.2 完整代码实现

#### main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users
from database import engine, Base

app = FastAPI(
    title="用户认证系统",
    description="完整的 JWT + RBAC + OAuth2 认证授权系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "用户认证系统 API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

#### schemas/user.py

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """用户基础 schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    """用户注册"""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """用户更新"""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """用户响应"""
    id: int
    is_active: bool
    roles: list[str]
    created_at: datetime

    class Config:
        from_attributes = True

class UserInDB(UserBase):
    """数据库用户"""
    id: int
    password_hash: str
    is_active: bool
    roles: list[str]
```

#### schemas/auth.py

```python
from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str

class TokenResponse(BaseModel):
    """Token 响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    """刷新 Token 请求"""
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str
    new_password: str = Field(..., min_length=8)

class RoleAssignRequest(BaseModel):
    """分配角色请求"""
    user_id: int
    role: str
```

#### dependencies.py

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from auth.jwt_auth import JWTAuth
from auth.rbac import RBACSystem
from models.user import User, UserInDB
from database import get_user_by_id

security = HTTPBearer()
jwt_auth = JWTAuth()
rbac = RBACSystem()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> UserInDB:
    """获取当前登录用户"""
    token = credentials.credentials
    payload = jwt_auth.verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效或已过期的 Token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    return user

def require_roles(*roles: str):
    """角色要求依赖"""
    async def checker(
        user: Annotated[UserInDB, Depends(get_current_user)]
    ) -> UserInDB:
        if not any(role in user.roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要角色之一: {', '.join(roles)}"
            )
        return user
    return checker
```

#### routers/auth.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from database import get_user_by_username, create_user, update_user
from schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from schemas.user import UserCreate, UserResponse
from auth.password import PasswordManager
from auth.jwt_auth import JWTAuth
from auth.rbac import RBACSystem
from dependencies import get_current_user, require_roles
from models.user import UserInDB

router = APIRouter(prefix="/auth", tags=["认证"])
password_mgr = PasswordManager()
jwt_auth = JWTAuth()

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """用户注册"""
    # 检查用户名是否已存在
    existing = get_user_by_username(user_data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 创建用户
    password_hash = password_mgr.hash_password(user_data.password)
    user = create_user(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        roles=["user"]
    )

    # 签发 Token
    tokens = jwt_auth.create_tokens(
        user_id=str(user.id),
        username=user.username,
        roles=user.roles
    )

    return tokens

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """用户登录"""
    user = get_user_by_username(credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 验证密码
    if not password_mgr.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 检查用户状态
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )

    # 签发 Token
    tokens = jwt_auth.create_tokens(
        user_id=str(user.id),
        username=user.username,
        roles=user.roles
    )

    return tokens

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshRequest):
    """刷新 Token"""
    new_tokens = jwt_auth.refresh_access_token(request.refresh_token)
    if not new_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新 Token"
        )
    return new_tokens

@router.post("/logout")
async def logout(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)]
):
    """用户登出"""
    jwt_auth.revoke_token(credentials.credentials)
    return {"message": "登出成功"}

@router.post("/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: Annotated[UserInDB, Depends(get_current_user)]
):
    """修改密码"""
    # 验证旧密码
    if not password_mgr.verify_password(old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )

    # 更新密码
    new_hash = password_mgr.hash_password(new_password)
    update_user(current_user.id, password_hash=new_hash)

    return {"message": "密码修改成功"}
```

#### routers/users.py

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, list
from schemas.user import UserResponse, UserUpdate, RoleAssignRequest
from models.user import UserInDB
from database import get_user_by_id, list_users, update_user
from dependencies import get_current_user, require_roles
from auth.rbac import RBACSystem

router = APIRouter(prefix="/users", tags=["用户"])
rbac = RBACSystem()

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
):
    """获取当前用户信息"""
    return current_user

@router.get("/", response_model=list[UserResponse])
async def list_all_users(
    _: Annotated[UserInDB, Depends(require_roles("admin", "moderator"))]
):
    """列出所有用户（需要管理员或版主）"""
    users = list_users()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: Annotated[UserInDB, Depends(get_current_user)]
):
    """获取指定用户"""
    # 可以查看自己，或管理员查看任何人
    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="权限不足")

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return user

@router.patch("/{user_id}")
async def update_user_info(
    user_id: int,
    data: UserUpdate,
    current_user: Annotated[UserInDB, Depends(get_current_user)]
):
    """更新用户信息"""
    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="权限不足")

    # 构建更新数据
    update_data = {}
    if data.email:
        update_data["email"] = data.email
    if data.password:
        from auth.password import PasswordManager
        password_mgr = PasswordManager()
        update_data["password_hash"] = password_mgr.hash_password(data.password)
    if data.is_active is not None:
        update_data["is_active"] = data.is_active

    if update_data:
        update_user(user_id, **update_data)

    return {"message": "更新成功"}

@router.post("/roles")
async def assign_role(
    request: RoleAssignRequest,
    _: Annotated[UserInDB, Depends(require_roles("admin"))]
):
    """分配角色（仅管理员）"""
    rbac.assign_role(request.user_id, request.role)
    return {"message": f"已为用户 {request.user_id} 分配角色 {request.role}"}
```

---

## Part 7: 安全最佳实践总结

### 7.1 认证安全检查清单

| 检查项 | 要求 | 重要程度 |
|--------|------|----------|
| 密码哈希 | 使用 bcrypt 或 argon2 | 🔴 必选 |
| Token 过期 | Access Token < 1小时 | 🔴 必选 |
| HTTPS | 生产环境必须使用 | 🔴 必选 |
| 强密钥 | 至少 256 位随机密钥 | 🔴 必选 |
| Token 黑名单 | 实现 Token 注销机制 | 🟠 推荐 |
| 刷新 Token | 实现 Token 续期 | 🟠 推荐 |
| 登录限流 | 防止暴力破解 | 🟠 推荐 |
| 审计日志 | 记录登录行为 | 🟡 建议 |

### 7.2 常见安全漏洞与防御

```python
# ❌ 漏洞 1：使用弱哈希算法
import hashlib
def bad_hash(password):
    return hashlib.md5(password.encode()).hexdigest()  # 不安全！

# ✅ 防御：使用 bcrypt
def good_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ❌ 漏洞 2：Token 永不过期
def create_unsafe_token(user_id):
    return jwt.encode({"sub": user_id}, secret)  # 没有 exp！

# ✅ 防御：设置过期时间
def create_safe_token(user_id):
    return jwt.encode({
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + timedelta(hours=1)
    }, secret)

# ❌ 漏洞 3：敏感信息放 Token
def bad_token(user):
    return jwt.encode({
        "sub": user.id,
        "password": user.password  # 危险！
    }, secret)

# ✅ 防御：只放必要信息
def good_token(user):
    return jwt.encode({
        "sub": user.id,
        "roles": user.roles
    }, secret)
```

---

## 📝 课程总结

### 核心知识点

1. **认证与授权区别**
   - 认证：验证"你是谁"
   - 授权：验证"你能做什么"

2. **JWT 实现要点**
   - Token 结构：Header + Payload + Signature
   - 签发与验证
   - 刷新机制
   - 黑名单管理

3. **密码安全**
   - bcrypt/argon2 哈希
   - 盐值处理
   - 密码策略验证

4. **RBAC 权限模型**
   - User ↔ Role ↔ Permission
   - 角色权限配置
   - FastAPI 依赖注入

5. **OAuth2 授权码流程**
   - 授权码交换
   - Token 获取
   - 用户信息获取

### 关键要点

- ✅ 使用 JWT 实现无状态认证
- ✅ 密码必须使用 bcrypt/argon2 哈希存储
- ✅ Token 必须设置合理的过期时间
- ✅ 使用 RBAC 实现细粒度权限控制
- ✅ 生产环境必须使用 HTTPS
- ✅ 实现 Token 黑名单支持登出

---

## 🚀 扩展话题

### 进阶话题预告

- **LDAP/Active Directory 集成**：企业用户认证
- **SAML 2.0**：企业级 SSO
- **OpenID Connect (OIDC)**：现代身份协议
- **零信任架构**：持续验证原则

---

## 📚 扩展阅读

- [JWT 官方文档](https://jwt.io/)
- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [bcrypt 官方文档](https://pypi.org/project/bcrypt/)
- [Passlib 文档](https://passlib.readthedocs.io/)

---

## ✅ 完成标准

完成本课程后，你应该能够：

- [ ] 理解认证与授权的区别
- [ ] 能实现 JWT Token 的创建、验证、刷新
- [ ] 能设计 RBAC 权限模型并实现
- [ ] 理解 OAuth2 授权码流程
- [ ] 实现完整的用户认证系统
- [ ] 理解密码安全最佳实践
- [ ] 在 FastAPI 中实现认证中间件
- [ ] 测试用例全部通过

---

**下一步**: 继续学习 [L39: E2E 测试工程化](../L39-e2e-testing/lesson.md)，将认证系统纳入端到端测试覆盖。
