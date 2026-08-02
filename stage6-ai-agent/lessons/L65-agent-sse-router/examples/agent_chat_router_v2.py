"""

from __future__ import annotations

L12 AI Agent 编排 - FastAPI SSE 路由 V2（持久化版）
===================================================

本模块实现 Agent 流式对话的 SSE API 端点（集成持久化）。

核心能力：
1. PostgreSQL 会话持久化
2. Token 控制与自动摘要
3. thread_id 会话管理
4. 历史消息加载
5. Redis 缓存层

作者：Python 3.13 全栈课程
"""

import asyncio
import json
import uuid
from collections.abc import AsyncGenerator
from typing import Annotated

from checkpoint_system import (
    MessageRecord,
    PostgreSQLCheckpointSaver,
    RedisCacheLayer,
)
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from pydantic import BaseModel, ConfigDict, Field
from token_control import TokenControlConfig, TokenControlNode

tracer = trace.get_tracer(__name__)


# ============================================================
# 1. 升级的请求/响应模型
# ============================================================


class ChatRequestV2(BaseModel):
    """对话请求 V2（支持 thread_id）"""

    message: str = Field(min_length=1, max_length=2000, description="用户消息")
    thread_id: str | None = Field(default=None, description="会话线程 ID（传入已有 ID 加载历史，不传则创建新会话）")
    stream: bool = Field(default=True, description="是否启用流式响应")
    include_history: bool = Field(default=True, description="是否包含历史上下文")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "搜索关于 Python 异步编程的知识",
                "thread_id": "thread_abc123",
                "stream": True,
                "include_history": True,
            }
        }
    )


class ConversationInfo(BaseModel):
    """会话信息"""

    thread_id: str
    user_id: str
    total_messages: int
    total_tokens: int
    created_at: str
    updated_at: str


class ChatResponseV2(BaseModel):
    """对话响应 V2"""

    message: str = Field(description="Agent 回复")
    thread_id: str = Field(description="会话线程 ID")
    conversation_info: ConversationInfo = Field(description="会话信息")
    token_statistics: dict = Field(description="Token 统计")


class ConversationListResponse(BaseModel):
    """会话列表响应"""

    conversations: list[ConversationInfo]
    total: int


# ============================================================
# 2. JWT 认证（复用）
# ============================================================


class JWTTokenData(BaseModel):
    """JWT Token 数据"""

    user_id: str
    username: str
    roles: list[str] = []


async def verify_jwt_token(request: Request) -> JWTTokenData:
    """验证 JWT Token"""
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少或无效的 Authorization Header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.replace("Bearer ", "")

    # 模拟验证
    if token == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效或已过期",
        )

    return JWTTokenData(user_id="user_123", username="demo_user", roles=["user", "agent_access"])


CurrentUser = Annotated[JWTTokenData, Depends(verify_jwt_token)]


# ============================================================
# 3. 全局状态（依赖注入）
# ============================================================

# 全局存储实例（在应用启动时初始化）
_pg_saver: PostgreSQLCheckpointSaver | None = None
_redis_cache: RedisCacheLayer | None = None
_token_control: TokenControlNode | None = None


async def get_pg_saver() -> PostgreSQLCheckpointSaver:
    """获取 PostgreSQL 存储"""
    if _pg_saver is None:
        raise HTTPException(status_code=503, detail="PostgreSQL 存储未初始化")
    return _pg_saver


async def get_redis_cache() -> RedisCacheLayer:
    """获取 Redis 缓存"""
    if _redis_cache is None:
        raise HTTPException(status_code=503, detail="Redis 缓存未初始化")
    return _redis_cache


async def get_token_control() -> TokenControlNode:
    """获取 Token 控制节点"""
    if _token_control is None:
        raise HTTPException(status_code=503, detail="Token 控制未初始化")
    return _token_control


# ============================================================
# 4. SSE 事件格式化（复用）
# ============================================================


def format_sse_event(event_data: dict, event_type: str = "message") -> str:
    """格式化 SSE 事件"""
    lines = [
        f"event: {event_type}",
        f"data: {json.dumps(event_data, ensure_ascii=False)}",
        "",
    ]
    return "\n".join(lines) + "\n"


# ============================================================
# 5. 流式事件生成器（增强版）
# ============================================================


async def generate_sse_events_v2(
    message: str,
    thread_id: str,
    user_id: str,
    include_history: bool,
    pg_saver: PostgreSQLCheckpointSaver,
    token_control: TokenControlNode,
    parent_span: trace.Span,
) -> AsyncGenerator[str]:
    """
    生成 SSE 格式的事件流 V2

    **增强功能**:
    - 加载历史上下文
    - Token 控制
    - 自动摘要
    - 持久化消息
    """
    with tracer.start_as_current_span(
        "generate_sse_events_v2",
        context=trace.set_span_in_context(parent_span),
    ) as span:
        span.set_attribute("thread_id", thread_id)
        span.set_attribute("user_id", user_id)
        span.set_attribute("include_history", include_history)

        try:
            # 1. 发送连接事件
            yield format_sse_event(
                {
                    "type": "connection",
                    "status": "connected",
                    "thread_id": thread_id,
                },
                event_type="connection",
            )

            # 2. Token 控制检查
            yield format_sse_event(
                {
                    "type": "system",
                    "message": "检查 Token 限制...",
                },
                event_type="system",
            )

            control_result = await token_control.check_and_compress(thread_id)

            # 如果触发了压缩
            if control_result["compression_result"]:
                compression = control_result["compression_result"]
                yield format_sse_event(
                    {
                        "type": "system",
                        "message": f"历史记忆已压缩（{compression['compression_ratio']:.1f}% 压缩率）",
                        "compression": compression,
                    },
                    event_type="system",
                )

            # 3. 加载历史上下文（如果需要）
            context_summary = ""
            if include_history:
                summary, recent_messages = await token_control.summarizer.get_conversation_context(
                    thread_id,
                    max_tokens=4000,
                )

                if summary:
                    context_summary = summary
                    yield format_sse_event(
                        {
                            "type": "system",
                            "message": f"已加载历史上下文（{len(recent_messages)} 条最近消息）",
                        },
                        event_type="system",
                    )

            # 4. 保存用户消息
            user_message = MessageRecord(
                message_id=f"msg_{uuid.uuid4().hex[:8]}",
                thread_id=thread_id,
                role="user",
                content=message,
                tokens=len(message) // 4,  # 简化估算
            )
            await pg_saver.add_message(thread_id, user_message)

            # 5. 模拟 Agent 推理 Token 流
            response_text = f"根据您的问题「{message}」，我需要搜索相关知识。"

            for i, char in enumerate(response_text):
                yield format_sse_event(
                    {
                        "event_type": "on_chat_model_stream",
                        "token": char,
                        "model": "claude-sonnet-3.5",
                        "is_final": False,
                        "sequence": i,
                    },
                    event_type="token",
                )
                await asyncio.sleep(0.02)

            # 6. 模拟工具调用
            yield format_sse_event(
                {
                    "event_type": "on_tool_start",
                    "tool_name": "search_knowledge",
                    "tool_input": {
                        "query": message,
                        "top_k": 5,
                        "context": context_summary[:100] if context_summary else None,
                    },
                },
                event_type="tool",
            )

            await asyncio.sleep(0.15)

            yield format_sse_event(
                {
                    "event_type": "on_tool_end",
                    "tool_name": "search_knowledge",
                    "tool_output": {
                        "success": True,
                        "results": [
                            {"doc_id": "doc_1", "score": 0.95},
                            {"doc_id": "doc_2", "score": 0.88},
                        ],
                    },
                    "duration_ms": 150.5,
                    "success": True,
                },
                event_type="tool",
            )

            # 7. 模拟最终响应
            final_text = "找到了相关文档，Python 异步编程主要使用 asyncio 库..."

            for i, char in enumerate(final_text):
                yield format_sse_event(
                    {
                        "event_type": "on_chat_model_stream",
                        "token": char,
                        "model": "qwen2.5:7b",
                        "is_final": False,
                        "sequence": len(response_text) + i,
                    },
                    event_type="token",
                )
                await asyncio.sleep(0.02)

            # 8. 最终 Token
            yield format_sse_event(
                {
                    "event_type": "on_chat_model_stream",
                    "token": "",
                    "model": "qwen2.5:7b",
                    "is_final": True,
                },
                event_type="token",
            )

            # 9. 保存 Agent 响应
            full_response = response_text + final_text
            agent_message = MessageRecord(
                message_id=f"msg_{uuid.uuid4().hex[:8]}",
                thread_id=thread_id,
                role="assistant",
                content=full_response,
                tokens=len(full_response) // 4,
            )
            await pg_saver.add_message(thread_id, agent_message)

            # 10. 完成事件
            yield format_sse_event(
                {
                    "type": "completion",
                    "status": "completed",
                    "thread_id": thread_id,
                    "token_statistics": control_result["statistics"],
                },
                event_type="completion",
            )

            span.set_status(Status(StatusCode.OK))

        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)

            yield format_sse_event(
                {
                    "type": "error",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
                event_type="error",
            )


# ============================================================
# 6. FastAPI Router V2
# ============================================================

router = APIRouter(
    prefix="/api/v2/agent",
    tags=["AI Agent V2"],
)


@router.post("/chat")
async def chat_stream_v2(
    request: Request,
    chat_request: ChatRequestV2,
    current_user: CurrentUser,
    pg_saver: Annotated[PostgreSQLCheckpointSaver, Depends(get_pg_saver)],
    redis_cache: Annotated[RedisCacheLayer, Depends(get_redis_cache)],
    token_control: Annotated[TokenControlNode, Depends(get_token_control)],
):
    """
    Agent 流式对话接口 V2（持久化版）

    **新增功能**:
    - thread_id 会话管理
    - 自动加载历史上下文
    - Token 控制与自动摘要
    - 消息持久化

    **请求示例**:
    ```json
    {
      "message": "搜索 Python 异步编程",
      "thread_id": "thread_abc123",
      "stream": true,
      "include_history": true
    }
    ```

    **行为**:
    - 如果 thread_id 存在 → 加载历史会话
    - 如果 thread_id 不存在或为 null → 创建新会话
    """
    with tracer.start_as_current_span("chat_stream_v2_endpoint") as span:
        span.set_attribute("user_id", current_user.user_id)
        span.set_attribute("message", chat_request.message)

        # 1. 处理 thread_id
        thread_id = chat_request.thread_id

        if not thread_id:
            # 创建新会话
            thread_id = f"thread_{uuid.uuid4().hex[:12]}"
            await pg_saver.create_conversation(
                thread_id,
                current_user.user_id,
                metadata={"source": "api_v2"},
            )
            span.add_event("new_conversation_created", {"thread_id": thread_id})

        else:
            # 检查会话是否存在
            conversation = await pg_saver.get_conversation(thread_id)

            if not conversation:
                # 会话不存在，创建新的
                await pg_saver.create_conversation(
                    thread_id,
                    current_user.user_id,
                    metadata={"source": "api_v2"},
                )
                span.add_event("conversation_initialized", {"thread_id": thread_id})

            elif conversation.user_id != current_user.user_id:
                # 会话属于其他用户
                raise HTTPException(status_code=403, detail="无权访问该会话")

        span.set_attribute("thread_id", thread_id)

        # 2. 流式响应
        if chat_request.stream:
            return StreamingResponse(
                generate_sse_events_v2(
                    chat_request.message,
                    thread_id,
                    current_user.user_id,
                    chat_request.include_history,
                    pg_saver,
                    token_control,
                    span,
                ),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                    "X-Thread-ID": thread_id,  # 返回 thread_id
                },
            )

        # 3. 非流式响应（降级）
        # 收集所有事件
        events = []
        async for event_str in generate_sse_events_v2(
            chat_request.message,
            thread_id,
            current_user.user_id,
            chat_request.include_history,
            pg_saver,
            token_control,
            span,
        ):
            events.append(event_str)

        # 获取会话信息
        conversation = await pg_saver.get_conversation(thread_id)
        token_stats = await token_control.check_and_compress(thread_id)

        return ChatResponseV2(
            message="响应已生成",
            thread_id=thread_id,
            conversation_info=ConversationInfo(
                thread_id=conversation.thread_id,
                user_id=conversation.user_id,
                total_messages=conversation.total_messages,
                total_tokens=conversation.total_tokens,
                created_at=conversation.created_at.isoformat(),
                updated_at=conversation.updated_at.isoformat(),
            ),
            token_statistics=token_stats["statistics"],
        )


@router.get("/conversations")
async def list_conversations(
    current_user: CurrentUser,
    pg_saver: Annotated[PostgreSQLCheckpointSaver, Depends(get_pg_saver)],
    limit: int = 20,
):
    """
    列出用户的会话列表

    **返回**: 会话列表（按更新时间倒序）
    """
    conversations = await pg_saver.list_conversations(
        current_user.user_id,
        limit=limit,
    )

    return ConversationListResponse(
        conversations=[
            ConversationInfo(
                thread_id=conv.thread_id,
                user_id=conv.user_id,
                total_messages=conv.total_messages,
                total_tokens=conv.total_tokens,
                created_at=conv.created_at.isoformat(),
                updated_at=conv.updated_at.isoformat(),
            )
            for conv in conversations
        ],
        total=len(conversations),
    )


@router.get("/conversations/{thread_id}")
async def get_conversation_detail(
    thread_id: str,
    current_user: CurrentUser,
    pg_saver: Annotated[PostgreSQLCheckpointSaver, Depends(get_pg_saver)],
):
    """
    获取会话详情

    **返回**: 会话元数据 + 最近消息
    """
    # 检查会话
    conversation = await pg_saver.get_conversation(thread_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="会话不存在")

    if conversation.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="无权访问该会话")

    # 获取消息
    messages = await pg_saver.get_messages(thread_id, limit=50)

    return {
        "conversation": ConversationInfo(
            thread_id=conversation.thread_id,
            user_id=conversation.user_id,
            total_messages=conversation.total_messages,
            total_tokens=conversation.total_tokens,
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat(),
        ),
        "messages": [
            {
                "message_id": msg.message_id,
                "role": msg.role,
                "content": msg.content,
                "tokens": msg.tokens,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in messages
        ],
    }


@router.delete("/conversations/{thread_id}")
async def delete_conversation(
    thread_id: str,
    current_user: CurrentUser,
    pg_saver: Annotated[PostgreSQLCheckpointSaver, Depends(get_pg_saver)],
):
    """
    删除会话

    **操作**: 软删除（更新 status 为 'deleted'）
    """
    # 检查会话
    conversation = await pg_saver.get_conversation(thread_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="会话不存在")

    if conversation.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="无权删除该会话")

    # 软删除
    async with pg_saver.pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE conversations
            SET status = 'deleted', updated_at = NOW()
            WHERE thread_id = $1
            """,
            thread_id,
        )

    return {"message": "会话已删除", "thread_id": thread_id}


# ============================================================
# 7. 初始化函数
# ============================================================


async def initialize_storage(
    pg_connection_string: str,
    redis_url: str,
):
    """
    初始化存储系统

    **在应用启动时调用**
    """
    global _pg_saver, _redis_cache, _token_control

    # PostgreSQL
    _pg_saver = PostgreSQLCheckpointSaver(pg_connection_string)
    await _pg_saver.setup()

    # Redis
    _redis_cache = RedisCacheLayer(redis_url)
    await _redis_cache.setup()

    # Token 控制
    config = TokenControlConfig(
        max_context_tokens=8000,
        target_context_tokens=4000,
        min_messages_for_summary=10,
    )
    _token_control = TokenControlNode(_pg_saver, config)

    print("✅ 存储系统已初始化")


async def cleanup_storage():
    """
    清理存储系统

    **在应用关闭时调用**
    """
    global _pg_saver, _redis_cache

    if _pg_saver:
        await _pg_saver.cleanup()

    if _redis_cache:
        await _redis_cache.cleanup()

    print("✅ 存储系统已清理")
