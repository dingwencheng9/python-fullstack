"""L49 Agent 工具测试用例。"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.fixture(scope="module", autouse=True)
# ruff: noqa: F821
# 符号通过 _inject_calc_symbols fixture 动态注入

def _inject_agent_tools(solutions, request) -> None:
    """从 ``solutions`` fixture 动态获取 ``01_agent_tools`` 子模块并注入模块命名空间。

    取代原先顶层的 ``importlib.import_module("solutions.01_agent_tools")`` 静态导入，
    避免依赖 sys.path 注入。测试体保持原样，运行时通过模块全局名解析。
    """
    try:
        request.module.__dict__["agent_tools"] = getattr(solutions, "01_agent_tools")
    except (AttributeError, ImportError) as e:
        pytest.fail(f"无法注入 agent_tools 模块: {str(e)}")


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("搜索Python", "搜索结果: 搜索Python"),
        ("查找FastAPI资料", "搜索结果: 查找FastAPI资料"),
    ],
)
def test_simple_agent_routes_search_queries(query: str, expected: str) -> None:
    """测试搜索类查询路由到搜索工具。"""
    try:
        tools = agent_tools.create_tool_registry()
        result = agent_tools.simple_agent(query, tools)
        assert result == expected
    except Exception as e:
        pytest.fail(f"测试搜索查询失败: {str(e)}")


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("计算1+2", "3"),
        ("计算(10-4)/2", "3.0"),
    ],
)
def test_simple_agent_routes_calculator_queries(expression: str, expected: str) -> None:
    """测试计算类查询路由到计算器工具。"""
    try:
        tools = agent_tools.create_tool_registry()
        result = agent_tools.simple_agent(expression, tools)
        assert result == expected
    except Exception as e:
        pytest.fail(f"测试计算查询失败: {str(e)}")


def test_simple_agent_returns_fallback_for_empty_query() -> None:
    """测试空查询边界返回无法处理。"""
    try:
        tools = agent_tools.create_tool_registry()
        result = agent_tools.simple_agent("", tools)
        assert result == "无法处理该查询"
    except Exception as e:
        pytest.fail(f"测试空查询失败: {str(e)}")


def test_simple_agent_propagates_tool_error() -> None:
    """测试工具异常路径，Agent 不应静默吞掉工具故障。"""

    def broken_search(_query: str) -> str:
        raise RuntimeError("搜索服务不可用")

    tools: dict[str, Callable[..., Any]] = {
        "search": broken_search,
        "calculator": agent_tools.calculator_tool,
    }

    with pytest.raises(RuntimeError, match="搜索服务不可用"):
        agent_tools.simple_agent("搜索Python", tools)


def test_calculator_tool_returns_error_for_invalid_expression() -> None:
    """测试非法表达式会返回友好错误。"""
    try:
        result = agent_tools.calculator_tool("1+")
        assert result == "计算错误"
    except Exception as e:
        pytest.fail(f"测试计算器工具错误处理失败: {str(e)}")
