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
│   ├── 03_fastapi_basics.py       # FastAPI 基础
│   ├── 04_pydantic_basics.py      # Pydantic 基础
│   ├── 05_dependency_injection.py # 依赖注入
│   ├── async_taskgroup.py          # 异步任务组
│   ├── contract_first_api.py      # 契约优先 API
│   ├── loguru_demo.py             # 日志演示
│   ├── middleware_demo.py         # 中间件演示
│   ├── opentelemetry_demo.py      # 可观测性演示
│   └── prometheus_metrics.py      # 指标监控
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

## 🔗 下一步

完成本课后继续学习：

- [L29: SQL 基础与数据库入门](../L29-sql-basics/README.md)

> 📖 **学习路径提示**：L29 将学习 SQL 基础和数据库操作。
