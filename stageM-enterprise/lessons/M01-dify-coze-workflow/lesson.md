# M01: Dify/Coze 工作流编排

> **课程编号**: M01
> **所属阶段**: Stage M - 企业级 AI 应用
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐ (中高级)
> **前置课程**: L60 (MCP 协议)、L61 (多智能体)
> **状态**: 🟡 完善中
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **理解工作流编排**：掌握 Dify/Coze 的工作流设计理念
2. **构建复杂流程**：使用可视化界面构建 AI 工作流
3. **集成外部系统**：将工作流与企业现有系统集成
4. **部署与运维**：将工作流部署到生产环境

---

## 📚 课程内容

### 第一部分：工作流编排基础

#### 1.1 为什么需要工作流编排

在企业场景中，AI 能力需要与业务流程深度整合。传统的 API 调用方式难以应对复杂的业务逻辑，而工作流编排提供了：

- **可视化设计**：通过图形界面设计业务流程
- **节点复用**：一次设计，多次使用
- **状态管理**：内置变量传递和状态追踪
- **错误处理**：统一的异常处理机制

#### 1.2 Dify vs Coze 对比

| 特性 | Dify | Coze |
|------|------|------|
| **部署方式** | 开源自部署 | 云服务/企业版 |
| **定制能力** | 完全可控 | 受限 |
| **适合场景** | 企业内网、数据敏感 | 快速原型、出海 |
| **插件生态** | 社区驱动 | 官方生态 |

#### 1.3 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                    工作流 (Workflow)                     │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  开始节点 │ → │ LLM 节点  │ → │ 工具节点  │          │
│  └──────────┘    └──────────┘    └──────────┘          │
│                      ↓                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │ 条件分支 │ ← │ 代码节点  │ ← │ 知识库节点 │          │
│  └──────────┘    └──────────┘    └──────────┘          │
└─────────────────────────────────────────────────────────┘
```

---

### 第二部分：Dify 实战

#### 2.1 安装与部署

```bash
# Docker 快速部署
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker-compose up -d

# 访问 http://localhost:80
```

#### 2.2 创建第一个工作流

1. **创建应用**：选择「导入 YAML」或从头创建
2. **添加节点**：从节点面板拖拽组件
3. **配置参数**：设置每个节点的输入输出
4. **测试运行**：使用调试面板验证

#### 2.3 常用节点类型

| 节点类型 | 用途 | 示例 |
|----------|------|------|
| **LLM** | 调用大模型 | 文本生成、对话 |
| **知识库检索** | RAG 增强 | 文档问答 |
| **条件分支** | 流程控制 | if/else 逻辑 |
| **代码执行** | 自定义逻辑 | 数据转换 |
| **HTTP 请求** | 外部 API | 第三方集成 |
| **模板转换** | 格式化输出 | JSON/HTML |

#### 2.4 变量与上下文传递

```python
# Dify 中的变量引用格式
# {{variable_name}}
# {{#节点ID.variable_name}}

# 示例：多节点变量传递
{
    "user_query": "{{#start.user_input}}",           # 起始节点输入
    "retrieved_docs": "{{#knowledge_base.docs}}",    # 知识库检索结果
    "llm_response": "{{#llm_node.response}}",        # LLM 输出
    "final_output": "{{#template.output}}"           # 模板格式化
}
```

---

### 第三部分：Coze 工作流

#### 3.1 Coze 平台概述

Coze（扣子）是字节跳动的 AI 应用平台，提供：

- **Bot Studio**：创建聊天机器人
- **Workflow**：可视化流程编排
- **插件市场**：丰富的插件生态
- **发布渠道**：抖音、微信、企业微信等

#### 3.2 创建 Coze 工作流

```python
# Coze API 调用示例
import httpx

COZE_API_KEY = "your_api_key"
COZE_BOT_ID = "your_bot_id"

async def call_coze_workflow(user_input: str) -> dict:
    """调用 Coze 工作流"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.coze.com/v1/chat",
            headers={
                "Authorization": f"Bearer {COZE_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "bot_id": COZE_BOT_ID,
                "user": "user_001",
                "query": user_input,
                "stream": False
            }
        )
        return response.json()
```

#### 3.3 工作流设计模式

```python
# 模式 1：顺序执行
# 开始 → 预处理 → LLM → 后处理 → 结束

# 模式 2：并行分支
# 开始 → [分支A] ↔ [分支B] ↔ [分支C] → 合并 → 结束

# 模式 3：循环迭代
# 开始 → while 条件 → 处理 → 更新条件 → 结束

# 模式 4：重试机制
# 开始 → 执行 → [成功?] → 是 → 结束
#                ↓ 否
#            重试 (最多3次) → 失败处理
```

---

### 第四部分：企业集成实践

#### 4.1 与企业微信集成

```python
# 企业微信机器人通知
import httpx

WECOM_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"

async def notify_via_wecom(message: str) -> None:
    """通过企业微信发送通知"""
    async with httpx.AsyncClient() as client:
        await client.post(
            WECOM_WEBHOOK,
            json={
                "msgtype": "text",
                "text": {
                    "content": f"[AI 工作流通知] {message}"
                }
            }
        )
```

#### 4.2 与飞书集成

```python
# 飞书 Webhook 通知
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

async def notify_via_feishu(message: str) -> None:
    """通过飞书发送通知"""
    async with httpx.AsyncClient() as client:
        await client.post(
            FEISHU_WEBHOOK,
            json={
                "msg_type": "text",
                "content": {
                    "text": f"[AI 工作流] {message}"
                }
            }
        )
```

#### 4.3 工作流监控

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
import httpx

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class WorkflowRun:
    """工作流执行记录"""
    run_id: str
    workflow_id: str
    status: WorkflowStatus
    started_at: datetime = field(default_factory=datetime.now)
    finished_at: datetime | None = None
    input_data: dict[str, Any] = field(default_factory=dict)
    output_data: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None

    @property
    def duration_seconds(self) -> float | None:
        """执行时长（秒）"""
        if self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None

    def is_successful(self) -> bool:
        """是否成功"""
        return self.status == WorkflowStatus.SUCCESS
```

---

## 🚀 实战案例

### 案例：智能客服工作流

```python
# 智能客服工作流设计
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

class Intent(Enum):
    """用户意图识别"""
    PRODUCT_INQUIRY = "product_inquiry"
    ORDER_STATUS = "order_status"
    COMPLAINT = "complaint"
    REFUND = "refund"
    UNKNOWN = "unknown"

@dataclass
class CustomerQuery:
    """客户查询"""
    user_id: str
    query_text: str
    intent: Intent = Intent.UNKNOWN
    context: dict = None

@dataclass
class WorkflowResponse:
    """工作流响应"""
    response_text: str
    intent: Intent
    confidence: float
    suggested_actions: list[str]

class IntentClassifier:
    """意图分类器"""

    # 关键词映射
    INTENT_KEYWORDS = {
        Intent.PRODUCT_INQUIRY: ["产品", "价格", "规格", "功能"],
        Intent.ORDER_STATUS: ["订单", "物流", "快递", "发货"],
        Intent.COMPLAINT: ["投诉", "不满", "问题", "反馈"],
        Intent.REFUND: ["退款", "退货", "取消"],
    }

    def classify(self, query: str) -> Intent:
        """分类用户意图"""
        query_lower = query.lower()
        for intent, keywords in self.INTENT_KEYWORDS.items():
            if any(kw in query_lower for kw in keywords):
                return intent
        return Intent.UNKNOWN

class SmartCustomerServiceWorkflow:
    """智能客服工作流"""

    def __init__(self):
        self.classifier = IntentClassifier()

    def process(self, query: CustomerQuery) -> WorkflowResponse:
        """
        处理流程：
        1. 意图识别
        2. 知识库检索
        3. LLM 生成回复
        4. 敏感词过滤
        5. 返回结果
        """
        # Step 1: 意图识别
        query.intent = self.classifier.classify(query.query_text)

        # Step 2: 根据意图选择处理策略
        if query.intent == Intent.ORDER_STATUS:
            response_text = self._handle_order_status(query)
        elif query.intent == Intent.COMPLAINT:
            response_text = self._handle_complaint(query)
        elif query.intent == Intent.PRODUCT_INQUIRY:
            response_text = self._handle_product_inquiry(query)
        else:
            response_text = self._handle_unknown(query)

        return WorkflowResponse(
            response_text=response_text,
            intent=query.intent,
            confidence=0.85,
            suggested_actions=["转人工", "查看常见问题"]
        )

    def _handle_order_status(self, query: CustomerQuery) -> str:
        """处理订单查询"""
        return f"您好！正在为您查询订单信息..."

    def _handle_complaint(self, query: CustomerQuery) -> str:
        """处理投诉"""
        return f"非常抱歉给您带来不便，我们会立即处理..."

    def _handle_product_inquiry(self, query: CustomerQuery) -> str:
        """处理产品咨询"""
        return f"关于您咨询的产品，我来为您详细介绍..."

    def _handle_unknown(self, query: CustomerQuery) -> str:
        """处理未知意图"""
        return f"抱歉，我没能理解您的问题，请问可以详细描述一下吗？"
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解 Dify 和 Coze 的核心差异和适用场景
- [ ] 在 Dify 中创建并部署工作流
- [ ] 在 Coze 中配置 Bot 和工作流
- [ ] 实现工作流与企业系统的集成
- [ ] 设置工作流监控和告警

---

## 🔗 相关资源

- [Dify 官方文档](https://docs.dify.ai/)
- [Coze 平台文档](https://www.coze.cn/docs)
- [LangChain 工作流](../../../stage6-ai-agent/lessons/L58-langgraph-adv/)

---

## 🔗 下一步

完成本课程后，你可以：

- 进入 M02: LlamaIndex 高级 RAG
- 学习 M03: MLOps 实验追踪
- 探索 M04: Litestar 框架

---

**最后更新**: 2026-07-18
