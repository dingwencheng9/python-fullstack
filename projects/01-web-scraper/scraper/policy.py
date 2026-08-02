"""爬虫合规策略：限速、透明 UA、封禁识别、退避。"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from enum import StrEnum


class CrawlDecision(StrEnum):
    """采集决策。"""

    ALLOW = "allow"
    SKIP = "skip"
    BACKOFF = "backoff"
    STOP = "stop"


@dataclass(frozen=True)
class PolicyResult:
    """策略检查结果。"""

    decision: CrawlDecision
    reason: str
    wait_seconds: float = 0.0


@dataclass
class CrawlPolicy:
    """合规采集策略。

    目标是"能安全停止"，不是"绕过限制"。
    """

    user_agent: str = "PythonFullstackCourseBot/1.0 (+educational; contact: course-local)"
    min_delay: float = 1.0
    max_retry: int = 3
    blocked_statuses: set[int] = field(default_factory=lambda: {401, 403, 429})
    block_markers: tuple[str, ...] = (
        "captcha",
        "verify you are human",
        "access denied",
        "too many requests",
        "验证码",
        "访问受限",
    )

    def headers(self) -> dict[str, str]:
        """返回透明 User-Agent 请求头。"""
        return {"User-Agent": self.user_agent}

    def should_stop_for_status(self, status_code: int) -> bool:
        """遇到明确封禁/认证状态时停止。"""
        return status_code in self.blocked_statuses

    def detect_block_page(self, html: str) -> bool:
        """识别验证码/封禁页面。"""
        lowered = html.lower()
        return any(marker.lower() in lowered for marker in self.block_markers)

    def backoff_seconds(self, attempt: int) -> float:
        """指数退避。"""
        attempt = max(attempt, 1)
        delay: float = self.min_delay * (2 ** (attempt - 1))
        return min(60.0, delay)

    def evaluate_response(self, status_code: int, html: str = "", attempt: int = 1) -> PolicyResult:
        """根据状态码和页面内容决定下一步。"""
        if self.should_stop_for_status(status_code):
            if status_code == 429 and attempt <= self.max_retry:
                return PolicyResult(
                    CrawlDecision.BACKOFF, "rate limited", self.backoff_seconds(attempt)
                )
            return PolicyResult(CrawlDecision.STOP, f"blocked status: {status_code}")
        if self.detect_block_page(html):
            return PolicyResult(CrawlDecision.STOP, "block page detected")
        return PolicyResult(CrawlDecision.ALLOW, "ok")


class RateLimiter:
    """简单限速器。"""

    def __init__(self, min_delay: float) -> None:
        self.min_delay = min_delay
        self.last_request = 0.0

    def wait(self) -> None:
        """等待到允许请求的时间点。"""
        elapsed = time.time() - self.last_request
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request = time.time()


def is_sensitive_url(url: str) -> bool:
    """简单识别不应采集的敏感路径。"""
    return bool(re.search(r"/(login|logout|admin|account|checkout|payment)", url, re.I))
