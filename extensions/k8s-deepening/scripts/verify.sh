#!/usr/bin/env bash
set -euo pipefail

command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl 未安装"; exit 1; }

NS="python-course-demo"
HOST="python-course.local"

echo "🔍 检查 namespace"
kubectl get namespace "$NS"

echo "🔍 检查 pods"
kubectl -n "$NS" get pods

echo "🔍 检查 service"
kubectl -n "$NS" get service python-course-demo

echo "🔍 检查 ingress"
kubectl -n "$NS" get ingress python-course-demo

echo "🔍 检查 HPA"
kubectl -n "$NS" get hpa python-course-demo

echo "🌐 本地访问方式："
echo "  curl -H 'Host: $HOST' http://localhost:8080/"
echo "  或把 127.0.0.1 $HOST 加到 /etc/hosts 后访问 http://$HOST:8080/"

echo "✅ 验证完成"
