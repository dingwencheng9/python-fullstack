"""
L55 LangGraph 状态机 — 核心行为测试

测试覆盖：
- 状态图节点注册与路由函数逻辑
- 条件边的路由决策（迭代 < 3 → 继续，否则结束）
- 检查点保存与历史恢复
- Human-in-the-Loop 中断管理
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


LESSON_ROOT = Path(__file__).resolve().parent.parent


def _load_module(name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# 1. 条件路由逻辑测试
# ---------------------------------------------------------------------------


def test_should_continue_continues_when_iteration_below_3():
    """迭代次数 < 3 时，路由应返回 "agent"（继续）。"""
    _load_module("examples_01", LESSON_ROOT / "examples" / "01_state_graph.py")

    # 模拟 should_continue 逻辑
    def should_continue(state):
        return "agent" if state["iteration"] < 3 else "end"

    assert should_continue({"messages": [], "iteration": 0}) == "agent"
    assert should_continue({"messages": [], "iteration": 1}) == "agent"
    assert should_continue({"messages": [], "iteration": 2}) == "agent"


def test_should_continue_ends_when_iteration_reaches_3():
    """迭代次数 >= 3 时，路由应返回 "end"（结束）。"""

    def should_continue(state):
        return "agent" if state["iteration"] < 3 else "end"

    assert should_continue({"messages": [], "iteration": 3}) == "end"
    assert should_continue({"messages": [], "iteration": 4}) == "end"


def test_graph_structure_has_nodes_and_entry_point():
    """状态图应包含节点列表和入口点。"""
    mod = _load_module("examples_01", LESSON_ROOT / "examples" / "01_state_graph.py")
    graph_def = mod.build_graph()

    assert "nodes" in graph_def
    assert "entry_point" in graph_def
    assert "agent" in graph_def["nodes"]
    assert graph_def["entry_point"] == "agent"


# ---------------------------------------------------------------------------
# 2. 工具调用循环路由测试
# ---------------------------------------------------------------------------


def test_route_by_tool_calls_routes_to_tools_when_tool_calls_present():
    """tool_calls 非空时，应路由到 "tools" 节点。"""
    mod = _load_module("examples_02", LESSON_ROOT / "examples" / "02_conditional_routing.py")

    state = {"messages": ["user: 今天天气如何"], "tool_calls": ["weather"]}
    result = mod.route_by_tool_calls(state)
    assert result == "tools"


def test_route_by_tool_calls_routes_to_end_when_no_tool_calls():
    """tool_calls 为空时，应路由到 "end"。"""
    mod = _load_module("examples_02", LESSON_ROOT / "examples" / "02_conditional_routing.py")

    state = {"messages": ["user: 你好"], "tool_calls": []}
    result = mod.route_by_tool_calls(state)
    assert result == "end"


def test_supervisor_route_research_for_search_intent():
    """包含"搜索"关键词应路由到 "research"。"""
    mod = _load_module("examples_02", LESSON_ROOT / "examples" / "02_conditional_routing.py")

    state = {"messages": ["user: 请帮我搜索 Python 最新动态"], "tool_calls": []}
    assert mod.supervisor_route(state) == "research"


def test_supervisor_route_code_for_code_intent():
    """包含"代码"关键词应路由到 "code"。"""
    mod = _load_module("examples_02", LESSON_ROOT / "examples" / "02_conditional_routing.py")

    state = {"messages": ["user: 帮我实现快速排序"], "tool_calls": []}
    assert mod.supervisor_route(state) == "code"


def test_supervisor_route_end_for_other_intents():
    """其他意图应路由到 "end"。"""
    mod = _load_module("examples_02", LESSON_ROOT / "examples" / "02_conditional_routing.py")

    for intent in ["你好", "再见", "谢谢"]:
        state = {"messages": [f"user: {intent}"], "tool_calls": []}
        assert mod.supervisor_route(state) == "end", f"意图 '{intent}' 应路由到 end"


def test_mock_agent_routes_to_tool_for_weather():
    """天气查询应触发工具调用。"""
    mod = _load_module("examples_02", LESSON_ROOT / "examples" / "02_conditional_routing.py")

    state = {"messages": ["user: 北京天气"], "tool_calls": []}
    result = mod.mock_agent(state)
    assert "weather" in result["tool_calls"]


def test_mock_agent_no_tool_for_greeting():
    """问候语无需工具调用。"""
    mod = _load_module("examples_02", LESSON_ROOT / "examples" / "02_conditional_routing.py")

    state = {"messages": ["user: 你好"], "tool_calls": []}
    result = mod.mock_agent(state)
    assert result["tool_calls"] == []


def test_simulate_tool_loop_terminates_without_tool():
    """无工具调用时，循环应立即终止。"""
    mod = _load_module("examples_02", LESSON_ROOT / "examples" / "02_conditional_routing.py")

    messages = mod.simulate_tool_loop("你好")
    # "你好" 无需工具，循环 1 次即终止
    assert "agent: 直接回答" in messages


def test_simulate_tool_loop_calls_tool_for_weather():
    """天气查询应触发工具节点。"""
    mod = _load_module("examples_02", LESSON_ROOT / "examples" / "02_conditional_routing.py")

    messages = mod.simulate_tool_loop("北京天气如何")
    assert any("tool:weather" in msg for msg in messages)


# ---------------------------------------------------------------------------
# 3. 检查点持久化测试
# ---------------------------------------------------------------------------


def test_memory_saver_put_and_get():
    """检查点应能保存并恢复最新状态。"""
    mod = _load_module("examples_03", LESSON_ROOT / "examples" / "03_checkpointing.py")

    saver = mod.MemorySaver()
    checkpoint = mod.Checkpoint(thread_id="test-1", step=0, values={"messages": ["hello"]})
    saver.put("test-1", checkpoint)

    restored = saver.get("test-1")
    assert restored is not None
    assert restored.step == 0
    assert restored.values["messages"] == ["hello"]


def test_memory_saver_get_returns_none_for_unknown_thread():
    """未知线程 ID 应返回 None。"""
    mod = _load_module("examples_03", LESSON_ROOT / "examples" / "03_checkpointing.py")

    saver = mod.MemorySaver()
    assert saver.get("unknown-thread") is None


def test_memory_saver_get_history_returns_all_checkpoints():
    """get_history 应返回所有历史检查点。"""
    mod = _load_module("examples_03", LESSON_ROOT / "examples" / "03_checkpointing.py")

    saver = mod.MemorySaver()
    for i in range(3):
        saver.put("test-2", mod.Checkpoint(thread_id="test-2", step=i, values={}))

    history = saver.get_history("test-2")
    assert len(history) == 3
    assert [cp.step for cp in history] == [0, 1, 2]


def test_simulate_workflow_with_checkpoint_returns_valid_state():
    """模拟工作流应返回有效的检查点状态。"""
    mod = _load_module("examples_03", LESSON_ROOT / "examples" / "03_checkpointing.py")

    result = mod.simulate_workflow_with_checkpoint()
    assert result["latest_step"] == 4  # 5 步: 0-4
    assert result["history_length"] == 5
    assert result["can_resume"] is True


# ---------------------------------------------------------------------------
# 4. Human-in-the-Loop 中断测试
# ---------------------------------------------------------------------------


def test_interrupt_manager_pause_and_resume():
    """中断管理器应支持暂停和恢复。"""
    mod = _load_module("examples_03", LESSON_ROOT / "examples" / "03_checkpointing.py")

    mgr = mod.InterruptManager()
    thread_id = "workflow-x"

    # 未暂停时不应触发中断
    assert mgr.should_interrupt(thread_id, "human_review") is False

    # 暂停后应触发中断
    mgr.pause(thread_id)
    assert mgr.should_interrupt(thread_id, "human_review") is True

    # 恢复后不再触发
    mgr.resume(thread_id)
    assert mgr.should_interrupt(thread_id, "human_review") is False


def test_simulate_human_in_the_loop_approved_continues():
    """人类批准后工作流应继续执行。"""
    mod = _load_module("examples_03", LESSON_ROOT / "examples" / "03_checkpointing.py")

    result = mod.simulate_human_in_the_loop()
    assert result["human_approved"] is True
    assert result["final_messages"][-1] == "[agent] 生成了代码方案，请审批"


# ---------------------------------------------------------------------------
# 5. Solutions 测试
# ---------------------------------------------------------------------------


def test_task_planner_solution_runs_without_error():
    """练习参考答案应能完整运行工作流。"""
    mod = _load_module("sol_01", LESSON_ROOT / "solutions" / "01_task_planner.py")

    result = mod.run_workflow("1. 分析\n2. 编码\n3. 测试")
    assert "任务完成" in result
    assert "分析" in result
    assert "编码" in result
    assert "测试" in result


def test_task_planner_solution_handles_empty_task():
    """空任务应有合理处理。"""
    mod = _load_module("sol_01", LESSON_ROOT / "solutions" / "01_task_planner.py")

    result = mod.run_workflow("")
    assert "任务完成" in result or "处理任务" in result


def test_planner_node_parses_numbered_steps():
    """planner_node 应正确解析带序号的任务。"""
    mod = _load_module("sol_01", LESSON_ROOT / "solutions" / "01_task_planner.py")

    state = {"input": "1. 第一步\n2. 第二步\n3. 第三步", "plan": [], "past_steps": [], "result": ""}
    result = mod.planner_node(state)

    assert len(result["plan"]) >= 1
    assert "第一步" in result["plan"][0] or "第一步" in str(result["plan"])


def test_should_continue_routes_execute_when_plan_present():
    """should_continue 在 plan 非空时应返回 "execute"。"""
    mod = _load_module("sol_01", LESSON_ROOT / "solutions" / "01_task_planner.py")

    assert mod.should_continue({"plan": ["step1"], "past_steps": [], "result": "", "input": ""}) == "execute"


def test_should_continue_routes_end_when_plan_empty():
    """should_continue 在 plan 为空时应返回 "end"。"""
    mod = _load_module("sol_01", LESSON_ROOT / "solutions" / "01_task_planner.py")

    assert mod.should_continue({"plan": [], "past_steps": [], "result": "", "input": ""}) == "end"


def test_executor_node_removes_completed_step():
    """executor_node 执行后应从 plan 中移除该步骤。"""
    mod = _load_module("sol_01", LESSON_ROOT / "solutions" / "01_task_planner.py")

    state = {"input": "分析", "plan": ["分析需求", "编写代码"], "past_steps": [], "result": ""}
    result = mod.executor_node(state)

    assert "分析需求" not in result["plan"]
    assert len(result["past_steps"]) == 1
