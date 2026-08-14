# L44: 微服务架构基础

> **课程编号**: L44
> **所属阶段**: Stage 4 - Web 开发进阶
> **课程时长**: 4 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: L36 异步背压, L40 消息队列

---

## 📚 课程概述

本课程讲解微服务架构的核心概念、设计模式和实现方法，涵盖服务拆分、API 网关、服务注册与发现等关键技术。

---

## 🎯 学习目标

1. 理解微服务架构的优势与挑战
2. 掌握服务拆分方法论
3. 理解 API 网关设计
4. 实现服务注册与发现

---

## 📋 课程大纲

- Part 1: 微服务架构概述
- Part 2: 服务拆分策略
- Part 3: API 网关
- Part 4: 服务注册与发现

---

## 🚀 快速开始

```bash
cd stage4-web-advanced/lessons/L44-microservices-basics

# 运行示例代码
python examples/01_service_discovery.py
python examples/02_circuit_breaker.py
python examples/03_api_gateway.py
```

## 📁 目录结构

```
L44-microservices-basics/
├── README.md                    # 本文档
├── lesson.md                    # 课程内容
├── examples/                    # 示例代码
│   ├── 01_service_discovery.py  # 服务发现
│   ├── 02_circuit_breaker.py  # 熔断器
│   └── 03_api_gateway.py    # API 网关
├── exercises/                   # 练习题
├── solutions/                   # 参考解答
└── tests/                       # 测试套件
```

## 🔧 环境准备

```bash
# Docker 和 Docker Compose
docker --version
docker-compose --version

# 本地开发工具
uv add fastapi uvicorn
```

---

## 📖 详细内容

### Part 1: 微服务架构概述

#### 单体 vs 微服务

| 维度 | 单体架构 | 微服务架构 |
|------|----------|------------|
| 部署 | 单一部署 | 独立部署 |
| 扩展 | 整体扩展 | 按需扩展 |
| 技术栈 | 统一 | 多样化 |
| 复杂度 | 开发简单 | 运维复杂 |
| 故障隔离 | 差 | 好 |

### Part 2: 服务拆分策略

#### 业务能力拆分

根据业务能力划分服务边界：

```
用户服务    订单服务    支付服务    物流服务
  │          │          │          │
  └──────────┴──────────┴──────────┘
                    │
              API Gateway
                    │
              负载均衡
```

#### 拆分原则

- **单一职责**: 每个服务只做一件事
- **高内聚低耦合**: 服务内部高度内聚，服务间松耦合
- **业务边界清晰**: 避免循环依赖
- **数据独立**: 每个服务有自己的数据库

### Part 3: API 网关

#### 网关职责

- 请求路由
- 认证授权
- 限流熔断
- 日志监控

```python
# 简单 API 网关示例
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.api_route("/{service}/{path:path}", methods=["GET", "POST"])
async def gateway(service: str, path: str, request: Request):
    routes = {
        "users": "http://user-service:8001",
        "orders": "http://order-service:8002",
        "products": "http://product-service:8003",
    }

    if service not in routes:
        return {"error": "Service not found"}, 404

    # 转发请求
    target = f"{routes[service]}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target,
            headers=dict(request.headers),
            content=await request.body(),
        )

    return response.json()
```

### Part 4: 服务注册与发现

#### 服务注册

```python
# 服务启动时注册
import httpx
import asyncio

async def register_service(service_name: str, port: int):
    service_id = f"{service_name}-{port}"

    await httpx.AsyncClient().put(
        "http://consul:8500/v1/agent/service/register",
        json={
            "ID": service_id,
            "Name": service_name,
            "Port": port,
            "Check": {
                "HTTP": f"http://localhost:{port}/health",
                "Interval": "10s",
            }
        }
    )
```

#### 服务发现

```python
async def discover_service(service_name: str) -> str:
    # 从 Consul 获取健康服务实例
    response = await httpx.AsyncClient().get(
        f"http://consul:8500/v1/health/service/{service_name}",
        params={"passing": "true"}
    )

    instances = response.json()
    if not instances:
        raise Exception(f"No healthy instance for {service_name}")

    # 简单负载均衡：随机选择
    import random
    instance = random.choice(instances)

    host = instance["Service"]["Address"]
    port = instance["Service"]["Port"]

    return f"http://{host}:{port}"
```

---

## 📝 练习题

### 练习 44.1：设计服务拆分方案

```markdown
目标：为电商系统设计微服务拆分方案
难度：⭐⭐⭐⭐
```

---

## ✅ 课后检查

- [ ] 理解单体 vs 微服务的区别
- [ ] 掌握服务拆分原则
- [ ] 实现简单 API 网关
- [ ] 理解服务注册与发现机制

---

## 🔗 下一步

完成本课后继续学习：

- [L45: 分布式系统实战](../L45-distributed-systems/README.md)

> 📖 **学习路径提示**：L45 将深入分布式系统，学习一致性、可用性和分区容错性。
