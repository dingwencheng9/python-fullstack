# K04: Helm 与 GitOps

> **课程编号**: K04
> **所属阶段**: Stage K - DevOps 平台工程
> **预计时长**: 4-6 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: K02, K03
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **Helm 进阶**：掌握 Helm 模板、钩子、测试
2. **GitOps 理念**：理解 GitOps 核心原则
3. **ArgoCD 实践**：使用 ArgoCD 实现 GitOps
4. **CI/CD 集成**：构建完整的 GitOps 工作流

---

## 📚 课程内容

### 第一部分：Helm 进阶

#### 1.1 模板函数和管道

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "app.fullname" . }}
  labels:
    {{- include "app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        {{- range .Values.service.ports }}
        - name: {{ .name }}
          containerPort: {{ .port }}
          protocol: {{ .protocol }}
        {{- end }}
        livenessProbe:
          httpGet:
            path: {{ .Values.probe.path }}
            port: {{ .Values.service.port }}
        readinessProbe:
          httpGet:
            path: {{ .Values.probe.path }}
            port: {{ .Values.service.port }}
        env:
        {{- range $key, $value := .Values.env }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
```

```python
# _helpers.tpl - 辅助模板函数
# 完整的命名模板
{{- define "app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "app.labels" -}}
helm.sh/chart: {{ include "app.name" . }}
{{ include "app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

#### 1.2 Helm 钩子

```yaml
# hooks/job.yaml - Helm 钩子
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "app.fullname" . }}-pre-install
  labels:
    {{- include "app.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: db-migration
        image: "{{ .Values.migration.image }}"
        args:
        - migrate
        - up
        env:
        {{- range $key, $value := .Values.database.env }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}

---
# 钩子类型
HOOK_TYPES = {
    "pre-install": "模板渲染之后，资源创建之前",
    "post-install": "所有资源创建之后",
    "pre-upgrade": "模板渲染之后，资源更新之前",
    "post-upgrade": "所有资源更新之后",
    "pre-rollback": "模板渲染之后，回滚之前",
    "post-rollback": "所有资源回滚之后",
    "pre-delete": "删除资源之前",
    "post-delete": "所有资源删除之后",
}
```

---

### 第二部分：GitOps 理念

#### 2.1 GitOps 核心原则

```python
"""
GitOps 核心原则

1. 声明式配置
   - 所有基础设施和应用配置声明在 Git 中
   - 不手动修改集群状态

2. Git 作为唯一真相来源
   - 基础设施即代码 (IaC)
   - 版本控制和审计追踪

3. 自动同步
   - 当 Git 状态变化时，自动同步到集群
   - 持续部署流水线

4. 漂移检测
   - 检测集群状态与 Git 声明的差异
   - 自动或手动修复
"""

# GitOps vs 传统 CI/CD
GITOPS_BENEFITS = {
    "一致性": "所有环境使用相同的配置",
    "可审计": "所有变更都有 Git 历史记录",
    "可回滚": "一键回滚到之前的版本",
    "安全": "减少直接访问集群的需求",
    "开发体验": "开发者使用熟悉的 Git 工作流",
}
```

#### 2.2 GitOps 仓库结构

```text
# GitOps 仓库结构
gitops-repo/
├── apps/
│   ├── production/
│   │   ├── app1/
│   │   │   ├── kustomization.yaml
│   │   │   └── values.yaml
│   │   └── app2/
│   └── staging/
│       └── app1/
├── clusters/
│   ├── production/
│   │   ├── apps.yaml
│   │   └── infra.yaml
│   └── staging/
└── infrastructure/
    ├── cert-manager/
    ├── ingress-nginx/
    └── monitoring/
```

---

### 第三部分：ArgoCD 实践

#### 3.1 ArgoCD 安装和配置

```yaml
# ArgoCD Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app1-production
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: production
  source:
    repoURL: https://github.com/org/gitops-repo
    targetRevision: main
    path: apps/production/app1
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

---
# ApplicationSet - 多集群部署
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: app1-all-clusters
spec:
  generators:
  - clusters:
      selector:
        matchLabels:
          env: production
  template:
    metadata:
      name: app1-{{name}}
    spec:
      project: production
      source:
        repoURL: https://github.com/org/gitops-repo
        targetRevision: main
        path: apps/production/app1
        kustomize:
          images:
          - app1:{{image}}
      destination:
        server: {{server}}
        namespace: production
```

#### 3.2 ArgoCD 通知

```yaml
# ArgoCD Notification
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
data:
  service.slack: |
    apiUrl: $SLACK_API_URL
    username: ArgoCD
    channel: "#deployments"

  template.app-sync-status: |
    message: |
      {{if eq .app.status.sync.status "OutOfSync"}}
      ⚠️ *{{.app.metadata.name}}* is OutOfSync
      {{else if eq .app.status.sync.status "Synced"}}
      ✅ *{{.app.metadata.name}}* is Synced
      {{end}}
      Application: {{.app.metadata.name}}
      Revision: {{.app.status.sync.revision}}

  trigger.on-sync-status: |
    - when: app.status.sync.status == "OutOfSync"
      oncePer: app.status.sync.revision
      send:
      - app-sync-status

  subscription.slack: |
    - recipients:
      - selector: app.name contains "production"
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 编写 Helm 模板
- [ ] 使用 Helm 钩子管理生命周期
- [ ] 理解 GitOps 核心原则
- [ ] 使用 ArgoCD 实现 GitOps

---

## 🔗 相关资源

- [Helm 文档](https://helm.sh/zh/docs/)
- [ArgoCD 文档](https://argoproj.github.io/cd/)
- [Flux GitOps](https://fluxcd.io/)

---

## 🔗 下一步

- K05: 平台工程

---

**最后更新**: 2026-07-18
