# L34: WebSocket 实时通信

> 🔧 **Stage 3 Web 基础核心课** | ⏱️ 3-4 小时 | ⭐⭐⭐⭐☆（高级）  
> 前置课程：L27 FastAPI、L32 SSE、L19 异步编程  
> 关键词：WebSocket、握手协议、全双工通信、连接管理、消息协议、心跳检测、断线重连

## 📋 课程定位

WebSocket 是"全双工实时通信"的标准方案。本课程深入 WebSocket 协议原理与 FastAPI 实现，让你掌握实时交互应用的核心技术。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 理解 WebSocket 与 HTTP SSE 的核心差异
- [ ] 实现 WebSocket 握手与连接管理
- [ ] 使用 FastAPI WebSocket 端点进行双向通信
- [ ] 实现心跳检测与断线重连
- [ ] 设计消息协议（JSON/二进制/自定义）
- [ ] 实现聊天室等多人实时应用
- [ ] 处理高并发 WebSocket 连接

## 📂 课程结构

```text
L34-websocket/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_chat_server.py       # WebSocket 聊天服务器
│   └── 02_client.py           # WebSocket 客户端
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L34-websocket
uv sync
uv run pytest tests -v
uv run uvicorn examples.ws_app:app --reload
```

## 🔗 后续课程

- **L34 HTMX + FastAPI 全栈开发**：综合运用实时通信技术
- **L35 Web 基础综合项目**：构建完整实时应用
