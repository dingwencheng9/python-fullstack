"""用户交互意图测试。

from __future__ import annotations

不启动真实浏览器，先从 HTML 结构验证用户路径是否完整。
"""

from pathlib import Path

import pytest

pytest.importorskip("bs4", reason="需要 beautifulsoup4")
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
PAGES = ROOT / "pages"


@pytest.mark.parametrize(
    ("page", "required_ids"),
    [
        ("htmx_demo.html", ["search-input", "search-results", "add-form", "item-list"]),
        ("capstone_demo.html", ["document-form", "document-result", "chat-form", "answer"]),
    ],
)
def test_required_interaction_targets_exist(page: str, required_ids: list[str]):
    soup = BeautifulSoup((PAGES / page).read_text(), "html.parser")
    for element_id in required_ids:
        assert soup.select_one(f"#{element_id}") is not None, f"{page} 缺 #{element_id}"


@pytest.mark.parametrize("page", ["htmx_demo.html", "capstone_demo.html"])
def test_no_duplicate_ids(page: str):
    soup = BeautifulSoup((PAGES / page).read_text(), "html.parser")
    ids = [tag.get("id") for tag in soup.find_all(id=True)]
    assert len(ids) == len(set(ids)), f"{page} 存在重复 id"


@pytest.mark.parametrize("page", ["htmx_demo.html", "capstone_demo.html"])
def test_required_inputs_have_labels_or_placeholders(page: str):
    soup = BeautifulSoup((PAGES / page).read_text(), "html.parser")
    for input_tag in soup.find_all(["input", "textarea"]):
        has_label = bool(soup.select_one(f'label[for="{input_tag.get("id")}"]'))
        has_placeholder = bool(input_tag.get("placeholder"))
        assert has_label or has_placeholder, f"{page} 输入框缺 label/placeholder"


def test_capstone_chat_supports_streaming_target():
    soup = BeautifulSoup((PAGES / "capstone_demo.html").read_text(), "html.parser")
    answer = soup.select_one("#answer")
    assert answer is not None
    assert answer.get("aria-live") == "polite"
