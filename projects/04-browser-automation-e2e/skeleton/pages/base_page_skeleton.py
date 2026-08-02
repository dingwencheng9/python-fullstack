"""

from __future__ import annotations

【骨架代码】基础页面对象 — Page Object 基类

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from playwright.sync_api import Page


class BasePage:
    """基础页面对象，封装所有页面通用操作"""

    def __init__(self, page: Page):
        # TODO:
        # 1. self.page = page
        # 2. self.base_url = 你的基础 URL（file:// 或者 http）
        # ← 你的代码写在这里
        pass

    def goto(self, path: str = "") -> None:
        """导航到指定路径"""
        # TODO: self.page.goto(self.base_url + path)
        # ← 你的代码写在这里

    def get_title(self) -> str:
        """获取页面标题"""
        # TODO: 返回页面标题
        # ← 你的代码写在这里

    def screenshot(self, path: str) -> None:
        """截图保存"""
        # TODO: self.page.screenshot(path=path)
        # ← 你的代码写在这里

    def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        """等待元素出现"""
        # TODO: 等待选择器
        # ← 你的代码写在这里

    def click(self, selector: str) -> None:
        """点击元素"""
        # TODO: 点击
        # ← 你的代码写在这里

    def fill(self, selector: str, text: str) -> None:
        """填写输入框"""
        # TODO: 填写
        # ← 你的代码写在这里

    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        # TODO: 获取文本
        # ← 你的代码写在这里

    def is_visible(self, selector: str) -> bool:
        """判断元素是否可见"""
        # TODO: 返回是否可见
        # ← 你的代码写在这里
