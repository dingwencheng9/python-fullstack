"""爬虫合规策略测试。"""

from __future__ import annotations

import pytest

from scraper.policy import CrawlDecision, CrawlPolicy, RateLimiter, is_sensitive_url
from scraper.robots import parse_robots_text


def test_policy_headers_are_transparent():
    policy = CrawlPolicy()
    headers = policy.headers()
    assert "User-Agent" in headers
    assert "PythonFullstackCourseBot" in headers["User-Agent"]


@pytest.mark.parametrize("status", [401, 403])
def test_blocked_status_stops(status: int):
    policy = CrawlPolicy()
    result = policy.evaluate_response(status)
    assert result.decision == CrawlDecision.STOP


def test_429_backs_off_before_retry_limit():
    policy = CrawlPolicy(max_retry=3)
    result = policy.evaluate_response(429, attempt=2)
    assert result.decision == CrawlDecision.BACKOFF
    assert result.wait_seconds >= policy.min_delay


def test_429_stops_after_retry_limit():
    policy = CrawlPolicy(max_retry=1)
    result = policy.evaluate_response(429, attempt=2)
    assert result.decision == CrawlDecision.STOP


@pytest.mark.parametrize(
    "html",
    [
        "<html>captcha required</html>",
        "<html>验证码</html>",
        "<html>Access Denied</html>",
    ],
)
def test_detect_block_page(html: str):
    policy = CrawlPolicy()
    assert policy.detect_block_page(html) is True


def test_allowed_response():
    policy = CrawlPolicy()
    result = policy.evaluate_response(200, "<html>ok</html>")
    assert result.decision == CrawlDecision.ALLOW


@pytest.mark.parametrize(("attempt", "expected_min"), [(1, 1.0), (2, 2.0), (3, 4.0)])
def test_backoff_seconds(attempt: int, expected_min: float):
    policy = CrawlPolicy(min_delay=1.0)
    assert policy.backoff_seconds(attempt) >= expected_min


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/login",
        "https://example.com/admin/users",
        "https://shop.example.com/checkout",
        "https://pay.example.com/payment/123",
    ],
)
def test_sensitive_urls(url: str):
    assert is_sensitive_url(url) is True


def test_robots_allows_public_path():
    text = "User-agent: *\nDisallow: /private\n"
    decision = parse_robots_text(text, "CourseBot", "https://example.com/public")
    assert decision.allowed is True


def test_robots_blocks_private_path():
    text = "User-agent: *\nDisallow: /private\n"
    decision = parse_robots_text(text, "CourseBot", "https://example.com/private/data")
    assert decision.allowed is False


def test_rate_limiter_wait_updates_timestamp():
    limiter = RateLimiter(min_delay=0)
    limiter.wait()
    assert limiter.last_request > 0
