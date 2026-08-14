# L64: Agent 部署与监控

> **课程编号**: L64  
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 4-5 小时  
> **难度**: ⭐⭐⭐⭐☆ (中高级)

---

## 📚 课程概览

- **位置**: Stage 5 / 第 8 课
- **学习时长**: 4-5 小时
- **难度**: ⭐⭐⭐⭐☆
- **前置课程**: L57 Agent 评估与调试
- **后续课程**: Stage 5 完结
- **课程主题**: 把 Agent 封装为可部署、可监控、可运维的生产服务

本 README 是课程入口地图。详细概念、代码讲解和练习说明以 `lesson.md` 为准；这里帮助你快速判断学习顺序、运行路径和完成标准。

## 🎯 学习目标

完成本课程后，你将掌握：

1. ✅ 使用 FastAPI、Pydantic 和异步接口封装 Agent 服务
2. ✅ 实现 SSE 流式响应、健康检查和错误处理
3. ✅ 使用 Docker、docker-compose 和 Kubernetes 部署服务
4. ✅ 接入 Prometheus、Grafana、告警和结构化日志
5. ✅ 实现优雅关闭、限流、降级和生产部署检查清单

## 📋 前置知识

- 完成 L48-L54，具备完整 Agent 开发、评估和调试经验
- 熟悉 FastAPI、Pydantic、异步函数和 HTTP API
- 了解 Docker 镜像、容器、环境变量和 Compose
- 理解 Prometheus 指标、Grafana 面板和 Kubernetes 基础概念

## 🗂️ 文件导航

| 文件                                    | 用途                        |
| --------------------------------------- | --------------------------- |
| `lesson.md`                             | 详细教程（678 行）          |
| `examples/01_deployment_monitoring.py`  | 演示本课核心 API 和完整流程 |
| `exercises/01_deployment_monitoring.py` | 需要你补全的实践项目        |
| `solutions/01_deployment_monitoring.py` | 对应练习的参考实现          |
| `tests/conftest.py`                     | 验证示例、练习和边界行为    |
| `tests/test_l51_solutions.py`           | 验证示例、练习和边界行为    |

> 说明：表格只列出本课需要直接关注的文件，`.gitkeep`、`__pycache__` 等占位或缓存文件不列入学习路径。

## 💡 核心知识点摘要

### 第一章: FastAPI 封装

部署从稳定 API 开始。
课程定义请求/响应模型、异步聊天接口、SSE 流式响应和健康检查，让 Agent 能以标准 HTTP 服务形式被前端或其他系统调用。

### 第二章: 容器化部署

容器化保证环境一致。
课程覆盖 Dockerfile、docker-compose 和 Kubernetes Deployment/Service，强调镜像体积、环境变量、资源限制和可重复启动。

### 第三章: 监控与告警

生产服务必须可观测。
Prometheus 指标记录请求数、延迟、错误和 Token；Grafana 告警帮助在故障扩大前发现问题。
日志用于追踪单次请求。

### 第四章: 生产最佳实践

最后一章补齐运维细节：优雅关闭、限流、降级、结构化日志、健康检查和部署清单。
目标是服务失败时可控、可定位、可恢复。

### 最佳实践总结

本课最后的总结章节把教程内容收敛成可执行清单。学习时不要只复制示例代码，要把清单转化为自己的检查流程：输入是什么、输出是什么、失败时如何定位。

### 练习题定位

练习题用于把概念转成工程能力。建议先独立完成 `exercises/`，再对照 `solutions/` 检查边界处理、类型注解、错误信息和测试覆盖。

## 🚀 快速开始

_(详细代码见 lesson.md)_

## 📊 完成标准

- [ ] 阅读完 `lesson.md`，能复述每一章的核心问题
- [ ] 运行所有 `examples/` 脚本，并理解输出含义
- [ ] 完成 `exercises/` 练习，代码不依赖硬编码答案
- [ ] 对照 `solutions/`，修正命名、结构、边界处理和类型注解
- [ ] `pytest tests/ -v` 全部通过
- [ ] 能解释以下关键词：FastAPI、SSE、Docker、Kubernetes、Prometheus

## 🔗 下一步

完成本课后继续学习：

- [L65: Agent SSE 路由](../L65-agent-sse-router/README.md)

> 📖 **学习路径提示**：L65 将学习 Server-Sent Events 路由在 Agent 中的应用。

---

## 🔗 下一步

完成本课后继续学习：

- [L65: Agent SSE 流式路由](../L65-agent-sse-router/README.md)
- L65 会学习 SSE（Server-Sent Events）实现 Agent 的流式输出与路由。
