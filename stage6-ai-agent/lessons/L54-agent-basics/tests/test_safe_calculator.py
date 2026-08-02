"""

from __future__ import annotations

安全计算器单元测试 - 覆盖正常计算与恶意注入拦截

测试策略:
1. 正常算术运算 (加减乘除幂取模)
2. 复杂表达式 (运算符优先级、括号)
3. 边界情况 (除零、负数、浮点数)
4. 恶意代码注入拦截 (函数调用、导入、属性访问等)
5. 语法错误处理

作者: Claude Code (Opus 4.8)
日期: 2026-06-22
"""
# ruff: noqa: F821
# 符号通过 _inject_calc_symbols fixture 动态注入模块命名空间，ruff 无法静态检测

import pytest


@pytest.fixture(scope="module", autouse=True)
def _inject_calc_symbols(solutions, request) -> None:
    """从 ``solutions`` fixture 动态获取安全计算器符号并注入模块命名空间。

    取代原先顶层的 ``from safe_calculator import ...`` 静态导入，避免依赖
    sys.path 注入。测试体保持原样，运行时通过模块全局名解析下列符号：
    ``SecurityValidationError`` / ``SafeMathEvaluator`` /
    ``calculator_tool`` / ``safe_calculate``。
    """
    sc = solutions.safe_calculator
    request.module.__dict__.update(
        SecurityValidationError=sc.SecurityValidationError,
        SafeMathEvaluator=sc.SafeMathEvaluator,
        calculator_tool=sc.calculator_tool,
        safe_calculate=sc.safe_calculate,
    )


class TestBasicArithmetic:
    """测试基础算术运算"""

    def test_addition(self):
        """测试加法"""
        assert safe_calculate("2 + 3") == 5
        assert safe_calculate("10 + 20 + 30") == 60
        assert safe_calculate("0 + 0") == 0

    def test_subtraction(self):
        """测试减法"""
        assert safe_calculate("10 - 3") == 7
        assert safe_calculate("5 - 10") == -5
        assert safe_calculate("100 - 50 - 25") == 25

    def test_multiplication(self):
        """测试乘法"""
        assert safe_calculate("4 * 5") == 20
        assert safe_calculate("2 * 3 * 4") == 24
        assert safe_calculate("0 * 999") == 0

    def test_division(self):
        """测试除法"""
        assert safe_calculate("20 / 4") == 5.0
        assert safe_calculate("7 / 2") == 3.5
        assert safe_calculate("10 / 3") == pytest.approx(3.333333, rel=1e-5)

    def test_floor_division(self):
        """测试整除"""
        assert safe_calculate("17 // 3") == 5
        assert safe_calculate("20 // 4") == 5
        assert safe_calculate("7 // 2") == 3

    def test_modulo(self):
        """测试取模"""
        assert safe_calculate("17 % 3") == 2
        assert safe_calculate("20 % 4") == 0
        assert safe_calculate("10 % 7") == 3

    def test_power(self):
        """测试幂运算"""
        assert safe_calculate("2 ** 3") == 8
        assert safe_calculate("2 ** 8") == 256
        assert safe_calculate("10 ** 0") == 1
        assert safe_calculate("5 ** 2") == 25

    def test_unary_operators(self):
        """测试一元运算符"""
        assert safe_calculate("-5") == -5
        assert safe_calculate("-(3 + 4)") == -7
        assert safe_calculate("+10") == 10
        assert safe_calculate("-(10 - 15)") == 5


class TestComplexExpressions:
    """测试复杂表达式与运算符优先级"""

    def test_operator_precedence(self):
        """测试运算符优先级"""
        assert safe_calculate("2 + 3 * 4") == 14  # 乘法优先
        assert safe_calculate("10 - 2 * 3") == 4
        assert safe_calculate("2 ** 3 + 1") == 9
        assert safe_calculate("10 / 2 + 3") == 8.0

    def test_parentheses(self):
        """测试括号改变优先级"""
        assert safe_calculate("(2 + 3) * 4") == 20
        assert safe_calculate("(10 - 2) * 3") == 24
        assert safe_calculate("2 ** (3 + 1)") == 16
        assert safe_calculate("(10 / 2) + 3") == 8.0

    def test_nested_expressions(self):
        """测试嵌套表达式"""
        assert safe_calculate("((2 + 3) * 4) - 5") == 15
        assert safe_calculate("2 * (3 + (4 * 5))") == 46
        assert safe_calculate("(10 + 20) / (5 - 2)") == 10.0

    def test_mixed_operations(self):
        """测试混合运算"""
        assert safe_calculate("2 + 3 * 4 - 5 / 2") == 11.5
        assert safe_calculate("10 % 3 + 2 ** 4") == 17
        assert safe_calculate("(100 - 50) // 3 * 2") == 32


class TestEdgeCases:
    """测试边界情况"""

    def test_zero_division(self):
        """测试除零错误"""
        with pytest.raises(ZeroDivisionError):
            safe_calculate("10 / 0")

        with pytest.raises(ZeroDivisionError):
            safe_calculate("5 // 0")

        with pytest.raises(ZeroDivisionError):
            safe_calculate("7 % 0")

    def test_negative_numbers(self):
        """测试负数运算"""
        assert safe_calculate("-5 + 3") == -2
        assert safe_calculate("-10 * -2") == 20
        assert safe_calculate("(-5) ** 2") == 25
        assert safe_calculate("-20 / 4") == -5.0

    def test_floating_point_numbers(self):
        """测试浮点数"""
        assert safe_calculate("3.14 + 2.86") == pytest.approx(6.0)
        assert safe_calculate("10.5 * 2") == 21.0
        assert safe_calculate("7.5 / 2.5") == 3.0
        assert safe_calculate("2.5 ** 2") == 6.25

    def test_large_numbers(self):
        """测试大数运算"""
        assert safe_calculate("999999 + 1") == 1000000
        assert safe_calculate("2 ** 20") == 1048576
        assert safe_calculate("1000000 / 1000") == 1000.0

    def test_very_small_results(self):
        """测试极小结果"""
        assert safe_calculate("1 / 1000000") == 1e-6
        assert safe_calculate("0.000001 * 2") == 2e-6


class TestSecurityInjectionBlocking:
    """测试恶意代码注入拦截 - 核心安全测试"""

    def test_block_function_calls(self):
        """拦截函数调用 - RCE 攻击向量"""
        malicious_expressions = [
            "__import__('os').system('ls')",
            "exec('print(1)')",
            "eval('1+1')",
            "open('/etc/passwd').read()",
            "compile('print(1)', '', 'exec')",
            "globals()",
            "locals()",
            "dir()",
            "help()",
            "print(1)",
            "int('123')",
            "float('3.14')",
        ]

        for expr in malicious_expressions:
            with pytest.raises(SecurityValidationError, match="检测到非法节点类型"):
                safe_calculate(expr)

    def test_block_attribute_access(self):
        """拦截属性访问 - 可能用于访问敏感对象"""
        malicious_expressions = [
            "__builtins__",
            "__globals__",
            "__dict__",
            "[].__class__.__bases__",
            "().__class__.__bases__[0].__subclasses__()",
        ]

        for expr in malicious_expressions:
            with pytest.raises(SecurityValidationError):
                safe_calculate(expr)

    def test_block_name_references(self):
        """拦截变量引用 - 防止访问外部作用域"""
        malicious_expressions = [
            "x",
            "variable",
            "globals",
            "locals",
            "__builtins__",
        ]

        for expr in malicious_expressions:
            with pytest.raises(SecurityValidationError):
                safe_calculate(expr)

    def test_block_import_statements(self):
        """拦截导入语句"""
        with pytest.raises(SecurityValidationError):
            safe_calculate("import os")

        with pytest.raises(SecurityValidationError):
            safe_calculate("from os import system")

    def test_block_lambda_functions(self):
        """拦截匿名函数"""
        with pytest.raises(SecurityValidationError):
            safe_calculate("lambda x: x + 1")

        with pytest.raises(SecurityValidationError):
            safe_calculate("(lambda: 42)()")

    def test_block_comprehensions(self):
        """拦截列表/字典/集合推导式"""
        malicious_expressions = [
            "[x for x in range(10)]",
            "{x: x**2 for x in range(5)}",
            "{x for x in range(10)}",
            "(x for x in range(10))",
        ]

        for expr in malicious_expressions:
            with pytest.raises(SecurityValidationError):
                safe_calculate(expr)

    def test_block_subscript_operations(self):
        """拦截下标访问 - 可能用于字典/列表访问"""
        malicious_expressions = [
            "[]",
            "[1, 2, 3]",
            "[1][0]",
            "{}",
            "{'key': 'value'}",
        ]

        for expr in malicious_expressions:
            with pytest.raises(SecurityValidationError):
                safe_calculate(expr)

    def test_block_boolean_operations(self):
        """拦截布尔运算 - 不在白名单内"""
        with pytest.raises(SecurityValidationError):
            safe_calculate("True and False")

        with pytest.raises(SecurityValidationError):
            safe_calculate("1 < 2")

        with pytest.raises(SecurityValidationError):
            safe_calculate("5 > 3")

    def test_block_string_literals(self):
        """拦截字符串字面量 - 可能用于构造恶意载荷"""
        with pytest.raises(SecurityValidationError):
            safe_calculate("'hello'")

        with pytest.raises(SecurityValidationError):
            safe_calculate('"world"')


class TestSyntaxErrors:
    """测试语法错误处理"""

    def test_invalid_syntax(self):
        """测试非法语法"""
        with pytest.raises(SecurityValidationError, match="表达式语法错误"):
            safe_calculate("2 +")

        with pytest.raises(SecurityValidationError, match="表达式语法错误"):
            safe_calculate("* 3")

        with pytest.raises(SecurityValidationError, match="表达式语法错误"):
            safe_calculate("((2 + 3)")

    def test_empty_expression(self):
        """测试空表达式"""
        with pytest.raises(SecurityValidationError):
            safe_calculate("")

    def test_whitespace_only(self):
        """测试仅包含空白字符"""
        with pytest.raises(SecurityValidationError):
            safe_calculate("   ")


class TestCalculatorToolInterface:
    """测试计算器工具接口 (用于 Agent 工具调用)"""

    def test_successful_calculation(self):
        """测试成功的计算"""
        assert calculator_tool("2 + 3") == "5"
        assert calculator_tool("10 / 2") == "5.0"
        assert calculator_tool("2 ** 8") == "256"

    def test_error_handling_no_leak(self):
        """测试错误处理 - 不泄露异常细节"""
        # 所有错误统一返回 "计算错误"
        assert calculator_tool("10 / 0") == "计算错误"
        assert calculator_tool("__import__('os')") == "计算错误"
        assert calculator_tool("2 +") == "计算错误"
        assert calculator_tool("invalid") == "计算错误"


class TestEvaluatorStateless:
    """测试求值器的无状态性 (多次调用互不影响)"""

    def test_multiple_evaluations(self):
        """测试多次求值互不影响"""
        evaluator = SafeMathEvaluator()

        result1 = evaluator.evaluate("2 + 3")
        assert result1 == 5

        result2 = evaluator.evaluate("10 * 5")
        assert result2 == 50

        # 验证第一次求值结果未被污染
        result3 = evaluator.evaluate("2 + 3")
        assert result3 == 5


# ============================================================================
# 集成测试：模拟真实 Agent 工具调用场景
# ============================================================================


class TestAgentIntegration:
    """集成测试 - 模拟 Agent 工具调用场景"""

    def test_agent_calculator_workflow(self):
        """模拟 Agent 使用计算器工具的完整流程"""
        # 用户查询: "计算 (100 - 32) * 5 / 9"
        user_query = "计算 (100 - 32) * 5 / 9"
        expression = user_query.replace("计算", "").strip()

        result = calculator_tool(expression)

        # 验证返回值是字符串（Agent 工具接口约定）
        assert isinstance(result, str)
        assert result != "计算错误"

        # 验证计算结果正确（华氏度转摄氏度）
        assert float(result) == pytest.approx(37.777777, rel=1e-5)

    def test_agent_handles_malicious_input(self):
        """模拟 Agent 接收到恶意输入"""
        # 攻击者尝试通过 Agent 执行系统命令
        malicious_query = "计算 __import__('os').system('rm -rf /')"
        expression = malicious_query.replace("计算", "").strip()

        result = calculator_tool(expression)

        # 验证返回安全的错误消息，而非执行命令
        assert result == "计算错误"


# ============================================================================
# Pytest 配置与运行
# ============================================================================

if __name__ == "__main__":
    # 直接运行此文件时执行测试
    pytest.main([__file__, "-v", "--tb=short"])
