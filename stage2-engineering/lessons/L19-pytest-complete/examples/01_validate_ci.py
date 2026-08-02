"""L17 示例 5: CI 配置验证器。读取并校验 .github/workflows/ci.yml。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_ci_config(path: str | Path = ".github/workflows/ci.yml") -> dict[str, Any]:
    """加载 CI 配置 YAML，并兼容 PyYAML 对 `on` 的布尔解析。"""
    config = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise TypeError("CI 配置应解析为 dict")
    if True in config and "on" not in config:
        config["on"] = config.pop(True)
    return config


def validate_ci_config(config: dict[str, Any]) -> list[str]:
    """校验 CI 配置完整性。"""
    errors: list[str] = []
    if "name" not in config:
        errors.append("缺 name 字段")
    if "on" not in config:
        errors.append("缺 on 触发")
    jobs = config.get("jobs", {})
    if not isinstance(jobs, dict) or not jobs:
        errors.append("缺 jobs")
        return errors
    for name, job in jobs.items():
        if not isinstance(job, dict):
            errors.append(f"job {name} 不是 dict")
            continue
        steps = job.get("steps", [])
        if not steps:
            errors.append(f"job {name} 无 steps")
    return errors


def get_python_versions(config: dict[str, Any]) -> list[str]:
    """获取测试矩阵中的 Python 版本，兼容 include 与 python-version 两种写法。"""
    matrix = config.get("jobs", {}).get("test", {}).get("strategy", {}).get("matrix", {})
    if not isinstance(matrix, dict):
        return []
    versions = matrix.get("python-version")
    if isinstance(versions, list):
        return [str(version) for version in versions]
    include = matrix.get("include")
    if isinstance(include, list):
        return [str(item["python-version"]) for item in include if isinstance(item, dict) and "python-version" in item]
    return []


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[4]
    config = load_ci_config(repo_root / ".github" / "workflows" / "ci.yml")
    print("Python 版本:", get_python_versions(config))
    errs = validate_ci_config(config)
    print("校验通过" if not errs else f"问题: {errs}")
