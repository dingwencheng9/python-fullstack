# mypy: disable-error-code="untyped-decorator"
"""聊天路由：普通回答 + SSE 流式回答。

from __future__ import annotations

注：FastAPI 装饰器在 mypy strict 下被视为 untyped（上游已知问题），
文件级关闭 ``untyped-decorator``，其他 strict 检查保留。
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.rbac import Principal, require_role
from app.routes.documents import get_rag_service
from app.services.graph_agent import GraphAgent

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


class ChatIn(BaseModel):
    question: str = Field(min_length=1)


def _agent_for_workspace(workspace_id: str) -> GraphAgent:
    """获取指定工作空间的 GraphAgent 实例。"""
    rag = get_rag_service(workspace_id)
    return GraphAgent(rag)


@router.post("")
async def chat(
    payload: ChatIn,
    principal: Annotated[Principal, Depends(require_role("viewer", "editor", "admin"))],
) -> dict[str, Any]:
    agent = _agent_for_workspace(principal.workspace_id)
    try:
        answer = agent.answer(payload.question)
    except Exception:
        logger.error(
            "Agent 回答失败: workspace=%s question=%s",
            principal.workspace_id,
            payload.question,
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="回答生成失败，请稍后重试") from None
    return {
        "question": answer.question,
        "answer": answer.answer,
        "sources": [{"text": c.text, "score": c.score} for c in answer.sources],
        "workspace_id": principal.workspace_id,
    }


@router.get("/stream")
async def chat_stream(
    question: str,
    principal: Annotated[Principal, Depends(require_role("viewer", "editor", "admin"))],
) -> StreamingResponse:
    agent = _agent_for_workspace(principal.workspace_id)

    def generate() -> Iterator[str]:
        try:
            for token in agent.stream_answer(question):
                yield f"data: {token}\n\n"
        except Exception:
            logger.error(
                "流式回答失败: workspace=%s question=%s",
                principal.workspace_id,
                question,
                exc_info=True,
            )
            yield "event: error\ndata: 流式回答生成失败\n\n"
        yield "event: done\ndata: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
