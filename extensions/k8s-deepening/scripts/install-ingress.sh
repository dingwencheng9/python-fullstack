#!/usr/bin/env bash
set -euo pipefail

command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl 未安装"; exit 1; }

echo "🚀 安装 ingress-nginx for kind"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

echo "⏳ 等待 ingress-nginx controller 就绪"
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=180s

echo "✅ ingress-nginx 就绪"
