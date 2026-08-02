"""Tests for E2E Testing module."""

from __future__ import annotations

import pytest

pytest.importorskip("playwright", reason="playwright 未安装；可选依赖")

# 使用 module 级别的全局变量，由 fixture 注入
LoginPage = None  # type: ignore[assignment]
DashboardPage = None  # type: ignore[assignment]


@pytest.fixture(autouse=True)
def _inject_solutions(solutions, request) -> None:
    """从 solutions 模块动态注入被测类，避免静态导入。"""
    try:
        request.module.LoginPage = solutions.solution_01_playwright.LoginPage
        request.module.DashboardPage = solutions.solution_01_playwright.DashboardPage
    except (AttributeError, ImportError) as e:
        pytest.skip(f"无法导入解决方案模块: {e}")


class TestPageObjects:
    """Test Page Object pattern."""

    def test_login_page_selectors(self) -> None:
        """Test that LoginPage has correct selectors."""
        assert LoginPage.USERNAME == "#username"
        assert LoginPage.PASSWORD == "#password"
        assert LoginPage.SUBMIT == 'button[type="submit"]'

    def test_dashboard_selectors(self) -> None:
        """Test that DashboardPage has correct selectors."""
        assert DashboardPage.TITLE == "h1.dashboard-title"
        assert DashboardPage.USER_MENU == ".user-menu"


class TestMockPage:
    """Test with mock page."""

    def test_login_page_object(self) -> None:
        """Test LoginPage object creation."""

        class MockPage:
            def fill(self, selector: str, value: str) -> None:
                pass

            def click(self, selector: str) -> None:
                pass

            def wait_for_selector(self, selector: str, timeout: int = 30000) -> object:
                class MockElement:
                    def text_content(self) -> str:
                        return "Success"

                return MockElement()

        page = MockPage()
        login = LoginPage(page, base_url="http://test.local")
        assert login.base_url == "http://test.local"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
