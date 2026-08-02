# L33: WebSocket 实时通信

> **课程编号**: L33
> **所属阶段**: Stage 3 - Web 开发基础
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐☆（高级）
> **前置课程**: L19, L27, L32
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L27**: FastAPI 可观测性与契约驱动（理解路由和异步）
- **L32**: SSE 实时推送（理解单向通信）
- **L19**: 异步编程（理解异步 IO）

**推荐掌握**：

- **L27**: OpenTelemetry（理解链路追踪）

**如果你还没有学习以上课程，建议先完成前置课程。**

---

L32 我们学了 SSE（服务器单向推送）。WebSocket 是它的补充——全双工、双向通信。

## 第一章：WebSocket 协议基础

### 1.1 为什么需要 WebSocket？

**问题场景**：

```
多人在线协作编辑文档：

❌ SSE 方案（单向推送）：
- 服务器可以推送其他人的编辑 → 客户端
- 客户端无法高效发送自己的编辑 → 服务器
- 需要额外的 HTTP POST 接口
- 两套通信机制，复杂且低效

✅ WebSocket 方案（双向通信）：
- 客户端 ←→ 服务器 持久连接
- 任意方向都可以主动发送消息
- 低延迟、单一连接
- 协议开销小（无 HTTP 头）
```

---

### 1.2 WebSocket vs SSE

**技术对比**：

| 特性 | SSE | WebSocket |
|------|-----|-----------|
| **通信方向** | 单向（服务器→客户端） | 双向（客户端←→服务器） |
| **协议** | HTTP/1.1 或 HTTP/2 | WebSocket 协议（ws://） |
| **数据格式** | 文本（必须） | 文本或二进制 |
| **自动重连** | ✅ 内置 | ❌ 需手动实现 |
| **事件 ID** | ✅ 支持断点续传 | ❌ 需自己实现 |
| **浏览器 API** | EventSource | WebSocket |
| **适用场景** | 通知、日志、AI 流式 | 聊天、游戏、协作编辑 |

**选择 WebSocket 的时机**：

- ✅ 需要客户端频繁发送消息
- ✅ 双向实时通信（聊天、游戏）
- ✅ 需要二进制数据传输
- ✅ 低延迟要求（<50ms）
- ✅ 协议开销敏感（大量小消息）

**选择 SSE 的时机**：

- ✅ 只需要服务器推送
- ✅ 需要自动重连
- ✅ 基于 HTTP（防火墙友好）
- ✅ AI Agent 流式对话

---

### 1.3 WebSocket 握手过程

**握手流程**：

```
1. 客户端发起 HTTP Upgrade 请求：

GET /ws HTTP/1.1
Host: localhost:8000
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
Sec-WebSocket-Version: 13

2. 服务器返回 101 Switching Protocols：

HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=

3. 握手完成，进入 WebSocket 帧通信模式
```

**关键字段**：

- `Upgrade: websocket`：请求协议升级
- `Sec-WebSocket-Key`：随机密钥（防劫持）
- `Sec-WebSocket-Accept`：密钥验证响应

---

### 1.4 WebSocket 帧格式

**帧结构**（简化）：

```
+-------+--------+----------+
| FIN   | Opcode | Payload  |
+-------+--------+----------+
| 1 bit | 4 bits | N bytes  |
+-------+--------+----------+
```

**Opcode（操作码）**：

- `0x1`：文本帧
- `0x2`：二进制帧
- `0x8`：关闭帧
- `0x9`：Ping 帧
- `0xA`：Pong 帧

**FastAPI 自动处理帧解析**，开发者只需关注消息内容。

---

## 第二章：FastAPI WebSocket 实现

### 2.1 基础 WebSocket 端点

**最小可用实现**：

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()                  # 1. 接受连接
    data = await websocket.receive_text()      # 2. 接收消息
    await websocket.send_text(f"收到: {data}")  # 3. 发送消息
```

**三步流程**：

1. `accept()`：完成握手
2. `receive_text()` / `receive_json()`：接收消息
3. `send_text()` / `send_json()`：发送消息

---

### 2.2 持续连接

**Echo 服务器**：

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/echo")
async def echo_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"回声: {data}")
    except WebSocketDisconnect:
        print("客户端断开连接")
```

**关键点**：

- `while True`：持续监听消息
- `WebSocketDisconnect`：捕获断开异常
- 异常后自动清理连接

---

### 2.3 连接管理

**多客户端广播**：

```python
from typing import Set

active_connections: set[WebSocket] = set()

@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # 广播给所有客户端（除自己）
            for conn in active_connections:
                if conn != websocket:
                    await conn.send_text(data)
    except WebSocketDisconnect:
        active_connections.discard(websocket)
```

**注意事项**：

- 使用 `set` 管理活跃连接
- 断开时从 `set` 移除
- 广播时排除发送者（可选）

---

## 第三章：聊天室实战

### 3.1 完整聊天服务器

**聊天室管理器**：

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import json
from datetime import datetime

app = FastAPI()

class ChatRoom:
    """多房间聊天管理器"""
    def __init__(self):
        self.rooms: dict[str, set[WebSocket]] = {}

    async def join(self, room: str, ws: WebSocket, username: str):
        """加入房间"""
        if room not in self.rooms:
            self.rooms[room] = set()

        self.rooms[room].add(ws)

        await self.broadcast(room, {
            "type": "system",
            "message": f"{username} 加入聊天室",
            "online": len(self.rooms[room]),
            "timestamp": datetime.now().isoformat()
        })

    async def leave(self, room: str, ws: WebSocket, username: str):
        """离开房间"""
        if room not in self.rooms:
            return

        self.rooms[room].discard(ws)

        if not self.rooms[room]:
            del self.rooms[room]
        else:
            await self.broadcast(room, {
                "type": "system",
                "message": f"{username} 离开聊天室",
                "online": len(self.rooms[room])
            })

    async def broadcast(self, room: str, message: dict):
        """广播消息到房间"""
        if room not in self.rooms:
            return

        message_json = json.dumps(message, ensure_ascii=False)

        for ws in self.rooms[room]:
            try:
                await ws.send_text(message_json)
            except Exception:
                # 发送失败的连接会在主循环中清理
                pass

chat = ChatRoom()

@app.websocket("/ws/chat/{room}/{username}")
async def chat_websocket(websocket: WebSocket, room: str, username: str):
    """聊天室 WebSocket 端点"""
    await websocket.accept()
    await chat.join(room, websocket, username)

    try:
        while True:
            msg = await websocket.receive_text()

            await chat.broadcast(room, {
                "type": "message",
                "username": username,
                "message": msg,
                "timestamp": datetime.now().isoformat()
            })
    except WebSocketDisconnect:
        await chat.leave(room, websocket, username)
```

**功能特性**：

- ✅ 多房间支持
- ✅ 用户名识别
- ✅ 加入/离开通知
- ✅ 在线人数统计
- ✅ 消息时间戳
- ✅ 结构化消息（JSON）

---

### 3.2 测试聊天室

**启动服务器**：

```bash
# 启动 FastAPI
uvicorn examples.01_chat_server:app --reload
```

**使用 websocat 测试**：

```bash
# 终端 1: Alice 加入 general 房间
websocat ws://localhost:8000/ws/chat/general/Alice

# 终端 2: Bob 加入 general 房间
websocat ws://localhost:8000/ws/chat/general/Bob
```

**预期输出**：

```json
// Alice 看到
{"type": "system", "message": "Alice 加入聊天室", "online": 1}
{"type": "system", "message": "Bob 加入聊天室", "online": 2}

// Bob 看到
{"type": "system", "message": "Bob 加入聊天室", "online": 2}
```

---

## 第四章：客户端实现

### 4.1 Python 客户端

**使用 websockets 库**：

```python
import asyncio
import websockets
import json

async def chat_client(room: str, username: str):
    uri = f"ws://localhost:8000/ws/chat/{room}/{username}"

    async with websockets.connect(uri) as ws:
        # 接收消息（后台任务）
        async def receive_messages():
            async for message in ws:
                data = json.loads(message)
                print(f"[{data['type']}] {data.get('username', 'System')}: {data['message']}")

        # 发送消息（主线程）
        async def send_messages():
            while True:
                msg = await asyncio.to_thread(input, ">>> ")
                await ws.send(msg)

        # 并发执行
        await asyncio.gather(
            receive_messages(),
            send_messages()
        )

asyncio.run(chat_client("general", "Alice"))
```

---

### 4.2 浏览器 JavaScript 客户端

**原生 WebSocket API**：

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/chat/general/Alice");

ws.onopen = () => {
  console.log("✅ 已连接");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`[${data.type}] ${data.username}: ${data.message}`);
};

ws.onclose = () => {
  console.log("❌ 已断开");
};

ws.onerror = (error) => {
  console.error("⚠️ 错误:", error);
};

// 发送消息
function sendMessage(msg) {
  ws.send(msg);
}
```

---

### 4.3 React Hook 实现

**useWebSocket Hook**：

```typescript
import { useState, useEffect, useCallback } from 'react';

interface Message {
  type: 'system' | 'message';
  username?: string;
  message: string;
  timestamp: string;
}

function useWebSocket(url: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const websocket = new WebSocket(url);

    websocket.onopen = () => {
      setIsConnected(true);
    };

    websocket.onmessage = (event) => {
      const data: Message = JSON.parse(event.data);
      setMessages(prev => [...prev, data]);
    };

    websocket.onclose = () => {
      setIsConnected(false);
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, [url]);

  const sendMessage = useCallback((message: string) => {
    if (ws && isConnected) {
      ws.send(message);
    }
  }, [ws, isConnected]);

  return { messages, isConnected, sendMessage };
}

// 组件中使用
function ChatComponent() {
  const { messages, isConnected, sendMessage } = useWebSocket(
    'ws://localhost:8000/ws/chat/general/Alice'
  );

  return (
    <div>
      <div className="status">
        {isConnected ? '✅ 已连接' : '❌ 未连接'}
      </div>
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={msg.type}>
            {msg.username && <strong>{msg.username}: </strong>}
            {msg.message}
          </div>
        ))}
      </div>
      <input
        onKeyPress={(e) => {
          if (e.key === 'Enter') {
            sendMessage(e.currentTarget.value);
            e.currentTarget.value = '';
          }
        }}
      />
    </div>
  );
}
```

---

## 第五章：生产级优化

### 5.1 断线重连

**客户端自动重连**：

```javascript
class ReconnectingWebSocket {
  constructor(url, options = {}) {
    this.url = url;
    this.reconnectDelay = options.reconnectDelay || 1000;
    this.maxReconnectDelay = options.maxReconnectDelay || 30000;
    this.reconnectAttempts = 0;
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log("✅ 已连接");
      this.reconnectAttempts = 0;
      this.onopen?.();
    };

    this.ws.onmessage = (event) => {
      this.onmessage?.(event);
    };

    this.ws.onclose = () => {
      console.log("❌ 连接断开，尝试重连...");
      this.scheduleReconnect();
    };

    this.ws.onerror = (error) => {
      console.error("⚠️ 错误:", error);
    };
  }

  scheduleReconnect() {
    const delay = Math.min(
      this.reconnectDelay * Math.pow(2, this.reconnectAttempts),
      this.maxReconnectDelay
    );

    this.reconnectAttempts++;

    setTimeout(() => {
      console.log(`尝试重连 (第 ${this.reconnectAttempts} 次)...`);
      this.connect();
    }, delay);
  }

  send(data) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(data);
    }
  }

  close() {
    this.shouldReconnect = false;
    this.ws.close();
  }
}

// 使用
const ws = new ReconnectingWebSocket('ws://localhost:8000/ws/chat/general/Alice');
ws.onmessage = (event) => console.log(event.data);
```

**关键特性**：

- ✅ 指数退避重连（1s → 2s → 4s → ... → 30s）
- ✅ 自动重连
- ✅ 重连次数计数

---

### 5.2 心跳检测

**服务器端心跳**：

```python
import asyncio

async def heartbeat_task(websocket: WebSocket):
    """心跳检测任务"""
    try:
        while True:
            await asyncio.sleep(30)
            await websocket.send_json({"type": "ping"})
    except WebSocketDisconnect:
        pass

@app.websocket("/ws/chat/{room}/{username}")
async def chat_websocket(websocket: WebSocket, room: str, username: str):
    await websocket.accept()
    await chat.join(room, websocket, username)

    # 启动心跳任务
    heartbeat = asyncio.create_task(heartbeat_task(websocket))

    try:
        while True:
            msg = await websocket.receive_text()

            # 处理 pong 响应
            if msg == "pong":
                continue

            await chat.broadcast(room, {
                "type": "message",
                "username": username,
                "message": msg,
            })
    except WebSocketDisconnect:
        heartbeat.cancel()
        await chat.leave(room, websocket, username)
```

**客户端响应**：

```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === 'ping') {
    ws.send('pong');
    return;
  }

  // 处理正常消息
  console.log(data);
};
```

---

### 5.3 JWT 认证

**WebSocket 鉴权**：

```python
from fastapi import Cookie, WebSocket, status

async def verify_jwt_token(token: str) -> dict:
    """验证 JWT Token（复用 L35 逻辑）"""
    # 这里应该调用真实的 JWT 验证
    # 参考 L35: 安全网关
    return {"user_id": "demo_user", "username": "alice"}

@app.websocket("/ws/chat/{room}")
async def auth_chat_websocket(
    websocket: WebSocket,
    room: str,
    token: str = Cookie(None)
):
    """带认证的 WebSocket 端点"""
    # 1. 验证 Token
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        user_data = await verify_jwt_token(token)
        username = user_data["username"]
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # 2. Token 有效，接受连接
    await websocket.accept()
    await chat.join(room, websocket, username)

    # 3. 正常处理消息
    try:
        while True:
            msg = await websocket.receive_text()
            await chat.broadcast(room, {
                "type": "message",
                "username": username,
                "message": msg,
            })
    except WebSocketDisconnect:
        await chat.leave(room, websocket, username)
```

**客户端传递 Token**：

```javascript
// 方式 1: Query String
const ws = new WebSocket(`ws://localhost:8000/ws/chat/general?token=${jwtToken}`);

// 方式 2: Cookie（需要服务器设置）
document.cookie = `token=${jwtToken}; path=/`;
const ws = new WebSocket('ws://localhost:8000/ws/chat/general');
```

---

### 5.4 广播性能优化

**并发广播**：

```python
import asyncio

async def broadcast_concurrent(connections: set[WebSocket], message: str):
    """并发广播（提高性能）"""
    tasks = [
        conn.send_text(message)
        for conn in connections
    ]

    # 并发发送，忽略失败的连接
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 统计失败的连接
    failed = sum(1 for r in results if isinstance(r, Exception))
    if failed > 0:
        print(f"⚠️ {failed} 个连接发送失败")
```

**性能对比**：

- **串行广播**：1000 个连接 × 10ms = 10 秒
- **并发广播**：1000 个连接 ÷ 100 并发 × 10ms = 100ms

---

## 📝 本章总结

### 核心知识点

1. **WebSocket 协议**：全双工、持久连接、握手流程
2. **FastAPI 实现**：`@app.websocket` + accept + receive/send
3. **连接管理**：set 存储活跃连接，广播消息
4. **聊天室实战**：多房间、用户识别、系统通知
5. **客户端集成**：Python websockets / 浏览器 WebSocket API
6. **生产优化**：断线重连、心跳检测、JWT 认证

### 关键要点

- ✅ WebSocket 适合双向通信场景
- ✅ 握手阶段基于 HTTP Upgrade
- ✅ 使用 `set` 管理多客户端连接
- ✅ 捕获 `WebSocketDisconnect` 清理连接
- ✅ 客户端需要自己实现重连机制

### 常见陷阱

- ❌ 忘记 `await websocket.accept()`（握手失败）
- ❌ 广播时不排除发送者（重复消息）
- ❌ 未捕获 `WebSocketDisconnect`（连接泄漏）
- ❌ 串行广播导致性能问题（应并发）
- ❌ 没有心跳检测（无法发现僵尸连接）

### 实用技巧

- 💡 使用 `asyncio.create_task` 启动后台心跳
- 💡 广播时用 `asyncio.gather` 并发发送
- 💡 消息使用 JSON 格式（结构化）
- 💡 客户端实现指数退避重连
- 💡 测试时用 `websocat` 命令行工具

### 典型应用场景

- 💬 实时聊天应用
- 🎮 多人在线游戏
- 📝 协作编辑（Google Docs）
- 📊 实时数据看板（Grafana）
- 🔔 推送通知系统

### 下一步

继续学习 [L34: HTMX 全栈开发](../L34-htmx/README.md)，探索另一种 Web 交互方式。
