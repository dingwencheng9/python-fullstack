# P05: 实时协作 SaaS 平台

> **课程编号**: P05
> **所属阶段**: Stage 4 - Web 开发进阶
> **预计时长**: 8-12 小时
> **难度**: ⭐⭐⭐⭐⭐（专家级）
> **前置课程**: L36-L46（全部 Stage 4 课程）
> **版本**: v1.0
> **核心版本**: Python 3.13

---

## 🚀 快速开始

```bash
# 从仓库根目录进入本课
cd stage4-web-advanced/lessons/P05-realtime-collaboration

# 安装依赖
uv sync

# 运行示例
uv run python examples/01_project_structure.py

# 运行练习
uv run python exercises/exercise_01_auth_websocket.py

# 运行测试
uv run pytest tests/ -q
```

## 📚 学习路径

1. 阅读 [`lesson.md`](lesson.md)，理解项目架构和整合知识点。
2. 运行 `examples/*.py`，观察各模块实现。
3. 完成 [`exercises/`](exercises/) 目录下的练习。
4. 对照 [`solutions/`](solutions/) 优化实现。
5. 运行 `uv run pytest tests/ -q` 验证理解。

## 📁 目录结构

| 路径 | 用途 |
|------|------|
| [`examples/`](examples/) | 示例代码：认证、WebSocket、Redis、Celery |
| [`exercises/`](exercises/) | 练习题 |
| [`solutions/`](solutions/) | 参考答案 |
| [`tests/`](tests/) | 单元测试 |
| [`lesson.md`](lesson.md) | 完整课程文档 |

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解项目整体架构。
- [ ] 运行全部示例，理解各模块实现。
- [ ] 完成认证 + WebSocket 整合练习。
- [ ] 完成 Redis 缓存 + Celery 任务练习。
- [ ] 通过 `uv run pytest tests/ -q`。
- [ ] 可选：实现 E2E 测试。

---

## 🔗 前置课程回顾

| 课程 | 核心知识 | 本项目应用 |
|------|----------|-------------|
| L36 | 异步背压 | 限流保护 |
| L37 | Web 安全 | 安全头、依赖注入 |
| L38 | 认证授权 | JWT + RBAC |
| L39 | E2E 测试 | Playwright 测试 |
| L40 | 消息队列 | Redis PubSub |
| L41 | API 性能 | Profiling、缓存 |
| L42 | 缓存策略 | Redis 多级缓存 |
| L43 | 异步任务 | Celery 后台任务 |
| L44 | 微服务 | 服务拆分模式 |
| L45 | 分布式 | 一致性方案 |
| L46 | WebSocket | 实时通信 |

## 🎯 项目概述

**TaskCollab** - 实时任务协作平台

- ✅ 用户认证 (JWT + RBAC)
- ✅ 实时任务更新 (WebSocket)
- ✅ 团队协作 (频道/房间)
- ✅ 通知系统 (Celery + WebSocket)
- ✅ 性能监控 (缓存 + Profiling)
- ✅ 微服务架构雏形
