#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
MANIFEST_DIR="$ROOT_DIR/extensions/k8s-deepening/manifests"

command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl 未安装"; exit 1; }

echo "🚀 部署原生 manifests"
kubectl apply -f "$MANIFEST_DIR/namespace.yaml"
kubectl apply -f "$MANIFEST_DIR/deployment.yaml"
kubectl apply -f "$MANIFEST_DIR/service.yaml"
kubectl apply -f "$MANIFEST_DIR/ingress.yaml"
kubectl apply -f "$MANIFEST_DIR/hpa.yaml"

echo "⏳ 等待 Deployment 就绪"
kubectl -n python-course-demo rollout status deployment/python-course-demo --timeout=120s

echo "✅ manifests 部署完成"
