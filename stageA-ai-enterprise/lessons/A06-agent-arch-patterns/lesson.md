# A06: Agent 架构设计模式

> **课程编号**: A06
> **所属阶段**: Stage A - AI Agent 企业级 (Specialization)
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: A05
> **版本**: v5.0
> **最后更新**: 2026-07-23

---

## 📌 学习目标

完成本课程后，你将能够：

1. **理解并实现 Agent 核心架构模式**：Supervisor、ReAct、Plan-Execute 等
2. **设计多 Agent 协作系统**：任务分配、通信、状态同步
3. **构建生产级 Agent 应用**：监控、容错、可观测性
4. **优化 Agent 性能**：缓存、批处理、异步优化

---

## 📖 课程导读

### 什么是 Agent 架构模式？

Agent 架构模式是解决复杂任务分解、协作和执行的设计范式。

| 模式 | 适用场景 | 核心思想 |
|------|----------|----------|
| ReAct | 单 Agent 推理 | 推理→行动→观察循环 |
| Plan-Execute | 复杂任务 | 规划与执行分离 |
| Supervisor | 多 Agent 协调 | 中央调度 + 专家节点 |
| Hierarchical | 大规模系统 | 层级管理 + 状态聚合 |

---

## Part 1: ReAct 模式深度实现

### 1.1 模式原理

```python
"""
ReAct = Reasoning + Acting

核心循环:
1. Thought (思考): 分析当前状态，决定下一步行动
2. Action (行动): 执行工具或 API 调用
3. Observation (观察): 获取行动结果
4. 重复直到完成任务
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Literal, Optional
from abc import ABC, abstractmethod


@dataclass
class AgentState:
    """Agent 执行状态"""
    task: str
    history: list["ActionLog"] = field(default_factory=list)
    current_thought: Optional[str] = None
    context: dict = field(default_factory=dict)


@dataclass
class ActionLog:
    """动作记录"""
    thought: str
    action: str
    observation: str
    timestamp: float = field(default_factory=time.time)


class ActionType(Enum):
    """可执行的动作类型"""
    SEARCH = "search"
    CALCULATE = "calculate"
    RETRIEVE = "retrieve"
    EXECUTE = "execute"
    RESPOND = "respond"
    ASK_USER = "ask_user"
```

### 1.2 ReAct Agent 实现

```python
import time
import json
from typing import Callable


class ReActAgent:
    """ReAct 模式 Agent 实现"""

    def __init__(
        self,
        llm: Callable[[str], str],
        tools: dict[str, Callable],
        max_iterations: int = 10,
    ):
        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations
        self.state = None

    def solve(self, task: str) -> str:
        """执行 ReAct 循环"""
        self.state = AgentState(task=task)

        for iteration in range(self.max_iterations):
            # 1. 思考阶段
            thought = self._think()
            self.state.current_thought = thought

            # 2. 决定动作
            action_type, action_input = self._decide_action(thought)

            # 3. 执行动作
            if action_type == ActionType.RESPOND:
                return action_input

            observation = self._act(action_type, action_input)

            # 4. 记录历史
            self.state.history.append(ActionLog(
                thought=thought,
                action=f"{action_type.value}: {action_input}",
                observation=observation,
            ))

        return "任务超时，未能完成"

    def _think(self) -> str:
        """生成思考"""
        history_text = self._format_history()

        prompt = f"""任务: {self.state.task}

历史:
{history_text}

请分析当前状态，决定下一步行动。输出格式:
思考: <你的推理过程>
动作: <search|calculate|retrieve|execute|respond>
输入: <动作参数>
"""
        response = self.llm(prompt)

        # 解析 LLM 响应
        return response

    def _decide_action(self, thought: str) -> tuple[ActionType, str]:
        """解析动作决策"""
        # 简单解析，实际应使用更 robust 的方法
        if "respond" in thought.lower():
            return ActionType.RESPOND, self._extract_response(thought)
        elif "search" in thought.lower():
            return ActionType.SEARCH, self._extract_search_query(thought)
        # ... 其他动作类型
        return ActionType.RESPOND, "无法完成"

    def _act(self, action_type: ActionType, action_input: str) -> str:
        """执行动作"""
        if action_type == ActionType.SEARCH:
            tool = self.tools.get("search")
            if tool:
                return tool(action_input)
        elif action_type == ActionType.CALCULATE:
            tool = self.tools.get("calculate")
            if tool:
                return str(tool(action_input))
        return "未知动作"

    def _format_history(self) -> str:
        """格式化历史"""
        if not self.state.history:
            return "无历史记录"
        return "\n".join(
            f"- 思考: {log.thought}\n  动作: {log.action}\n  观察: {log.observation}"
            for log in self.state.history
        )

    def _extract_response(self, thought: str) -> str:
        """提取响应内容"""
        # 从 thought 中提取最终响应
        return "根据分析..."
```

---

## Part 2: Plan-Execute 模式

### 2.1 模式原理

```python
"""
Plan-Execute = 规划阶段 + 执行阶段分离

优势:
1. 规划阶段可以"预演"，避免执行错误
2. 支持人工审核计划
3. 计划可以缓存和复用
"""

from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class PlanStep:
    """计划步骤"""
    id: int
    action: str
    params: dict
    dependencies: list[int] = field(default_factory=list)
    status: str = "pending"  # pending, executing, completed, failed
    result: Optional[str] = None


@dataclass
class ExecutionPlan:
    """执行计划"""
    steps: list[PlanStep]
    estimated_cost: float = 0.0
    estimated_time: float = 0.0
    requires_approval: bool = False
    approved: bool = False


class PlanGenerator:
    """计划生成器"""

    def __init__(self, llm: Callable[[str], str]):
        self.llm = llm

    def generate(self, task: str) -> ExecutionPlan:
        """生成执行计划"""
        prompt = f"""任务: {task}

请将任务分解为可执行的步骤，输出 JSON 格式:
{{
    "steps": [
        {{"id": 1, "action": "...", "params": {{}}, "dependencies": []}}
    ],
    "estimated_cost": 0.0,
    "estimated_time": 0.0
}}
"""
        response = self.llm(prompt)
        plan_data = json.loads(response)

        steps = [
            PlanStep(
                id=step["id"],
                action=step["action"],
                params=step.get("params", {}),
                dependencies=step.get("dependencies", []),
            )
            for step in plan_data["steps"]
        ]

        return ExecutionPlan(
            steps=steps,
            estimated_cost=plan_data.get("estimated_cost", 0.0),
            estimated_time=plan_data.get("estimated_time", 0.0),
            requires_approval=plan_data.get("estimated_cost", 0) > 10.0,
        )


class PlanExecutor:
    """计划执行器"""

    def __init__(self, tools: dict[str, Callable]):
        self.tools = tools

    def execute(self, plan: ExecutionPlan) -> list[PlanStep]:
        """执行计划"""
        if plan.requires_approval and not plan.approved:
            raise PermissionError("计划需要人工审批")

        results = []
        completed = set()

        while len(completed) < len(plan.steps):
            # 找到可执行的步骤
            for step in plan.steps:
                if step.id in completed:
                    continue
                if all(dep in completed for dep in step.dependencies):
                    # 执行步骤
                    step.status = "executing"
                    step.result = self._execute_step(step)
                    step.status = "completed"
                    completed.add(step.id)
                    results.append(step)

        return results

    def _execute_step(self, step: PlanStep) -> str:
        """执行单个步骤"""
        tool = self.tools.get(step.action)
        if not tool:
            return f"未知动作: {step.action}"
        return str(tool(**step.params))
```

### 2.2 Human-in-the-Loop 集成

```python
class HumanInLoopPlanner:
    """人工介入计划器"""

    def __init__(
        self,
        plan_generator: PlanGenerator,
        approval_callback: Callable[[ExecutionPlan], bool],
    ):
        self.plan_generator = plan_generator
        self.approval_callback = approval_callback

    async def plan_and_approve(self, task: str) -> ExecutionPlan:
        """生成计划并请求审批"""
        plan = self.plan_generator.generate(task)

        if plan.requires_approval:
            approved = await self.approval_callback(plan)
            plan.approved = approved
            if not approved:
                raise PermissionError("计划未获批准")

        return plan
```

---

## Part 3: Supervisor 模式

### 3.1 模式原理

```python
"""
Supervisor 模式 = 中央调度器 + 专家 Agent

                    ┌─────────────┐
                    │ Supervisor  │
                    └──────┬──────┘
                           │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   ┌─────────┐      ┌─────────┐      ┌─────────┐
   │Research │      │ Writer  │      │Reviewer │
   │ Agent   │      │ Agent   │      │ Agent   │
   └─────────┘      └─────────┘      └─────────┘
```

### 3.2 Supervisor 实现

```python
from typing import Literal


class SupervisorAgent:
    """Supervisor 模式实现"""

    def __init__(
        self,
        llm: Callable[[str], str],
        agents: dict[str, "BaseAgent"],
    ):
        self.llm = llm
        self.agents = agents
        self.current_task: Optional[str] = None

    async def process(self, task: str) -> str:
        """处理任务"""
        self.current_task = task

        # 分析任务类型
        task_type = await self._classify_task(task)

        # 选择合适的 Agent
        agent = self._select_agent(task_type)

        # 委托执行
        result = await agent.execute(task)

        # 质量检查
        if not await self._quality_check(result):
            # 重新执行
            result = await self._retry(agent, task)

        return result

    async def _classify_task(self, task: str) -> str:
        """任务分类"""
        prompt = f"""分析任务类型:
{task}

可选类型: research, write, review, calculate, search, general
输出: <类型>
"""
        return self.llm(prompt).strip().lower()

    def _select_agent(self, task_type: str) -> "BaseAgent":
        """选择 Agent"""
        agent_map = {
            "research": self.agents["research"],
            "write": self.agents["writer"],
            "review": self.agents["reviewer"],
            "calculate": self.agents["calculator"],
            "search": self.agents["search"],
        }
        return agent_map.get(task_type, self.agents["general"])

    async def _quality_check(self, result: str) -> bool:
        """质量检查"""
        prompt = f"""评估结果质量:
{result}

检查项:
1. 是否完整回答了问题
2. 是否有事实错误
3. 格式是否规范

输出: yes 或 no 及原因
"""
        response = self.llm(prompt)
        return "yes" in response.lower()

    async def _retry(self, agent: "BaseAgent", task: str) -> str:
        """重试"""
        return await agent.execute(task)
```

---

## Part 4: 多 Agent 协作系统

### 4.1 Agent 通信协议

```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class AgentMessage:
    """Agent 间消息"""
    id: str = field(default_factory=lambda: str(uuid4()))
    sender: str = ""
    receiver: str = ""
    content: dict = field(default_factory=dict)
    message_type: str = "request"  # request, response, broadcast
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None


class MessageBus:
    """消息总线"""

    def __init__(self):
        self.subscribers: dict[str, list] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()

    def subscribe(self, agent_id: str, topics: list[str]):
        """订阅主题"""
        for topic in topics:
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            self.subscribers[topic].append(agent_id)

    def publish(self, topic: str, message: AgentMessage):
        """发布消息"""
        self.message_queue.put_nowait((topic, message))

    async def dispatch(self):
        """分发消息"""
        while True:
            topic, message = await self.message_queue.get()
            for subscriber in self.subscribers.get(topic, []):
                await self._deliver(subscriber, message)


class MultiAgentSystem:
    """多 Agent 系统"""

    def __init__(self):
        self.agents: dict[str, "BaseAgent"] = {}
        self.message_bus = MessageBus()

    def register(self, agent: "BaseAgent"):
        """注册 Agent"""
        self.agents[agent.id] = agent
        self.message_bus.subscribe(agent.id, agent.topics)

    async def send_message(
        self,
        sender: str,
        receiver: str,
        content: dict,
    ) -> AgentMessage:
        """发送消息"""
        message = AgentMessage(
            sender=sender,
            receiver=receiver,
            content=content,
            message_type="request",
        )

        self.message_bus.publish(receiver, message)

        # 等待响应
        response = await self._wait_for_response(message.correlation_id)
        return response

    async def broadcast(
        self,
        sender: str,
        topic: str,
        content: dict,
    ) -> list[AgentMessage]:
        """广播消息"""
        message = AgentMessage(
            sender=sender,
            content=content,
            message_type="broadcast",
        )

        self.message_bus.publish(topic, message)

        # 收集所有响应
        responses = []
        for _ in range(len(self.message_bus.subscribers.get(topic, []))):
            response = await self._wait_for_response(message.correlation_id)
            responses.append(response)

        return responses
```

---

## Part 5: 生产环境实践

### 5.1 监控与可观测性

```python
from prometheus_client import Counter, Histogram, Gauge
import structlog

# 指标定义
agent_requests = Counter(
    "agent_requests_total",
    "Total requests",
    ["agent_id", "status"],
)

agent_latency = Histogram(
    "agent_latency_seconds",
    "Agent processing latency",
    ["agent_id", "action_type"],
)

active_agents = Gauge(
    "active_agents",
    "Number of active agents",
    ["agent_type"],
)

# 日志
logger = structlog.get_logger()


class MonitoredAgent:
    """带监控的 Agent 基类"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    async def execute(self, task: str) -> str:
        start_time = time.time()

        try:
            result = await self._execute_impl(task)

            agent_requests.labels(
                agent_id=self.agent_id,
                status="success",
            ).inc()

            return result

        except Exception as e:
            agent_requests.labels(
                agent_id=self.agent_id,
                status="error",
            ).inc()

            logger.error(
                "agent_execution_failed",
                agent_id=self.agent_id,
                error=str(e),
            )
            raise

        finally:
            latency = time.time() - start_time
            agent_latency.labels(
                agent_id=self.agent_id,
                action_type="execute",
            ).observe(latency)

    @abstractmethod
    async def _execute_impl(self, task: str) -> str:
        """实际执行逻辑"""
        pass
```

### 5.2 错误处理与重试

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential


class ResilientAgent:
    """带重试的 Agent"""

    def __init__(
        self,
        base_agent: "BaseAgent",
        max_retries: int = 3,
    ):
        self.base_agent = base_agent
        self.max_retries = max_retries

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def execute_with_retry(self, task: str) -> str:
        """带指数退避的重试"""
        try:
            return await self.base_agent.execute(task)
        except RateLimitError:
            # 触发重试
            raise
        except PermanentError:
            # 不重试，直接返回错误
            raise

    async def execute_with_fallback(
        self,
        task: str,
        fallback: Callable[[str], str],
    ) -> str:
        """带降级的执行"""
        try:
            return await self.execute_with_retry(task)
        except Exception as e:
            logger.warning(
                "agent_execution_fallback",
                error=str(e),
            )
            return fallback(task)
```

---

## 💡 常见陷阱

### 陷阱 1: 过度设计的 Agent 架构

```python
# ❌ 错误：为简单任务创建复杂的多 Agent 系统
class OverEngineeredSystem:
    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.planner = PlanGenerator()
        self.executor = PlanExecutor()
        self.reviewer = ReviewAgent()
        self.cacher = CacheManager()
        # ... 10+ 组件

# ✅ 正确：从简单开始，按需扩展
class SimpleAgent:
    def __init__(self):
        self.llm = openai.ChatCompletion.create
        self.tools = {"search": search_tool}

    async def solve(self, task: str) -> str:
        return await self.llm(task)
```

### 陷阱 2: 忽略 Agent 状态管理

```python
# ❌ 错误：无状态的 Agent
class StatelessAgent:
    async def solve(self, task: str) -> str:
        # 每次都从头开始，无法利用历史上下文
        return await self.llm(task)

# ✅ 正确：维护对话历史
class StatefulAgent:
    def __init__(self):
        self.conversation_history: list[dict] = []

    async def solve(self, task: str) -> str:
        self.conversation_history.append({"role": "user", "content": task})
        response = await self.llm(self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
```

---

## 📚 延伸阅读

- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [AutoGen 框架](https://microsoft.github.io/autogen/)
- [CrewAI 框架](https://docs.crewai.com/)
- [Agent 设计模式](https://arxiv.org/abs/2308.00352)

---

## ✅ 自检清单

- [ ] 理解 ReAct 模式的推理→行动→观察循环
- [ ] 实现 Plan-Execute 模式的任务规划
- [ ] 设计 Supervisor 模式的多 Agent 协调
- [ ] 实现 Agent 间的消息通信机制
- [ ] 添加监控和错误处理

---

## 🔗 下一步

- [A07: Agent 安全渗透测试](../A07-agent-pentest/) — 红队测试方法论
- [A08: Agent 安全护栏](../A08-agent-guardrails/) — 输入输出过滤

---

**课程制作**: Python 3.13 全栈课程组
**最后更新**: 2026-07-23
**版本**: v5.0
