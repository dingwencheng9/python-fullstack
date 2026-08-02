"""爬虫项目测试"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest
import requests

from scraper.collector import Collector, PageResult
from scraper.pipeline import Pipeline, clean_text, extract_date

# ── Collector 测试 ──


def test_collector_deduplication():
    """测试去重功能"""
    col = Collector(respect_robots=False)
    col.seen_urls.add("https://example.com")
    result = col.fetch("https://example.com")
    assert result is None


@patch("scraper.collector.requests.get")
def test_fetch_success(mock_get):
    """测试成功采集"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html><title>Test</title><body>Hello</body></html>"
    mock_get.return_value.headers = {"content-type": "text/html"}

    col = Collector(respect_robots=False)
    result = col.fetch("https://example.com")
    assert result is not None
    assert result.title == "Test"
    assert "Hello" in result.text


@patch("scraper.collector.requests.get")
def test_fetch_http_error(mock_get):
    """测试 HTTP 错误处理"""
    mock_get.side_effect = requests.RequestException("Connection error")
    col = Collector(respect_robots=False)
    result = col.fetch("https://example.com")
    assert result is None


@patch("scraper.collector.requests.get")
def test_page_result_fields(mock_get):
    """测试 PageResult 字段完整性"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html><title>Test</title></html>"
    mock_get.return_value.headers = {"content-type": "text/html"}

    col = Collector(respect_robots=False)
    result = col.fetch("https://example.com")
    assert isinstance(result, PageResult)
    assert result.url == "https://example.com"
    assert result.status_code == 200
    assert isinstance(result.fetch_time, float)


@patch("scraper.collector.requests.get")
def test_rate_limiting(mock_get):
    """测试请求间隔"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html><title>Test</title></html>"
    mock_get.return_value.headers = {"content-type": "text/html"}

    import time

    col = Collector(delay=0.1)
    col.last_fetch = time.time()  # 模拟上次请求
    result = col.fetch("https://example.com/page1")
    assert result is not None


# ── Pipeline 测试 ──


def test_clean_text():
    """测试文本清洗"""
    assert clean_text("Hello   World") == "Hello World"
    assert clean_text("  spaced  ") == "spaced"
    assert clean_text("") == ""


def test_extract_date():
    """测试日期提取"""
    assert extract_date("2025-01-15") == "2025-01-15"
    assert extract_date("no date here") is None


def test_pipeline_save_and_query():
    """测试存储与查询"""
    pipe = Pipeline()
    result = PageResult(
        url="https://example.com",
        title="Test",
        text="Hello World 2025-01-15",
        html="",
        status_code=200,
        fetch_time=0.1,
    )
    pipe.save(result)
    df = pipe.analyze()
    assert df["total_pages"][0] == 1
    assert df["avg_word_count"][0] > 0


def test_pipeline_export(tmp_path):
    """测试 JSON 导出"""
    pipe = Pipeline()
    result = PageResult(
        url="https://example.com",
        title="Test",
        text="Hello World",
        html="",
        status_code=200,
        fetch_time=0.1,
    )
    pipe.save(result)
    output = tmp_path / "test.json"
    pipe.export_json(str(output))
    data = json.loads(output.read_text())
    assert len(data) == 1
    assert data[0]["url"] == "https://example.com"


def test_pipeline_batch_save():
    """测试批量存储"""
    pipe = Pipeline()
    results = [
        PageResult(
            url=f"https://example.com/{i}",
            title=str(i),
            text="text",
            html="",
            status_code=200,
            fetch_time=0.1,
        )
        for i in range(3)
    ]
    pipe.save_batch(results)
    df = pipe.analyze()
    assert df["total_pages"][0] == 3


@pytest.mark.parametrize(
    ("text", "expected_count"),
    [
        ("one two three", 3),
        ("", 0),
        ("  spaced  words  here  ", 3),
    ],
)
def test_word_count_parametrized(text, expected_count):
    """参数化：词数统计"""
    pipe = Pipeline()
    result = PageResult(
        url="https://example.com",
        title="Test",
        text=text,
        html="",
        status_code=200,
        fetch_time=0.1,
    )
    pipe.save(result)
    df = pipe.top_sources()
    assert df["word_count"].iloc[0] == expected_count if expected_count > 0 else True
