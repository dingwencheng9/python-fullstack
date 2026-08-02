"""

from __future__ import annotations

L49练习: Agent工具调用

任务: 实现一个简单的Agent工具系统
"""

from collections.abc import Callable


def create_tool_registry() -> dict[str, Callable]:
    """
    创建工具注册表

    要求:
    1. 实现search工具
    2. 实现calculator工具
    3. 返回工具字典
    """
    # ========================================
    # 👉 TODO: 实现工具注册
    # ========================================

    # 步骤 1: 定义 search 工具
    # 功能: 模拟搜索功能，返回查询结果
    #
    # 示例:
    # def search(query: str) -> str:
    #     """搜索工具"""
    #     return f"搜索结果: {query} 的相关信息..."

    # 步骤 2: 定义 calculator 工具
    # ⚠️ 安全提示: 禁止使用 eval()！请参考 solutions/safe_calculator.py 中的
    # 基于 AST NodeVisitor 的安全实现，仅允许白名单算术运算符。
    #
    # 示例（简化版，生产环境请使用 safe_calculator.py）:
    # def calculator(expression: str) -> str:
    #     """计算器工具（安全版本）"""
    #     try:
    #         # 参考 solutions/safe_calculator.py 实现
    #         # 使用 AST 白名单解析，拒绝函数调用、导入等危险操作
    #         result = safe_calculate(expression)
    #         return f"计算结果: {result}"
    #     except Exception as e:
    #         return "计算错误"  # 不泄露异常细节

    # 步骤 3: 创建工具字典
    # 将工具函数注册到字典中
    #
    # 示例:
    # tools = {
    #     "search": search,
    #     "calculator": calculator
    # }
    # return tools

    # 💡 提示:
    # - 工具函数应该接受字符串参数
    # - 工具函数应该返回字符串结果
    # - 可以添加更多工具（如 weather, translate 等）

    # 👉 在下方实现你的代码
    raise NotImplementedError("请实现 create_tool_registry 函数")


def simple_agent(query: str, tools: dict[str, Callable]) -> str:
    """
    简单Agent实现

    要求:
    1. 根据query选择合适的工具
    2. 调用工具并返回结果
    """
    # ========================================
    # 👉 TODO: 实现 Agent 逻辑
    # ========================================

    # 步骤 1: 分析用户查询
    # 根据关键词判断应该使用哪个工具
    #
    # 示例逻辑:
    # - 如果 query 包含 "搜索", "查找", "search" → 使用 search 工具
    # - 如果 query 包含 "计算", "算", "=" → 使用 calculator 工具
    # - 其他情况 → 返回无法处理的提示

    # 步骤 2: 提取工具参数
    # 从 query 中提取需要传递给工具的参数
    #
    # 示例:
    # query = "搜索 Python 教程"
    # tool_input = "Python 教程"  # 去掉 "搜索" 关键词
    #
    # query = "计算 2 + 3"
    # tool_input = "2 + 3"  # 去掉 "计算" 关键词

    # 步骤 3: 调用工具
    # 根据选择的工具名称，从 tools 字典获取函数并调用
    #
    # 示例:
    # if "搜索" in query or "search" in query.lower():
    #     tool_name = "search"
    #     tool_input = query.replace("搜索", "").strip()
    #     tool_function = tools[tool_name]
    #     result = tool_function(tool_input)
    #     return result

    # 步骤 4: 返回结果
    # 如果没有匹配的工具，返回友好的提示
    #
    # 示例:
    # return "抱歉，我无法处理这个请求。支持的操作: 搜索、计算"

    # 💡 提示:
    # - 使用 if-elif-else 判断 query 包含哪些关键词
    # - 使用 str.replace() 或 split() 提取参数
    # - 使用 tools[tool_name](input) 调用工具
    # - 考虑大小写不敏感: query.lower()

    # 💡 完整示例:
    # query_lower = query.lower()
    #
    # if "搜索" in query or "search" in query_lower:
    #     tool_input = query.replace("搜索", "").strip()
    #     return tools["search"](tool_input)
    #
    # elif "计算" in query or "=" in query:
    #     tool_input = query.replace("计算", "").strip()
    #     return tools["calculator"](tool_input)
    #
    # else:
    #     return "无法理解请求。支持: 搜索、计算"

    # 👉 在下方实现你的代码
    raise NotImplementedError("请实现 simple_agent 函数")
