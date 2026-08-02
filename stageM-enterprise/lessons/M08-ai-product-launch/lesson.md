# M08: AI 产品发布与运营

> **课程编号**: M08
> **所属阶段**: Stage M - 企业级 AI 应用
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: M01-M07
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **产品发布策略**：制定 AI 产品发布计划
2. **用户反馈收集**：建立用户反馈机制
3. **产品迭代**：基于数据驱动产品迭代
4. **运营监控**：监控 AI 产品核心指标

---

## 📚 课程内容

### 第一部分：产品发布策略

#### 1.1 发布模式

```python
# AI 产品发布模式
RELEASE_MODES = {
    "灰度发布": {
        "description": "逐步将流量切换到新版本",
        "steps": ["小流量验证", "10% 流量", "50% 流量", "全量发布"],
        "风险": "低",
    },
    "金丝雀发布": {
        "description": "新版本只处理少量请求",
        "steps": ["1% 流量", "5% 流量", "逐步扩大"],
        "风险": "低",
    },
    "特性开关": {
        "description": "通过配置控制功能开启",
        "steps": ["关闭新功能", "内部用户", "白名单用户", "全量用户"],
        "风险": "中",
    },
}
```

#### 1.2 发布清单

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class ReleaseChecklist:
    """发布检查清单"""
    feature_name: str
    release_date: datetime
    items: dict = field(default_factory=dict)

    def add_item(self, name: str, status: str = "pending") -> None:
        """添加检查项"""
        self.items[name] = {
            "status": status,
            "checked_at": None,
            "checked_by": None
        }

    def check_item(self, name: str, checked_by: str) -> bool:
        """检查项完成"""
        if name in self.items:
            self.items[name]["status"] = "completed"
            self.items[name]["checked_at"] = datetime.now()
            self.items[name]["checked_by"] = checked_by
            return True
        return False

    @property
    def completion_rate(self) -> float:
        """完成率"""
        if not self.items:
            return 0.0
        completed = sum(1 for v in self.items.values()
                       if v["status"] == "completed")
        return completed / len(self.items)

# 常用检查项
DEFAULT_CHECKLIST = [
    "功能测试通过",
    "性能测试通过",
    "安全扫描通过",
    "文档更新完成",
    "监控告警配置",
    "回滚方案准备",
    "值班人员确认",
    "用户公告准备",
]
```

---

### 第二部分：用户反馈收集

#### 2.1 反馈系统

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

class FeedbackType(Enum):
    """反馈类型"""
    BUG_REPORT = "bug"
    FEATURE_REQUEST = "feature"
    USABILITY = "usability"
    PERFORMANCE = "performance"
    OTHER = "other"

class FeedbackPriority(Enum):
    """优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Feedback:
    """用户反馈"""
    id: str
    user_id: str
    feedback_type: FeedbackType
    content: str
    created_at: datetime = field(default_factory=datetime.now)
    priority: FeedbackPriority = FeedbackPriority.MEDIUM
    status: str = "new"
    metadata: dict = field(default_factory=dict)
    response: Optional[str] = None

class FeedbackCollector:
    """反馈收集器"""

    def __init__(self):
        self.feedbacks: list[Feedback] = []

    def add_feedback(
        self,
        user_id: str,
        feedback_type: FeedbackType,
        content: str,
        metadata: dict = None
    ) -> Feedback:
        """添加反馈"""
        feedback = Feedback(
            id=f"fb_{len(self.feedbacks) + 1}",
            user_id=user_id,
            feedback_type=feedback_type,
            content=content,
            metadata=metadata or {}
        )
        self.feedbacks.append(feedback)
        return feedback

    def get_by_type(self, feedback_type: FeedbackType) -> list[Feedback]:
        """按类型获取反馈"""
        return [f for f in self.feedbacks if f.feedback_type == feedback_type]

    def get_by_priority(self, priority: FeedbackPriority) -> list[Feedback]:
        """按优先级获取反馈"""
        return [f for f in self.feedbacks if f.priority == priority]

    def get_unresponded(self) -> list[Feedback]:
        """获取未回复反馈"""
        return [f for f in self.feedbacks if f.response is None]
```

#### 2.2 用户评分系统

```python
import statistics
from dataclasses import dataclass

@dataclass
class Rating:
    """用户评分"""
    user_id: str
    score: int  # 1-5
    comment: str
    timestamp: datetime = field(default_factory=datetime.now)
    aspects: dict = None  # 多维度评分

class RatingSystem:
    """评分系统"""

    def __init__(self):
        self.ratings: list[Rating] = []

    def add_rating(self, rating: Rating) -> None:
        """添加评分"""
        if not 1 <= rating.score <= 5:
            raise ValueError("Score must be between 1 and 5")
        self.ratings.append(rating)

    @property
    def average_score(self) -> float:
        """平均分"""
        if not self.ratings:
            return 0.0
        return statistics.mean(r.score for r in self.ratings)

    def get_score_distribution(self) -> dict[int, int]:
        """分数分布"""
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating in self.ratings:
            distribution[rating.score] += 1
        return distribution

    def get_nps_score(self) -> float:
        """NPS 净推荐值"""
        if not self.ratings:
            return 0.0

        promoters = sum(1 for r in self.ratings if r.score >= 9)
        detractors = sum(1 for r in self.ratings if r.score <= 6)

        return (promoters - detractors) / len(self.ratings) * 100
```

---

### 第三部分：数据驱动迭代

#### 3.1 指标分析

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class ProductMetrics:
    """产品指标"""
    date: datetime
    dau: int = 0  # 日活用户
    mau: int = 0  # 月活用户
    new_users: int = 0
    retention_rate: float = 0.0
    avg_session_duration: float = 0.0  # 秒
    conversion_rate: float = 0.0
    nps_score: float = 0.0

class MetricsAnalyzer:
    """指标分析器"""

    def __init__(self):
        self.metrics_history: list[ProductMetrics] = []

    def add_metrics(self, metrics: ProductMetrics) -> None:
        """添加指标"""
        self.metrics_history.append(metrics)

    def get_trend(self, days: int = 7) -> dict:
        """获取趋势"""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [m for m in self.metrics_history if m.date >= cutoff]

        if not recent:
            return {}

        return {
            "dau_trend": [m.dau for m in recent],
            "retention_trend": [m.retention_rate for m in recent],
            "avg_dau": sum(m.dau for m in recent) / len(recent),
            "avg_retention": sum(m.retention_rate for m in recent) / len(recent),
        }

    def detect_anomaly(self, metric_name: str, threshold: float = 0.2) -> list:
        """异常检测"""
        anomalies = []

        if metric_name == "dau":
            values = [m.dau for m in self.metrics_history]
        elif metric_name == "retention":
            values = [m.retention_rate for m in self.metrics_history]
        else:
            return anomalies

        if len(values) < 3:
            return anomalies

        avg = sum(values) / len(values)

        for i, val in enumerate(values):
            change = abs(val - avg) / avg if avg > 0 else 0
            if change > threshold:
                anomalies.append({
                    "index": i,
                    "value": val,
                    "expected": avg,
                    "change_pct": change * 100
                })

        return anomalies
```

#### 3.2 A/B 测试

```python
import random
from dataclasses import dataclass, field
from typing import Callable

@dataclass
class ABTestVariant:
    """A/B 测试变体"""
    name: str
    traffic_percentage: float
    is_control: bool = False

@dataclass
class ABTestResult:
    """测试结果"""
    test_id: str
    variant_name: str
    impressions: int = 0
    conversions: int = 0

    @property
    def conversion_rate(self) -> float:
        if self.impressions == 0:
            return 0.0
        return self.conversions / self.impressions

class ABTestEngine:
    """A/B 测试引擎"""

    def __init__(self):
        self.tests: dict[str, list[ABTestVariant]] = {}
        self.results: dict[str, dict[str, ABTestResult]] = {}

    def create_test(
        self,
        test_id: str,
        variants: list[ABTestVariant]
    ) -> None:
        """创建测试"""
        self.tests[test_id] = variants
        self.results[test_id] = {
            v.name: ABTestResult(test_id=test_id, variant_name=v.name)
            for v in variants
        }

    def get_variant(self, test_id: str, user_id: str) -> str:
        """获取用户变体"""
        if test_id not in self.tests:
            raise ValueError(f"Test not found: {test_id}")

        variants = self.tests[test_id]

        # 基于用户 ID 哈希确保一致性
        hash_val = hash(f"{test_id}:{user_id}")
        normalized = (hash_val % 1000) / 1000.0

        cumulative = 0.0
        for variant in variants:
            cumulative += variant.traffic_percentage / 100.0
            if normalized < cumulative:
                return variant.name

        return variants[-1].name

    def record_impression(self, test_id: str, variant_name: str) -> None:
        """记录曝光"""
        if test_id in self.results:
            self.results[test_id][variant_name].impressions += 1

    def record_conversion(self, test_id: str, variant_name: str) -> None:
        """记录转化"""
        if test_id in self.results:
            self.results[test_id][variant_name].conversions += 1

    def get_winner(self, test_id: str, confidence: float = 0.95) -> Optional[str]:
        """获取获胜变体"""
        if test_id not in self.results:
            return None

        results = self.results[test_id]

        # 简单比较（实际应使用统计显著性检验）
        best = None
        best_rate = 0.0

        for name, result in results.items():
            rate = result.conversion_rate
            if rate > best_rate and result.impressions > 100:
                best_rate = rate
                best = name

        return best
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 制定 AI 产品发布计划
- [ ] 建立用户反馈收集机制
- [ ] 分析产品核心指标
- [ ] 设计并执行 A/B 测试

---

## 🔗 相关资源

- [Product Hunt](https://producthunt.com/)
- [Amplitude Analytics](https://amplitude.com/)
- [Mixpanel](https://mixpanel.com/)

---

## 🔗 下一步


[Stage R: 前沿探索实验室](../../../stageR-frontier/)

---

**最后更新**: 2026-07-18
