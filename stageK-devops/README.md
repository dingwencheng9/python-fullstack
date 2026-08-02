# Stage K: DevOps 与平台工程

> **阶段编号**: Stage K
> **课程数量**: 5 课 (K01-K05)
> **预计学时**: ~30 小时
> **前置要求**: Stage 6 (AI Agent 开发)

---

## 📚 课程列表

| 编号 | 课程名称 | 主题 | 学时 | 难度 |
|------|----------|------|------|------|
| K01 | AI Agent 部署与可观测性 | Prometheus、OpenTelemetry、Grafana | 6h | ⭐⭐⭐⭐ |
| K02 | Kubernetes 基础 | Pod、Deployment、Service、ConfigMap | 8h | ⭐⭐⭐⭐ |
| K03 | Kubernetes 进阶 | 存储、网络、安全、RBAC | 6h | ⭐⭐⭐⭐ |
| K04 | Helm 与 GitOps | Chart 开发、ArgoCD、自动化部署 | 5h | ⭐⭐⭐⭐ |
| K05 | 平台工程 | 内部开发者平台、Backstage、IaC | 8h | ⭐⭐⭐⭐⭐ |

---

## 🎯 学习路径

```
K01 可观测性 → K02 Kubernetes → K03 Kubernetes进阶 → K04 Helm/GitOps
                                                                       ↓
                                                              K05 平台工程综合
```

---

## 📖 学习目标

完成 Stage K 后，你将掌握：

1. **可观测性** — Prometheus 指标、Grafana 仪表板、OpenTelemetry 追踪
2. **Kubernetes 进阶** — Deployment、Service、ConfigMap、Secret 管理
3. **Helm 包管理** — Chart 开发、Template 编写、版本发布
4. **GitOps 实践** — ArgoCD、自动化部署、配置同步
5. **平台工程** — 内部开发者平台、Backstage、基础设施即代码
6. **容器编排** — 多容器协同、网络配置、存储管理
7. **自动化运维** — 基础设施即代码、配置管理、密钥安全

---

## 🛠️ 环境要求

- **Python 版本**: 3.13.x
- **包管理**: uv
- **容器化**: Docker, Docker Compose
- **编排工具**: Kubernetes (Minikube/Docker Desktop), Helm
- **可选**: Istio, ArgoCD, Backstage

```bash
# 安装依赖
uv sync

# 运行测试（全阶段）
uv run pytest stageK-devops/lessons/ -v

# 代码检查
uv run ruff check stageK-devops/
uv run mypy stageK-devops/lessons/ --ignore-missing-imports
```

---

## 📁 课程结构

每个课程包含：

```
K{XX}-课程名/
├── README.md           # 课程概览与快速开始
├── lesson.md           # 详细教学内容
├── examples/           # 示例代码（可直接运行）
├── exercises/          # 练习题模板
├── solutions/          # 参考解答
└── tests/              # 单元测试
```

---

## 🔗 衔接课程

- **前置**: [Stage 6: AI Agent 开发](../stage6-ai-agent/)
- **后续**: [Stage M: 企业级商业应用](../stageM-enterprise/)

---

## 📊 统计数据

| 指标 | 数值 |
|------|------|
| 课程数量 | 5 |
| 示例代码 | ~30 个 |
| 练习题 | ~15 个 |
| 测试用例 | 200+ |
| 预计学时 | ~30 小时 |

---

## 🏆 完成标准

- [ ] 完成所有 5 个课程的学习
- [ ] 通过所有课程测试
- [ ] 完成所有练习题
- [ ] 能够构建完整可观测性体系
- [ ] 掌握 Kubernetes 进阶技能
- [ ] 理解 GitOps 实践

---

## ⚡ 快速参考

### Prometheus 指标采集

```python
from prometheus_client import Counter, Histogram

# 定义指标
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'Request duration')

# 使用指标
@request_duration.time()
def handle_request():
    request_count.inc()
    # 处理请求
```

### OpenTelemetry 追踪

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# 配置追踪
provider = TracerProvider()
trace.set_tracer_provider(provider)

# 创建追踪器
tracer = trace.get_tracer(__name__)

# 使用追踪
with tracer.start_as_current_span("process_request") as span:
    span.set_attribute("user.id", user_id)
    # 处理请求
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-api
  template:
    metadata:
      labels:
        app: agent-api
    spec:
      containers:
        - name: api
          image: agent-api:latest
          ports:
            - containerPort: 8000
```

### Helm Chart

```bash
# 创建 Chart
helm create my-chart

# 部署
helm install my-release my-chart/

# 升级
helm upgrade my-release my-chart/ -f values.yaml
```

---

> **版本**: v5.0
> **最后更新**: 2026-07-22
