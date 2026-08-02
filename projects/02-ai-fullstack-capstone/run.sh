#!/usr/bin/env bash
# 项目 2 - AI Fullstack Capstone 一键启动
#
# 用法：
#   bash run.sh                # 默认：本地启动 FastAPI + Mock LLM
#   bash run.sh --docker       # 用 Docker Compose 启动 (含 Qdrant)
#   bash run.sh --test         # 只跑测试
#   bash run.sh --help

set -euo pipefail

MODE="local"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

while [[ $# -gt 0 ]]; do
    case $1 in
        --docker) MODE="docker"; shift ;;
        --test) MODE="test"; shift ;;
        --host) HOST="$2"; shift 2 ;;
        --port) PORT="$2"; shift 2 ;;
        --help|-h)
            sed -n '1,10p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *) echo "未知参数: $1" && exit 1 ;;
    esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

case "$MODE" in
    local)
        echo "🚀 本地启动项目 2 — FastAPI + Mock LLM"
        echo "📂 项目根: $ROOT"
        echo ""
        echo "前置：uv sync --extra web --extra ai"
        echo ""
        PYTHONPATH=projects/02-ai-fullstack-capstone uv run uvicorn \
            app.main:app \
            --host "$HOST" \
            --port "$PORT" \
            --reload
        ;;
    docker)
        echo "🐳 Docker 启动项目 2"
        cd projects/02-ai-fullstack-capstone
        docker compose up --build
        ;;
    test)
        echo "🧪 运行项目 2 测试"
        PYTHONPATH=projects/02-ai-fullstack-capstone uv run pytest \
            projects/02-ai-fullstack-capstone/tests/ \
            --no-cov -v
        ;;
esac
