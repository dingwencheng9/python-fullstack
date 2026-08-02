"""

from __future__ import annotations

L21: Specialized Worker Agents

实现两个专业 Worker Agent：
1. DataAnalyst Agent - Pandas 数据分析专家
2. Knowledge Agent - 向量检索与知识管理
"""

from __future__ import annotations

from typing import Any

from .agents import (
    AgentMessage,
    AgentRole,
    AgentState,
    BaseAgent,
    MessageType,
)
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
import pandas as pd

tracer = trace.get_tracer(__name__)


# ============================================================================
# DataAnalyst Agent - Pandas 数据分析专家
# ============================================================================


class DataAnalystAgent(BaseAgent):
    """
    DataAnalyst Agent - 数据分析专家

    职责:
    1. 接收 Supervisor 分配的数据分析任务
    2. 使用 Pandas 执行数据分析
    3. 返回分析结果和摘要
    """

    def __init__(self):
        super().__init__(AgentRole.DATA_ANALYST, "data_analyst_001")
        self.capabilities = [
            "analyze_sales_data",
            "calculate_statistics",
            "generate_report",
            "data_aggregation",
        ]

    async def process_message(self, message: AgentMessage, state: AgentState) -> AgentMessage:
        """处理来自 Supervisor 的消息"""

        with tracer.start_as_current_span(
            "data_analyst_process_message",
            attributes={"message_id": message.message_id, "message_type": message.message_type},
        ) as span:
            try:
                if message.message_type == MessageType.TASK_ASSIGNMENT:
                    # 执行任务
                    action = message.payload.get("action")
                    parameters = message.payload.get("parameters", {})

                    span.set_attribute("action", action)

                    # 执行数据分析
                    result = await self._execute_analysis(action, parameters, message.context)

                    # 返回结果报告
                    return self.create_message(
                        message_type=MessageType.RESULT_REPORT,
                        to_agent=AgentRole.SUPERVISOR,
                        context=message.context,
                        payload={"result": result, "success": True},
                        trace_context=self._get_trace_context(),
                    )

                # 不支持的消息类型
                span.add_event("unsupported_message_type")
                return self.create_message(
                    message_type=MessageType.ERROR_REPORT,
                    to_agent=AgentRole.SUPERVISOR,
                    context=message.context,
                    payload={"error": f"Unsupported message type: {message.message_type}"},
                    trace_context=self._get_trace_context(),
                )

            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)

                return self.create_message(
                    message_type=MessageType.ERROR_REPORT,
                    to_agent=AgentRole.SUPERVISOR,
                    context=message.context,
                    payload={"error": str(e), "error_type": type(e).__name__},
                    trace_context=self._get_trace_context(),
                )

    async def _execute_analysis(
        self, action: str, parameters: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """执行数据分析"""

        with tracer.start_as_current_span(
            f"data_analyst_{action}", attributes={"action": action}
        ) as span:
            if action == "analyze_data":
                # 模拟数据分析
                result = await self._analyze_sales_data(parameters, context)

            elif action == "calculate_statistics":
                result = await self._calculate_statistics(parameters, context)

            elif action == "generate_report":
                result = await self._generate_report(parameters, context)

            else:
                span.add_event("unknown_action")
                result = {
                    "error": f"Unknown action: {action}",
                    "summary": f"不支持的操作: {action}",
                }

            span.set_attribute("result_keys", ",".join(result.keys()))
            return result

    async def _analyze_sales_data(
        self, parameters: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """分析销售数据"""

        with tracer.start_as_current_span("analyze_sales_data") as span:
            # 模拟数据分析（实际项目中应读取真实数据）
            # 创建示例 DataFrame
            sample_data = pd.DataFrame(
                {
                    "product": ["Product A", "Product B", "Product C"],
                    "sales": [1000, 1500, 800],
                    "profit": [200, 300, 150],
                }
            )

            # 计算统计信息
            total_sales = sample_data["sales"].sum()
            total_profit = sample_data["profit"].sum()
            avg_sales = sample_data["sales"].mean()
            top_product = sample_data.loc[sample_data["sales"].idxmax(), "product"]

            result = {
                "statistics": {
                    "total_sales": float(total_sales),
                    "total_profit": float(total_profit),
                    "average_sales": float(avg_sales),
                    "top_product": top_product,
                },
                "data": sample_data.to_dict(orient="records"),
                "summary": (
                    f"数据分析完成：总销售额 {total_sales}，"
                    f"总利润 {total_profit}，"
                    f"最佳产品 {top_product}"
                ),
            }

            span.set_attribute("total_sales", float(total_sales))
            span.set_attribute("top_product", top_product)
            span.add_event("analysis_completed", {"record_count": len(sample_data)})

            return result

    async def _calculate_statistics(
        self, parameters: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """计算统计指标"""

        with tracer.start_as_current_span("calculate_statistics") as span:
            # 模拟统计计算
            result = {
                "mean": 1100.0,
                "median": 1000.0,
                "std": 350.0,
                "min": 800.0,
                "max": 1500.0,
                "summary": "统计计算完成：平均值 1100，标准差 350",
            }

            span.add_event("statistics_calculated")
            return result

    async def _generate_report(
        self, parameters: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """生成分析报告"""

        with tracer.start_as_current_span("generate_report") as span:
            report = {
                "title": "数据分析报告",
                "sections": [
                    {"name": "概览", "content": "销售数据分析概览"},
                    {"name": "详细分析", "content": "产品销售详细分析"},
                ],
                "summary": "分析报告已生成，包含 2 个部分",
            }

            span.add_event("report_generated", {"sections_count": len(report["sections"])})

            return report


# ============================================================================
# Knowledge Agent - 向量检索与知识管理
# ============================================================================


class KnowledgeAgent(BaseAgent):
    """
    Knowledge Agent - 知识专家

    职责:
    1. 接收 Supervisor 分配的知识检索任务
    2. 执行向量检索（模拟）
    3. 返回检索结果和摘要
    """

    def __init__(self):
        super().__init__(AgentRole.KNOWLEDGE, "knowledge_001")
        self.capabilities = ["search_knowledge", "retrieve_documents", "answer_question"]

    async def process_message(self, message: AgentMessage, state: AgentState) -> AgentMessage:
        """处理来自 Supervisor 的消息"""

        with tracer.start_as_current_span(
            "knowledge_process_message",
            attributes={"message_id": message.message_id, "message_type": message.message_type},
        ) as span:
            try:
                if message.message_type == MessageType.TASK_ASSIGNMENT:
                    # 执行任务
                    action = message.payload.get("action")
                    parameters = message.payload.get("parameters", {})

                    span.set_attribute("action", action)

                    # 执行知识检索
                    result = await self._execute_search(action, parameters, message.context)

                    # 返回结果报告
                    return self.create_message(
                        message_type=MessageType.RESULT_REPORT,
                        to_agent=AgentRole.SUPERVISOR,
                        context=message.context,
                        payload={"result": result, "success": True},
                        trace_context=self._get_trace_context(),
                    )

                # 不支持的消息类型
                span.add_event("unsupported_message_type")
                return self.create_message(
                    message_type=MessageType.ERROR_REPORT,
                    to_agent=AgentRole.SUPERVISOR,
                    context=message.context,
                    payload={"error": f"Unsupported message type: {message.message_type}"},
                    trace_context=self._get_trace_context(),
                )

            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)

                return self.create_message(
                    message_type=MessageType.ERROR_REPORT,
                    to_agent=AgentRole.SUPERVISOR,
                    context=message.context,
                    payload={"error": str(e), "error_type": type(e).__name__},
                    trace_context=self._get_trace_context(),
                )

    async def _execute_search(
        self, action: str, parameters: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """执行知识检索"""

        with tracer.start_as_current_span(
            f"knowledge_{action}", attributes={"action": action}
        ) as span:
            if action == "search_knowledge":
                result = await self._search_knowledge_base(parameters, context)

            elif action == "retrieve_documents":
                result = await self._retrieve_documents(parameters, context)

            elif action == "answer_question":
                result = await self._answer_question(parameters, context)

            else:
                span.add_event("unknown_action")
                result = {
                    "error": f"Unknown action: {action}",
                    "summary": f"不支持的操作: {action}",
                }

            span.set_attribute("result_keys", ",".join(result.keys()))
            return result

    async def _search_knowledge_base(
        self, parameters: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """搜索知识库"""

        with tracer.start_as_current_span("search_knowledge_base") as span:
            user_query = context.get("user_query", "")

            span.set_attribute("query", user_query)

            # 模拟向量检索（实际项目中应使用向量数据库）
            # 返回模拟的检索结果
            search_results = [
                {
                    "id": "doc_001",
                    "title": "Python 异步编程指南",
                    "content": "Python 的异步编程使用 asyncio 库...",
                    "score": 0.92,
                },
                {
                    "id": "doc_002",
                    "title": "FastAPI 最佳实践",
                    "content": "FastAPI 是一个现代、快速的 Web 框架...",
                    "score": 0.85,
                },
                {
                    "id": "doc_003",
                    "title": "数据分析实战",
                    "content": "使用 Pandas 进行数据分析...",
                    "score": 0.78,
                },
            ]

            result = {
                "query": user_query,
                "results": search_results,
                "result_count": len(search_results),
                "top_score": search_results[0]["score"] if search_results else 0,
                "summary": (
                    f"检索到 {len(search_results)} 个相关文档，"
                    f"最高相关度 {search_results[0]['score']:.2f}"
                    if search_results
                    else "未找到相关文档"
                ),
            }

            span.set_attribute("result_count", len(search_results))
            span.add_event("search_completed", {"query": user_query, "hits": len(search_results)})

            return result

    async def _retrieve_documents(
        self, parameters: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """检索文档"""

        with tracer.start_as_current_span("retrieve_documents") as span:
            doc_ids = parameters.get("doc_ids", [])

            span.set_attribute("doc_ids_count", len(doc_ids))

            # 模拟文档检索
            documents = [
                {
                    "id": doc_id,
                    "title": f"Document {doc_id}",
                    "content": f"Content of document {doc_id}",
                }
                for doc_id in doc_ids[:3]  # 最多返回3个
            ]

            result = {
                "documents": documents,
                "count": len(documents),
                "summary": f"检索到 {len(documents)} 个文档",
            }

            span.add_event("documents_retrieved", {"count": len(documents)})
            return result

    async def _answer_question(
        self, parameters: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """回答问题"""

        with tracer.start_as_current_span("answer_question") as span:
            question = context.get("user_query", "")

            span.set_attribute("question", question)

            # 模拟问答（实际项目中应使用 RAG）
            answer = (
                "根据知识库检索，Python 异步编程主要使用 asyncio 库，"
                "通过 async/await 语法实现非阻塞的并发执行。"
            )

            result = {
                "question": question,
                "answer": answer,
                "confidence": 0.88,
                "sources": ["doc_001", "doc_002"],
                "summary": f"问题已回答，置信度 {0.88:.2f}",
            }

            span.set_attribute("confidence", 0.88)
            span.add_event("question_answered")

            return result


# ============================================================================
# 文件信息
# ============================================================================

__all__ = [
    "DataAnalystAgent",
    "KnowledgeAgent",
]
