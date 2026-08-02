# ArgoCD GitOps 自动化部署指南

本目录包含 ArgoCD GitOps 配置，实现从 Git 仓库到 Kubernetes 集群的自动化持续部署。

---

## 📋 架构概览

```
┌─────────────┐
│ Git Repo    │ ← 开发者推送变更
│ (main分支)  │
└──────┬──────┘
       │
       │ ArgoCD 自动监听
       ▼
┌─────────────┐
│   ArgoCD    │ ← 自动同步策略
│  Operator   │   • prune: true (垃圾回收)
└──────┬──────┘   • selfHeal: true (漂移修复)
       │
       │ 声明式应用
       ▼
┌─────────────┐
│ Kubernetes  │ ← 自动部署 infra/k8s/
│   Cluster   │   • app-deployment.yaml
└─────────────┘   • qdrant-statefulset.yaml
```

---

## 🚀 快速开始

### 前置条件

1. **Kubernetes 集群**（Minikube / GKE / EKS / AKS）
2. **ArgoCD 已安装**（参见下文安装步骤）
3. **Git 仓库访问权限**（HTTPS / SSH）

### 1. 安装 ArgoCD

```bash
# 创建 ArgoCD 命名空间
kubectl create namespace argocd

# 安装 ArgoCD（稳定版）
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 等待 Pod 就绪
kubectl wait --for=condition=available --timeout=600s \
  deployment/argocd-server -n argocd

# 获取初始管理员密码
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo

# 端口转发访问 UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

访问 https://localhost:8080，使用 `admin` + 上面的密码登录。

### 2. 配置 Git 仓库访问

**方式 1：公开仓库（无需认证）**

直接跳过，ArgoCD 可以拉取公开仓库。

**方式 2：私有仓库（HTTPS）**

```bash
kubectl create secret generic repo-credentials \
  --namespace argocd \
  --from-literal=url=https://github.com/YOUR_ORG/ai-fullstack-capstone.git \
  --from-literal=username=YOUR_GITHUB_USERNAME \
  --from-literal=password=YOUR_PERSONAL_ACCESS_TOKEN

kubectl label secret repo-credentials \
  -n argocd argocd.argoproj.io/secret-type=repository
```

**方式 3：私有仓库（SSH）**

```bash
# 生成 SSH 密钥（无密码）
ssh-keygen -t ed25519 -C "argocd@example.com" -f ~/.ssh/argocd_deploy_key -N ""

# 添加公钥到 GitHub Deploy Keys（Settings → Deploy Keys）
cat ~/.ssh/argocd_deploy_key.pub

# 创建 ArgoCD Secret
kubectl create secret generic argocd-repo-ssh \
  --namespace argocd \
  --from-file=sshPrivateKey=$HOME/.ssh/argocd_deploy_key \
  --from-literal=url=git@github.com:YOUR_ORG/ai-fullstack-capstone.git

kubectl label secret argocd-repo-ssh \
  -n argocd argocd.argoproj.io/secret-type=repository
```

### 3. 部署 Application

**修改仓库 URL**（在 `argocd-app.yaml` 中）：

```yaml
spec:
  source:
    repoURL: https://github.com/YOUR_ORG/ai-fullstack-capstone.git # 修改为实际仓库
    targetRevision: main # 或 master / production
```

**创建应用密钥**（与 K8s 部署指南一致）：

```bash
kubectl create namespace ai-fullstack

kubectl create secret generic app-secrets \
  --namespace ai-fullstack \
  --from-literal=secret-key="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

**部署 ArgoCD Application**：

```bash
kubectl apply -f infra/gitops/argocd-app.yaml

# 验证应用状态
kubectl get application -n argocd

# 查看详细同步状态
kubectl describe application ai-fullstack-capstone -n argocd
```

### 4. 验证自动同步

**触发同步测试**：

```bash
# 修改 infra/k8s/app-deployment.yaml（例如：replicas: 3 → 5）
git commit -am "test: scale to 5 replicas"
git push origin main

# ArgoCD 将在 3 分钟内自动检测并同步（默认轮询间隔）
# 实时监控同步进度
kubectl logs -f deployment/argocd-application-controller -n argocd
```

**手动触发同步**（测试用）：

```bash
# 使用 ArgoCD CLI
argocd app sync ai-fullstack-capstone

# 或使用 kubectl
kubectl patch application ai-fullstack-capstone \
  -n argocd \
  --type merge \
  -p '{"operation":{"sync":{}}}'
```

---

## 🔐 自动同步策略详解

### `prune: true` - 垃圾回收

**作用**：删除 Git 中不存在但 K8s 中存在的资源。

**场景**：

```bash
# 开发者从 infra/k8s/ 中删除 old-service.yaml
git rm infra/k8s/old-service.yaml
git commit -m "chore: remove deprecated service"
git push

# ArgoCD 自动执行
kubectl delete service old-service -n ai-fullstack
```

**风险**：误删 Git 文件会导致生产资源被删除。建议：

- 生产环境使用 `prune: false`（手动审核删除）
- 或配置 `PruneLast: true`（最后删除，减少服务中断）

### `selfHeal: true` - 漂移修复

**作用**：自动回滚手动 `kubectl` 修改，强制与 Git 保持一致。

**场景**：

```bash
# 运维人员手动扩容（绕过 Git）
kubectl scale deployment ai-fullstack-app --replicas=10 -n ai-fullstack

# ArgoCD 检测到漂移，5 分钟内自动回滚到 Git 声明的 replicas: 3
```

**适用场景**：

- ✅ **生产环境**：防止配置漂移，确保 Git 为唯一真实源
- ❌ **开发环境**：可能阻碍快速调试（频繁手动修改）

**禁用方式**（开发环境）：

```yaml
syncPolicy:
  automated:
    selfHeal: false # 允许手动修改
```

---

## 📊 监控与故障排查

### 查看同步状态

```bash
# 应用整体状态
kubectl get application -n argocd
# NAME                      SYNC STATUS   HEALTH STATUS
# ai-fullstack-capstone     Synced        Healthy

# 详细同步信息
kubectl describe application ai-fullstack-capstone -n argocd

# 实时日志
kubectl logs -f deployment/argocd-application-controller -n argocd
```

### 常见故障

#### 1. Sync 失败：`ImagePullBackOff`

**原因**：镜像不存在或无权限拉取。

**解决**：

```bash
# 验证镜像是否存在
docker pull registry.company.com/ai-fullstack:v1.0.0

# 创建 ImagePullSecret
kubectl create secret docker-registry regcred \
  --docker-server=registry.company.com \
  --docker-username=USER \
  --docker-password=PASSWORD \
  -n ai-fullstack

# 在 Deployment 中引用
spec:
  template:
    spec:
      imagePullSecrets:
        - name: regcred
```

#### 2. Sync 失败：`Namespace not found`

**原因**：`CreateNamespace=true` 未生效。

**解决**：

```bash
# 手动创建命名空间
kubectl create namespace ai-fullstack

# 或验证 ArgoCD RBAC
kubectl auth can-i create namespaces --as=system:serviceaccount:argocd:argocd-application-controller
```

#### 3. 漂移检测误报

**原因**：动态字段（如 HPA 修改的 `replicas`）触发 Out of Sync。

**解决**：在 `argocd-app.yaml` 中添加 `ignoreDifferences`：

```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas # 忽略副本数变化
```

---

## 🛡️ 生产环境最佳实践

### 1. 多环境隔离

使用不同 Git 分支或目录：

```yaml
# 开发环境
spec:
  source:
    repoURL: https://github.com/YOUR_ORG/ai-fullstack-capstone.git
    targetRevision: develop
    path: infra/k8s/dev

# 生产环境
spec:
  source:
    targetRevision: main
    path: infra/k8s/prod
```

### 2. 变更审批流程

生产环境禁用自动同步，启用手动审批：

```yaml
syncPolicy:
  automated: null # 禁用自动同步

  syncOptions:
    - CreateNamespace=true
```

部署流程：

```bash
# 1. 开发者推送到 Git
git push origin main

# 2. 运维人员审查变更
argocd app diff ai-fullstack-capstone

# 3. 手动批准同步
argocd app sync ai-fullstack-capstone
```

### 3. 回滚策略

```bash
# 查看历史版本
argocd app history ai-fullstack-capstone

# 回滚到指定版本
argocd app rollback ai-fullstack-capstone <REVISION_ID>

# 或通过 Git 回滚
git revert <COMMIT_HASH>
git push origin main
```

### 4. 通知集成

配置 Slack / Email 通知（在 ArgoCD ConfigMap 中）：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token
  trigger.on-sync-succeeded: |
    - send: [slack-success]
  template.slack-success: |
    message: "Application {{.app.metadata.name}} synced successfully!"
```

---

## 📚 参考资料

- [ArgoCD 官方文档](https://argo-cd.readthedocs.io/)
- [GitOps 最佳实践](https://www.weave.works/technologies/gitops/)
- [ArgoCD Sync Policies](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)
- [Multi-Environment Patterns](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)

---

## 🔗 相关文件

| 文件                             | 用途                      |
| -------------------------------- | ------------------------- |
| `argocd-app.yaml`                | ArgoCD Application 清单   |
| `../k8s/app-deployment.yaml`     | 应用 Deployment + Service |
| `../k8s/qdrant-statefulset.yaml` | Qdrant StatefulSet        |
| `../k8s/README.md`               | Kubernetes 手动部署指南   |
