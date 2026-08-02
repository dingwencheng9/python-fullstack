"""

from __future__ import annotations

Freelance Demo 测试配置

提供测试夹具和共享工具。
"""

from pathlib import Path

import pytest


@pytest.fixture
def project_root():
    """项目根目录"""
    return Path(__file__).parent.parent


@pytest.fixture
def templates_dir(project_root):
    """模板目录"""
    return project_root / "templates"


@pytest.fixture
def output_dir(tmp_path):
    """临时输出目录"""
    output = tmp_path / "output"
    output.mkdir()
    return output
