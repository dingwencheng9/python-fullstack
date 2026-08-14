# L33: SSE 服务器推送事件

> 🔧 **Stage 3 Web 基础核心课** | ⏱️ 4-5 小时 | ⭐⭐⭐⭐☆（高级）  
> 前置课程：L27 FastAPI、L19 异步编程、L26 HTTP 长连接  
> 关键词：Server-Sent Events、SSE、HTTP 长连接、实时推送、EventSource、异步流、进度通知

## 📋 课程定位

SSE 是"轻量级实时通信"的首选方案。相比 WebSocket，SSE 更简单、更适合服务器到客户端的单向推送。本课程让你掌握 SSE 实战技能。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 理解 SSE 与 WebSocket 的适用场景差异
- [ ] 使用 FastAPI 实现 SSE 端点
- [ ] 处理 SSE 连接的生命周期（建立、保持心跳、断开）
- [ ] 实现多客户端管理与广播
- [ ] 处理断线重连与消息补偿
- [ ] 使用 SSE 实现实时进度通知
- [ ] 优化 SSE 的性能与资源占用

## 📂 课程结构

```text
L33-sse/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── app.py                  # SSE 基础应用
│   ├── app_v2.py              # SSE 进阶应用
│   ├── agent_chat_router.py    # Agent 聊天路由
│   ├── agent_chat_router_v2.py # Agent 聊天路由 v2
│   ├── checkpoint_system.py   # 检查点系统
│   ├── cli_client.py          # CLI 客户端
│   ├── cli_client_v2.py       # CLI 客户端 v2
│   ├── frontend.html           # 前端页面
│   └── token_control.py       # Token 控制
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L33-sse
uv sync
uv run pytest tests -v
uv run uvicorn examples.sse_app:app --reload
```

## 🔗 下一步

完成本课后继续学习：

- [L34: WebSocket 实时通信](../L34-websocket/README.md)

> 📖 **学习路径提示**：L34 将学习 WebSocket，实现客户端与服务器的全双工实时通信。
