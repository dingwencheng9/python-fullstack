# L35: Web 基础综合项目

> **课程编号**: L35
> **所属阶段**: Stage 3 - Web 开发基础
> **预计时长**: 10-12 小时
> **难度**: ⭐⭐⭐⭐⭐（高级）
> **前置课程**: L26, L27, L28, L31
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ **整合知识**：综合运用 HTTP、FastAPI、SQL、认证、SSE、WebSocket、HTMX
2. ✅ **项目架构**：设计清晰的分层项目结构
3. ✅ **API 开发**：构建完整的 RESTful API 系统
4. ✅ **数据库操作**：使用 SQLAlchemy 2.0 实现 CRUD
5. ✅ **用户认证**：实现 JWT 认证和授权
6. ✅ **实时通信**：集成 SSE 和 WebSocket
7. ✅ **前端交互**：使用 HTMX 实现动态交互
8. ✅ **容器部署**：Docker 容器化部署

---

## 📚 项目概述

### 项目：TaskFlow 任务管理系统

一个完整的任务管理 RESTful API 系统：

```
┌─────────────────────────────────────────────────────────┐
│                  TaskFlow 架构                         │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │  HTMX   │  │  REST   │  │  SSE    │            │
│  │  前端   │  │   API   │  │  实时   │            │
│  └────┬────┘  └────┬────┘  └────┬────┘            │
│       │            │            │                   │
│       └────────────┴────────────┘                   │
│                    │                                 │
│              ┌─────▼─────┐                           │
│              │  FastAPI  │                           │
│              │   服务    │                           │
│              └─────┬─────┘                           │
│                    │                                 │
│              ┌─────▼─────┐                           │
│              │ SQLAlchemy │                          │
│              │   ORM      │                          │
│              └─────┬─────┘                           │
│                    │                                 │
│              ┌─────▼─────┐                           │
│              │ PostgreSQL│                           │
│              │  数据库    │                           │
│              └───────────┘                           │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

### 功能列表

| 功能 | 技术实现 | 优先级 |
|------|---------|--------|
| 用户注册/登录 | JWT Bearer Token | P0 |
| 任务 CRUD | RESTful API + SQLAlchemy | P0 |
| 任务分类 | 标签系统 | P1 |
| 实时通知 | Server-Sent Events | P1 |
| 在线状态 | WebSocket 心跳 | P2 |
| 权限控制 | RBAC 权限模型 | P1 |
| 容器化部署 | Docker + Docker Compose | P1 |

### 技术栈

```
后端: FastAPI + Pydantic V2 + SQLAlchemy 2.0
数据库: SQLite (开发) / PostgreSQL (生产)
实时: SSE + WebSocket
前端: HTMX + TailwindCSS
认证: Python-Jose (JWT)
容器: Docker + Docker Compose
测试: pytest + httpx + pytest-asyncio
```

---

## Part 1: 项目初始化

### 1.1 创建项目结构

```bash
# 创建项目目录
mkdir -p L35-web-project
cd L35-web-project

# 创建目录结构
mkdir -p app/{api,core,models,schemas,services}
mkdir -p app/api/endpoints
mkdir -p tests
mkdir -p docker

# 创建 __init__.py
touch app/__init__.py
touch app/api/__init__.py
touch app/api/endpoints/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch tests/__init__.py

# 查看结构
tree -L 3 app/
```

### 1.2 配置 pyproject.toml

```toml
# pyproject.toml
[project]
name = "taskflow"
version = "1.0.0"
description = "TaskFlow - 任务管理系统"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.14.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.20",
    "aiosqlite>=0.20.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.25.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.8.0",
    "mypy>=1.14.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.mypy]
python_version = "3.13"
strict = true
```

### 1.3 配置管理

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""

    # 应用信息
    app_name: str = "TaskFlow"
    debug: bool = False

    # 数据库
    database_url: str = "sqlite+aiosqlite:///./taskflow.db"

    # JWT 配置
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    """获取配置（单例）"""
    return Settings()
```

### 1.4 数据库连接

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

settings = get_settings()

# 创建异步引擎
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

# 创建会话工厂
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    pass

async def get_db() -> AsyncSession:
    """获取数据库会话"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """初始化数据库（创建所有表）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

### 1.5 FastAPI 应用入口

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.database import init_db
from app.api.endpoints import users, tasks, auth, events

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    # 启动时
    await init_db()
    print(f"✅ {settings.app_name} 已启动")
    yield
    # 关闭时
    print(f"👋 {settings.app_name} 已关闭")

app = FastAPI(
    title=settings.app_name,
    description="任务管理系统 API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["任务"])
app.include_router(events.router, prefix="/api/events", tags=["实时事件"])

@app.get("/")
async def root():
    return {"message": f"欢迎使用 {settings.app_name}"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

---

## Part 2: 数据模型

### 2.1 用户模型

```python
# app/models/user.py
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.core.database import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # 关系
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner")

    def __repr__(self) -> str:
        return f"<User {self.username}>"
```

### 2.2 任务模型

```python
# app/models/task.py
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.core.database import Base

class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    # 外键
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # 关系
    owner: Mapped["User"] = relationship("User", back_populates="tasks")
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="task_tags",
        back_populates="tasks"
    )

    def __repr__(self) -> str:
        return f"<Task {self.title}>"


class Tag(Base):
    """标签模型"""
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    color: Mapped[str] = mapped_column(String(7), default="#3B82F6")

    # 关系
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="task_tags",
        back_populates="tags"
    )


# 关联表
from sqlalchemy import Table, Column, Integer

task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
```

### 2.3 模型导出

```python
# app/models/__init__.py
from app.models.user import User
from app.models.task import Task, Tag, task_tags

__all__ = ["User", "Task", "Tag", "task_tags"]
```

---

## Part 3: Pydantic Schemas

### 3.1 用户 Schemas

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """用户基础 schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    """用户创建"""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """用户更新"""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase):
    """用户响应"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserBase):
    """数据库用户（包含密码哈希）"""
    id: int
    password_hash: str
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

### 3.2 任务 Schemas

```python
# app/schemas/task.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class TagBase(BaseModel):
    """标签基础"""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$")

class TagCreate(TagBase):
    """标签创建"""
    pass

class TagResponse(TagBase):
    """标签响应"""
    id: int

    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    """任务基础"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    """任务创建"""
    tag_ids: Optional[list[int]] = []

class TaskUpdate(BaseModel):
    """任务更新"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    tag_ids: Optional[list[int]] = None

class TaskResponse(TaskBase):
    """任务响应"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)

class TaskListResponse(BaseModel):
    """任务列表响应"""
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    pages: int
```

---

## Part 4: 安全与认证

### 4.1 密码工具

```python
# app/core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)
```

### 4.2 JWT 工具

```python
# app/core/jwt.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """验证令牌"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None
```

### 4.3 依赖注入

```python
# app/api/deps.py
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated, Optional

from app.core.database import get_db
from app.core.jwt import verify_token
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """获取当前用户"""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
        )

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    return user

async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """获取当前超级用户"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限",
        )
    return current_user
```

---

## Part 5: API 路由

### 5.1 认证路由

```python
# app/api/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash
from app.core.jwt import create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserBase
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """用户注册"""
    # 检查用户名是否存在
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )

    # 检查邮箱是否存在
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册",
        )

    # 创建用户
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

@router.post("/login")
async def login(
    username: str,
    password: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """用户登录"""
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    # 创建访问令牌
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    """获取当前用户信息"""
    return current_user
```

### 5.2 任务路由

```python
# app/api/endpoints/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Annotated

from app.core.database import get_db
from app.models.user import User
from app.models.task import Task, Tag
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    completed: bool = Query(None),
    search: str = Query(None),
):
    """获取任务列表"""
    # 构建查询
    query = select(Task).where(Task.user_id == current_user.id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    if search:
        query = query.where(Task.title.ilike(f"%{search}%"))

    # 统计总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # 分页
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(Task.created_at.desc())

    result = await db.execute(query)
    tasks = result.scalars().all()

    return TaskListResponse(
        items=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """创建任务"""
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=current_user.id,
    )

    # 添加标签
    if task_data.tag_ids:
        result = await db.execute(
            select(Tag).where(Tag.id.in_(task_data.tag_ids))
        )
        tags = result.scalars().all()
        task.tags = list(tags)

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """获取单个任务"""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在",
        )

    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """更新任务"""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在",
        )

    # 更新字段
    update_data = task_data.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)

    for field, value in update_data.items():
        setattr(task, field, value)

    # 更新标签
    if tag_ids is not None:
        result = await db.execute(
            select(Tag).where(Tag.id.in_(tag_ids))
        )
        tags = result.scalars().all()
        task.tags = list(tags)

    await db.commit()
    await db.refresh(task)

    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """删除任务"""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在",
        )

    await db.delete(task)
    await db.commit()
```

### 5.3 用户路由

```python
# app/api/endpoints/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.api.deps import get_current_user, get_current_superuser

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def list_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(get_current_superuser)],
):
    """获取所有用户（仅管理员）"""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
```

### 5.4 SSE 事件路由

```python
# app/api/endpoints/events.py
import asyncio
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.database import get_db
from app.models.user import User
from app.models.task import Task
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/sse")
async def sse_events(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """SSE 实时事件流"""
    async def event_generator():
        last_check = 0

        while True:
            # 模拟实时事件
            import time
            current_time = int(time.time())

            if current_time > last_check:
                last_check = current_time
                yield f"data: {{'time': {current_time}, 'user': '{current_user.username}'}}\n\n"

            await asyncio.sleep(5)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
```

---

## Part 6: 前端 HTMX 集成

### 6.1 HTMX 模板

```html
<!-- app/templates/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TaskFlow - 任务管理</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-gray-800">TaskFlow</h1>
            <p class="text-gray-600">任务管理系统</p>
        </header>

        <!-- 登录表单 -->
        <div id="auth-section" class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
            <form hx-post="/api/auth/login" hx-target="#auth-section" hx-swap="innerHTML">
                <div class="mb-4">
                    <label class="block text-gray-700 mb-2">用户名</label>
                    <input type="text" name="username" required
                           class="w-full px-3 py-2 border rounded-lg">
                </div>
                <div class="mb-4">
                    <label class="block text-gray-700 mb-2">密码</label>
                    <input type="password" name="password" required
                           class="w-full px-3 py-2 border rounded-lg">
                </div>
                <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600">
                    登录
                </button>
            </form>
        </div>

        <!-- 任务列表 -->
        <div id="task-list" class="mt-8">
            <!-- HTMX 会动态加载任务列表 -->
        </div>
    </div>
</body>
</html>
```

---

## Part 7: Docker 部署

### 7.1 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# 安装依赖
COPY pyproject.toml .
RUN pip install uv && uv sync --frozen

# 复制代码
COPY app/ ./app/

# 环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7.2 Docker Compose

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://taskflow:taskflow@db:5432/taskflow
      - SECRET_KEY=your-secret-key-change-in-production
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ..:/app

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=taskflow
      - POSTGRES_PASSWORD=taskflow
      - POSTGRES_DB=taskflow
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U taskflow"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

---

## Part 8: 测试

### 8.1 测试配置

```python
# tests/conftest.py
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.database import Base, get_db

# 测试数据库
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session():
    """创建测试数据库会话"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest.fixture
async def client(db_session):
    """创建测试客户端"""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
```

### 8.2 认证测试

```python
# tests/test_auth.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """测试用户注册"""
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    """测试用户登录"""
    # 先注册
    await client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "testpassword123",
        },
    )

    # 登录
    response = await client.post(
        "/api/auth/login",
        params={"username": "loginuser", "password": "testpassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
```

### 8.3 任务测试

```python
# tests/test_tasks.py
import pytest
from httpx import AsyncClient

async def get_auth_token(client: AsyncClient) -> str:
    """获取认证令牌"""
    await client.post(
        "/api/auth/register",
        json={
            "username": "taskuser",
            "email": "task@example.com",
            "password": "testpassword123",
        },
    )
    response = await client.post(
        "/api/auth/login",
        params={"username": "taskuser", "password": "testpassword123"},
    )
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    """测试创建任务"""
    token = await get_auth_token(client)

    response = await client.post(
        "/api/tasks/",
        json={"title": "测试任务", "description": "测试描述"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试任务"
    assert data["completed"] is False

@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient):
    """测试获取任务列表"""
    token = await get_auth_token(client)

    # 创建任务
    await client.post(
        "/api/tasks/",
        json={"title": "任务1"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # 获取列表
    response = await client.get(
        "/api/tasks/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
```

---

## 📝 课程总结

### 核心知识点

1. **项目架构**：分层设计（API、Service、Model、Schema）
2. **异步开发**：SQLAlchemy 异步会话 + async/await
3. **认证授权**：JWT Token + 依赖注入
4. **RESTful API**：CRUD + 分页 + 过滤
5. **实时通信**：SSE 事件流
6. **容器化**：Docker + Docker Compose
7. **测试**：pytest + httpx 异步测试

### 项目亮点

| 亮点 | 说明 |
|------|------|
| 异步优先 | 全程使用 async/await |
| 类型安全 | Pydantic + SQLAlchemy 2.0 |
| 分层清晰 | API → Service → Model |
| 测试覆盖 | 认证、任务 CRUD |

---

## ✅ 完成标准

完成本课程后，你应该能够：

- [ ] 创建完整的 FastAPI 项目结构
- [ ] 使用 SQLAlchemy 2.0 定义数据模型
- [ ] 实现 JWT 认证系统
- [ ] 构建完整的 CRUD API
- [ ] 实现 SSE 实时通知
- [ ] 使用 HTMX 实现前端交互
- [ ] 使用 Docker 容器化部署
- [ ] 编写 pytest 异步测试

---

**下一步**: 继续学习 [L36: 异步背压与限流](../../../stage4-web-advanced/lessons/L36-async-backpressure/lesson.md)
