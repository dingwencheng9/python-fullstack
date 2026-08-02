"""

from __future__ import annotations

【骨架代码】静态页面测试

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from playwright.sync_api import Page


def test_htmx_page_loads(page: Page) -> None:
    """测试 HTMX 页面能加载，标题正确"""
    # TODO:
    # 1. 创建页面对象
    # 2. 加载页面
    # 3. 断言标题包含 HTMX
    # ← 你的代码写在这里


def test_htmx_no_empty_links(page: Page) -> None:
    """测试页面没有空链接"""
    # TODO:
    # 检查所有 a 标签，href 不为空且不是 #
    # ← 你的代码写在这里


def test_htmx_no_duplicate_ids(page: Page) -> None:
    """测试没有重复 id 属性"""
    # TODO:
    # 收集所有元素的 id，检查重复
    # ← 你的代码写在这里


def test_capstone_page_has_components(page: Page) -> None:
    """测试 Capstone 页面有必要组件"""
    # TODO:
    # 检查查询输入框、提交按钮、答案区域存在
    # ← 你的代码写在这里
