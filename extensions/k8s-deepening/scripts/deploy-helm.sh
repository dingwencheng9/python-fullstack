#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CHART_DIR="$ROOT_DIR/extensions/k8s-deepening/helm/python-course-demo"

command -v helm >/dev/null 2>&1 || { echo "❌ helm 未安装: https://helm.sh/docs/intro/install/"; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl 未安装"; exit 1; }

echo "🚀 使用 Helm 部署 python-course-demo"
helm upgrade --install python-course-demo "$CHART_DIR" \
  --namespace python-course-demo \
  --create-namespace

kubectl -n python-course-demo rollout status deployment/python-course-demo --timeout=120s
echo "✅ Helm 部署完成"
