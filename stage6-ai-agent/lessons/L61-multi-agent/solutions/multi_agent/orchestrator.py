"""

from __future__ import annotations

L21: LangGraph 状态机编排

使用 LangGraph 的 StateGraph 实现层级化多 Agent 协同编排
"""

from __future__ import annotations

from typing import Any, Literal

from .agents import (
    AgentRole,
    AgentState,
    SupervisorAgent,
    TaskStatus,
)
from langgraph.graph import END, StateGraph
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from .workers import DataAnalystAgent, KnowledgeAgent

tracer = trace.get_tracer(__name__)


# ============================================================================
# 多 Agent 编排器
# ============================================================================


class MultiAgentOrchestrator:
    """
    多 Agent 协同编排器

    使用 LangGraph StateGraph 实现层级化编排：
    1. Supervisor 拆解任务并分配
    2. Workers 并行执行任务
    3. Supervisor 聚合结果并决策下一步
    """

    def __init__(self):
        # 初始化 Agents
        self.supervisor = SupervisorAgent()
        self.data_analyst = DataAnalystAgent()
        self.knowledge_agent = KnowledgeAgent()

        # Worker 注册表（注册模式：解耦角色路由逻辑）
        self.worker_registry: dict[AgentRole, Any] = {
            AgentRole.DATA_ANALYST: self.data_analyst,
            AgentRole.KNOWLEDGE: self.knowledge_agent,
        }

        # 构建状态图
        self.graph = self._build_graph()

    def register_worker(self, role: AgentRole, worker: Any) -> None:
        """动态注册新的 Worker（支持运行时扩展）。

        Args:
            role: Worker 角色
            worker: Worker 实例

        Example:
            >>> orchestrator = MultiAgentOrchestrator()
            >>> new_worker = ResearcherAgent()
            >>> orchestrator.register_worker(AgentRole.RESEARCHER, new_worker)
        """
        try:
            self.worker_registry[role] = worker
        except Exception as e:
            raise RuntimeError(f"Failed to register worker for role {role}: {str(e)}") from e

    def unregister_worker(self, role: AgentRole) -> None:
        """取消注册 Worker。

        Args:
            role: 要移除的 Worker 角色
        """
        try:
            self.worker_registry.pop(role, None)
        except Exception as e:
            raise RuntimeError(f"Failed to unregister worker for role {role}: {str(e)}") from e

    def _build_graph(self) -> StateGraph:
        """构建 LangGraph 状态图"""

        try:
            # 创建状态图
            workflow = StateGraph(AgentState)

            # 添加节点
            workflow.add_node("plan_tasks", self._plan_tasks_node)
            workflow.add_node("delegate_task", self._delegate_task_node)
            workflow.add_node("execute_workers", self._execute_workers_node)
            workflow.add_node("aggregate_results", self._aggregate_results_node)

            # 设置入口点
            workflow.set_entry_point("plan_tasks")

            # 添加边
            workflow.add_edge("plan_tasks", "delegate_task")
            workflow.add_edge("delegate_task", "execute_workers")
            workflow.add_edge("execute_workers", "aggregate_results")

            # 条件边：决定是否继续或结束
            workflow.add_conditional_edges(
                "aggregate_results",
                self._should_continue,
                {
                    "continue": "delegate_task",  # 继续执行下一个任务
                    "finish": END,  # 结束并返回结果
                },
            )

            return workflow.compile()
        except Exception as e:
            raise RuntimeError(f"Failed to build graph: {str(e)}") from e

    async def _plan_tasks_node(self, state: AgentState) -> AgentState:
        """节点 1: 任务规划"""

        with tracer.start_as_current_span("node_plan_tasks") as span:
            try:
                span.set_attribute("user_query", state["user_query"])

                # Supervisor 拆解任务
                task_plan = await self.supervisor.plan_tasks(
                    user_query=state["user_query"], state=state
                )

                # 更新状态
                state["task_plan"] = task_plan
                state["current_task_index"] = 0
                state["status"] = TaskStatus.IN_PROGRESS
                state["messages"] = []
                state["tool_results"] = {}

                span.set_attribute("tasks_count", len(task_plan))
                span.add_event("tasks_planned", {"tasks": str(task_plan)})

                return state
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                state["error"] = f"Task planning failed: {str(e)}"
                state["status"] = TaskStatus.FAILED
                return state

    async def _delegate_task_node(self, state: AgentState) -> AgentState:
        """节点 2: 任务委派"""

        with tracer.start_as_current_span("node_delegate_task") as span:
            try:
                current_index = state["current_task_index"]
                task_plan = state["task_plan"]

                if current_index >= len(task_plan):
                    span.add_event("no_more_tasks")
                    return state

                # 获取当前任务
                current_task = task_plan[current_index]

                span.set_attribute("task_id", current_task["task_id"])
                span.set_attribute("target_agent", current_task["agent"])

                # Supervisor 委派任务
                message = await self.supervisor.delegate_task(task=current_task, state=state)

                # 保存消息
                state["messages"].append(message)
                state["current_message"] = message

                span.add_event(
                    "task_delegated",
                    {"message_id": message.message_id, "to_agent": message.to_agent},
                )

                return state
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                state["error"] = f"Task delegation failed: {str(e)}"
                state["status"] = TaskStatus.FAILED
                return state

    async def _execute_workers_node(self, state: AgentState) -> AgentState:
        """节点 3: Worker 执行"""

        with tracer.start_as_current_span("node_execute_workers") as span:
            try:
                current_message = state.get("current_message")

                if not current_message:
                    span.add_event("no_current_message")
                    return state

                target_agent_role = current_message.to_agent

                span.set_attribute("target_agent", target_agent_role)

                # 路由到对应的 Worker（使用注册表，符合开闭原则）
                worker = self.worker_registry.get(target_agent_role)
                if worker is None:
                    span.set_status(Status(StatusCode.ERROR))
                    state["error"] = f"Unknown agent: {target_agent_role}"
                    span.add_event(
                        "worker_not_found",
                        {
                            "target_agent": target_agent_role,
                            "available_workers": list(self.worker_registry.keys()),
                        },
                    )
                    return state

                # Worker 处理消息
                try:
                    response_message = await worker.process_message(
                        message=current_message, state=state
                    )

                    # 保存响应消息
                    state["messages"].append(response_message)

                    # Supervisor 处理 Worker 的响应
                    await self.supervisor.process_message(message=response_message, state=state)

                    span.add_event(
                        "worker_executed",
                        {
                            "worker": target_agent_role,
                            "response_type": response_message.message_type,
                        },
                    )

                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(e)

                    state["error"] = f"Worker execution failed: {str(e)}"
                    state["status"] = TaskStatus.FAILED

                return state
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                state["error"] = f"Worker execution node failed: {str(e)}"
                state["status"] = TaskStatus.FAILED
                return state

    async def _aggregate_results_node(self, state: AgentState) -> AgentState:
        """节点 4: 结果聚合"""

        with tracer.start_as_current_span("node_aggregate_results") as span:
            try:
                # 增加任务索引
                state["current_task_index"] += 1

                # 增加迭代计数
                state["iteration_count"] = state.get("iteration_count", 0) + 1

                span.set_attribute("current_index", state["current_task_index"])
                span.set_attribute("iteration_count", state["iteration_count"])

                # 检查是否所有任务完成
                if state["current_task_index"] >= len(state["task_plan"]):
                    # Supervisor 聚合所有结果
                    final_answer = await self.supervisor.aggregate_results(state)

                    state["final_answer"] = final_answer
                    state["status"] = TaskStatus.COMPLETED

                    span.add_event(
                        "all_tasks_completed", {"final_answer_length": len(final_answer)}
                    )

                return state
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                state["error"] = f"Result aggregation failed: {str(e)}"
                state["status"] = TaskStatus.FAILED
                return state

    async def _should_continue(self, state: AgentState) -> Literal["continue", "finish"]:
        """条件判断：是否继续执行"""

        with tracer.start_as_current_span("should_continue") as span:
            try:
                decision = await self.supervisor.decide_next_action(state)

                span.set_attribute("decision", decision)
                span.add_event("decision_made", {"decision": decision})

                return decision
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                return "finish"  # 出错时选择结束流程

    async def run(self, user_query: str, trace_id: str | None = None) -> dict[str, Any]:
        """
        运行多 Agent 协同流程

        Args:
            user_query: 用户查询
            trace_id: 追踪 ID（可选）

        Returns:
            执行结果
        """

        with tracer.start_as_current_span(
            "multi_agent_orchestrator_run", attributes={"user_query": user_query}
        ) as span:
            try:
                # 初始化状态
                initial_state: AgentState = {
                    "user_query": user_query,
                    "task_id": f"task_{span.get_span_context().span_id:016x}",
                    "task_plan": [],
                    "current_task_index": 0,
                    "messages": [],
                    "current_message": None,
                    "tool_results": {},
                    "final_answer": None,
                    "status": TaskStatus.PENDING,
                    "error": None,
                    "trace_id": trace_id or f"{span.get_span_context().trace_id:032x}",
                    "iteration_count": 0,
                }

                try:
                    # 执行状态图
                    final_state = await self.graph.ainvoke(initial_state)

                    span.set_attribute("status", final_state["status"])
                    span.set_attribute("iterations", final_state["iteration_count"])

                    # 构建返回结果
                    result = {
                        "success": final_state["status"] == TaskStatus.COMPLETED,
                        "final_answer": final_state.get("final_answer"),
                        "task_id": final_state["task_id"],
                        "trace_id": final_state["trace_id"],
                        "iterations": final_state["iteration_count"],
                        "tasks_executed": final_state["current_task_index"],
                        "total_tasks": len(final_state["task_plan"]),
                        "error": final_state.get("error"),
                        "tool_results": final_state.get("tool_results", {}),
                    }

                    if result["success"]:
                        span.add_event("execution_succeeded")
                    else:
                        span.set_status(Status(StatusCode.ERROR))
                        span.add_event("execution_failed", {"error": result["error"]})

                    return result

                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(e)

                    return {
                        "success": False,
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "task_id": initial_state["task_id"],
                        "trace_id": initial_state["trace_id"],
                    }
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)

                return {
                    "success": False,
                    "error": f"Orchestrator run failed: {str(e)}",
                    "error_type": type(e).__name__,
                    "task_id": f"task_{span.get_span_context().span_id:016x}",
                    "trace_id": trace_id or f"{span.get_span_context().trace_id:032x}",
                }


# ============================================================================
# 简化的运行接口
# ============================================================================


async def run_multi_agent_query(user_query: str, trace_id: str | None = None) -> dict[str, Any]:
    """
    简化的多 Agent 查询接口

    Args:
        user_query: 用户查询
        trace_id: 追踪 ID（可选）

    Returns:
        执行结果

    Example:
        >>> result = await run_multi_agent_query("分析销售数据并检索相关知识")
        >>> print(result["final_answer"])
    """

    try:
        orchestrator = MultiAgentOrchestrator()
        return await orchestrator.run(user_query, trace_id)
    except Exception as e:
        return {
            "success": False,
            "error": f"Multi-agent query failed: {str(e)}",
            "error_type": type(e).__name__,
            "task_id": None,
            "trace_id": trace_id,
        }


# ============================================================================
# 文件信息
# ============================================================================

__all__ = [
    "MultiAgentOrchestrator",
    "run_multi_agent_query",
]
