"""L58 Agent 评估与调试测试用例。"""

from __future__ import annotations

import pytest

# 使用 module 级别的全局变量，由 fixture 注入
AgentDebugger = None  # type: ignore[assignment]
AgentMetrics = None  # type: ignore[assignment]


@pytest.fixture(autouse=True)
def _inject_solutions(solutions, request) -> None:
    """从 solutions 模块动态注入被测类，避免静态导入。

    取代原先顶层的 ``import_module("solutions.xxx")`` 静态导入，
    避免依赖 sys.path 注入。测试体保持原样，运行时通过模块全局名解析。
    """
    _solution_module = getattr(solutions, "01_evaluation_debugging")
    request.module.AgentDebugger = _solution_module.AgentDebugger
    request.module.AgentMetrics = _solution_module.AgentMetrics


def test_agent_metrics_initial_state() -> None:
    """初始状态无任务记录。"""
    m = AgentMetrics()
    metrics = m.get_metrics()
    assert metrics["total_tasks"] == 0
    assert metrics["success_rate"] == 0


def test_agent_metrics_record_success() -> None:
    """成功任务影响 success_rate。"""
    m = AgentMetrics()
    m.record_task(success=True, tokens=100, duration=1.0)
    m.record_task(success=True, tokens=200, duration=2.0)
    metrics = m.get_metrics()
    assert metrics["total_tasks"] == 2
    assert metrics["success_rate"] == 1.0
    assert metrics["avg_tokens"] == 150.0


@pytest.mark.parametrize(
    ("results", "expected_rate"),
    [
        ([True, True, True], 1.0),
        ([True, False], 0.5),
        ([False, False], 0.0),
        ([True, True, False, False], 0.5),
    ],
)
def test_agent_metrics_success_rate_parametrized(
    results: list[bool],
    expected_rate: float,
) -> None:
    """参数化：不同成功/失败组合的 success_rate。"""
    m = AgentMetrics()
    for success in results:
        m.record_task(success=success, tokens=10, duration=0.1)
    assert m.get_metrics()["success_rate"] == pytest.approx(expected_rate)


def test_agent_metrics_empty_division_safe() -> None:
    """边界：无任务时不触发除零。"""
    m = AgentMetrics()
    metrics = m.get_metrics()
    assert metrics["avg_tokens"] == 0
    assert metrics["avg_time"] == 0


def test_agent_debugger_log_basic() -> None:
    """日志记录基本功能。"""
    d = AgentDebugger()
    d.log("INFO", "started")
    d.log("ERROR", "failure", {"code": 500})
    assert len(d.logs) == 2


def test_agent_debugger_get_errors_filters() -> None:
    """get_errors 仅返回 ERROR 级别。"""
    d = AgentDebugger()
    d.log("INFO", "ok")
    d.log("ERROR", "fail1")
    d.log("WARNING", "warn")
    d.log("ERROR", "fail2")
    errors = d.get_errors()
    assert len(errors) == 2
    assert all(e["level"] == "ERROR" for e in errors)


def test_agent_debugger_log_data_default() -> None:
    """边界：未提供 data 时使用空 dict。"""
    d = AgentDebugger()
    d.log("INFO", "message")
    assert d.logs[0]["data"] == {}
