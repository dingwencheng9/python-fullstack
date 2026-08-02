# K05: 平台工程

> **课程编号**: K05
> **所属阶段**: Stage K - DevOps 平台工程
> **预计时长**: 6-8 小时
> **难度**: ⭐⭐⭐⭐⭐
> **前置课程**: K02, K03, K04
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **平台工程理念**：理解平台工程和开发者体验
2. **Backstage 集成**：使用 Backstage 构建开发者门户
3. **IDP 架构**：设计内部开发者平台
4. **度量体系**：建立开发者生产力度量

---

## 📚 课程内容

### 第一部分：平台工程理念

#### 1.1 什么是平台工程

```python
"""
平台工程定义

平台工程是一门将基础设施和工具封装为产品的方法论，
目标是提供自助服务平台，让开发团队能够高效、安全地交付软件。

核心理念：
1. 开发者即客户 - 以开发者体验为核心
2. 金丝雀发布 - 小范围验证新功能
3. 安全左移 - 安全检查集成到开发流程
4. 基础设施即代码 - 所有配置版本化
5. 可观测性 - 全链路追踪和监控
"""

# 传统 DevOps vs 平台工程
COMPARISON = {
    "传统 DevOps": [
        "每个团队自己管理基础设施",
        "重复的配置和工具",
        "安全策略不一致",
        "部署流程各异",
    ],
    "平台工程": [
        "共享平台团队提供基础设施",
        "标准化的自助服务平台",
        "统一的安全策略",
        "一致的部署体验",
    ]
}
```

#### 1.2 开发者体验 (DevEx)

```python
# 开发者体验关键指标
DEX_METRICS = {
    "部署频率": "代码从提交到生产环境的频率",
    "变更前置时间": "代码提交到生产部署的时间",
    "变更失败率": "生产环境变更失败的百分比",
    "恢复时间 (MTTR)": "从故障中恢复的平均时间",
    "自助服务能力": "开发者无需平台团队协助的比例",
}

# 优秀 DevEx 的特征
GREAT_DEX = {
    "速度": "快速启动新项目和服务",
    "一致性": "所有服务使用相同的部署流程",
    "安全性": "安全检查自动化，不拖慢开发",
    "可观测性": "日志、指标、追踪开箱即用",
    "文档": "清晰的文档和示例",
}
```

---

### 第二部分：Backstage 开发者门户

#### 2.1 Backstage 架构

```yaml
# Backstage 安装
# backstage/helm/backstage/values.yaml
backstage:
  image:
    repository: roadieg/backstage
    tag: "latest"
  app:
    baseUrl: https://backstage.example.com
  ingress:
    enabled: true
    className: nginx
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
    hosts:
      - host: backstage.example.com
        paths:
          - path: /
            pathType: Prefix

  config:
    app:
      title: Developer Portal
      organization: Example Corp

    catalog:
      locations:
        - type: url
          target: https://github.com/org/backstage-catalog/blob/main/org.yaml
        - type: url
          target: https://github.com/org/backstage-catalog/blob/main/**/*.yaml

    techdocs:
      builder: external
      publisher:
        type: google-gcs
        googleGcs:
          projectId: my-project
          bucketName: my-bucket
```

#### 2.2 组件定义

```yaml
# catalog/components/app-template.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-new-service
  annotations:
    github.com/project-slug: org/my-new-service
    backstage.io/techdocs-ref: dir:.
    prometheus.io/rule: my-new-service
spec:
  type: service
  lifecycle: production
  owner: platform-team
  system: order-management
  dependsOn:
    - component:database
    - resource:order-queue
  providesApis:
    - my-new-service-api

---
# systems/order-management.yaml
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: order-management
  description: 订单管理系统
spec:
  owner: commerce-team
  domain: ecommerce
  components:
    - my-new-service
    - payment-service
    - inventory-service
```

```python
# Backstage 插件示例
# 简单的 GitHub 集成
from backstage_plugin import *

class GitHubPlugin:
    """GitHub 插件"""

    def __init__(self, token: str):
        self.token = token

    async def get_pr_status(self, repo: str) -> dict:
        """获取 PR 状态"""
        return {
            "open_prs": 5,
            "merged_prs": 10,
            "pending_reviews": 2,
        }

    async def get_deployments(self, repo: str) -> list:
        """获取部署历史"""
        return [
            {"env": "production", "status": "success", "version": "v1.2.0"},
            {"env": "staging", "status": "success", "version": "v1.3.0"},
        ]
```

---

### 第三部分：IDP 架构

#### 3.1 IDP 组件

```python
"""
内部开发者平台组件

┌─────────────────────────────────────────────────────────────┐
│                    Developer Portal (Backstage)               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  服务   │  │  文档   │  │  监控   │  │  部署   │       │
│  │  目录   │  │  中心   │  │  视图   │  │  控制   │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Platform APIs                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  IAM    │  │  CI/CD  │  │  监控   │  │  告警   │       │
│  │  API    │  │  API    │  │  API    │  │  API    │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Infrastructure                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │   K8s   │  │  Vault  │  │  ArgoCD │  │Prometh. │       │
│  │ Cluster │  │ Secrets │  │ GitOps  │  │ Monitor │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
└─────────────────────────────────────────────────────────────┘
"""

# IDP 核心服务
IDP_SERVICES = {
    "身份认证": "Keycloak / Dex",
    "密钥管理": "HashiCorp Vault / AWS Secrets Manager",
    "CI/CD": "GitHub Actions / GitLab CI / Tekton",
    "GitOps": "ArgoCD / Flux",
    "监控告警": "Prometheus / Grafana / AlertManager",
    "日志聚合": "Loki / Elasticsearch / CloudWatch",
    "追踪": "Jaeger / Tempo",
}
```

#### 3.2 自助服务模板

```yaml
# 自助服务 - 服务创建模板
apiVersion: backstage.io/v1alpha1
kind: ResourceTemplate
metadata:
  name: service-creation
  title: 创建新服务
  description: 使用模板创建新的微服务
spec:
  steps:
  - id: template
    name: 服务模板
    action: fabric:template
    input:
      templateEntity:
        apiVersion: backstage.io/v1alpha1
        kind: Component
        metadata:
          name: ${{ values.name }}
          description: ${{ values.description }}
        spec:
          type: service
          lifecycle: ${{ values.lifecycle }}
          owner: ${{ values.owner }}
  - id: publish
    name: 发布到 Git
    action: publish:github
    input:
      repoUrl: github.com?owner=${{ values.org }}&repo=${{ values.name }}
  - id: register
    name: 注册到目录
    action: catalog:register
    input:
      repoLocation: ${{ steps.publish.output.repoUrl }}

---
# 工作流定义
workflows:
  - name: 服务创建
    trigger: "service creation request"
    steps:
      - Create repository from template
      - Initialize CI/CD pipeline
      - Configure monitoring
      - Deploy to dev environment
      - Register in service catalog
    approval: required for production
```

---

### 第四部分：度量体系

#### 4.1 DORA 指标

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DoraMetrics:
    """DORA 四键指标"""
    deployment_frequency: str  # 部署频率
    lead_time_for_changes: str  # 变更前置时间
    change_failure_rate: float  # 变更失败率
    time_to_restore_service: str  # 服务恢复时间

@dataclass
class TeamMetrics:
    """团队指标"""
    team_name: str
    period: str
    dora: DoraMetrics
    developer_satisfaction: float  # 开发者满意度 (1-5)
    cognitive_load: str  # 认知负荷

# 优秀的 DORA 指标 (精英级别)
ELITE_DORA = {
    "deployment_frequency": "按需部署（每天多次）",
    "lead_time_for_changes": "< 1 小时",
    "change_failure_rate": "< 5%",
    "time_to_restore_service": "< 1 小时",
}
```

#### 4.2 平台使用率

```python
# 平台使用率指标
PLATFORM_USAGE = {
    "service_catalog_coverage": {
        "description": "服务目录覆盖率",
        "formula": "已注册服务 / 总服务数",
        "target": "> 90%",
    },
    "self_service_adoption": {
        "description": "自助服务使用率",
        "formula": "自助创建资源数 / 总资源创建数",
        "target": "> 80%",
    },
    "platform_team_efficiency": {
        "description": "平台团队效率",
        "formula": "开发者问题解决数 / 平台团队工时",
        "target": "持续提升",
    },
    "time_toproduction": {
        "description": "从代码提交到生产的时间",
        "formula": "平均部署时间",
        "target": "< 1 天",
    },
}

# 收集和展示指标
class MetricsCollector:
    """指标收集器"""

    def collect(self) -> dict:
        """收集所有指标"""
        return {
            "dora": self._collect_dora(),
            "usage": self._collect_usage(),
            "satisfaction": self._collect_satisfaction(),
        }

    def _collect_dora(self) -> dict:
        """收集 DORA 指标"""
        # 实际从 CI/CD 系统、日志系统收集
        return {
            "deployment_frequency": "per_day",
            "lead_time_for_changes": "2_hours",
            "change_failure_rate": 0.03,
            "time_to_restore_service": "45_minutes",
        }
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解平台工程核心理念
- [ ] 使用 Backstage 构建开发者门户
- [ ] 设计内部开发者平台架构
- [ ] 建立开发者度量体系

---

## 🔗 相关资源

- [Platform Engineering 社区](https://platformengineering.org/)
- [Backstage 文档](https://backstage.io/docs/)
- [DORA Metrics](https://dora.dev/research/2021/dora-report/)

---

## 🔗 下一步

完成 Stage K 后，进入：

- Stage M: 企业级 AI 应用
- Stage R: 前沿探索实验室

---

**最后更新**: 2026-07-18
