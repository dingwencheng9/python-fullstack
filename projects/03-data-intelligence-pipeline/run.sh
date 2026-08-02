#!/usr/bin/env bash
# 项目 3 - Data Intelligence Pipeline 一键启动
#
# 用法：
#   bash run.sh                                 # 用项目 1 输出生成报告
#   bash run.sh --input X.json --output X.md   # 自定义输入输出
#   bash run.sh --test                          # 只跑测试
#   bash run.sh --help

set -euo pipefail

MODE="run"
INPUT="${INPUT:-projects/freelance-demo/sample_data/scraped.json}"
OUTPUT="${OUTPUT:-output/report.md}"

while [[ $# -gt 0 ]]; do
    case $1 in
        --input) INPUT="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        --test) MODE="test"; shift ;;
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
    run)
        echo "📊 项目 3 — 数据智能流水线"
        echo "📂 项目根: $ROOT"
        echo "📥 输入: $INPUT"
        echo "📤 输出: $OUTPUT"
        echo ""
        if [[ ! -f "$INPUT" ]]; then
            echo "❌ 输入文件不存在: $INPUT"
            echo "提示：先运行项目 1 爬虫生成 JSON，或使用 sample_data/scraped.json"
            exit 1
        fi
        mkdir -p "$(dirname "$OUTPUT")"
        PYTHONPATH=projects/03-data-intelligence-pipeline uv run python -m pipeline.report \
            "$INPUT" "$OUTPUT"
        echo "✅ 报告已生成: $OUTPUT"
        ;;
    test)
        echo "🧪 运行项目 3 测试"
        PYTHONPATH=projects/03-data-intelligence-pipeline uv run pytest \
            projects/03-data-intelligence-pipeline/tests/ \
            --no-cov -v
        ;;
esac
