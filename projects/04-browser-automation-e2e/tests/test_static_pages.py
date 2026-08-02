"""静态页面结构测试。"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("bs4", reason="需要 beautifulsoup4")
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
PAGES = ROOT / "pages"


def parse_page(name: str) -> BeautifulSoup:
    return BeautifulSoup((PAGES / name).read_text(), "html.parser")


def test_htmx_demo_has_search_form():
    soup = parse_page("htmx_demo.html")
    search = soup.select_one("#search-input")
    assert search is not None
    assert search.get("hx-get") == "/search"
    assert search.get("hx-target") == "#search-results"
    assert "delay:300ms" in search.get("hx-trigger", "")


def test_htmx_demo_has_add_form():
    soup = parse_page("htmx_demo.html")
    form = soup.select_one("#add-form")
    assert form is not None
    assert form.get("hx-post") == "/items"
    assert form.get("hx-swap") == "beforeend"


def test_capstone_has_document_form():
    soup = parse_page("capstone_demo.html")
    form = soup.select_one("#document-form")
    assert form is not None
    assert form.get("hx-post") == "/documents"
    assert form.get("hx-target") == "#document-result"


def test_capstone_has_chat_form():
    soup = parse_page("capstone_demo.html")
    form = soup.select_one("#chat-form")
    assert form is not None
    assert form.get("hx-get") == "/chat/stream"
    assert form.get("hx-target") == "#answer"


def test_all_pages_include_htmx_script():
    for page in PAGES.glob("*.html"):
        soup = BeautifulSoup(page.read_text(), "html.parser")
        scripts = [s.get("src", "") for s in soup.find_all("script")]
        assert any("htmx" in src.lower() for src in scripts), f"{page.name} 缺 HTMX script"
