"""练习 1 参考答案: fixture 管理临时文件"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """创建临时目录和文件，测试后清理。"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.txt"
        file_path.write_text("Hello, Test!", encoding="utf-8")
        yield tmpdir
        # 离开 with 块自动清理


def test_read_temp_file(temp_dir):
    file_path = Path(temp_dir) / "test.txt"
    content = file_path.read_text(encoding="utf-8")
    assert content == "Hello, Test!"
