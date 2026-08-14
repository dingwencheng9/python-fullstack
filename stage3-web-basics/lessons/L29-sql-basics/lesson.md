# L29: 数据库基础与 SQL 入门

> **课程编号**: L29
> **所属阶段**: Stage 3 - Web 开发基础
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐☆☆（中级）
> **前置课程**: L26
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ **数据库基础**：理解关系型数据库核心概念
2. ✅ **SQL 查询**：熟练编写 SELECT/INSERT/UPDATE/DELETE
3. ✅ **表设计**：设计规范的数据库表结构
4. ✅ **ORM 入门**：使用 SQLAlchemy 2.0 进行数据库操作
5. ✅ **项目实战**：构建博客系统数据库层

---

## 📚 课程导读

### 为什么要学习数据库？

现代 Web 应用几乎都需要持久化存储数据：

```
┌─────────────────────────────────────────────────────────┐
│                   Web 应用架构                         │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  用户请求 ──→ API ──→ 业务逻辑 ──→ 数据库            │
│                              ↓                         │
│                         返回结果                       │
│                                                     │
│  数据库是所有应用的核心：                             │
│  - 用户信息存储                                       │
│  - 业务数据管理                                       │
│  - 数据一致性保障                                     │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

---

```mermaid
flowchart TB
    subgraph SQL["SQL 查询类型"]
        A[SELECT 查询] --> D[WHERE 条件]
        A --> E[JOIN 关联]
        A --> F[GROUP 分组]
        B[INSERT 插入] --> G[VALUES]
        C[UPDATE 更新] --> H[SET + WHERE]
    end
    
    subgraph ORM["SQLAlchemy 2.0"]
        I[create_async_engine] --> J[AsyncSession]
        J --> K[select()<br/>查询构建]
        K --> L[结果处理<br/>scalar_one()]
    end
    
    subgraph Pattern["设计模式"]
        M[单表操作] --> N[CRUD 基本]
        N --> O[事务管理<br/>commit/rollback]
        O --> P[连接池<br/>pool_size]
    end
    
    style SQL fill:#e3f2fd
    style ORM fill:#c8e6c9
    style Pattern fill:#fff3e0
```

---

## Part 1: 数据库概述

### 1.1 关系型数据库 vs 非关系型数据库

**关系型数据库（RDBMS）**：

| 数据库 | 特点 | 适用场景 |
|--------|------|----------|
| PostgreSQL | 功能最强大、扩展性强 | 企业级、复杂查询 |
| MySQL | 简单易用、Web首选 | Web应用、中小型 |
| SQLite | 零配置、嵌入式 | 移动App、测试、小型应用 |
| MariaDB | MySQL兼容、性能优化 | Web应用、云计算 |

**非关系型数据库（NoSQL）**：

| 类型 | 数据库 | 适用场景 |
|------|--------|----------|
| 文档型 | MongoDB | JSON文档存储 |
| 键值型 | Redis | 缓存、Session |
| 列式型 | Cassandra | 时序数据、大数据 |
| 向量型 | Qdrant | AI Embedding |

### 1.2 PostgreSQL 快速入门

```bash
# macOS 安装
brew install postgresql@16

# Linux 安装
sudo apt install postgresql postgresql-contrib

# 启动服务
brew services start postgresql@16  # macOS
sudo systemctl start postgresql   # Linux

# 连接数据库
psql -U postgres

# 或者指定数据库
psql -U postgres -d myapp
```

### 1.3 创建第一个数据库

```sql
-- 查看所有数据库
\l

-- 创建数据库
CREATE DATABASE myapp;

-- 连接到指定数据库
\c myapp

-- 创建用户（可选）
CREATE USER myapp_user WITH PASSWORD 'secret_password';
GRANT ALL PRIVILEGES ON DATABASE myapp TO myapp_user;

-- 给用户授权
GRANT ALL ON SCHEMA public TO myapp_user;
```

---

## Part 2: SQL 基础查询

### 2.1 创建表

```sql
-- 创建用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,           -- 自增主键
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建文章表
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    published BOOLEAN DEFAULT FALSE,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建评论表
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 查看表结构
\d users
\d posts
```

### 2.2 数据类型

| 类型 | 说明 | 示例 |
|------|------|------|
| INTEGER/INT | 整数 | 1, 42, -5 |
| BIGINT | 大整数 | 9223372036854775807 |
| SERIAL | 自增整数 | 1, 2, 3... |
| VARCHAR(n) | 变长字符串 | 'hello' |
| TEXT | 无限长文本 | 长文章内容 |
| BOOLEAN | 布尔值 | TRUE/FALSE |
| DATE | 日期 | '2024-01-15' |
| TIMESTAMP | 时间戳 | '2024-01-15 10:30:00' |
| JSON/JSONB | JSON数据 | '{"key": "value"}' |
| UUID | 通用唯一标识 | 'a0eebc99...' |

### 2.3 INSERT 插入数据

```sql
-- 插入单条数据
INSERT INTO users (username, email, password_hash)
VALUES ('alice', 'alice@example.com', 'hash123');

-- 插入多条数据
INSERT INTO users (username, email, password_hash) VALUES
    ('bob', 'bob@example.com', 'hash456'),
    ('charlie', 'charlie@example.com', 'hash789');

-- 插入并返回
INSERT INTO users (username, email, password_hash)
VALUES ('david', 'david@example.com', 'hash012')
RETURNING id, username, created_at;

-- 从其他表插入
INSERT INTO posts (title, content, author_id)
SELECT title, content, 1 FROM old_posts WHERE status = 'published';
```

### 2.4 SELECT 查询基础

```sql
-- 查询所有列
SELECT * FROM users;

-- 查询指定列
SELECT username, email FROM users;

-- 别名
SELECT username AS "用户名", email AS "邮箱" FROM users;

-- 过滤重复
SELECT DISTINCT author_id FROM posts;

-- 带条件查询
SELECT * FROM users WHERE is_active = TRUE;

-- 多条件
SELECT * FROM posts
WHERE published = TRUE
  AND author_id = 1;

-- 模糊查询
SELECT * FROM users WHERE email LIKE '%@example.com';

-- IN 查询
SELECT * FROM users WHERE id IN (1, 2, 3);

-- BETWEEN 范围
SELECT * FROM posts WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- 排序
SELECT * FROM users ORDER BY created_at DESC;  -- 降序
SELECT * FROM users ORDER BY username ASC;      -- 升序

-- 分页 LIMIT
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 0;  -- 第1页
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 10; -- 第2页
```

### 2.5 聚合函数

```sql
-- COUNT 计数
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM posts WHERE published = TRUE;

-- SUM 求和
SELECT SUM(amount) FROM orders;

-- AVG 平均值
SELECT AVG(price) FROM products;

-- MAX/MIN 最大最小
SELECT MAX(price), MIN(price) FROM products;

-- 组合使用
SELECT
    COUNT(*) AS total_posts,
    COUNT(*) FILTER (WHERE published = TRUE) AS published_posts,
    AVG(LENGTH(content)) AS avg_content_length
FROM posts;
```

### 2.6 GROUP BY 分组

```sql
-- 按作者分组统计文章数
SELECT
    author_id,
    COUNT(*) AS post_count
FROM posts
GROUP BY author_id;

-- HAVING 过滤分组结果
SELECT
    author_id,
    COUNT(*) AS post_count
FROM posts
GROUP BY author_id
HAVING COUNT(*) > 5;

-- 多字段分组
SELECT
    author_id,
    published,
    COUNT(*) AS count
FROM posts
GROUP BY author_id, published;
```

### 2.7 多表连接 JOIN

```sql
-- INNER JOIN 内连接（只保留匹配的行）
SELECT
    users.username,
    posts.title,
    posts.created_at
FROM users
INNER JOIN posts ON users.id = posts.author_id;

-- 等价简写
SELECT
    u.username,
    p.title,
    p.created_at
FROM users u
INNER JOIN posts p ON u.id = p.author_id;

-- LEFT JOIN 左外连接（保留左表所有行）
SELECT
    u.username,
    p.title
FROM users u
LEFT JOIN posts p ON u.id = p.author_id;
-- 即使没有文章的用户也会显示

-- RIGHT JOIN 右外连接
SELECT
    u.username,
    p.title
FROM users u
RIGHT JOIN posts p ON u.id = p.author_id;

-- FULL OUTER JOIN 全外连接
SELECT
    u.username,
    p.title
FROM users u
FULL OUTER JOIN posts p ON u.id = p.author_id;

-- 多表连接
SELECT
    u.username,
    p.title,
    c.content AS comment
FROM users u
JOIN posts p ON u.id = p.author_id
JOIN comments c ON p.id = c.post_id
WHERE p.published = TRUE;
```

### 2.8 子查询

```sql
-- 查询文章数大于5的作者
SELECT * FROM users
WHERE id IN (
    SELECT author_id FROM posts
    GROUP BY author_id
    HAVING COUNT(*) > 5
);

-- 查询最新发布的文章
SELECT * FROM posts
WHERE created_at = (
    SELECT MAX(created_at) FROM posts
);

-- 使用 EXISTS
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM posts p
    WHERE p.author_id = u.id
    AND p.published = TRUE
);
```

### 2.9 UPDATE 更新数据

```sql
-- 更新单条
UPDATE users
SET email = 'new_email@example.com'
WHERE id = 1;

-- 更新多条
UPDATE posts
SET published = TRUE, updated_at = CURRENT_TIMESTAMP
WHERE created_at < '2024-01-01';

-- 使用表达式
UPDATE products
SET price = price * 0.9
WHERE stock > 100;

-- 返回更新后的数据
UPDATE users
SET is_active = FALSE
WHERE id = 1
RETURNING id, username, is_active;
```

### 2.10 DELETE 删除数据

```sql
-- 删除指定数据
DELETE FROM comments
WHERE post_id = 1;

-- 使用子查询删除
DELETE FROM users
WHERE id NOT IN (
    SELECT DISTINCT author_id FROM posts
);

-- 返回删除的数据
DELETE FROM posts
WHERE id = 5
RETURNING id, title;

-- 清空表（慎用！）
TRUNCATE TABLE posts RESTART IDENTITY;
```

---

## Part 3: 数据库设计与规范化

### 3.1 三大范式

**第一范式（1NF）**：原子性
- 每个列都是不可再分的最小数据单元
- 每一列都是单一值

```sql
-- ❌ 违反1NF：地址包含多个值
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    address VARCHAR(500)  -- 包含省、市、区、街道
);

-- ✅ 符合1NF：拆分地址
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    province VARCHAR(50),
    city VARCHAR(50),
    district VARCHAR(50),
    street VARCHAR(200)
);
```

**第二范式（2NF）**：完全函数依赖
- 在1NF基础上，非主键列必须完全依赖于主键
- 不能只依赖于主键的一部分

```sql
-- ❌ 违反2NF：course_name 只依赖于 (student_id, course_id) 中的 course_id
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    course_name VARCHAR(100),  -- 只依赖 course_id
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id)
);

-- ✅ 符合2NF：拆分到 courses 表
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

**第三范式（3NF）**：传递依赖
- 在2NF基础上，非主键列之间不能有传递依赖

```sql
-- ❌ 违反3NF：college_name 传递依赖于 college_id
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    college_id INTEGER,
    college_name VARCHAR(100),  -- 传递依赖：college_id → college_name
    FOREIGN KEY (college_id) REFERENCES colleges(id)
);

-- ✅ 符合3NF：通过 JOIN 查询获取
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    college_id INTEGER,
    FOREIGN KEY (college_id) REFERENCES colleges(id)
);
```

### 3.2 主键与外键

```sql
-- 主键约束
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    -- 或使用 UUID
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);

-- 外键约束
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES users(id),
    -- 级联操作
    FOREIGN KEY (author_id) REFERENCES users(id)
        ON DELETE CASCADE      -- 删除用户时删除文章
        ON UPDATE CASCADE,      -- 更新用户ID时同步更新
    -- 或
        ON DELETE SET NULL     -- 删除用户时设为NULL
        ON DELETE RESTRICT     -- 阻止删除（有外链时）
);

-- 唯一约束
CREATE TABLE users (
    email VARCHAR(100) UNIQUE,
    -- 复合唯一
    UNIQUE (first_name, last_name, birth_date)
);

-- 检查约束
CREATE TABLE products (
    price DECIMAL(10, 2) CHECK (price > 0),
    status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'archived'))
);
```

### 3.3 索引优化

```sql
-- 创建索引
CREATE INDEX idx_posts_author ON posts(author_id);
CREATE INDEX idx_posts_created ON posts(created_at DESC);
CREATE INDEX idx_posts_title ON posts(title VARCHAR_PATTERN_OPS);  -- 模糊搜索

-- 复合索引（顺序很重要！）
CREATE INDEX idx_users_email_username ON users(email, username);

-- 唯一索引
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- 查看查询计划
EXPLAIN SELECT * FROM posts WHERE author_id = 1;
EXPLAIN ANALYZE SELECT * FROM posts WHERE author_id = 1;

-- 创建表达式索引
CREATE INDEX idx_posts_title_lower ON posts(LOWER(title));

-- 部分索引
CREATE INDEX idx_posts_published ON posts(created_at)
WHERE published = TRUE;
```

---

## Part 4: SQLAlchemy ORM 入门

### 4.1 安装和配置

```bash
# 安装依赖
uv add sqlalchemy aiosqlite

# 生产环境使用
uv add psycopg2-binary   # PostgreSQL
# 或
uv add asyncpg           # 异步 PostgreSQL
```

### 4.2 模型定义

```python
# app/models.py
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, func, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List

class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    pass

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # 关系
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Post(Base):
    """文章模型"""
    __tablename__ = "posts"
    __table_args__ = (
        Index("idx_posts_author_created", "author_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    published: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # 关系
    author: Mapped["User"] = relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post {self.title}>"
```

### 4.3 同步会话操作

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# 创建引擎（同步）
engine = create_engine("sqlite:///./myapp.db", echo=True)

# 创建表
Base.metadata.create_all(engine)

# 创建会话
with Session(engine) as session:
    # CREATE - 创建用户
    user = User(
        username="alice",
        email="alice@example.com",
        password_hash="hashed_password"
    )
    session.add(user)
    session.commit()  # 提交事务

    # READ - 查询用户
    result = session.execute(select(User).where(User.username == "alice"))
    user = result.scalar_one_or_none()

    # READ - 查询所有用户
    result = session.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()

    # UPDATE - 更新用户
    user.email = "new_email@example.com"
    session.commit()

    # DELETE - 删除用户
    session.delete(user)
    session.commit()

    # 关联操作
    post = Post(title="Hello World", author=user)
    session.add(post)
    session.commit()
```

### 4.4 异步会话操作

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 创建异步引擎
engine = create_async_engine(
    "sqlite+aiosqlite:///./myapp.db",
    echo=True
)

# 创建会话工厂
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def main():
    async with async_session() as session:
        # CREATE
        user = User(
            username="bob",
            email="bob@example.com",
            password_hash="hashed"
        )
        session.add(user)
        await session.commit()

        # READ
        from sqlalchemy import select
        result = await session.execute(
            select(User).where(User.username == "bob")
        )
        user = result.scalar_one_or_none()

        # UPDATE
        if user:
            user.email = "new_bob@example.com"
            await session.commit()

        # DELETE
        await session.delete(user)
        await session.commit()

asyncio.run(main())
```

### 4.5 关系操作

```python
async def relationship_demo():
    async with async_session() as session:
        # 创建用户和文章
        user = User(username="author", email="author@example.com", password_hash="x")
        session.add(user)
        await session.flush()  # 获取 ID

        post = Post(title="First Post", author=user)
        session.add(post)
        await session.commit()

        # 懒加载关系
        result = await session.execute(select(User))
        user = result.scalar_one()
        print(user.posts)  # 自动加载关联的文章

        # 预加载关系（推荐）
        from sqlalchemy.orm import selectinload
        result = await session.execute(
            select(User).options(selectinload(User.posts))
        )
        users = result.scalars().all()
        for user in users:
            print(f"{user.username}: {len(user.posts)} posts")

        # 过滤关联对象
        result = await session.execute(
            select(Post).where(Post.author.has(username="author"))
        )
        posts = result.scalars().all()
```

### 4.6 复杂查询

```python
from sqlalchemy import func, and_, or_

async def complex_queries():
    async with async_session() as session:
        # 聚合查询
        result = await session.execute(
            select(
                User.username,
                func.count(Post.id).label("post_count")
            )
            .join(Post)
            .group_by(User.id)
            .having(func.count(Post.id) > 5)
        )
        stats = result.all()

        # 模糊查询
        result = await session.execute(
            select(User).where(User.username.like("%alice%"))
        )

        # 复杂条件
        result = await session.execute(
            select(Post).where(
                and_(
                    Post.published == True,
                    or_(
                        Post.title.like("%Python%"),
                        Post.content.like("%Python%")
                    )
                )
            )
        )

        # 分页查询
        page = 1
        page_size = 10
        result = await session.execute(
            select(Post)
            .order_by(Post.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
```

---

## Part 5: 项目实战 - 博客数据库

### 5.1 项目结构

```
blog_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
├── tests/
│   └── test_crud.py
└── pyproject.toml
```

### 5.2 CRUD 封装

```python
# app/crud.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.models import User, Post

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """根据 ID 获取用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """根据用户名获取用户"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[User]:
    """获取用户列表"""
    result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())

async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password_hash: str
) -> User:
    """创建用户"""
    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_posts(
    db: AsyncSession,
    published: Optional[bool] = None,
    author_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Post]:
    """获取文章列表"""
    query = select(Post)

    if published is not None:
        query = query.where(Post.published == published)

    if author_id is not None:
        query = query.where(Post.author_id == author_id)

    result = await db.execute(
        query
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())

async def count_posts(
    db: AsyncSession,
    published: Optional[bool] = None
) -> int:
    """统计文章数量"""
    query = select(func.count(Post.id))

    if published is not None:
        query = query.where(Post.published == published)

    result = await db.execute(query)
    return result.scalar()
```

---

## 📝 课程总结

### 核心知识点

1. **SQL 基础**
   - DDL: CREATE TABLE, ALTER, DROP
   - DML: INSERT, SELECT, UPDATE, DELETE
   - DQL: WHERE, ORDER BY, GROUP BY, JOIN

2. **数据库设计**
   - 三大范式（1NF, 2NF, 3NF）
   - 主键、外键、索引
   - 规范化 vs 性能权衡

3. **SQLAlchemy ORM**
   - 模型定义（DeclarativeBase）
   - 会话操作（Session/AsyncSession）
   - 关系（relationship）
   - 查询（select, where, join）

### 常见错误

| 错误 | 解决方案 |
|------|----------|
| 忘记 COMMIT | 检查事务是否提交 |
| SQL 注入 | 使用参数化查询 |
| N+1 查询 | 使用 selectinload 预加载 |
| 索引未生效 | 用 EXPLAIN 检查执行计划 |

---

## ✅ 完成标准

完成本课程后，你应该能够：

- [ ] 理解关系型数据库核心概念
- [ ] 熟练编写 SQL 查询语句
- [ ] 设计规范的数据库表结构
- [ ] 使用 SQLAlchemy 定义数据模型
- [ ] 实现 CRUD 数据库操作
- [ ] 理解数据库规范化原则

---

**下一步**: 继续学习 [L30: 异步数据操作与 ORM](../L30-database-engineering/lesson.md)
