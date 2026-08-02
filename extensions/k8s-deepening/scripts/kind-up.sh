#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CLUSTER_NAME="python-course-k8s"
CONFIG="$ROOT_DIR/extensions/k8s-deepening/kind/cluster.yaml"

command -v kind >/dev/null 2>&1 || { echo "❌ kind 未安装: https://kind.sigs.k8s.io/docs/user/quick-start/"; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl 未安装"; exit 1; }

if kind get clusters | grep -qx "$CLUSTER_NAME"; then
  echo "✅ kind cluster 已存在: $CLUSTER_NAME"
else
  echo "🚀 创建 kind cluster: $CLUSTER_NAME"
  kind create cluster --config "$CONFIG"
fi

kubectl cluster-info --context "kind-$CLUSTER_NAME"
echo "✅ kind cluster 就绪"
