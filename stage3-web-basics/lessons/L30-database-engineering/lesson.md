# L30: 异步数据持久化与事务原子性

> **课程编号**: L30
> **所属阶段**: Stage 3 - Web 开发基础
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐☆（高级应用）
> **前置课程**: L19, L27, L28
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L19**: Pytest 入门
- **L27**: FastAPI 可观测性与契约驱动

**如果你还没有学习以上课程，建议先完成前置课程。**

---

> **课程定位**: Stage 3 数据持久化核心模块 - 异步持久化层升维
>
> **核心目标**: 用 SQLAlchemy 2.0 异步 ORM + 乐观锁粉碎旧模块的同步技术债
>
> **前置要求**:
>
> - 完成 L27 FastAPI 可观测性（OpenTelemetry 追踪）
> - 理解事务 ACID 特性
> - 熟悉异步编程基础
>
> **学习时长**: 8-10 小时（4 章）
>
> **作者**: Python 3.13 全栈课程

---

```mermaid
flowchart TB
    subgraph ORM["SQLAlchemy 2.0 异步"]
        A[create_async_engine] --> B[AsyncSession]
        B --> C[事务边界<br/>begin()]
        C --> D[操作数据库]
        D --> E[commit()<br/>rollback()]
    end
    
    subgraph Lock["并发控制"]
        F[乐观锁<br/>version 字段] --> G[冲突检测]
        H[悲观锁<br/>SELECT FOR UPDATE] --> I[排他锁]
        G --> J[重试机制]
    end
    
    subgraph Trace["可观测性"]
        K[SQLAlchemy OTel] --> L[追踪 SQL]
        L --> M[慢查询检测]
        M --> N[性能优化]
    end
    
    subgraph Pattern["性能基准"]
        O[事务时长<br/><100ms] --> P[单查询<br/><50ms]
        P --> Q[冲突率<br/><10%]
    end
    
    style ORM fill:#e3f2fd
    style Lock fill:#c8e6c9
    style Trace fill:#fff3e0
    style Pattern fill:#f3e5f5
```

---

## 📋 目录

- [第一章：旧模块的数据库技术债](#第一章旧模块的数据库技术债)
- [第二章：事务原子性与边界定义](#第二章事务原子性与边界定义)
- [第三章：乐观锁 vs 悲观锁](#第三章乐观锁-vs-悲观锁)
- [第四章：慢查询追踪与性能诊断](#第四章慢查询追踪与性能诊断)

---

## 第一章：旧模块的数据库技术债

### 1.1 技术债盘点结果

**传统同步实现常见问题统计**:

| 指标           | 数据             | 评级        |
| -------------- | ---------------- | ----------- |
| **数据库代码** | 548 行           | 中型模块    |
| **ORM 类型**   | 100% Django 同步 | 🔴 过时     |
| **事务管理**   | 0%               | 🔴 完全缺失 |
| **并发控制**   | 0%               | 🔴 完全缺失 |
| **慢查询追踪** | 0%               | 🔴 缺失     |
| **巨型模型类** | 230 行单模型     | 🔴 违反 SRP |

---

### 1.2 核心问题示例

#### 问题 1: 无事务保护的多步骤操作

**旧代码** (`interview/admin.py:223-228`):

```python
def save_model(self, request, obj, form, change):
    obj.last_editor = request.user.username
    if not obj.creator:
        obj.creator = request.user.username
    obj.modified_date = datetime.now()
    obj.save()  # ❌ 无事务包裹
```

**问题**:

- 步骤 1 成功，步骤 2 失败 → 数据不一致
- 无回滚机制
- 并发修改无保护

---

#### 问题 2: 230 行巨型模型类

**旧代码** (`interview/models.py`):

```python
class Candidate(models.Model):
    """候选人模型（50+ 字段）"""
    # 基础信息
    username = models.CharField(...)
    phone = models.CharField(...)
    # 初试信息
    first_interviewer = models.CharField(...)
    first_score = models.IntegerField(...)
    # 复试信息
    second_interviewer = models.CharField(...)
    second_score = models.IntegerField(...)
    # HR 复试信息
    hr_interviewer = models.CharField(...)
    hr_score = models.IntegerField(...)
    # ... 总共 50+ 字段
```

**违反原则**:

- ❌ 单一职责原则（SRP）
- ❌ 应拆分为 `Candidate` + `Interview` + `InterviewRound`

---

### 1.3 现代化解决方案

**L32 现代化设计**:

1. ✅ **SQLAlchemy 2.0 异步 ORM**
2. ✅ **事务上下文管理器**
3. ✅ **乐观锁版本控制**
4. ✅ **OpenTelemetry 数据库追踪**

---

## 第二章：事务原子性与边界定义

### 2.1 事务的 ACID 特性

**ACID**:

- **Atomicity（原子性）**: 全部成功或全部失败
- **Consistency（一致性）**: 数据完整性约束
- **Isolation（隔离性）**: 并发事务互不干扰
- **Durability（持久性）**: 提交后永久保存

---

### 2.2 事务上下文管理器设计

> 💡 **核心实现**: `examples/01_sqlalchemy_async_transaction.py` 第 130-150 行
>
> 展示如何用 `@asynccontextmanager` 封装事务边界

**设计思路**:

```python
@asynccontextmanager
async def transaction_scope(session: AsyncSession):
    """
    事务上下文管理器

    **自动行为**:
    1. 进入上下文 → 开启事务
    2. 代码块执行成功 → 提交事务
    3. 代码块抛出异常 → 回滚事务
    """
    try:
        yield session
        await session.commit()  # ← 成功时提交
    except Exception as e:
        await session.rollback()  # ← 失败时回滚
        raise e
```

**使用方式**:

```python
async with transaction_scope(session):
    # 所有操作在同一事务中
    session.add(product)
    session.add(order)
    # 自动提交
```

---

### 2.3 为什么要显式回滚？

**问题**: ORM 不是会自动回滚吗？

**答案**: **不完全自动**

**SQLAlchemy 行为**:

- ✅ **异常时自动回滚连接状态**
- ❌ **不自动清理 Session 对象状态**
- ❌ **不自动重置脏对象（dirty objects）**

**示例**:

```python
# ❌ 没有显式回滚
async def bad_transaction():
    session.add(product)
    await session.commit()  # 失败
    # 此时 product 仍在 session 中（脏状态）
    # 后续操作可能基于错误状态

# ✅ 显式回滚
async def good_transaction():
    try:
        session.add(product)
        await session.commit()
    except Exception:
        await session.rollback()  # 清理 session 状态
        raise
```

---

### 2.4 事务边界最佳实践

**原则**: **事务应该尽可能短**

**对比**:

| 反模式                  | 最佳实践                    |
| ----------------------- | --------------------------- |
| ❌ 在事务中调用外部 API | ✅ 外部调用在事务外         |
| ❌ 在事务中发送邮件     | ✅ 邮件放入队列，事务外发送 |
| ❌ 在事务中执行长计算   | ✅ 计算完成后再开启事务     |
| ❌ 事务跨多个 HTTP 请求 | ✅ 每个请求独立事务         |

**推荐结构**:

```python
# 1. 准备数据（事务外）
data = await fetch_from_api()
processed = complex_calculation(data)

# 2. 开启事务（仅数据库操作）
async with transaction_scope(session):
    product = Product(**processed)
    session.add(product)
    # 快速提交
```

---

## 第三章：乐观锁 vs 悲观锁

### 3.1 库存扣减的并发挑战

**场景**: 100 件库存，两个用户同时购买

```
时刻 T1: 用户 A 读取库存 100
时刻 T2: 用户 B 读取库存 100
时刻 T3: 用户 A 购买 10 件 → 库存 90（写入数据库）
时刻 T4: 用户 B 购买 95 件 → 库存 5（写入数据库）

问题：实际卖出 105 件，超卖 5 件 ❌
```

**解决方案**: **并发控制**

---

### 3.2 乐观锁实现（Optimistic Locking）

> 💡 **核心实现**: `examples/01_sqlalchemy_async_transaction.py` 第 165-250 行
>
> 展示乐观锁的完整实现与版本冲突检测

**设计原理**:

**步骤 1: 添加版本字段**

```python
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)

    # 乐观锁版本字段（关键）
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
```

**步骤 2: 更新时检查版本**

```python
# 读取当前版本
product = await session.get(Product, product_id)
current_version = product.version

# 原子更新（WHERE 子句包含版本检查）
update_stmt = (
    update(Product)
    .where(Product.id == product_id)
    .where(Product.version == current_version)  # ← 版本检查
    .values(
        stock=Product.stock - quantity,
        version=Product.version + 1,  # ← 版本递增
    )
)

result = await session.execute(update_stmt)

# 检查更新行数
if result.rowcount == 0:
    raise RuntimeError("版本冲突，请重试")
```

---

### 3.3 悲观锁实现（Pessimistic Locking）

> 💡 **对比实现**: `examples/01_sqlalchemy_async_transaction.py` 第 255-295 行
>
> 展示 SELECT FOR UPDATE 的悲观锁实现

**设计原理**:

```python
# SELECT FOR UPDATE（加排他锁）
stmt = (
    select(Product)
    .where(Product.id == product_id)
    .with_for_update()  # ← 悲观锁
)

product = (await session.execute(stmt)).scalar_one()

# 此时其他事务被阻塞，无法读取此行
# 直接更新（无冲突风险）
product.stock -= quantity
```

---

### 3.4 乐观锁 vs 悲观锁深度对比

#### 性能对比

| 维度         | 乐观锁       | 悲观锁     |
| ------------ | ------------ | ---------- |
| **读取性能** | 无锁，极快   | 加锁，等待 |
| **写入性能** | 冲突时重试   | 无冲突     |
| **并发能力** | 高（无阻塞） | 低（阻塞） |
| **适用场景** | 读多写少     | 写多读少   |

**具体数据**（假设 100 并发）:

| 场景       | 乐观锁         | 悲观锁         | 说明         |
| ---------- | -------------- | -------------- | ------------ |
| 冲突率 1%  | 平均延迟 50ms  | 平均延迟 200ms | 乐观锁更快   |
| 冲突率 50% | 平均延迟 300ms | 平均延迟 250ms | 悲观锁更稳定 |
| 冲突率 90% | 平均延迟 800ms | 平均延迟 300ms | 悲观锁占优   |

---

#### 为什么高并发下乐观锁延时更低？

**乐观锁优势**:

1. ✅ **无锁等待**：读取时不加锁，并发度高
2. ✅ **快速路径**：99% 场景无冲突，直接成功
3. ✅ **资源占用少**：无锁表维护开销

**悲观锁劣势**:

1. ❌ **锁等待**：后续请求排队等待
2. ❌ **死锁风险**：多表更新时可能死锁
3. ❌ **锁竞争**：高并发时锁表压力大

**量化分析**:

```
乐观锁平均延迟 = 读取时间 + 写入时间 + (冲突率 × 重试时间)
                = 10ms + 20ms + (1% × 100ms)
                = 31ms

悲观锁平均延迟 = 锁等待时间 + 读取时间 + 写入时间
                = 150ms + 10ms + 20ms
                = 180ms

结论：冲突率 < 15% 时，乐观锁更快
```

---

#### 什么情况下悲观锁是唯一选择？

**场景 1: 库存为 1 的秒杀**

```python
# 100 人抢 1 件商品
# 冲突率 = 99%
# 乐观锁：99 次重试，延迟爆炸
# 悲观锁：串行执行，稳定
```

**场景 2: 金融交易**

```python
# 银行转账：A → B
# 要求：绝对不能重试（幂等性问题）
# 乐观锁：重试可能导致重复扣款
# 悲观锁：一次成功，无重试
```

**场景 3: 关键业务数据**

```python
# 订单状态机：pending → processing → completed
# 要求：状态转换必须严格串行
# 乐观锁：可能出现状态跳跃
# 悲观锁：保证状态转换顺序
```

**决策树**:

```
冲突率 < 10%？
  ├─ 是 → 乐观锁
  └─ 否 → 需要重试？
         ├─ 是 → 乐观锁
         └─ 否 → 悲观锁
```

---

## 第四章：慢查询追踪与性能诊断

### 4.1 生产环境的性能噩梦

**问题**: 用户反馈"页面加载慢"

**传统排查流程**:

1. ❌ 查看应用日志（无 SQL 记录）
2. ❌ 开启数据库慢查询日志（影响性能）
3. ❌ 手动分析 SQL（耗时数小时）
4. ❌ 难以关联业务场景

**现代化方案**: **OpenTelemetry 分布式追踪**

---

### 4.2 SQLAlchemy OTel 集成

> 💡 **核心实现**: `examples/01_sqlalchemy_async_transaction.py` 第 36-42 行
>
> 展示如何用两行代码注入数据库追踪

**配置代码**:

```python
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# 创建引擎
engine = create_async_engine(DATABASE_URL)

# 注入 OpenTelemetry（一行代码）
SQLAlchemyInstrumentor().instrument(
    engine=engine.sync_engine,
    service="inventory-service",
)
```

**自动追踪内容**:

- ✅ SQL 语句（完整文本）
- ✅ 执行时间（毫秒）
- ✅ 返回行数
- ✅ 数据库连接信息
- ✅ 错误堆栈

---

### 4.3 慢查询示例

> 💡 **慢查询演示**: `examples/01_sqlalchemy_async_transaction.py` 第 340-365 行
>
> 展示如何触发慢查询并追踪

**业务代码**:

```python
async def slow_query_example(session: AsyncSession):
    """慢查询示例"""
    with tracer.start_as_current_span("slow_query_example") as span:
        # 模拟复杂查询（返回 1000 行）
        stmt = select(Product).limit(1000)
        result = await session.execute(stmt)
        products = result.scalars().all()

        span.set_attribute("query.row_count", len(products))
        return products
```

**Jaeger UI 展示**:

```
Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736
├── GET /products [250ms]
│   └── slow_query_example [230ms]
│       └── SELECT * FROM products LIMIT 1000 [220ms]  ← 慢查询
│           ├── db.statement: SELECT ...
│           ├── db.row_count: 1000
│           ├── db.system: postgresql
│           └── db.connection_string: postgresql://localhost
```

---

### 4.4 生产环境价值

**价值 1: 精准定位慢查询**

传统方式:

```
应用日志: "请求耗时 2.5s"
↓
数据库日志: 5000 条 SQL（哪条慢？）
↓
手动分析: 耗时 2 小时
```

OTel 方式:

```
Jaeger UI: 点击慢请求
↓
自动展示: SQL 语句 + 执行时间
↓
定位问题: 耗时 30 秒
```

**价值 2: 关联业务上下文**

**Span 属性**:

```python
span.set_attribute("user.id", 12345)
span.set_attribute("product.id", 678)
span.set_attribute("query.row_count", 10000)
```

**分析能力**:

- ✅ "哪些用户遇到慢查询？"
- ✅ "哪些产品导致慢查询？"
- ✅ "慢查询是否与返回行数相关？"

**价值 3: 自动化告警**

**集成 Prometheus**:

```yaml
# 告警规则
- alert: SlowDatabaseQuery
  expr: db_query_duration_seconds > 1.0
  for: 1m
  annotations:
    summary: "慢查询告警"
    description: "SQL 执行超过 1 秒"
```

---

## 生产级实战总结

### 核心要点回顾

💡 **5 个必须掌握的知识点**:

1. **事务边界**: 尽可能短，只包含数据库操作
2. **显式回滚**: 清理 Session 状态，避免脏数据
3. **乐观锁优先**: 冲突率 < 10% 时性能最优
4. **悲观锁兜底**: 高冲突场景或金融交易
5. **OTel 追踪**: 生产环境必备，慢查询定位利器

---

### 技术选型决策树

```
需要并发控制？
├─ 是 → 冲突率 < 10%？
│       ├─ 是 → 乐观锁
│       └─ 否 → 允许重试？
│               ├─ 是 → 乐观锁
│               └─ 否 → 悲观锁
└─ 否 → 无锁（单线程场景）
```

---

### 最佳实践清单

**数据库设计**:

- [ ] 拆分巨型模型类（单一职责）
- [ ] 添加 version 字段（乐观锁）
- [ ] 添加 created_at/updated_at（审计）
- [ ] 避免 NULL 字段（性能优化）

**事务管理**:

- [ ] 使用事务上下文管理器
- [ ] 显式回滚异常
- [ ] 控制事务边界（<100ms）
- [ ] 避免嵌套事务

**并发控制**:

- [ ] 默认使用乐观锁
- [ ] 高冲突场景使用悲观锁
- [ ] 实现重试机制（指数退避）
- [ ] 监控冲突率

**可观测性**:

- [ ] 注入 SQLAlchemy OTel
- [ ] 记录慢查询（>100ms）
- [ ] 关联业务上下文
- [ ] 配置告警规则

---

### 性能基准

**优化目标**:

| 指标         | 目标    | 说明           |
| ------------ | ------- | -------------- |
| 事务时长     | < 100ms | 超过则拆分     |
| 单查询时长   | < 50ms  | 超过则优化索引 |
| 冲突率       | < 10%   | 超过则用悲观锁 |
| 连接池利用率 | < 80%   | 超过则扩容     |

---

## 附录 A：MongoDB 扩展（选修）

### A.1 NoSQL vs SQL 对比

| 维度 | SQL 关系型 | NoSQL 文档型 |
|------|------------|--------------|
| 数据模型 | 关系表 | 文档集合 |
| Schema | 固定结构 | 灵活多变 |
| 事务 | ACID 强一致 | 最终一致 |
| 适用场景 | 结构化数据 | 文档存储、日志 |
| 代表产品 | PostgreSQL | MongoDB |

### A.2 Motor 异步驱动

**Motor** 是 MongoDB 官方异步 Python 驱动，兼容 asyncio。

```python
# examples/05_mongodb_async.py
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Pydantic 模型（与 SQLAlchemy 对比）
class UserDocument(BaseModel):
    """MongoDB 文档模型"""
    name: str = Field(..., min_length=2, max_length=50)
    email: str
    tags: list[str] = Field(default_factory=list)
    metadata: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MongoDBSession:
    """MongoDB 异步会话封装"""

    def __init__(self, connection_string: str = "mongodb://localhost:27017"):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(connection_string)
        self.db = self.client["app_database"]

    @property
    def users(self):
        """获取用户集合"""
        return self.db["users"]

    async def close(self):
        """关闭连接"""
        self.client.close()


# 创建实例
mongo = MongoDBSession()
```

### A.3 CRUD 操作

```python
# examples/05_mongodb_async.py (续)


async def create_user(mongo: MongoDBSession, user: UserDocument) -> str:
    """创建用户文档"""
    result = await mongo.users.insert_one(user.model_dump())
    return str(result.inserted_id)


async def find_user_by_email(
    mongo: MongoDBSession, email: str
) -> Optional[dict]:
    """按邮箱查找用户"""
    return await mongo.users.find_one({"email": email})


async def find_users_by_tags(
    mongo: MongoDBSession, tags: list[str], limit: int = 10
) -> list[dict]:
    """按标签查找用户（数组包含查询）"""
    cursor = mongo.users.find(
        {"tags": {"$in": tags}}  # $in 运算符
    ).limit(limit)

    return await cursor.to_list(length=limit)


async def update_user_tags(
    mongo: MongoDBSession, user_id: str, new_tags: list[str]
) -> int:
    """更新用户标签（返回修改数量）"""
    result = await mongo.users.update_one(
        {"_id": user_id},
        {
            "$set": {"tags": new_tags},
            "$currentDate": {"updated_at": True}
        }
    )
    return result.modified_count
```

### A.4 与 SQLAlchemy 对比

| 操作 | SQLAlchemy (L30) | Motor (MongoDB) |
|------|------------------|------------------|
| 连接 | `create_async_engine()` | `AsyncIOMotorClient()` |
| 模型 | `class User(Base)` | `class UserDocument(BaseModel)` |
| 查询 | `select(User).where(...)` | `collection.find_one({...})` |
| 插入 | `session.add()` + `commit()` | `insert_one()` |
| 更新 | `update().where()` | `update_one()` + `$set` |

**代码对比**:

```python
# SQLAlchemy (参考 L30)
async def get_user_sql(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


# MongoDB Motor
async def get_user_mongo(mongo: MongoDBSession, user_id: str) -> Optional[dict]:
    return await mongo.users.find_one({"_id": user_id})
```

### A.5 聚合管道

```python
# examples/05_mongodb_async.py (续)


async def aggregate_user_stats(mongo: MongoDBSession) -> list[dict]:
    """聚合管道：统计用户标签分布"""
    pipeline = [
        # 展开 tags 数组
        {"$unwind": "$tags"},
        # 按标签分组计数
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        # 按计数降序排列
        {"$sort": {"count": -1}},
        # 限制前 10 个
        {"$limit": 10},
    ]

    cursor = mongo.users.aggregate(pipeline)
    return await cursor.to_list(length=10)
```

### A.6 索引优化

```python
async def create_indexes(mongo: MongoDBSession) -> None:
    """创建索引提升查询性能"""
    # 单字段索引
    await mongo.users.create_index("email", unique=True)

    # 复合索引
    await mongo.users.create_index([
        ("tags", 1),       # 1=升序
        ("created_at", -1)  # -1=降序
    ])

    # 文本索引（全文搜索）
    await mongo.users.create_index([
        ("name", "text"),
        ("email", "text")
    ])
```

### A.7 何时使用 MongoDB？

**适合使用 MongoDB 的场景**:

- ✅ 内容管理系统（文档存储）
- ✅ 用户画像（灵活字段）
- ✅ 日志系统（时序数据）
- ✅ 实时分析（高写入）
- ✅ 原型开发（Schema 频繁变更）

**继续使用 SQL 的场景**:

- ✅ 金融交易（强一致性）
- ✅ 复杂关联查询（JOIN）
- ✅ 报表统计（OLAP）

### A.8 练习

1. 使用 Motor 实现用户 CRUD 操作
2. 实现基于标签的用户搜索
3. 使用聚合管道统计用户活跃度

---

**课程完成**！你已掌握 SQLAlchemy 2.0 异步持久化与事务原子性的生产级实战技能。🎉


## 🔗 下一步


[L31: SQL 进阶](../L31-sql-advanced/)
