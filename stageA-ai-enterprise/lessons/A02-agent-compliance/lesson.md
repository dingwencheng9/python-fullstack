# A02: Agent 合规与审计

> **课程编号**: A02
> **所属阶段**: Stage A - AI Agent 企业级 (Specialization)
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐ (中高级)
> **前置课程**: A01
> **版本**: v5.0
> **最后更新**: 2026-07-22

---

## 📌 学习目标

完成本课程后，你将能够：

1. **合规框架**：理解 AI Agent 的主要合规要求
2. **审计系统**：设计完整的审计追踪系统
3. **数据治理**：实现数据分类和保留策略
4. **报告生成**：生成合规报告和审计证据

---

## 📚 课程内容

### 第一部分：合规框架

#### 1.1 AI 合规概述

```python
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class ComplianceFramework(Enum):
    """合规框架"""
    GDPR = "gdpr"           # 通用数据保护条例
    CCPA = "ccpa"           # 加州消费者隐私法
    SOC2 = "soc2"           # 服务组织控制
    HIPAA = "hipaa"         # 健康保险便携性
    PCI_DSS = "pci_dss"     # 支付卡行业数据安全

@dataclass
class ComplianceRequirement:
    """合规要求"""
    framework: ComplianceFramework
    control_id: str
    description: str
    mandatory: bool

# 示例要求
REQUIREMENTS = [
    ComplianceRequirement(
        ComplianceFramework.GDPR,
        "A.1",
        "数据处理的法律依据",
        True
    ),
    ComplianceRequirement(
        ComplianceFramework.GDPR,
        "A.2",
        "数据主体权利保障",
        True
    ),
]
```

#### 1.2 数据分类

```python
class DataClassification(Enum):
    """数据分类级别"""
    PUBLIC = "public"           # 公开
    INTERNAL = "internal"       # 内部
    CONFIDENTIAL = "confidential"  # 机密
    RESTRICTED = "restricted"   # 高度机密

class DataClassifier:
    """数据分类器"""

    CLASSIFICATION_RULES = {
        "pii": DataClassification.RESTRICTED,
        "financial": DataClassification.CONFIDENTIAL,
        "internal_communication": DataClassification.INTERNAL,
    }

    @classmethod
    def classify(cls, data: dict) -> DataClassification:
        """分类数据"""
        # 简单规则匹配
        content = str(data).lower()

        if "ssn" in content or "passport" in content:
            return DataClassification.RESTRICTED

        if "credit_card" in content or "bank" in content:
            return DataClassification.CONFICTED

        return DataClassification.PUBLIC
```

---

### 第二部分：审计追踪

#### 2.1 审计日志架构

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import json

@dataclass
class AuditRecord:
    """审计记录"""
    event_id: str
    timestamp: datetime
    event_type: str
    actor: str  # 谁执行了操作
    resource: str  # 操作了什么资源
    action: str  # 执行了什么操作
    result: str  # 结果如何
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "actor": self.actor,
            "resource": self.resource,
            "action": self.action,
            "result": self.result,
            "metadata": self.metadata
        }

class AuditLogger:
    """审计日志器"""

    def __init__(self, storage: str):
        self.storage = Path(storage)
        self.storage.mkdir(parents=True, exist_ok=True)
        self.buffer: list[AuditRecord] = []

    def log(self, record: AuditRecord) -> None:
        """记录审计事件"""
        self.buffer.append(record)

        # 批量写入
        if len(self.buffer) >= 100:
            self.flush()

    def flush(self) -> None:
        """刷新缓冲区到存储"""
        if not self.buffer:
            return

        filename = self.storage / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"

        with open(filename, "a") as f:
            for record in self.buffer:
                f.write(json.dumps(record.to_dict()) + "\n")

        self.buffer.clear()
```

#### 2.2 审计查询

```python
class AuditQuery:
    """审计查询"""

    def __init__(self, storage: str):
        self.storage = Path(storage)

    def query(
        self,
        start_time: datetime,
        end_time: datetime,
        actor: str = None,
        event_type: str = None
    ) -> list[AuditRecord]:
        """查询审计记录"""
        results = []

        # 遍历所有审计文件
        for file in self.storage.glob("audit_*.jsonl"):
            with open(file) as f:
                for line in f:
                    record = json.loads(line)

                    # 时间过滤
                    timestamp = datetime.fromisoformat(record["timestamp"])
                    if not (start_time <= timestamp <= end_time):
                        continue

                    # 角色过滤
                    if actor and record["actor"] != actor:
                        continue

                    # 事件类型过滤
                    if event_type and record["event_type"] != event_type:
                        continue

                    results.append(record)

        return results
```

---

### 第三部分：合规报告

#### 3.1 报告生成

```python
from datetime import timedelta

class ComplianceReporter:
    """合规报告生成器"""

    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger

    def generate_report(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """生成合规报告"""
        records = self.audit_logger.query(start_date, end_date)

        # 统计
        total_events = len(records)
        success_events = sum(1 for r in records if r["result"] == "success")
        failed_events = sum(1 for r in records if r["result"] == "failure")

        # 用户活动统计
        user_activity = {}
        for r in records:
            actor = r["actor"]
            user_activity[actor] = user_activity.get(actor, 0) + 1

        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "summary": {
                "total_events": total_events,
                "success_rate": success_events / total_events if total_events else 0,
                "failed_events": failed_events
            },
            "user_activity": user_activity
        }
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解主要合规框架的要求
- [ ] 实现数据分类系统
- [ ] 设计完整的审计日志架构
- [ ] 生成合规报告

---

## 🔗 相关资源

- [GDPR Compliance Guide](https://gdpr.eu/)
- [SOC 2 Compliance Requirements](https://www.aicpa.org/soc2)
- [AI Regulatory Framework](https://www.euaistrategy.eu/)

---

## 🔗 下一步

- A03: Agent 监控与可观测性
- A04: Agent 成本管理
- A05: Agent 项目实战

---

**最后更新**: 2026-07-18
