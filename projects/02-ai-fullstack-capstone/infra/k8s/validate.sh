#!/bin/bash
# Kubernetes YAML 验证脚本

set -euo pipefail

K8S_DIR="/Users/nexo/projects/python-learning/courses/13-python3.13-fullstack/projects/02-ai-fullstack-capstone/infra/k8s"

echo "🔍 验证 Kubernetes YAML 清单..."

# 检查 kubectl 是否安装
if ! command -v kubectl &> /dev/null; then
    echo "⚠️  kubectl 未安装，跳过 kubectl 验证"
    echo "   使用基础 YAML 语法检查..."

    # 使用 Python YAML 库验证语法
    if command -v python3 &> /dev/null; then
        python3 <<EOF
import yaml
import sys

files = [
    "${K8S_DIR}/app-deployment.yaml",
    "${K8S_DIR}/qdrant-statefulset.yaml"
]

for file_path in files:
    try:
        with open(file_path, 'r') as f:
            docs = list(yaml.safe_load_all(f))
            print(f"✅ {file_path}: {len(docs)} 个 Kubernetes 资源定义")
    except yaml.YAMLError as e:
        print(f"❌ {file_path}: YAML 语法错误")
        print(f"   {e}")
        sys.exit(1)

print("\n✅ 所有 YAML 文件语法验证通过")
EOF
    else
        echo "⚠️  Python 未安装，无法验证 YAML 语法"
    fi
else
    # 使用 kubectl 验证
    echo "使用 kubectl 验证配置..."

    for yaml_file in "${K8S_DIR}"/*.yaml; do
        if [[ -f "${yaml_file}" ]]; then
            echo "  验证: $(basename "${yaml_file}")"
            kubectl apply --dry-run=client -f "${yaml_file}" > /dev/null
            echo "  ✅ $(basename "${yaml_file}") 验证通过"
        fi
    done

    echo ""
    echo "✅ 所有 Kubernetes 清单验证通过"
fi
