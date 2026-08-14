# L58: LangGraph 工作流编排（基础）

> **课程编号**: L58
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 4-6 小时
> **难度**: ⭐⭐⭐☆☆（中级）
> **前置课程**: L56 LangChain 与应用编排, L57 RAG 向量数据库
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

---

## 🎯 课程目标

本课程将帮助你：

1. 理解 LangGraph 的核心概念和设计哲学
2. 掌握 StateGraph 的构建方法
3. 学会使用条件路由和边控制流
4. 实现状态持久化和记忆系统
5. 构建人机协同和多 Agent 协作系统

---

## 📖 目录

1. [为什么需要 LangGraph](#1-为什么需要-langgraph)
2. [StateGraph 基础](#2-stategraph-基础)
3. [节点与边](#3-节点与边)
4. [Reducer 策略](#4-reducer-策略)
5. [检查点与记忆](#5-检查点与记忆)
6. [条件路由](#6-条件路由)
7. [人机协同](#7-人机协同)
8. [流式输出](#8-流式输出)
9. [多 Agent 子图](#9-多-agent-子图)
10. [生产级模式](#10-生产级模式)

---

## 1. 为什么需要 LangGraph

### 1.1 Chain 的局限性

LangChain 的 Chain 适合简单的线性流程：

```python
# Chain: 线性流程
prompt -> model -> output
```

但现实中的 Agent 需要：

- **循环**：根据条件重复执行
- **分支**：不同输入走不同路径
- **状态**：跨步骤记住上下文
- **中断**：等待人工确认后继续

### 1.2 LangGraph 的解决方案

LangGraph 基于**状态机**模型，提供：

| 特性 | 描述 | Chain | LangGraph |
|------|------|-------|-----------|
| 循环 | 迭代执行 | ❌ | ✅ |
| 分支 | 条件路由 | ⚠️ | ✅ |
| 状态 | 持久化上下文 | ❌ | ✅ |
| 中断 | 人机协同 | ❌ | ✅ |

### 1.3 概念对比

```python
# Chain 思维（线性）
chain = prompt | model | output_parser

# LangGraph 思维（状态机）
graph = StateGraph(State)
graph.add_node("process", process_node)
graph.add_edge(START, "process")
graph.add_edge("process", END)
```

---

## 2. StateGraph 基础

### 2.1 核心概念

LangGraph 的核心是 **StateGraph**，由以下组件构成：

```
┌─────────────────────────────────────────┐
│                StateGraph               │
├─────────────────────────────────────────┤
│  State: TypedDict - 共享状态            │
│  Nodes: 函数 - 处理逻辑                 │
│  Edges: 连接 - 控制流                   │
│  Graph: 编译后的可执行图                │
└─────────────────────────────────────────┘
```

### 2.2 最小示例

```python
"""示例: 最简单的 LangGraph"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1. 定义状态类型
class AgentState(TypedDict):
    """Agent 的共享状态"""
    messages: list[str]
    next_action: str | None

# 2. 定义节点函数
def should_continue(state: AgentState) -> str:
    """决定是否继续"""
    return END if len(state["messages"]) >= 3 else "process"

def process_node(state: AgentState) -> AgentState:
    """处理节点"""
    new_message = f"处理 {len(state['messages']) + 1}"
    return {
        "messages": state["messages"] + [new_message],
        "next_action": None,
    }

# 3. 构建图
builder = StateGraph(AgentState)

# 添加节点
builder.add_node("process", process_node)

# 添加边
builder.add_edge(START, "process")

# 添加条件边
builder.add_conditional_edges(
    "process",
    should_continue,
    {END: END, "process": "process"}  # 继续或结束
)

# 4. 编译图
graph = builder.compile()

# 5. 执行
result = graph.invoke({"messages": [], "next_action": None})
print(result)
# {'messages': ['处理 1', '处理 2', '处理 3'], 'next_action': None}
```

### 2.3 状态设计原则

```python
# ✅ 好的状态设计
class GoodState(TypedDict):
    """清晰、可组合的状态"""
    messages: list[BaseMessage]  # 对话历史
    context: dict[str, Any]       # 外部上下文
    current_step: str             # 当前步骤
    intermediate_results: dict    # 中间结果

# ❌ 避免的状态设计
class BadState(TypedDict):
    """过于复杂或冗余"""
    all_previous_thoughts: str    # 存储为字符串而非列表
    temp_variables: dict          # 临时变量混入状态
    computed_values: float        # 可以从其他字段计算得出
```

---

## 3. 节点与边

### 3.1 节点类型

#### 普通节点

```python
def simple_node(state: AgentState) -> AgentState:
    """普通处理节点"""
    return {"messages": state["messages"] + ["新消息"]}

builder.add_node("simple", simple_node)
```

#### 带名称的节点

```python
def analyze_node(state: AgentState) -> AgentState:
    """分析节点"""
    return {"analysis": "分析结果"}

def respond_node(state: AgentState) -> AgentState:
    """响应节点"""
    return {"response": "响应内容"}

builder.add_node("analyze", analyze_node)
builder.add_node("respond", respond_node)
```

### 3.2 边的类型

#### 直接边

```python
# 固定流向: START -> process -> END
builder.add_edge(START, "process")
builder.add_edge("process", END)
```

#### 条件边

```python
from typing import Literal

def route_based_on_intent(state: AgentState) -> Literal["analyze", "respond"]:
    """根据意图路由"""
    if "分析" in state.get("query", ""):
        return "analyze"
    return "respond"

builder.add_conditional_edges(
    "router",
    route_based_on_intent,
    {
        "analyze": "analyze_node",
        "respond": "respond_node",
    }
)
```

### 3.3 节点组合模式

```python
"""节点组合: 分析 -> 决策 -> 执行"""

def analyze(state: AgentState) -> AgentState:
    """分析阶段"""
    query = state["query"]
    analysis = f"分析了: {query}"
    return {"analysis": analysis, "stage": "analyzed"}

def decide(state: AgentState) -> AgentState:
    """决策阶段"""
    analysis = state.get("analysis", "")
    decision = f"基于 {analysis} 做决策"
    return {"decision": decision, "stage": "decided"}

def execute(state: AgentState) -> AgentState:
    """执行阶段"""
    decision = state.get("decision", "")
    result = f"执行: {decision}"
    return {"result": result, "stage": "completed"}

# 构建流水线
builder.add_node("analyze", analyze)
builder.add_node("decide", decide)
builder.add_node("execute", execute)

builder.add_edge(START, "analyze")
builder.add_edge("analyze", "decide")
builder.add_edge("decide", "execute")
builder.add_edge("execute", END)
```

---

## 4. Reducer 策略

### 4.1 问题背景

当多个节点返回相同键时，如何合并状态？

```python
# 节点 A 返回
{"messages": ["A 的消息"]}

# 节点 B 返回
{"messages": ["B 的消息"]}

# 合并结果？
```

### 4.2 Reducer 函数

```python
from operator import add
from typing import Annotated

class StateWithReducer(TypedDict):
    """使用 Reducer 的状态"""
    messages: Annotated[list[str], add]  # 追加策略
    counter: Annotated[int, max]          # 最大值策略
    last_update: str                      # 覆盖策略（默认）

def node_a(state: StateWithReducer) -> StateWithReducer:
    return {"messages": ["A 消息"], "counter": 1, "last_update": "A"}

def node_b(state: StateWithReducer) -> StateWithReducer:
    return {"messages": ["B 消息"], "counter": 2, "last_update": "B"}

# 测试合并
# 最终 messages = ["A 消息", "B 消息"]  # 追加
# 最终 counter = 2                        # max
# 最终 last_update = "B"                  # 覆盖
```

### 4.3 内置 Reducer

| Reducer | 行为 | 适用场景 |
|---------|------|----------|
| `operator.add` | 追加到列表 | messages, history |
| `operator.and_` | 集合交集 | tags, categories |
| `operator.or_` | 集合并集 | permissions |
| `max` | 取最大值 | scores, counters |
| `min` | 取最小值 | thresholds |
| 无 | 覆盖 | single-value 字段 |

### 4.4 自定义 Reducer

```python
from functools import reduce

def merge_dict_values(left: dict, right: dict) -> dict:
    """深度合并字典"""
    result = left.copy()
    for key, value in right.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dict_values(result[key], value)
        else:
            result[key] = value
    return result

class StateWithCustomReducer(TypedDict):
    """自定义 Reducer 状态"""
    config: Annotated[dict, merge_dict_values]
    history: Annotated[list[dict], add]

def update_config(state: StateWithCustomReducer) -> StateWithCustomReducer:
    return {
        "config": {"model": "gpt-4", "temperature": 0.7},
        "history": [{"action": "update_config"}]
    }

def extend_config(state: StateWithCustomReducer) -> StateWithCustomReducer:
    return {
        "config": {"timeout": 30, "retries": 3},
        "history": [{"action": "extend_config"}]
    }

# 测试: config 会深度合并，history 会追加
```

---

## 5. 检查点与记忆

### 5.1 为什么需要检查点

```python
# 无检查点: 状态不持久化
graph = builder.compile()

# 每次调用都是新开始
result1 = graph.invoke({"messages": ["Hello"]})
result2 = graph.invoke({"messages": ["Hello"]})
# result1 和 result2 互不影响，无法记住之前的对话
```

### 5.2 MemorySaver

```python
from langgraph.checkpoint.memory import MemorySaver

# 有检查点: 状态持久化
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 第一次调用
thread_id = "user_123"
result1 = graph.invoke(
    {"messages": ["Hello"]},
    config={"configurable": {"thread_id": thread_id}}
)
# State: {messages: ["Hello"]}

# 第二次调用（同一线程，自动恢复状态）
result2 = graph.invoke(
    {"messages": ["Hi again"]},
    config={"configurable": {"thread_id": thread_id}}
)
# State: {messages: ["Hello", "Hi again"]}
```

### 5.3 持久化检查点

```python
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg

# PostgreSQL 检查点（生产环境）
conn = psycopg.connect("postgresql://user:pass@localhost/db")

checkpointer = PostgresSaver(conn)
checkpointer.setup()  # 创建表

graph = builder.compile(checkpointer=checkpointer)

# 使用 thread_id 隔离会话
result = graph.invoke(
    {"query": "分析销售数据"},
    config={
        "configurable": {
            "thread_id": "session_001",
            "checkpoint_ns": "analysis",
        }
    }
)
```

### 5.4 检查点操作

```python
# 获取历史快照
snapshots = list(checkpointer.get_history({"thread_id": "user_123"}))

for snapshot in snapshots:
    print(f"Checkpoint ID: {snapshot.id}")
    print(f"State: {snapshot.channel_values}")
    print(f"Created: {snapshot.created_at}")

# 从特定检查点恢复
graph = builder.compile(checkpointer=checkpointer)
result = graph.invoke(
    None,  # 不传入新状态
    config={
        "configurable": {
            "thread_id": "user_123",
            "checkpoint_id": "checkpoint_abc123",
        }
    }
)
```

---

## 6. 条件路由

### 6.1 基础条件路由

```python
from typing import Literal

def route_intent(state: AgentState) -> Literal["web_search", "db_query", "respond"]:
    """根据意图路由到不同节点"""
    query = state.get("query", "").lower()

    if any(kw in query for kw in ["最新", "新闻", "搜索"]):
        return "web_search"
    elif any(kw in query for kw in ["查询", "用户", "订单"]):
        return "db_query"
    return "respond"

builder.add_conditional_edges(
    "router",
    route_intent,
    {
        "web_search": "search_node",
        "db_query": "query_node",
        "respond": "respond_node",
    }
)
```

### 6.2 多条件组合

```python
def route_complex(state: AgentState) -> Literal["fast", "deep", "error"]:
    """复杂条件路由"""
    query = state.get("query", "")
    priority = state.get("priority", "normal")
    tokens_available = state.get("tokens_available", 0)

    # 错误处理优先
    if "error" in query.lower():
        return "error"

    # 高优先级走深度分析
    if priority == "high":
        return "deep"

    # 低 token 走快速响应
    if tokens_available < 1000:
        return "fast"

    # 默认深度分析
    return "deep"

builder.add_conditional_edges(
    "assess",
    route_complex,
    {
        "error": "error_handler",
        "fast": "quick_response",
        "deep": "deep_analysis",
    }
)
```

### 6.3 条件边的else分支

```python
def router_with_default(state: AgentState) -> str:
    """返回目标节点或特殊标记"""
    query = state.get("query", "")

    if "search" in query:
        return "search"
    elif "db" in query:
        return "database"

    # 没有匹配，返回特殊标记
    return "__end__"

# 使用 default 关键字处理默认分支
builder.add_conditional_edges(
    "router",
    router_with_default,
    {
        "search": "search_node",
        "database": "db_node",
    },
    default=END  # 默认结束
)
```

---

## 7. 人机协同

### 7.1 为什么需要人机协同

```python
# 场景: Agent 需要在执行敏感操作前获得人工确认
# - 转账操作
# - 发送邮件
# - 删除数据
# - 支付确认
```

### 7.2 Interrupt 模式

```python
from langgraph.types import interrupt

def should_execute_action(state: AgentState) -> AgentState:
    """决策节点"""
    action = state.get("pending_action", {})

    if action.get("type") == "sensitive":
        # 中断并等待人工确认
        user_input = interrupt({
            "message": "请确认执行此操作",
            "action": action,
        })
        return {"confirmed": user_input.get("confirmed", False)}

    return {"confirmed": True}

def execute_action(state: AgentState) -> AgentState:
    """执行节点"""
    if not state.get("confirmed"):
        return {"result": "操作已取消"}

    action = state.get("pending_action", {})
    return {"result": f"执行了: {action.get('type')}"}
```

### 7.3 手动恢复执行

```python
# 模拟用户确认
user_confirmation = {
    "confirmed": True,
    "approved_by": "admin@example.com",
}

# 使用 interrupt 的返回值继续执行
result = graph.invoke(
    None,  # 不传入新状态
    config={
        "configurable": {
            "thread_id": "session_123",
        }
    },
    stream_mode="values"
)

# 遍历中间状态
for state in result:
    if "__interrupt__" in state:
        print(f"需要人工确认: {state['__interrupt__']}")
```

### 7.4 工具调用中的人机协同

```python
def transfer_money(state: AgentState) -> AgentState:
    """转账操作"""
    transfer = state.get("pending_transfer", {})

    # 检查金额是否超过阈值
    if transfer.get("amount", 0) > 10000:
        confirmation = interrupt({
            "message": f"转账金额 {transfer['amount']} 超过阈值",
            "action": "bank_transfer",
            "require_approval": True,
        })
        if not confirmation.get("approved"):
            return {"transfer_result": "已拒绝"}

    # 执行转账
    return {"transfer_result": "转账成功"}
```

---

## 8. 流式输出

### 8.1 Token 流式输出

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", streaming=True)

builder = StateGraph(AgentState)
# ... 添加节点和边 ...

graph = builder.compile()

# 流式输出
for chunk in graph.stream(
    {"messages": [{"role": "user", "content": "写一首诗"}]},
    stream_mode="tokens"
):
    if "llm" in chunk:
        print(chunk["llm"], end="", flush=True)
```

### 8.2 自定义流式节点

```python
async def streaming_node(state: AgentState) -> AgentState:
    """流式处理节点"""

    async def generate():
        for i in range(10):
            yield f"chunk_{i}"
            await asyncio.sleep(0.1)

    collected = []
    async for chunk in generate():
        collected.append(chunk)

    return {"chunks": collected}

builder.add_node("streaming", streaming_node)

# 流式模式
for event in graph.stream(
    {"query": "处理"},
    stream_mode="custom"  # 或 "values", "updates", "debug"
):
    print(f"Event: {event}")
```

### 8.3 流式与检查点结合

```python
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 在流式输出过程中保存检查点
config = {"configurable": {"thread_id": "stream_session"}}

events = graph.stream(
    {"query": "长文本处理"},
    config=config,
    stream_mode="values"
)

for idx, state in enumerate(events):
    print(f"Step {idx}: {state.get('step_name')}")
    # 每个状态都被自动保存到检查点
```

---

## 9. 多 Agent 子图

### 9.1 子图概念

```python
# 主图
main_graph = StateGraph(MainState)

# 子图: 研究 Agent
research_graph = StateGraph(ResearchState)
research_graph.add_node("search", search_node)
research_graph.add_node("synthesize", synthesize_node)
research_graph.add_edge(START, "search")
research_graph.add_edge("search", "synthesize")
research_graph.add_edge("synthesize", END)

# 编译子图
research_agent = research_graph.compile()

# 在主图中调用子图
def run_research(state: MainState) -> MainState:
    """运行研究子图"""
    result = research_agent.invoke({"query": state["query"]})
    return {"research_result": result["summary"]}

main_graph.add_node("research", run_research)
```

### 9.2 完整示例: 研究 + 写作 Agent

```python
from typing import TypedDict
from operator import add

# ============== 状态定义 ==============

class ResearchState(TypedDict):
    query: str
    sources: list[str]
    findings: list[str]

class WritingState(TypedDict):
    topic: str
    outline: str | None
    draft: str | None
    revisions: list[str]

class CoordinatorState(TypedDict):
    task: str
    research: Annotated[dict, add]  # 累积研究结果
    writing: dict                   # 写作状态
    final_output: str | None

# ============== 研究 Agent ==============

def search_sources(state: ResearchState) -> ResearchState:
    sources = [f"source_{i}" for i in range(3)]
    return {"sources": sources}

def analyze_findings(state: ResearchState) -> ResearchState:
    findings = [f"finding about {s}" for s in state["sources"]]
    return {"findings": findings}

research_builder = StateGraph(ResearchState)
research_builder.add_node("search", search_sources)
research_builder.add_node("analyze", analyze_findings)
research_builder.add_edge(START, "search")
research_builder.add_edge("search", "analyze")
research_builder.add_edge("analyze", END)
research_agent = research_builder.compile()

# ============== 写作 Agent ==============

def create_outline(state: WritingState) -> WritingState:
    return {"outline": f"Outline for: {state['topic']}"}

def write_draft(state: WritingState) -> WritingState:
    return {"draft": f"Draft based on: {state['outline']}"}

def revise(state: WritingState) -> WritingState:
    return {"revisions": state.get("revisions", []) + ["revision_1"]}

writing_builder = StateGraph(WritingState)
writing_builder.add_node("outline", create_outline)
writing_builder.add_node("draft", write_draft)
writing_builder.add_node("revise", revise)
writing_builder.add_edge(START, "outline")
writing_builder.add_edge("outline", "draft")
writing_builder.add_edge("draft", "revise")
writing_builder.add_edge("revise", END)
writing_agent = writing_builder.compile()

# ============== 协调 Agent ==============

def research_task(state: CoordinatorState) -> CoordinatorState:
    result = research_agent.invoke({"query": state["task"]})
    return {"research": {"findings": result["findings"]}}

def write_task(state: CoordinatorState) -> CoordinatorState:
    result = writing_agent.invoke({"topic": state["task"]})
    return {"writing": result}

def finalize(state: CoordinatorState) -> CoordinatorState:
    return {"final_output": f"Final: {state['task']}"}

coord_builder = StateGraph(CoordinatorState)
coord_builder.add_node("research", research_task)
coord_builder.add_node("write", write_task)
coord_builder.add_node("finalize", finalize)
coord_builder.add_edge(START, "research")
coord_builder.add_edge("research", "write")
coord_builder.add_edge("write", "finalize")
coord_builder.add_edge("finalize", END)

coord_graph = coord_builder.compile()

# 执行
result = coord_graph.invoke({"task": "AI Agent 的发展趋势"})
print(result["final_output"])
```

---

## 10. 生产级模式

### 10.1 错误处理与重试

```python
from langgraph.errors import NodeInterrupt
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def reliable_node(state: AgentState) -> AgentState:
    """带重试的可靠节点"""
    try:
        result = call_external_api(state["query"])
        return {"result": result}
    except RateLimitError:
        raise  # 让 tenacity 重试
    except PermanentError as e:
        return {"error": str(e)}

def error_handler(state: AgentState) -> AgentState:
    """错误处理节点"""
    error = state.get("error", "Unknown error")
    return {"recovery_action": f"通知管理员: {error}"}
```

### 10.2 超时控制

```python
from asyncio import timeout as async_timeout

async def slow_operation(state: AgentState) -> AgentState:
    """带超时的操作"""
    try:
        async with async_timeout(30):  # 30秒超时
            result = await call_llm(state["query"])
            return {"result": result}
    except asyncio.TimeoutError:
        return {"error": "操作超时"}

builder = StateGraph(AgentState)
builder.add_node("process", slow_operation)
```

### 10.3 并行执行

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_node(state: AgentState) -> AgentState:
    """并行执行多个任务"""
    tasks = state.get("tasks", [])

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_task, t) for t in tasks]
        results = [f.result() for f in futures]

    return {"parallel_results": results}
```

### 10.4 动态图更新

```python
def adaptive_graph(state: AgentState) -> AgentGraph:
    """根据状态动态选择图"""
    complexity = state.get("task_complexity", "simple")

    if complexity == "simple":
        return simple_graph
    elif complexity == "medium":
        return medium_graph
    return complex_graph

def execute_adaptive(state: AgentState) -> AgentState:
    """执行自适应图"""
    graph = adaptive_graph(state)
    result = graph.invoke(state)
    return {"adaptive_result": result}
```

---

## 📝 总结

本课程涵盖了 LangGraph 的核心概念和实用模式：

| 概念 | 关键点 |
|------|--------|
| StateGraph | 状态机模型，状态 + 节点 + 边 |
| Reducer | 控制状态合并策略 |
| 检查点 | 多轮对话状态持久化 |
| 条件路由 | 根据状态动态选择路径 |
| 人机协同 | 敏感操作人工确认 |
| 流式输出 | 实时响应用户 |
| 子图 | 多 Agent 协作 |

---

## 🔗 延伸学习

- [L53 LangChain 基础](../L56-langchain/) - LCEL 基础
- [L55 Agent 基础](../L54-agent-basics/) - ReAct 模式
- [L58 LangGraph 进阶](../L62-langgraph-server/) - 高级模式
- [L61 多 Agent 编排](../L61-multi-agent/) - 多 Agent 协作

---

*课程版本: v1.0 | 最后更新: 2026-07-20*

## 🔗 下一步

完成本课后继续学习：

- [L59: Agent 记忆系统](../L59-agent-memory/README.md)

> 📖 **学习路径提示**：L59 将学习 Agent 的记忆管理和上下文维护。
