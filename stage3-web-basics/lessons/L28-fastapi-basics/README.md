# L28: FastAPI 可观测性与契约驱动

> 🔧 **Stage 3 Web 基础核心课** | ⏱️ 4-5 小时 | ⭐⭐⭐⭐☆（高级应用）  
> 前置课程：L26 HTTP 协议基础、L19 异步编程  
> 关键词：FastAPI、Pydantic、OpenAPI、Swagger、OpenTelemetry、可观测性、日志、追踪、契约测试

## 📋 课程定位

FastAPI 是现代 Python Web 框架的事实标准。本课程不仅教你 FastAPI 基础，更强调**可观测性**——让服务"可见、可追踪、可度量"，这是生产级 Web 服务的必备能力。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 使用 FastAPI 构建 CRUD RESTful API
- [ ] 定义 Pydantic 模型进行请求/响应验证
- [ ] 使用 OpenAPI/Swagger 自动生成 API 文档
- [ ] 配置日志系统实现结构化日志
- [ ] 使用 OpenTelemetry 实现分布式追踪
- [ ] 编写契约测试验证 API 行为
- [ ] 实现健康检查与就绪探针

## 📂 课程结构

```text
L28-fastapi-basics/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_fastapi_crud.py
│   ├── 02_pydantic_validation.py
│   ├── 03_openapi_docs.py
│   └── 04_observability.py
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L28-fastapi-basics
uv sync
uv run pytest tests -v
uv run uvicorn examples.main:app --reload
```

## 🔗 后续课程

- **L28 数据库基础与 SQL 入门**：为 FastAPI 添加数据库持久化
- **L32 SSE 服务器推送事件**：学习实时通信
- **L34 HTMX + FastAPI 全栈开发**：构建交互式 Web 应用
