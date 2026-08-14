# L36: 异步背压机制 - 详细课程

> **课程编号**: L36
> **所属阶段**: Stage 4 - Web 开发进阶
> **预计时长**: 6 小时
> **难度**: ⭐⭐⭐⭐☆（高级）
> **前置课程**: L19, L27
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


## 📚 前置知识

学习本课程前，你应该已经掌握：

- **L19**: `asyncio`、协程、Task、TaskGroup、超时与取消
- **L22**: 高阶异步流控、任务编排、异步管道
- **L27**: FastAPI 基础接口、依赖注入、HTTP 状态码与可观测性

如果你还不能解释 `await`、`asyncio.Queue`、`asyncio.Semaphore` 和 `asyncio.timeout` 的行为，建议先回顾 L19。

---

```mermaid
flowchart TB
    subgraph Problem["背压问题"]
        A[流量升高] --> B[无限创建 Task]
        B --> C[无限堆积 Queue]
        C --> D[内存升高]
        D --> E[响应变慢]
        E --> F[调用方超时]
        F --> G[重试放大流量]
        G --> H[级联故障]
    end

    subgraph Solutions["背压机制"]
        I[并发限制<br/>Semaphore] --> J[保护资源]
        K[速率限制<br/>Token Bucket] --> J
        L[有界队列<br/>Queue(maxsize)] --> J
        M[超时控制<br/>asyncio.timeout] --> J
        N[重试策略<br/>指数退避] --> J
        O[熔断器<br/>CircuitBreaker] --> J
        P[服务降级<br/>Fallback] --> J
    end

    subgraph Result["保护效果"]
        Q[系统稳定] --> R[可预测延迟]
        R --> S[资源可控]
        S --> T[故障隔离]
    end

    style Problem fill:#ffcdd2
    style Solutions fill:#c8e6c9
    style Result fill:#e3f2fd
```

---

## 模块 1: 为什么异步系统必须有背压

### 1.1 背压的定义

**背压（Backpressure）** 是一种容量保护机制：当下游处理速度不足时，系统通过限流、排队、拒绝、降级或熔断等方式，把压力反馈给上游，避免资源被无限消耗。

没有背压的异步系统常见事故链路：

```text
流量升高
  ↓
无限创建 Task / 无限堆积 Queue
  ↓
内存升高、连接池耗尽、响应变慢
  ↓
调用方超时并重试
  ↓
流量进一步放大
  ↓
级联故障
```

### 1.2 背压不是单一算法

| 机制 | 解决的问题 | 常见动作 |
|------|------------|----------|
| 并发限制 | 同时工作太多 | `Semaphore`、连接池上限 |
| 速率限制 | 单位时间请求太多 | Token Bucket、滑动窗口 |
| 有界队列 | 生产速度大于消费速度 | 等待、拒绝、丢弃低优先级任务 |
| 超时 | 等待时间不可控 | `asyncio.timeout`、HTTP timeout |
| 重试 | 瞬时失败 | 指数退避、抖动、最大次数 |
| 熔断 | 下游持续失败 | 快速失败、半开探测、恢复 |
| 降级 | 保核心能力 | 返回缓存、简化结果、异步补偿 |

### 1.3 课程里的生产原则

本课所有实践遵循三个原则：

1. **容量有边界**：任何并发、队列、连接和重试都必须有上限。
2. **等待有期限**：任何等待都要有超时，不能无限挂起。
3. **失败可观测**：拒绝、超时、熔断、降级都要能被指标和日志看见。

---

## 模块 2: 容量预算与异步瓶颈识别

### 2.1 容量预算四要素

设计一个异步接口时，先回答四个问题：

| 问题 | 示例 |
|------|------|
| 入口速率是多少？ | 100 req/s |
| 单请求平均耗时是多少？ | 200 ms |
| 最大并发应该是多少？ | 100 × 0.2 = 20 个并发 |
| 超过容量时怎么处理？ | 排队 1 秒，超时后返回 429/503 |

### 2.2 Little's Law 的直觉

```text
并发量 ≈ 到达速率 × 平均响应时间
```

如果接口平均耗时 500 ms，入口是 200 req/s，那么系统中平均会有约 100 个请求同时存在。连接池、线程池、队列和下游服务都必须围绕这个数字设计。

### 2.3 常见危险信号

- `asyncio.gather(*huge_list)` 一次性创建大量 Task
- `asyncio.Queue()` 没有 `maxsize`
- HTTP 客户端没有连接池上限和超时
- 数据库连接池上限大于数据库可承受连接数
- 重试没有最大次数、没有退避、没有抖动
- 限流只在网关层做，应用内部没有保护

---

## 模块 3: Semaphore 控制并发上限

### 3.1 最小并发控制

`asyncio.Semaphore` 用于限制同时进入某段关键区域的协程数量。

```python
import asyncio

async def bounded_worker(semaphore: asyncio.Semaphore, task_id: int) -> str:
    async with semaphore:
        await asyncio.sleep(0.1)
        return f"task-{task_id}-done"

async def main() -> list[str]:
    semaphore = asyncio.Semaphore(3)
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(bounded_worker(semaphore, i)) for i in range(10)]
    return [task.result() for task in tasks]
```

### 3.2 入口并发保护

在 Web 服务中，Semaphore 常用于保护 CPU 密集段、下游 API、数据库写入或文件处理。

```python
import asyncio
from fastapi import HTTPException, status

processor_limit = asyncio.Semaphore(20)

async def handle_expensive_request() -> dict[str, str]:
    try:
        async with asyncio.timeout(2.0):
            async with processor_limit:
                await asyncio.sleep(0.2)
                return {"status": "ok"}
    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="service is busy, retry later",
        )
```

### 3.3 Semaphore 的边界

Semaphore 只限制“同时执行数量”，不限制单位时间速率。如果任务很短，仍可能产生很高 QPS；如果任务很长，请求会排队等待。因此生产系统通常把 Semaphore 与超时、队列和速率限制组合使用。

---

## 模块 4: 有界 Queue 构建生产者-消费者背压

### 4.1 为什么队列必须有 maxsize

无界队列会把下游处理能力不足转换成内存膨胀。生产环境应默认使用有界队列。

```python
import asyncio

queue: asyncio.Queue[str] = asyncio.Queue(maxsize=100)

async def producer(item: str) -> bool:
    try:
        await asyncio.wait_for(queue.put(item), timeout=0.5)
        return True
    except TimeoutError:
        return False

async def consumer() -> None:
    while True:
        item = await queue.get()
        try:
            await process(item)
        finally:
            queue.task_done()
```

### 4.2 队列满时的策略

| 策略 | 适用场景 | 风险 |
|------|----------|------|
| 等待 | 用户可接受短暂延迟 | 延迟升高 |
| 直接拒绝 | API 请求、同步任务 | 调用方需处理 429/503 |
| 丢弃旧任务 | 指标、日志、实时状态 | 数据可能不完整 |
| 丢弃低优先级 | 多优先级任务 | 需要优先级设计 |
| 写入持久队列 | 订单、支付、审计 | 系统复杂度升高 |

### 4.3 队列指标

生产环境至少监控：

- `queue_size`
- `queue_capacity`
- `enqueue_wait_seconds`
- `dequeue_lag_seconds`
- `dropped_total`
- `rejected_total`

---

## 模块 5: Token Bucket 速率限制

### 5.1 算法直觉

Token Bucket 允许稳定速率和短暂突发：桶按固定速率补充 token，请求消耗 token。桶空时，请求等待或被拒绝。

```python
import asyncio
import time
from dataclasses import dataclass, field

@dataclass
class TokenBucket:
    capacity: float
    rate: float
    tokens: float = field(init=False)
    last_update: float = field(init=False)

    def __post_init__(self) -> None:
        self.tokens = self.capacity
        self.last_update = time.monotonic()

    def refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now

    async def acquire(self, cost: float = 1.0) -> None:
        while True:
            self.refill()
            if self.tokens >= cost:
                self.tokens -= cost
                return
            await asyncio.sleep((cost - self.tokens) / self.rate)
```

### 5.2 适用场景

Token Bucket 适合：

- 调用第三方 API 的客户端限速
- 对内部昂贵操作做速率平滑
- 允许短暂突发但限制长期平均速率

不适合单独解决：

- 下游持续超时
- 数据库连接池耗尽
- 请求内部创建大量子任务

---

## 模块 6: 滑动窗口限流

### 6.1 固定窗口的问题

固定窗口可能在窗口边界产生双倍突发。例如每分钟 60 次，请求可能集中在第 59 秒和下一分钟第 1 秒。

### 6.2 滑动窗口实现

```python
import asyncio
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: float) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def acquire(self) -> bool:
        async with self._lock:
            now = time.monotonic()
            while self.requests and self.requests[0] <= now - self.window_seconds:
                self.requests.popleft()
            if len(self.requests) >= self.max_requests:
                return False
            self.requests.append(now)
            return True
```

### 6.3 与 Token Bucket 的选择

| 算法 | 优点 | 适合 |
|------|------|------|
| Token Bucket | 支持突发、实现简单 | API 客户端、全局 QPS 控制 |
| 滑动窗口 | 边界更平滑、统计直观 | 用户级限流、租户级配额 |
| 漏桶 | 输出稳定 | 消息发送、平滑写入 |

---

## 模块 7: 超时、取消与快速失败

### 7.1 为什么超时是背压的一部分

没有超时的等待会占住并发槽、连接、内存和调用方耐心。超时可以把“无限等待”变成“可观察的失败”。

```python
import asyncio

async def call_downstream() -> dict[str, str]:
    await asyncio.sleep(0.2)
    return {"status": "ok"}

async def safe_call() -> dict[str, str]:
    try:
        async with asyncio.timeout(1.0):
            return await call_downstream()
    except TimeoutError:
        return {"status": "timeout"}
```

### 7.2 取消传播

异步任务被取消时要释放资源：

```python
async def worker(semaphore: asyncio.Semaphore) -> None:
    async with semaphore:
        try:
            await long_running_job()
        finally:
            await cleanup()
```

### 7.3 超时预算

一次请求经过多个下游时，总超时不能简单叠加。推荐从入口 SLA 倒推：

```text
入口 SLA 2s
├─ 鉴权 100ms
├─ 数据库 500ms
├─ 外部 API 800ms
├─ 聚合渲染 300ms
└─ 预留 300ms
```

---

## 模块 8: 重试、指数退避与熔断

### 8.1 错误的重试会放大故障

如果服务已经过载，无退避重试会把 1 次失败变成 N 次额外请求。生产重试必须具备：

- 最大次数
- 指数退避
- 随机抖动
- 只重试可恢复错误
- 与熔断器配合

```python
import asyncio
import random
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")

async def retry_with_backoff(func: Callable[[], Awaitable[T]], attempts: int = 3) -> T:
    last_error: Exception | None = None
    for index in range(attempts):
        try:
            return await func()
        except TimeoutError as exc:
            last_error = exc
            delay = 0.1 * (2**index) + random.uniform(0, 0.05)
            await asyncio.sleep(delay)
    raise RuntimeError("retry exhausted") from last_error
```

### 8.2 熔断器状态

```text
CLOSED    正常调用，统计失败
OPEN      快速失败，不再打下游
HALF_OPEN 放少量探测请求，成功则恢复，失败则继续熔断
```

### 8.3 熔断与限流的关系

- 限流解决“请求太多”
- 熔断解决“下游不可用”
- 降级解决“核心能力要保住”

三者经常同时出现。

---

## 模块 9: FastAPI 生产接口中的背压组合

### 9.1 推荐组合

```text
入口请求
  ↓
用户/租户级滑动窗口限流
  ↓
全局 Semaphore 并发限制
  ↓
有界 Queue 或连接池
  ↓
下游调用超时
  ↓
可恢复错误重试
  ↓
持续失败熔断
  ↓
指标、日志、告警
```

### 9.2 HTTP 状态码建议

| 状态码 | 场景 |
|--------|------|
| 429 Too Many Requests | 调用方超过配额或限流阈值 |
| 503 Service Unavailable | 服务当前过载、熔断或依赖不可用 |
| 504 Gateway Timeout | 上游网关等待下游超时 |
| 202 Accepted | 请求已接收，转入异步处理 |

### 9.3 返回 Retry-After

```python
from fastapi import HTTPException, status

raise HTTPException(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="rate limit exceeded",
    headers={"Retry-After": "2"},
)
```

---

## 模块 10: 观测、压测与调参

### 10.1 必备指标

| 指标 | 说明 |
|------|------|
| `inflight_requests` | 当前并发请求数 |
| `queue_depth` | 队列长度 |
| `queue_wait_seconds` | 入队等待时间 |
| `rate_limited_total` | 被限流请求数 |
| `timeout_total` | 超时次数 |
| `circuit_state` | 熔断器状态 |
| `retry_total` | 重试次数 |
| `downstream_latency_seconds` | 下游延迟 |

### 10.2 压测观察顺序

1. 低流量下确认功能正确。
2. 逐步升高 QPS，找到延迟拐点。
3. 观察队列长度是否持续增长。
4. 观察 429/503 是否按预期出现。
5. 注入下游超时，确认熔断和恢复。
6. 调整 Semaphore、队列长度、超时和重试次数。

### 10.3 调参经验

- 并发上限不要超过下游真实容量。
- 队列长度越大，越容易隐藏问题并增加尾延迟。
- 超时应小于调用方超时，避免调用方已放弃而服务仍在工作。
- 重试次数越多，越要降低并发或引入熔断。
- 对用户请求优先快速失败，对后台任务可排队和补偿。

---


### 模块 11: 生产级背压最佳实践

#### 11.1 分层背压架构

```python
"""
分层背压策略：

Layer 1: 网关层（nginx/云网关）
- 限制总 QPS
- 基于 IP/用户维度的限流

Layer 2: API 网关（Kong/Traefik）
- 路由级限流
- 服务级熔断
- 重试策略配置

Layer 3: 应用层（FastAPI/ASGI）
- 租户级滑动窗口
- 全局 Semaphore
- 有界 Queue

Layer 4: 基础设施层
- 连接池大小
- 数据库连接限制
- Redis 连接限制
"""

# FastAPI 应用层背压实现
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import time

app = FastAPI()

# 全局限流：使用 Redis 分布式限流
from redis import Redis
from datetime import datetime

redis_client = Redis(host="localhost", port=6379, decode_responses=True)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """全局限流中间件"""
    client_id = request.client.host if request.client else "unknown"
    key = f"rate_limit:{client_id}"
    
    # 滑动窗口限流
    now = time.time()
    window = 60  # 60秒窗口
    
    # 移除窗口外的记录
    redis_client.zremrangebyscore(key, 0, now - window)
    
    # 获取当前请求数
    current_count = redis_client.zcard(key)
    
    if current_count >= 100:  # 每分钟最多 100 请求
        return JSONResponse(
            status_code=429,
            content={"detail": "rate limit exceeded"},
            headers={"Retry-After": "60"},
        )
    
    # 添加当前请求
    redis_client.zadd(key, {str(now): now})
    redis_client.expire(key, window + 1)
    
    response = await call_next(request)
    return response
```

#### 11.2 自适应限流

```python
"""
自适应限流策略：
- 根据系统负载动态调整限流阈值
- 使用移动平均算法平滑流量波动
- 负载指标：CPU、内存、延迟、队列深度
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Callable
import psutil


@dataclass
class AdaptiveRateLimiter:
    """自适应限流器"""
    
    base_rate: int = 100  # 基础 QPS
    min_rate: int = 10    # 最小 QPS
    max_rate: int = 1000  # 最大 QPS
    
    # 负载指标
    target_cpu: float = 0.7      # 目标 CPU 使用率
    target_latency: float = 0.5  # 目标 P99 延迟（秒）
    
    # 滑动窗口
    latency_window: list = field(default_factory=list)
    window_size: int = 100
    
    # 调整参数
    adjustment_factor: float = 0.1  # 每次调整 10%
    adjustment_interval: float = 5.0  # 每 5 秒调整一次
    
    _current_rate: int = field(init=False)
    _last_adjustment: float = field(init=False)
    
    def __post_init__(self):
        self._current_rate = self.base_rate
        self._last_adjustment = time.time()
    
    def record_latency(self, latency: float):
        """记录延迟"""
        self.latency_window.append(latency)
        if len(self.latency_window) > self.window_size:
            self.latency_window.pop(0)
    
    def get_p99_latency(self) -> float:
        """计算 P99 延迟"""
        if not self.latency_window:
            return 0.0
        sorted_latencies = sorted(self.latency_window)
        idx = int(len(sorted_latencies) * 0.99)
        return sorted_latencies[min(idx, len(sorted_latencies) - 1)]
    
    def get_cpu_usage(self) -> float:
        """获取 CPU 使用率"""
        return psutil.cpu_percent() / 100.0
    
    async def adjust_rate(self):
        """根据负载调整速率"""
        now = time.time()
        if now - self._last_adjustment < self.adjustment_interval:
            return
        
        cpu = self.get_cpu_usage()
        p99 = self.get_p99_latency()
        
        # 计算调整方向
        increase = True
        if cpu > self.target_cpu or p99 > self.target_latency:
            increase = False
        
        # 计算新速率
        if increase:
            new_rate = int(self._current_rate * (1 + self.adjustment_factor))
        else:
            new_rate = int(self._current_rate * (1 - self.adjustment_factor))
        
        # 限制在范围内
        self._current_rate = max(self.min_rate, min(self.max_rate, new_rate))
        self._last_adjustment = now
    
    @property
    def current_rate(self) -> int:
        return self._current_rate


# 使用示例
limiter = AdaptiveRateLimiter(base_rate=100)


async def handle_request():
    start = time.time()
    try:
        # 处理请求
        await asyncio.sleep(0.1)
        latency = time.time() - start
        limiter.record_latency(latency)
    finally:
        # 定期调整限流
        await limiter.adjust_rate()
```

#### 11.3 背压监控告警

```python
"""
背压监控指标与告警规则

关键指标：
1. 请求延迟 (P50/P95/P99)
2. 队列深度
3. 拒绝率
4. 熔断器状态
5. 资源使用率

告警规则示例：
- P99 延迟 > 2s，持续 5 分钟
- 拒绝率 > 5%
- 熔断器打开
"""

from prometheus_client import Counter, Gauge, Histogram
import time

# 定义指标
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0],
)

QUEUE_DEPTH = Gauge(
    "queue_depth",
    "Current queue depth",
    ["queue_name"],
)

REJECTED_REQUESTS = Counter(
    "rejected_requests_total",
    "Total number of rejected requests",
    ["reason"],  # rate_limit, circuit_breaker, timeout
)

CIRCUIT_BREAKER_STATE = Gauge(
    "circuit_breaker_state",
    "Circuit breaker state (0=closed, 1=half-open, 2=open)",
    ["service"],
)


# 监控中间件示例
@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start = time.time()
    endpoint = request.url.path
    
    try:
        response = await call_next(request)
        latency = time.time() - start
        
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        
        return response
    except HTTPException as e:
        latency = time.time() - start
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        
        if e.status_code == 429:
            REJECTED_REQUESTS.labels(reason="rate_limit").inc()
        elif e.status_code == 503:
            REJECTED_REQUESTS.labels(reason="circuit_breaker").inc()
        
        raise
```

### 模块 12: 背压故障排查指南

#### 12.1 常见问题诊断

```python
"""
背压问题诊断流程：

1. 识别症状
   - 请求延迟增加
   - 超时增加
   - 拒绝率上升

2. 定位瓶颈
   - 检查队列深度
   - 检查 CPU/内存
   - 检查下游服务延迟

3. 根因分析
   - 是流量突增？
   - 是下游变慢？
   - 是资源不足？
"""

# 诊断脚本示例
import asyncio
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class BackpressureDiagnosis:
    """背压诊断结果"""
    queue_depth: int
    in_flight_requests: int
    avg_latency: float
    p99_latency: float
    rejection_rate: float
    cpu_usage: float
    memory_usage: float
    
    def summary(self) -> str:
        return f"""
背压诊断报告
============
队列深度: {self.queue_depth}
在途请求: {self.in_flight_requests}
平均延迟: {self.avg_latency:.3f}s
P99 延迟: {self.p99_latency:.3f}s
拒绝率: {self.rejection_rate:.1%}
CPU 使用: {self.cpu_usage:.1%}
内存使用: {self.memory_usage:.1%}

建议:
{'⚠️ 队列积压，可能需要扩容' if self.queue_depth > 100 else '✅ 队列正常'}
{'⚠️ 延迟过高，检查下游服务' if self.p99_latency > 1.0 else '✅ 延迟正常'}
{'⚠️ 拒绝率过高，检查限流配置' if self.rejection_rate > 0.05 else '✅ 拒绝率正常'}
{'⚠️ CPU 负载高，考虑优化或扩容' if self.cpu_usage > 0.8 else '✅ CPU 正常'}
"""


async def diagnose_backpressure(
    queue_depth_func: callable,
    in_flight_func: callable,
    latency_func: callable,
) -> BackpressureDiagnosis:
    """执行背压诊断"""
    # 收集指标
    qd = queue_depth_func()
    ifr = in_flight_func()
    
    # 收集延迟数据
    latencies = []
    for _ in range(100):
        lat = latency_func()
        latencies.append(lat)
        await asyncio.sleep(0.01)
    
    avg_lat = sum(latencies) / len(latencies)
    p99_lat = sorted(latencies)[int(len(latencies) * 0.99)]
    
    # 收集资源指标
    cpu = psutil.cpu_percent() / 100
    mem = psutil.virtual_memory().percent / 100
    
    return BackpressureDiagnosis(
        queue_depth=qd,
        in_flight_requests=ifr,
        avg_latency=avg_lat,
        p99_latency=p99_lat,
        rejection_rate=0.02,  # 从监控系统获取
        cpu_usage=cpu,
        memory_usage=mem,
    )
```

#### 12.2 背压调优参数

```python
"""
背压参数调优指南

1. Semaphore 并发数
   - 初始值: CPU 核心数 * 2
   - 调整依据: 延迟和吞吐量曲线

2. 队列大小
   - 初始值: 预期 QPS * 预期处理时间 * 2
   - 调整依据: 队列积压和拒绝率

3. 超时时间
   - 初始值: P99 延迟 * 2
   - 调整依据: 下游服务延迟分布

4. 熔断阈值
   - 错误率: 50% 持续 10 秒
   - 半开试探: 10% 流量
   - 恢复时间: 30 秒
"""

from dataclasses import dataclass


@dataclass
class BackpressureConfig:
    """背压配置"""
    # Semaphore 配置
    max_concurrent: int = 100
    semaphore_timeout: float = 30.0
    
    # 队列配置
    queue_size: int = 1000
    queue_timeout: float = 60.0
    
    # 限流配置
    rate_limit_rps: int = 100
    rate_limit_window: int = 60
    
    # 超时配置
    default_timeout: float = 5.0
    slow_request_threshold: float = 2.0
    
    # 熔断配置
    circuit_breaker_threshold: float = 0.5  # 50% 错误率
    circuit_breaker_window: int = 10  # 10 秒窗口
    circuit_breaker_recovery: int = 30  # 30 秒恢复
    
    @classmethod
    def from_env(cls) -> "BackpressureConfig":
        """从环境变量加载配置"""
        import os
        return cls(
            max_concurrent=int(os.getenv("MAX_CONCURRENT", "100")),
            queue_size=int(os.getenv("QUEUE_SIZE", "1000")),
            rate_limit_rps=int(os.getenv("RATE_LIMIT_RPS", "100")),
        )
```

#### 12.3 背压测试策略

```python
"""
背压测试策略

1. 单元测试
   - 测试单个限流器
   - 测试熔断器状态转换
   - 测试队列满时的行为

2. 集成测试
   - 测试限流 + 熔断组合
   - 测试超时 + 重试组合
   - 测试背压传播

3. 压力测试
   - 逐步增加负载
   - 测试背压触发
   - 测试恢复行为
"""

import pytest
import asyncio
from backpressure import (
    RateLimiter,
    CircuitBreaker,
    SemaphoreLimiter,
)


@pytest.mark.asyncio
async def test_rate_limiter_backpressure():
    """测试限流器背压"""
    limiter = RateLimiter(rate=10, window=1)  # 每秒 10 个请求
    
    # 前 10 个请求应该通过
    for _ in range(10):
        result = await limiter.acquire()
        assert result is True
    
    # 第 11 个请求应该被限流
    result = await limiter.acquire()
    assert result is False


@pytest.mark.asyncio
async def test_circuit_breaker_states():
    """测试熔断器状态转换"""
    cb = CircuitBreaker(
        failure_threshold=5,
        recovery_timeout=1,
    )
    
    # 初始状态：关闭
    assert cb.state == "closed"
    
    # 触发熔断
    for _ in range(6):
        await cb.record_failure()
    
    assert cb.state == "open"
    
    # 等待恢复
    await asyncio.sleep(1.5)
    
    # 状态变为半开
    assert cb.state == "half-open"


@pytest.mark.asyncio
async def test_semaphore_backpressure():
    """测试 Semaphore 背压"""
    limiter = SemaphoreLimiter(max_concurrent=2)
    
    # 获取两个许可
    async with limiter.acquire():
        async with limiter.acquire():
            # 此时没有可用许可
            # 使用 wait_for 测试超时
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(
                    limiter.acquire(),
                    timeout=0.1,
                )
```

### 模块 13: 背压与 Kubernetes

#### 13.1 Kubernetes 资源限制

```yaml
# Kubernetes Deployment 配置示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: app
          resources:
            # 资源请求（保证的最小资源）
            requests:
              memory: "256Mi"
              cpu: "250m"
            # 资源限制（最大可用资源）
            limits:
              memory: "512Mi"
              cpu: "500m"
```

#### 13.2 HPA 背压配置

```yaml
# Horizontal Pod Autoscaler 配置
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
    # 基于 CPU 自动扩缩容
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    
    # 基于自定义指标自动扩缩容
    - type: Pods
      pods:
        metric:
          name: queue_depth
        target:
          type: AverageValue
          averageValue: "100"
```

#### 13.3 服务网格背压

```yaml
# Istio VirtualService 限流配置
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
    - my-service
  http:
    - route:
        - destination:
            host: my-service
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: gateway-error,connect-failure,refused-stream
      timeout: 10s
    - match:
        - headers:
            x-api-key:
              regex: ".*"
      route:
        - destination:
            host: my-service
      rateLimit:
        rules:
          - destinations:
              - destination:
                  host: my-service
            rateLimitByDestination:
              requestsPerUnit: 100
              unit: minute
```

### 模块 14: 面试题精选

#### 14.1 背压概念理解

```python
"""
Q: 什么是背压？为什么需要背压？

A: 背压（Backpressure）是系统在负载过高时的一种自我保护机制。
   当下游处理能力不足时，限制上游的请求发送速度，防止系统过载崩溃。

为什么需要背压：
1. 防止资源耗尽（内存、连接数）
2. 保护下游服务不被压垮
3. 提供更好的用户体验（有控制的失败 vs 无响应的超时）
4. 实现系统稳定性
"""

"""
Q: 背压和限流有什么区别？

A: 背压是系统级的自我保护机制，包括限流但不仅限于限流：
- 背压 = 限流 + 熔断 + 队列控制 + 超时 + 重试
- 限流只是背压策略的一种实现

背压的目标是保护整个系统的稳定性
限流的目标是控制资源使用
"""
```

#### 14.2 背压实现方案

```python
"""
Q: 有哪些常见的背压实现方案？

A: 常见的背压实现方案：

1. 队列背压（有界队列）
   - 当队列满时阻塞生产者
   - 优点：实现简单
   - 缺点：可能导致死锁

2. 信号量背压
   - 使用 Semaphore 控制并发数
   - 优点：精确控制
   - 缺点：不能区分不同类型的请求

3. 滑动窗口限流
   - 在时间窗口内限制请求数
   - 优点：流量平滑
   - 缺点：实现较复杂

4. Token Bucket
   - 按固定速率发放令牌
   - 优点：允许突发流量
   - 缺点：实现较复杂

5. 熔断器
   - 当错误率过高时快速失败
   - 优点：保护下游
   - 缺点：需要正确的阈值配置
"""
```

#### 14.3 背压在微服务中的应用

```python
"""
Q: 在微服务架构中，背压是如何传递的？

A: 背压在微服务间通过以下方式传递：

1. HTTP 响应头
   - Retry-After: 建议客户端等待时间
   - X-RateLimit-Remaining: 剩余配额
   - X-RateLimit-Reset: 配额重置时间

2. 错误码传播
   - 429 Too Many Requests
   - 503 Service Unavailable
   - 504 Gateway Timeout

3. gRPC 状态码
   - RESOURCE_EXHAUSTED (8)
   - UNAVAILABLE (14)

4. 消息队列
   - 队列满时拒绝生产
   - 消费者慢时背压生产者
"""

# 客户端重试策略示例
import asyncio
from typing import TypeVar, Callable
import random

T = TypeVar("T")


async def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
) -> T:
    """带背压感知的重试"""
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            
            if attempt == max_retries:
                raise
            
            # 检查是否应该等待
            if hasattr(e, "retry_after"):
                delay = e.retry_after
            else:
                # 指数退避 + 抖动
                delay = min(base_delay * (2 ** attempt), max_delay)
                delay += random.uniform(0, delay * 0.1)
            
            await asyncio.sleep(delay)
    
    raise last_exception
```



---

## 📝 练习题

### 练习 1: 自适应限流器

实现一个根据响应时间动态调整速率的限流器：

- 响应时间 > 1s：降低 10% 速率
- 响应时间 < 500ms：提高 5% 速率
- 速率必须有最小值和最大值
- 调整动作需要记录日志或指标

### 练习 2: 有界任务管道

实现一个生产者-消费者管道：

- 队列必须设置 `maxsize`
- 生产者入队等待超过 500ms 时返回失败
- 消费者处理失败时要记录并继续消费
- 提供 `queue_depth` 和 `dropped_total` 指标

### 练习 3: 受保护的下游 API 客户端

封装一个 API 客户端：

- 全局并发不超过 20
- 单租户每分钟不超过 60 次
- 单次请求超时 1s
- 最多重试 2 次，使用指数退避
- 连续失败 5 次后熔断 30s

---

## ✅ 完成标准

- [ ] 能解释背压与限流、熔断、降级的区别
- [ ] 能写出 Semaphore 并发保护代码
- [ ] 能写出有界 Queue 生产者-消费者模型
- [ ] 能实现 Token Bucket 或滑动窗口限流
- [ ] 能为 FastAPI 接口选择合适的 429/503/202 返回策略
- [ ] 能设计超时、重试、熔断的组合策略
- [ ] 能列出背压相关核心指标
- [ ] 通过本课测试：`uv run --extra dev pytest stage4-web-advanced/lessons/L36-async-backpressure/tests -q`

## 🔗 下一步

- **L37 Web 安全完整指南**：在容量保护基础上处理认证、授权、输入与攻击面
- **L38 E2E 测试**：通过浏览器级测试验证限流与错误体验
- **L39 API 性能优化**：用压测、profiling 和缓存继续优化性能
