"""

from __future__ import annotations

L21: 多 Agent 协同编排 - 核心架构定义

本模块实现了一个完整的多 Agent 协同体系，包括：
1. Supervisor Agent - 任务全局拆解与协调
2. DataAnalyst Agent - Pandas 数据分析专家
3. Knowledge Agent - 向量检索与知识管理

技术栈:
- LangGraph: 状态机编排
- OpenTelemetry: 分布式追踪
- Redis: Agent 间通信
- PostgreSQL: 任务持久化
"""

from abc import ABC, abstractmethod
from datetime import datetime, UTC
from enum import StrEnum
import json
from typing import Any, Literal, TypedDict
import uuid

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from pydantic import BaseModel, ConfigDict, Field

# ============================================================================
# 消息传递协议定义
# ============================================================================


class MessageType(StrEnum):
    """Agent 间消息类型"""

    TASK_ASSIGNMENT = "task_assignment"  # 任务分配
    TOOL_EXECUTION = "tool_execution"  # 工具执行
    RESULT_REPORT = "result_report"  # 结果报告
    STATUS_UPDATE = "status_update"  # 状态更新
    ERROR_REPORT = "error_report"  # 错误报告


class AgentRole(StrEnum):
    """Agent 角色类型"""

    SUPERVISOR = "supervisor"  # 监督者
    DATA_ANALYST = "data_analyst"  # 数据分析师
    KNOWLEDGE = "knowledge"  # 知识专家


class TaskStatus(StrEnum):
    """任务状态"""

    PENDING = "pending"  # 待处理
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    DELEGATED = "delegated"  # 已委派


class AgentMessage(BaseModel):
    """Agent 间消息协议 - JSON-based Messaging"""

    message_id: str = Field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:8]}")
    message_type: MessageType

    # 发送方和接收方
    from_agent: AgentRole
    to_agent: AgentRole

    # 上下文和内容
    context: dict[str, Any] = Field(default_factory=dict)
    payload: dict[str, Any] = Field(default_factory=dict)

    # 追踪信息
    trace_id: str | None = None
    span_id: str | None = None
    parent_span_id: str | None = None

    # 时间戳
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message_type": "task_assignment",
                "from_agent": "supervisor",
                "to_agent": "data_analyst",
                "context": {"user_query": "分析销售数据", "task_id": "task_001"},
                "payload": {"task": "analyze_sales_data", "parameters": {"file_path": "sales.csv"}},
            }
        }
    )


# ============================================================================
# 状态机状态定义
# ============================================================================


class AgentState(TypedDict):
    """多 Agent 协同状态"""

    # 用户输入
    user_query: str

    # 任务管理
    task_id: str
    task_plan: list[dict[str, Any]]  # 任务拆解计划
    current_task_index: int

    # Agent 通信
    messages: list[AgentMessage]  # 消息历史
    current_message: AgentMessage | None

    # 工具执行结果
    tool_results: dict[str, Any]  # {agent_role: result}

    # 最终输出
    final_answer: str | None

    # 状态控制
    status: TaskStatus
    error: str | None

    # 追踪信息
    trace_id: str
    iteration_count: int


# ============================================================================
# Agent 基类定义
# ============================================================================

tracer = trace.get_tracer(__name__)


class BaseAgent(ABC):
    """Agent 基类"""

    def __init__(self, role: AgentRole, agent_id: str):
        self.role = role
        self.agent_id = agent_id
        self.status = "idle"

    @abstractmethod
    async def process_message(self, message: AgentMessage, state: AgentState) -> AgentMessage:
        """处理接收到的消息"""

    def create_message(
        self,
        message_type: MessageType,
        to_agent: AgentRole,
        context: dict[str, Any],
        payload: dict[str, Any],
        trace_context: dict[str, str] | None = None,
    ) -> AgentMessage:
        """创建消息"""

        msg = AgentMessage(
            message_type=message_type,
            from_agent=self.role,
            to_agent=to_agent,
            context=context,
            payload=payload,
        )

        # 注入追踪上下文
        if trace_context:
            msg.trace_id = trace_context.get("trace_id")
            msg.span_id = trace_context.get("span_id")
            msg.parent_span_id = trace_context.get("parent_span_id")

        return msg

    def _get_trace_context(self) -> dict[str, str]:
        """获取当前追踪上下文"""
        span = trace.get_current_span()
        if span and span.get_span_context().is_valid:
            ctx = span.get_span_context()
            return {
                "trace_id": format(ctx.trace_id, "032x"),
                "span_id": format(ctx.span_id, "016x"),
                "parent_span_id": format(ctx.span_id, "016x"),
            }
        return {}


# ============================================================================
# Supervisor Agent - 任务全局拆解与协调
# ============================================================================


class SupervisorAgent(BaseAgent):
    """
    Supervisor Agent - 主控 Agent

    职责:
    1. 接收用户查询，进行 Plan-and-Solve 模式的任务拆解
    2. 将子任务分配给专业 Worker Agent
    3. 聚合 Workers 返回的结果
    4. 决策是否继续任务或汇总输出
    """

    def __init__(self):
        super().__init__(AgentRole.SUPERVISOR, "supervisor_001")
        self.available_workers = {
            AgentRole.DATA_ANALYST: "data_analyst_001",
            AgentRole.KNOWLEDGE: "knowledge_001",
        }

    async def plan_tasks(self, user_query: str, state: AgentState) -> list[dict[str, Any]]:
        """
        Plan-and-Solve: 任务拆解

        将用户查询拆解为可执行的子任务序列
        """

        with tracer.start_as_current_span("supervisor_plan_tasks") as span:
            span.set_attribute("user_query", user_query)

            # 简化的任务拆解逻辑（生产环境应使用 LLM）
            tasks = []

            # 判断是否需要数据分析
            if any(keyword in user_query.lower() for keyword in ["分析", "统计", "数据", "报表"]):
                tasks.append(
                    {
                        "task_id": f"task_{uuid.uuid4().hex[:8]}",
                        "agent": AgentRole.DATA_ANALYST,
                        "action": "analyze_data",
                        "description": "执行数据分析",
                        "priority": "high",
                    }
                )

            # 判断是否需要知识检索
            if any(keyword in user_query.lower() for keyword in ["查询", "检索", "知识", "文档"]):
                tasks.append(
                    {
                        "task_id": f"task_{uuid.uuid4().hex[:8]}",
                        "agent": AgentRole.KNOWLEDGE,
                        "action": "search_knowledge",
                        "description": "检索相关知识",
                        "priority": "medium",
                    }
                )

            # 默认：知识检索
            if not tasks:
                tasks.append(
                    {
                        "task_id": f"task_{uuid.uuid4().hex[:8]}",
                        "agent": AgentRole.KNOWLEDGE,
                        "action": "search_knowledge",
                        "description": "检索相关知识",
                        "priority": "medium",
                    }
                )

            span.set_attribute("tasks_count", len(tasks))
            span.add_event("tasks_planned", {"tasks": json.dumps(tasks)})

            return tasks

    async def delegate_task(self, task: dict[str, Any], state: AgentState) -> AgentMessage:
        """委派任务给 Worker Agent"""

        with tracer.start_as_current_span("supervisor_delegate_task") as span:
            span.set_attribute("task_id", task["task_id"])
            span.set_attribute("target_agent", task["agent"])

            # 创建任务分配消息
            message = self.create_message(
                message_type=MessageType.TASK_ASSIGNMENT,
                to_agent=AgentRole(task["agent"]),
                context={
                    "user_query": state["user_query"],
                    "task_id": task["task_id"],
                    "task_description": task["description"],
                },
                payload={"action": task["action"], "priority": task["priority"], "parameters": {}},
                trace_context=self._get_trace_context(),
            )

            span.add_event(
                "task_delegated", {"message_id": message.message_id, "to_agent": task["agent"]}
            )

            return message

    async def aggregate_results(self, state: AgentState) -> str:
        """聚合 Workers 返回的结果"""

        with tracer.start_as_current_span("supervisor_aggregate_results") as span:
            tool_results = state.get("tool_results", {})

            span.set_attribute("results_count", len(tool_results))

            # 简化的结果聚合逻辑
            aggregated = []

            for agent_role, result in tool_results.items():
                if result and isinstance(result, dict):
                    summary = result.get("summary", str(result))
                    aggregated.append(f"[{agent_role}] {summary}")

            final_answer = "\n\n".join(aggregated) if aggregated else "未获取到有效结果"

            span.add_event("results_aggregated", {"final_answer_length": len(final_answer)})

            return final_answer

    async def decide_next_action(self, state: AgentState) -> Literal["continue", "finish"]:
        """
        决策下一步行动

        根据当前状态决定是继续执行任务还是汇总输出
        """

        with tracer.start_as_current_span("supervisor_decide_next_action") as span:
            # 检查是否还有待执行的任务
            current_index = state.get("current_task_index", 0)
            total_tasks = len(state.get("task_plan", []))

            span.set_attribute("current_index", current_index)
            span.set_attribute("total_tasks", total_tasks)

            # 检查是否有错误
            if state.get("error"):
                span.add_event("error_detected", {"error": state["error"]})
                return "finish"

            # 检查是否所有任务完成
            if current_index >= total_tasks:
                span.add_event("all_tasks_completed")
                return "finish"

            # 检查迭代次数限制（防止无限循环）
            if state.get("iteration_count", 0) > 10:
                span.add_event("max_iterations_reached")
                return "finish"

            span.add_event("continue_execution")
            return "continue"

    async def process_message(self, message: AgentMessage, state: AgentState) -> AgentMessage:
        """处理 Worker 返回的消息"""

        with tracer.start_as_current_span("supervisor_process_message") as span:
            span.set_attribute("message_id", message.message_id)
            span.set_attribute("message_type", message.message_type)
            span.set_attribute("from_agent", message.from_agent)

            # 根据消息类型处理
            if message.message_type == MessageType.RESULT_REPORT:
                # 保存 Worker 的执行结果
                agent_role = message.from_agent
                result = message.payload.get("result")

                if "tool_results" not in state:
                    state["tool_results"] = {}

                state["tool_results"][agent_role] = result

                span.add_event(
                    "result_received", {"from_agent": agent_role, "has_result": result is not None}
                )

            elif message.message_type == MessageType.ERROR_REPORT:
                # 记录错误
                error_msg = message.payload.get("error", "Unknown error")
                state["error"] = f"{message.from_agent}: {error_msg}"

                span.set_status(Status(StatusCode.ERROR))
                span.add_event("error_received", {"error": error_msg})

            # 返回确认消息
            return self.create_message(
                message_type=MessageType.STATUS_UPDATE,
                to_agent=message.from_agent,
                context={"status": "received"},
                payload={"acknowledged": True},
                trace_context=self._get_trace_context(),
            )


# ============================================================================
# 文件信息
# ============================================================================

__all__ = [
    "AgentMessage",
    "AgentRole",
    "AgentState",
    "BaseAgent",
    "MessageType",
    "SupervisorAgent",
    "TaskStatus",
]
