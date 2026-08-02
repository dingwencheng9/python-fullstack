"""LangGraph 智能 Agent。

from __future__ import annotations

基于 LangGraph StateGraph 实现的简单问答 Agent，支持：
- 检索相关文档
- 生成回答
- 回答质量检查
- 不确定时要求用户澄清

设计模式：状态机 + 节点函数 + 条件路由
"""

import asyncio
import concurrent.futures
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from langgraph.graph import END, StateGraph

from app.models import Answer, Chunk
from app.services.rag import RAGService


@dataclass
class AgentState:
    """Agent 状态机状态。"""

    # 输入
    question: str = ""
    # 中间状态
    retrieved_chunks: list[Chunk] = field(default_factory=list)
    draft_answer: str = ""
    # 输出
    final_answer: str = ""
    needs_clarification: bool = False
    clarification_reason: str = ""


class GraphAgent:
    """基于 LangGraph 的智能问答 Agent。"""

    def __init__(self, rag: RAGService | None = None) -> None:
        self.rag = rag or RAGService()
        self.graph: Any = self._build_graph()

    def _run_async(self, coro):
        """运行异步函数，处理嵌套事件循环。

        LangGraph 通过 invoke() 同步调用时，需要这个方法来执行异步操作。
        它会检测是否已经在事件循环中，如果是则使用线程池执行，否则创建新循环。
        """
        try:
            asyncio.get_running_loop()
            # 已经在事件循环中，使用线程池执行协程
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result()
        except RuntimeError:
            # 没有运行中的事件循环，安全地创建新的
            return asyncio.run(coro)

    def _build_graph(self) -> Any:
        """构建状态机工作流。

        工作流：
        retrieve → generate_answer → check_quality → END
                                     ↓
                                 ask_clarification → END
        """
        workflow = StateGraph(AgentState)

        # 定义节点
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("generate_answer", self._generate_node)
        workflow.add_node("check_quality", self._quality_check_node)
        workflow.add_node("ask_clarification", self._clarification_node)

        # 定义边
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate_answer")
        workflow.add_edge("generate_answer", "check_quality")

        # 条件路由：检查回答质量
        workflow.add_conditional_edges(
            "check_quality",
            self._route_after_quality_check,
            {"good": END, "bad": "ask_clarification", "clarify": "ask_clarification"},
        )
        workflow.add_edge("ask_clarification", END)

        return workflow.compile()

    def _retrieve_node(self, state: AgentState) -> dict[str, Any]:
        """检索节点：根据问题检索相关文档片段。"""
        chunks = self._run_async(self.rag.retrieve(state.question, top_k=3))
        return {"retrieved_chunks": chunks}

    def _generate_node(self, state: AgentState) -> dict[str, Any]:
        """生成回答节点：基于检索到的片段生成回答。"""
        if not state.retrieved_chunks:
            return {"draft_answer": "我没有在知识库中找到相关内容。请先导入文档或换一个问题。"}

        # 构建上下文
        context = "\n".join(
            [
                f"[片段 {i + 1}]: {chunk.text[:200]}..."
                for i, chunk in enumerate(state.retrieved_chunks)
            ]
        )

        answer = f"根据检索到的信息：\n\n{context}\n\n总结："
        if len(state.retrieved_chunks) >= 2:
            answer += "综合以上信息，你的问题的答案是..."
        elif state.retrieved_chunks:
            answer += f"根据找到的信息，{state.retrieved_chunks[0].text[:300]}..."

        return {"draft_answer": answer}

    def _quality_check_node(self, state: AgentState) -> dict[str, Any]:
        """质量检查节点：检查回答是否足够好。"""
        answer = state.draft_answer
        chunks = state.retrieved_chunks

        # 简单质量规则
        if not chunks:
            return {"needs_clarification": False}  # 已经回答了无相关信息

        # 检查检索到的相关度
        total_score = sum(c.score or 0 for c in chunks)
        avg_score = total_score / len(chunks) if chunks else 0

        if avg_score < -0.5:  # stub embedder 的相似度可能在负数范围
            return {
                "needs_clarification": True,
                "clarification_reason": "检索到的相关信息太少，请提供更多上下文或换个问法。",
            }

        if len(answer) < 50:
            # 回答太短，信息不足
            return {
                "needs_clarification": True,
                "clarification_reason": "问题太宽泛，请提供更具体的问题。",
            }

        return {"needs_clarification": False}

    def _clarification_node(self, state: AgentState) -> dict[str, Any]:
        """澄清节点：生成澄清回答。"""
        if state.needs_clarification:
            return {"final_answer": f"抱歉，{state.clarification_reason}"}
        return {"final_answer": state.draft_answer}

    def _route_after_quality_check(self, state: AgentState) -> str:
        """条件路由：根据质量检查结果决定下一步。"""
        if state.needs_clarification:
            return "clarify"
        # 如果回答足够好，直接结束
        return "good"

    def answer(self, question: str) -> Answer:
        """回答用户问题。"""
        state = AgentState(question=question)
        result = self.graph.invoke(state)

        sources = result.get("retrieved_chunks", [])
        answer = result.get("final_answer") or result.get("draft_answer", "")

        return Answer(question=question, answer=answer, sources=sources)

    def stream_answer(self, question: str) -> Iterator[str]:
        """模拟流式输出。"""
        answer = self.answer(question)
        # 逐词流式输出
        for word in answer.answer.split():
            yield word + " "
