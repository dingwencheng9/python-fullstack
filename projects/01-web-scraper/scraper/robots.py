"""robots.txt 合规检查。"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests


@dataclass(frozen=True)
class RobotsDecision:
    """robots.txt 决策。"""

    allowed: bool
    robots_url: str
    reason: str


class RobotsChecker:
    """robots.txt 检查器。"""

    def __init__(self, user_agent: str) -> None:
        self.user_agent = user_agent
        self.cache: dict[str, RobotFileParser] = {}

    def can_fetch(self, url: str) -> RobotsDecision:
        """判断 URL 是否允许抓取。"""
        parsed = urlparse(url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        robots_url = urljoin(origin, "/robots.txt")
        parser = self.cache.get(origin)
        if parser is None:
            parser = self._load_parser(robots_url)
            self.cache[origin] = parser
        allowed = parser.can_fetch(self.user_agent, url)
        reason = "allowed by robots.txt" if allowed else "blocked by robots.txt"
        return RobotsDecision(allowed, robots_url, reason)

    def _load_parser(self, robots_url: str) -> RobotFileParser:
        parser = RobotFileParser()
        parser.set_url(robots_url)
        try:
            response = requests.get(robots_url, timeout=5, headers={"User-Agent": self.user_agent})
            if response.status_code == 200:
                parser.parse(response.text.splitlines())
            else:
                parser.parse([])  # 无 robots 或不可读时默认允许
        except requests.RequestException:
            parser.parse([])
        return parser


def parse_robots_text(text: str, user_agent: str, url: str) -> RobotsDecision:
    """纯文本 robots 测试辅助函数。"""
    parser = RobotFileParser()
    parser.parse(text.splitlines())
    return RobotsDecision(
        allowed=parser.can_fetch(user_agent, url),
        robots_url="inline://robots.txt",
        reason="parsed inline robots.txt",
    )
