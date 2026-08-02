"""生产级异步爬虫流式数据管道 - 标准答案

完整实现所有功能：
- 异步HTTP请求（aiohttp）✅
- 流式数据处理（AsyncGenerator）✅
- 限流控制（Semaphore）✅
- 结构化并发（TaskGroup）✅
- 数据库存储（asyncpg）✅
- 性能监控（每秒处理数、成功率）✅
- 优雅关闭（SIGINT）✅
- 完整类型注解（mypy --strict）✅
- 异常处理（except* ExceptionGroup）✅
"""

from __future__ import annotations

import asyncio
import signal
import sys
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import TypedDict

try:
    import aiohttp
    import asyncpg
    import pytest

    _NETWORK_DEPS_AVAILABLE = True
except ImportError:
    aiohttp = None  # type: ignore[assignment]
    asyncpg = None  # type: ignore[assignment]
    pytest = None  # type: ignore[assignment]
    _NETWORK_DEPS_AVAILABLE = False


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
    batch_size: int = 10


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
# HTTP 会话管理
# ============================================================================


@asynccontextmanager
async def http_session(config: CrawlerConfig) -> AsyncGenerator[aiohttp.ClientSession]:
    """HTTP 会话上下文管理器"""
    timeout = aiohttp.ClientTimeout(total=config.timeout)
    connector = aiohttp.TCPConnector(
        limit=config.max_concurrent,
        limit_per_host=config.max_concurrent,
    )

    session = aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        headers={"User-Agent": "Mozilla/5.0 CrawlerPipeline/1.0"},
    )

    try:
        yield session
    finally:
        await session.close()
        # 等待连接完全关闭
        await asyncio.sleep(0.25)


# ============================================================================
# 页面爬取
# ============================================================================


async def crawl_page(
    url: str,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    config: CrawlerConfig,
) -> PageResult:
    """爬取单个页面"""
    async with semaphore:
        last_exception: Exception | None = None

        for attempt in range(config.retry_attempts):
            try:
                async with session.get(url) as response:
                    html = await response.text()

                    # 简单提取标题
                    title = "Untitled"
                    if "<title>" in html:
                        start = html.find("<title>") + 7
                        end = html.find("</title>", start)
                        if end > start:
                            title = html[start:end].strip()

                    # 截断内容（避免过大）
                    content = html[:1000] if len(html) > 1000 else html

                    return PageResult(
                        url=url,
                        title=title,
                        content=content,
                        status=response.status,
                        crawled_at=datetime.now().isoformat(),
                    )

            except (TimeoutError, aiohttp.ClientError) as e:
                last_exception = e

                if attempt < config.retry_attempts - 1:
                    wait_time = config.backoff_factor**attempt
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise

        # 理论上不会到达这里，但为了类型检查
        if last_exception:
            raise last_exception
        raise RuntimeError("Unexpected state")


# ============================================================================
# 爬虫管道
# ============================================================================


async def crawler_pipeline(
    urls: list[str],
    config: CrawlerConfig,
) -> AsyncGenerator[PageResult]:
    """爬虫流式管道"""
    stats = CrawlerStats(total=len(urls))
    semaphore = asyncio.Semaphore(config.max_concurrent)

    async with http_session(config) as session:
        try:
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(crawl_page(url, session, semaphore, config)) for url in urls]

            # 所有任务成功完成
            for task in tasks:
                result = task.result()
                stats.success += 1
                yield result

        except* aiohttp.ClientError as eg:
            stats.failed += len(eg.exceptions)
            print(f"\n⚠️ 网络错误: {len(eg.exceptions)} 个")
            for exc in eg.exceptions:
                print(f"  - {exc}")

        except* TimeoutError as eg:
            stats.failed += len(eg.exceptions)
            print(f"\n⚠️ 超时错误: {len(eg.exceptions)} 个")

        except* Exception as eg:
            stats.failed += len(eg.exceptions)
            print(f"\n⚠️ 其他错误: {len(eg.exceptions)} 个")
            for exc in eg.exceptions:
                print(f"  - {type(exc).__name__}: {exc}")

        finally:
            # 打印统计信息
            print("\n" + "=" * 60)
            print("爬取统计")
            print("=" * 60)
            print(f"总数: {stats.total}")
            print(f"成功: {stats.success}")
            print(f"失败: {stats.failed}")
            print(f"成功率: {stats.success_rate:.2f}%")
            print(f"吞吐量: {stats.throughput:.2f} pages/s")
            print(f"耗时: {stats.elapsed_seconds:.2f}s")
            print("=" * 60)


# ============================================================================
# 数据库操作
# ============================================================================


@asynccontextmanager
async def db_connection(config: CrawlerConfig) -> AsyncGenerator[asyncpg.Connection]:
    """数据库连接上下文管理器"""
    conn = await asyncpg.connect(config.db_url)

    try:
        yield conn
    finally:
        await conn.close()


async def init_database(config: CrawlerConfig) -> None:
    """初始化数据库表"""
    async with db_connection(config) as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                title TEXT,
                content TEXT,
                status INTEGER,
                crawled_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        print("✓ 数据库表已初始化")


async def save_to_database(
    results: list[PageResult],
    config: CrawlerConfig,
) -> None:
    """批量保存到数据库"""
    if not results:
        return

    async with db_connection(config) as conn:
        # 使用事务
        async with conn.transaction():
            # 批量插入（使用 ON CONFLICT 避免重复）
            await conn.executemany(
                """
                INSERT INTO pages (url, title, content, status, crawled_at)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (url) DO UPDATE SET
                    title = EXCLUDED.title,
                    content = EXCLUDED.content,
                    status = EXCLUDED.status,
                    crawled_at = EXCLUDED.crawled_at
                """,
                [
                    (
                        result["url"],
                        result["title"],
                        result["content"],
                        result["status"],
                        result["crawled_at"],
                    )
                    for result in results
                ],
            )


# ============================================================================
# 优雅关闭
# ============================================================================


class GracefulShutdown:
    """优雅关闭处理器"""

    def __init__(self) -> None:
        self.shutdown_event = asyncio.Event()
        self.original_handlers: dict[signal.Signals, object] = {}

    def setup(self) -> None:
        """设置信号处理"""
        for sig in (signal.SIGTERM, signal.SIGINT):
            self.original_handlers[sig] = signal.signal(sig, self._signal_handler)

    def _signal_handler(self, signum: int, frame: object) -> None:
        """信号处理函数"""
        print(f"\n收到信号 {signum}，准备关闭...")
        self.shutdown_event.set()

    def restore(self) -> None:
        """恢复原始信号处理"""
        for sig, handler in self.original_handlers.items():
            signal.signal(sig, handler)

    async def wait(self) -> None:
        """等待关闭信号"""
        await self.shutdown_event.wait()


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
        batch_size=10,
    )

    # 设置优雅关闭
    shutdown = GracefulShutdown()
    shutdown.setup()

    # 测试 URL 列表
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/200",
        "https://httpbin.org/html",
        "https://example.com",
        "https://www.python.org",
    ] * 4  # 20 个 URL

    print("生产级异步爬虫流式数据管道")
    print("=" * 60)
    print(f"URL 数量: {len(urls)}")
    print(f"最大并发: {config.max_concurrent}")
    print(f"超时: {config.timeout}s")
    print(f"重试次数: {config.retry_attempts}")
    print(f"批量大小: {config.batch_size}")
    print("=" * 60)

    # 初始化数据库（可选）
    try:
        await init_database(config)
    except Exception as e:
        print(f"⚠️ 数据库初始化失败: {e}")
        print("继续运行（不保存到数据库）...\n")
        config = replace(config, db_url="")

    # 收集结果
    results: list[PageResult] = []
    batch: list[PageResult] = []

    try:
        async for result in crawler_pipeline(urls, config):
            results.append(result)
            batch.append(result)

            print(f"✓ [{len(results)}/{len(urls)}] {result['title'][:50]} ({result['status']})")

            # 批量保存
            if len(batch) >= config.batch_size and config.db_url:
                try:
                    await save_to_database(batch, config)
                    print(f"  → 批量保存 {len(batch)} 条记录")
                    batch = []
                except Exception as e:
                    print(f"  ✗ 保存失败: {e}")

            # 检查关闭信号
            if shutdown.shutdown_event.is_set():
                print("\n⚠️ 收到关闭信号，停止爬取...")
                break

    except KeyboardInterrupt:
        print("\n\n⚠️ 收到中断信号，正在优雅关闭...")

    finally:
        # 保存剩余结果
        if batch and config.db_url:
            print(f"\n保存剩余 {len(batch)} 条记录...")
            try:
                await save_to_database(batch, config)
                print("✓ 保存成功")
            except Exception as e:
                print(f"✗ 保存失败: {e}")

        # 恢复信号处理
        shutdown.restore()

        # 最终统计
        print(f"\n最终收集 {len(results)} 条结果")


def require_network_deps() -> None:
    """检查网络依赖是否可用，不可用则跳过测试。

    使用方式：
        pytest.importorskip("aiohttp")  # 先检查 pytest 可用
        require_network_deps()          # 再检查模块内依赖
    """
    if not _NETWORK_DEPS_AVAILABLE:
        pytest.skip("需要 aiohttp 和 asyncpg 依赖（uv add aiohttp asyncpg）", allow_module_level=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已退出")
        sys.exit(0)
