# Stage 4: Web 开发进阶

> **阶段编号**: Stage 4  
> **课程数量**: 11 课 (L36-L46)  
> **预计学时**: ~60 小时  
> **前置要求**: Stage 3（Web 开发基础）

---

## 📚 课程列表

| 编号 | 课程名称 | 学时 | 难度 |
|------|----------|------|------|
| L36 | [异步背压机制](lessons/L36-async-backpressure/) | 6h | ⭐⭐⭐⭐ |
| L37 | [Web 安全完整实践](lessons/L37-web-security-complete/) | 4h | ⭐⭐⭐⭐ |
| L38 | [认证与授权](lessons/L38-auth-authorization/) | 6h | ⭐⭐⭐⭐ |
| L39 | [E2E 测试工程化](lessons/L39-e2e-testing/) | 5h | ⭐⭐⭐⭐ |
| L40 | [消息队列](lessons/L40-message-queue/) | 5h | ⭐⭐⭐⭐ |
| L41 | [API 性能优化](lessons/L41-api-performance/) | 5h | ⭐⭐⭐⭐ |
| L42 | [缓存策略深入](lessons/L42-caching-strategy/) | 5h | ⭐⭐⭐⭐ |
| L43 | [异步任务处理](lessons/L43-async-tasks/) | 5h | ⭐⭐⭐⭐ |
| L44 | [微服务架构基础](lessons/L44-microservices-basics/) | 5h | ⭐⭐⭐⭐ |
| L45 | [分布式系统实战](lessons/L45-distributed-systems/) | 5h | ⭐⭐⭐⭐ |
| L46 | [WebSocket 高级应用](lessons/L46-websocket-advanced/) | 5h | ⭐⭐⭐⭐ |

---

## 🎯 学习路径

```
L36 异步背压 → L37 Web 安全 → L38 认证授权
       ↓              ↓               ↓
L39 E2E 测试 ← L40 消息队列 → L41 API 性能
       ↓              ↓               ↓
L42 缓存策略 → L43 异步任务 → L44 微服务
                   ↓
        L45 分布式系统 → L46 WebSocket 高级
```

---

## 📖 学习目标

完成 Stage 4 后，你将掌握：

1. **异步系统保护** — 背压机制、限流、熔断、排队策略、生产监控
2. **Web 安全加固** — 防御性编程、CORS、CSRF、XSS、SQL 注入防护
3. **身份认证与授权** — JWT、OAuth 2.0、RBAC、ABAC 权限模型
4. **端到端测试** — Playwright、集成测试、Mock 与 Stub、性能测试
5. **消息队列架构** — Redis Streams、RabbitMQ、事件驱动、微服务通信
6. **API 性能优化** — 数据库索引、查询优化、N+1 问题、连接池管理
7. **缓存策略** — Redis 缓存、缓存失效策略、分布式缓存、本地缓存
8. **异步任务处理** — Celery、后台任务、定时任务、任务队列
9. **微服务架构** — 服务拆分、API 网关、服务发现、容器编排
10. **分布式系统** — 一致性、CAP 定理、分布式事务、容错处理
11. **实时通信高级** — WebSocket 集群、Socket.IO、性能调优

---

## 🛠️ 环境要求

- **Python 版本**: 3.13.x
- **包管理**: uv
- **数据库**: PostgreSQL + Redis
- **消息队列**: Redis Streams / RabbitMQ
- **测试框架**: pytest + Playwright
- **容器化**: Docker + Docker Compose

```bash
# 安装依赖
uv sync

# 运行测试（全阶段）
uv run pytest stage4-web-advanced/lessons/ -v

# 运行单个课程测试
uv run pytest stage4-web-advanced/lessons/L36-async-backpressure/tests/ -v
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

- **前置**: [Stage 3: Web 开发基础](../stage3-web-basics/)
- **后续**: [Stage 5: 数据工程](../stage5-data-engineering/)

---

## 📊 统计数据

| 指标 | 数值 |
|------|------|
| 课程数量 | 11 |
| 示例代码 | ~110 个 |
| 练习题 | ~55 个 |
| 测试用例 | 1600+ |
| 预计学时 | ~60 小时 |

---

## 🏆 完成标准

- [ ] 完成所有 11 个课程的学习
- [ ] 通过所有课程测试（1600+ 测试用例）
- [ ] 完成所有练习题
- [ ] 理解每个课程的核心概念
- [ ] 能够独立构建高可用 Web 应用
- [ ] 掌握微服务架构与分布式系统设计

---
