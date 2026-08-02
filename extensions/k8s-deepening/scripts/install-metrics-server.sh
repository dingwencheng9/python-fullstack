#!/usr/bin/env bash
set -euo pipefail

command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl 未安装"; exit 1; }

echo "🚀 安装 metrics-server"
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

echo "🔧 patch metrics-server 以兼容 kind 自签证书"
kubectl -n kube-system patch deployment metrics-server --type=json -p='[
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}
]'

echo "⏳ 等待 metrics-server 就绪"
kubectl -n kube-system rollout status deployment/metrics-server --timeout=180s

echo "✅ metrics-server 就绪"
