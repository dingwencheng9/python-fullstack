# A13: Agent 成本管理

> **课程编号**: A13
> **所属阶段**: Stage A - AI Agent 企业级 (Specialization)
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: A05
> **版本**: v5.0
> **最后更新**: 2026-07-23

---

## 📌 学习目标

完成本课程后，你将能够：

1. **Token 计量与成本优化**
2. 实现流量控制和限流策略
3. 优化资源利用和成本

---

## Part 1: 核心概念

### 1.1 问题背景

Token 计量与成本优化是保障 Agent 服务稳定性和成本可控的关键能力。

### 1.2 技术方案

```python
from dataclasses import dataclass, field
from typing import Optional, Literal
from datetime import datetime, timedelta
from enum import Enum
import time


class LimitType(Enum):
    """限流类型"""
    RATE_LIMIT = "rate_limit"  # 速率限制
    QUOTA = "quota"  # 配额限制
    CONCURRENT = "concurrent"  # 并发限制


@dataclass
class LimitConfig:
    """限流配置"""
    limit_type: LimitType
    rate: float = 100  # 每秒请求数
    quota: int = 1000  # 每日配额
    window: int = 60  # 时间窗口（秒）
    burst: int = 10  # 突发容量


@dataclass
class UsageRecord:
    """使用记录"""
    user_id: str
    timestamp: datetime
    tokens: int
    requests: int
    cost: float = 0.0


class RateLimiter:
    """速率限制器 - 令牌桶算法"""

    def __init__(self, config: LimitConfig):
        self.config = config
        self.tokens = config.burst
        self.last_update = time.time()

    async def acquire(self, user_id: str) -> bool:
        """获取令牌"""
        now = time.time()
        elapsed = now - self.last_update

        # 补充令牌
        self.tokens = min(
            self.config.burst,
            self.tokens + elapsed * self.config.rate,
        )
        self.last_update = now

        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


class QuotaManager:
    """配额管理器"""

    def __init__(self, config: LimitConfig):
        self.config = config
        self.usage: dict[str, list[UsageRecord]] = {}

    def check_quota(self, user_id: str) -> tuple[bool, int]:
        """检查配额

        Returns:
            (是否有配额, 剩余配额)
        """
        today = datetime.now().date()

        if user_id not in self.usage:
            return True, self.config.quota

        # 统计今日使用量
        today_usage = sum(
            r.requests
            for r in self.usage[user_id]
            if r.timestamp.date() == today
        )

        remaining = max(0, self.config.quota - today_usage)
        return remaining > 0, remaining

    def record_usage(self, user_id: str, requests: int, tokens: int, cost: float):
        """记录使用"""
        if user_id not in self.usage:
            self.usage[user_id] = []

        self.usage[user_id].append(UsageRecord(
            user_id=user_id,
            timestamp=datetime.now(),
            requests=requests,
            tokens=tokens,
            cost=cost,
        ))

        # 清理旧记录（保留30天）
        cutoff = datetime.now() - timedelta(days=30)
        self.usage[user_id] = [
            r for r in self.usage[user_id]
            if r.timestamp > cutoff
        ]


class ConcurrentLimiter:
    """并发限制器"""

    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self.current = 0
        self.waiting: asyncio.Queue = asyncio.Queue()

    async def acquire(self):
        """获取并发许可"""
        if self.current < self.max_concurrent:
            self.current += 1
            return True

        # 等待释放
        await self.waiting.get()
        self.current += 1
        return True

    def release(self):
        """释放并发许可"""
        self.current -= 1
        if not self.waiting.empty():
            self.waiting.put_nowait(True)
```

---

## Part 2: 实现方案

### 2.1 综合限流器

```python
import asyncio


class UnifiedRateLimiter:
    """统一限流器"""

    def __init__(self, config: LimitConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config)
        self.quota_manager = QuotaManager(config)
        self.concurrent_limiter = ConcurrentLimiter(
            max_concurrent=config.burst
        )

    async def check(self, user_id: str) -> tuple[bool, str, dict]:
        """检查限流

        Returns:
            (是否允许, 原因, 详情)
        """
        # 1. 检查并发限制
        if self.current >= self.max_concurrent:
            return False, "concurrent_limit", {"current": self.current}

        # 2. 检查速率限制
        if not await self.rate_limiter.acquire(user_id):
            return False, "rate_limit", {"rate": self.config.rate}

        # 3. 检查配额
        has_quota, remaining = self.quota_manager.check_quota(user_id)
        if not has_quota:
            return False, "quota_exceeded", {"remaining": remaining}

        return True, "allowed", {"remaining": remaining}

    async def acquire(self, user_id: str) -> bool:
        """获取许可"""
        allowed, reason, _ = await self.check(user_id)
        if allowed:
            await self.concurrent_limiter.acquire()
        return allowed

    def release(self):
        """释放许可"""
        self.concurrent_limiter.release()

    def record(self, user_id: str, requests: int, tokens: int, cost: float):
        """记录使用"""
        self.quota_manager.record_usage(user_id, requests, tokens, cost)
```

### 2.2 滑动窗口限流

```python
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SlidingWindowRateLimiter:
    """滑动窗口限流器"""

    max_requests: int
    window_seconds: int
    requests: dict[str, deque] = field(default_factory=dict)

    async def is_allowed(self, user_id: str) -> bool:
        """检查是否允许请求"""
        now = datetime.now()
        cutoff = now.timestamp() - self.window_seconds

        if user_id not in self.requests:
            self.requests[user_id] = deque()

        # 清理过期请求
        timestamps = self.requests[user_id]
        while timestamps and timestamps[0] < cutoff:
            timestamps.popleft()

        # 检查限制
        if len(timestamps) >= self.max_requests:
            return False

        # 记录新请求
        timestamps.append(now.timestamp())
        return True
```

---

## Part 3: 生产实践

### 3.1 指标采集

```python
from prometheus_client import Counter, Histogram, Gauge


rate_limit_hits = Counter(
    "rate_limit_hits_total",
    "Total rate limit hits",
    ["reason", "user_id"],
)

quota_usage = Gauge(
    "quota_usage",
    "Current quota usage",
    ["user_id"],
)

concurrent_requests = Gauge(
    "concurrent_requests",
    "Current concurrent requests",
)
```

### 3.2 告警配置

```python
# 告警规则示例 (Prometheus AlertManager)
"""
groups:
- name: rate_limit_alerts
  rules:
  - alert: HighRateLimitHits
    expr: rate(rate_limit_hits_total[5m]) > 10
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High rate limit hits"

  - alert: QuotaNearLimit
    expr: quota_usage / quota_limit > 0.9
    for: 10m
    labels:
      severity: critical
    annotations:
      summary: "User quota near limit"
"""
```

---

## 💡 最佳实践

### 实践 1: 分层限流

```python
# 1. 边缘限流 (Redis)
self.edge_limiter = RedisRateLimiter(
    key_prefix="rl:",
    max_requests=1000,
    window=60,
)

# 2. 应用限流
self.app_limiter = UnifiedRateLimiter(config)

# 3. LLM 限流
self.llm_limiter = TokenRateLimiter(
    max_tokens_per_minute=100000,
)
```

### 实践 2: 优雅降级

```python
async def handle_rate_limit(self, user_id: str) -> dict:
    """处理限流 - 返回友好的错误"""
    has_quota, remaining = self.quota_manager.check_quota(user_id)

    return {
        "error": "rate_limit_exceeded",
        "message": "请求过于频繁，请稍后再试",
        "retry_after": 60,  # 秒
        "quota_remaining": remaining,
        "reset_at": datetime.now() + timedelta(seconds=60),
    }
```

---

## ✅ 自检清单

- [ ] 理解 Token 计量与成本优化的核心概念
- [ ] 实现速率限制和配额管理
- [ ] 配置监控和告警
- [ ] 实现优雅降级

---

## 🔗 下一步

- [A12: Agent SLO 监控](../A12-agent-slo/) — 服务质量目标
- [A13: Agent 成本管理](../A13-agent-cost-management/) — 成本优化

---

**课程制作**: Python 3.13 全栈课程组
**最后更新**: 2026-07-23
**版本**: v5.0
