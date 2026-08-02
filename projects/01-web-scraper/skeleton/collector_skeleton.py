"""

from __future__ import annotations

【骨架代码】数据采集器 — 请求 + 解析 + 去重

TODO: 按照注释提示，补全代码，实现一个完整的爬虫
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

# 导入已经写好的策略模块（不需要修改）
from scraper.policy import CrawlPolicy

logger = logging.getLogger(__name__)


@dataclass
class PageResult:
    """单页采集结果（不需要修改）"""

    url: str
    title: str
    text: str
    html: str
    status_code: int
    fetch_time: float
    metadata: dict = field(default_factory=dict)


class Collector:
    """网页采集器：请求、解析、去重"""

    def __init__(
        self,
        delay: float = 1.0,
        timeout: int = 10,
        policy: CrawlPolicy | None = None,
        respect_robots: bool = True,
    ) -> None:
        # TODO: 初始化以下属性：
        # 1. self.delay = 请求间隔（秒）
        # 2. self.timeout = 请求超时（秒）
        # 3. self.seen_urls = 空集合，用来存储已经爬过的URL
        # 4. self.last_fetch = 0.0，记录上次请求时间，用来限速
        # 5. self.policy = 传入的policy或者默认CrawlPolicy(min_delay=delay)
        # 6. self.robots = RobotsChecker(self.policy.user_agent)， robots.txt检查器
        # 7. self.respect_robots = 传入的respect_robots参数，是否遵守robots.txt
        pass  # ← 你的代码写在这里

    def fetch(self, url: str) -> PageResult | None:
        """采集单页

        步骤：
        1. 检查URL是否已经爬过，如果是，跳过
        2. 检查是否是敏感路径，如果是，跳过
        3. 如果respect_robots为True，检查robots.txt是否允许爬取
        4. 调用_rate_limit()限速
        5. 发送GET请求，设置超时和请求头
        6. 评估响应状态，根据policy决定是否继续
        7. 解析HTML，提取标题和正文
        8. 返回PageResult对象
        """
        # TODO: 实现上面的步骤
        # 提示：
        # - requests.get()发送请求
        # - BeautifulSoup解析HTML
        # - self._extract_title()提取标题
        # - self._extract_text()提取正文
        # ← 你的代码写在这里

    def crawl(self, start_url: str, max_pages: int = 10) -> list[PageResult]:
        """多页爬取（自动发现链接）

        步骤：
        1. 初始化队列，把start_url放进去
        2. 当队列不为空，且结果数量小于max_pages时：
           a. 取出队列第一个URL
           b. 调用fetch()采集
           c. 如果采集成功，加入结果列表
           d. 提取页面内的所有链接
           e. 符合跟进条件的链接加入队列
        3. 返回所有采集结果
        """
        # TODO: 实现广度优先爬取
        # 提示：
        # - 使用列表作为队列，pop(0)取出第一个元素
        # - urljoin()合并相对URL为绝对URL
        # - self._should_follow()判断是否应该跟进链接
        # ← 你的代码写在这里

    def _rate_limit(self) -> None:
        """请求间隔控制

        步骤：
        1. 计算距离上次请求的时间elapsed
        2. 如果elapsed < self.delay，sleep相应的时间
        3. 更新self.last_fetch为当前时间
        """
        # TODO: 实现限速逻辑
        # ← 你的代码写在这里

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取页面标题

        步骤：
        1. 如果soup有title标签，返回其中的文本（去掉前后空白）
        2. 否则返回空字符串
        """
        # TODO: 实现标题提取
        # ← 你的代码写在这里

    def _extract_text(self, soup: BeautifulSoup) -> str:
        """提取正文（移除脚本/样式/导航/页脚/页头）

        步骤：
        1. 移除soup中的["script", "style", "nav", "footer", "header"]标签
        2. 提取所有文本，用换行分隔，去掉前后空白
        """
        # TODO: 实现正文提取
        # 提示：tag.decompose()移除标签
        # 提示：soup.get_text(separator="\n", strip=True)提取文本
        # ← 你的代码写在这里

    def _should_follow(self, href: str, base_url: str) -> bool:
        """判断是否应跟进该链接

        步骤：
        1. 如果href为空或者已经在self.seen_urls中，返回False
        2. 解析href和base_url的域名
        3. 只跟进同域的链接（parsed.netloc相等）
        """
        # TODO: 实现链接跟进判断
        # 提示：urlparse()解析URL的netloc
        # ← 你的代码写在这里
