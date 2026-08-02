"""Example 2: Advanced Test Fixtures"""

import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext


@pytest.fixture(scope="session")
def browser():
    """Session-scoped browser fixture."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def context(browser: Browser):
    """Function-scoped context with auth."""
    context = browser.new_context()
    # Pre-authenticate
    context.add_cookies([{"name": "session_id", "value": "test-session-123", "domain": "localhost", "path": "/"}])
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    """Function-scoped page."""
    page = context.new_page()
    yield page
    page.close()


def test_authenticated_request(page: Page):
    """Test with pre-authenticated user."""
    page.goto("http://localhost:8000/profile")
    # Session cookie is already set
    assert "Profile" in page.title() or page.url.endswith("/profile")


@pytest.fixture
def test_data():
    """Provide test data for tests."""
    return {
        "users": [
            {"name": "Alice", "email": "alice@test.com"},
            {"name": "Bob", "email": "bob@test.com"},
        ],
        "posts": [
            {"title": "First Post", "content": "Hello World"},
        ],
    }


def test_with_data(page: Page, test_data):
    """Test using shared test data."""
    user = test_data["users"][0]
    page.goto("http://localhost:8000/users/new")
    page.fill("#name", user["name"])
    page.fill("#email", user["email"])
    # ...
