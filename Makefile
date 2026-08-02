.PHONY: help install test test-projects test-cov test-cov-html test-cov-report \
        mkdocs mkdocs-serve lint lint-strict lint-fix \
        clean clean-all demo run-p1 run-p2 run-p3 run-p4 run-demo \
        ci-local typecheck verify-metadata

help:  ## 显示所有可用命令
	@echo "Python 3.13 全栈课程 - Make 命令速查"
	@echo ""
	@echo "用法: make <target>"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ─── 环境 ─────────────────────────────────────────
install:  ## 安装所有可选依赖（web + ai）
	uv sync --extra web --extra ai

# ─── 测试 ─────────────────────────────────────────
test:  ## 跑课程全量测试（不含项目）
	uv run pytest --no-cov -p no:cacheprovider -q

test-cov:  ## 跑测试并生成覆盖率报告（终端输出）
	uv run pytest --cov --cov-report=term-missing

test-cov-html:  ## 跑测试并生成 HTML 覆盖率报告
	uv run pytest --cov --cov-report=html --cov-report=term-missing
	@echo ""
	@echo "📊 HTML 覆盖率报告已生成: htmlcov/index.html"

test-cov-report:  ## 打开 HTML 覆盖率报告（需先运行 test-cov-html）
	@if [ -f htmlcov/index.html ]; then \
		open htmlcov/index.html || xdg-open htmlcov/index.html || echo "请手动打开 htmlcov/index.html"; \
	else \
		echo "❌ HTML 报告不存在，请先运行: make test-cov-html"; \
	fi

test-projects:  ## 跑 4 个综合项目独立测试
	@echo "=== 项目 1 ===" && PYTHONPATH=projects/01-web-scraper uv run pytest projects/01-web-scraper/tests/ --no-cov -q
	@echo "=== 项目 2 ===" && PYTHONPATH=projects/02-ai-fullstack-capstone uv run pytest projects/02-ai-fullstack-capstone/tests/ --no-cov -q
	@echo "=== 项目 3 ===" && PYTHONPATH=projects/03-data-intelligence-pipeline uv run pytest projects/03-data-intelligence-pipeline/tests/ --no-cov -q
	@echo "=== 项目 4 ===" && PYTHONPATH=projects/04-browser-automation-e2e uv run pytest projects/04-browser-automation-e2e/tests/ --no-cov -q

# ─── 构建与文档 ───────────────────────────────────
mkdocs:  ## 严格构建 mkdocs 站点
	uv run mkdocs build

mkdocs-serve:  ## 本地启动 mkdocs 预览
	uv run mkdocs serve

# ─── 代码质量 ─────────────────────────────────────
lint:  ## ruff 检查（不修复）
	-uv run ruff check .

lint-strict:  ## ruff 严格检查（有错就退出）
	uv run ruff check .

lint-fix:  ## ruff 安全自动修复
	uv run ruff check . --fix

typecheck:  ## mypy strict 类型检查
	uv run mypy .

verify-metadata:  ## 验证所有课程的元数据完整性和一致性
	python3 scripts/ci/verify_course_metadata.py

ci-local:  ## 本地复制 GitHub CI 完整门禁
	@echo "▶ 1/4 ruff..."
	@uv run ruff check .
	@echo "▶ 2/4 mypy strict..."
	@uv run mypy .
	@echo "▶ 3/4 mkdocs strict..."
	@NO_MKDOCS_2_WARNING=1 uv run --extra docs mkdocs build
	@echo "▶ 4/4 pytest..."
	@uv run pytest \
		stage0-python-basics stage1-python-intermediate stage2-engineering \
		stage3-web-basics stage4-web-advanced/lessons \
		stage5-data-engineering \
		--no-cov -p no:cacheprovider -q 2>&1 | tail -10
	@echo ""
	@echo "✅ 四件套全部通过 — 可以 PR/合并"

# ─── 项目运行 ─────────────────────────────────────
run-p1:  ## 运行项目 1（爬虫，需指定 URL=...）
	@URL=$${URL:-https://example.com}; \
	PYTHONPATH=projects/01-web-scraper uv run python projects/01-web-scraper/main.py \
	  --url "$$URL" --max-pages 5 --output projects/01-web-scraper/output.json

run-p2:  ## 运行项目 2（FastAPI + Mock LLM）
	bash projects/02-ai-fullstack-capstone/run.sh

run-p3:  ## 运行项目 3（数据流水线）
	bash projects/03-data-intelligence-pipeline/run.sh

run-p4:  ## 运行项目 4（E2E 测试）
	bash projects/04-browser-automation-e2e/run.sh

run-demo:  ## 运行 freelance-demo 离线流程
	bash projects/freelance-demo/run.sh --skip-ai

demo: run-demo  ## run-demo 别名

# ─── 清理 ─────────────────────────────────────────
clean:  ## 清理缓存目录
	@find . -type d -name "__pycache__" -not -path "./.venv/*" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -not -path "./.venv/*" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -not -path "./.venv/*" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .mypy_cache .coverage htmlcov 2>/dev/null || true
	@echo "✅ 缓存已清理"

clean-all: clean  ## 清理缓存 + 构建产物
	@rm -rf site
	@find . -type d -name "output" -not -path "./.venv/*" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ 全部产物已清理"

# ─── 验证 ─────────────────────────────────────────
verify: lint mkdocs test test-projects  ## 全套验证
	@echo ""
	@echo "✅ 所有验证全部通过"
