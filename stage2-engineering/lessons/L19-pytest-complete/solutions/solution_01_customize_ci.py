"""练习 4 参考答案: 自定义 CI 工作流。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# 1. 哪个触发事件会导致 CI 运行？
# 答案: push 到 main 分支，以及 pull_request 到 main 分支。

# 2. 矩阵测试包含了哪些 Python 版本？
# 答案: 当前主测试矩阵包含 Python 3.13；free-threading smoke 包含 3.13t 和 3.14t。

# 3. 质量门包含哪些主要步骤？
# 答案:
# - Ruff check（代码质量检查）
# - Mypy strict（类型检查）
# - MkDocs/Markdown links（文档构建与链接检查）
# - Pytest full suite（运行测试）

# 4. --frozen 参数的作用是什么？
# 答案: uv sync --frozen 确保使用 uv.lock 中锁定的精确版本，
# 不更新依赖，保证 CI 环境的可重现性。


def load_ci_config(repo_root: Path) -> dict[str, Any]:
    """加载 CI 配置，并兼容 PyYAML 对 GitHub Actions `on` 键的解析。"""
    ci_path = repo_root / ".github" / "workflows" / "ci.yml"
    if not ci_path.exists():
        raise FileNotFoundError(f"CI 配置不存在: {ci_path}")
    config = yaml.safe_load(ci_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise TypeError("CI 配置应解析为 dict")
    if True in config and "on" not in config:
        config["on"] = config.pop(True)
    return config


def get_main_python_versions(config: dict[str, Any]) -> list[str]:
    """读取主测试 job 的 Python 版本矩阵。"""
    matrix = config.get("jobs", {}).get("test", {}).get("strategy", {}).get("matrix", {})
    if not isinstance(matrix, dict):
        return []
    include = matrix.get("include")
    if isinstance(include, list):
        return [str(item["python-version"]) for item in include if isinstance(item, dict) and "python-version" in item]
    versions = matrix.get("python-version")
    if isinstance(versions, list):
        return [str(version) for version in versions]
    return []


def customize_ci_example(config: dict[str, Any]) -> dict[str, Any]:
    """示例：在主测试 job 中插入 uv 缓存步骤。"""
    steps = config["jobs"]["test"]["steps"]
    cache_step = {
        "name": "Cache uv",
        "uses": "actions/cache@v4",
        "with": {
            "path": "~/.cache/uv",
            "key": "uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}",
            "restore-keys": "uv-${{ runner.os }}-",
        },
    }
    if not any(step.get("name") == "Cache uv" for step in steps if isinstance(step, dict)):
        for index, step in enumerate(steps):
            if isinstance(step, dict) and "uv sync" in str(step.get("run", "")):
                steps.insert(index, cache_step)
                break
    return config


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[4]
    config = load_ci_config(repo_root)

    print("当前 Python 版本矩阵:", get_main_python_versions(config))
    trigger_config = config.get("on", {})
    print("触发事件:", list(trigger_config.keys()) if isinstance(trigger_config, dict) else trigger_config)
