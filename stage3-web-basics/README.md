# Stage 3: Web 开发基础

> **阶段编号**: Stage 3  
> **课程数量**: 10 课 (L27-L35)  
> **预计学时**: ~56 小时  
> **前置要求**: Stage 2（现代化基础内功）

---

## 📚 课程列表

| 编号 | 课程名称 | 学时 | 难度 |
|------|----------|------|------|
| L27 | [HTTP 协议与抓包基础](lessons/L27-http/) | 3-4h | ⭐⭐⭐ |
| L28 | [FastAPI 可观测性与契约驱动](lessons/L28-fastapi-basics/) | 4-5h | ⭐⭐⭐⭐ |
| L29 | [数据库基础与 SQL 入门](lessons/L29-sql-basics/) | 4-5h | ⭐⭐⭐ |
| L30 | [异步数据持久化与事务原子性](lessons/L30-database-engineering/) | 4-5h | ⭐⭐⭐⭐ |
| L31 | [SQL 进阶](lessons/L31-sql-advanced/) | 4-5h | ⭐⭐⭐⭐ |
| L32 | [Docker 容器化部署](lessons/L32-docker/) | 2-3h | ⭐⭐⭐ |
| L33 | [SSE 服务器推送事件](lessons/L33-sse/) | 4-5h | ⭐⭐⭐⭐ |
| L34 | [WebSocket 实时通信](lessons/L34-websocket/) | 3-4h | ⭐⭐⭐⭐ |
| L35 | [HTMX + FastAPI 全栈开发](lessons/L35-htmx/) | 4h | ⭐⭐⭐⭐ |
| P04 | [Web 基础综合项目](lessons/P04-web-project/) | 10-12h | ⭐⭐⭐⭐⭐ |

---

## 🎯 学习路径

```
L27 HTTP 协议 → L28 FastAPI → L29 SQL 基础
         ↓              ↓               ↓
L30 异步持久化 → L31 SQL 进阶 → L32 Docker
         ↓              ↓               ↓
L33 SSE ← L34 WebSocket → L35 HTMX
                   ↓
          P04 Web 基础综合项目
```

---

## 📖 学习目标

完成 Stage 3 后，你将掌握：

1. **HTTP 协议深度理解** — 抓包调试、请求/响应结构、状态码、Header 语义
2. **现代 Web 框架** — FastAPI 路由、依赖注入、Pydantic 模型验证
3. **数据库编程** — SQL 基础、SQLAlchemy 2.0 ORM、事务管理、连接池
4. **异步数据处理** — 异步生成器、流式传输、SSE/WebSocket 实时通信
5. **容器化与部署** — Docker 镜像构建、多容器编排、容器网络
6. **全栈开发能力** — HTMX 渐进式增强、前后端分离、实时数据流
7. **Web 安全基础** — 认证授权、输入验证、常见攻防技巧
8. **性能优化意识** — 数据库索引、查询优化、缓存策略
9. **工程化实践** — 代码结构、测试覆盖、日志监控、错误处理
10. **综合项目经验** — 独立完成任务管理系统全栈项目

---

## 🛠️ 环境要求

- **Python 版本**: 3.13.x
- **包管理**: uv
- **数据库**: PostgreSQL (推荐) / SQLite (学习)
- **测试框架**: pytest
- **容器化**: Docker + Docker Compose

```bash
# 安装依赖
uv sync

# 运行测试（全阶段）
uv run pytest stage3-web-basics/lessons/ -v

# 运行单个课程测试
uv run pytest stage3-web-basics/lessons/L26-http/tests/ -v
```

---

## 📁 课程结构

每个课程包含：

```
L{XX}-课程名/
├── README.md           # 课程概览与快速开始
├── lesson.md           # 详细教学内容
├── examples/           # 示例代码（可直接运行）
├── exercises/          # 练习题模板
├── solutions/          # 参考解答
└── tests/              # 单元测试
```

---

## 🔗 衔接课程

- **前置**: [Stage 2: 现代化基础内功](../stage2-engineering/)
- **后续**: [Stage 4: Web 开发进阶](../stage4-web-advanced/)

---

## 📊 统计数据

| 指标 | 数值 |
|------|------|
| 课程数量 | 10 |
| 示例代码 | ~100 个 |
| 练习题 | ~50 个 |
| 测试用例 | 1500+ |
| 预计学时 | ~56 小时 |

---

## 🏆 完成标准

- [ ] 完成所有 10 个课程的学习
- [ ] 通过所有课程测试（1500+ 测试用例）
- [ ] 完成所有练习题
- [ ] 理解每个课程的核心概念
- [ ] 能够独立构建生产级 Web 应用
- [ ] 成功部署 Docker 化的全栈项目

---
