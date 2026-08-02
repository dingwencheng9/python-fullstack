# K02: Kubernetes 基础

> **课程编号**: K02
> **所属阶段**: Stage K - DevOps 平台工程
> **预计时长**: 6-8 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: L64
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **理解 K8s 架构**：掌握 Kubernetes 集群架构与核心组件
2. **掌握资源对象**：熟练使用 Pod、Deployment、Service、ConfigMap 等
3. **部署应用**：将 Python 应用部署到 Kubernetes 集群
4. **故障排查**：诊断和解决常见 K8s 问题

---

## 📚 课程内容

### 第一部分：Kubernetes 架构

#### 1.1 集群架构

```python
"""
Kubernetes 架构概述

┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │    Master    │    │    Worker    │    │    Worker    │  │
│  │   (Control   │    │    Node 1    │    │    Node 2    │  │
│  │    Plane)    │    │              │    │              │  │
│  │              │    │  ┌────────┐  │    │  ┌────────┐  │  │
│  │ ┌──────────┐ │    │  │  Pod   │  │    │  │  Pod   │  │  │
│  │ │ kube-    │ │    │  └────────┘  │    │  └────────┘  │  │
│  │ │ apiserver│ │    │  ┌────────┐  │    │  ┌────────┐  │  │
│  │ └──────────┘ │    │  │  Pod   │  │    │  │  Pod   │  │  │
│  │ ┌──────────┐ │    │  └────────┘  │    │  └────────┘  │  │
│  │ │ kube-    │ │    │              │    │              │  │
│  │ │ scheduler│ │    │  kubelet    │    │  kubelet     │  │
│  │ └──────────┘ │    │  containerd │    │  containerd  │  │
│  │ ┌──────────┐ │    └──────────────┘    └──────────────┘  │
│  │ │ etcd     │ │                                           │
│  │ └──────────┘ │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
"""

# Kubernetes 核心组件
K8S_COMPONENTS = {
    "ControlPlane": {
        "kube-apiserver": "API 服务器，集群控制入口",
        "kube-scheduler": "调度器，分配 Pod 到节点",
        "kube-controller-manager": "控制器管理器，运行控制器",
        "etcd": "高可用键值存储，保存集群状态",
    },
    "Node": {
        "kubelet": "节点代理，管理容器生命周期",
        "kube-proxy": "网络代理，处理服务发现和负载均衡",
        "container-runtime": "容器运行时 (containerd/cri-o)",
    }
}
```

#### 1.2 核心概念

```python
# Kubernetes 核心资源对象
K8S_RESOURCES = {
    "Pod": {
        "description": "最小部署单元，包含一个或多个容器",
        "example": "一个 Web 服务器 + 一个日志收集器",
        "特点": ["共享网络命名空间", "共享存储卷", "紧密耦合"]
    },
    "Deployment": {
        "description": "声明式更新，管理 Pod 副本集",
        "example": "确保始终运行 3 个副本",
        "特点": ["滚动更新", "回滚", "扩缩容"]
    },
    "Service": {
        "description": "稳定的网络端点，负载均衡到 Pod",
        "example": "ClusterIP, NodePort, LoadBalancer",
        "特点": ["服务发现", "健康检查", "负载均衡"]
    },
    "ConfigMap": {
        "description": "存储配置数据",
        "example": "应用配置文件、环境变量",
        "特点": ["解耦配置", "热更新"]
    },
    "Secret": {
        "description": "存储敏感信息",
        "example": "密码、API 密钥、证书",
        "特点": ["Base64 编码", "加密存储"]
    }
}
```

---

### 第二部分：资源对象详解

#### 2.1 Pod 资源

```yaml
# pod.yaml - Pod 定义
apiVersion: v1
kind: Pod
metadata:
  name: python-app
  labels:
    app: python-app
    version: v1
spec:
  containers:
  - name: app
    image: python:3.13-slim
    command: ["python", "-m", "http.server", "8000"]
    ports:
    - containerPort: 8000
    env:
    - name: ENVIRONMENT
      value: "production"
    resources:
      requests:
        memory: "128Mi"
        cpu: "250m"
      limits:
        memory: "256Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 5
```

```python
# Python 应用健康检查端点
# health.py
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/ready":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Ready")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), HealthHandler)
    server.serve_forever()
```

#### 2.2 Deployment 资源

```yaml
# deployment.yaml - Deployment 定义
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-app
  labels:
    app: python-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: python-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: python-app
        version: v1
    spec:
      containers:
      - name: app
        image: myregistry/python-app:v1
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: database.host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database.password
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

```bash
# Deployment 操作命令
kubectl create -f deployment.yaml
kubectl get deployments
kubectl describe deployment python-app
kubectl rollout status deployment python-app
kubectl rollout history deployment python-app
kubectl rollout undo deployment python-app
kubectl scale deployment python-app --replicas=5
kubectl set image deployment/python-app app=myregistry/python-app:v2
```

#### 2.3 Service 资源

```yaml
# service.yaml - Service 定义
apiVersion: v1
kind: Service
metadata:
  name: python-app-svc
spec:
  type: ClusterIP  # 或 NodePort, LoadBalancer
  selector:
    app: python-app
  ports:
  - name: http
    port: 80
    targetPort: 8000
    protocol: TCP
  - name: metrics
    port: 9090
    targetPort: 9090

---
# NodePort Service 示例
apiVersion: v1
kind: Service
metadata:
  name: python-app-nodeport
spec:
  type: NodePort
  selector:
    app: python-app
  ports:
  - port: 80
    targetPort: 8000
    nodePort: 30080  # 可选，指定端口

---
# Ingress 示例
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: python-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: python-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: python-app-svc
            port:
              number: 80
```

#### 2.4 ConfigMap 和 Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database.host: "postgres.default.svc.cluster.local"
  database.port: "5432"
  database.name: "myapp"
  app.log-level: "info"

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  # echo -n "password" | base64
  database.password: cGFzc3dvcmQ=
  # echo -n "secret-key" | base64
  api.key: c2VjcmV0LWtleQ==
```

```python
# Python 应用读取环境变量
# app.py
import os
import json
from typing import Optional

class AppConfig:
    """应用配置"""

    def __init__(self):
        # 数据库配置
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_name = os.getenv("DB_NAME", "myapp")
        self.db_password = os.getenv("DB_PASSWORD", "")

        # 应用配置
        self.log_level = os.getenv("APP_LOG_LEVEL", "info")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

    @classmethod
    def from_env(cls) -> "AppConfig":
        """从环境变量创建配置"""
        return cls()

    def to_dict(self) -> dict:
        """转换为字典（隐藏敏感信息）"""
        return {
            "db_host": self.db_host,
            "db_port": self.db_port,
            "db_name": self.db_name,
            "log_level": self.log_level,
            "debug": self.debug
        }

if __name__ == "__main__":
    config = AppConfig.from_env()
    print(json.dumps(config.to_dict(), indent=2))
```

---

### 第三部分：Helm 包管理

#### 3.1 Helm 基础

```bash
# Helm 安装和使用
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo postgresql
helm install my-postgres bitnami/postgresql
helm list
helm values my-postgres > values.yaml
helm upgrade my-postgres bitnami/postgresql -f values.yaml
helm rollback my-postgres 1
helm uninstall my-postgres
```

#### 3.2 Chart 结构

```yaml
# chart.yaml - Chart 定义
apiVersion: v2
name: python-app
description: A Helm chart for Python application
type: application
version: 1.0.0
appVersion: "1.0.0"

---
# values.yaml - 默认配置
replicaCount: 3

image:
  repository: myregistry/python-app
  tag: "v1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: python-app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: python-app-tls
      hosts:
        - python-app.example.com
```

```bash
# 创建 Chart
helm create python-app-chart
cd python-app-chart

# 目录结构
# python-app-chart/
# ├── Chart.yaml
# ├── values.yaml
# ├── charts/
# ├── templates/
# │   ├── deployment.yaml
# │   ├── service.yaml
# │   ├── ingress.yaml
# │   └── _helpers.tpl
# └── .helmignore

# 验证和安装
helm lint .
helm template my-release .
helm install my-release .
helm install my-release --dry-run --debug .
```

---

### 第四部分：生产最佳实践

#### 4.1 资源限制

```yaml
# 生产环境资源配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-app
spec:
  template:
    spec:
      containers:
      - name: app
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        # 水平自动扩缩容
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: python-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: python-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### 4.2 高可用部署

```yaml
# 高可用部署策略
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-app
spec:
  replicas: 3
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - python-app
        topologyKey: kubernetes.io/hostname
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: python-app
```

#### 4.3 Pod 中断预算

```yaml
# PDB - 确保最小可用
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: python-app-pdb
spec:
  minAvailable: 2  # 或使用 maxUnavailable
  selector:
    matchLabels:
      app: python-app
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解 Kubernetes 集群架构
- [ ] 创建和管理 Pod、Deployment、Service
- [ ] 使用 ConfigMap 和 Secret 管理配置
- [ ] 使用 Helm 打包和部署应用
- [ ] 配置资源限制和 HPA

---

## 🔗 相关资源

- [Kubernetes 官方文档](https://kubernetes.io/zh/docs/)
- [Kubernetes 中文社区](https://kubernetes.io/zh/)
- [Helm 文档](https://helm.sh/zh/docs/)

---

## 🔗 下一步

- K03: Kubernetes 进阶
- K04: Helm 与 GitOps
- K05: 平台工程

---

**最后更新**: 2026-07-18
