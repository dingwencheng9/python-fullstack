"""L49示例: 使用 mock 工具演示 ReAct 决策循环。"""

from __future__ import annotations

import ast
import operator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def search_tool(query: str) -> str:
    """模拟搜索工具。"""
    return f"搜索结果: {query} -> Python 3.13 支持更现代的类型语法"


def evaluate_expression(expression: str) -> float:
    """只计算四则运算表达式。"""
    node = ast.parse(expression, mode="eval").body
    return evaluate_node(node)


def evaluate_node(node: ast.AST) -> float:
    """递归计算受支持的 AST 节点。"""
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](evaluate_node(node.left), evaluate_node(node.right))
    raise ValueError("仅支持数字和四则运算")


def calculator_tool(expression: str) -> str:
    """模拟计算工具。"""
    try:
        return str(evaluate_expression(expression))
    except (SyntaxError, ValueError, ZeroDivisionError):
        return "计算错误"


def react_agent(query: str, tools: dict[str, Callable[[str], str]]) -> list[str]:
    """返回 ReAct 轨迹，便于观察 Agent 如何选择工具。"""
    trace = [f"Question: {query}"]
    if "搜索" in query:
        trace.append("Thought: 需要查询资料")
        trace.append("Action: search")
        trace.append(f"Observation: {tools['search'](query)}")
    elif "计算" in query:
        expression = query.replace("计算", "").strip()
        trace.append("Thought: 需要执行数学计算")
        trace.append("Action: calculator")
        trace.append(f"Observation: {tools['calculator'](expression)}")
    else:
        trace.append("Thought: 不需要工具")
    trace.append("Final Answer: 基于观察给出最终回答")
    return trace


if __name__ == "__main__":
    registry = {"search": search_tool, "calculator": calculator_tool}
    for step in react_agent("搜索Python 3.13新特性", registry):
        print(step)
