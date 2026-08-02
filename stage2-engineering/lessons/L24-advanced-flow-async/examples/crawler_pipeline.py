"""生产级异步爬虫流式数据管道

功能清单:
- 异步HTTP请求（aiohttp）✅
- 流式数据处理（AsyncGenerator）✅
- 限流控制（Semaphore）✅
- 结构化并发（TaskGroup）✅
- 数据库存储（asyncpg）✅
- 性能监控（每秒处理数、成功率）✅
- 优雅关闭（SIGINT）✅
- 完整类型注解（mypy --strict）✅
- 异常处理（except* ExceptionGroup）✅

学生任务：
1. 实现 crawl_page() 函数
2. 实现 crawler_pipeline() 异步生成器
3. 实现 save_to_database() 批量存储
4. 实现性能监控逻辑
5. 实现优雅关闭处理
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import TypedDict

try:
    import aiohttp
    import asyncpg
except ImportError:
    print("请安装依赖: uv add aiohttp asyncpg")
    raise


# ============================================================================
# 数据结构定义
# ============================================================================


@dataclass(frozen=True)
class CrawlerConfig:
    """爬虫配置"""

    max_concurrent: int = 5
    timeout: float = 30.0
    retry_attempts: int = 3
    backoff_factor: float = 2.0
    db_url: str = "postgresql://localhost/crawler"


class PageResult(TypedDict):
    """页面结果类型"""

    url: str
    title: str
    content: str
    status: int
    crawled_at: str


@dataclass
class CrawlerStats:
    """爬虫统计"""

    total: int = 0
    success: int = 0
    failed: int = 0
    start_time: float = field(default_factory=time.time)

    @property
    def success_rate(self) -> float:
        """成功率"""
        return (self.success / self.total * 100) if self.total > 0 else 0.0

    @property
    def elapsed_seconds(self) -> float:
        """运行时间"""
        return time.time() - self.start_time

    @property
    def throughput(self) -> float:
        """吞吐量（每秒处理数）"""
        return self.success / self.elapsed_seconds if self.elapsed_seconds > 0 else 0.0


# ============================================================================
# TODO: 学生需要实现的部分
# ============================================================================


@asynccontextmanager
async def http_session(config: CrawlerConfig) -> AsyncGenerator[aiohttp.ClientSession]:
    """HTTP 会话上下文管理器

    TODO: 实现以下功能
    1. 创建 ClientSession，配置 timeout 和 connector
    2. 使用 try/finally 确保资源清理
    3. 返回 session 供外部使用
    """
    # TODO: 实现
    raise NotImplementedError("请实现 http_session")


async def crawl_page(
    url: str,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    config: CrawlerConfig,
) -> PageResult:
    """爬取单个页面

    TODO: 实现以下功能
    1. 使用 semaphore 限流
    2. 实现重试逻辑（指数退避）
    3. 提取页面标题
    4. 返回 PageResult

    提示：
    - 使用 async with semaphore 控制并发
    - 使用 for attempt in range(config.retry_attempts) 实现重试
    - 使用 response.text() 获取 HTML
    - 简单提取标题：查找 <title> 标签
    """
    # TODO: 实现
    raise NotImplementedError("请实现 crawl_page")


async def crawler_pipeline(
    urls: list[str],
    config: CrawlerConfig,
) -> AsyncGenerator[PageResult]:
    """爬虫流式管道

    TODO: 实现以下功能
    1. 创建统计对象和 Semaphore
    2. 使用 TaskGroup 并发执行任务
    3. 使用 except* 捕获不同类型异常
    4. 流式产出结果（使用 yield）
    5. 在 finally 块打印统计信息

    提示：
    - 使用 async with http_session(config) as session
    - 使用 async with asyncio.TaskGroup() as tg
    - 使用 tg.create_task() 创建任务
    - 使用 except* aiohttp.ClientError 捕获网络错误
    - 使用 except* asyncio.TimeoutError 捕获超时
    """
    # TODO: 实现
    raise NotImplementedError("请实现 crawler_pipeline")
    yield  # 使其成为生成器（移除此行并实现真正的 yield）


@asynccontextmanager
async def db_connection(config: CrawlerConfig) -> AsyncGenerator[asyncpg.Connection]:
    """数据库连接上下文管理器

    TODO: 实现以下功能
    1. 使用 asyncpg.connect() 连接数据库
    2. 使用 try/finally 确保连接关闭
    3. 返回连接对象
    """
    # TODO: 实现
    raise NotImplementedError("请实现 db_connection")


async def save_to_database(
    results: list[PageResult],
    config: CrawlerConfig,
) -> None:
    """批量保存到数据库

    TODO: 实现以下功能
    1. 连接数据库
    2. 批量插入数据
    3. 处理可能的数据库错误

    提示：
    - 使用 async with db_connection(config) as conn
    - 使用 conn.executemany() 批量插入
    - SQL: INSERT INTO pages (url, title, content, status, crawled_at) VALUES ($1, $2, $3, $4, $5)
    """
    # TODO: 实现
    raise NotImplementedError("请实现 save_to_database")


# ============================================================================
# 主程序
# ============================================================================


async def main() -> None:
    """主函数"""
    # 配置
    config = CrawlerConfig(
        max_concurrent=5,
        timeout=30.0,
        retry_attempts=3,
    )

    # 测试 URL 列表
    urls = [f"https://example.com/page{i}" for i in range(20)]

    print(f"开始爬取 {len(urls)} 个页面...")
    print(f"最大并发: {config.max_concurrent}")
    print(f"超时: {config.timeout}s")
    print(f"重试次数: {config.retry_attempts}")
    print("-" * 60)

    # 收集结果
    results: list[PageResult] = []

    try:
        async for result in crawler_pipeline(urls, config):
            results.append(result)
            print(f"✓ {result['title'][:50]} ({result['status']})")

    except KeyboardInterrupt:
        print("\n\n⚠️ 收到中断信号，正在优雅关闭...")

    # 保存到数据库（如果有结果）
    if results:
        print(f"\n保存 {len(results)} 条结果到数据库...")
        try:
            await save_to_database(results, config)
            print("✓ 保存成功")
        except Exception as e:
            print(f"✗ 保存失败: {e}")


if __name__ == "__main__":
    # 设置信号处理（优雅关闭）
    # TODO: 实现优雅关闭逻辑

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已退出")
