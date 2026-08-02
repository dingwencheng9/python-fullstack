"""练习 1: 编写 fixture。

目标：创建一个 @pytest.fixture 提供临时目录和文件，测试函数使用该
fixture 验证文件读写。参考答案见 solutions/solution_01_write_fixture.py。
"""

from __future__ import annotations

import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir() -> Iterator[Path]:
    """创建临时目录和测试文件，测试完成后自动清理。"""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        (path / "test.txt").write_text("Hello, Test!", encoding="utf-8")
        yield path


def test_read_temp_file(temp_dir: Path) -> None:
    """验证 fixture 提供的临时文件可读。"""
    file_path = temp_dir / "test.txt"
    assert file_path.read_text(encoding="utf-8") == "Hello, Test!"
