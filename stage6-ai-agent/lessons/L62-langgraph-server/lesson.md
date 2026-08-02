L62: LangGraph 高级模式与生产部署 - 详细教程

> **课程编号**: L62
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐⭐（AI Agent 专家级）
> **前置课程**: L61 多智能体
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


---

---

## 📚 目录

- [第一章：LangGraph 基础](#第一章langgraph-基础)
- [第二章：条件路由与循环](#第二章条件路由与循环)
- [第三章：状态持久化](#第三章状态持久化)
- [第四章：高级特性](#第四章高级特性)

---

## 第一章：LangGraph 基础

### 1.1 为什么需要 LangGraph？

**LangChain LCEL 的局限**:

- ❌ 循环难以实现
- ❌ 条件分支复杂
- ❌ 状态管理困难

**LangGraph 的优势**:

- ✅ 声明式状态机
- ✅ 原生支持循环
- ✅ 灵活的条件路由
- ✅ 持久化与中断

---

### 1.2 基础状态机

```python
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, END

# 1. 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add]  # add = 追加模式
    iteration: int

# 2. 定义节点函数
def agent_node(state: AgentState) -> AgentState:
    return {
        "messages": [f"处理第 {state['iteration']} 轮"],
        "iteration": state["iteration"] + 1
    }

# 3. 构建图
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

# 4. 编译
app = graph.compile()

# 5. 执行
result = app.invoke({"messages": [], "iteration": 1})
print(result)
# {'messages': ['处理第 1 轮'], 'iteration': 2}
```python
---

### 1.3 状态注解详解

```python
from typing import Annotated
from operator import add

class State(TypedDict):
    # 追加模式 (列表累加)
    messages: Annotated[list, add]

    # 覆盖模式 (默认)
    counter: int

    # 自定义合并
    data: Annotated[dict, lambda old, new: {**old, **new}]
```python
**注解作用**: 定义多个节点更新同一状态字段时的合并策略

---

## 第二章：条件路由与循环

### 2.1 条件边 (Conditional Edges)

```python
from typing import Literal

class State(TypedDict):
    messages: Annotated[list, add]
    next: str

def agent_node(state: State) -> State:
    # 决定下一步
    if len(state["messages"]) < 3:
        return {"messages": ["继续"], "next": "continue"}
    return {"messages": ["完成"], "next": "end"}

# 路由函数
def should_continue(state: State) -> Literal["agent", "end"]:
    return "agent" if state["next"] == "continue" else "end"

# 构建图
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")

# 条件边
graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "agent": "agent",  # 循环
        "end": END
    }
)

app = graph.compile()
result = app.invoke({"messages": [], "next": ""})
```python
---

### 2.2 工具调用循环

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langchain.tools import tool

# 定义工具
@tool
def search(query: str) -> str:
    """搜索工具"""
    return f"搜索结果: {query}"

tools = [search]
tool_node = ToolNode(tools)

# Agent 节点
def agent_node(state: State):
    llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 路由函数
def should_continue(state: State) -> Literal["tools", "end"]:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

# 构建图
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")  # 工具执行后返回 Agent

app = graph.compile()
```python
---

### 2.3 多路由决策

```python
from typing import Literal

def route_decision(state: State) -> Literal["research", "code", "review", "end"]:
    last_msg = state["messages"][-1].content

    if "搜索" in last_msg:
        return "research"
    elif "代码" in last_msg:
        return "code"
    elif "审查" in last_msg:
        return "review"
    else:
        return "end"

# 构建图
graph = StateGraph(State)
graph.add_node("supervisor", supervisor_node)
graph.add_node("research", research_node)
graph.add_node("code", code_node)
graph.add_node("review", review_node)

graph.set_entry_point("supervisor")
graph.add_conditional_edges(
    "supervisor",
    route_decision,
    {
        "research": "research",
        "code": "code",
        "review": "review",
        "end": END
    }
)

# 所有专家节点返回 supervisor
graph.add_edge("research", "supervisor")
graph.add_edge("code", "supervisor")
graph.add_edge("review", "supervisor")
```python
---

## 第三章：状态持久化

### 3.1 内存检查点

```python
from langgraph.checkpoint.memory import MemorySaver

# 创建检查点
memory = MemorySaver()

# 编译时启用
app = graph.compile(checkpointer=memory)

# 执行 (带线程 ID)
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke(input_data, config)

# 后续调用自动恢复状态
result2 = app.invoke(new_input, config)  # 继承之前的状态
```python
---

### 3.2 Human-in-the-Loop 中断

```python
# 编译时指定中断点
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["human_review"]  # 在此节点前中断
)

# 首次执行
config = {"configurable": {"thread_id": "workflow-1"}}
result = app.invoke({"messages": [HumanMessage("请生成代码")]}, config)

# 工作流中断，等待人类审核
print(result)  # 显示当前状态

# 人类审核后继续
user_feedback = input("批准 (y/n): ")
if user_feedback == "y":
    final_result = app.invoke(None, config)  # None = 继续
```python
---

### 3.3 PostgreSQL 持久化

```python
from langgraph.checkpoint.postgres import PostgresSaver

# PostgreSQL 检查点
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/db"
)

app = graph.compile(checkpointer=checkpointer)

# 跨会话/进程恢复
config = {"configurable": {"thread_id": "user-456"}}
result = app.invoke(input_data, config)
```python
---

### 3.4 Redis Checkpointer: 分布式生产部署

**生产环境推荐方案**，适用于：
- ✅ 多实例水平扩展
- ✅ 毫秒级状态恢复
- ✅ 自动 TTL 过期清理
- ✅ 高可用 Redis Cluster

```python
# 安装: pip install langgraph-checkpoint-redis

from langgraph.checkpoint.redis import RedisSaver
from langgraph.graph import StateGraph, START, END
import redis.asyncio as aioredis
import os

class LangGraphServer:
    """LangGraph 生产服务器"""

    def __init__(self):
        self.app = None
        self._setup_graph()

    def _setup_graph(self):
        """初始化图"""
        graph = StateGraph(State)
        graph.add_node("agent", self.agent_node)
        graph.add_node("tools", self.tools_node)
        graph.add_edge(START, "agent")
        graph.add_edge("tools", "agent")
        # ... 添加条件边

        # Redis Checkpointer（生产级）
        self.app = graph.compile(
            checkpointer=RedisSaver.from_conn_string(
                os.getenv("REDIS_URL", "redis://localhost:6379"),
                session_ttl=int(os.getenv("SESSION_TTL", "3600"))
            )
        )

    async def handle_request(self, user_input: str, thread_id: str):
        """处理请求"""
        config = {"configurable": {"thread_id": thread_id}}

        # 流式响应
        async for chunk in self.app.astream(
            {"messages": [HumanMessage(user_input)]},
            config
        ):
            yield chunk

# Docker 部署
"""
services:
  agent-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      REDIS_URL: redis://redis:6379
      SESSION_TTL: "7200"
    depends_on:
      redis:
        condition: service_healthy

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: >
      redis-server
      --appendonly yes
      --maxmemory 2gb
      --maxmemory-policy allkeys-lru
"""

# Kubernetes 部署
"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-server
spec:
  replicas: 3  # 水平扩展
  template:
    spec:
      containers:
      - name: agent
        env:
        - name: REDIS_URL
          value: "redis://redis-cluster:6379"
        - name: SESSION_TTL
          value: "3600"
"""
```

### 3.5 Checkpointer 选型指南

| 场景 | Checkpointer | 配置要点 |
|------|--------------|----------|
| 开发/测试 | MemorySaver | 无需额外依赖 |
| 小型生产 | PostgresSaver | 连接池大小 |
| **大型生产** | **RedisSaver** | **session_ttl + 连接池** |
| 高可用 | Redis Cluster | Sentinel 故障转移 |

---

## 第四章：高级特性

### 4.1 流式输出

```python
# 流式执行
for chunk in app.stream({"messages": [HumanMessage("你好")]}):
    print(chunk)
    # 输出: {'agent': {...}}, {'tools': {...}}, ...
```python
---

### 4.2 异步执行

```python
import asyncio

async def run_agent():
    result = await app.ainvoke({"messages": [HumanMessage("查询")]})
    return result

result = asyncio.run(run_agent())
```text
---

### 4.3 子图 (Subgraph)

```python
# 定义子图
subgraph = StateGraph(SubState)
subgraph.add_node("step1", step1_node)
subgraph.add_node("step2", step2_node)
subgraph.add_edge("step1", "step2")
compiled_subgraph = subgraph.compile()

# 嵌入主图
main_graph = StateGraph(MainState)
main_graph.add_node("subgraph", compiled_subgraph)
```text
---

### 4.4 并行执行

```python
# 并行节点
graph.add_node("parallel_a", node_a)
graph.add_node("parallel_b", node_b)

# 同时触发
graph.add_edge("start", "parallel_a")
graph.add_edge("start", "parallel_b")

# 汇聚
graph.add_edge("parallel_a", "merge")
graph.add_edge("parallel_b", "merge")
```text
---

## 第五章：生产部署与监控

### 5.1 图序列化与反序列化

```python
import json

# 序列化图结构
def serialize_graph(app):
    """将编译后的图序列化为 JSON"""
    graph_def = {
        "nodes": list(app.graph.nodes.keys()),
        "edges": [
            {"from": edge.source, "to": edge.target}
            for edge in app.graph.edges
        ],
    }
    return json.dumps(graph_def, indent=2)

# 反序列化并重建
def deserialize_and_run(graph_json: str, input_data: dict):
    """从 JSON 重建图并执行"""
    graph_def = json.loads(graph_json)
    # 重建图结构...
    return app.invoke(input_data)
```

### 5.2 FastAPI 集成

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI(title="LangGraph Agent API")

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    thread_id: str
    interrupted: bool = False

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}

    # 检查是否有中断的工作流
    if app.get_state(config) and app.get_state(config).next:
        # 恢复执行
        result = app.invoke(None, config)
    else:
        # 新请求
        result = app.invoke(
            {"messages": [HumanMessage(request.message)]},
            config
        )

    return ChatResponse(
        response=result["messages"][-1].content,
        thread_id=request.thread_id,
    )

@app.get("/status/{thread_id}")
async def get_status(thread_id: str):
    """获取工作流状态"""
    config = {"configurable": {"thread_id": thread_id}}
    state = app.get_state(config)
    return {
        "thread_id": thread_id,
        "next_node": state.next if state else None,
        "messages_count": len(state.values.get("messages", [])) if state else 0,
    }

@app.post("/interrupt/{thread_id}")
async def interrupt_workflow(thread_id: str):
    """中断工作流"""
    app.update_state(
        {"configurable": {"thread_id": thread_id}},
        {"should_interrupt": True}
    )
    return {"status": "interrupted"}
```

### 5.3 Prometheus 监控

```python
from prometheus_client import Counter, Histogram, Gauge

# 指标定义
graph_invocations = Counter(
    "langgraph_invocations_total",
    "Total graph invocations",
    ["graph_name", "status"]
)

graph_duration = Histogram(
    "langgraph_invocation_duration_seconds",
    "Graph invocation duration",
    ["graph_name"]
)

active_threads = Gauge(
    "langgraph_active_threads",
    "Number of active threads",
    ["graph_name"]
)

def monitored_invoke(app, input_data: dict, config: dict):
    """带监控的图调用"""
    import time
    start = time.time()

    try:
        result = app.invoke(input_data, config)
        graph_invocations.labels(graph_name=app.graph.name, status="success").inc()
        return result
    except Exception as e:
        graph_invocations.labels(graph_name=app.graph.name, status="error").inc()
        raise
    finally:
        graph_duration.labels(graph_name=app.graph.name).observe(time.time() - start)
```

---

## 第六章：错误处理与重试

### 6.1 节点级重试

```python
from tenacity import retry, stop_after_attempt, wait_exponential

def robust_node(state: State) -> State:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def call_external_api(data):
        # 可能失败的外部调用
        return external_service.process(data)

    result = call_external_api(state["data"])
    return {"result": result}
```

### 6.2 错误边界节点

```python
def error_boundary(state: State, error: Exception) -> State:
    """错误处理节点"""
    return {
        "error": str(error),
        "error_type": type(error).__name__,
        "messages": [
            AIMessage(content=f"处理失败: {error}")
        ]
    }

# 添加错误处理边
graph.add_edge("risky_node", "error_handler")
graph.add_edge("error_handler", END)
```

### 6.3 超时控制

```python
import signal
from functools import wraps

def timeout_handler(signum, frame):
    raise TimeoutError("Node execution timed out")

def with_timeout(seconds: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
        return wrapper
    return decorator

@with_timeout(30)
def long_running_node(state: State) -> State:
    """带超时的节点"""
    return process(state)
```

---

## 第七章：状态可视化与调试

### 7.1 生成 Mermaid 图表

```python
def generate_mermaid_diagram(app):
    """生成 Mermaid 格式的图"""
    lines = ["```mermaid", "stateDiagram-v2"]

    # 添加状态
    for node in app.graph.nodes:
        lines.append(f'    [*] --> {node}')
        lines.append(f'    {node} --> [*]')

    # 添加边
    for edge in app.graph.edges:
        lines.append(f'    {edge.source} --> {edge.target}')

    lines.append("```")
    return "\n".join(lines)
```

### 7.2 状态历史追踪

```python
def get_execution_history(app, thread_id: str):
    """获取执行历史"""
    config = {"configurable": {"thread_id": thread_id}}
    history = []

    for checkpoint in app.get_state_history(config):
        history.append({
            "timestamp": checkpoint.config.get("timestamp"),
            "next_node": checkpoint.next,
            "values": checkpoint.values,
        })

    return history

def visualize_history(history: list):
    """可视化执行历史"""
    for i, state in enumerate(history):
        print(f"\n=== Step {i} ===")
        print(f"Next: {state['next_node']}")
        print(f"Messages: {len(state['values'].get('messages', []))}")
```

### 7.3 条件边调试

```python
def debug_route(state: State) -> Literal["a", "b", "end"]:
    """带调试输出的路由函数"""
    print(f"[DEBUG] Routing with state: {state}")

    if state["should_continue"]:
        print(f"[DEBUG] → Routing to 'a'")
        return "a"
    else:
        print(f"[DEBUG] → Routing to 'end'")
        return "end"

# 在生产环境使用
def production_route(state: State) -> Literal["a", "b", "end"]:
    """生产环境路由函数"""
    return "a" if state["should_continue"] else "end"
```

---

## 第八章：高级模式

### 8.1 动态图构建

```python
def build_dynamic_graph(steps: list[str]) -> CompiledGraph:
    """根据配置动态构建图"""
    graph = StateGraph(State)

    # 添加所有步骤节点
    for step in steps:
        graph.add_node(step, create_step_node(step))

    # 设置入口点
    graph.set_entry_point(steps[0])

    # 连接所有步骤
    for i in range(len(steps) - 1):
        graph.add_edge(steps[i], steps[i + 1])

    # 添加条件边（最后一步）
    graph.add_conditional_edges(
        steps[-1],
        lambda state: "end" if state["complete"] else steps[-1]
    )

    return graph.compile()

# 使用
graph = build_dynamic_graph(["validate", "transform", "load"])
```

### 8.2 动态节点注册

```python
class DynamicGraphBuilder:
    """动态图构建器"""

    def __init__(self, state_class: type):
        self.graph = StateGraph(state_class)
        self.nodes = {}

    def register_node(self, name: str, func: callable):
        """注册节点"""
        self.graph.add_node(name, func)
        self.nodes[name] = func

    def register_sequential_edges(self, node_names: list[str]):
        """注册顺序边"""
        for i in range(len(node_names) - 1):
            self.graph.add_edge(node_names[i], node_names[i + 1])

    def compile(self) -> CompiledGraph:
        """编译图"""
        return self.graph.compile()

# 使用
builder = DynamicGraphBuilder(AgentState)
builder.register_node("start", start_node)
builder.register_node("process", process_node)
builder.register_node("end", end_node)
builder.register_sequential_edges(["start", "process", "end"])
app = builder.compile()
```

### 8.3 Send 并行模式

```python
from typing import Annotated
from operator import add
from langgraph.constants import Send

class ParallelState(TypedDict):
    results: Annotated[list, add]
    status: str

def fan_out_function(state: ParallelState) -> list[dict]:
    """Fan-out: 返回多个任务"""
    tasks = []
    for item in state["items"]:
        tasks.append(Send("worker", {"item": item}))
    return tasks

def worker_node(state: dict) -> dict:
    """工作节点"""
    return {"results": [process_item(state["item"])]}

graph = StateGraph(ParallelState)
graph.add_node("fan_out", fan_out_function)
graph.add_node("worker", worker_node)
graph.add_node("merge", merge_node)

graph.set_entry_point("fan_out")
graph.add_conditional_edges("fan_out", lambda x: ["worker"] * len(x["items"]))
graph.add_edge("worker", "merge")
```

---

## 第九章：LangGraph 与 LangChain 集成

### 9.1 使用 LangChain 的 LLM

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage

def create_llm_node(
    model_name: str = "gpt-4o-mini",
    temperature: float = 0
):
    """创建 LLM 节点工厂"""
    if "gpt" in model_name:
        llm = ChatOpenAI(model=model_name, temperature=temperature)
    elif "claude" in model_name:
        llm = ChatAnthropic(model=model_name)
    else:
        raise ValueError(f"Unsupported model: {model_name}")

    def llm_node(state: State) -> State:
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    return llm_node

# 使用
graph.add_node("llm", create_llm_node("gpt-4o-mini", temperature=0.7))
```

### 9.2 使用 LangChain 工具

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate

@tool
def get_weather(city: str) -> str:
    """获取天气信息"""
    return f"{city}今天晴天，20°C"

@tool
def search_news(topic: str) -> str:
    """搜索新闻"""
    return f"关于{topic}的最新新闻..."

tools = [get_weather, search_news]

def create_agent_tools_node(prompt_template: str):
    """创建 Agent 工具节点"""
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)

    def agent_tools_node(state: State) -> State:
        result = executor.invoke({"input": state["messages"][-1].content})
        return {"messages": [AIMessage(content=result["output"])]}

    return agent_tools_node
```

### 9.3 RAG 集成

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def create_rag_node(vectorstore: Chroma, k: int = 3):
    """创建 RAG 检索节点"""

    def rag_node(state: State) -> State:
        query = state["messages"][-1].content

        # 检索相关文档
        docs = vectorstore.similarity_search(query, k=k)

        # 构建上下文
        context = "\n".join([doc.page_content for doc in docs])

        # 增强查询
        enhanced_query = f"基于以下上下文回答问题：\n\n{context}\n\n问题：{query}"

        return {"enhanced_query": enhanced_query, "retrieved_docs": docs}

    return rag_node
```

---

## 🎯 最佳实践总结

### ✅ LangGraph 设计清单

- [ ] 状态定义清晰 (TypedDict + 必要字段)
- [ ] 使用 Annotated 定义合并策略
- [ ] 节点函数职责单一
- [ ] 路由逻辑显式清晰
- [ ] 循环有明确终止条件
- [ ] 启用 Checkpointer 持久化
- [ ] 关键节点添加 Human-in-Loop

### 常见模式

**模式 1: 简单顺序流**

```text
START → A → B → C → END
```python
**模式 2: 条件分支**

```text
START → Agent → [条件] → Tools/END
```python
**模式 3: 循环处理**

```text
START → Agent ⇄ Tools (循环) → END
```python
**模式 4: 并行执行**

```text
START → [A, B, C 并行] → Merge → END
```

---

## 🔗 延伸阅读

### 相关课程

- **L53 LangChain 基础** - LCEL 管道
- **L54 Agent 基础** - ReAct Agent
- **L61 多智能体编排** - Supervisor 模式

### 推荐资源

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [LangGraph 教程](https://langchain-ai.github.io/langgraph/tutorials/)
- [状态机模式](https://en.wikipedia.org/wiki/Finite-state_machine)

---

## 📝 练习题

### 练习 1: 任务规划 Agent

创建规划执行循环:

- Agent 生成计划
- 执行每个步骤
- 验证结果
- 循环直到完成

### 练习 2: 代码审查工作流

实现代码生成审查流程:

- Coder 生成代码
- Reviewer 审查
- 如不通过返回 Coder
- 最多迭代 3 次

### 练习 3: Human-in-Loop 审批

实现需要人类审批的工作流:

- Agent 生成方案
- 中断等待审批
- 批准后继续执行
- 支持多轮修改

---

**练习答案**: 参见 `solutions/` 目录

---

## 📝 本章总结

### 核心知识点

1. **LangGraph 图结构**：StateGraph、节点、边、条件边
2. **状态管理**：TypedDict 状态、状态更新、状态合并
3. **条件分支**：路由函数、条件边、多分支切换
4. **持久化**：CheckpointSaver、状态保存与恢复
5. **流式输出**：Token 流、节点流、状态流
6. **Human-in-the-Loop**：中断、审批、动态修改状态
7. **多 Agent 协作**：子图调用、状态传递、共享上下文
8. **生产部署**：序列化图结构、API 服务化、监控

### 关键要点

- ✅ LangGraph = 有状态的可视化工作流
- ✅ 状态是跨节点共享的数据
- ✅ Checkpoint 支持断点恢复
- ✅ Human-in-the-Loop 实现人工干预
- ✅ 流式输出提升用户体验

### 常见陷阱

- ❌ 状态定义过于复杂（难以维护）
- ❌ 忘记保存 Checkpoint（无法恢复）
- ❌ 条件边逻辑错误（死循环或死路）
- ❌ 不处理流式中断
- ❌ 多 Agent 状态混淆

### 实用技巧

- 💡 使用 `START → node → END` 简化图定义
- 💡 使用 `@entrypoint` 部署图结构
- 💡 使用 `MemorySaver` 开发环境存储
- 💡 使用 `sqlite` 或 `postgres` 生产存储
- 💡 使用 `interrupt()` 插入人工审批点
- 💡 使用 `update_state()` 动态修改状态

### 典型应用场景

- 🔄 复杂工作流自动化（多步骤审批）
- 💬 对话系统（带记忆的聊天机器人）
- 📝 文档处理流水线（解析 → 提取 → 生成）
- 🎮 游戏 AI（NPC 决策树）
- 🔧 DevOps 自动化（部署流水线）


## 🔗 下一步


[L59: Agent 记忆管理](../L59-agent-memory/)
