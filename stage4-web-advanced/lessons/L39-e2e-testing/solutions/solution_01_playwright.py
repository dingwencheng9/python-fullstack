"""Solution: Playwright E2E Testing with Page Object"""

from playwright.sync_api import Page, sync_playwright


class BasePage:
    """Base page object with common actions."""

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def click(self, selector: str):
        self.page.click(selector)

    def fill(self, selector: str, value: str):
        self.page.fill(selector, value)

    def wait_for(self, selector: str, timeout: int = 30000):
        return self.page.wait_for_selector(selector, timeout=timeout)


class LoginPage(BasePage):
    """Login page object."""

    USERNAME = "#username"
    PASSWORD = "#password"
    SUBMIT = 'button[type="submit"]'
    ERROR = ".error-message"
    SUCCESS = ".success-message"

    def __init__(self, page: Page, base_url: str = "http://localhost:8000"):
        super().__init__(page)
        self.base_url = base_url

    def navigate(self):
        self.goto(f"{self.base_url}/login")

    def login(self, username: str, password: str) -> bool:
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.SUBMIT)

        try:
            self.wait_for(self.SUCCESS, timeout=5000)
            return True
        except Exception:
            return False

    def get_error(self) -> str | None:
        try:
            error = self.wait_for(self.ERROR, timeout=2000)
            return error.text_content()
        except Exception:
            return None


class DashboardPage(BasePage):
    """Dashboard page object."""

    TITLE = "h1.dashboard-title"
    USER_MENU = ".user-menu"
    LOGOUT = "button.logout"

    def is_loaded(self) -> bool:
        try:
            self.wait_for(self.TITLE)
            return True
        except Exception:
            return False


def run_e2e_tests():
    """Run E2E tests with Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Test login flow
        login_page = LoginPage(page)
        login_page.navigate()

        result = login_page.login("testuser", "testpass")
        assert result, "Login should succeed"

        # Test dashboard
        dashboard = DashboardPage(page)
        assert dashboard.is_loaded(), "Dashboard should load"

        browser.close()
        print("All E2E tests passed!")


if __name__ == "__main__":
    run_e2e_tests()
