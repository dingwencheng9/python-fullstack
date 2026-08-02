"""

from __future__ import annotations

L21 测试套件: 基础 Agent 节点

测试策略:
- 使用 Mock 隔离外部 LLM 调用
- 验证状态机的执行流程
- 确保消息累加语义正确

运行方式:
    pytest tests/test_basic_agent.py -v
"""

from __future__ import annotations

import importlib.util
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

pytest.importorskip("langchain_core", reason="需要 langchain-core（uv sync --extra ai）")

# 导入被测试模块
try:
    from langchain_core.messages import AIMessage, HumanMessage
except ImportError as e:
    pytest.fail(f"导入 langchain_core.messages 失败: {str(e)}")

# examples 已由根 conftest.py 加载到 sys.modules["examples"]
import sys

if "examples" in sys.modules:
    _examples_mod = sys.modules["examples"]
    AgentState = _examples_mod.AgentState  # type: ignore[assignment]
    agent_node = _examples_mod.agent_node  # type: ignore[assignment]
    create_agent_graph = _examples_mod.create_agent_graph  # type: ignore[assignment]
else:
    # fallback: 手动加载
    import importlib.util

    examples_dir = Path(__file__).parent.parent / "examples"
    spec = importlib.util.spec_from_file_location(
        "basic_agent_node_01", examples_dir / "basic_agent_node_01.py"
    )
    _mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_mod)
    AgentState = _mod.AgentState  # type: ignore[assignment]
    agent_node = _mod.agent_node  # type: ignore[assignment]
    create_agent_graph = _mod.create_agent_graph  # type: ignore[assignment]


# ============================================================================
# 测试夹具
# ============================================================================
@pytest.fixture
def sample_state() -> AgentState:
    """创建测试用的初始状态"""
    return {
        "messages": [HumanMessage(content="测试任务")],
        "task_completed": False,
    }


# ============================================================================
# 单元测试: agent_node 函数
# ============================================================================
def test_agent_node_updates_messages(sample_state: AgentState) -> None:
    """测试 agent_node 能正确添加 AI 消息到消息列表"""
    try:
        # 执行
        result = agent_node(sample_state)

        # 验证
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)
        assert "测试任务" in result["messages"][0].content
    except Exception as e:
        pytest.fail(f"test_agent_node_updates_messages 失败: {str(e)}")


def test_agent_node_marks_task_completed(sample_state: AgentState) -> None:
    """测试 agent_node 能正确标记任务为已完成"""
    try:
        # 执行
        result = agent_node(sample_state)

        # 验证
        assert "task_completed" in result
        assert result["task_completed"] is True
    except Exception as e:
        pytest.fail(f"test_agent_node_marks_task_completed 失败: {str(e)}")


def test_agent_node_handles_empty_message() -> None:
    """测试 agent_node 能处理空消息（边界情况）"""
    try:
        # 准备
        state: AgentState = {
            "messages": [HumanMessage(content="")],
            "task_completed": False,
        }

        # 执行
        result = agent_node(state)

        # 验证：应该仍然返回有效结果
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["task_completed"] is True
    except Exception as e:
        pytest.fail(f"test_agent_node_handles_empty_message 失败: {str(e)}")


# ============================================================================
# 集成测试: 完整图执行
# ============================================================================
def test_create_agent_graph_structure() -> None:
    """测试图的结构是否正确"""
    try:
        # 执行
        graph = create_agent_graph()

        # 验证：图应该可以正常编译
        assert graph is not None
        # LangGraph 编译后的图对象应该有 invoke 方法
        assert hasattr(graph, "invoke")
    except Exception as e:
        pytest.fail(f"test_create_agent_graph_structure 失败: {str(e)}")


def test_graph_execution_flow(sample_state: AgentState) -> None:
    """测试图的完整执行流程"""
    try:
        # 准备
        graph = create_agent_graph()

        # 执行
        final_state = graph.invoke(sample_state)

        # 验证：最终状态
        assert len(final_state["messages"]) == 2  # 原始消息 + AI 回复
        assert isinstance(final_state["messages"][0], HumanMessage)
        assert isinstance(final_state["messages"][1], AIMessage)
        assert final_state["task_completed"] is True
    except Exception as e:
        pytest.fail(f"test_graph_execution_flow 失败: {str(e)}")


def test_graph_preserves_original_messages(sample_state: AgentState) -> None:
    """测试图执行不会丢失原始消息（累加语义）"""
    try:
        # 准备
        graph = create_agent_graph()

        # 执行
        final_state = graph.invoke(sample_state)

        # 验证：原始消息应该保留
        assert final_state["messages"][0].content == "测试任务"
        assert isinstance(final_state["messages"][0], HumanMessage)
    except Exception as e:
        pytest.fail(f"test_graph_preserves_original_messages 失败: {str(e)}")


# ============================================================================
# 性能测试
# ============================================================================
def test_graph_execution_performance(sample_state: AgentState) -> None:
    """测试图执行的性能（应该在合理时间内完成）"""
    try:
        graph = create_agent_graph()

        start_time = time.time()
        graph.invoke(sample_state)
        elapsed_time = time.time() - start_time

        # 验证：应该在 1 秒内完成（因为没有真实 LLM 调用）
        assert elapsed_time < 1.0, f"执行时间过长: {elapsed_time:.3f}s"
    except Exception as e:
        pytest.fail(f"test_graph_execution_performance 失败: {str(e)}")


# ============================================================================
# 边界情况测试
# ============================================================================
def test_graph_with_multiple_initial_messages() -> None:
    """测试图能处理多条初始消息"""
    try:
        # 准备
        state: AgentState = {
            "messages": [
                HumanMessage(content="消息1"),
                HumanMessage(content="消息2"),
                HumanMessage(content="消息3"),
            ],
            "task_completed": False,
        }
        graph = create_agent_graph()

        # 执行
        final_state = graph.invoke(state)

        # 验证：所有消息都保留 + 1 条 AI 回复
        assert len(final_state["messages"]) == 4
        assert final_state["task_completed"] is True
    except Exception as e:
        pytest.fail(f"test_graph_with_multiple_initial_messages 失败: {str(e)}")


def test_graph_with_long_message() -> None:
    """测试图能处理长消息"""
    try:
        # 准备：创建一个很长的消息
        long_message = "测试任务 " * 1000  # 约 10000 字符
        state: AgentState = {
            "messages": [HumanMessage(content=long_message)],
            "task_completed": False,
        }
        graph = create_agent_graph()

        # 执行
        final_state = graph.invoke(state)

        # 验证：应该正常处理
        assert len(final_state["messages"]) == 2
        assert long_message in final_state["messages"][0].content
    except Exception as e:
        pytest.fail(f"test_graph_with_long_message 失败: {str(e)}")


# ============================================================================
# Mock 示例测试（如果未来集成真实 LLM）
# ============================================================================
@pytest.mark.skip(reason="示例测试：演示如何 Mock LLM 调用")
def test_agent_node_with_mocked_llm(sample_state: AgentState) -> None:
    """
    示例：演示如何 Mock LLM 调用

    如果 agent_node 中使用了真实的 LLM（如 ChatOpenAI），
    可以使用这种方式 Mock
    """
    try:
        # Mock LLM 响应
        with patch("langchain_openai.ChatOpenAI") as mock_llm_class:
            # 配置 Mock 行为
            mock_llm = MagicMock()
            mock_llm.invoke.return_value = AIMessage(content="Mocked LLM 响应")
            mock_llm_class.return_value = mock_llm

            # 执行
            result = agent_node(sample_state)

            # 验证
            assert "messages" in result
            # mock_llm.invoke.assert_called_once()  # 验证 LLM 被调用了一次
    except Exception as e:
        pytest.fail(f"test_agent_node_with_mocked_llm 失败: {str(e)}")


# ============================================================================
# 异步测试示例（如果节点函数是异步的）
# ============================================================================
@pytest.mark.asyncio
@pytest.mark.skip(reason="示例测试：演示异步测试")
async def test_async_agent_node_example() -> None:
    """
    示例：演示如何测试异步节点函数

    如果节点函数是 async def，使用 @pytest.mark.asyncio
    """
    try:
        # 准备
        state: AgentState = {  # noqa: F841
            "messages": [HumanMessage(content="异步测试")],
            "task_completed": False,
        }

        # Mock 异步 LLM 调用
        with patch("langchain_openai.ChatOpenAI") as mock_llm_class:
            mock_llm = MagicMock()
            mock_llm.ainvoke = AsyncMock(return_value=AIMessage(content="异步响应"))
            mock_llm_class.return_value = mock_llm

            # 如果 agent_node 是异步的：
            # result = await agent_node(state)
            # assert "messages" in result

            # 当前 agent_node 是同步的，这里仅作示例
    except Exception as e:
        pytest.fail(f"test_async_agent_node_example 失败: {str(e)}")
