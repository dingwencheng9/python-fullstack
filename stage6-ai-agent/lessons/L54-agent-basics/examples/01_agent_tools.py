"""

from __future__ import annotations

L49示例: Agent基础与工具

学习目标:
- Agent概念
- Tool定义
- ReAct模式
"""

import ast
import operator
from typing import Annotated

from langchain.tools import tool

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def evaluate_expression(expression: str) -> float:
    """只计算四则运算表达式"""
    node = ast.parse(expression, mode="eval").body
    return evaluate_node(node)


def evaluate_node(node: ast.AST) -> float:
    """递归计算受支持的 AST 节点"""
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](evaluate_node(node.left), evaluate_node(node.right))
    raise ValueError("仅支持数字和四则运算")


# 1. Tool定义
print("=== 1. Tool定义 ===")


@tool
def search(query: Annotated[str, "搜索查询"]) -> str:
    """搜索工具: 根据查询返回结果"""
    # 模拟搜索
    return f"搜索 '{query}' 的结果: [示例结果1, 示例结果2, 示例结果3]"


@tool
def calculator(expression: Annotated[str, "数学表达式"]) -> float | str:
    """计算器: 计算数学表达式"""
    try:
        return evaluate_expression(expression)
    except (SyntaxError, ValueError, ZeroDivisionError):
        return "计算错误"


print(f"✅ 已定义工具: {search.name}, {calculator.name}")

# 2. Agent基础结构
print("\n=== 2. Agent结构 ===")

tools = [search, calculator]

print("Agent组件:")
print("  1. LLM (大语言模型)")
print("  2. Tools (工具集)")
print("  3. Prompt (提示模板)")
print("  4. Memory (可选)")

# 3. ReAct模式
print("\n=== 3. ReAct模式 ===")

react_example = """
Thought: 我需要搜索Python的信息
Action: search
Action Input: "Python programming"
Observation: [搜索结果]
Thought: 现在我可以回答了
Final Answer: Python是一种高级编程语言...
"""

print("ReAct流程:")
print(react_example)

# 4. 简单Agent实现
print("\n=== 4. Agent使用示例 ===")


def simple_agent(query: str, available_tools: list) -> str:
    """简单Agent实现"""
    print(f"Query: {query}")
    tool_names = {item.name for item in available_tools}

    # 判断需要使用哪个工具
    if "搜索" in query or "查找" in query:
        if "search" not in tool_names:
            return "缺少搜索工具"
        tool = search
        result = tool.invoke(query)
    elif "计算" in query or "+" in query or "-" in query:
        if "calculator" not in tool_names:
            return "缺少计算器工具"
        tool = calculator
        # 提取表达式
        import re

        expr = re.search(r"[\d+\-*/()]+", query)
        result = tool.invoke(expr.group()) if expr else "无法提取计算表达式"
    else:
        result = "无需使用工具，直接回答"

    return str(result)


# 测试
result1 = simple_agent("帮我搜索Python教程", tools)
print(f"结果1: {result1}")

result2 = simple_agent("计算 100 + 200", tools)
print(f"结果2: {result2}")

print("\n✅ Agent基础示例完成")
