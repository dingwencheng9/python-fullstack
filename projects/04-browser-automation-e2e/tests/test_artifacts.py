"""E2E artifacts 目录测试。"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parent.parent
ARTIFACTS = ROOT / "artifacts"


def test_artifacts_dir_exists():
    assert ARTIFACTS.exists()
    assert ARTIFACTS.is_dir()


def test_gitkeep_present():
    assert (ARTIFACTS / ".gitkeep").exists()


def test_can_write_report_artifact(tmp_path):
    report = tmp_path / "report.txt"
    report.write_text("E2E report")
    assert report.read_text() == "E2E report"
