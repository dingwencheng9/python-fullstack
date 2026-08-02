"""
L55 示例: 条件路由与工具调用循环

学习目标:
- add_conditional_edges 的路由函数签名
- 工具调用循环的实现（agent → tools → agent）
- 多路由决策的 Supervisor 模式
"""

from __future__ import annotations

from typing import Literal


# --- 模拟 Agent / Tool 节点 ---
class SimState(dict):
    """简化状态，模拟 messages 列表。"""

    messages: list[str]
    tool_calls: list[str]


def mock_agent(state: SimState) -> SimState:
    """模拟 LLM Agent：根据 messages 内容决定是否调用工具。"""
    last = state["messages"][-1] if state["messages"] else ""
    if "天气" in last:
        return {
            "messages": state["messages"] + ["agent: 需要调用 weather 工具"],
            "tool_calls": ["weather"],
        }
    if "搜索" in last:
        return {
            "messages": state["messages"] + ["agent: 需要调用 search 工具"],
            "tool_calls": ["search"],
        }
    return {"messages": state["messages"] + ["agent: 直接回答"], "tool_calls": []}


def mock_tool(state: SimState) -> SimState:
    """模拟工具执行节点。"""
    tool = state["tool_calls"][0] if state["tool_calls"] else "none"
    return {
        "messages": state["messages"] + [f"[tool:{tool}] 执行完成"],
        "tool_calls": [],
    }


# --- 路由函数 ---
def route_by_tool_calls(state: SimState) -> Literal["tools", "end"]:
    """根据 tool_calls 是否非空路由到 tools 节点或结束。"""
    return "tools" if state.get("tool_calls") else "end"


def supervisor_route(state: SimState) -> Literal["research", "code", "end"]:
    """Supervisor 模式：根据内容关键词路由到不同专家节点。"""
    last = state["messages"][-1] if state["messages"] else ""
    if "研究" in last or "搜索" in last:
        return "research"
    if "代码" in last or "实现" in last:
        return "code"
    return "end"


# --- 模拟执行 ---
def simulate_tool_loop(user_input: str) -> list[str]:
    """模拟 agent → tools → agent 循环（最多 3 轮）。"""
    state: SimState = {"messages": [f"user: {user_input}"], "tool_calls": []}
    history = [dict(state)]

    for _ in range(3):
        state = mock_agent(state)
        history.append(dict(state))
        if not state["tool_calls"]:
            break
        state = mock_tool(state)
        history.append(dict(state))

    return [m for s in history for m in s["messages"]]


# --- 演示运行 ---
if __name__ == "__main__":
    print("=== 1. 工具调用循环 ===")
    for msg in simulate_tool_loop("北京今天天气如何"):
        print(f"  {msg}")

    print("\n=== 2. 直接回答（无需工具） ===")
    for msg in simulate_tool_loop("你好"):
        print(f"  {msg}")

    print("\n=== 3. Supervisor 路由 ===")
    for intent, query in [
        ("research", "请帮我搜索 Python 最新动态"),
        ("code", "帮我实现一个快速排序"),
        ("other", "你好"),
    ]:
        result = supervisor_route({"messages": [f"user: {query}"], "tool_calls": []})
        print(f"  '{intent}' 输入 → 路由到 '{result}'")
