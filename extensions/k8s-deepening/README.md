# Kubernetes 进阶扩展

**面向人群**：完成 Stage 5（L59 部署），希望进一步学习生产级 Kubernetes 部署实践的学员  
**主线环境**：kind  
**附录环境**：minikube（仅说明差异）

---

## 🔧 前置要求

- Docker（运行中）
- kind ≥ 0.20
- kubectl ≥ 1.29
- Helm ≥ 3.10（用于 Helm 章节）

---

## 📚 学习模块

| 模块              | 内容                                             | 预计时间 |
| ----------------- | ------------------------------------------------ | -------- |
| 1. 集群创建       | kind 集群配置、Ingress 端口映射                  | 5 分钟   |
| 2. 原生 Manifests | Namespace / Deployment / Service / Ingress / HPA | 10 分钟  |
| 3. Metrics Server | HPA 依赖的指标采集                               | 5 分钟   |
| 4. Helm Chart     | 从复制 YAML 到参数化部署                         | 15 分钟  |
| 5. GitOps         | Argo CD 自动同步（主线） + Flux 对比（附录）     | 20 分钟  |

---

## 🚀 快速开始

所有脚本从仓库根目录运行。

### 第 1 步：创建 kind 集群

```bash
bash extensions/k8s-deepening/scripts/kind-up.sh
```

创建 1 control-plane + 1 worker 集群，预映射 80/443 端口用于 Ingress。

### 第 2 步：安装 Ingress Controller

```bash
bash extensions/k8s-deepening/scripts/install-ingress.sh
```

安装 ingress-nginx，等待就绪。

### 第 3 步：安装 Metrics Server

```bash
bash extensions/k8s-deepening/scripts/install-metrics-server.sh
```

HPA 依赖 Metrics Server 采集 Pod CPU/Memory 指标。脚本自动 patch `--kubelet-insecure-tls` 以适配 kind 环境。

### 第 4 步：原生 Manifests 部署

```bash
bash extensions/k8s-deepening/scripts/deploy-manifests.sh
```

一次性应用：

- `namespace.yaml` - `python-course-demo` 命名空间
- `deployment.yaml` - nginx 演示应用，含 CPU/Memory requests
- `service.yaml` - ClusterIP 服务
- `ingress.yaml` - 主机 `python-course.local` 路由
- `hpa.yaml` - 自动扩缩容，min=1, max=5, CPU 50%

### 第 5 步：验证

```bash
bash extensions/k8s-deepening/scripts/verify.sh
```

检查所有资源状态，并显示本地访问方式。

**本地访问**：

```bash
# 方式 1：通过 Host header
curl -H 'Host: python-course.local' http://localhost:8080/

# 方式 2：添加 hosts 记录后直接访问
echo '127.0.0.1 python-course.local' | sudo tee -a /etc/hosts
curl http://python-course.local:8080/
```

### 第 6 步：Helm 部署

```bash
bash extensions/k8s-deepening/scripts/deploy-helm.sh
```

使用教学 Helm Chart 部署，演示参数化配置。

Chart 位于 `extensions/k8s-deepening/helm/python-course-demo/`：

- `values.yaml` - 可配置镜像、副本数、资源限制、Ingress、HPA
- `templates/` - 对应原生 manifests 的模板化版本

### 第 7 步：GitOps（Argo CD）

> ⚠️ **警告**：Argo CD 资源占用较大，仅在需要 GitOps 实践时安装。

```bash
# 安装 Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 等待 Argo CD 就绪
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

# 部署 Application
kubectl apply -f extensions/k8s-deepening/gitops/argocd-app.yaml
```

**⚠️ 重要提示**：

- `gitops/argocd-app.yaml` 中的 `repoURL` 指向公开仓库，如果你使用自己的 Fork，请修改为你的仓库地址
- `syncPolicy.automated.prune: true` - 自动删除 Git 中移除的资源
- `syncPolicy.automated.selfHeal: true` - 自动修正集群与 Git 的差异（会覆盖手动修改）
- ⚠️ 生产环境建议：
  - 先禁用 `prune`，直到同步行为验证无误
  - `selfHeal` 可能掩盖手动调试问题，请评估团队工作流
  - 关键资源可添加 `argocd.argoproj.io/sync-options: Prune=false` 注解保护

**访问 Argo CD UI**：

```bash
# 获取初始密码
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# 端口转发
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

访问 https://localhost:8081，用户名 `admin`。

---

## 📁 目录结构

```text
extensions/k8s-deepening/
├── README.md                    # 本文档
├── kind/
│   └── cluster.yaml             # kind 集群配置（1cp + 1worker, 端口映射）
├── manifests/                   # K8s 原生资源
│   ├── namespace.yaml           # python-course-demo 命名空间
│   ├── deployment.yaml          # nginx 演示应用
│   ├── service.yaml             # ClusterIP 服务
│   ├── ingress.yaml             # Ingress 路由
│   └── hpa.yaml                 # 水平自动扩缩容
├── helm/
│   └── python-course-demo/      # 教学 Helm Chart
│       ├── Chart.yaml           # Chart 元数据
│       ├── values.yaml          # 默认配置值
│       └── templates/           # 模板化资源
├── gitops/
│   ├── argocd-app.yaml          # Argo CD Application（主线）
│   ├── flux-gitrepository.yaml  # Flux GitRepository（附录）
│   └── flux-kustomization.yaml  # Flux Kustomization（附录）
└── scripts/                     # 一键运行脚本
    ├── kind-up.sh               # 创建集群
    ├── install-ingress.sh       # 安装 Ingress Nginx
    ├── install-metrics-server.sh # 安装 Metrics Server
    ├── deploy-manifests.sh      # 部署原生 Manifests
    ├── deploy-helm.sh           # 部署 Helm Chart
    └── verify.sh                # 验证所有资源
```

---

## 📋 附录 A: minikube 差异

本教程主线使用 kind，如果你更熟悉 minikube，以下是关键差异：

### minikube 集群创建

```bash
minikube start --cpus=2 --memory=4g
minikube addons enable ingress
minikube addons enable metrics-server
```

### Ingress 访问

```bash
# minikube tunnel 在另一终端运行
minikube tunnel

# 获取 minikube IP，添加到 hosts
echo "$(minikube ip) python-course.local" | sudo tee -a /etc/hosts
```

### HPA

minikube 的 metrics-server 默认已配置好 TLS，无需 patch。

---

## 📋 附录 B: Flux vs Argo CD 对比

| 特性     | Argo CD       | Flux                        |
| -------- | ------------- | --------------------------- |
| UI       | 丰富的 Web UI | 无原生 UI，需 Weave GitOps  |
| 架构     | 中心化控制器  | 分布式 Kustomize Controller |
| 同步触发 | Push + Pull   | Pull 为主（60 秒轮询）      |
| 多集群   | 原生支持      | 需额外配置                  |
| 回滚     | UI 一键回滚   | Git revert                  |
| 学习曲线 | 中等          | 较陡                        |

**Flux 快速示例**（不纳入主线命令）：

```bash
# 参考 gitops/flux-gitrepository.yaml 与 gitops/flux-kustomization.yaml
# 完整安装请参考 Flux 官方文档
```

---

## 🧹 清理

```bash
# 删除 kind 集群（推荐，彻底清理）
kind delete cluster --name python-course-k8s

# 或仅删除演示资源
kubectl delete namespace python-course-demo

# 如安装了 Argo CD
kubectl delete namespace argocd
```

---

## ❓ 常见问题

### Q: HPA 显示 `unknown/50%` 不工作？

A: 检查 metrics-server 是否已就绪，或等待 1-2 分钟让指标采集。

```bash
kubectl top pods -n python-course-demo
```

### Q: Ingress 访问 404？

A: 确认 Host header 正确，或检查 ingress-nginx controller 日志：

```bash
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

### Q: 可以把这个部署到云厂商 K8s 吗？

A: 可以！移除 kind 特定配置，修改 Ingress className 和 Service type 即可。本教程的 manifests 和 Helm Chart 设计为通用可移植。

---

## 📚 进阶阅读

- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [kind 文档](https://kind.sigs.k8s.io/)
- [Helm 文档](https://helm.sh/docs/)
- [Argo CD 文档](https://argo-cd.readthedocs.io/)
- [Ingress Nginx](https://kubernetes.github.io/ingress-nginx/)
