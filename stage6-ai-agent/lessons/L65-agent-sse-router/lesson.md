# L65: Agent SSE 流式路由

> **课程编号**: L65
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐☆（高级应用）
> **前置课程**: L64 Agent 部署
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L64**: Agent 部署与监控（理解 Agent 部署与可观测性）
- **L27**: FastAPI 入门（SSE 实现基础）

**如果你还没有学习以上课程，建议先完成前置课程。**

---

---

---

## 📚 课程内容

### 模块 1: SSE 协议基础 (3h)

#### 什么是 SSE？

SSE（Server-Sent Events）是 HTML62 标准的一部分，允许服务器向客户端推送实时数据。

**核心特性**:

- ⚡ 单向通信（服务器 → 客户端）
- 🔄 自动重连机制
- 📡 基于 HTTP 协议
- 🎯 文本数据传输
- 💾 支持事件 ID 和重试

**SSE vs WebSocket**:

| 特性       | SSE                   | WebSocket      |
| ---------- | --------------------- | -------------- |
| 通信方向   | 单向（服务器→客户端） | 双向           |
| 协议       | HTTP                  | WebSocket 协议 |
| 重连       | 自动重连              | 需手动实现     |
| 浏览器支持 | 广泛支持              | 广泛支持       |
| 复杂度     | 简单                  | 复杂           |
| 适用场景   | 实时推送、通知        | 实时聊天、游戏 |

**什么时候选择 SSE？**

- ✅ 服务器需要主动推送数据
- ✅ 不需要客户端向服务器发送频繁消息
- ✅ 需要自动重连机制
- ✅ 简单的实时更新场景

---

#### SSE 协议格式

**基本格式**:

```
event: message_type
data: {"key": "value"}
id: unique_event_id
retry: 3000

```

**字段说明**:

- `event`: 事件类型（可选，默认 "message"）
- `data`: 事件数据（必需，可以是多行）
- `id`: 事件 ID（可选，用于断线重连）
- `retry`: 重连延迟（毫秒）

**示例**:

```
event: token
data: {"type":"token","content":"Hello"}

event: token
data: {"type":"token","content":" World"}

event: completion
data: {"type":"completion","status":"success"}

```

**注意事项**:

- 每个字段后面必须有 `\n`
- 事件之间用空行 `\n\n` 分隔
- `data` 字段可以重复多次（多行数据）

---

#### Python SSE 实现

**使用 FastAPI StreamingResponse**:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def generate_sse_events():
    """生成 SSE 事件流"""
    # 发送连接建立事件
    yield f"event: connection\n"
    yield f"data: {{'status': 'connected'}}\n\n"

    # 模拟流式数据
    for i in range(10):
        await asyncio.sleep(0.5)
        yield f"event: token\n"
        yield f"data: {{'index': {i}, 'content': 'Hello {i}'}}\n\n"

    # 发送完成事件
    yield f"event: completion\n"
    yield f"data: {{'status': 'completed'}}\n\n"

@app.get("/stream")
async def stream_events():
    return StreamingResponse(
        generate_sse_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

**关键点**:

1. 使用 `async def` 生成器函数
2. `StreamingResponse` 的 `media_type` 必须是 `text/event-stream`
3. 设置 `Cache-Control: no-cache` 防止缓存
4. 设置 `Connection: keep-alive` 保持连接

---

### 模块 2: FastAPI 流式响应实战 (3h)

#### AI Agent 流式对话架构

```
客户端 (React/Vue)
    ↓ POST /api/v1/agent/chat
    ↓ Authorization: Bearer <jwt>
FastAPI Router
    ↓ JWT 验证
    ↓ 提取 Trace Context
Agent 流式生成
    ↓ Token 逐个生成
    ↓ 工具调用事件
    ↓ 状态更新事件
SSE 格式化
    ↓ event: token
    ↓ event: tool
    ↓ event: completion
客户端实时渲染
```

---

#### 核心实现代码

**定义请求/响应模型**:

```python
from pydantic import BaseModel, Field
from typing import Literal

class ChatRequest(BaseModel):
    """对话请求"""
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: str | None = None
    stream: bool = True

class SSEEvent(BaseModel):
    """SSE 事件"""
    event_type: Literal["connection", "token", "tool", "completion", "error"]
    data: dict
```

**实现流式路由**:

```python
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio
import time

router = APIRouter(prefix="/api/v1/agent")

async def generate_agent_events(message: str):
    """生成 Agent 流式事件"""
    try:
        # 1. 连接建立
        yield format_sse_event("connection", {"status": "connected"})

        # 2. 模拟 Token 流式生成
        tokens = ["根据", "您的", "问题", "，", "我", "理解", "为", "..."]
        for token in tokens:
            await asyncio.sleep(0.1)
            yield format_sse_event("token", {
                "content": token,
                "timestamp": time.time()
            })

        # 3. 工具调用事件
        yield format_sse_event("tool", {
            "tool_name": "search_knowledge",
            "status": "started"
        })

        await asyncio.sleep(0.5)

        yield format_sse_event("tool", {
            "tool_name": "search_knowledge",
            "status": "completed",
            "result": "找到 3 条相关记录"
        })

        # 4. 完成事件
        yield format_sse_event("completion", {
            "status": "success",
            "total_tokens": len(tokens)
        })

    except Exception as e:
        yield format_sse_event("error", {
            "message": str(e),
            "type": type(e).__name__
        })

def format_sse_event(event_type: str, data: dict) -> str:
    """格式化 SSE 事件"""
    return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

@router.post("/chat")
async def chat_stream(request: Request, chat_request: ChatRequest):
    """Agent 流式对话接口"""
    if not chat_request.stream:
        raise HTTPException(status_code=400, detail="必须启用流式模式")

    return StreamingResponse(
        generate_agent_events(chat_request.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
```

---

### 模块 3: JWT 认证与 OpenTelemetry 集成 (2h)

#### JWT 认证集成

复用 L64 的 JWT 认证逻辑：

```python
from fastapi import Depends, Header
from typing import Annotated

async def get_current_user(
    authorization: str = Header(None)
) -> dict:
    """验证 JWT Token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="缺少认证 Token")

    token = authorization.replace("Bearer ", "")
    # 调用 L64 的验证逻辑
    user_data = await verify_jwt_token(token)
    return user_data

@router.post("/chat")
async def chat_stream(
    request: Request,
    chat_request: ChatRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """需要认证的流式接口"""
    user_id = current_user["user_id"]

    return StreamingResponse(
        generate_agent_events(chat_request.message, user_id),
        media_type="text/event-stream",
    )
```

---

#### OpenTelemetry 追踪

**提取和传递 Trace Context**:

```python
from opentelemetry import trace
from opentelemetry.propagate import extract

async def generate_agent_events(message: str, user_id: str):
    """带追踪的事件生成"""
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("agent_stream") as span:
        span.set_attribute("user_id", user_id)
        span.set_attribute("message_length", len(message))

        yield format_sse_event("connection", {
            "status": "connected",
            "trace_id": span.get_span_context().trace_id
        })

        # 流式生成...
        async for token in generate_tokens(message):
            with tracer.start_as_current_span("generate_token"):
                yield format_sse_event("token", {"content": token})

        yield format_sse_event("completion", {"status": "success"})
```

**完整的追踪实现**:

```python
from opentelemetry import trace
from opentelemetry.propagate import extract, inject

def extract_trace_context(request: Request) -> dict:
    """从请求头提取 Trace Context"""
    carrier = dict(request.headers)
    context = extract(carrier)
    return context

def inject_trace_context() -> dict:
    """注入 Trace Context 到响应"""
    carrier = {}
    inject(carrier)
    return carrier

@router.post("/chat")
async def chat_stream(request: Request, chat_request: ChatRequest):
    # 提取 Trace Context
    context = extract_trace_context(request)

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("chat_stream_endpoint", context=context):
        return StreamingResponse(
            generate_agent_events(chat_request.message),
            media_type="text/event-stream",
        )
```

---

### 模块 4: 客户端集成 (2h)

#### JavaScript 客户端

```javascript
class AgentClient {
  constructor(baseUrl, token) {
    this.baseUrl = baseUrl;
    this.token = token;
  }

  async chat(message, onEvent) {
    const response = await fetch(`${this.baseUrl}/api/v1/agent/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.token}`,
      },
      body: JSON.stringify({ message, stream: true }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let currentEvent = null;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();

      for (const line of lines) {
        if (line.startsWith("event:")) {
          currentEvent = line.replace("event:", "").trim();
        } else if (line.startsWith("data:")) {
          const dataStr = line.replace("data:", "").trim();
          if (dataStr && currentEvent) {
            const data = JSON.parse(dataStr);
            onEvent(currentEvent, data);
          }
        }
      }
    }
  }
}

// 使用示例
const client = new AgentClient("http://localhost:8000", "your-jwt-token");

await client.chat("Python 异步编程", (eventType, data) => {
  switch (eventType) {
    case "connection":
      console.log("✅ 连接建立");
      break;
    case "token":
      process.stdout.write(data.content);
      break;
    case "tool":
      console.log(`\n🔧 工具: ${data.tool_name} - ${data.status}`);
      break;
    case "completion":
      console.log("\n✅ 完成");
      break;
    case "error":
      console.error("\n❌ 错误:", data.message);
      break;
  }
});
```

---

#### React Hook 实现

```typescript
import { useState, useCallback } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

function useAgentChat(baseUrl: string, token: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    setIsStreaming(true);
    setError(null);

    // 添加用户消息
    setMessages(prev => [...prev, { role: 'user', content }]);

    // 添加空的 assistant 消息
    setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

    try {
      const response = await fetch(`${baseUrl}/api/v1/agent/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ message: content, stream: true }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let currentEvent = null;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop()!;

        for (const line of lines) {
          if (line.startsWith('event:')) {
            currentEvent = line.replace('event:', '').trim();
          } else if (line.startsWith('data:')) {
            const dataStr = line.replace('data:', '').trim();
            if (dataStr && currentEvent === 'token') {
              const data = JSON.parse(dataStr);

              setMessages(prev => {
                const updated = [...prev];
                const lastMsg = updated[updated.length - 1];
                updated[updated.length - 1] = {
                  ...lastMsg,
                  content: lastMsg.content + data.content,
                };
                return updated;
              });
            } else if (currentEvent === 'error') {
              const data = JSON.parse(dataStr);
              setError(data.message);
            }
          }
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误');
    } finally {
      setIsStreaming(false);
    }
  }, [baseUrl, token]);

  return { messages, isStreaming, error, sendMessage };
}

// 组件中使用
function ChatComponent() {
  const { messages, isStreaming, error, sendMessage } = useAgentChat(
    'http://localhost:8000',
    'your-jwt-token'
  );

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i} className={msg.role}>
          {msg.content}
        </div>
      ))}
      {error && <div className="error">{error}</div>}
      {isStreaming && <div className="loading">生成中...</div>}
    </div>
  );
}
```

---

## 📝 练习题

### 综合练习: Agent SSE 流式路由

**文件**: `exercises/exercise_01.py`

本练习整合了 SSE 流式路由的核心功能，包括：

1. **基础 SSE 实现**：每秒推送当前时间
2. **JWT 保护的流式接口**：添加认证机制
3. **错误处理与超时控制**：实现优雅的错误处理

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
from datetime import datetime

app = FastAPI()

@app.get("/time")
async def stream_time():
    """实现流式时间推送

    要求:
    - 每秒推送一次当前时间
    - 推送 10 次后自动结束
    - 使用标准 SSE 格式
    """
    # 你的代码
    pass

@app.post("/protected/stream")
async def protected_stream():
    """实现受保护的流式接口

    要求:
    - 添加 JWT Token 验证
    - 验证 Bearer Token 格式
    """
    # 你的代码
    pass

async def generate_events_with_error_handling(timeout: int = 30):
    """实现错误处理和超时控制

    要求:
    - 捕获所有异常并发送 error 事件
    - 实现超时控制（30 秒）
    - 客户端断开连接时优雅退出
    """
    try:
        # 你的代码
        pass
    except asyncio.TimeoutError:
        # 超时处理
        pass
    except asyncio.CancelledError:
        # 取消处理
        pass
    except Exception as e:
        # 其他错误处理
        pass
```

---

## 🎯 总结

### 核心知识点

1. ✅ **SSE 协议**: `event`/`data`/`id`/`retry` 格式规范
2. ✅ **FastAPI StreamingResponse**: 实现流式响应
3. ✅ **JWT 认证**: 保护 SSE 端点安全
4. ✅ **OpenTelemetry**: 分布式链路追踪
5. ✅ **错误处理**: 异常捕获与优雅降级
6. ✅ **客户端集成**: JavaScript/TypeScript/React 实现

### 学习成果

完成本课程后，你应该能够：

- ✅ 理解 SSE 协议的工作原理
- ✅ 使用 FastAPI 构建流式 API
- ✅ 集成 JWT 认证保护接口
- ✅ 实现完整的错误处理机制
- ✅ 在前端实现 SSE 客户端

### 下一步

- [ ] 完成所有练习题（3 个）
- [ ] 运行测试套件：`pytest tests/ -v`
- [ ] 阅读 README.md 了解项目集成
- [ ] 进入 L38（RAG 智能代理）

---

## 📚 参考资料

- [MDN: Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [SSE vs WebSocket](https://ably.com/topic/server-sent-events-vs-websockets)

---

**作者**: Python 3.13 全栈课程团队
