"""

from __future__ import annotations

安全计算器模块 - 基于 AST NodeVisitor 的白名单数学表达式解析器

重构说明:
- 移除所有 eval() 调用，消除 RCE 风险
- 使用 ast.NodeVisitor 进行规范的 AST 遍历
- 仅允许: +, -, *, /, **, //, % 和数字字面量
- 任何非法节点（函数调用、导入、属性访问等）触发 SecurityValidationError

作者: Claude Code (Opus 4.8)
日期: 2026-06-22
"""

from __future__ import annotations

import ast
import operator
from typing import Any


class SecurityValidationError(Exception):
    """安全验证失败异常 - 检测到非法的表达式结构"""

    pass


class SafeMathEvaluator(ast.NodeVisitor):
    """基于 AST NodeVisitor 的安全数学表达式求值器

    白名单策略:
    - 仅允许数字常量 (int/float)
    - 仅允许算术运算符: +, -, *, /, **, //, %
    - 仅允许一元负号: -x

    拒绝所有其他节点类型:
    - Call (函数调用，如 __import__)
    - Attribute (属性访问，如 obj.attr)
    - Name (变量引用，如 globals, locals)
    - Import/ImportFrom (导入语句)
    - Lambda (匿名函数)
    - 以及所有其他非白名单节点
    """

    # 白名单: 允许的二元运算符
    ALLOWED_BINARY_OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
    }

    # 白名单: 允许的一元运算符
    ALLOWED_UNARY_OPS = {
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def __init__(self):
        """初始化求值器"""
        self.result: int | float | None = None

    def evaluate(self, expression: str) -> int | float:
        """求值数学表达式

        Args:
            expression: 数学表达式字符串，如 "2 + 3 * 4"

        Returns:
            计算结果 (int 或 float)

        Raises:
            SecurityValidationError: 表达式包含非法节点
            SyntaxError: 表达式语法错误
            ZeroDivisionError: 除零错误
            ValueError: 其他计算错误
        """
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as e:
            raise SecurityValidationError(f"表达式语法错误: {e}") from e

        # 访问 AST 树，触发白名单验证
        self.visit(tree.body)

        if self.result is None:
            raise SecurityValidationError("表达式求值失败")

        return self.result

    def visit_Constant(self, node: ast.Constant) -> Any:
        """访问常量节点 (数字字面量)

        仅接受 int 和 float 类型的常量
        """
        if isinstance(node.value, (int, float)):
            self.result = node.value
            return self.result

        # 拒绝字符串、布尔值等其他常量
        raise SecurityValidationError(f"不支持的常量类型: {type(node.value).__name__}")

    def visit_Num(self, node: ast.Num) -> Any:
        """访问数字节点 (Python 3.7 及以下的兼容性)"""
        self.result = node.n
        return self.result

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        """访问一元运算符节点 (如 -x, +x)"""
        op_type = type(node.op)

        if op_type not in self.ALLOWED_UNARY_OPS:
            raise SecurityValidationError(f"不支持的一元运算符: {op_type.__name__}")

        # 递归求值操作数
        self.visit(node.operand)
        operand_value = self.result

        # 应用运算符
        op_func = self.ALLOWED_UNARY_OPS[op_type]
        self.result = op_func(operand_value)
        return self.result

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        """访问二元运算符节点 (如 x + y, x * y)"""
        op_type = type(node.op)

        if op_type not in self.ALLOWED_BINARY_OPS:
            raise SecurityValidationError(f"不支持的二元运算符: {op_type.__name__}")

        # 递归求值左右操作数
        self.visit(node.left)
        left_value = self.result

        self.visit(node.right)
        right_value = self.result

        # 应用运算符
        op_func = self.ALLOWED_BINARY_OPS[op_type]

        try:
            self.result = op_func(left_value, right_value)
        except ZeroDivisionError:
            raise ZeroDivisionError("除零错误")
        except Exception as e:
            raise ValueError(f"计算错误: {e}") from e

        return self.result

    def generic_visit(self, node: ast.AST) -> Any:
        """访问任何非白名单节点 - 触发安全异常

        这是 ast.NodeVisitor 的默认处理函数，会捕获所有未显式处理的节点类型
        """
        raise SecurityValidationError(
            f"检测到非法节点类型: {type(node).__name__} - 此节点可能用于代码注入攻击"
        )


def safe_calculate(expression: str) -> int | float:
    """安全计算数学表达式 (公共 API)

    示例:
        >>> safe_calculate("2 + 3")
        5
        >>> safe_calculate("10 / 2")
        5.0
        >>> safe_calculate("2 ** 8")
        256
        >>> safe_calculate("__import__('os').system('ls')")
        SecurityValidationError: 检测到非法节点类型: Call

    Args:
        expression: 数学表达式字符串

    Returns:
        计算结果

    Raises:
        SecurityValidationError: 非法表达式
        ZeroDivisionError: 除零错误
    """
    evaluator = SafeMathEvaluator()
    return evaluator.evaluate(expression)


def calculator_tool(expression: str) -> str:
    """计算器工具 - 用于 Agent 工具调用

    与原有接口保持兼容，但底层使用安全的 AST 解析器

    Args:
        expression: 数学表达式字符串

    Returns:
        计算结果字符串，或 "计算错误" (不泄露异常细节)
    """
    try:
        result = safe_calculate(expression)
        return str(result)
    except (SecurityValidationError, ZeroDivisionError, SyntaxError, ValueError):
        # 生产环境：不泄露具体异常信息给用户
        return "计算错误"


if __name__ == "__main__":
    # 快速验证
    print("✅ 基础运算:")
    print(f"  2 + 3 = {safe_calculate('2 + 3')}")
    print(f"  10 - 7 = {safe_calculate('10 - 7')}")
    print(f"  4 * 5 = {safe_calculate('4 * 5')}")
    print(f"  20 / 4 = {safe_calculate('20 / 4')}")
    print(f"  2 ** 8 = {safe_calculate('2 ** 8')}")
    print(f"  17 // 3 = {safe_calculate('17 // 3')}")
    print(f"  17 % 3 = {safe_calculate('17 % 3')}")
    print(f"  -(3 + 4) = {safe_calculate('-(3 + 4)')}")

    print("\n🛡️ 安全测试:")

    # 测试恶意注入
    malicious_tests = [
        "__import__('os').system('ls')",
        "exec('print(1)')",
        "globals()",
        "locals()",
        "open('/etc/passwd').read()",
        "__builtins__",
        "[x for x in range(10)]",  # 列表推导式
        "lambda x: x + 1",  # Lambda
    ]

    for expr in malicious_tests:
        try:
            safe_calculate(expr)
            print(f"  ❌ FAILED: {expr} (应该被拒绝)")
        except SecurityValidationError:
            print(f"  ✅ BLOCKED: {expr[:40]}...")
