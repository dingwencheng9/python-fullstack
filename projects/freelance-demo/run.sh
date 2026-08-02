#!/usr/bin/env bash
# Freelance Demo 一键启动脚本
# 把项目 1（爬虫）+ 项目 3（数据分析）+ 项目 2（AI问答）串起来演示
#
# 用法：
#   bash run.sh                                    # 完整流程
#   bash run.sh --url https://example.com         # 指定起始 URL
#   bash run.sh --skip-crawl                      # 跳过爬取，复用已有数据
#   bash run.sh --skip-ai                         # 跳过 AI 部分
#   bash run.sh --help                            # 查看所有选项

set -euo pipefail
IFS=$'\n\t'

# ---------- 默认参数 ----------
URL="${URL:-https://example.com}"
MAX_PAGES="${MAX_PAGES:-5}"
OUTPUT_DIR="${OUTPUT_DIR:-./output}"
SKIP_CRAWL=0
SKIP_REPORT=0
SKIP_AI=0

# ---------- 解析命令行 ----------
while [[ $# -gt 0 ]]; do
    case $1 in
        --url) URL="$2"; shift 2 ;;
        --max-pages) MAX_PAGES="$2"; shift 2 ;;
        --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
        --skip-crawl) SKIP_CRAWL=1; shift ;;
        --skip-report) SKIP_REPORT=1; shift ;;
        --skip-ai) SKIP_AI=1; shift ;;
        --help|-h)
            sed -n '1,15p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *) echo "未知参数: $1" && exit 1 ;;
    esac
done

# ---------- 工具检查 ----------
echo "🔍 检查环境 ..."
command -v uv >/dev/null 2>&1 || { echo "❌ 需要 uv 工具：https://docs.astral.sh/uv/"; exit 1; }
echo "✅ uv 已安装"

# 动态解析项目根目录（相对于脚本所在目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT" || { echo "❌ 无法切换到项目根目录: $ROOT"; exit 1; }
echo "📂 项目根：$ROOT"

# 验证关键子项目目录存在性
PROJECT_01="$ROOT/projects/01-web-scraper"
PROJECT_02="$ROOT/projects/02-ai-fullstack-capstone"
PROJECT_03="$ROOT/projects/03-data-intelligence-pipeline"

if [[ ! -d "$PROJECT_01" ]]; then
    echo "❌ 子项目不存在: $PROJECT_01"
    echo "   请确保在正确的仓库目录下运行此脚本"
    exit 1
fi

if [[ ! -d "$PROJECT_03" ]]; then
    echo "❌ 子项目不存在: $PROJECT_03"
    exit 1
fi

if [[ ! -d "$PROJECT_02" ]]; then
    echo "❌ 子项目不存在: $PROJECT_02"
    exit 1
fi

echo "✅ 子项目目录验证通过"

mkdir -p "$OUTPUT_DIR" || { echo "❌ 无法创建输出目录: $OUTPUT_DIR"; exit 1; }

# ---------- 1. 爬虫阶段 ----------
SCRAPED_JSON="$OUTPUT_DIR/scraped.json"
if [[ $SKIP_CRAWL -eq 0 ]]; then
    echo ""
    echo "🕷️  [1/3] 爬虫阶段 — 采集 $URL（最多 $MAX_PAGES 页）"

    if ! PYTHONPATH="$PROJECT_01" uv run python "$PROJECT_01/main.py" \
        --url "$URL" \
        --max-pages "$MAX_PAGES" \
        --output "$SCRAPED_JSON"; then
        echo "❌ 爬虫阶段失败（退出码: $?）"
        echo "   检查网络连接或目标 URL 是否可访问"
        exit 1
    fi

    if [[ ! -f "$SCRAPED_JSON" ]]; then
        echo "❌ 爬虫未生成预期输出文件: $SCRAPED_JSON"
        exit 1
    fi

    echo "✅ 已生成 $SCRAPED_JSON"
else
    echo "⏭️  跳过爬虫阶段（使用已有 $SCRAPED_JSON）"
    [[ -f "$SCRAPED_JSON" ]] || { echo "❌ 未找到 $SCRAPED_JSON，请去掉 --skip-crawl"; exit 1; }
fi

# ---------- 2. 数据分析阶段 ----------
REPORT_MD="$OUTPUT_DIR/report.md"
if [[ $SKIP_REPORT -eq 0 ]]; then
    echo ""
    echo "📊 [2/3] 数据分析阶段 — 清洗 + 特征 + 生成报告"

    if ! PYTHONPATH="$PROJECT_03" uv run python \
        "$SCRIPT_DIR/run_pipeline.py" \
        --input "$SCRAPED_JSON" \
        --output "$REPORT_MD"; then
        echo "❌ 数据分析阶段失败（退出码: $?）"
        echo "   检查 $SCRAPED_JSON 是否为有效的 JSON 格式"
        exit 1
    fi

    if [[ ! -f "$REPORT_MD" ]]; then
        echo "❌ 分析未生成预期报告文件: $REPORT_MD"
        exit 1
    fi

    echo "✅ 已生成报告 $REPORT_MD"
else
    echo "⏭️  跳过分析阶段"
fi

# ---------- 3. AI 问答阶段 ----------
if [[ $SKIP_AI -eq 0 ]]; then
    echo ""
    echo "🤖 [3/3] AI 问答阶段 — 启动 FastAPI + RAG"
    echo "   访问 http://localhost:8000 看 HTMX 界面"
    echo "   访问 http://localhost:8000/docs 看 API 文档"
    echo "   按 Ctrl+C 退出"
    echo ""

    if ! PYTHONPATH="$PROJECT_02" uv run python \
        "$SCRIPT_DIR/run_ai.py" \
        --documents "$SCRAPED_JSON"; then
        echo "❌ AI 服务启动失败（退出码: $?）"
        echo "   检查端口 8000 是否被占用，或依赖是否完整安装"
        exit 1
    fi
else
    echo "⏭️  跳过 AI 阶段"
    echo ""
    echo "🎉 全流程完成！查看结果："
    echo "   📄 爬取数据：$SCRAPED_JSON"
    echo "   📄 分析报告：$REPORT_MD"
fi
