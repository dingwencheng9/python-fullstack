"""

from __future__ import annotations

L57: 多 Agent 协同编排 - 单元测试

测试多 Agent 系统的各个组件
"""

import pytest

# 依赖检查
try:
    pytest.importorskip(
        "opentelemetry", reason="需要 opentelemetry/langchain（uv sync --extra ai）"
    )
    pytest.importorskip("langgraph", reason="需要 langgraph（uv sync --extra ai）")
except Exception as e:
    print(f"Error checking required dependencies: {e}")
    import sys

    sys.exit(1)

# 使用 module 级别的全局变量，由 fixture 注入
AgentMessage = None  # type: ignore[assignment]
AgentRole = None  # type: ignore[assignment]
MessageType = None  # type: ignore[assignment]
SupervisorAgent = None  # type: ignore[assignment]
TaskStatus = None  # type: ignore[assignment]
MultiAgentOrchestrator = None  # type: ignore[assignment]
DataAnalystAgent = None  # type: ignore[assignment]
KnowledgeAgent = None  # type: ignore[assignment]


@pytest.fixture(autouse=True)
def _inject_solutions(solutions, request) -> None:
    """从 solutions 模块动态注入被测类，避免静态导入。

    取代原先顶层的 ``sys.path.insert`` + 静态导入，避免依赖 sys.path 注入。
    测试体保持原样，运行时通过模块全局名解析。
    """
    try:
        agents_module = solutions.multi_agent.agents
        orchestrator_module = solutions.multi_agent.orchestrator
        workers_module = solutions.multi_agent.workers

        request.module.AgentMessage = agents_module.AgentMessage
        request.module.AgentRole = agents_module.AgentRole
        request.module.MessageType = agents_module.MessageType
        request.module.SupervisorAgent = agents_module.SupervisorAgent
        request.module.TaskStatus = agents_module.TaskStatus
        request.module.MultiAgentOrchestrator = orchestrator_module.MultiAgentOrchestrator
        request.module.DataAnalystAgent = workers_module.DataAnalystAgent
        request.module.KnowledgeAgent = workers_module.KnowledgeAgent
    except (AttributeError, ImportError) as e:
        print(f"Error importing required modules: {e}")
        import sys
        sys.exit(1)


# ============================================================================
# 测试 Agent 消息协议
# ============================================================================


class TestAgentMessage:
    """测试 Agent 消息协议"""

    def test_message_creation(self):
        """测试消息创建"""
        try:
            message = AgentMessage(
                message_type=MessageType.TASK_ASSIGNMENT,
                from_agent=AgentRole.SUPERVISOR,
                to_agent=AgentRole.DATA_ANALYST,
                context={"user_query": "test"},
                payload={"action": "analyze"},
            )

            assert message.message_type == MessageType.TASK_ASSIGNMENT
            assert message.from_agent == AgentRole.SUPERVISOR
            assert message.to_agent == AgentRole.DATA_ANALYST
            assert message.message_id.startswith("msg_")
            assert message.timestamp is not None
        except Exception as e:
            pytest.fail(f"test_message_creation failed: {str(e)}")

    def test_message_serialization(self):
        """测试消息序列化"""
        try:
            message = AgentMessage(
                message_type=MessageType.RESULT_REPORT,
                from_agent=AgentRole.DATA_ANALYST,
                to_agent=AgentRole.SUPERVISOR,
                context={},
                payload={"result": {"data": "test"}},
            )

            # 序列化为 JSON
            json_str = message.model_dump_json()
            assert "message_type" in json_str
            assert "result_report" in json_str

            # 反序列化
            message_dict = message.model_dump()
            restored = AgentMessage(**message_dict)
            assert restored.message_id == message.message_id
        except Exception as e:
            pytest.fail(f"test_message_serialization failed: {str(e)}")


# ============================================================================
# 测试 Supervisor Agent
# ============================================================================


class TestSupervisorAgent:
    """测试 Supervisor Agent"""

    @pytest.fixture
    def supervisor(self):
        try:
            return SupervisorAgent()
        except Exception as e:
            pytest.fail(f"Failed to create SupervisorAgent fixture: {str(e)}")

    @pytest.fixture
    def sample_state(self):
        return {
            "user_query": "分析销售数据",
            "task_id": "test_task",
            "task_plan": [],
            "current_task_index": 0,
            "messages": [],
            "current_message": None,
            "tool_results": {},
            "final_answer": None,
            "status": TaskStatus.PENDING,
            "error": None,
            "trace_id": "test_trace",
            "iteration_count": 0,
        }

    @pytest.mark.asyncio
    async def test_plan_tasks_data_analysis(self, supervisor, sample_state):
        """测试数据分析任务规划"""
        try:
            tasks = await supervisor.plan_tasks("分析销售数据", sample_state)

            assert len(tasks) > 0
            assert any(task["agent"] == AgentRole.DATA_ANALYST for task in tasks)
        except Exception as e:
            pytest.fail(f"test_plan_tasks_data_analysis failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_plan_tasks_knowledge_search(self, supervisor, sample_state):
        """测试知识检索任务规划"""
        try:
            tasks = await supervisor.plan_tasks("查询 Python 文档", sample_state)

            assert len(tasks) > 0
            assert any(task["agent"] == AgentRole.KNOWLEDGE for task in tasks)
        except Exception as e:
            pytest.fail(f"test_plan_tasks_knowledge_search failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_plan_tasks_hybrid(self, supervisor, sample_state):
        """测试混合任务规划"""
        try:
            tasks = await supervisor.plan_tasks("分析数据并检索知识", sample_state)

            assert len(tasks) >= 2
            agent_types = {task["agent"] for task in tasks}
            assert AgentRole.DATA_ANALYST in agent_types
            assert AgentRole.KNOWLEDGE in agent_types
        except Exception as e:
            pytest.fail(f"test_plan_tasks_hybrid failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_delegate_task(self, supervisor, sample_state):
        """测试任务委派"""
        try:
            task = {
                "task_id": "task_001",
                "agent": AgentRole.DATA_ANALYST,
                "action": "analyze_data",
                "description": "测试任务",
                "priority": "high",
            }

            message = await supervisor.delegate_task(task, sample_state)

            assert message.message_type == MessageType.TASK_ASSIGNMENT
            assert message.from_agent == AgentRole.SUPERVISOR
            assert message.to_agent == AgentRole.DATA_ANALYST
            assert message.payload["action"] == "analyze_data"
        except Exception as e:
            pytest.fail(f"test_delegate_task failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_aggregate_results(self, supervisor, sample_state):
        """测试结果聚合"""
        try:
            sample_state["tool_results"] = {
                "data_analyst": {"summary": "数据分析完成", "data": {"total": 1000}},
                "knowledge": {"summary": "检索到 3 个文档", "results": []},
            }

            final_answer = await supervisor.aggregate_results(sample_state)

            assert "data_analyst" in final_answer
            assert "knowledge" in final_answer
            assert "数据分析完成" in final_answer
            assert "检索到 3 个文档" in final_answer
        except Exception as e:
            pytest.fail(f"test_aggregate_results failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_decide_next_action_continue(self, supervisor, sample_state):
        """测试决策：继续执行"""
        try:
            sample_state["task_plan"] = [{"task_id": "task_001"}, {"task_id": "task_002"}]
            sample_state["current_task_index"] = 0

            decision = await supervisor.decide_next_action(sample_state)

            assert decision == "continue"
        except Exception as e:
            pytest.fail(f"test_decide_next_action_continue failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_decide_next_action_finish(self, supervisor, sample_state):
        """测试决策：完成"""
        try:
            sample_state["task_plan"] = [{"task_id": "task_001"}]
            sample_state["current_task_index"] = 1

            decision = await supervisor.decide_next_action(sample_state)

            assert decision == "finish"
        except Exception as e:
            pytest.fail(f"test_decide_next_action_finish failed: {str(e)}")


# ============================================================================
# 测试 DataAnalyst Agent
# ============================================================================


class TestDataAnalystAgent:
    """测试 DataAnalyst Agent"""

    @pytest.fixture
    def data_analyst(self):
        try:
            return DataAnalystAgent()
        except Exception as e:
            pytest.fail(f"Failed to create DataAnalystAgent fixture: {str(e)}")

    @pytest.fixture
    def sample_message(self):
        return AgentMessage(
            message_type=MessageType.TASK_ASSIGNMENT,
            from_agent=AgentRole.SUPERVISOR,
            to_agent=AgentRole.DATA_ANALYST,
            context={"user_query": "分析销售数据"},
            payload={"action": "analyze_data", "parameters": {}},
        )

    @pytest.fixture
    def sample_state(self):
        return {
            "user_query": "分析销售数据",
            "task_id": "test_task",
            "task_plan": [],
            "current_task_index": 0,
            "messages": [],
            "current_message": None,
            "tool_results": {},
            "final_answer": None,
            "status": TaskStatus.PENDING,
            "error": None,
            "trace_id": "test_trace",
            "iteration_count": 0,
        }

    @pytest.mark.asyncio
    async def test_process_task_assignment(self, data_analyst, sample_message, sample_state):
        """测试处理任务分配消息"""
        try:
            response = await data_analyst.process_message(sample_message, sample_state)

            assert response.message_type == MessageType.RESULT_REPORT
            assert response.from_agent == AgentRole.DATA_ANALYST
            assert response.to_agent == AgentRole.SUPERVISOR
            assert response.payload["success"] is True
            assert "result" in response.payload
        except Exception as e:
            pytest.fail(f"test_process_task_assignment failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_analyze_sales_data(self, data_analyst, sample_message, sample_state):
        """测试销售数据分析"""
        try:
            response = await data_analyst.process_message(sample_message, sample_state)

            result = response.payload["result"]
            assert "statistics" in result
            assert "summary" in result
            assert result["statistics"]["total_sales"] > 0
        except Exception as e:
            pytest.fail(f"test_analyze_sales_data failed: {str(e)}")


# ============================================================================
# 测试 Knowledge Agent
# ============================================================================


class TestKnowledgeAgent:
    """测试 Knowledge Agent"""

    @pytest.fixture
    def knowledge_agent(self):
        try:
            return KnowledgeAgent()
        except Exception as e:
            pytest.fail(f"Failed to create KnowledgeAgent fixture: {str(e)}")

    @pytest.fixture
    def sample_message(self):
        return AgentMessage(
            message_type=MessageType.TASK_ASSIGNMENT,
            from_agent=AgentRole.SUPERVISOR,
            to_agent=AgentRole.KNOWLEDGE,
            context={"user_query": "查询 Python 文档"},
            payload={"action": "search_knowledge", "parameters": {}},
        )

    @pytest.fixture
    def sample_state(self):
        return {
            "user_query": "查询 Python 文档",
            "task_id": "test_task",
            "task_plan": [],
            "current_task_index": 0,
            "messages": [],
            "current_message": None,
            "tool_results": {},
            "final_answer": None,
            "status": TaskStatus.PENDING,
            "error": None,
            "trace_id": "test_trace",
            "iteration_count": 0,
        }

    @pytest.mark.asyncio
    async def test_process_task_assignment(self, knowledge_agent, sample_message, sample_state):
        """测试处理任务分配消息"""
        try:
            response = await knowledge_agent.process_message(sample_message, sample_state)

            assert response.message_type == MessageType.RESULT_REPORT
            assert response.from_agent == AgentRole.KNOWLEDGE
            assert response.to_agent == AgentRole.SUPERVISOR
            assert response.payload["success"] is True
            assert "result" in response.payload
        except Exception as e:
            pytest.fail(f"test_process_task_assignment failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_search_knowledge_base(self, knowledge_agent, sample_message, sample_state):
        """测试知识库检索"""
        try:
            response = await knowledge_agent.process_message(sample_message, sample_state)

            result = response.payload["result"]
            assert "results" in result
            assert "result_count" in result
            assert "summary" in result
            assert result["result_count"] > 0
        except Exception as e:
            pytest.fail(f"test_search_knowledge_base failed: {str(e)}")


# ============================================================================
# 测试 MultiAgentOrchestrator
# ============================================================================


class TestMultiAgentOrchestrator:
    """测试多 Agent 编排器"""

    @pytest.fixture
    def orchestrator(self):
        try:
            return MultiAgentOrchestrator()
        except Exception as e:
            pytest.fail(f"Failed to create MultiAgentOrchestrator fixture: {str(e)}")

    @pytest.mark.asyncio
    async def test_run_data_analysis_query(self, orchestrator):
        """测试数据分析查询"""
        try:
            result = await orchestrator.run("分析销售数据")

            assert result["success"] is True
            assert isinstance(result["final_answer"], str) and result["final_answer"].strip()
            assert result["tasks_executed"] >= 1
            assert result["tasks_executed"] <= result["total_tasks"]
            assert "data_analyst" in result["tool_results"]
            analyst_payload = result["tool_results"]["data_analyst"]
            assert isinstance(analyst_payload, dict)
            assert "summary" in analyst_payload
        except Exception as e:
            pytest.fail(f"test_run_data_analysis_query failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_run_knowledge_search_query(self, orchestrator):
        """测试知识检索查询"""
        try:
            result = await orchestrator.run("查询 Python 文档")

            assert result["success"] is True
            assert isinstance(result["final_answer"], str) and result["final_answer"].strip()
            assert result["tasks_executed"] >= 1
            assert "knowledge" in result["tool_results"]
            knowledge_payload = result["tool_results"]["knowledge"]
            assert isinstance(knowledge_payload, dict)
            assert "results" in knowledge_payload or "summary" in knowledge_payload
        except Exception as e:
            pytest.fail(f"test_run_knowledge_search_query failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_run_hybrid_query(self, orchestrator):
        """测试混合查询：两个 agent 都被调度。"""
        try:
            result = await orchestrator.run("分析数据并检索知识")

            assert result["success"] is True
            assert isinstance(result["final_answer"], str) and result["final_answer"].strip()
            assert result["tasks_executed"] >= 2
            assert {"data_analyst", "knowledge"}.issubset(result["tool_results"].keys())
        except Exception as e:
            pytest.fail(f"test_run_hybrid_query failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_trace_propagation(self, orchestrator):
        """测试追踪上下文传播"""
        try:
            result = await orchestrator.run("测试追踪", trace_id="custom_trace_123")

            assert result["trace_id"] == "custom_trace_123"
        except Exception as e:
            pytest.fail(f"test_trace_propagation failed: {str(e)}")


# ============================================================================
# 运行测试
# ============================================================================

if __name__ == "__main__":
    try:
        pytest.main([__file__, "-v", "--tb=short"])
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        sys.exit(1)
