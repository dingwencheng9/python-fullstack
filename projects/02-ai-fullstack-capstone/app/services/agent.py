"""Mock LLM Agent 服务。

修复版本：支持异步调用
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.metrics import (
    rag_context_chars_histogram,
    rag_context_truncations_total,
    rag_retrieved_chunks_histogram,
)
from app.models import Answer
from app.services.rag import RAGService

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

# 上下文大小限制（防止 LLM 上下文溢出）
MAX_CONTEXT_CHARS = 4000  # 约 1000 tokens


class MockAgent:
    """离线可运行的知识助手。"""

    def __init__(self, rag: RAGService | None = None) -> None:
        self.rag = rag or RAGService()

    def _truncate_context(self, chunks: list[object], max_chars: int = MAX_CONTEXT_CHARS) -> str:
        """防御性截断：限制上下文总大小，防止 LLM 上下文溢出。

        Args:
            chunks: 检索到的文档片段列表
            max_chars: 最大字符数限制

        Returns:
            截断后的上下文字符串
        """
        context_parts = []
        total_chars = 0
        truncated = False

        for chunk in chunks:
            # 每个 chunk 最多取 200 字符
            chunk_text = chunk.text[:200]  # type: ignore[attr-defined]
            chunk_len = len(chunk_text)

            # 检查是否会超出总限制
            if total_chars + chunk_len > max_chars:
                # 添加截断标记
                remaining = max_chars - total_chars
                if remaining > 50:  # 至少保留 50 字符才值得添加
                    context_parts.append(chunk_text[:remaining])
                context_parts.append("\n... [上下文已截断以防止溢出]")
                truncated = True
                break

            context_parts.append(chunk_text)
            total_chars += chunk_len

        # 记录 Prometheus 指标
        workspace = "default"  # 当前使用默认 workspace
        rag_context_chars_histogram.labels(workspace=workspace).observe(total_chars)
        if truncated:
            rag_context_truncations_total.labels(workspace=workspace).inc()

        return "\n".join(context_parts)

    async def answer_async(self, question: str) -> Answer:
        """基于检索片段回答问题（异步版本）。"""
        # 异步调用检索
        sources = await self.rag.retrieve(question, top_k=3)

        # 记录检索到的文档数量
        workspace = "default"
        rag_retrieved_chunks_histogram.labels(workspace=workspace).observe(len(sources))

        if not sources:
            return Answer(
                question=question,
                answer="我没有在知识库中找到相关内容。请先导入文档。",
                sources=[],
            )

        # ✅ 使用防御性截断，防止上下文爆炸
        context = self._truncate_context(sources, max_chars=MAX_CONTEXT_CHARS)  # type: ignore[arg-type]
        answer = f"根据知识库，相关信息如下：\n{context}"
        return Answer(question=question, answer=answer, sources=sources)

    def answer(self, question: str) -> Answer:
        """基于检索片段回答问题（同步版本）。

        建议优先使用 answer_async() 方法。
        """
        import asyncio

        return asyncio.run(self.answer_async(question))

    async def stream_answer_async(self, question: str) -> AsyncIterator[str]:
        """异步模拟 token 流式输出。"""
        answer = await self.answer_async(question)
        for word in answer.answer.split():
            yield word + " "

    def stream_answer(self, question: str) -> Iterator[str]:
        """模拟 token 流式输出（同步版本）。

        建议优先使用 stream_answer_async() 方法。
        """
        import asyncio

        answer = asyncio.run(self.answer_async(question))
        for word in answer.answer.split():
            yield word + " "
