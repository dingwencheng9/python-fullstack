# A17: Agent 流水线

> **课程编号**: A17
> **所属阶段**: Stage A - AI Agent 企业级 (Specialization)
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: A05
> **版本**: v5.0
> **最后更新**: 2026-07-23

---

## 📌 学习目标

完成本课程后，你将能够：

1. **任务编排与异步处理**
2. 理解核心概念和实现原理
3. 掌握生产环境最佳实践

---

## Part 1: 核心概念

### 1.1 问题背景

任务编排与异步处理是 Agent 生产部署中的关键能力。

### 1.2 技术架构

```python
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class AgentConfig:
    """Agent 配置"""
    enabled: bool = True
    timeout: int = 30
    max_retries: int = 3
    cache_enabled: bool = True


@dataclass
class AgentRequest:
    """Agent 请求"""
    request_id: str
    user_id: str
    content: str
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentResponse:
    """Agent 响应"""
    request_id: str
    status: Status
    result: Optional[Any] = None
    error: Optional[str] = None
    processing_time: float = 0.0
```

---

## Part 2: 实现方案

### 2.1 核心实现

```python
import asyncio
from typing import Callable, Optional


class AgentCore:
    """Agent 核心类"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.cache = {}
        self.metrics = {"total": 0, "success": 0, "failed": 0}

    async def process(self, request: AgentRequest) -> AgentResponse:
        """处理请求"""
        start_time = time.time()
        self.metrics["total"] += 1

        try:
            # 1. 输入验证
            if not self.validate(request):
                raise ValueError("Invalid request")

            # 2. 检查缓存
            if self.config.cache_enabled:
                cached = self.get_from_cache(request)
                if cached:
                    return cached

            # 3. 执行处理
            result = await self.execute(request)

            # 4. 更新缓存
            if self.config.cache_enabled:
                self.update_cache(request, result)

            self.metrics["success"] += 1

            return AgentResponse(
                request_id=request.request_id,
                status=Status.SUCCESS,
                result=result,
                processing_time=time.time() - start_time,
            )

        except Exception as e:
            self.metrics["failed"] += 1
            return AgentResponse(
                request_id=request.request_id,
                status=Status.FAILED,
                error=str(e),
                processing_time=time.time() - start_time,
            )

    def validate(self, request: AgentRequest) -> bool:
        """验证请求"""
        return bool(request.content and request.user_id)

    def get_from_cache(self, request: AgentRequest) -> Optional[AgentResponse]:
        """获取缓存"""
        key = self._cache_key(request)
        return self.cache.get(key)

    def update_cache(self, request: AgentRequest, result: Any):
        """更新缓存"""
        key = self._cache_key(request)
        self.cache[key] = result

    def _cache_key(self, request: AgentRequest) -> str:
        """生成缓存键"""
        return f"{request.user_id}:{hash(request.content)}"

    async def execute(self, request: AgentRequest) -> Any:
        """执行处理 - 子类实现"""
        raise NotImplementedError
```

### 2.2 高级特性

```python
class AdvancedAgent(AgentCore):
    """高级 Agent 实现"""

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.rate_limiter = RateLimiter(rate=100, per=60)
        self.circuit_breaker = CircuitBreaker()

    async def process(self, request: AgentRequest) -> AgentResponse:
        """带保护的处理"""
        # 1. 速率限制检查
        if not await self.rate_limiter.acquire(request.user_id):
            return AgentResponse(
                request_id=request.request_id,
                status=Status.FAILED,
                error="Rate limit exceeded",
            )

        # 2. 熔断器检查
        if self.circuit_breaker.is_open():
            return AgentResponse(
                request_id=request.request_id,
                status=Status.FAILED,
                error="Service temporarily unavailable",
            )

        # 3. 执行处理
        response = await super().process(request)

        # 4. 更新熔断器状态
        self.circuit_breaker.record(response.status == Status.SUCCESS)

        return response


class RateLimiter:
    """速率限制器"""

    def __init__(self, rate: int, per: float):
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
        self.user_tokens: dict[str, float] = {}

    async def acquire(self, user_id: str) -> bool:
        """获取令牌"""
        current = time.time()
        elapsed = current - self.last_check
        self.last_check = current

        if user_id not in self.user_tokens:
            self.user_tokens[user_id] = self.rate

        self.user_tokens[user_id] += elapsed * (self.rate / self.per)
        self.user_tokens[user_id] = min(self.user_tokens[user_id], self.rate)

        if self.user_tokens[user_id] < 1.0:
            return False

        self.user_tokens[user_id] -= 1.0
        return True


class CircuitBreaker:
    """熔断器"""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0.0
        self.state = "closed"  # closed, open, half_open

    def is_open(self) -> bool:
        """检查是否熔断"""
        if self.state == "closed":
            return False
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half_open"
                return False
            return True
        return False

    def record(self, success: bool):
        """记录执行结果"""
        if success:
            self.failures = 0
            self.state = "closed"
        else:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "open"
```

---

## Part 3: 生产实践

### 3.1 监控指标

```python
from prometheus_client import Counter, Histogram, Gauge


# 指标定义
agent_requests = Counter(
    "agent_requests_total",
    "Total requests",
    ["status"],
)

agent_latency = Histogram(
    "agent_latency_seconds",
    "Agent processing latency",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
)

agent_errors = Counter(
    "agent_errors_total",
    "Total errors",
    ["error_type"],
)

active_requests = Gauge(
    "agent_active_requests",
    "Number of active requests",
)
```

### 3.2 日志记录

```python
import structlog

logger = structlog.get_logger()


class LoggedAgent(AdvancedAgent):
    """带日志的 Agent"""

    async def process(self, request: AgentRequest) -> AgentResponse:
        """带完整日志的处理"""
        logger.info(
            "agent_request_start",
            request_id=request.request_id,
            user_id=request.user_id,
        )

        try:
            response = await super().process(request)

            if response.status == Status.SUCCESS:
                logger.info(
                    "agent_request_success",
                    request_id=request.request_id,
                    processing_time=response.processing_time,
                )
            else:
                logger.error(
                    "agent_request_failed",
                    request_id=request.request_id,
                    error=response.error,
                )

            return response

        except Exception as e:
            logger.exception(
                "agent_request_exception",
                request_id=request.request_id,
                error=str(e),
            )
            raise
```

---

## Part 4: 最佳实践

### 4.1 配置建议

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| timeout | 30s | 单次请求超时 |
| max_retries | 3 | 最大重试次数 |
| cache_ttl | 3600s | 缓存有效期 |
| rate_limit | 100/min | 用户速率限制 |

### 4.2 性能优化

```python
# 1. 使用连接池
self.http_client = httpx.AsyncClient(
    timeout=30.0,
    limits=httpx.Limits(max_keepalive_connections=20),
)

# 2. 批量处理
async def batch_process(self, requests: list[AgentRequest]) -> list[AgentResponse]:
    """批量处理请求"""
    tasks = [self.process(req) for req in requests]
    return await asyncio.gather(*tasks, return_exceptions=True)

# 3. 流式处理
async def stream_process(self, request: AgentRequest) -> AsyncGenerator[str]:
    """流式处理响应"""
    async for chunk in self._stream_execute(request):
        yield chunk
```

---

## 💡 常见陷阱

### 陷阱 1: 忽略错误处理

```python
# ❌ 错误：捕获所有异常但不处理
try:
    result = await agent.process(request)
except Exception as e:
    pass  # 静默忽略

# ✅ 正确：记录并优雅处理
try:
    result = await agent.process(request)
except RateLimitError:
    return AgentResponse(status=Status.FAILED, error="Rate limit")
except TimeoutError:
    return AgentResponse(status=Status.FAILED, error="Timeout")
except Exception as e:
    logger.error("Unexpected error", error=str(e))
    return AgentResponse(status=Status.FAILED, error="Internal error")
```

### 陷阱 2: 缓存未失效

```python
# ❌ 错误：缓存永不过期
self.cache[key] = result  # 永远有效

# ✅ 正确：设置 TTL
self.cache[key] = {"result": result, "expires_at": time.time() + ttl}

# ✅ 正确：使用 LRU 缓存
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_result(self, key: str) -> Any:
    return self._compute(key)
```

---

## 📚 延伸阅读

- [OWASP LLM Top 10](https://owasp.org/www-project-llm-top-10/)
- [Agent 安全指南](https://www.anthropic.com/research)
- [LangChain 安全文档](https://python.langchain.com/docs/security)

---

## ✅ 自检清单

- [ ] 理解 任务编排与异步处理的核心概念
- [ ] 实现基础处理逻辑
- [ ] 配置错误处理和重试机制
- [ ] 添加监控和日志
- [ ] 遵循生产环境最佳实践

---

## 🔗 下一步

- [A08: Agent 安全护栏](../A08-agent-guardrails/) — 输入输出过滤
- [A09: Agent 隐私保护](../A09-agent-privacy/) — 数据保护

---

**课程制作**: Python 3.13 全栈课程组
**最后更新**: 2026-07-23
**版本**: v5.0
