"""
练习题 2 参考解答: 条件路由逻辑
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
import re


class QueryState(TypedDict):
    """查询状态"""

    query: str
    route: str | None
    result: str | None


def handle_weather(state: QueryState) -> QueryState:
    """处理天气查询"""
    return {
        "result": "今天天气晴朗，温度 25°C",
        "route": "weather",
    }


def handle_news(state: QueryState) -> QueryState:
    """处理新闻查询"""
    return {
        "result": "最新新闻: AI 技术持续发展",
        "route": "news",
    }


def handle_math(state: QueryState) -> QueryState:
    """处理数学计算"""
    query = state["query"]
    # 匹配数学表达式
    match = re.search(r"([\d]+)\s*([+\-*/])\s*([\d]+)", query)
    if match:
        a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        else:
            result = a / b
        return {"result": f"计算结果: {result}", "route": "math"}
    return {"result": "无法解析数学表达式", "route": "math"}


def handle_general(state: QueryState) -> QueryState:
    """处理通用查询"""
    return {
        "result": f"你好！我收到你的消息: {state['query']}",
        "route": "general",
    }


def classify_query(state: QueryState) -> Literal["weather", "news", "math", "general"]:
    """分类查询并返回路由目标"""
    query = state["query"].lower()

    if "天气" in query or "温度" in query:
        return "weather"
    elif "新闻" in query or "最近" in query:
        return "news"
    elif re.search(r"[\d]+[\s]*[+\-*/][\s]*[\d]+", query):
        return "math"
    return "general"


def main() -> None:
    """主函数"""
    builder = StateGraph(QueryState)

    # 添加节点
    builder.add_node("classify", lambda s: s)  # 分类节点（透传）
    builder.add_node("weather", handle_weather)
    builder.add_node("news", handle_news)
    builder.add_node("math", handle_math)
    builder.add_node("general", handle_general)

    # 添加边
    builder.add_edge(START, "classify")

    # 添加条件边
    builder.add_conditional_edges(
        "classify",
        classify_query,
        {
            "weather": "weather",
            "news": "news",
            "math": "math",
            "general": "general",
        },
    )

    # 所有节点结束
    for node in ["weather", "news", "math", "general"]:
        builder.add_edge(node, END)

    graph = builder.compile()

    # 测试用例
    test_cases = [
        ("今天天气怎么样", "weather"),
        ("最近有什么新闻", "news"),
        ("计算 2+2", "math"),
        ("你好", "general"),
    ]

    print("=" * 60)
    print("条件路由测试结果:")
    print("=" * 60)

    for query, expected_route in test_cases:
        result = graph.invoke(
            {
                "query": query,
                "route": None,
                "result": None,
            }
        )
        print(f"\n输入: {query}")
        print(f"路由: {result['route']}")
        print(f"结果: {result['result']}")
        assert result["route"] == expected_route, (
            f"路由应该 {expected_route}, 实际 {result['route']}"
        )

    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    main()
