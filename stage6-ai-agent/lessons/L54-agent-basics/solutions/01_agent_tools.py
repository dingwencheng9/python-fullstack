"""L54 参考答案: Agent 工具与安全计算器

包含：
1. _safe_eval: 用 AST 白名单替代 eval()，防止 RCE 攻击
2. search_tool / calculator_tool: Agent 可调用的安全工具
3. simple_agent: 基于关键字路由的简单 Agent 实现

安全说明：
    本文件使用纯 AST 白名单求值替代 eval()，通过类型检查和操作符白名单
    确保只能执行简单的数学表达式，不存在任意代码执行风险。
"""

from __future__ import annotations

import ast
import operator
import re
from collections.abc import Callable
from typing import Any

# ------------------------------------------------------------------
# 安全计算器：用 AST 白名单替换 eval，避免任意代码执行风险
# ------------------------------------------------------------------
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _safe_eval(expr: str) -> int | float:
    """用 AST 白名单安全求值算术表达式（支持 + - * / ** // % 和数字）。

    返回结果保留原始数值类型：整数 + - * // % 仍是 int，``/`` 与浮点字面量产生 float。

    Raises:
        ValueError / ZeroDivisionError: 非法表达式或除零时抛出（被调用方捕获）。
    """
    tree = ast.parse(expr, mode="eval")
    if not isinstance(tree.body, ast.expr):
        raise ValueError("仅支持算术表达式")

    def _eval(node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -_eval(node.operand)
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_func = _ALLOWED_OPS.get(type(node.op))
            if op_func is None:
                raise ValueError(f"不支持的操作符: {type(node.op).__name__}")
            return op_func(left, right)
        raise ValueError(f"不支持的语法节点: {type(node).__name__}")

    return _eval(tree.body)


def search_tool(query: str) -> str:
    """搜索工具"""
    return f"搜索结果: {query}"


def calculator_tool(expression: str) -> str:
    """计算器工具（AST 白名单，安全）。

    - 合法整数运算返回 ``"3"``、浮点运算返回 ``"3.0"``。
    - 非法表达式统一返回 ``"计算错误"``，避免泄露内部异常细节。
    """
    try:
        result = _safe_eval(expression)
    except (ValueError, ZeroDivisionError, SyntaxError):
        return "计算错误"
    return str(result)


def create_tool_registry() -> dict[str, Callable[..., Any]]:
    """创建工具注册表"""
    return {"search": search_tool, "calculator": calculator_tool}


# ------------------------------------------------------------------
# 简单 Agent：基于关键字路由到对应工具
# ------------------------------------------------------------------
_SEARCH_PREFIXES = ("搜索", "查找")
_CALCULATOR_PREFIX = "计算"


def simple_agent(query: str, tools: dict[str, Callable[..., Any]]) -> str:
    """根据 query 关键字路由到对应工具。

    - 以 ``搜索`` / ``查找`` 开头 → 调用 ``tools["search"]``，把整个 query 作为参数
    - 以 ``计算`` 开头 → 提取后续算术表达式调用 ``tools["calculator"]``
    - 其他（含空字符串）→ 返回 ``"无法处理该查询"``

    工具异常不静默吞掉，向上抛给调用方。
    """
    if not query:
        return "无法处理该查询"

    if query.startswith(_SEARCH_PREFIXES):
        return tools["search"](query)

    if query.startswith(_CALCULATOR_PREFIX):
        expression = query[len(_CALCULATOR_PREFIX) :].strip()
        # 容忍练习中可能出现的全角字符，例如"计算 1 + 2"
        expression = re.sub(r"\s+", "", expression)
        return tools["calculator"](expression)

    return "无法处理该查询"
