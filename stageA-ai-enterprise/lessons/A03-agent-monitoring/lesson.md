# A03: Agent 监控与可观测性

> **课程编号**: A03
> **所属阶段**: Stage A - AI Agent 企业级 (Specialization)
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐ (中高级)
> **前置课程**: A01, A02
> **版本**: v5.0
> **最后更新**: 2026-07-22

---

## 📌 学习目标

完成本课程后，你将能够：

1. **可观测性架构**：理解日志、指标、追踪三大支柱
2. **指标设计**：设计 Agent 关键性能指标 (KPIs)
3. **告警系统**：构建智能告警和阈值管理
4. **仪表板**：创建运维仪表板

---

## 📚 课程内容

### 第一部分：可观测性架构

#### 1.1 三大支柱

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any
import time

class ObservableAgent:
    """可观测性 Agent"""

    def __init__(self):
        self.metrics: dict[str, Any] = {}
        self.traces: list[dict] = []
        self.logs: list[dict] = []

    # === 日志 (Logs) ===
    def log(self, level: str, message: str, **kwargs) -> None:
        """记录日志"""
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        })

    # === 指标 (Metrics) ===
    def increment(self, metric: str, value: int = 1) -> None:
        """递增指标"""
        if metric not in self.metrics:
            self.metrics[metric] = 0
        self.metrics[metric] += value

    def gauge(self, metric: str, value: float) -> None:
        """设置仪表指标"""
        self.metrics[metric] = value

    # === 追踪 (Traces) ===
    def trace(self, operation: str, func, *args, **kwargs) -> Any:
        """追踪操作"""
        start = time.time()
        trace_id = f"{datetime.now().timestamp()}"

        try:
            result = func(*args, **kwargs)
            self.traces.append({
                "trace_id": trace_id,
                "operation": operation,
                "duration": time.time() - start,
                "status": "success"
            })
            return result
        except Exception as e:
            self.traces.append({
                "trace_id": trace_id,
                "operation": operation,
                "duration": time.time() - start,
                "status": "error",
                "error": str(e)
            })
            raise
```

#### 1.2 OpenTelemetry 集成

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

class OTelAgent:
    """OpenTelemetry 集成"""

    def __init__(self, service_name: str):
        # 创建资源
        resource = Resource.create({
            "service.name": service_name,
            "service.version": "1.0.0"
        })

        # 创建追踪器提供者
        provider = TracerProvider(resource=resource)

        # 添加导出器（实际应连接 OTLP）
        # processor = BatchSpanProcessor(OTLPExporter(endpoint="http://localhost:4317"))
        # provider.add_span_processor(processor)

        trace.set_tracer_provider(provider)
        self.tracer = trace.get_tracer(__name__)

    @property
    def span(self):
        """获取追踪器"""
        return self.tracer
```

---

### 第二部分：关键指标设计

#### 2.1 Agent KPIs

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import statistics

@dataclass
class AgentMetrics:
    """Agent 指标"""
    # 请求指标
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0

    # 延迟指标
    latencies: list[float] = field(default_factory=list)

    # Token 指标
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def success_rate(self) -> float:
        """成功率"""
        return self.successful_requests / self.total_requests if self.total_requests else 0

    @property
    def p50_latency(self) -> Optional[float]:
        """P50 延迟"""
        return statistics.median(self.latencies) if self.latencies else None

    @property
    def p95_latency(self) -> Optional[float]:
        """P95 延迟"""
        if not self.latencies:
            return None
        sorted_latencies = sorted(self.latencies)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[idx]

    @property
    def total_tokens(self) -> int:
        """总 Token 数"""
        return self.prompt_tokens + self.completion_tokens
```

#### 2.2 指标收集器

```python
from collections import defaultdict
import time

class MetricsCollector:
    """指标收集器"""

    def __init__(self):
        self.counters: dict[str, int] = defaultdict(int)
        self.gauges: dict[str, float] = {}
        self.histograms: dict[str, list[float]] = defaultdict(list)

    def inc(self, name: str, value: int = 1) -> None:
        """递增计数器"""
        self.counters[name] += value

    def set_gauge(self, name: str, value: float) -> None:
        """设置仪表值"""
        self.gauges[name] = value

    def observe(self, name: str, value: float) -> None:
        """观察直方图值"""
        self.histograms[name].append(value)

    def get_snapshot(self) -> dict:
        """获取指标快照"""
        return {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {
                name: {
                    "count": len(values),
                    "sum": sum(values),
                    "min": min(values) if values else 0,
                    "max": max(values) if values else 0,
                    "avg": statistics.mean(values) if values else 0
                }
                for name, values in self.histograms.items()
            }
        }

# 使用
collector = MetricsCollector()
collector.inc("requests_total")
collector.observe("request_duration", 0.5)
collector.set_gauge("queue_size", 10)

snapshot = collector.get_snapshot()
print(f"Requests: {snapshot['counters']['requests_total']}")
```

---

### 第三部分：告警系统

#### 3.1 告警规则

```python
from dataclasses import dataclass
from enum import Enum

class AlertSeverity(Enum):
    CRITICAL = "critical"  # 立即处理
    WARNING = "warning"    # 需要关注
    INFO = "info"          # 信息性

@dataclass
class AlertRule:
    """告警规则"""
    name: str
    condition: str  # 条件表达式
    severity: AlertSeverity
    window: int  # 时间窗口（秒）
    threshold: float
    message: str

ALERT_RULES = [
    AlertRule(
        name="high_error_rate",
        condition="error_rate",
        severity=AlertSeverity.CRITICAL,
        window=300,
        threshold=0.05,  # 5% 错误率
        message="错误率超过 5%"
    ),
    AlertRule(
        name="high_latency",
        condition="p95_latency",
        severity=AlertSeverity.WARNING,
        window=300,
        threshold=5.0,  # 5 秒
        message="P95 延迟超过 5 秒"
    ),
]
```

#### 3.2 告警管理器

```python
class AlertManager:
    """告警管理器"""

    def __init__(self):
        self.rules: list[AlertRule] = []
        self.active_alerts: dict[str, dict] = {}
        self.handlers: list[callable] = []

    def add_rule(self, rule: AlertRule) -> None:
        """添加告警规则"""
        self.rules.append(rule)

    def add_handler(self, handler: callable) -> None:
        """添加告警处理器"""
        self.handlers.append(handler)

    def evaluate(self, metrics: dict) -> list[dict]:
        """评估告警规则"""
        fired_alerts = []

        for rule in self.rules:
            metric_value = metrics.get(rule.condition, 0)

            if metric_value > rule.threshold:
                alert = {
                    "rule": rule.name,
                    "severity": rule.severity.value,
                    "message": rule.message,
                    "value": metric_value,
                    "threshold": rule.threshold
                }
                fired_alerts.append(alert)

                # 触发处理器
                for handler in self.handlers:
                    handler(alert)

        return fired_alerts
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解可观测性三大支柱
- [ ] 设计 Agent 关键指标
- [ ] 实现指标收集系统
- [ ] 构建告警规则和处理器

---

## 🔗 相关资源

- [OpenTelemetry Documentation](https://opentelemetry.io/)
- [Prometheus Metrics](https://prometheus.io/docs/concepts/metric_types/)
- [Grafana Dashboard Guide](https://grafana.com/docs/grafana/latest/dashboards/)

---

## 🔗 下一步

- A04: Agent 成本管理
- A05: Agent 项目实战
- Stage A: AI Agent 企业级应用

---

**最后更新**: 2026-07-18
