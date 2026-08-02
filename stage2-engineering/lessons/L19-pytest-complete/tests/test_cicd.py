"""L17 CI/CD 测试。"""

from __future__ import annotations

import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[4]  # Go up to repo root
HERE = pathlib.Path(__file__).parent.parent
CI_FILE = ROOT / ".github" / "workflows" / "ci.yml"


def test_ci_file_exists():
    """验证仓库中有 CI 配置文件"""
    assert CI_FILE.exists(), ".github/workflows/ci.yml 不存在"
    content = CI_FILE.read_text()
    assert len(content) > 50, "CI 配置太短"


def test_ci_has_trigger():
    """验证 CI 配置了触发事件"""
    content = CI_FILE.read_text()
    assert "push" in content, "需要 push 触发"
    assert "pull_request" in content, "需要 pull_request 触发"


def test_ci_has_matrix():
    """验证 CI 配置了矩阵测试（项目锁定 Python 3.13，矩阵以 3.13 为主）"""
    content = CI_FILE.read_text()
    assert "matrix" in content, "需要 matrix 多版本测试"
    assert "3.13" in content, "应包含 Python 3.13（项目最低要求）"


def test_ci_has_ruff():
    """验证 CI 包含 ruff 检查"""
    content = CI_FILE.read_text()
    assert "ruff" in content.lower(), "应包含 ruff lint"


def test_ci_has_pytest():
    """验证 CI 包含 pytest"""
    content = CI_FILE.read_text()
    assert "pytest" in content.lower(), "应包含 pytest"


def test_ci_has_uv():
    """验证 CI 使用 uv"""
    content = CI_FILE.read_text()
    assert "uv sync" in content, "应使用 uv sync"


@pytest.mark.parametrize(
    "keyword,desc",
    [
        ("ruff", "代码检查"),
        ("pytest", "测试框架"),
        ("matrix", "多版本测试"),
        ("uv sync", "依赖安装"),
    ],
)
def test_ci_contains_keyword(keyword, desc):
    """参数化：CI 配置包含关键组件"""
    content = CI_FILE.read_text()
    assert keyword in content, f"配置中应包含 {desc} ({keyword})"


@pytest.mark.parametrize(
    "file_suffix,expected_count",
    [
        ("*.yml", 1),  # CI file
    ],
)
def test_workflow_file_patterns(file_suffix, expected_count):
    """参数化：工作流文件存在性"""
    files = list(ROOT.glob(f".github/workflows/{file_suffix}"))
    assert len(files) >= expected_count


def test_examples_valid():
    """验证示例工作流文件为合法 YAML"""
    examples = sorted(HERE.glob("examples/*.yml"))
    assert len(examples) >= 2, "至少需要 2 个示例"
    for ex in examples:
        content = ex.read_text()
        assert "name:" in content, f"{ex.name} 缺 name 字段"
        assert "on:" in content, f"{ex.name} 缺 on 触发"
        assert "jobs:" in content, f"{ex.name} 缺 jobs 配置"
