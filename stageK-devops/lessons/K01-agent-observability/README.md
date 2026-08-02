# K01 AI Agent 部署与可观测性

> **课程描述**: 从开发到生产的桥梁 — Docker 容器化、监控指标、分布式追踪与日志管理

## 📚 课程内容

本课程涵盖以下核心主题：

- Docker 多阶段构建与 Agent 容器化
- 环境配置与密钥管理
- Prometheus 指标采集
- OpenTelemetry 分布式追踪
- Grafana 仪表板配置
- 结构化日志与聚合

## 🚀 快速开始

```bash
# 进入课程目录
cd stageK-devops/lessons/K01-agent-observability

# 安装依赖
uv sync

# 运行示例
uv run python examples/01_dockerfile_agent.py
```

## 📁 目录结构

```
.
├── lesson.md        # 课程详细文档
├── examples/        # 示例代码
│   ├── 01_dockerfile_agent.py
│   ├── 02_environment_config.py
│   ├── 03_prometheus_metrics.py
│   ├── 04_otel_tracing.py
│   └── 05_structured_logging.py
├── exercises/       # 练习题
├── solutions/       # 参考解答
└── tests/           # 单元测试
```

## 🔗 前置课程

- [L65 RAG 向量数据库](../../../stage6-ai-agent/lessons/L57-rag-vector/) - 完整 RAG 系统
- [L64 Agent 部署与监控](../../../stage6-ai-agent/lessons/L64-agent-deployment/) - 基础部署概念

## 🔗 后续课程

- [K02 Kubernetes 基础](../K02-kubernetes-basics/) - K8s 编排

---

[← 返回课程总览](../../README.md)
