"""测试套件：爬虫管道项目

覆盖：
- examples/crawler_pipeline.py（教学存根）
- solutions/solution_03_crawler_pipeline.py（参考答案）

注意：测试使用 solutions fixture 导入参考答案，而非直接导入 examples。

运行方式:
    pytest tests/test_crawler.py -v
"""

from __future__ import annotations

import asyncio
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# 条件跳过：检查 solution 模块的网络依赖是否可用
# 如果 aiohttp/asyncpg 不可用，跳过整个测试文件
def _get_crawler_module():
    """从 sys.modules 获取爬虫模块，处理不同命名方式"""
    # 尝试多种可能的模块名
    for name in ["solution_03_crawler_pipeline", "_test_L22_async_flow.solution_03_crawler_pipeline"]:
        mod = sys.modules.get(name)
        if mod is not None:
            return mod
    return None


_crawler_module = _get_crawler_module()
_NETWORK_DEPS_AVAILABLE = getattr(_crawler_module, "_NETWORK_DEPS_AVAILABLE", False) if _crawler_module else False

if not _NETWORK_DEPS_AVAILABLE:
    pytest.skip("需要 aiohttp 和 asyncpg 依赖（uv add aiohttp asyncpg）", allow_module_level=True)

# 为方便测试，创建简化的访问接口
solution_03_crawler_pipeline = _crawler_module


# ============================================================================
# 测试数据结构
# ============================================================================


def test_crawler_config(solutions) -> None:
    """测试爬虫配置"""
    CrawlerConfig = solution_03_crawler_pipeline.CrawlerConfig

    config = CrawlerConfig(
        max_concurrent=10,
        timeout=60.0,
        retry_attempts=5,
    )

    assert config.max_concurrent == 10
    assert config.timeout == 60.0
    assert config.retry_attempts == 5
    assert config.backoff_factor == 2.0  # 默认值


def test_crawler_stats(solutions) -> None:
    """测试爬虫统计"""
    crawler_pipeline = solution_03_crawler_pipeline
    CrawlerStats = crawler_pipeline.CrawlerStats

    stats = CrawlerStats(total=100, success=80, failed=20)

    assert stats.total == 100
    assert stats.success == 80
    assert stats.failed == 20
    assert stats.success_rate == 80.0
    assert stats.throughput > 0


def test_page_result_type(solutions) -> None:
    """测试 PageResult 类型"""
    crawler_pipeline = solution_03_crawler_pipeline
    PageResult = crawler_pipeline.PageResult

    result: PageResult = {
        "url": "https://example.com",
        "title": "Example Domain",
        "content": "<html>...</html>",
        "status": 200,
        "crawled_at": "2026-06-08T10:00:00",
    }

    assert result["url"] == "https://example.com"
    assert result["status"] == 200


# ============================================================================
# 测试 HTTP 会话管理
# ============================================================================


@pytest.mark.asyncio
async def test_http_session(solutions) -> None:
    """测试 HTTP 会话上下文管理器"""
    crawler_pipeline = solution_03_crawler_pipeline
    CrawlerConfig = crawler_pipeline.CrawlerConfig
    http_session = crawler_pipeline.http_session

    config = CrawlerConfig(timeout=10.0, max_concurrent=5)

    async with http_session(config) as session:
        assert session is not None
        assert not session.closed


# ============================================================================
# 测试页面爬取（使用 Mock）
# ============================================================================


@pytest.mark.asyncio
async def test_crawl_page_success(solutions) -> None:
    """测试成功爬取页面"""
    crawler_pipeline = solution_03_crawler_pipeline
    CrawlerConfig = crawler_pipeline.CrawlerConfig
    crawl_page = crawler_pipeline.crawl_page

    config = CrawlerConfig(retry_attempts=3)
    semaphore = asyncio.Semaphore(1)

    # Mock HTTP 响应
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(return_value="<html><head><title>Test Page</title></head></html>")

    mock_session = AsyncMock()
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)

    result = await crawl_page(
        "https://example.com",
        mock_session,
        semaphore,
        config,
    )

    assert result["url"] == "https://example.com"
    assert result["status"] == 200
    assert result["title"] == "Test Page"
    assert len(result["content"]) > 0


@pytest.mark.asyncio
async def test_crawl_page_retry(solutions) -> None:
    """测试爬取失败后重试"""
    import aiohttp

    crawler_pipeline = solution_03_crawler_pipeline
    CrawlerConfig = crawler_pipeline.CrawlerConfig
    crawl_page = crawler_pipeline.crawl_page

    config = CrawlerConfig(retry_attempts=2, backoff_factor=0.1)
    semaphore = asyncio.Semaphore(1)

    # Mock: 第一次失败，第二次成功
    call_count = 0

    async def mock_get_side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1

        if call_count == 1:
            raise aiohttp.ClientError("Network error")

        # 第二次成功
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="<html><head><title>Success</title></head></html>")
        return mock_response

    mock_session = AsyncMock()
    mock_cm = AsyncMock()
    mock_cm.__aenter__ = AsyncMock(side_effect=mock_get_side_effect)
    mock_cm.__aexit__ = AsyncMock(return_value=None)
    mock_session.get = MagicMock(return_value=mock_cm)

    result = await crawl_page(
        "https://example.com",
        mock_session,
        semaphore,
        config,
    )

    assert result["status"] == 200
    assert call_count == 2  # 确认重试了


@pytest.mark.asyncio
async def test_crawl_page_max_retries_exceeded(solutions) -> None:
    """测试超过最大重试次数"""
    import aiohttp

    crawler_pipeline = solution_03_crawler_pipeline
    CrawlerConfig = crawler_pipeline.CrawlerConfig
    crawl_page = crawler_pipeline.crawl_page

    config = CrawlerConfig(retry_attempts=2, backoff_factor=0.1)
    semaphore = asyncio.Semaphore(1)

    # Mock: 始终失败
    mock_session = AsyncMock()
    mock_cm = AsyncMock()
    mock_cm.__aenter__ = AsyncMock(side_effect=aiohttp.ClientError("Network error"))
    mock_cm.__aexit__ = AsyncMock(return_value=None)
    mock_session.get = MagicMock(return_value=mock_cm)

    with pytest.raises(aiohttp.ClientError):
        await crawl_page(
            "https://example.com",
            mock_session,
            semaphore,
            config,
        )


# ============================================================================
# 测试爬虫管道
# ============================================================================


@pytest.mark.asyncio
async def test_crawler_pipeline_basic(solutions) -> None:
    """测试爬虫管道基本功能"""
    crawler_pipeline = solution_03_crawler_pipeline
    CrawlerConfig = crawler_pipeline.CrawlerConfig
    crawler_pipeline_func = crawler_pipeline.crawler_pipeline

    config = CrawlerConfig(
        max_concurrent=2,
        timeout=10.0,
        retry_attempts=1,
    )

    # 使用真实的 httpbin.org 进行测试（或 Mock）
    urls = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/html",
    ]

    results: list = []

    # 使用 Mock 避免真实网络请求
    with patch.object(crawler_pipeline, "http_session") as mock_session_ctx:
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="<html><head><title>Mock Page</title></head></html>")

        mock_cm = AsyncMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        mock_session.get = MagicMock(return_value=mock_cm)
        mock_session.close = AsyncMock()

        mock_session_ctx.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.return_value.__aexit__ = AsyncMock(return_value=None)

        async for result in crawler_pipeline_func(urls, config):
            results.append(result)

    assert len(results) == 2
    for result in results:
        assert result["status"] == 200
        assert "url" in result
        assert "title" in result


# ============================================================================
# 测试数据库操作（使用 Mock）
# ============================================================================


@pytest.mark.asyncio
async def test_db_connection(solutions) -> None:
    """测试数据库连接（使用 Mock）"""
    crawler_pipeline = solution_03_crawler_pipeline
    CrawlerConfig = crawler_pipeline.CrawlerConfig
    db_connection = crawler_pipeline.db_connection

    config = CrawlerConfig(db_url="postgresql://localhost/test")

    # Mock asyncpg.connect
    with patch.object(crawler_pipeline, "asyncpg") as mock_asyncpg:
        mock_conn = AsyncMock()
        mock_conn.close = AsyncMock()
        # 正确设置 connect 返回协程
        mock_asyncpg.connect = AsyncMock(return_value=mock_conn)

        async with db_connection(config) as conn:
            assert conn is not None


@pytest.mark.asyncio
async def test_save_to_database(solutions) -> None:
    """测试批量保存到数据库（使用 Mock）"""
    crawler_pipeline = solution_03_crawler_pipeline
    CrawlerConfig = crawler_pipeline.CrawlerConfig
    PageResult = crawler_pipeline.PageResult
    save_to_database = crawler_pipeline.save_to_database

    config = CrawlerConfig(db_url="postgresql://localhost/test")

    results: list[PageResult] = [
        {
            "url": "https://example.com/1",
            "title": "Page 1",
            "content": "Content 1",
            "status": 200,
            "crawled_at": "2026-06-08T10:00:00",
        },
        {
            "url": "https://example.com/2",
            "title": "Page 2",
            "content": "Content 2",
            "status": 200,
            "crawled_at": "2026-06-08T10:00:01",
        },
    ]

    # Mock 数据库连接
    with patch.object(crawler_pipeline, "db_connection") as mock_db_ctx:
        mock_conn = AsyncMock()
        mock_transaction = AsyncMock()
        mock_transaction.__aenter__ = AsyncMock()
        mock_transaction.__aexit__ = AsyncMock(return_value=None)
        mock_conn.transaction = MagicMock(return_value=mock_transaction)
        mock_conn.executemany = AsyncMock()

        mock_db_ctx.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_db_ctx.return_value.__aexit__ = AsyncMock(return_value=None)

        await save_to_database(results, config)

        # 验证 executemany 被调用
        mock_conn.executemany.assert_called_once()


# ============================================================================
# 测试优雅关闭
# ============================================================================


def test_graceful_shutdown_setup(solutions) -> None:
    """测试优雅关闭设置"""
    crawler_pipeline = solution_03_crawler_pipeline
    GracefulShutdown = crawler_pipeline.GracefulShutdown

    shutdown = GracefulShutdown()
    shutdown.setup()

    assert not shutdown.shutdown_event.is_set()

    # 恢复信号处理
    shutdown.restore()


@pytest.mark.asyncio
async def test_graceful_shutdown_wait(solutions) -> None:
    """测试优雅关闭等待"""
    crawler_pipeline = solution_03_crawler_pipeline
    GracefulShutdown = crawler_pipeline.GracefulShutdown

    shutdown = GracefulShutdown()

    # 在后台设置事件
    async def set_event():
        await asyncio.sleep(0.1)
        shutdown.shutdown_event.set()

    asyncio.create_task(set_event())

    # 等待事件
    await shutdown.wait()

    assert shutdown.shutdown_event.is_set()


# ============================================================================
# 集成测试
# ============================================================================


@pytest.mark.asyncio
async def test_full_pipeline_integration(solutions) -> None:
    """测试完整管道集成（使用 Mock）"""
    crawler_pipeline = solution_03_crawler_pipeline
    CrawlerConfig = crawler_pipeline.CrawlerConfig
    crawler_pipeline_func = crawler_pipeline.crawler_pipeline

    config = CrawlerConfig(
        max_concurrent=3,
        timeout=10.0,
        retry_attempts=2,
    )

    urls = [f"https://example.com/page{i}" for i in range(5)]

    # Mock HTTP 会话
    with patch.object(crawler_pipeline, "http_session") as mock_session_ctx:
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="<html><head><title>Test</title></head></html>")

        mock_cm = AsyncMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        mock_session.get = MagicMock(return_value=mock_cm)
        mock_session.close = AsyncMock()

        mock_session_ctx.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.return_value.__aexit__ = AsyncMock(return_value=None)

        results: list = []
        async for result in crawler_pipeline_func(urls, config):
            results.append(result)

        assert len(results) == 5
        assert all(r["status"] == 200 for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
