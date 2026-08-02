# K03: Kubernetes 进阶

> **课程编号**: K03
> **所属阶段**: Stage K - DevOps 平台工程
> **预计时长**: 6-8 小时
> **难度**: ⭐⭐⭐⭐⭐
> **前置课程**: K02
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **高级调度**：掌握污点、容忍度、亲和性调度
2. **网络深入**：理解 CNI、网络策略、Service Mesh
3. **存储管理**：使用 PV、PVC、StorageClass
4. **安全加固**：配置 RBAC、SecurityContext、NetworkPolicy

---

## 📚 课程内容

### 第一部分：高级调度

#### 1.1 污点与容忍度

```yaml
# Node 设置污点
kubectl taint nodes node1 key=value:NoSchedule
kubectl taint nodes node1 dedicated=ml-workloads:NoExecute

# Pod 设置容忍度
apiVersion: v1
kind: Pod
metadata:
  name: ml-pod
spec:
  containers:
  - name: ml
    image: pytorch/pytorch:latest
  tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "ml-workloads"
    effect: "NoExecute"
    tolerationSeconds: 3600
```

```python
# Python 调度策略示例
class SchedulingStrategy:
    """调度策略"""

    @staticmethod
    def should_schedule(pod: dict, node: dict) -> bool:
        """判断是否应该调度"""
        # 检查污点容忍度
        pod_tolerations = pod.get("spec", {}).get("tolerations", [])
        node_taints = node.get("spec", {}).get("taints", [])

        # 如果节点有污点但 Pod 没有容忍度，不调度
        if node_taints and not pod_tolerations:
            return False

        # 检查所有污点是否被容忍
        for taint in node_taints:
            if not SchedulingStrategy._is_tolerated(taint, pod_tolerations):
                return False

        return True

    @staticmethod
    def _is_tolerated(taint: dict, tolerations: list) -> bool:
        """检查污点是否被容忍"""
        for toleration in tolerations:
            if toleration.get("key") == taint.get("key"):
                if toleration.get("operator", "Equal") == "Exists":
                    return True
                if toleration.get("value") == taint.get("value"):
                    if toleration.get("effect") in [taint.get("effect"), ""]:
                        return True
        return False
```

#### 1.2 亲和性与反亲和性

```yaml
# Pod 亲和性 - 将 Web 服务调度到缓存附近
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - redis-cache
        topologyKey: topology.kubernetes.io/zone
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - web
          topologyKey: kubernetes.io/hostname

# 节点亲和性 - GPU 工作负载调度到 GPU 节点
apiVersion: v1
kind: Pod
metadata:
  name: ml-pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu
            operator: Exists
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 10
        preference:
          matchExpressions:
          - key: node-type
            operator: In
            values:
            - ml-compute
```

---

### 第二部分：网络深入

#### 2.1 网络策略

```yaml
# 默认拒绝所有入站流量
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
# 允许前端访问后端
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
spec:
  podSelector:
    matchLabels:
      app: backend
      tier: api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080

---
# 限制出站流量
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-egress-policy
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 53  # DNS
```

#### 2.2 Service Mesh (Istio)

```yaml
# Istio VirtualService
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
  - backend
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: backend
        subset: v2
      weight: 100
  - route:
    - destination:
        host: backend
        subset: v1
      weight: 90
    - destination:
        host: backend
        subset: v2
      weight: 10

---
# 流量镜像
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: backend-mirror
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
        subset: v1
    mirror:
      host: backend
      subset: v2
    mirrorPercentage:
      value: 10
```

---

### 第三部分：存储管理

#### 3.1 PersistentVolume 和 PVC

```yaml
# Static PV
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-fast-disk
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: fast
  hostPath:
    path: /data/pv-fast-disk

---
# PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast

---
# Pod 使用 PVC
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: python:3.13-slim
    volumeMounts:
    - name: data
      mountPath: /app/data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: app-storage
```

#### 3.2 StorageClass

```yaml
# StorageClass - AWS EBS
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: aws-gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer

---
# StorageClass - NFS
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-storage
provisioner: nfs-subdir-external-provisioner
parameters:
  archiveOnDelete: "false"
  pathPattern: "${.PVC.namespace}/${.PVC.name}"
```

---

### 第四部分：安全加固

#### 4.1 RBAC

```yaml
# ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production

---
# Role - 限制权限
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-reader
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]

---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-reader-binding
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: production
roleRef:
  kind: Role
  name: app-reader
  apiGroup: rbac.authorization.k8s.io
```

#### 4.2 SecurityContext

```yaml
# Pod SecurityContext
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: python:3.13-slim
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 配置污点、容忍度、亲和性调度
- [ ] 使用 NetworkPolicy 保护网络
- [ ] 配置 PV、PVC、StorageClass
- [ ] 实施 RBAC 和 SecurityContext

---

## 🔗 下一步

- K04: Helm 与 GitOps
- K05: 平台工程

---

**最后更新**: 2026-07-18
