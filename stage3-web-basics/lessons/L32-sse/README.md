# L32: SSE 服务器推送事件

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
L32-sse/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_sse_basics.py
│   ├── 02_sse_broadcast.py
│   └── 03_progress_sse.py
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L32-sse
uv sync
uv run pytest tests -v
uv run uvicorn examples.sse_app:app --reload
```

## 🔗 后续课程

- **L33 WebSocket 实时通信**：学习全双工实时通信
- **L34 HTMX + FastAPI 全栈开发**：使用 HTMX 集成 SSE
