"""

from __future__ import annotations

【骨架代码】AI 全栈应用页面对象

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from playwright.sync_api import Page

from .base_page_skeleton import BasePage


class CapstonePage(BasePage):
    """AI 全栈 Capstone 页面"""

    def __init__(self, page: Page):
        # TODO:
        # 调用父类 __init__
        # 定义选择器：
        # - self.query_input = "#query-input"
        # - self.submit_button = "#submit-button"
        # - self.answer_area = "#answer-area"
        # - self.document_upload = "#document-upload"
        # ← 你的代码写在这里
        pass

    def load(self, base_url: str) -> None:
        """加载页面"""
        # TODO: 导航到 Capstone 首页
        # ← 你的代码写在这里

    def ask_question(self, question: str) -> None:
        """提问"""
        # TODO:
        # 1. 填写问题
        # 2. 点击提交
        # ← 你的代码写在这里

    def wait_for_answer(self) -> None:
        """等待回答完成（SSE 流式输出）"""
        # TODO: 等待回答区域有内容
        # ← 你的代码写在这里

    def get_answer_text(self) -> str:
        """获取回答文本"""
        # TODO: 返回回答文本
        # ← 你的代码写在这里

    def upload_document(self, file_path: str) -> None:
        """上传文档"""
        # TODO: 使用 page.set_input_files 上传文件
        # ← 你的代码写在这里
