"""
练习题 2: 条件路由逻辑

请根据用户输入的查询类型，实现智能路由功能：

1. 定义 QueryState:
   - query: str (用户查询)
   - route: str | None (路由目标)
   - result: str | None (处理结果)

2. 实现以下处理器节点:
   - handle_weather: 返回天气预报
   - handle_news: 返回新闻摘要
   - handle_math: 计算数学表达式
   - handle_general: 返回通用回复

3. 实现路由函数 classify_query，根据查询内容返回路由目标:
   - 包含"天气"或"温度": route to handle_weather
   - 包含"新闻"或"最近": route to handle_news
   - 包含数学表达式(如 "1+1", "2*3"): route to handle_math
   - 其他: route to handle_general

4. 测试用例:
   - "今天天气怎么样" -> handle_weather
   - "最近有什么新闻" -> handle_news
   - "计算 2+2*3" -> handle_math
   - "你好" -> handle_general
"""

from typing import TypedDict, Literal


class QueryState(TypedDict):
    """查询状态"""

    query: str
    route: str | None
    result: str | None


def handle_weather(state: QueryState) -> QueryState:
    """处理天气查询"""
    # TODO: 返回天气信息
    pass


def handle_news(state: QueryState) -> QueryState:
    """处理新闻查询"""
    # TODO: 返回新闻摘要
    pass


def handle_math(state: QueryState) -> QueryState:
    """处理数学计算"""
    # TODO: 解析并计算数学表达式
    # 提示: 使用 re 模块匹配数学表达式
    pass


def handle_general(state: QueryState) -> QueryState:
    """处理通用查询"""
    # TODO: 返回通用回复
    pass


def classify_query(state: QueryState) -> Literal["weather", "news", "math", "general"]:
    """
    分类查询并返回路由目标

    Args:
        state: 当前状态

    Returns:
        路由目标: "weather", "news", "math", 或 "general"
    """
    # TODO: 实现分类逻辑
    pass


def main() -> None:
    """主函数"""
    # TODO: 构建图
    pass

    # TODO: 编译并测试
    pass


if __name__ == "__main__":
    main()
