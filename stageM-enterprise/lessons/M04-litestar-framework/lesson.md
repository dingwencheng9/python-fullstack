# M04: Litestar 框架

> **课程编号**: M04
> **所属阶段**: Stage M - 企业级 AI 应用
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐ (中高级)
> **前置课程**: L27 (FastAPI 基础)、L37 (Web 安全)
> **状态**: 🟡 完善中
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **理解 Litestar**：掌握 Litestar 的设计理念和优势
2. **构建高性能 API**：使用 Litestar 构建生产级 API
3. **插件生态**：熟练使用 SQLAlchemy、Redis 等插件
4. **性能优化**：发挥 Litestar 的高性能特性

---

## 📚 课程内容

### 第一部分：Litestar 概述

#### 1.1 为什么选择 Litestar

```
Litestar vs FastAPI 对比：

| 特性          | Litestar      | FastAPI       |
|---------------|---------------|---------------|
| 性能          | ⭐⭐⭐⭐⭐       | ⭐⭐⭐⭐        |
| 类型安全      | ⭐⭐⭐⭐⭐       | ⭐⭐⭐⭐        |
| 插件生态      | ⭐⭐⭐⭐        | ⭐⭐⭐⭐⭐       |
| 社区规模      | ⭐⭐⭐         | ⭐⭐⭐⭐⭐       |
| 学习曲线      | 平缓          | 较陡          |
| 文档质量      | ⭐⭐⭐⭐⭐       | ⭐⭐⭐⭐        |

Litestar 优势：
- 内置依赖注入系统
- 更强的类型安全
- 更好的性能（基于 Starlette 优化）
- 清晰的插件架构
```

#### 1.2 Litestar 核心概念

```python
# Litestar 应用结构
from litestar import Litestar, get, post
from litestar.datastructures import State
from litestar.dto import DTO

# 路由
@get("/users/{user_id:int}")  # 类型化路径参数
async def get_user(user_id: int, state: State) -> dict:
    ...

# 请求体
@post("/users")
async def create_user(data: CreateUserDTO) -> UserDTO:
    ...

# 应用入口
app = Litestar(
    route_handlers=[get_user, create_user],
    dependencies={"db": provides_database},  # 依赖注入
    middleware=[...],  # 中间件
    plugins=[...],     # 插件
)
```

---

### 第二部分：基础 API 开发

#### 2.1 项目结构

```python
# my_app/
# ├── __init__.py
# ├── app.py           # 应用入口
# ├── config.py        # 配置
# ├── domain/          # 领域模块
# │   ├── __init__.py
# │   ├── user/
# │   │   ├── __init__.py
# │   │   ├── router.py
# │   │   ├── controller.py
# │   │   ├── service.py
# │   │   ├── repository.py
# │   │   └── dto.py
# │   └── product/
# └── lib/
#     ├── __init__.py
#     ├── database.py
#     └── cache.py
```

#### 2.2 第一个 Litestar 应用

```python
# app.py
from litestar import Litestar, get, post
from litestar.datastructures import State
from litestar.config.cors import CORSConfig
from pydantic import BaseModel
from typing import List, Optional

# DTO 定义
class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]

# 内存存储（演示用）
users_db: List[User] = []
user_id_counter = 1

# 路由处理
@get("/")
async def index() -> dict:
    return {"message": "Welcome to Litestar API", "version": "1.0.0"}

@get("/users")
async def list_users() -> List[User]:
    return users_db

@get("/users/{user_id:int}")
async def get_user(user_id: int) -> User:
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@post("/users")
async def create_user(data: UserCreate) -> User:
    global user_id_counter
    user = User(id=user_id_counter, **data.model_dump())
    users_db.append(user)
    user_id_counter += 1
    return user

@get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}

# 应用配置
from litestar import HTTPException

app = Litestar(
    route_handlers=[
        index,
        list_users,
        get_user,
        create_user,
        health_check
    ],
    cors_config=CORSConfig(
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    debug=True,
)

# 运行
# uvicorn app:app --reload
```

#### 2.3 依赖注入系统

```python
from litestar import get, Provide, Dependency
from contextlib import asynccontextmanager
from typing import AsyncGenerator

# 数据库连接管理器
class Database:
    def __init__(self):
        self.connected = False

    async def connect(self):
        self.connected = True
        print("Database connected")

    async def disconnect(self):
        self.connected = False
        print("Database disconnected")

# 依赖提供者
async def provide_db(state: "State") -> AsyncGenerator[Database, None]:
    """数据库依赖"""
    db = Database()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

async def provide_cache() -> dict:
    """缓存依赖"""
    return {"cache": {}}

# 带依赖的路由
@get("/users/{user_id:int}")
async def get_user_with_db(
    user_id: int,
    db: Database = Dependency(provider=provide_db),
    cache: dict = Dependency(provider=provide_cache)
) -> dict:
    """
    Litestar 的依赖注入：
    - 自动管理依赖生命周期
    - 支持异步和同步依赖
    - 依赖可以相互引用
    """
    # 先查缓存
    cache_key = f"user:{user_id}"
    if cache_key in cache.get("cache", {}):
        return cache["cache"][cache_key]

    # 查数据库
    user_data = {"id": user_id, "name": f"User {user_id}"}

    # 更新缓存
    cache.setdefault("cache", {})[cache_key] = user_data

    return user_data

# 应用配置
app = Litestar(
    route_handlers=[get_user_with_db],
    dependencies={"db": provide_db, "cache": provide_cache}
)
```

---

### 第三部分：SQLAlchemy 集成

#### 3.1 配置与模型

```python
# database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from litestar import Litestar
from contextlib import asynccontextmanager

# 数据库配置
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/mydb"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    pass

# 异步依赖
async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# 应用生命周期
@asynccontextmanager
async def app_lifespan(app: Litestar):
    # 启动时创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 关闭时清理
    await engine.dispose()
```

#### 3.2 模型定义

```python
# models.py
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional

from .database import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # 关系
    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="author", lazy="selectin"
    )

class Post(Base):
    """文章模型"""
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # 关系
    author: Mapped["User"] = relationship("User", back_populates="posts")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary="post_tags", back_populates="posts"
    )

class Tag(Base):
    """标签模型"""
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        "Post", secondary="post_tags", back_populates="tags"
    )

# 关联表
from sqlalchemy import Table, Column

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)
```

#### 3.3 Repository 模式

```python
# repository.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, TypeVar, Generic

from .database import Base
from .models import User, Post

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    """仓储基类"""

    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        result = await self.session.execute(
            select(self.model).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(self, id: int, **kwargs) -> Optional[T]:
        instance = await self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            await self.session.flush()
            await self.session.refresh(instance)
        return instance

    async def delete(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.flush()
            return True
        return False


class UserRepository(BaseRepository[User]):
    """用户仓储"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_with_posts(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.posts))
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def search_by_name(self, name_pattern: str) -> List[User]:
        result = await self.session.execute(
            select(User).where(User.name.ilike(f"%{name_pattern}%"))
        )
        return list(result.scalars().all())


class PostRepository(BaseRepository[Post]):
    """文章仓储"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Post)

    async def get_published(self, limit: int = 10) -> List[Post]:
        result = await self.session.execute(
            select(Post)
            .options(selectinload(Post.author))
            .where(Post.published == True)
            .order_by(Post.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_author(self, author_id: int) -> List[Post]:
        result = await self.session.execute(
            select(Post).where(Post.author_id == author_id)
        )
        return list(result.scalars().all())
```

#### 3.4 Service 层

```python
# service.py
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel

from .models import User, Post
from .repository import UserRepository, PostRepository

class CreatePostDTO(BaseModel):
    title: str
    content: str
    author_id: int
    published: bool = False

class PostService:
    """文章服务"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.post_repo = PostRepository(session)
        self.user_repo = UserRepository(session)

    async def create_post(self, data: CreatePostDTO) -> Post:
        """创建文章"""
        # 验证作者存在
        author = await self.user_repo.get_by_id(data.author_id)
        if not author:
            raise ValueError(f"Author with id {data.author_id} not found")

        return await self.post_repo.create(
            title=data.title,
            content=data.content,
            author_id=data.author_id,
            published=data.published
        )

    async def get_feed(self, limit: int = 10) -> List[Post]:
        """获取文章流"""
        return await self.post_repo.get_published(limit)

    async def publish_post(self, post_id: int) -> Optional[Post]:
        """发布文章"""
        return await self.post_repo.update(post_id, published=True)
```

---

### 第四部分：路由与控制器

#### 4.1 路由组织

```python
# domain/user/router.py
from litestar import Router, get, post, put, delete
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession

from .controller import UserController
from .service import UserService
from .repository import UserRepository

user_router = Router(
    path="/users",
    route_handlers=[UserController],
    dependencies={
        "service": Provide(lambda: UserService)
    }
)

# domain/product/router.py
product_router = Router(
    path="/products",
    route_handlers=[],  # 待实现
    dependencies={}
)
```

#### 4.2 控制器

```python
# domain/user/controller.py
from litestar import Controller, get, post, put, delete, Param
from litestar.dto import DTO
from typing import List
from pydantic import BaseModel, EmailStr

from .service import UserService

class CreateUserDTO(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None

class UpdateUserDTO(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None

class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    age: int | None

class UserController(Controller):
    """用户控制器"""

    path = "/users"

    @get()
    async def list_users(self, service: UserService) -> List[UserDTO]:
        """获取用户列表"""
        users = await service.get_all_users()
        return [UserDTO.model_validate(u) for u in users]

    @get("/{user_id:int}")
    async def get_user(
        self,
        user_id: int,
        service: UserService
    ) -> UserDTO:
        """获取单个用户"""
        user = await service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserDTO.model_validate(user)

    @post()
    async def create_user(
        self,
        data: CreateUserDTO,
        service: UserService
    ) -> UserDTO:
        """创建用户"""
        user = await service.create_user(data)
        return UserDTO.model_validate(user)

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_id: int,
        data: UpdateUserDTO,
        service: UserService
    ) -> UserDTO:
        """更新用户"""
        user = await service.update_user(user_id, data.model_dump(exclude_unset=True))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserDTO.model_validate(user)

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        user_id: int,
        service: UserService
    ) -> dict:
        """删除用户"""
        success = await service.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
```

---

### 第五部分：中间件与安全

#### 5.1 中间件

```python
from litestar import Litestar, Request, Response
from litestar.middleware.base import MiddlewareProtocol
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.gzip import GZipMiddleware
from typing import Callable

# 自定义中间件
class RequestLoggingMiddleware(MiddlewareProtocol):
    """请求日志中间件"""

    async def __call__(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        # 请求前处理
        import time
        start_time = time.time()

        print(f"→ {request.method} {request.url.path}")

        # 调用下一个处理器
        response = await call_next(request)

        # 请求后处理
        duration = time.time() - start_time
        print(f"← {request.method} {request.url.path} - {response.status_code} ({duration:.3f}s)")

        # 添加自定义响应头
        response.headers["X-Process-Time"] = str(duration)

        return response

class RateLimitMiddleware(MiddlewareProtocol):
    """限流中间件"""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    async def __call__(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # 清理过期记录
        self.requests = {
            ip: times
            for ip, times in self.requests.items()
            if times[-1] > current_time - self.window_seconds
        }

        # 检查限流
        if client_ip not in self.requests:
            self.requests[client_ip] = []

        self.requests[client_ip].append(current_time)

        if len(self.requests[client_ip]) > self.max_requests:
            return Response(
                content="Rate limit exceeded",
                status_code=429,
                headers={"Retry-After": str(self.window_seconds)}
            )

        return await call_next(request)

import time

# 应用配置
app = Litestar(
    route_handlers=[...],
    middleware=[
        TrustedHostMiddleware(allowed_hosts=["example.com"]),
        GZipMiddleware,
        RequestLoggingMiddleware,
        RateLimitMiddleware(max_requests=100, window_seconds=60),
    ]
)
```

#### 5.2 认证与授权

```python
from litestar import get, post, Request, HTTPException
from litestar.middleware.base import MiddlewareProtocol
from litestar.security.jwt import JWTAuth, JWTConfig
from dataclasses import dataclass
from typing import Optional

# JWT 配置
jwt_config = JWTConfig(
    secret="your-secret-key-change-in-production",
    token_algorithm="HS256",
    access_token_expiration=3600  # 1小时
)

jwt_auth = JWTAuth[jwt_config]()

# 用户模型
@dataclass
class User:
    id: int
    username: str
    email: str
    role: str

# 模拟用户数据库
USERS_DB = {
    "admin": User(id=1, username="admin", email="admin@example.com", role="admin"),
    "user": User(id=2, username="user", email="user@example.com", role="user"),
}

# 认证中间件
class JWTAuthMiddleware(MiddlewareProtocol):
    """JWT 认证中间件"""

    async def __call__(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        # 公开路径
        public_paths = ["/login", "/health"]
        if request.url.path in public_paths:
            return await call_next(request)

        # 获取 Token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")

        token = auth_header.split(" ")[1]

        try:
            # 验证 Token
            payload = jwt_auth解密(token)  # 实际使用 jwt_auth.decode(token)
            request.state.user = payload
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)

@post("/login")
async def login(request: Request) -> dict:
    """登录获取 Token"""
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    # 验证用户（实际应该查数据库）
    user = USERS_DB.get(username)
    if not user or password != "password123":  # 简化验证
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 生成 Token
    token = jwt_auth.create_token(
        {"sub": str(user.id), "username": user.username, "role": user.role}
    )

    return {"access_token": token, "token_type": "bearer"}

@get("/protected")
async def protected_route(request: Request) -> dict:
    """受保护的路由"""
    user = request.state.user
    return {
        "message": f"Hello {user['username']}",
        "role": user["role"]
    }

@get("/admin")
async def admin_route(request: Request) -> dict:
    """管理员专属路由"""
    user = request.state.user
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"message": "Welcome, Admin!"}
```

---

## 🚀 实战案例

### 案例：构建博客 API

```python
# blog_app.py - 完整博客 API 示例
from litestar import Litestar, get, post, put, delete, Controller
from litestar.di import Provide
from litestar.config.cors import CORSConfig
from litestar.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from contextlib import asynccontextmanager

# ===== 配置 =====
DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

# ===== 模型 =====
from sqlalchemy import String, Integer, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from litestar.contrib.sqlalchemy.base import CommonBase

class BlogBase(CommonBase):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# ===== DTO =====
class BlogCreate(BaseModel):
    title: str
    content: str
    author: str
    published: bool = False

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    published: bool
    created_at: datetime

# ===== 服务 =====
class BlogService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[BlogBase]:
        from sqlalchemy import select
        result = await self.session.execute(select(BlogBase))
        return list(result.scalars().all())

    async def get_by_id(self, blog_id: int) -> Optional[BlogBase]:
        from sqlalchemy import select
        result = await self.session.execute(
            select(BlogBase).where(BlogBase.id == blog_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: BlogCreate) -> BlogBase:
        blog = BlogBase(**data.model_dump())
        self.session.add(blog)
        await self.session.flush()
        await self.session.refresh(blog)
        return blog

    async def update(self, blog_id: int, data: BlogUpdate) -> Optional[BlogBase]:
        blog = await self.get_by_id(blog_id)
        if not blog:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(blog, key, value)
        await self.session.flush()
        return blog

    async def delete(self, blog_id: int) -> bool:
        blog = await self.get_by_id(blog_id)
        if not blog:
            return False
        await self.session.delete(blog)
        return True

# ===== 控制器 =====
class BlogController(Controller):
    path = "/blogs"

    @get()
    async def list_blogs(self, service: BlogService) -> List[BlogResponse]:
        blogs = await service.get_all()
        return [BlogResponse.model_validate(b) for b in blogs]

    @get("/{blog_id:int}")
    async def get_blog(self, blog_id: int, service: BlogService) -> BlogResponse:
        blog = await service.get_by_id(blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return BlogResponse.model_validate(blog)

    @post()
    async def create_blog(self, data: BlogCreate, service: BlogService) -> BlogResponse:
        blog = await service.create(data)
        return BlogResponse.model_validate(blog)

    @put("/{blog_id:int}")
    async def update_blog(
        self, blog_id: int, data: BlogUpdate, service: BlogService
    ) -> BlogResponse:
        blog = await service.update(blog_id, data)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return BlogResponse.model_validate(blog)

    @delete("/{blog_id:int}")
    async def delete_blog(self, blog_id: int, service: BlogService) -> dict:
        success = await service.delete(blog_id)
        if not success:
            raise HTTPException(status_code=404, detail="Blog not found")
        return {"message": "Blog deleted"}

# ===== 依赖 =====
async def provide_db():
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    engine = create_async_engine(DATABASE_URL)
    async with async_sessionmaker(engine)() as session:
        yield session

async def provide_blog_service(session: AsyncSession) -> BlogService:
    return BlogService(session)

# ===== 应用 =====
app = Litestar(
    route_handlers=[BlogController],
    dependencies={
        "service": Provide(provide_blog_service)
    },
    cors_config=CORSConfig(allow_origins=["*"]),
)

# 运行: uvicorn blog_app:app --reload
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解 Litestar 的设计理念和优势
- [ ] 使用 Litestar 构建 CRUD API
- [ ] 集成 SQLAlchemy 进行数据库操作
- [ ] 实现 Repository 和 Service 分层
- [ ] 配置中间件进行日志、限流等操作
- [ ] 实现 JWT 认证和授权
- [ ] 优化 Litestar 应用的性能

---

## 🔗 相关资源

- [Litestar 官方文档](https://litestar.dev/)
- [Litestar SQLAlchemy 插件](https://docs.litestar.dev/reference/plugins/sqlalchemy.html)
- [Litestar 性能对比](https://github.com/litestar-org/litestar-benchmark)

---

## 🔗 下一步

完成本课程后，你可以：

- 进入 M05: RAG 深度优化
- 学习 M06: AI Agent 最终项目
- 探索 Stage R: 前沿探索实验室

---

**最后更新**: 2026-07-18
