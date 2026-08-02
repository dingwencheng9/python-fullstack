"""Exercise 1: Playwright E2E Test"""


class LoginPage:
    """Login Page Object"""

    def __init__(self, page):
        self.page = page

    USERNAME = "#username"
    PASSWORD = "#password"
    SUBMIT = 'button[type="submit"]'

    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME, username)
        self.page.fill(self.PASSWORD, password)
        self.page.click(self.SUBMIT)


def test():
    # Placeholder test
    print("PASS: Page Object pattern defined")


if __name__ == "__main__":
    test()
