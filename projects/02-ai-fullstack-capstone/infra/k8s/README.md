# Kubernetes 部署指南

## 📋 前置要求

- Kubernetes 集群 v1.25+
- kubectl CLI 已配置并连接到目标集群
- 集群支持 PersistentVolume 动态分配
- 已构建并推送 Docker 镜像到容器注册表

---

## 🚀 快速部署

### 1. 准备镜像

```bash
# 构建并打标签
docker build -t your-registry.com/ai-fullstack-capstone:latest .

# 推送到容器注册表
docker push your-registry.com/ai-fullstack-capstone:latest

# 更新 infra/k8s/app-deployment.yaml 中的镜像地址
# 将 image: ai-fullstack-capstone:latest 修改为实际镜像地址
```

### 2. 创建命名空间（可选）

```bash
kubectl create namespace ai-fullstack
kubectl config set-context --current --namespace=ai-fullstack
```

### 3. 配置密钥

```bash
# 生成强随机密钥
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# 创建 Kubernetes Secret
kubectl create secret generic app-secrets \
  --from-literal=secret-key="${SECRET_KEY}" \
  --namespace=default
```

### 4. 部署 Qdrant 向量数据库

```bash
# 部署 StatefulSet 和 Service
kubectl apply -f infra/k8s/qdrant-statefulset.yaml

# 等待 Qdrant 就绪
kubectl wait --for=condition=ready pod -l app=qdrant --timeout=300s

# 验证状态
kubectl get statefulset qdrant
kubectl get service qdrant-service
```

### 5. 部署应用

```bash
# 部署 Deployment、Service 和 PVC
kubectl apply -f infra/k8s/app-deployment.yaml

# 等待所有副本就绪
kubectl wait --for=condition=available deployment/ai-fullstack-app --timeout=300s

# 验证状态
kubectl get deployment ai-fullstack-app
kubectl get pods -l app=ai-fullstack
kubectl get service ai-fullstack-service
```

---

## 🔍 验证部署

### 检查 Pod 状态

```bash
# 查看所有 Pod
kubectl get pods

# 查看详细信息
kubectl describe pod <pod-name>

# 查看日志
kubectl logs -f deployment/ai-fullstack-app
kubectl logs -f statefulset/qdrant
```

### 健康检查

```bash
# 端口转发到本地
kubectl port-forward service/ai-fullstack-service 8080:80

# 测试健康端点
curl http://localhost:8080/health

# 测试 Qdrant
kubectl port-forward service/qdrant-service 6333:6333
curl http://localhost:6333/healthz
```

---

## 📊 监控和调试

### 查看资源使用

```bash
# Pod 资源使用
kubectl top pods

# 节点资源使用
kubectl top nodes
```

### 事件日志

```bash
# 查看最近事件
kubectl get events --sort-by='.lastTimestamp'

# 持续监控事件
kubectl get events --watch
```

### 进入容器调试

```bash
# 进入应用容器
kubectl exec -it deployment/ai-fullstack-app -- /bin/bash

# 查看环境变量
kubectl exec deployment/ai-fullstack-app -- env
```

---

## 🔄 滚动更新

### 更新镜像

```bash
# 方法 1: 直接修改 YAML 并重新应用
kubectl apply -f infra/k8s/app-deployment.yaml

# 方法 2: 使用 kubectl set image
kubectl set image deployment/ai-fullstack-app \
  fastapi-app=your-registry.com/ai-fullstack-capstone:v2.0.0

# 监控滚动更新进度
kubectl rollout status deployment/ai-fullstack-app
```

### 回滚部署

```bash
# 查看历史版本
kubectl rollout history deployment/ai-fullstack-app

# 回滚到上一个版本
kubectl rollout undo deployment/ai-fullstack-app

# 回滚到指定版本
kubectl rollout undo deployment/ai-fullstack-app --to-revision=2
```

---

## 📈 扩缩容

### 水平扩展

```bash
# 手动扩展副本数
kubectl scale deployment/ai-fullstack-app --replicas=5

# 自动扩展（需配置 HPA）
kubectl autoscale deployment ai-fullstack-app \
  --min=3 --max=10 --cpu-percent=70
```

### 垂直扩展

修改 `infra/k8s/app-deployment.yaml` 中的资源限制：

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

然后重新应用：

```bash
kubectl apply -f infra/k8s/app-deployment.yaml
```

---

## 🗑️ 清理资源

```bash
# 删除应用部署
kubectl delete -f infra/k8s/app-deployment.yaml

# 删除 Qdrant
kubectl delete -f infra/k8s/qdrant-statefulset.yaml

# 删除 PVC（会删除数据！）
kubectl delete pvc duckdb-pvc
kubectl delete pvc qdrant-storage-qdrant-0

# 删除密钥
kubectl delete secret app-secrets
```

---

## ⚠️ 生产环境注意事项

### 1. 镜像安全

- 使用私有容器注册表
- 配置 imagePullSecrets
- 定期扫描镜像漏洞

### 2. 密钥管理

- 使用外部密钥管理系统（Vault、AWS Secrets Manager、Azure Key Vault）
- 不要在 YAML 中硬编码敏感信息
- 定期轮换密钥

### 3. 资源限制

- 根据实际负载调整 CPU 和内存限制
- 避免 OOMKilled（内存溢出被杀死）
- 使用 ResourceQuota 限制命名空间资源

### 4. 持久化存储

- 选择合适的 StorageClass（SSD、网络存储）
- 配置数据备份策略
- 测试灾难恢复流程

### 5. 网络策略

- 配置 NetworkPolicy 限制 Pod 间通信
- 使用 Ingress 配置 TLS 终结
- 启用 Service Mesh（如 Istio）增强安全性

### 6. 日志和监控

- 集成 Prometheus + Grafana 监控
- 配置 ELK/Loki 日志聚合
- 设置告警规则

---

## 🔗 相关资源

- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [Qdrant 部署指南](https://qdrant.tech/documentation/guides/distributed_deployment/)
- [FastAPI 部署最佳实践](https://fastapi.tiangolo.com/deployment/)
