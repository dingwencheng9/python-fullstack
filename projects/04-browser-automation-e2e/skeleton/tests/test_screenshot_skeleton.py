"""

from __future__ import annotations

【骨架代码】截图测试

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page


def test_screenshot_htmx(page: Page, artifacts_dir: Path) -> None:
    """保存 HTMX 页面截图"""
    # TODO:
    # 1. 加载页面
    # 2. 截图保存到 artifacts_dir / "htmx.png"
    # 3. 断言截图文件存在
    # ← 你的代码写在这里


def test_screenshot_capstone(page: Page, artifacts_dir: Path, capstone_url: str) -> None:
    """保存 Capstone 页面截图"""
    # TODO:
    # 1. 加载页面
    # 2. 截图保存
    # ← 你的代码写在这里
