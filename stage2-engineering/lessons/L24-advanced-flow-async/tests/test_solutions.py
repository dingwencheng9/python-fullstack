"""
测试套件：验证所有练习题答案

运行方式:
    pytest tests/test_solutions.py -v
    pytest tests/test_solutions.py::test_exercise_01 -v
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

# ============================================================================
# 测试练习 1
# ============================================================================


@pytest.mark.asyncio
async def test_exercise_01(solutions) -> None:
    """测试练习 1: 异步文件读取"""
    # 如果 aiofiles 未安装，跳过测试（教学可选依赖）
    pytest.importorskip("aiofiles", reason="aiofiles 是教学可选依赖")

    # 从 fixture 获取答案模块
    read_lines_async = solutions.solution_01_async_contextvar.read_lines_async

    # 创建测试文件
    test_file = Path("/tmp/test_exercise_01.txt")
    test_content = "Line 1\nLine 2\n  Line 3  \nLine 4\n"
    test_file.write_text(test_content, encoding="utf-8")

    try:
        # 读取所有行
        lines: list[str] = []
        async for line in read_lines_async(str(test_file)):
            lines.append(line)

        # 验证结果
        assert lines == ["Line 1", "Line 2", "Line 3", "Line 4"]

    finally:
        # 清理
        test_file.unlink(missing_ok=True)


# ============================================================================
# 测试综合项目
# ============================================================================


@pytest.mark.asyncio
async def test_crawler_pipeline(solutions) -> None:
    """测试爬虫管道基本功能（使用本地假会话隔离网络）。"""
    # 从 solutions fixture 获取 crawler_pipeline 模块
    # 注意：使用 solution_03_crawler_pipeline（完整实现），而非 crawler_pipeline（教学存根）
    if not hasattr(solutions, "solution_03_crawler_pipeline"):
        pytest.skip("solution_03_crawler_pipeline 模块未找到（项目可选）")

    crawler_pipeline = solutions.solution_03_crawler_pipeline
    CrawlerConfig = crawler_pipeline.CrawlerConfig  # noqa: N806
    crawl_page = crawler_pipeline.crawl_page

    class FakeResponse:
        """模拟 aiohttp 响应上下文。"""

        status = 200

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb) -> None:
            return None

        async def text(self) -> str:
            return "<html><title>本地测试页面</title><body>content</body></html>"

    class FakeSession:
        """模拟 aiohttp ClientSession.get。"""

        def get(self, url: str) -> FakeResponse:
            assert url == "https://example.test/html"
            return FakeResponse()

    config = CrawlerConfig(max_concurrent=2, timeout=10.0, retry_attempts=1)
    semaphore = asyncio.Semaphore(1)

    result = await crawl_page(
        "https://example.test/html",
        FakeSession(),
        semaphore,
        config,
    )

    assert result["status"] == 200
    assert result["url"] == "https://example.test/html"
    assert result["title"] == "本地测试页面"
    assert len(result["content"]) > 0


# ============================================================================
# 性能测试
# ============================================================================


@pytest.mark.asyncio
async def test_async_performance() -> None:
    """测试异步性能优势"""
    import time

    # 同步版本
    def sync_tasks(n: int) -> list[int]:
        results = []
        for i in range(n):
            # 模拟 I/O
            import time

            time.sleep(0.01)
            results.append(i)
        return results

    # 异步版本
    async def async_task(i: int) -> int:
        await asyncio.sleep(0.01)
        return i

    async def async_tasks(n: int) -> list[int]:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(async_task(i)) for i in range(n)]
        return [t.result() for t in tasks]

    # 测试同步版本
    start = time.time()
    sync_results = sync_tasks(10)
    sync_time = time.time() - start

    # 测试异步版本
    start = time.time()
    async_results = await async_tasks(10)
    async_time = time.time() - start

    print(f"\n同步耗时: {sync_time:.2f}s")
    print(f"异步耗时: {async_time:.2f}s")
    print(f"性能提升: {sync_time / async_time:.2f}x")

    # 验证结果一致
    assert sync_results == async_results

    # 异步应该更快（至少 2x）
    assert async_time < sync_time / 2


# ============================================================================
# 测试练习 2
# ============================================================================


@pytest.mark.asyncio
async def test_exercise_02(solutions) -> None:
    """测试练习 2: 异步上下文管理器与资源池"""
    # 从 fixture 获取答案模块
    solution_02 = solutions.solution_02_semaphore
    ConnectionPool = solution_02.ConnectionPool  # noqa: N806
    GenericPool = solution_02.GenericPool  # noqa: N806
    create_pool = solution_02.create_pool
    get_connection = solution_02.get_connection
    managed_resource = solution_02.managed_resource

    # 测试连接池上下文管理器
    pool = ConnectionPool(size=2)
    await pool.initialize()

    async with get_connection(pool) as conn:
        assert conn.conn_id in [0, 1]
        assert conn.in_use is True
        result = await conn.execute("SELECT 1")
        assert len(result) == 1

    await pool.close()

    # 测试 PEP 695 泛型函数
    string_pool = create_pool(["A", "B", "C"])
    assert string_pool == ["A", "B", "C"]

    int_pool = create_pool([1, 2, 3])
    assert int_pool == [1, 2, 3]

    # 测试泛型类
    generic_pool: GenericPool[int] = GenericPool([10, 20, 30])
    await generic_pool.initialize()

    async with managed_resource(generic_pool) as item:
        assert item in [10, 20, 30]


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        (["A"], ["A"]),
        ([1, 2, 3], [1, 2, 3]),
        ([], []),
    ],
)
def test_create_pool_parametrized(solutions, items: list[object], expected: list[object]) -> None:
    """参数化验证泛型资源池工厂保留输入内容。"""
    create_pool = solutions.solution_02_semaphore.create_pool

    assert create_pool(items) == expected


@pytest.mark.asyncio
async def test_connection_pool_acquire_raises_timeout_when_empty(solutions) -> None:
    """异常路径：容量为 0 的连接池获取资源会在外层超时。"""
    ConnectionPool = solutions.solution_02_semaphore.ConnectionPool  # noqa: N806

    pool = ConnectionPool(size=0)
    await pool.initialize()

    with pytest.raises(TimeoutError):
        await asyncio.wait_for(pool.acquire(), timeout=0.01)


@pytest.mark.asyncio
async def test_generic_pool_boundary_single_item_released(solutions) -> None:
    """边界场景：单元素泛型池退出上下文后资源可再次获取。"""
    GenericPool = solutions.solution_02_semaphore.GenericPool  # noqa: N806
    managed_resource = solutions.solution_02_semaphore.managed_resource

    pool: GenericPool[str] = GenericPool(["only"])
    await pool.initialize()

    async with managed_resource(pool) as item:
        assert item == "only"

    assert await pool.acquire() == "only"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
