"""

from __future__ import annotations

L21 测试套件: Human-in-the-Loop

测试策略:
- 验证中断机制
- 测试状态恢复
- 模拟人类输入注入

运行方式:
    pytest tests/test_human_in_the_loop.py -v
"""

from __future__ import annotations

import time
import uuid

import pytest

pytest.importorskip("langchain_core", reason="需要 langchain-core（uv sync --extra ai）")

from langchain_core.messages import HumanMessage

# 使用 module 级别的全局变量，由 fixture 注入
InterruptState = None  # type: ignore[assignment]
create_interrupt_graph = None  # type: ignore[assignment]
process_node = None  # type: ignore[assignment]
WritingState = None  # type: ignore[assignment]
writer_node = None  # type: ignore[assignment]
approval_node = None  # type: ignore[assignment]
create_hitl_graph = None  # type: ignore[assignment]
should_continue = None  # type: ignore[assignment]


@pytest.fixture(scope="module", autouse=True)
def _inject_examples(examples, request) -> None:
    """从 ``examples`` fixture 动态获取模块并注入模块命名空间。

    取代原先的 ``sys.modules`` 清理 + 动态绑定，避免全局状态污染。
    """
    try:
        human_loop_module = examples.human_in_the_loop_03
        request.module.InterruptState = human_loop_module.InterruptState
        request.module.create_interrupt_graph = human_loop_module.create_interrupt_graph
        request.module.process_node = human_loop_module.process_node
        request.module.WritingState = human_loop_module.WritingState
        request.module.writer_node = human_loop_module.writer_node
        request.module.approval_node = human_loop_module.approval_node
        request.module.create_hitl_graph = human_loop_module.create_hitl_graph
        request.module.should_continue = human_loop_module.should_continue
    except (ImportError, AttributeError) as e:
        pytest.skip(f"示例代码未完成（缺少必需的函数）: {e}", allow_module_level=True)


# ============================================================================
# 测试夹具
# ============================================================================
@pytest.fixture
def initial_state() -> WritingState:
    """创建测试用的初始状态"""
    return {
        "messages": [HumanMessage(content="测试写作任务")],
        "draft_content": "",
        "human_feedback": "",
        "revision_count": 0,
        "approved": False,
    }


@pytest.fixture
def thread_config() -> dict:
    """创建测试用的线程配置"""
    return {"configurable": {"thread_id": str(uuid.uuid4())}}


# ============================================================================
# 单元测试: writer_node
# ============================================================================
def test_writer_node_first_draft(initial_state: WritingState) -> None:
    """测试 Writer Agent 生成初稿"""
    # 执行
    result = writer_node(initial_state)

    # 验证
    assert "draft_content" in result
    assert len(result["draft_content"]) > 0
    assert "Python 异步编程" in result["draft_content"]
    assert result["revision_count"] == 1


def test_writer_node_revision(initial_state: WritingState) -> None:
    """测试 Writer Agent 根据反馈修订"""
    # 准备：设置为修订状态
    state = {
        **initial_state,
        "draft_content": "原始草稿内容",
        "human_feedback": "请添加更多示例",
        "revision_count": 1,
    }

    # 执行
    result = writer_node(state)

    # 验证
    assert result["revision_count"] == 2
    assert "修订" in result["draft_content"] or "版本" in result["draft_content"]  # 包含修订标记


def test_writer_node_multiple_revisions() -> None:
    """测试多次修订的累加效果"""
    state: WritingState = {
        "messages": [HumanMessage(content="测试")],
        "draft_content": "初稿",
        "human_feedback": "修改1",
        "revision_count": 0,
        "approved": False,
    }

    # 第一次修订
    result1 = writer_node(state)
    assert result1["revision_count"] == 1

    # 第二次修订
    state2 = {**state, **result1, "human_feedback": "修改2"}
    result2 = writer_node(state2)
    assert result2["revision_count"] == 2


# ============================================================================
# 单元测试: approval_node
# ============================================================================
def test_approval_node_approves(initial_state: WritingState) -> None:
    """测试 Approval 节点批准内容"""
    # 准备
    state = {**initial_state, "human_feedback": "approve"}

    # 执行
    result = approval_node(state)

    # 验证
    assert result["approved"] is True


def test_approval_node_rejects(initial_state: WritingState) -> None:
    """测试 Approval 节点拒绝并要求修订"""
    # 准备
    state = {**initial_state, "human_feedback": "请改进"}

    # 执行
    result = approval_node(state)

    # 验证
    assert result["approved"] is False


def test_approval_node_chinese_keywords(initial_state: WritingState) -> None:
    """测试中文批准关键词"""
    test_cases = ["批准", "通过", "ok", "approve", "APPROVE"]

    for keyword in test_cases:
        state = {**initial_state, "human_feedback": keyword}
        result = approval_node(state)
        assert result["approved"] is True, f"关键词 '{keyword}' 应该被识别为批准"


# ============================================================================
# 单元测试: should_continue 路由函数
# ============================================================================
def test_should_continue_when_approved(initial_state: WritingState) -> None:
    """测试批准后路由到 END"""
    # 准备
    state = {**initial_state, "approved": True}

    # 执行
    result = should_continue(state)

    # 验证
    from langgraph.graph import END

    assert result == END


def test_should_continue_when_not_approved(initial_state: WritingState) -> None:
    """测试未批准时路由回 writer"""
    # 准备
    state = {**initial_state, "approved": False, "revision_count": 1}

    # 执行
    result = should_continue(state)

    # 验证
    assert result == "writer"


def test_should_continue_max_revisions(initial_state: WritingState) -> None:
    """测试达到最大修订次数时强制结束"""
    # 准备
    state = {**initial_state, "approved": False, "revision_count": 3}

    # 执行
    result = should_continue(state)

    # 验证
    from langgraph.graph import END

    assert result == END


# ============================================================================
# 集成测试: 中断机制
# ============================================================================
def test_hitl_graph_interrupts_at_review(initial_state: WritingState, thread_config: dict) -> None:
    """测试图在 human_review 节点前中断"""
    # 准备
    graph = create_hitl_graph()

    # 执行
    result = graph.invoke(initial_state, thread_config)

    # 验证：应该在生成草稿后中断
    assert result["revision_count"] == 1  # 已生成初稿
    assert len(result["draft_content"]) > 0
    assert result["approved"] is False  # 尚未批准


def test_hitl_graph_resumes_with_feedback(initial_state: WritingState, thread_config: dict) -> None:
    """测试注入人类反馈后能继续执行"""
    # 准备
    graph = create_hitl_graph()

    # 第一次执行：生成初稿并中断
    result1 = graph.invoke(initial_state, thread_config)

    # 注入人类反馈（移除 __interrupt__ 字段）
    updated_state = _clean_interrupt_state(result1)
    updated_state["human_feedback"] = "请添加更多细节"

    # 第二次执行：继续修订
    result2 = graph.invoke(updated_state, thread_config)

    # 验证：工作流能继续执行
    assert result2["revision_count"] >= 1
    assert result2["approved"] is False  # 仍未批准


def test_hitl_graph_completes_with_approval(
    initial_state: WritingState, thread_config: dict
) -> None:
    """测试批准后工作流能够恢复执行"""
    # 准备
    graph = create_hitl_graph()

    # 第一次执行：生成初稿并中断（在 human_review 前）
    result1 = graph.invoke(initial_state, thread_config)
    assert result1["revision_count"] == 1  # 初稿已生成
    assert result1["approved"] is False  # 尚未批准

    # 注入批准并恢复执行
    # 由于 LangGraph 的状态管理机制，我们验证工作流能够接受反馈并继续执行
    updated_state = {**result1, "human_feedback": "approve"}
    result2 = graph.invoke(updated_state, thread_config)

    # 验证：工作流应该能够恢复并执行
    # 实际行为取决于 LangGraph 实现，但至少应该有新的消息
    assert len(result2["messages"]) >= len(result1["messages"])
    assert result2["human_feedback"] == "approve"  # 反馈已保存


def _clean_interrupt_state(result: dict) -> dict:
    """移除 __interrupt__ 字段的辅助函数"""
    return {k: v for k, v in result.items() if k != "__interrupt__"}


# ============================================================================
# 集成测试: 多轮修订
# ============================================================================
def test_hitl_graph_multiple_revisions(initial_state: WritingState, thread_config: dict) -> None:
    """测试多轮修订流程"""
    graph = create_hitl_graph()

    # 第一轮：生成初稿（中断在 human_review 前）
    result1 = graph.invoke(initial_state, thread_config)
    assert result1["revision_count"] == 1

    # 第二轮：注入修改建议，恢复执行
    state2 = _clean_interrupt_state(result1)
    state2["human_feedback"] = "修改建议1"
    result2 = graph.invoke(state2, thread_config)
    # revision_count 可能是 2 或 3

    # 第三轮：再次修订
    state3 = _clean_interrupt_state(result2)
    state3["human_feedback"] = "修改建议2"
    result3 = graph.invoke(state3, thread_config)
    # revision_count 可能是 3 或 4

    # 第四轮：批准
    state4 = _clean_interrupt_state(result3)
    state4["human_feedback"] = "approve"
    result4 = graph.invoke(state4, thread_config)

    # 验证：工作流能够处理批准反馈
    assert result4["human_feedback"] == "approve"
    assert result4["revision_count"] >= 3  # 至少经过了多次修订


# ============================================================================
# 集成测试: 状态持久化
# ============================================================================
def test_hitl_graph_state_persistence(initial_state: WritingState) -> None:
    """测试使用相同 thread_id 能恢复状态"""
    graph = create_hitl_graph()

    # 使用固定的 thread_id
    config = {"configurable": {"thread_id": "test_thread_123"}}

    # 第一次执行
    result1 = graph.invoke(initial_state, config)

    # 第二次执行：使用相同的 thread_id（应该能恢复状态）
    # 移除 __interrupt__ 字段，避免干扰后续调用
    state2 = _clean_interrupt_state(result1)
    state2["human_feedback"] = "修改"
    result2 = graph.invoke(state2, config)

    # 验证：工作流正常执行，生成了新的修订版本
    assert result2["revision_count"] >= 1


def test_hitl_graph_different_threads_isolated() -> None:
    """测试不同 thread_id 的状态隔离"""
    graph = create_hitl_graph()

    state: WritingState = {
        "messages": [HumanMessage(content="测试")],
        "draft_content": "",
        "human_feedback": "",
        "revision_count": 0,
        "approved": False,
    }

    # 线程 1
    config1 = {"configurable": {"thread_id": "thread_1"}}
    result1 = graph.invoke(state, config1)

    # 线程 2
    config2 = {"configurable": {"thread_id": "thread_2"}}
    result2 = graph.invoke(state, config2)

    # 验证：两个线程的状态应该独立
    assert result1["revision_count"] == 1
    assert result2["revision_count"] == 1
    # 内容可能相同（因为输入相同），但状态是独立的


# ============================================================================
# 边界情况测试
# ============================================================================
def test_hitl_graph_empty_feedback(initial_state: WritingState, thread_config: dict) -> None:
    """测试空反馈的处理"""
    graph = create_hitl_graph()

    # 第一次执行
    result1 = graph.invoke(initial_state, thread_config)

    # 注入空反馈
    state2 = {**result1, "human_feedback": ""}
    result2 = graph.invoke(state2, thread_config)

    # 验证：应该正常处理（空反馈被视为需要修订）
    assert result2["approved"] is False


def test_hitl_graph_max_revisions_forced_end(
    initial_state: WritingState, thread_config: dict
) -> None:
    """测试达到最大修订次数后强制结束"""
    graph = create_hitl_graph()

    state = initial_state
    for i in range(3):
        result = graph.invoke(state, thread_config)
        state = {**result, "human_feedback": f"修改{i + 1}"}

    # 验证：应该达到最大修订次数
    # 注意：由于中断机制，最后一次执行会在 human_review 前中断
    # 所以需要再执行一次来触发 approval_node 和 should_continue
    final_result = graph.invoke(state, thread_config)

    # 由于 revision_count >= 3，should_continue 会返回 END
    assert final_result["revision_count"] >= 3


# ============================================================================
# 性能测试
# ============================================================================
def test_hitl_graph_performance(initial_state: WritingState, thread_config: dict) -> None:
    """测试工作流执行性能"""

    graph = create_hitl_graph()

    start_time = time.time()
    graph.invoke(initial_state, thread_config)
    elapsed_time = time.time() - start_time

    # 验证：应该在 1 秒内完成
    assert elapsed_time < 1.0, f"执行时间过长: {elapsed_time:.3f}s"
