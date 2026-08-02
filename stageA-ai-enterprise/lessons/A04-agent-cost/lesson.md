# A04: Agent 成本管理

> **课程编号**: A04
> **所属阶段**: Stage A - AI Agent 企业级 (Specialization)
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐ (中高级)
> **前置课程**: A03
> **版本**: v5.0
> **最后更新**: 2026-07-22

---

## 📌 学习目标

完成本课程后，你将能够：

1. **成本模型**：理解 LLM 成本计算模型
2. **使用追踪**：追踪 Token 使用量和成本
3. **优化策略**：实施成本优化策略
4. **预算管理**：设置预算限制和告警

---

## 📚 课程内容

### 第一部分：成本模型

#### 1.1 LLM 定价模型

```python
from dataclasses import dataclass
from enum import Enum

class ModelType(Enum):
    GPT4O = "gpt-4o"
    GPT4O_MINI = "gpt-4o-mini"
    CLAUDE_3_5 = "claude-3-5-sonnet"
    GEMINI_PRO = "gemini-1.5-pro"

@dataclass
class ModelPricing:
    """模型定价"""
    model: str
    input_cost_per_mtok: float  # 每百万输入 Token 成本
    output_cost_per_mtok: float  # 每百万输出 Token 成本

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """计算成本"""
        input_cost = (input_tokens / 1_000_000) * self.input_cost_per_mtok
        output_cost = (output_tokens / 1_000_000) * self.output_cost_per_mtok
        return input_cost + output_cost

# 示例定价 (2024 年参考)
PRICING = {
    ModelType.GPT4O: ModelPricing(
        model=ModelType.GPT4O.value,
        input_cost_per_mtok=5.00,   # $5/MTok
        output_cost_per_mtok=15.00   # $15/MTok
    ),
    ModelType.GPT4O_MINI: ModelPricing(
        model=ModelType.GPT4O_MINI.value,
        input_cost_per_mtok=0.15,   # $0.15/MTok
        output_cost_per_mtok=0.60    # $0.60/MTok
    ),
    ModelType.CLAUDE_3_5: ModelPricing(
        model=ModelType.CLAUDE_3_5.value,
        input_cost_per_mtok=3.00,
        output_cost_per_mtok=15.00
    ),
}

def calculate_monthly_cost(
    daily_requests: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    model: ModelType
) -> float:
    """计算月成本"""
    pricing = PRICING[model]
    daily_cost = pricing.calculate_cost(avg_input_tokens, avg_output_tokens) * daily_requests
    return daily_cost * 30  # 月成本
```

#### 1.2 成本分析

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CostRecord:
    """成本记录"""
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    request_id: str

class CostAnalyzer:
    """成本分析器"""

    def __init__(self):
        self.records: list[CostRecord] = []

    def record(self, record: CostRecord) -> None:
        """记录成本"""
        self.records.append(record)

    def get_total_cost(self, start: datetime = None, end: datetime = None) -> float:
        """获取总成本"""
        filtered = self._filter_by_date(start, end)
        return sum(r.cost for r in filtered)

    def get_cost_by_model(self) -> dict[str, float]:
        """按模型分组成本"""
        costs = {}
        for record in self.records:
            costs[record.model] = costs.get(record.model, 0) + record.cost
        return costs

    def get_top_consumers(self, limit: int = 10) -> list[CostRecord]:
        """获取最高消费者"""
        return sorted(self.records, key=lambda r: r.cost, reverse=True)[:limit]

    def _filter_by_date(self, start: datetime, end: datetime) -> list[CostRecord]:
        """按日期过滤"""
        if not start and not end:
            return self.records

        filtered = self.records
        if start:
            filtered = [r for r in filtered if r.timestamp >= start]
        if end:
            filtered = [r for r in filtered if r.timestamp <= end]
        return filtered
```

---

### 第二部分：使用追踪

#### 2.1 Token 追踪器

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import hashlib

@dataclass
class TokenUsage:
    """Token 使用情况"""
    request_id: str
    timestamp: datetime
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: dict = field(default_factory=dict)

class TokenTracker:
    """Token 追踪器"""

    def __init__(self):
        self.usage_records: list[TokenUsage] = []

    def track(self, usage: TokenUsage) -> None:
        """追踪使用"""
        self.usage_records.append(usage)

    def get_user_usage(self, user_id: str) -> dict:
        """获取用户使用情况"""
        user_records = [r for r in self.usage_records if r.user_id == user_id]

        total_tokens = sum(r.total_tokens for r in user_records)
        total_cost = sum(r.cost for r in user_records)
        request_count = len(user_records)

        return {
            "user_id": user_id,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "request_count": request_count,
            "avg_tokens_per_request": total_tokens / request_count if request_count else 0
        }

    def get_daily_summary(self, date: datetime) -> dict:
        """获取每日摘要"""
        day_records = [
            r for r in self.usage_records
            if r.timestamp.date() == date.date()
        ]

        return {
            "date": date.date().isoformat(),
            "total_requests": len(day_records),
            "total_tokens": sum(r.total_tokens for r in day_records),
            "total_cost": sum(r.cost for r in day_records)
        }
```

#### 2.2 使用仪表板数据

```python
class CostDashboard:
    """成本仪表板数据生成器"""

    def __init__(self, tracker: TokenTracker):
        self.tracker = tracker

    def get_dashboard_data(self, days: int = 7) -> dict:
        """生成仪表板数据"""
        from datetime import timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        daily_summaries = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            summary = self.tracker.get_daily_summary(date)
            daily_summaries.append(summary)

        # 按模型分组
        model_usage = {}
        for record in self.tracker.usage_records:
            if record.timestamp >= start_date:
                if record.model not in model_usage:
                    model_usage[record.model] = {"tokens": 0, "cost": 0}
                model_usage[record.model]["tokens"] += record.total_tokens
                model_usage[record.model]["cost"] += record.cost

        return {
            "period": {"start": start_date.isoformat(), "end": end_date.isoformat()},
            "daily_summaries": daily_summaries,
            "model_usage": model_usage,
            "total_cost": sum(s["total_cost"] for s in daily_summaries)
        }
```

---

### 第三部分：优化策略

#### 3.1 成本优化技术

```python
class CostOptimizer:
    """成本优化器"""

    @staticmethod
    def suggest_model_downgrade(usage: TokenUsage) -> str:
        """建议降级模型"""
        # 简单启发式
        if usage.completion_tokens < 100:
            return "gpt-4o-mini"
        elif usage.completion_tokens < 500:
            return "gpt-4o-mini"
        else:
            return usage.model

    @staticmethod
    def estimate_savings(
        original_tokens: int,
        optimized_tokens: int,
        model: str
    ) -> float:
        """估算节省成本"""
        pricing = PRICING.get(ModelType(model), PRICING[ModelType.GPT4O_MINI])
        original_cost = pricing.calculate_cost(original_tokens, 0)
        optimized_cost = pricing.calculate_cost(optimized_tokens, 0)
        return original_cost - optimized_cost

    @staticmethod
    def suggest_caching(user_id: str, request_count: int) -> bool:
        """建议启用缓存"""
        # 重复请求超过 30% 时建议缓存
        return request_count > 100 and request_count % 3 == 0
```

#### 3.2 缓存策略

```python
import hashlib
import json
from typing import Optional
from datetime import datetime, timedelta

class ResponseCache:
    """响应缓存"""

    def __init__(self, ttl: int = 3600):
        self.cache: dict[str, tuple[str, datetime]] = {}
        self.ttl = ttl

    def _make_key(self, prompt: str, model: str) -> str:
        """生成缓存键"""
        content = json.dumps({"prompt": prompt, "model": model})
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, prompt: str, model: str) -> Optional[str]:
        """获取缓存"""
        key = self._make_key(prompt, model)

        if key in self.cache:
            response, timestamp = self.cache[key]

            # 检查过期
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return response

            del self.cache[key]

        return None

    def set(self, prompt: str, model: str, response: str) -> None:
        """设置缓存"""
        key = self._make_key(prompt, model)
        self.cache[key] = (response, datetime.now())

    def invalidate(self, prompt: str, model: str) -> None:
        """使缓存失效"""
        key = self._make_key(prompt, model)
        self.cache.pop(key, None)
```

---

### 第四部分：预算管理

#### 4.1 预算系统

```python
@dataclass
class Budget:
    """预算"""
    name: str
    amount: float
    spent: float = 0.0
    period: str = "monthly"  # monthly, daily, one-time

    @property
    def remaining(self) -> float:
        """剩余预算"""
        return max(0, self.amount - self.spent)

    @property
    def utilization(self) -> float:
        """预算使用率"""
        return self.spent / self.amount if self.amount else 0

    def is_exceeded(self) -> bool:
        """是否超预算"""
        return self.spent > self.amount

class BudgetManager:
    """预算管理器"""

    def __init__(self):
        self.budgets: dict[str, Budget] = {}
        self.alerts: list[callable] = []

    def add_budget(self, budget: Budget) -> None:
        """添加预算"""
        self.budgets[budget.name] = budget

    def add_alert_handler(self, handler: callable) -> None:
        """添加告警处理器"""
        self.alerts.append(handler)

    def record_spending(self, budget_name: str, amount: float) -> None:
        """记录支出"""
        if budget_name not in self.budgets:
            raise ValueError(f"Budget not found: {budget_name}")

        budget = self.budgets[budget_name]
        budget.spent += amount

        # 检查告警阈值
        utilization = budget.utilization
        for threshold, handler in [(0.8, "warning"), (1.0, "critical")]:
            if utilization >= threshold:
                for alert in self.alerts:
                    alert(budget_name, utilization, threshold)

    def check_budget(self, budget_name: str, proposed_cost: float) -> bool:
        """检查预算是否允许"""
        if budget_name not in self.budgets:
            return True

        budget = self.budgets[budget_name]
        return budget.remaining >= proposed_cost
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解 LLM 成本计算模型
- [ ] 实现 Token 使用追踪
- [ ] 应用成本优化策略
- [ ] 设计预算管理系统

---

## 🔗 相关资源

- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)

---

## 🔗 下一步

- A05: Agent 项目实战
- Stage A: AI Agent 企业级应用

---

**最后更新**: 2026-07-18
