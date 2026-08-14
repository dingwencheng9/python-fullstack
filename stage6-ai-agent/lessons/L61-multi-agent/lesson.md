# L61: 多智能体编排 (Multi-Agent Orchestration)

> **课程编号**: L61
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐⭐（AI Agent 专家级）
> **前置课程**: L60 Agent 规划
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L58**: LangGraph 进阶（状态机与子图）
- **L55**: MCP 协议（Agent 间通信协议）

**如果你还没有学习以上课程，建议先完成前置课程。**

---

> **课程定位**: Stage 6 AI Agent 终极模块 - 使用 LangGraph 构建生产级多智能体系统  
> **前置要求**: L56 LangChain, L54 Agent 基础  
> **后续课程**: L63 Agent 评估, L64 Agent 部署  
> **学习时长**: 5-6 小时

---

---

## 📚 目录

- [第一章：LangGraph 状态机基础](#第一章langgraph-状态机基础)
- [第二章：Supervisor 路由模式](#第二章supervisor-路由模式)
- [第三章：Human-in-the-Loop](#第三章human-in-the-loop)
- [第四章：生产化实践](#第四章生产化实践)

---

## 第一章：LangGraph 状态机基础

### 1.1 核心概念

**LangGraph = 状态机 + LLM**

```yaml
StateGraph
├── 状态 (State): TypedDict 定义
├── 节点 (Node): 处理函数
├── 边 (Edge): 确定性/条件性
└── 编译 (Compile): 生成可执行图
```python
---

### 1.2 基础状态机

```python
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# 1. 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add]  # add = 消息追加到列表
    next: str

# 2. 定义节点函数
def agent_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke(state["messages"])
    return {
        "messages": [response],
        "next": "END"
    }

# 3. 构建图
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

# 4. 编译
app = graph.compile()

# 5. 执行
result = app.invoke({
    "messages": [("human", "你好")]
})
```python
---

### 1.3 状态注解 (Annotated)

```python
from typing import Annotated
from operator import add

class State(TypedDict):
    # 追加模式 (add)
    messages: Annotated[list, add]

    # 覆盖模式 (默认)
    counter: int

    # 自定义合并
    data: Annotated[dict, lambda x, y: {**x, **y}]
```python
**Annotated 作用**: 定义状态更新策略

---

## 第二章：Supervisor 路由模式

### 2.1 架构设计

```text
┌─────────────────────────────────┐
│       Supervisor Agent           │
│    (分析任务 → 选择专家)         │
└────────┬────────────┬───────────┘
         ↓            ↓
   ┌─────────┐  ┌─────────┐
   │Researcher│  │  Coder  │
   └─────────┘  └─────────┘
         ↓            ↓
   ┌─────────────────────────┐
   │      聚合结果            │
   └─────────────────────────┘
```python
---

### 2.2 完整实现

```python
from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# 状态定义
class SupervisorState(TypedDict):
    messages: Annotated[list, add]
    next: str

# Supervisor 节点
def supervisor(state: SupervisorState) -> SupervisorState:
    llm = ChatOpenAI(model="gpt-4o-mini")

    system_prompt = """
    你是一个任务协调员。分析用户请求，选择合适的专家：
    - researcher: 信息搜索和研究
    - coder: 代码编写
    - FINISH: 任务完成

    直接返回专家名称。
    """

    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    response = llm.invoke(messages)

    next_agent = response.content.strip().lower()

    return {
        "messages": [response],
        "next": next_agent
    }

# 专家 Agent 节点
def researcher(state: SupervisorState) -> SupervisorState:
    # 研究任务
    return {
        "messages": [HumanMessage(content="[Researcher] 完成研究")],
        "next": "supervisor"
    }

def coder(state: SupervisorState) -> SupervisorState:
    # 编码任务
    return {
        "messages": [HumanMessage(content="[Coder] 完成编码")],
        "next": "supervisor"
    }

# 路由函数
def should_continue(state: SupervisorState) -> Literal["researcher", "coder", "end"]:
    next_agent = state.get("next", "end")
    if next_agent == "finish":
        return "end"
    return next_agent

# 构建图
graph = StateGraph(SupervisorState)

# 添加节点
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher)
graph.add_node("coder", coder)

# 设置入口
graph.set_entry_point("supervisor")

# 条件边 (Supervisor → 专家)
graph.add_conditional_edges(
    "supervisor",
    should_continue,
    {
        "researcher": "researcher",
        "coder": "coder",
        "end": END
    }
)

# 确定边 (专家 → Supervisor)
graph.add_edge("researcher", "supervisor")
graph.add_edge("coder", "supervisor")

# 编译
app = graph.compile()

# 执行
result = app.invoke({
    "messages": [HumanMessage(content="搜索 Python 新特性并写示例代码")]
})
```text
---

### 2.3 执行流程

```text
1. 用户输入 → Supervisor
2. Supervisor 分析 → "researcher"
3. Researcher 执行 → 返回 Supervisor
4. Supervisor 再次分析 → "coder"
5. Coder 执行 → 返回 Supervisor
6. Supervisor 判断 → "finish"
7. 结束
```python
---

## 第三章：Human-in-the-Loop

### 3.1 中断机制

```python
from langgraph.checkpoint.memory import MemorySaver

# 1. 创建检查点
memory = MemorySaver()

# 2. 编译时启用中断
app = graph.compile(
    checkpointer=memory,
    interrupt_before=["human_review"]  # 在此节点前中断
)

# 3. 首次执行
config = {"configurable": {"thread_id": "1"}}
result = app.invoke(input_data, config)

# 4. 人类审核
print("请审核内容:", result)
user_feedback = input("批准还是修改？")

# 5. 继续执行
if user_feedback == "批准":
    final_result = app.invoke(None, config)  # None = 继续上次状态
```python
---

### 3.2 完整示例

```python
# 定义状态
class ReviewState(TypedDict):
    content: str
    approved: bool

# Agent 节点
def generate_content(state: ReviewState) -> ReviewState:
    return {"content": "生成的内容...", "approved": False}

# 人类审核节点
def human_review(state: ReviewState) -> ReviewState:
    print(f"待审核内容: {state['content']}")
    decision = input("批准 (y/n): ")
    return {"approved": decision.lower() == "y"}

# 条件判断
def check_approval(state: ReviewState) -> Literal["publish", "revise"]:
    return "publish" if state["approved"] else "revise"

# 构建图
graph = StateGraph(ReviewState)
graph.add_node("generate", generate_content)
graph.add_node("review", human_review)
graph.add_node("publish", lambda s: s)

graph.set_entry_point("generate")
graph.add_edge("generate", "review")
graph.add_conditional_edges("review", check_approval)

# 启用中断
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["review"]
)

# 执行
config = {"configurable": {"thread_id": "workflow-1"}}
result = app.invoke({"content": "", "approved": False}, config)

# 等待人类输入...
final = app.invoke(None, config)
```python
---

## 第四章：生产化实践

### 4.1 异步执行

```python
import asyncio

# 异步节点
async def async_agent(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}

# 异步执行
result = await app.ainvoke(input_data)
```python
---

### 4.2 流式输出

```python
# 流式执行
for chunk in app.stream(input_data):
    print(chunk)
```python
---

### 4.3 状态持久化 (PostgreSQL)

```python
from langgraph.checkpoint.postgres import PostgresSaver

# PostgreSQL59 检查点
checkpointer = PostgresSaver(
    connection_string="postgresql://user:pass@localhost/db"
)

app = graph.compile(checkpointer=checkpointer)

# 跨会话恢复
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke(input_data, config)
```python
---

### 4.4 Mock 测试

```python
from unittest.mock import AsyncMock, patch
import pytest

@pytest.mark.asyncio
async def test_supervisor_routing():
    """测试 Supervisor 路由逻辑"""

    # Mock LLM
    with patch("langchain_openai.ChatOpenAI") as mock_llm:
        mock_llm.return_value.ainvoke = AsyncMock(
            return_value=HumanMessage(content="researcher")
        )

        # 执行
        result = await app.ainvoke({"messages": [HumanMessage(content="搜索信息")]})

        # 验证
        assert result["next"] == "researcher"
```text
---

## 🎯 最佳实践总结

### ✅ 多智能体设计清单

- [ ] 状态定义清晰 (TypedDict + Annotated)
- [ ] 节点职责单一
- [ ] 路由逻辑明确
- [ ] 循环终止条件清晰
- [ ] 启用检查点持久化
- [ ] 异常处理完善
- [ ] Mock 测试覆盖

### 常见模式

**模式 1: Sequential (顺序)**

```text
A → B → C → END
```python
**模式 2: Parallel (并行)**

```text
START → [A, B, C] → Merge → END
```python
**模式 3: Supervisor (监督)**

```python
Supervisor ⇄ [Agent1, Agent2, Agent3]
```python
**模式 4: Human-in-Loop (人类参与)**

```text
Agent → [INTERRUPT] → Human → Continue
```

---

## 第五章：Agent 通信协议

### 5.1 消息队列模式

```python
import asyncio
from typing import Protocol

class AgentProtocol(Protocol):
    async def send_message(self, message: dict) -> None: ...
    async def receive_message(self) -> dict: ...

class MessageQueue:
    """Agent 间消息队列"""

    def __init__(self):
        self.queues: dict[str, asyncio.Queue] = {}

    def create_queue(self, agent_id: str) -> asyncio.Queue:
        """为 Agent 创建专用队列"""
        queue = asyncio.Queue()
        self.queues[agent_id] = queue
        return queue

    async def send(self, to: str, message: dict):
        """发送消息"""
        if to not in self.queues:
            self.create_queue(to)
        await self.queues[to].put(message)

    async def broadcast(self, message: dict):
        """广播消息"""
        for queue in self.queues.values():
            await queue.put(message)
```

### 5.2 发布-订阅模式

```python
class PubSub:
    """发布-订阅系统"""

    def __init__(self):
        self.subscribers: dict[str, list[asyncio.Queue]] = {}

    def subscribe(self, topic: str) -> asyncio.Queue:
        """订阅主题"""
        queue = asyncio.Queue()
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(queue)
        return queue

    async def publish(self, topic: str, message: dict):
        """发布消息"""
        if topic in self.subscribers:
            for queue in self.subscribers[topic]:
                await queue.put(message)
```

### 5.3 共享状态模式

```python
class SharedState:
    """共享状态协调"""

    def __init__(self):
        self.state: dict = {}
        self.lock = asyncio.Lock()

    async def update(self, key: str, value: any):
        """更新状态"""
        async with self.lock:
            self.state[key] = value

    async def get(self, key: str) -> any:
        """获取状态"""
        async with self.lock:
            return self.state.get(key)

    async def compare_and_set(self, key: str, expected: any, new_value: any) -> bool:
        """原子 CAS 操作"""
        async with self.lock:
            if self.state.get(key) == expected:
                self.state[key] = new_value
                return True
            return False
```

---

## 第六章：容错与恢复

### 6.1 Agent 失败处理

```python
class ResilientAgent:
    """带容错能力的 Agent"""

    def __init__(self, agent, max_retries: int = 3):
        self.agent = agent
        self.max_retries = max_retries

    async def execute_with_retry(self, task: dict) -> dict:
        """带重试的执行"""
        for attempt in range(self.max_retries):
            try:
                return await self.agent.execute(task)
            except AgentError as e:
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # 指数退避
                self.agent.reset()  # 重置 Agent 状态
```

### 6.2 任务超时控制

```python
import asyncio

async def execute_with_timeout(agent, task: dict, timeout: float = 60.0) -> dict:
    """带超时的任务执行"""
    try:
        return await asyncio.wait_for(
            agent.execute(task),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return {"error": "任务超时", "task_id": task.get("id")}
```

### 6.3 状态检查点

```python
class CheckpointManager:
    """检查点管理器"""

    def __init__(self, storage):
        self.storage = storage
        self.checkpoints: dict[str, dict] = {}

    async def save_checkpoint(self, workflow_id: str, state: dict):
        """保存检查点"""
        checkpoint = {
            "workflow_id": workflow_id,
            "state": state,
            "timestamp": asyncio.get_event_loop().time()
        }
        self.checkpoints[workflow_id] = checkpoint
        await self.storage.save(checkpoint)

    async def restore_checkpoint(self, workflow_id: str) -> dict | None:
        """恢复检查点"""
        return self.checkpoints.get(workflow_id)
```

---

## 第七章：性能优化

### 7.1 Agent 池化

```python
import asyncio
from queue import Queue

class AgentPool:
    """Agent 连接池"""

    def __init__(self, factory, pool_size: int = 10):
        self.factory = factory
        self.pool: Queue = Queue(maxsize=pool_size)
        self._initialize()

    def _initialize(self):
        """初始化池"""
        for _ in range(self.pool.maxsize):
            agent = self.factory()
            self.pool.put(agent)

    async def acquire(self) -> Agent:
        """获取 Agent"""
        return await asyncio.to_thread(self.pool.get)

    def release(self, agent: Agent):
        """释放 Agent"""
        self.pool.put(agent)

    async def execute(self, task: dict) -> dict:
        """使用池执行任务"""
        agent = await self.acquire()
        try:
            return await agent.execute(task)
        finally:
            self.release(agent)
```

### 7.2 任务批处理

```python
async def batch_execute(agents: list, tasks: list[dict]) -> list[dict]:
    """批量执行任务"""
    semaphore = asyncio.Semaphore(5)  # 限制并发数

    async def limited_execute(agent, task):
        async with semaphore:
            return await agent.execute(task)

    results = await asyncio.gather(*[
        limited_execute(agent, task)
        for agent, task in zip(agents, tasks)
    ])
    return results
```

### 7.3 缓存中间结果

```python
from functools import lru_cache

class CachedOrchestrator:
    """带缓存的编排器"""

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.cache = {}

    def _make_cache_key(self, task: dict) -> str:
        """生成缓存键"""
        return f"{task.get('type')}:{task.get('input', '')}"

    async def execute(self, task: dict) -> dict:
        """带缓存的执行"""
        key = self._make_cache_key(task)

        if key in self.cache:
            return self.cache[key]

        result = await self.orchestrator.execute(task)
        self.cache[key] = result
        return result
```

---

## 第八章：监控与可观测性

### 8.1 追踪执行路径

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class TracedOrchestrator:
    """带追踪的编排器"""

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    async def execute(self, task: dict) -> dict:
        """追踪执行"""
        with tracer.start_as_current_span("orchestrator.execute") as span:
            span.set_attribute("task.type", task.get("type"))
            span.set_attribute("task.id", task.get("id"))

            try:
                result = await self.orchestrator.execute(task)
                span.set_attribute("result.status", "success")
                return result
            except Exception as e:
                span.set_attribute("result.status", "error")
                span.record_exception(e)
                raise
```

### 8.2 指标收集

```python
from prometheus_client import Counter, Histogram

execution_count = Counter(
    "agent_execution_total",
    "Total agent executions",
    ["agent_name", "status"]
)

execution_duration = Histogram(
    "agent_execution_duration_seconds",
    "Agent execution duration",
    ["agent_name"]
)

async def monitored_execute(agent, task: dict) -> dict:
    """带监控的执行"""
    import time
    start = time.time()

    try:
        result = await agent.execute(task)
        execution_count.labels(agent.name, "success").inc()
        return result
    except Exception as e:
        execution_count.labels(agent.name, "error").inc()
        raise
    finally:
        execution_duration.labels(agent.name).observe(time.time() - start)
```

### 8.3 健康检查

```python
class HealthCheckMixin:
    """健康检查混入"""

    async def health_check(self) -> dict:
        """检查所有 Agent 健康状态"""
        results = {}

        for agent in self.agents:
            try:
                status = await agent.ping()
                results[agent.name] = {
                    "status": "healthy" if status else "degraded",
                    "latency_ms": status.get("latency", 0)
                }
            except Exception as e:
                results[agent.name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }

        return {
            "overall": "healthy" if all(
                r["status"] == "healthy" for r in results.values()
            ) else "degraded",
            "agents": results
        }
```

---

## 🔗 延伸阅读

### 相关课程

- **L56 LangChain 基础** - Chain 组合
- **L54 Agent 基础** - 单 Agent 实现
- **L58 LangGraph** - 深入 LangGraph

### 推荐资源

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [Multi-Agent 设计模式](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
- [Human-in-the-Loop 指南](https://langchain-ai.github.io/langgraph/how-tos/human-in-the-loop/)

---

## 📝 练习题

### 练习 1: 研究写作工作流

实现 Researcher + Writer 双 Agent:

- Researcher 搜索资料
- Writer 撰写文章
- Human 审核修改
- 最多迭代 3 轮

### 练习 2: 代码审查系统

实现 Coder + Reviewer + Tester:

- Coder 生成代码
- Reviewer 审查问题
- Tester 运行测试
- 循环直到通过

### 练习 3: 客服路由系统

实现智能客服路由:

- Classifier 分类问题
- Technical Agent 处理技术问题
- Billing Agent 处理账单问题
- General Agent 处理通用问题

---

**练习答案**: 参见 `solutions/` 目录

**下一课**: [L63 Agent 评估与优化](../L63-agent-evaluation/lesson.md)

## 🔗 下一步

[L63: Agent 评估与调试](../L63-agent-evaluation/)
