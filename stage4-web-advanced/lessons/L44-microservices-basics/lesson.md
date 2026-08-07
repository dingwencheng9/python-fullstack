# L44: 微服务架构基础

> **课程编号**: L44
> **所属阶段**: Stage 4 - Web 开发进阶
> **预计时长**: 5-6 小时
> **难度**: ⭐⭐⭐⭐⭐（专家级）
> **前置课程**: L41, L43
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ **微服务基础**：理解微服务架构核心概念
2. ✅ **服务拆分**：掌握服务拆分的原则和方法
3. ✅ **服务通信**：实现同步和异步服务通信
4. ✅ **服务发现**：使用 Consul/Etcd 实现服务发现
5. ✅ **API 网关**：实现统一的 API 网关
6. ✅ **配置管理**：实现分布式配置管理

---

```mermaid
flowchart TB
    subgraph Monolith["单体架构"]
        A[用户服务] --> B[共享数据库]
        C[订单服务] --> B
        D[支付服务] --> B
    end

    subgraph Microservices["微服务架构"]
        E[用户服务<br/>独立 DB] --> F[API Gateway]
        G[订单服务<br/>独立 DB] --> F
        H[支付服务<br/>独立 DB] --> F
        I[通知服务] -.->|异步| G
        J[服务发现<br/>Consul/Etcd] --> E
        J --> G
        J --> H
    end

    subgraph Patterns["微服务模式"]
        K[Circuit Breaker<br/>熔断器] --> L[Service Mesh<br/>服务网格]
        M[API Gateway<br/>统一入口] --> L
        N[Distributed Config<br/>配置中心] --> O[灰度发布]
    end

    style Monolith fill:#ffcdd2
    style Microservices fill:#c8e6c9
    style Patterns fill:#e3f2fd
```

---

## Part 1: 微服务 vs 单体架构

### 1.1 架构对比

```
┌─────────────────────────────────────────────────────────┐
│                   单体 vs 微服务                        │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  单体架构：                                        │
│  ┌─────────────────────────────────┐               │
│  │        用户服务  │ 订单服务     │               │
│  │        支付服务  │ 商品服务     │               │
│  │        库存服务  │ 通知服务     │               │
│  └─────────────────────────────────┘               │
│  ┌─────────────────────────────────┐               │
│  │         数据库 (共享)            │               │
│  └─────────────────────────────────┘               │
│                                                     │
│  微服务架构：                                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐              │
│  │ 用户服务 │ │ 订单服务 │ │ 支付服务 │              │
│  │  独立DB  │ │  独立DB  │ │  独立DB  │              │
│  └─────────┘ └─────────┘ └─────────┘              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐              │
│  │ 商品服务 │ │ 库存服务 │ │ 通知服务 │              │
│  │  独立DB  │ │  独立DB  │ │  独立DB  │              │
│  └─────────┘ └─────────┘ └─────────┘              │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

### 1.2 优缺点对比

| 维度 | 单体架构 | 微服务架构 |
|------|----------|------------|
| **开发速度** | 慢（代码量大） | 快（服务独立） |
| **部署** | 整体部署 | 独立部署 |
| **扩展** | 整体扩展 | 按需扩展 |
| **故障隔离** | 差 | 好 |
| **技术栈** | 统一 | 灵活 |
| **复杂度** | 低 | 高 |
| **运维成本** | 低 | 高 |
| **团队协作** | 冲突多 | 独立性强 |

### 1.3 适用场景

**适合微服务**：
- 大型团队（10+ 开发者）
- 复杂业务域
- 需要高频部署
- 需要弹性扩展

**适合单体**：
- 小型团队（< 5 开发者）
- 简单业务
- 快速起步
- MVP 原型

---

## Part 2: 服务拆分原则

### 2.1 领域驱动设计（DDD）

```python
"""
DDD 限界上下文
"""

# 上下文：电商
# 领域：用户、订单、支付、商品、库存

# 用户限界上下文
class UserService:
    """用户服务 - 边界：用户注册、认证、资料管理"""
    pass

# 订单限界上下文
class OrderService:
    """订单服务 - 边界：下单、取消、查询"""
    pass

# 支付限界上下文
class PaymentService:
    """支付服务 - 边界：支付、退款"""
    pass

# 商品限界上下文
class ProductService:
    """商品服务 - 边界：商品上架、搜索、详情"""
    pass

# 库存限界上下文
class InventoryService:
    """库存服务 - 边界：库存扣减、查询"""
    pass

# 注意：跨边界调用通过 API 进行，而不是直接调用
```

### 2.2 拆分粒度

| 粒度 | 服务示例 | 特点 |
|------|----------|------|
| **过粗** | 电商服务（一个服务包含所有） | 等同于单体 |
| **适中** | 用户、订单、支付、商品、库存 | 平衡复杂度和独立性 |
| **过细** | 用户注册、用户认证、用户资料 | 服务爆炸，难以维护 |

### 2.3 服务边界原则

1. **单一职责**：每个服务只负责一个业务领域
2. **高内聚**：相关功能在同一服务内
3. **低耦合**：服务间通过 API 通信，不共享数据库
4. **独立部署**：每个服务可以独立部署和扩展

---

## Part 3: 服务通信

### 3.1 同步通信 - REST

```python
# 用户服务 (端口 8001)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    email: str

# 模拟数据库
users_db = {}

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.post("/users", response_model=User)
async def create_user(user: User):
    users_db[user.id] = user
    return user

# 订单服务调用用户服务
import httpx

class OrderServiceClient:
    def __init__(self, user_service_url: str):
        self.user_service_url = user_service_url

    async def get_user(self, user_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.user_service_url}/users/{user_id}")
            if response.status_code == 404:
                raise ValueError(f"User {user_id} not found")
            response.raise_for_status()
            return response.json()

order_client = OrderServiceClient("http://localhost:8001")
user = await order_client.get_user(123)
```

### 3.2 同步通信 - gRPC

```protobuf
// user.proto
syntax = "proto3";

package user;

service UserService {
    rpc GetUser (GetUserRequest) returns (User);
    rpc CreateUser (CreateUserRequest) returns (User);
}

message GetUserRequest {
    int32 user_id = 1;
}

message CreateUserRequest {
    string username = 1;
    string email = 2;
}

message User {
    int32 id = 1;
    string username = 2;
    string email = 3;
}
```

```python
# 用户服务 (gRPC)
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        # 查询逻辑
        user = get_user_from_db(request.user_id)
        return user_pb2.User(
            id=user.id,
            username=user.username,
            email=user.email
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

### 3.3 异步通信 - 消息队列

```python
# 订单服务发布事件
import aio_pika

async def publish_order_created(order_id: int, user_id: int):
    connection = await aio_pika.connect_robust("amqp://localhost")
    channel = await connection.channel()

    message = aio_pika.Message(
        body=json.dumps({
            "event": "order.created",
            "order_id": order_id,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }).encode()
    )

    await channel.default_exchange.publish(
        message,
        routing_key="orders"
    )

# 通知服务订阅事件
async def consume_order_events():
    connection = await aio_pika.connect_robust("amqp://localhost")
    channel = await connection.channel()

    queue = await channel.declare_queue("notifications")
    await queue.consume(process_order_event)

async def process_order_event(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)

        if data["event"] == "order.created":
            # 发送订单确认邮件
            await send_confirmation_email(data["user_id"], data["order_id"])
        elif data["event"] == "order.cancelled":
            # 发送取消通知
            await send_cancellation_email(data["user_id"], data["order_id"])
```

### 3.4 异步通信 - Event-Driven

```python
# 使用 Redis Streams 实现事件驱动
import redis.asyncio as redis

class EventBus:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def publish(self, stream: str, event: dict):
        """发布事件"""
        await self.redis.xadd(stream, event)

    async def subscribe(self, stream: str, group: str, consumer: str):
        """订阅事件"""
        # 确保消费者组存在
        try:
            await self.redis.xgroup_create(stream, group, id="0", mkstream=True)
        except:
            pass

        # 读取新事件
        while True:
            messages = await self.redis.xreadgroup(
                group, consumer, {stream: ">"}, count=1
            )

            for stream_name, entries in messages:
                for message_id, data in entries:
                    yield message_id, data

# 使用
event_bus = EventBus("redis://localhost:6379")

# 发布事件
await event_bus.publish("order_events", {
    "type": "order.created",
    "order_id": 123,
    "user_id": 456
})

# 订阅事件
async for message_id, data in event_bus.subscribe("order_events", "notifications", "consumer-1"):
    if data["type"] == "order.created":
        await send_notification(data["user_id"])
        await event_bus.redis.xack("order_events", "notifications", message_id)
```

---

## Part 4: 服务发现

### 4.1 Consul 服务注册

```python
import consul.aio

class ConsulServiceRegistry:
    """Consul 服务注册"""

    def __init__(self, consul_host: str = "localhost", consul_port: int = 8500):
        self.consul = consul.aio.Consul(host=consul_host, port=consul_port)

    async def register(
        self,
        service_name: str,
        service_id: str,
        port: int,
        health_check: str = None
    ):
        """注册服务"""
        await self.consul.agent.service.register(
            name=service_name,
            service_id=service_id,
            port=port,
            check=health_check
        )

    async def deregister(self, service_id: str):
        """注销服务"""
        await self.consul.agent.service.deregister(service_id)

    async def discover(self, service_name: str) -> list[dict]:
        """发现服务实例"""
        _, services = await self.consul.health.service(service_name, passing=True)

        instances = []
        for service in services:
            instances.append({
                "id": service["Service"]["ID"],
                "name": service["Service"]["Service"],
                "host": service["Service"]["Address"],
                "port": service["Service"]["Port"]
            })

        return instances

# 使用
registry = ConsulServiceRegistry()

# 注册服务
await registry.register(
    service_name="user-service",
    service_id="user-service-1",
    port=8001,
    health_check="http://localhost:8001/health"
)

# 发现服务
instances = await registry.discover("user-service")
print(f"Found {len(instances)} instances")
```

### 4.2 客户端负载均衡

```python
import random

class LoadBalancer:
    """简单负载均衡器"""

    def __init__(self, registry: ConsulServiceRegistry):
        self.registry = registry
        self.cache = {}

    async def get_service_url(self, service_name: str) -> str:
        """获取服务 URL"""
        if service_name not in self.cache:
            instances = await self.registry.discover(service_name)
            self.cache[service_name] = instances

        instances = self.cache.get(service_name, [])
        if not instances:
            raise ValueError(f"No instances for {service_name}")

        # 随机负载均衡
        instance = random.choice(instances)
        return f"http://{instance['host']}:{instance['port']}"

    async def call_service(self, service_name: str, path: str):
        """调用服务"""
        url = await self.get_service_url(service_name)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}{path}")
            return response.json()
```

---

## Part 5: API 网关

### 5.1 网关架构

```
┌─────────────────────────────────────────────────────────┐
│                    API 网关架构                         │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  客户端 ──→ [API Gateway] ──→ 用户服务 (8001)        │
│                  │                                    │
│                  ├──→ 订单服务 (8002)                │
│                  │                                    │
│                  ├──→ 支付服务 (8003)                │
│                  │                                    │
│                  └──→ 商品服务 (8004)                │
│                                                     │
│  网关功能：                                         │
│  • 路由转发                                        │
│  • 认证授权                                        │
│  • 限流熔断                                        │
│  • 日志监控                                        │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

### 5.2 网关实现

```python
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import ProxyResponse
import httpx
import time

app = FastAPI()

# 服务路由配置
ROUTES = {
    "/api/users": "http://localhost:8001",
    "/api/orders": "http://localhost:8002",
    "/api/payments": "http://localhost:8003",
    "/api/products": "http://localhost:8004",
}

# 限流配置
RATE_LIMIT = 100  # 每秒请求数
request_counts = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """限流中间件"""
    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in request_counts:
        request_counts[client_ip] = []

    # 清理过期的请求记录
    request_counts[client_ip] = [
        t for t in request_counts[client_ip]
        if current_time - t < 1
    ]

    if len(request_counts[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    request_counts[client_ip].append(current_time)

    response = await call_next(request)
    return response

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(full_path: str, request: Request):
    """代理请求"""
    # 查找目标服务
    target_base = None
    for prefix, url in ROUTES.items():
        if full_path.startswith(prefix):
            target_base = url
            break

    if not target_base:
        raise HTTPException(status_code=404, detail="Route not found")

    # 构建目标 URL
    target_url = f"{target_base}/{full_path}"

    # 转发请求
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={k: v for k, v in request.headers.items()
                        if k.lower() not in ["host", "content-length"]},
                content=await request.body()
            )

            return ProxyResponse(
                status_code=response.status_code,
                content=response.content,
                headers=response.headers
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Service unavailable")
```

---

## Part 6: 配置管理

### 6.1 分布式配置中心

```python
import etcd3

class ConfigCenter:
    """分布式配置中心"""

    def __init__(self, etcd_host: str = "localhost", etcd_port: int = 2379):
        self.client = etcd3.client(host=etcd_host, port=etcd_port)
        self.watches = {}

    async def put(self, key: str, value: dict):
        """设置配置"""
        import json
        await self.client.put(key, json.dumps(value))

    async def get(self, key: str) -> dict:
        """获取配置"""
        import json
        value, _ = await self.client.get(key)
        if value:
            return json.loads(value)
        return {}

    async def watch(self, key: str, callback: callable):
        """监听配置变化"""
        events_iterator, cancel = await self.client.watch(key)

        async def watch_loop():
            async for event in events_iterator:
                if event.value:
                    import json
                    config = json.loads(event.value)
                    await callback(config)

        return watch_loop()

# 使用
config_center = ConfigCenter()

# 设置配置
await config_center.put("/config/user-service/database", {
    "host": "localhost",
    "port": 5432,
    "name": "users"
})

# 获取配置
db_config = await config_center.get("/config/user-service/database")
print(f"Database config: {db_config}")
```

### 6.2 服务配置

```python
from pydantic import BaseModel
from functools import lru_cache

class ServiceConfig(BaseModel):
    """服务配置"""
    service_name: str
    host: str
    port: int
    database_url: str
    redis_url: str
    log_level: str = "INFO"

    @classmethod
    async def load(cls, service_name: str) -> "ServiceConfig":
        """从配置中心加载配置"""
        config_center = ConfigCenter()
        data = await config_center.get(f"/config/{service_name}")
        return cls(**data)

@lru_cache()
def get_config() -> ServiceConfig:
    """获取配置（单例）"""
    # 同步方式：使用环境变量或本地配置
    return ServiceConfig(
        service_name="user-service",
        host="0.0.0.0",
        port=8001,
        database_url="postgresql://user:pass@localhost/users",
        redis_url="redis://localhost:6379"
    )
```

---

## Part 7: 服务间通信最佳实践

### 7.1 熔断器模式

```python
import asyncio
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # 正常
    OPEN = "open"          # 熔断
    HALF_OPEN = "half_open"  # 半开

class CircuitBreaker:
    """熔断器"""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    async def call(self, func, *args, **kwargs):
        """调用函数"""
        if self.state == CircuitState.OPEN:
            # 检查是否可以进入半开状态
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# 使用
breaker = CircuitBreaker(failure_threshold=5)

async def call_user_service(user_id: int):
    return await breaker.call(user_service_client.get_user, user_id)
```

### 7.2 重试策略

```python
import asyncio
from functools import wraps

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise

                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator

# 使用
@retry(max_attempts=3, delay=0.5, backoff=2.0, exceptions=(httpx.RequestError,))
async def call_service_with_retry(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

---

## Part 8: 监控与追踪

### 8.1 分布式追踪

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# 配置追踪
provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(JaegerExporter(agent_host_name="localhost"))
)
trace.set_tracer_provider(provider)

# 追踪服务调用
@app.api_route("/{full_path:path}")
async def traced_proxy(full_path: str, request: Request):
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("proxy_request") as span:
        span.set_attribute("http.path", f"/{full_path}")
        span.set_attribute("http.method", request.method)

        # 调用下游服务
        try:
            result = await proxy(full_path, request)
            span.set_attribute("http.status_code", 200)
            return result
        except Exception as e:
            span.set_attribute("http.status_code", 500)
            span.record_exception(e)
            raise
```

### 8.2 健康检查

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """健康检查"""
    checks = {
        "status": "healthy",
        "services": {}
    }

    # 检查依赖服务
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8001/health", timeout=2)
            checks["services"]["user_service"] = "up" if response.status_code == 200 else "down"
    except:
        checks["services"]["user_service"] = "down"
        checks["status"] = "degraded"

    return checks

@router.get("/ready")
async def readiness_check():
    """就绪检查"""
    # 检查数据库连接
    try:
        await db.execute("SELECT 1")
        return {"status": "ready"}
    except:
        raise HTTPException(status_code=503, detail="Database not ready")
```

---

## 📝 课程总结

### 核心知识点

1. **微服务基础**：微服务 vs 单体架构对比
2. **服务拆分**：DDD 限界上下文、拆分原则
3. **服务通信**：REST、gRPC、消息队列、事件驱动
4. **服务发现**：Consul、Etcd、客户端负载均衡
5. **API 网关**：路由转发、认证授权、限流熔断
6. **配置管理**：分布式配置中心
7. **最佳实践**：熔断器、重试策略、分布式追踪

### 关键要点

- ✅ 微服务适用于大型团队和复杂业务
- ✅ 服务间通过 API 通信，不共享数据库
- ✅ 异步通信提高系统解耦性
- ✅ 熔断器防止故障传播
- ✅ 分布式追踪帮助排查问题

---

## ✅ 完成标准

完成本课程后，你应该能够：

- [ ] 理解微服务架构核心概念
- [ ] 掌握服务拆分的原则和方法
- [ ] 实现同步和异步服务通信
- [ ] 使用服务发现机制
- [ ] 实现 API 网关
- [ ] 实现分布式配置管理
- [ ] 使用熔断器和重试策略

---

**下一步**: 继续学习 [L45: 分布式系统实战](../L45-distributed-systems/lesson.md)
