# L32: Docker 容器化基础

> 🔧 **Stage 3 Web 基础核心课** | ⏱️ 2-3 小时 | ⭐⭐☆☆☆（入门-中级）  
> 前置课程：L27 FastAPI、L28 SQL 基础  
> 关键词：Docker、镜像、容器、Registry、Dockerfile、Compose、环境隔离、CI/CD、微服务部署

## 📋 课程定位

容器化是现代应用部署的事实标准。本课程从 Docker 基础到实战，让你掌握容器化开发与部署能力。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 理解 Docker 核心概念（镜像、容器、Registry）
- [ ] 编写优化的 Dockerfile 构建应用镜像
- [ ] 使用 Docker Compose 编排多容器应用
- [ ] 配置数据卷实现数据持久化
- [ ] 使用 Docker 网络实现容器间通信
- [ ] 构建 CI/CD 流程中的 Docker 集成
- [ ] 优化镜像大小与构建速度

## 📂 课程结构

```text
L32-docker/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_check_dockerfile.py  # Dockerfile 检查
│   ├── 02_mock_compose.py      # Mock Compose
│   ├── 03_docker_commands.py    # Docker 命令
│   ├── Dockerfile.fastapi       # FastAPI Dockerfile
│   └── docker-compose.yml      # Compose 配置
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L32-docker
uv sync
uv run pytest tests -v
docker build -t myapp:latest .
docker compose up
```

## 🔗 下一步

完成本课后继续学习：

- [L33: SSE 服务器推送事件](../L33-sse/README.md)

> 📖 **学习路径提示**：L33 将学习 Server-Sent Events，实现服务器向客户端的实时推送。
