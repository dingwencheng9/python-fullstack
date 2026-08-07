# P04: Web 基础综合项目

> 🔧 **Stage 3 Web 基础收官课** | ⏱️ 10-12 小时 | ⭐⭐⭐⭐⭐（综合）  
> 前置课程：L26-L34（HTTP、FastAPI、SQL、Docker、SSE、WebSocket、HTMX）  
> 关键词：全栈项目、综合实战、架构设计、API 设计、数据库设计、前后端集成、容器化部署

## 📋 课程定位

Stage 3 的收官之作。本课程带你从零构建一个完整的 Web 应用，综合运用 HTTP、FastAPI、SQL、容器化、实时通信等技术，建立全栈开发能力。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 从需求出发设计完整的 Web 应用架构
- [ ] 设计规范的 RESTful API 接口
- [ ] 设计合理的数据库模型
- [ ] 实现用户认证与权限控制
- [ ] 使用 SSE/WebSocket 实现实时功能
- [ ] 使用 HTMX 实现无刷新交互
- [ ] 使用 Docker 容器化部署应用
- [ ] 编写项目文档与测试

## 📂 课程结构

```text
P04-web-project/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_project_structure.py
│   ├── 02_models.py
│   ├── 03_api_endpoints.py
│   └── 04_frontend.py
├── exercises/             # 练习题（项目扩展）
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/P04-web-project
uv sync
uv run pytest tests -v
docker compose up
```

## 🧭 建议学习顺序

1. 阅读 `lesson.md` 理解项目需求与架构设计
2. 按照章节逐步实现：数据库模型 → API 端点 → 前端页面
3. 实现认证与权限控制
4. 添加实时功能（SSE/WebSocket）
5. 使用 HTMX 增强交互
6. 容器化部署

## 🔗 后续课程

- **L36 异步背压机制**：为 Web 应用添加生产级流控
- **L37 Web 安全完整指南**：在项目中加入安全防护
- **L38 E2E 测试**：为项目添加端到端测试
