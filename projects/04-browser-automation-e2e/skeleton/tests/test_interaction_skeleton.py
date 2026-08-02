"""

from __future__ import annotations

【骨架代码】交互测试

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from playwright.sync_api import Page


def test_htmx_submit_interaction(page: Page) -> None:
    """测试 HTMX 点击提交后更新结果"""
    # TODO:
    # 1. 加载页面
    # 2. 输入文本
    # 3. 点击提交
    # 4. 等待结果更新
    # 5. 断言结果包含输入文本
    # ← 你的代码写在这里


def test_capstone_question_interaction(page: Page, capstone_url: str) -> None:
    """测试 Capstone 提问交互"""
    # TODO:
    # 1. 加载页面
    # 2. 输入问题
    # 3. 提交
    # 4. 等待回答
    # 5. 断言回答不为空
    # ← 你的代码写在这里
