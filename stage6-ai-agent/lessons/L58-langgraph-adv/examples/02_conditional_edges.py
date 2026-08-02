"""
示例 2: 条件边与路由

展示如何使用条件边根据状态动态选择下一个节点。
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal


class RouterState(TypedDict):
    """路由状态"""

    query: str
    intent: str | None
    result: str | None


def analyze_intent(state: RouterState) -> RouterState:
    """
    分析用户意图

    Args:
        state: 当前状态

    Returns:
        更新后的状态
    """
    query = state["query"].lower()

    if any(kw in query for kw in ["搜索", "查找", "search"]):
        intent = "search"
    elif any(kw in query for kw in ["计算", "数学", "calculate"]):
        intent = "calculate"
    elif any(kw in query for kw in ["翻译", "translate"]):
        intent = "translate"
    else:
        intent = "general"

    return {"intent": intent}


def search_node(state: RouterState) -> RouterState:
    """搜索节点"""
    return {"result": f"搜索结果: {state['query']}"}


def calculate_node(state: RouterState) -> RouterState:
    """计算节点"""
    return {"result": f"计算结果: {state['query']}"}


def translate_node(state: RouterState) -> RouterState:
    """翻译节点"""
    return {"result": f"翻译结果: {state['query']}"}


def general_node(state: RouterState) -> RouterState:
    """通用响应节点"""
    return {"result": f"通用响应: {state['query']}"}


def route_intent(state: RouterState) -> Literal["search", "calculate", "translate", "general"]:
    """
    根据意图路由到对应节点

    Args:
        state: 当前状态

    Returns:
        目标节点名称
    """
    return state.get("intent", "general")


def main() -> None:
    """主函数"""
    # 构建图
    builder = StateGraph(RouterState)

    # 添加节点
    builder.add_node("analyze", analyze_intent)
    builder.add_node("search", search_node)
    builder.add_node("calculate", calculate_node)
    builder.add_node("translate", translate_node)
    builder.add_node("general", general_node)

    # 添加边
    builder.add_edge(START, "analyze")

    # 添加条件边
    builder.add_conditional_edges(
        "analyze",
        route_intent,
        {
            "search": "search",
            "calculate": "calculate",
            "translate": "translate",
            "general": "general",
        },
    )

    # 所有处理节点都指向 END
    for node in ["search", "calculate", "translate", "general"]:
        builder.add_edge(node, END)

    # 编译并执行
    graph = builder.compile()

    # 测试不同意图
    test_queries = [
        "搜索 Python 教程",
        "计算 2+2",
        "翻译 Hello World",
        "今天天气怎么样",
    ]

    print("=" * 60)
    print("条件路由测试")
    print("=" * 60)

    for query in test_queries:
        result = graph.invoke({"query": query, "intent": None, "result": None})
        print(f"\n输入: {query}")
        print(f"意图: {result['intent']}")
        print(f"结果: {result['result']}")


if __name__ == "__main__":
    main()
