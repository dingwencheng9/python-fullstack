"""P05 示例 1: 项目结构与配置

⚠️ 安全警告：此文件中的配置仅用于教学演示。
生产环境必须通过环境变量或密钥管理服务（如 AWS Secrets Manager、HashiCorp Vault）管理敏感配置。
"""

from __future__ import annotations

import os


def _get_env(key: str, default: str, required: bool = False) -> str:
    """从环境变量获取配置（生产级模式）"""
    value = os.environ.get(key, default)
    if required and not value:
        raise ValueError(f"必须设置环境变量: {key}")
    return value


# ============ 配置管理 ============

class Config:
    """应用配置 - 参考 L44 配置管理

    ⚠️ 注意：所有敏感配置必须通过环境变量设置。
    示例：
        DATABASE_URL = os.environ["DATABASE_URL"]
        SECRET_KEY = os.environ["SECRET_KEY"]
    """

    # 数据库配置（使用环境变量）
    DATABASE_URL: str = _get_env(
        "DATABASE_URL",
        "postgresql+asyncpg://user:pass@localhost:5432/taskcollab"
    )
    REDIS_URL: str = _get_env("REDIS_URL", "redis://localhost:6379")

    # JWT 配置（敏感 - 必须设置环境变量）
    SECRET_KEY: str = _get_env(
        "JWT_SECRET_KEY",
        "change-me-in-production",
        required=True
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    # Celery
    CELERY_BROKER_URL: str = _get_env("CELERY_BROKER_URL", "redis://localhost:6379")
    CELERY_RESULT_BACKEND: str = _get_env("CELERY_RESULT_BACKEND", "redis://localhost:6379")

    # Cache TTL
    CACHE_TTL_SHORT: int = 60  # 1 分钟
    CACHE_TTL_MEDIUM: int = 300  # 5 分钟
    CACHE_TTL_LONG: int = 3600  # 1 小时


config = Config()

# ============ 数据模型示例 ============

class UserRole:
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    VIEWER = "viewer"


class TaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


def demonstrate_project_structure():
    """演示项目结构"""
    print("=" * 60)
    print("TaskCollab - 实时协作 SaaS 平台")
    print("=" * 60)

    print("\n📁 项目目录结构:")
    print("""
    P05-realtime-collaboration/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py              # FastAPI 应用入口
    │   ├── config.py             # 配置管理
    │   ├── dependencies.py       # 依赖注入
    │   ├── models/               # SQLAlchemy 模型
    │   │   ├── user.py
    │   │   ├── task.py
    │   │   └── team.py
    │   ├── schemas/             # Pydantic schemas
    │   │   ├── auth.py
    │   │   ├── task.py
    │   │   └── websocket.py
    │   ├── api/                 # API 路由
    │   │   ├── auth.py
    │   │   ├── tasks.py
    │   │   └── websocket.py
    │   ├── services/            # 业务逻辑
    │   │   ├── auth.py
    │   │   ├── task.py
    │   │   └── notification.py
    │   ├── core/                # 核心模块
    │   │   ├── security.py      # 安全工具
    │   │   ├── websocket.py     # WebSocket 管理
    │   │   └── redis.py        # Redis 客户端
    │   └── celery_app/          # Celery 配置
    │       └── tasks.py
    ├── tests/
    ├── docker-compose.yml
    └── pyproject.toml
    """)

    print("\n⚙️ 配置参数:")
    print(f"  DATABASE_URL: {config.DATABASE_URL}")
    print(f"  REDIS_URL: {config.REDIS_URL}")
    print(f"  RATE_LIMIT: {config.RATE_LIMIT_REQUESTS} req/{config.RATE_LIMIT_WINDOW}s")

    print("\n👥 角色权限:")
    print("  ADMIN: 完全访问")
    print("  MANAGER: 团队管理")
    print("  MEMBER: 任务操作")
    print("  VIEWER: 只读访问")

    print("\n📊 任务状态:")
    print("  PENDING: 待处理")
    print("  IN_PROGRESS: 进行中")
    print("  COMPLETED: 已完成")
    print("  CANCELLED: 已取消")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_project_structure()
