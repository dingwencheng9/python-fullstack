"""

from __future__ import annotations

L21 测试套件: Supervisor 路由模式

测试策略:
- 验证条件路由逻辑
- 测试循环工作流
- 确保不同 Agent 正确执行

运行方式:
    pytest tests/test_supervisor_router.py -v
"""

from __future__ import annotations

import time
from unittest.mock import patch

import pytest

# 必须在导入 langchain_core 之前执行 importorskip，否则收集阶段直接崩溃
pytest.importorskip("langchain_core", reason="需要 langchain-core（uv sync --extra ai）")

from langchain_core.messages import HumanMessage

# 使用 module 级别的全局变量，由 fixture 注入
SupervisorState = None  # type: ignore[assignment]
coder_node = None  # type: ignore[assignment]
create_supervisor_graph = None  # type: ignore[assignment]
researcher_node = None  # type: ignore[assignment]
should_continue = None  # type: ignore[assignment]
supervisor_node = None  # type: ignore[assignment]


@pytest.fixture(scope="module", autouse=True)
def _inject_examples(examples, request) -> None:
    """从 ``examples`` fixture 动态获取模块并注入模块命名空间。

    取代原先的 ``sys.modules`` 清理 + 动态绑定，避免全局状态污染。
    """
    try:
        supervisor_module = examples.supervisor_router_02
        request.module.SupervisorState = supervisor_module.SupervisorState
        request.module.coder_node = supervisor_module.coder_node
        request.module.create_supervisor_graph = supervisor_module.create_supervisor_graph
        request.module.researcher_node = supervisor_module.researcher_node
        request.module.should_continue = supervisor_module.should_continue
        request.module.supervisor_node = supervisor_module.supervisor_node
    except (ImportError, AttributeError) as e:
        pytest.skip(f"示例代码未完成（缺少必需的函数）: {e}", allow_module_level=True)


# ============================================================================
# 测试夹具
# ============================================================================
@pytest.fixture
def initial_state() -> SupervisorState:
    """创建测试用的初始状态"""
    return {
        "messages": [HumanMessage(content="测试任务")],
        "next_agent": "",
        "iteration": 0,
    }


# ============================================================================
# 单元测试: supervisor_node
# ============================================================================
def test_supervisor_first_iteration(initial_state: SupervisorState) -> None:
    """测试 Supervisor 在第一轮迭代中路由到 researcher"""
    try:
        # 执行
        result = supervisor_node(initial_state)

        # 验证
        assert result["next_agent"] == "researcher"
        assert result["iteration"] == 1
        assert len(result["messages"]) == 1
    except Exception as e:
        pytest.fail(f"test_supervisor_first_iteration 失败: {str(e)}")


def test_supervisor_second_iteration(initial_state: SupervisorState) -> None:
    """测试 Supervisor 在第二轮迭代中路由到 coder"""
    try:
        # 准备：设置为第一轮迭代后的状态
        state = {**initial_state, "iteration": 1}

        # 执行
        result = supervisor_node(state)

        # 验证
        assert result["next_agent"] == "coder"
        assert result["iteration"] == 2
    except Exception as e:
        pytest.fail(f"test_supervisor_second_iteration 失败: {str(e)}")


def test_supervisor_third_iteration(initial_state: SupervisorState) -> None:
    """测试 Supervisor 在第三轮迭代中标记为完成"""
    try:
        # 准备：设置为第二轮迭代后的状态
        state = {**initial_state, "iteration": 2}

        # 执行
        result = supervisor_node(state)

        # 验证
        assert result["next_agent"] == "FINISH"
        assert result["iteration"] == 3
    except Exception as e:
        pytest.fail(f"test_supervisor_third_iteration 失败: {str(e)}")


# ============================================================================
# 单元测试: researcher_node
# ============================================================================
def test_researcher_node_generates_research(initial_state: SupervisorState) -> None:
    """测试 Researcher Agent 生成研究结果"""
    try:
        # 执行
        result = researcher_node(initial_state)

        # 验证
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert "研究结果" in result["messages"][0].content
        assert result["messages"][0].name == "researcher"
    except Exception as e:
        pytest.fail(f"test_researcher_node_generates_research 失败: {str(e)}")


# ============================================================================
# 单元测试: coder_node
# ============================================================================
def test_coder_node_generates_code(initial_state: SupervisorState) -> None:
    """测试 Coder Agent 生成代码"""
    try:
        # 执行
        result = coder_node(initial_state)

        # 验证
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert "代码" in result["messages"][0].content
        assert result["messages"][0].name == "coder"
    except Exception as e:
        pytest.fail(f"test_coder_node_generates_code 失败: {str(e)}")


# ============================================================================
# 单元测试: should_continue 路由函数
# ============================================================================
def test_should_continue_routes_to_researcher(initial_state: SupervisorState) -> None:
    """测试路由函数正确路由到 researcher"""
    try:
        # 准备
        state = {**initial_state, "next_agent": "researcher"}

        # 执行
        result = should_continue(state)

        # 验证
        assert result == "researcher"
    except Exception as e:
        pytest.fail(f"test_should_continue_routes_to_researcher 失败: {str(e)}")


def test_should_continue_routes_to_coder(initial_state: SupervisorState) -> None:
    """测试路由函数正确路由到 coder"""
    try:
        # 准备
        state = {**initial_state, "next_agent": "coder"}

        # 执行
        result = should_continue(state)

        # 验证
        assert result == "coder"
    except Exception as e:
        pytest.fail(f"test_should_continue_routes_to_coder 失败: {str(e)}")


def test_should_continue_routes_to_end(initial_state: SupervisorState) -> None:
    """测试路由函数在任务完成时路由到 END"""
    try:
        # 准备
        state = {**initial_state, "next_agent": "FINISH"}

        # 执行
        result = should_continue(state)

        # 验证
        from langgraph.graph import END

        assert result == END
    except Exception as e:
        pytest.fail(f"test_should_continue_routes_to_end 失败: {str(e)}")


def test_should_continue_handles_unknown_agent(initial_state: SupervisorState) -> None:
    """测试路由函数处理未知 Agent（安全保护）"""
    try:
        # 准备
        state = {**initial_state, "next_agent": "unknown_agent"}

        # 执行
        result = should_continue(state)

        # 验证：应该默认路由到 END
        from langgraph.graph import END

        assert result == END
    except Exception as e:
        pytest.fail(f"test_should_continue_handles_unknown_agent 失败: {str(e)}")


# ============================================================================
# 集成测试: 完整图执行
# ============================================================================
def test_supervisor_graph_full_execution(initial_state: SupervisorState) -> None:
    """测试 Supervisor 图的完整执行流程"""
    try:
        # 准备
        graph = create_supervisor_graph()

        # 执行
        final_state = graph.invoke(initial_state)

        # 验证：应该完成完整的工作流
        # 初始消息 + supervisor 决策 + researcher 结果 + supervisor 决策 + coder 结果 + supervisor 决策
        assert len(final_state["messages"]) >= 5
        assert final_state["iteration"] == 3
        assert final_state["next_agent"] == "FINISH"
    except Exception as e:
        pytest.fail(f"test_supervisor_graph_full_execution 失败: {str(e)}")


def test_supervisor_graph_iteration_count(initial_state: SupervisorState) -> None:
    """测试工作流的迭代次数"""
    try:
        # 准备
        graph = create_supervisor_graph()

        # 执行
        final_state = graph.invoke(initial_state)

        # 验证：应该迭代 3 次
        assert final_state["iteration"] == 3
    except Exception as e:
        pytest.fail(f"test_supervisor_graph_iteration_count 失败: {str(e)}")


def test_supervisor_graph_message_accumulation(initial_state: SupervisorState) -> None:
    """测试消息累加语义（所有消息都应保留）"""
    try:
        # 准备
        graph = create_supervisor_graph()

        # 执行
        final_state = graph.invoke(initial_state)

        # 验证：消息应该累加
        # 检查是否包含不同 Agent 的消息
        agent_names = [msg.name for msg in final_state["messages"] if hasattr(msg, "name")]
        assert "researcher" in agent_names
        assert "coder" in agent_names
    except Exception as e:
        pytest.fail(f"test_supervisor_graph_message_accumulation 失败: {str(e)}")


# ============================================================================
# 边界情况测试
# ============================================================================
def test_supervisor_graph_with_empty_message() -> None:
    """测试空消息的处理"""
    try:
        # 准备
        state: SupervisorState = {
            "messages": [HumanMessage(content="")],
            "next_agent": "",
            "iteration": 0,
        }
        graph = create_supervisor_graph()

        # 执行
        final_state = graph.invoke(state)

        # 验证：应该正常完成
        assert final_state["iteration"] == 3
        assert final_state["next_agent"] == "FINISH"
    except Exception as e:
        pytest.fail(f"test_supervisor_graph_with_empty_message 失败: {str(e)}")


# ============================================================================
# 性能测试
# ============================================================================
def test_supervisor_graph_performance(initial_state: SupervisorState) -> None:
    """测试工作流执行性能"""
    try:
        graph = create_supervisor_graph()

        start_time = time.time()
        graph.invoke(initial_state)
        elapsed_time = time.time() - start_time

        # 验证：应该在 2 秒内完成（无真实 LLM 调用）
        assert elapsed_time < 2.0, f"执行时间过长: {elapsed_time:.3f}s"
    except Exception as e:
        pytest.fail(f"test_supervisor_graph_performance 失败: {str(e)}")


# ============================================================================
# Mock 示例（演示如何 Mock Supervisor 的 LLM 决策）
# ============================================================================
@pytest.mark.skip(reason="示例测试：演示 Supervisor LLM Mock")
def test_supervisor_with_mocked_llm(initial_state: SupervisorState) -> None:
    """
    示例：演示如何 Mock Supervisor 的 LLM 决策

    在实际应用中，Supervisor 会使用 LLM 分析任务并决策路由
    """
    try:
        from unittest.mock import MagicMock

        from langchain_core.messages import AIMessage

        # Mock LLM 响应
        with patch("langchain_openai.ChatOpenAI") as mock_llm_class:
            mock_llm = MagicMock()
            # 模拟 LLM 返回路由决策
            mock_llm.invoke.return_value = AIMessage(content='{"next_agent": "researcher"}')
            mock_llm_class.return_value = mock_llm

            # 如果 supervisor_node 使用了真实 LLM，这里会被 Mock
            # result = supervisor_node(initial_state)
            # assert result["next_agent"] == "researcher"

            # 当前实现是硬编码逻辑，这里仅作示例
    except Exception as e:
        pytest.fail(f"test_supervisor_with_mocked_llm 失败: {str(e)}")
