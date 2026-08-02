"""Playwright 配置示例。

from __future__ import annotations

真实浏览器测试启用方法：
    pip install playwright pytest-playwright
    playwright install chromium
    pytest tests/ --browser chromium
"""

from pathlib import Path
from typing import TypedDict


class ViewportSize(TypedDict):
    width: int
    height: int


ARTIFACTS_DIR: Path = Path(__file__).parent / "artifacts"
PAGES_DIR: Path = Path(__file__).parent / "pages"

HEADLESS: bool = True
DEFAULT_VIEWPORT: ViewportSize = {"width": 1280, "height": 720}
