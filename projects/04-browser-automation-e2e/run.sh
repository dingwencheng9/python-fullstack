#!/usr/bin/env bash
# 项目 4 - Browser Automation E2E 一键启动
#
# 用法：
#   bash run.sh                # 跑完整 E2E 测试
#   bash run.sh --headed       # 带浏览器界面跑
#   bash run.sh --install      # 安装 Playwright 浏览器
#   bash run.sh --help

set -euo pipefail

MODE="run"
HEADED=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --headed) HEADED="--headed"; shift ;;
        --install) MODE="install"; shift ;;
        --help|-h)
            sed -n '1,8p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *) echo "未知参数: $1" && exit 1 ;;
    esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

case "$MODE" in
    install)
        echo "📦 安装 Playwright 浏览器"
        uv run playwright install chromium
        ;;
    run)
        echo "🧪 项目 4 — Browser Automation E2E"
        echo "📂 项目根: $ROOT"
        echo ""
        PYTHONPATH=projects/04-browser-automation-e2e uv run pytest \
            projects/04-browser-automation-e2e/tests/ \
            --no-cov -v $HEADED
        ;;
esac
