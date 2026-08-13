"""L54 LangGraph 测试套件"""

import pytest

# 模块级别跳过
pytest.importorskip("langgraph", reason="langgraph 未安装")

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from operator import add


class GraphState(TypedDict):
    """测试用状态"""

    value: int
    history: list[str]


def simple_node(state: GraphState) -> GraphState:
    """简单处理节点"""
    return {
        "value": state["value"] + 1,
        "history": state["history"] + [f"step_{state['value'] + 1}"],
    }


class TestStateGraphBasics:
    """StateGraph 基础测试"""

    def test_simple_graph(self) -> None:
        """测试最简单的图"""
        builder = StateGraph(GraphState)
        builder.add_node("process", simple_node)
        builder.add_edge(START, "process")
        builder.add_edge("process", END)

        graph = builder.compile()

        result = graph.invoke({"value": 0, "history": []})

        assert result["value"] == 1
        assert len(result["history"]) == 1

    def test_loop_graph(self) -> None:
        """测试循环图"""
        builder = StateGraph(GraphState)

        def increment(state: GraphState) -> GraphState:
            return {
                "value": state["value"] + 1,
                "history": state["history"] + ["inc"],
            }

        def should_continue(state: GraphState) -> str:
            return "increment" if state["value"] < 3 else END

        builder.add_node("increment", increment)
        builder.add_edge(START, "increment")
        builder.add_conditional_edges(
            "increment", should_continue, {"increment": "increment", END: END}
        )

        graph = builder.compile()
        result = graph.invoke({"value": 0, "history": []})

        assert result["value"] == 3
        assert len(result["history"]) == 3


class TestConditionalEdges:
    """条件边测试"""

    def test_conditional_routing(self) -> None:
        """测试条件路由"""
        from typing import Literal

        class RouterState(TypedDict):
            query: str
            result: str | None

        def analyze(state: RouterState) -> RouterState:
            return {"result": f"分析: {state['query']}"}

        def route(state: RouterState) -> Literal["a", "b"]:
            return "a" if "a" in state["query"] else "b"

        builder = StateGraph(RouterState)
        builder.add_node("analyze", analyze)
        builder.add_edge(START, "analyze")
        builder.add_conditional_edges("analyze", route, {"a": END, "b": END})

        graph = builder.compile()

        result1 = graph.invoke({"query": "test_a", "result": None})
        assert result1["result"] == "分析: test_a"

        result2 = graph.invoke({"query": "test_b", "result": None})
        assert result2["result"] == "分析: test_b"


class TestReducer:
    """Reducer 测试"""

    def test_list_append_reducer(self) -> None:
        """测试列表追加 Reducer"""

        class ListState(TypedDict):
            items: Annotated[list[str], add]

        builder = StateGraph(ListState)

        def add_item(state: ListState) -> ListState:
            return {"items": [f"item_{len(state['items'])}"]}

        builder.add_node("add", add_item)
        builder.add_edge(START, "add")
        builder.add_edge("add", END)

        graph = builder.compile()

        # 执行多次（模拟并行节点返回）
        result = graph.invoke({"items": ["initial"]})

        assert "initial" in result["items"]
        assert len(result["items"]) >= 1


class TestCheckpointer:
    """检查点测试"""

    def test_memory_checkpointer(self) -> None:
        """测试内存检查点"""
        from langgraph.checkpoint.memory import MemorySaver

        class ChatState(TypedDict):
            messages: Annotated[list[str], add]

        checkpointer = MemorySaver()

        builder = StateGraph(ChatState)

        def chat(state: ChatState) -> ChatState:
            return {"messages": ["response"]}

        builder.add_node("chat", chat)
        builder.add_edge(START, "chat")
        builder.add_edge("chat", END)

        graph = builder.compile(checkpointer=checkpointer)

        # 第一轮（触发 checkpointer 保存）
        _result1 = graph.invoke(
            {"messages": ["hi"]}, config={"configurable": {"thread_id": "test"}}
        )

        # 第二轮
        result2 = graph.invoke(
            {"messages": ["hi"]},  # 新消息
            config={"configurable": {"thread_id": "test"}},
        )

        # 验证消息累积
        assert len(result2["messages"]) == 4  # hi, response, hi, response


class TestSubgraph:
    """子图测试"""

    def test_nested_subgraph(self) -> None:
        """测试嵌套子图"""

        class SubState(TypedDict):
            value: int

        class MainState(TypedDict):
            sub_result: int

        # 构建子图
        sub_builder = StateGraph(SubState)

        def sub_process(state: SubState) -> SubState:
            return {"value": state["value"] * 2}

        sub_builder.add_node("process", sub_process)
        sub_builder.add_edge(START, "process")
        sub_builder.add_edge("process", END)
        sub_graph = sub_builder.compile()

        # 主图
        builder = StateGraph(MainState)

        def main_process(state: MainState) -> MainState:
            sub_result = sub_graph.invoke({"value": state["sub_result"]})
            return {"sub_result": sub_result["value"]}

        builder.add_node("process", main_process)
        builder.add_edge(START, "process")
        builder.add_edge("process", END)

        graph = builder.compile()
        result = graph.invoke({"sub_result": 5})

        assert result["sub_result"] == 10
