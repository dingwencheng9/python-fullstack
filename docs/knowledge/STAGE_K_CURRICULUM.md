# Stage K: DevOps 与平台工程 — 课程大纲

> **文档版本**: v1.1
> **课程编号**: K01-K05
> **阶段定位**: 垂直专精阶段
> **前置要求**: Stage 6 完成
> **建议学时**: 30 小时
> **最后更新**: 2026-07-24

---

## 📋 阶段概述

**定位**: AI Agent 部署与可观测性 → Kubernetes → Helm → GitOps → 平台工程

**学习路径**:
```
Stage 6 (L54-L65) → Stage K
```

**就业方向**: DevOps 工程师、平台工程师、SRE

---

## K01: AI Agent 部署与可观测性

**能力等级**: K1  
**前置依赖**: L65 (AI Agent 基础)

**知识点**:

| 层级 | 知识点 | 说明 |
|------|--------|------|
| L1 | [观测] Prometheus 架构 | Pull 模型、时序数据库 |
| L1 | [观测] Grafana 仪表盘 | 可视化配置 |
| L2 | [观测] OpenTelemetry | 统一追踪标准 |
| L2 | [观测] PromQL 查询 | 指标查询语言 |
| L3 | [观测] Alertmanager | 告警规则与通知 |
| L3 | [观测] Recording Rules | 预计算指标 |

---

## K02: Kubernetes 基础

**能力等级**: K1 → K2  
**前置依赖**: K01

**知识点**:

| 层级 | 知识点 | 说明 |
|------|--------|------|
| L1 | [K8s] Pod 与容器 | Pod 概念、容器规范 |
| L1 | [K8s] ReplicaSet | 副本管理 |
| L2 | [K8s] Deployment | 滚动更新、回滚 |
| L2 | [K8s] Service | ClusterIP/NodePort/LoadBalancer |
| L3 | [K8s] Ingress | HTTP 路由、域名 |
| L3 | [K8s] ConfigMap/Secret | 配置管理 |

---

## K03: Kubernetes 进阶

**能力等级**: K2 → K3  
**前置依赖**: K02

**知识点**:

| 层级 | 知识点 | 说明 |
|------|--------|------|
| L1 | [K8s] PersistentVolume | 持久化存储 |
| L1 | [K8s] StorageClass | 动态存储供给 |
| L2 | [K8s] HPA | 水平自动扩缩容 |
| L2 | [K8s] RBAC | 角色权限控制 |
| L3 | [K8s] NetworkPolicy | 网络隔离策略 |
| L3 | [K8s] 亲和性与反亲和 | 调度策略 |

---

## K04: Helm 与 GitOps

**能力等级**: K3  
**前置依赖**: K02

**知识点**:

| 层级 | 知识点 | 说明 |
|------|--------|------|
| L1 | [Helm] Chart 结构 | templates/values.yaml |
| L1 | [Helm] 模板语法 | Go 模板、函数 |
| L2 | [Helm] Release 管理 | install/upgrade/rollback |
| L2 | [GitOps] ArgoCD 基础 | 声明式部署 |
| L3 | [GitOps] Application | 应用定义与同步 |
| L3 | [GitOps] Sync Policy | 自动/手动同步策略 |

---

## K05: 平台工程

**能力等级**: K4 → K5  
**前置依赖**: K01-K04

**知识点**:

| 层级 | 知识点 | 说明 |
|------|--------|------|
| L1 | [平台] 内部开发者平台 | 自助服务平台理念 |
| L1 | [平台] Backstage 入门 | 开发者门户 |
| L2 | [平台] 服务目录 | 服务注册与发现 |
| L2 | [平台] 软件模板 | 项目脚手架 |
| L3 | [平台] 策略即代码 | Policy-as-Code |
| L3 | [平台] FinOps | 云成本优化 |

---

## 📊 阶段统计

| 维度 | 数值 |
|------|------|
| 课程总数 | 5 课 |
| 知识点总数 | ~32 个 |
| 建议学时 | 30 小时 |
| 能力等级 | K1 → K5 |

---

## 🔗 相关文档

- `docs/knowledge/COURSE_KNOWLEDGE_MAP.md` - 课程体系总览
- `stageK-devops/lessons/` - 课程实际目录
