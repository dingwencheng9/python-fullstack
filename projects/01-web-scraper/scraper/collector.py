"""数据采集器 — 请求 + 解析 + 去重"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from scraper.policy import CrawlDecision, CrawlPolicy, is_sensitive_url
from scraper.robots import RobotsChecker

logger = logging.getLogger(__name__)


@dataclass
class PageResult:
    """单页采集结果"""

    url: str
    title: str
    text: str
    html: str
    status_code: int
    fetch_time: float
    metadata: dict[str, str] = field(default_factory=dict)


class Collector:
    """网页采集器：请求、解析、去重"""

    def __init__(
        self,
        delay: float = 1.0,
        timeout: int = 10,
        policy: CrawlPolicy | None = None,
        respect_robots: bool = True,
    ) -> None:
        self.delay = delay  # 请求间隔(秒)
        self.timeout = timeout
        self.seen_urls: set[str] = set()
        self.last_fetch: float = 0.0
        self.policy = policy or CrawlPolicy(min_delay=delay)
        self.robots = RobotsChecker(self.policy.user_agent)
        self.respect_robots = respect_robots

    def fetch(self, url: str) -> PageResult | None:
        """采集单页"""
        if url in self.seen_urls:
            logger.debug(f"跳过已采集: {url}")
            return None
        if is_sensitive_url(url):
            logger.warning(f"跳过敏感路径: {url}")
            return None
        if self.respect_robots:
            decision = self.robots.can_fetch(url)
            if not decision.allowed:
                logger.warning(f"robots.txt 禁止采集: {url}")
                return None

        self._rate_limit()
        try:
            resp = requests.get(url, timeout=self.timeout, headers=self.policy.headers())
            policy_result = self.policy.evaluate_response(resp.status_code, resp.text)
            if policy_result.decision in {CrawlDecision.STOP, CrawlDecision.BACKOFF}:
                logger.warning(f"策略停止采集 {url}: {policy_result.reason}")
                return None
            resp.raise_for_status()
        except requests.RequestException:
            logger.exception("请求失败 %s", url)
            return None

        self.seen_urls.add(url)
        start = time.time()
        soup = BeautifulSoup(resp.text, "lxml")
        fetch_time = time.time() - start

        return PageResult(
            url=url,
            title=self._extract_title(soup),
            text=self._extract_text(soup),
            html=resp.text,
            status_code=resp.status_code,
            fetch_time=fetch_time,
            metadata={"content_type": resp.headers.get("content-type", "")},
        )

    def crawl(self, start_url: str, max_pages: int = 10) -> list[PageResult]:
        """多页爬取（自动发现链接）"""
        results: list[PageResult] = []
        queue = [start_url]

        while queue and len(results) < max_pages:
            url = queue.pop(0)
            result = self.fetch(url)
            if result is None:
                continue

            results.append(result)

            # 发现页面内的链接
            soup = BeautifulSoup(result.html, "lxml")
            for link in soup.find_all("a", href=True):
                raw_href = link["href"]
                # bs4 stub 把 attribute 标成 Sequence[str]（理论上多值），实际单值时取首个
                href_value = raw_href if isinstance(raw_href, str) else raw_href[0]
                href = urljoin(url, href_value)
                if self._should_follow(href, start_url):
                    queue.append(href)

        return results

    def _rate_limit(self) -> None:
        """请求间隔控制"""
        elapsed = time.time() - self.last_fetch
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_fetch = time.time()

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取页面标题"""
        if soup.title:
            return soup.title.get_text(strip=True)
        return ""

    def _extract_text(self, soup: BeautifulSoup) -> str:
        """提取正文（移除脚本/样式）"""
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)

    def _should_follow(self, href: str, base_url: str) -> bool:
        """判断是否应跟进该链接"""
        if not href or href in self.seen_urls:
            return False
        parsed = urlparse(href)
        # 只跟进同域链接
        return parsed.netloc == urlparse(base_url).netloc
