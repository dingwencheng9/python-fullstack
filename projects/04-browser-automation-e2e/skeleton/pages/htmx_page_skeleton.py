"""

from __future__ import annotations

【骨架代码】HTMX 演示页面对象

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from playwright.sync_api import Page

from .base_page_skeleton import BasePage


class HtmxDemoPage(BasePage):
    """HTMX 演示页面"""

    def __init__(self, page: Page):
        # TODO: 调用父类 __init__
        # 定义选择器：
        # - self.input_selector = "#demo-input"
        # - self.button_selector = "#demo-button"
        # - self.result_selector = "#result"
        # ← 你的代码写在这里
        pass

    def load(self) -> None:
        """加载页面"""
        # TODO: self.goto("/path/to/htmx_demo.html")
        # ← 你的代码写在这里

    def enter_text(self, text: str) -> None:
        """输入文本"""
        # TODO: 调用 self.fill
        # ← 你的代码写在这里

    def click_submit(self) -> None:
        """点击提交"""
        # TODO: 点击按钮
        # ← 你的代码写在这里

    def wait_for_result(self) -> None:
        """等待 HTMX 更新结果"""
        # TODO: 等待结果区域可见
        # ← 你的代码写在这里

    def get_result_text(self) -> str:
        """获取结果文本"""
        # TODO: 返回结果文本
        # ← 你的代码写在这里
