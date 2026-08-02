"""
L55 LangGraph 核心: Router Agent 状态机

企业级基础编排示例:
- PEP 695 新泛型语法（type Alias）
- TypedDict 定义 Agent State
- StateGraph + Conditional Edges 条件路由
- START / END 节点 + 条件边

技术版本: langgraph >=1.2.6, Python 3.13+
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict
from operator import add

from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph


# =============================================================================
# 1. 状态定义（TypedDict + PEP 695 Annotated 合并策略）
# =============================================================================


class RouterState(TypedDict, total=False):
    """Agent 执行状态。

    - messages: 追加模式，多节点写入不覆盖，累积追加。
    - intent:    覆盖模式，每次 LLM 判断后替换。
    - iteration: 覆盖模式，迭代计数器。
    """

    messages: Annotated[list[str], add]
    intent: str
    iteration: int


# =============================================================================
# 2. 节点函数（Node Functions）
# =============================================================================


def triage_node(state: RouterState) -> RouterState:
    """分类节点: 根据用户消息判断意图，返回 intent 字段。

    简化版意图识别（生产中替换为真实 LLM 调用）。
    每次执行 iteration +1，与 should_route / should_retry 配合控制循环上限。
    """
    last_msg = state["messages"][-1] if state["messages"] else ""

    if any(kw in last_msg for kw in ("搜索", "查询", "什么", "最新")):
        detected = "search"
    elif any(kw in last_msg for kw in ("代码", "实现", "写", "帮我")):
        detected = "code"
    elif any(kw in last_msg for kw in ("天气", "温度", "下雨")):
        detected = "weather"
    elif any(kw in last_msg for kw in ("你好", "嗨", "Hi")):
        detected = "greeting"
    else:
        detected = "general"

    return {
        "intent": detected,
        "messages": [f"[triage] 识别意图: {detected}，迭代 #{state['iteration'] + 1}"],
        "iteration": state["iteration"] + 1,
    }


def search_node(state: RouterState) -> RouterState:
    """搜索节点: 返回搜索结果（模拟）。"""
    return {
        "messages": [f"[search] 正在搜索: {state['messages'][-1]}"],
    }


def code_node(state: RouterState) -> RouterState:
    """代码节点: 返回代码建议（模拟）。"""
    return {
        "messages": ["[code] 为您生成代码方案..."],
    }


def weather_node(state: RouterState) -> RouterState:
    """天气节点: 返回天气信息（模拟）。"""
    return {
        "messages": ["[weather] 查询天气信息中..."],
    }


def greeting_node(state: RouterState) -> RouterState:
    """问候节点: 简单回复。"""
    return {
        "messages": ["[greeting] 你好！有什么可以帮助您的？"],
    }


def general_node(state: RouterState) -> RouterState:
    """通用节点: 默认回复。"""
    return {
        "messages": ["[general] 收到，我理解您的需求。"],
    }


def should_route(
    state: RouterState,
) -> Literal["search", "code", "weather", "greeting", "general", "__end__"]:
    """条件边路由函数: 根据 triage 后的 intent 路由到对应节点或结束。

    LangGraph 0.2.x 条件边签名:
        path 函数返回 hashable 类型的节点名称字符串（或 END = "__end__"）。

    当 intent 为 search/code/weather 时，进入对应节点；
    greeting/general 为简单回复，无需继续路由，直接结束；
    iteration >= 3 时强制结束，防止无限循环。
    """
    if state["iteration"] >= 3:
        return END  # type: ignore[return-value]

    intent_map: dict[str, Literal["search", "code", "weather"]] = {
        "search": "search",
        "code": "code",
        "weather": "weather",
    }
    if state["intent"] in intent_map:
        return intent_map[state["intent"]]
    return END  # type: ignore[return-value]  # greeting / general / unknown → 直接结束


def should_retry(state: RouterState) -> Literal["triage", "__end__"]:
    """第二轮条件边: search/code/weather 执行完后，回到 triage 做第二轮判断。

    用于演示多轮对话循环。
    """
    if state["iteration"] >= 3:
        return END  # type: ignore[return-value]
    return "triage"


# =============================================================================
# 3. 图构建（StateGraph 0.2.x API）
# =============================================================================


def build_router_graph() -> StateGraph[RouterState]:
    """构建意图路由状态机图。

    图结构::

        START → triage → ┬→ search  → retry → triage → …
                         ├→ code    → retry
                         ├→ weather → retry
                         ├→ greeting → END
                         └→ general → END

    其中 retry 条件边由 should_retry 控制，达到迭代上限后流向 END。
    """
    graph = StateGraph(RouterState)

    # 注册所有节点
    graph.add_node("triage", triage_node)
    graph.add_node("search", search_node)
    graph.add_node("code", code_node)
    graph.add_node("weather", weather_node)
    graph.add_node("greeting", greeting_node)
    graph.add_node("general", general_node)

    # 入口点: START → triage
    graph.set_entry_point("triage")

    # 条件边: triage → {search, code, weather, END}
    # 路由函数返回 END 时自动流向 LangGraph 内置 END 节点
    graph.add_conditional_edges(
        source="triage",
        path=should_route,
        path_map={
            "search": "search",
            "code": "code",
            "weather": "weather",
            "__end__": END,  # 路由返回 END 时流向内置终止节点
        },
    )

    # search / code / weather 执行完后，通过条件边回到 triage 或结束
    for node_name in ("search", "code", "weather"):
        graph.add_conditional_edges(
            source=node_name,
            path=should_retry,
            path_map={
                "triage": "triage",
                "__end__": END,  # 路由返回 END 时流向内置终止节点
            },
        )

    # greeting 和 general 为叶子节点，直接连接到 END
    graph.add_edge("greeting", END)
    graph.add_edge("general", END)

    return graph


def compile_router() -> CompiledRouterGraph:
    """编译并返回可执行的 Router Agent。"""
    return build_router_graph().compile()


# 类型别名（PEP 695）: 编译后的图类型
type CompiledRouterGraph = CompiledStateGraph


# =============================================================================
# 4. 执行入口
# =============================================================================

if __name__ == "__main__":
    app = compile_router()

    test_queries = [
        "请帮我搜索 Python 3.13 最新动态",
        "帮我实现一个快速排序",
        "北京今天天气如何",
        "你好",
        "随便聊聊",
    ]

    print("=" * 60)
    print("Router Agent — 意图路由演示")
    print("=" * 60)

    for query in test_queries:
        print(f"\n[输入] {query}")
        result = app.invoke(
            {
                "messages": [f"user: {query}"],
                "intent": "unknown",
                "iteration": 0,
            }
        )
        print(f"[意图] {result['intent']}")
        print(f"[迭代] {result['iteration']}")
        print("[消息轨迹]")
        for msg in result["messages"]:
            print(f"  • {msg}")
        print("-" * 60)
