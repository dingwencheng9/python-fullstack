"""示例 1: Playwright 基础"""

import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.fixture
def browser():
    """浏览器 Fixture"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """页面 Fixture"""
    page = browser.new_page()
    yield page
    page.close()


def test_homepage_loads(page):
    """测试首页加载"""
    page.goto("http://localhost:8000")
    expect(page.locator("h1")).to_be_visible()


def test_login_flow(page):
    """测试登录流程"""
    page.goto("http://localhost:8000/login")
    page.fill("#username", "testuser")
    page.fill("#password", "testpass")
    page.click("button[type=submit]")
    expect(page.locator(".success-message")).to_be_visible()
