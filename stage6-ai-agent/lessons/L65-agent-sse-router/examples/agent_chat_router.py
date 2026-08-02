"""

from __future__ import annotations

L12 AI Agent 编排 - FastAPI SSE 路由
====================================

本模块实现 Agent 流式对话的 SSE API 端点。

核心能力：
1. FastAPI StreamingResponse + SSE 协议
2. JWT 认证集成（L11 安全网关）
3. OpenTelemetry Trace Context 传递
4. 流式事件实时推送

作者：Python 3.13 全栈课程
"""

import asyncio
import json
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from pydantic import BaseModel, ConfigDict, Field

# 导入流式事件捕获系统（假设已安装）
# from .streaming_events import StreamingAgentOrchestrator, Event


tracer = trace.get_tracer(__name__)
propagator = TraceContextTextMapPropagator()


# ============================================================
# 1. 请求/响应模型
# ============================================================


class ChatRequest(BaseModel):
    """对话请求"""

    message: str = Field(min_length=1, max_length=2000, description="用户消息")
    conversation_id: str | None = Field(default=None, description="会话 ID（可选）")
    stream: bool = Field(default=True, description="是否启用流式响应")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "搜索关于 Python 异步编程的知识",
                "conversation_id": "conv_123",
                "stream": True,
            }
        }
    )


class ChatResponse(BaseModel):
    """对话响应（非流式）"""

    message: str = Field(description="Agent 回复")
    conversation_id: str = Field(description="会话 ID")
    events_count: int = Field(description="事件总数")
    duration_ms: float = Field(description="总耗时（毫秒）")


# ============================================================
# 2. JWT 认证依赖（集成 L11 安全网关）
# ============================================================


class JWTTokenData(BaseModel):
    """JWT Token 数据"""

    user_id: str
    username: str
    roles: list[str] = []


async def verify_jwt_token(request: Request) -> JWTTokenData:
    """
    验证 JWT Token

    **集成点**: stage3-web-apis/lessons/L35-security-gateway

    **流程**:
    1. 从 Authorization Header 提取 Token
    2. 验证 Token 签名和有效期
    3. 返回 Token 数据
    """
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少或无效的 Authorization Header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.replace("Bearer ", "")

    # 这里应调用 L11 的 JWT 验证逻辑
    # from ..L11_security_gateway.auth import verify_token
    # token_data = await verify_token(token)

    # 模拟验证（生产环境需要真实验证）
    if token == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 模拟返回数据
    return JWTTokenData(user_id="user_123", username="demo_user", roles=["user", "agent_access"])


# 依赖注入
CurrentUser = Annotated[JWTTokenData, Depends(verify_jwt_token)]


# ============================================================
# 3. SSE 事件格式化
# ============================================================


def format_sse_event(event_data: dict, event_type: str = "message") -> str:
    """
    格式化 SSE 事件

    **SSE 协议格式**:
    ```
    event: message
    data: {"key": "value"}

    ```

    **注意**: 每个事件后需要两个换行符
    """
    lines = [
        f"event: {event_type}",
        f"data: {json.dumps(event_data, ensure_ascii=False)}",
        "",  # 空行作为事件分隔
    ]
    return "\n".join(lines) + "\n"


# ============================================================
# 4. OpenTelemetry Trace Context 传递
# ============================================================


def extract_trace_context(request: Request) -> dict:
    """
    从 HTTP Headers 提取 Trace Context

    **W3C Trace Context 标准**:
    - traceparent: 00-{trace-id}-{span-id}-{trace-flags}
    - tracestate: (可选)
    """
    # 从 Headers 提取 Trace Context
    carrier = dict(request.headers)
    context = propagator.extract(carrier)

    return context


def inject_trace_context(span: trace.Span) -> dict:
    """
    注入 Trace Context 到事件

    **用途**: 确保客户端可以关联 Trace
    """
    carrier = {}
    propagator.inject(carrier, context=trace.set_span_in_context(span))

    return carrier


# ============================================================
# 5. 流式事件生成器（SSE 格式）
# ============================================================


async def generate_sse_events(
    message: str,
    conversation_id: str,
    user_id: str,
    parent_span: trace.Span,
) -> AsyncGenerator[str]:
    """
    生成 SSE 格式的事件流

    **流程**:
    1. 提取 Trace Context
    2. 运行 Agent（流式）
    3. 格式化为 SSE 事件
    4. 实时推送
    """
    # 创建子 Span（继承 parent_span）
    with tracer.start_as_current_span(
        "generate_sse_events",
        context=trace.set_span_in_context(parent_span),
    ) as span:
        span.set_attribute("message", message)
        span.set_attribute("conversation_id", conversation_id)
        span.set_attribute("user_id", user_id)

        try:
            # 注入 Trace Context 到首个事件
            trace_context = inject_trace_context(span)

            # 发送连接成功事件
            yield format_sse_event(
                {
                    "type": "connection",
                    "status": "connected",
                    "conversation_id": conversation_id,
                    "trace_context": trace_context,
                },
                event_type="connection",
            )

            # 模拟 Agent 流式执行
            # 生产环境应该调用: StreamingAgentOrchestrator().run_streaming(message)

            # 模拟 Token 流
            response_text = "根据您的问题，我需要搜索相关知识。"
            for i, char in enumerate(response_text):
                event_data = {
                    "event_type": "on_chat_model_stream",
                    "token": char,
                    "model": "claude-sonnet-3.5",
                    "is_final": False,
                    "sequence": i,
                }

                yield format_sse_event(event_data, event_type="token")

                await asyncio.sleep(0.02)  # 模拟延迟

            # 模拟工具调用
            yield format_sse_event(
                {
                    "event_type": "on_tool_start",
                    "tool_name": "search_knowledge",
                    "tool_input": {"query": message, "top_k": 5},
                },
                event_type="tool",
            )

            await asyncio.sleep(0.15)  # 模拟工具执行

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

            # 模拟最终响应 Token 流
            final_text = "找到了相关文档，Python 异步编程主要使用 asyncio..."
            for i, char in enumerate(final_text):
                event_data = {
                    "event_type": "on_chat_model_stream",
                    "token": char,
                    "model": "qwen2.5:7b",
                    "is_final": False,
                    "sequence": len(response_text) + i,
                }

                yield format_sse_event(event_data, event_type="token")

                await asyncio.sleep(0.02)

            # 发送最终 Token
            yield format_sse_event(
                {
                    "event_type": "on_chat_model_stream",
                    "token": "",
                    "model": "qwen2.5:7b",
                    "is_final": True,
                },
                event_type="token",
            )

            # 发送完成事件
            yield format_sse_event(
                {
                    "type": "completion",
                    "status": "completed",
                    "conversation_id": conversation_id,
                },
                event_type="completion",
            )

            span.set_status(Status(StatusCode.OK))
            span.add_event("sse_stream_completed")

        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)

            # 发送错误事件
            yield format_sse_event(
                {
                    "type": "error",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
                event_type="error",
            )


# ============================================================
# 6. FastAPI Router
# ============================================================

router = APIRouter(
    prefix="/api/v1/agent",
    tags=["AI Agent"],
)


@router.post(
    "/chat",
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "SSE 流式响应",
            "content": {
                "text/event-stream": {
                    "example": """event: connection
data: {"type":"connection","status":"connected"}

event: token
data: {"event_type":"on_chat_model_stream","token":"你好"}

event: completion
data: {"type":"completion","status":"completed"}
"""
                }
            },
        },
        401: {"description": "未授权（缺少或无效的 JWT Token）"},
        422: {"description": "请求参数验证失败"},
    },
)
async def chat_stream(
    request: Request,
    chat_request: ChatRequest,
    current_user: CurrentUser,
):
    """
    Agent 流式对话接口

    **功能**:
    - 接收用户消息
    - 实时流式返回 Agent 响应
    - 支持 Token 流、工具调用事件

    **认证**: 需要 JWT Token（Bearer Token）

    **SSE 事件类型**:
    - `connection`: 连接建立
    - `token`: Token 流式生成
    - `tool`: 工具调用事件
    - `completion`: 对话完成
    - `error`: 错误事件

    **示例**:
    ```bash
    curl -X POST http://localhost:8000/api/v1/agent/chat \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your-jwt-token" \
      -d '{"message": "搜索 Python 异步编程", "stream": true}' \
      --no-buffer
    ```
    """
    with tracer.start_as_current_span("chat_stream_endpoint") as span:
        # 提取 Trace Context
        extract_trace_context(request)

        # 设置 Span 属性
        span.set_attribute("user_id", current_user.user_id)
        span.set_attribute("username", current_user.username)
        span.set_attribute("message", chat_request.message)
        span.set_attribute("stream", chat_request.stream)

        # 生成会话 ID
        import uuid

        conversation_id = chat_request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        span.set_attribute("conversation_id", conversation_id)

        # 非流式响应（降级）
        if not chat_request.stream:
            # 收集所有事件
            events = []
            async for event_str in generate_sse_events(
                chat_request.message,
                conversation_id,
                current_user.user_id,
                span,
            ):
                # 解析事件（简化处理）
                events.append(event_str)

            return ChatResponse(
                message="响应已生成（非流式模式）",
                conversation_id=conversation_id,
                events_count=len(events),
                duration_ms=0.0,
            )

        # 流式响应（SSE）
        return StreamingResponse(
            generate_sse_events(
                chat_request.message,
                conversation_id,
                current_user.user_id,
                span,
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Nginx 禁用缓冲
            },
        )


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "agent-chat"}


# ============================================================
# 7. 使用示例（Python 客户端）
# ============================================================


async def example_client():
    """
    Python 客户端示例

    **依赖**: httpx
    """
    import httpx

    url = "http://localhost:8000/api/v1/agent/chat"
    headers = {
        "Authorization": "Bearer your-jwt-token-here",
        "Content-Type": "application/json",
    }
    data = {
        "message": "搜索关于 Python 异步编程的知识",
        "stream": True,
    }

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, json=data, headers=headers) as response:
            print(f"状态码: {response.status_code}\n")

            async for line in response.aiter_lines():
                if line.startswith("event:"):
                    event_type = line.replace("event:", "").strip()
                    print(f"\n[事件类型: {event_type}]")

                elif line.startswith("data:"):
                    data_str = line.replace("data:", "").strip()
                    try:
                        data = json.loads(data_str)
                        print(f"  数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    except json.JSONDecodeError:
                        print(f"  数据: {data_str}")


# ============================================================
# 8. JavaScript 客户端示例
# ============================================================

JAVASCRIPT_CLIENT_EXAMPLE = """
// JavaScript/TypeScript 客户端示例
async function chatWithAgent(message: string, token: string) {
  const response = await fetch('http://localhost:8000/api/v1/agent/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      message: message,
      stream: true,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }

  // 创建 EventSource 替代方案（Fetch + SSE 解析）
  const reader = response.body!.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();

    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\\n');

    for (const line of lines) {
      if (line.startsWith('event:')) {
        const eventType = line.replace('event:', '').trim();
        console.log(`[事件] ${eventType}`);
      }

      else if (line.startsWith('data:')) {
        const dataStr = line.replace('data:', '').trim();

        try {
          const data = JSON.parse(dataStr);

          // Token 流式渲染
          if (data.event_type === 'on_chat_model_stream' && !data.is_final) {
            process.stdout.write(data.token); // 打字机效果
          }

          // 工具调用
          else if (data.event_type === 'on_tool_start') {
            console.log(`\\n\\n🔧 工具: ${data.tool_name}`);
          }

          else if (data.event_type === 'on_tool_end') {
            console.log(`✅ ${data.success ? '成功' : '失败'} (${data.duration_ms}ms)`);
          }
        } catch (e) {
          // 非 JSON 数据
        }
      }
    }
  }
}

// 使用示例
chatWithAgent('搜索 Python 异步编程', 'your-jwt-token');
"""


if __name__ == "__main__":
    print("=" * 80)
    print("L12 AI Agent 编排 - FastAPI SSE 路由")
    print("=" * 80 + "\n")

    print("💡 使用方法:\n")
    print("1. 启动 FastAPI 服务:")
    print("   uvicorn main:app --reload\n")

    print("2. 测试 SSE 端点:")
    print("   curl -X POST http://localhost:8000/api/v1/agent/chat \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -H "Authorization: Bearer demo-token" \\')
    print('     -d \'{"message": "搜索 Python", "stream": true}\' \\')
    print("     --no-buffer\n")

    print("3. Python 客户端:")
    print("   python -c 'import asyncio; asyncio.run(example_client())'\n")

    print("4. JavaScript 客户端:")
    print("   见上面的 JAVASCRIPT_CLIENT_EXAMPLE\n")

    print("=" * 80)
    print("核心要点:")
    print("=" * 80)
    print("  1. ✅ FastAPI StreamingResponse + SSE 协议")
    print("  2. ✅ JWT 认证集成（L11 安全网关）")
    print("  3. ✅ OpenTelemetry Trace Context 传递")
    print("  4. ✅ 流式事件实时推送")
    print("  5. ✅ Python + JavaScript 客户端示例")
