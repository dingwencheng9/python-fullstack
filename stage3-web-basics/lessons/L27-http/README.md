# L27: HTTP 协议与抓包基础

> 🔧 **Stage 3 Web 基础核心课** | ⏱️ 3-4 小时 | ⭐⭐⭐☆☆（中级）  
> 前置课程：L25 工程化综合项目  
> 关键词：HTTP、TCP/IP、TCP 三次握手、四次挥手、状态码、请求方法、Header、Cookie、Session、TLS/HTTPS、抓包工具

## 📋 课程定位

HTTP 是 Web 开发的根基。不理解 HTTP，就无法理解 Web 应用的运行原理。本课程从协议演进到抓包实践，建立"看得见、摸得着"的 HTTP 认知体系。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 解释 HTTP/1.0、HTTP/1.1、HTTP/2、HTTP/3 的演进差异
- [ ] 分析 TCP 三次握手与四次挥手的过程
- [ ] 解读 HTTP 请求/响应的结构（Start Line、Headers、Body）
- [ ] 区分 GET/POST/PUT/DELETE 等请求方法的使用场景
- [ ] 使用抓包工具（如 Wireshark/mitmproxy）分析真实流量
- [ ] 理解 Cookie、Session、JWT 的认证机制差异
- [ ] 分析 HTTPS 的 TLS 握手过程

## 📂 课程结构

```text
L27-http/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_http_methods.py
│   ├── 02_headers.py
│   └── 03_cookie_session.py
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L27-http
uv sync
uv run pytest tests -v
```

## 🔗 后续课程

- **L27 FastAPI 可观测性与契约驱动**：在理解 HTTP 基础上学习 RESTful API 设计
- **L28 数据库基础与 SQL 入门**：理解 HTTP 后端的数据持久化层
