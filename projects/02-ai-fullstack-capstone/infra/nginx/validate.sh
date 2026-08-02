#!/bin/bash
# Nginx 配置验证脚本

set -euo pipefail

NGINX_CONF="/Users/nexo/projects/python-learning/courses/13-python3.13-fullstack/projects/02-ai-fullstack-capstone/infra/nginx/nginx.conf"

echo "🔍 验证 Nginx 配置语法..."

# 使用 Docker 临时容器验证 Nginx 配置
docker run --rm \
  -v "${NGINX_CONF}:/etc/nginx/nginx.conf:ro" \
  nginx:alpine \
  nginx -t

echo "✅ Nginx 配置语法验证通过"
