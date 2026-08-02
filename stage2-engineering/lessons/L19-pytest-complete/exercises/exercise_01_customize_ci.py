"""练习 4: 自定义 CI 工作流。

阅读仓库根目录 `.github/workflows/ci.yml`，回答触发事件、Python 版本、
质量门和 `uv sync --frozen` 的作用。
"""

from __future__ import annotations

ANSWERS = {
    "triggers": "push 到 main、pull_request 到 main",
    "python_versions": "当前主测试矩阵包含 Python 3.13；free-threading smoke 包含 3.13t 和 3.14t",
    "quality_gates": "ruff check、mypy --strict、mkdocs/markdown links、pytest",
    "uv_frozen": "根据锁文件安装依赖，不更新版本，保证 CI 环境可复现",
}


if __name__ == "__main__":
    for key, value in ANSWERS.items():
        print(f"{key}: {value}")
