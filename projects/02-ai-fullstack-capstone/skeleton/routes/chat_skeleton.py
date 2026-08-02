# ruff: noqa: F821
# 骨架代码：学生填空用教学模板，类型未定义为设计意图

"""

from __future__ import annotations

【骨架代码】聊天问答路由

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from fastapi import APIRouter

# TODO: 导入模型和服务
# from ...models import ChatRequest, ChatResponse, SearchResult
# from ...services.rag import RAGService
# from ...services.agent import AgentService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/completions")
def chat_completion(
    request: ChatRequest, rag_service: RAGService, agent_service: AgentService
) -> ChatResponse:
    """同步问答（非流式）

    步骤：
    1. RAG 检索相关文档片段
    2. Agent 生成回答
    3. 返回回答和来源
    """
    # TODO: 实现同步问答
    # ← 你的代码写在这里


@router.post("/completions/stream")
def chat_completion_stream(
    request: ChatRequest, rag_service: RAGService, agent_service: AgentService
):
    """SSE 流式问答

    步骤：
    1. RAG 检索相关文档片段
    2. 调用 Agent 流式生成回答
    3. 通过 SSE 逐块发送
    """
    # TODO: 实现流式问答
    # 提示：使用 yield 逐个输出事件
    # 提示：返回 EventSourceResponse
    # ← 你的代码写在这里
