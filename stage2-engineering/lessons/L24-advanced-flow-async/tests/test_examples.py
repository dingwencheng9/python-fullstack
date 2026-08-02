"""
测试套件：Examples 模块完整测试

覆盖：
- example_01_async_generators.py
- example_02_context_managers.py
- example_03_taskgroup_exceptions.py

运行方式:
    pytest tests/test_examples.py -v
"""

import asyncio
from pathlib import Path

import pytest

# 添加 examples 到路径
examples_path = Path(__file__).parent.parent / "examples"

# ============================================================================
# 测试 Example 01: 异步生成器
# ============================================================================


@pytest.mark.asyncio
async def test_sync_generator(solutions) -> None:
    """测试同步生成器"""
    example_01_async_generators = solutions.example_01_async_generators
    sync_range = example_01_async_generators.sync_range

    results: list[int] = []
    for num in sync_range(5):
        results.append(num)

    assert results == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_async_generator(solutions) -> None:
    """测试异步生成器"""
    example_01_async_generators = solutions.example_01_async_generators
    async_range = example_01_async_generators.async_range

    results: list[int] = []
    async for num in async_range(5):
        results.append(num)

    assert results == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_echo_generator(solutions) -> None:
    """测试 send 生成器"""
    example_01_async_generators = solutions.example_01_async_generators
    echo_generator = example_01_async_generators.echo_generator

    gen = echo_generator()

    # 首次调用
    first = next(gen)
    assert "Echo-0" in first
    assert "START" in first

    # 发送数据
    second = gen.send("Hello")
    assert "Echo-1" in second
    assert "Hello" in second

    third = gen.send("World")
    assert "Echo-2" in third
    assert "World" in third

    gen.close()


@pytest.mark.asyncio
async def test_async_echo(solutions) -> None:
    """测试异步 send 生成器"""
    example_01_async_generators = solutions.example_01_async_generators
    async_echo = example_01_async_generators.async_echo

    gen = async_echo()

    # 首次调用
    first = await gen.asend(None)
    assert "AsyncEcho-0" in first
    assert "START" in first

    # 发送数据
    second = await gen.asend("Task1")
    assert "AsyncEcho-1" in second
    assert "Task1" in second

    await gen.aclose()


@pytest.mark.asyncio
async def test_stream_pipeline(solutions) -> None:
    """测试流式管道"""
    example_01_async_generators = solutions.example_01_async_generators
    data_source = example_01_async_generators.data_source
    transform_stream = example_01_async_generators.transform_stream

    results: list[str] = []
    async for item in transform_stream(data_source()):
        results.append(item)

    assert len(results) == 10
    assert results[0] == "Item-000"
    assert results[9] == "Item-009"


# ============================================================================
# 测试 Example 02: 上下文管理器
# ============================================================================


@pytest.mark.asyncio
async def test_file_manager_old(solutions) -> None:
    """测试旧式文件管理器"""
    import tempfile

    example_02_context_managers = solutions.example_02_context_managers
    FileManagerOld = example_02_context_managers.FileManagerOld  # noqa: N806

    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("Test Content")
        temp_path = f.name

    try:
        # 使用旧式管理器读取
        with FileManagerOld(temp_path) as f:
            content = f.read()

        assert content == "Test Content"
    finally:
        Path(temp_path).unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_file_manager_new(solutions) -> None:
    """测试新式文件管理器"""
    import tempfile

    example_02_context_managers = solutions.example_02_context_managers
    file_manager = example_02_context_managers.file_manager

    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("Test Content")
        temp_path = f.name

    try:
        # 使用新式管理器读取
        with file_manager(temp_path) as f:
            content = f.read()

        assert content == "Test Content"
    finally:
        Path(temp_path).unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_async_resource_old(solutions) -> None:
    """测试旧式异步资源管理器"""
    example_02_context_managers = solutions.example_02_context_managers
    AsyncResourceOld = example_02_context_managers.AsyncResourceOld  # noqa: N806

    async with AsyncResourceOld("Database") as resource:
        assert resource == "Database"


@pytest.mark.asyncio
async def test_async_resource_new(solutions) -> None:
    """测试新式异步资源管理器"""
    example_02_context_managers = solutions.example_02_context_managers
    async_resource = example_02_context_managers.async_resource

    async with async_resource("Database") as resource:
        assert resource == "Database"


@pytest.mark.asyncio
async def test_db_pool(solutions) -> None:
    """测试数据库连接池"""
    example_02_context_managers = solutions.example_02_context_managers
    db_pool = example_02_context_managers.db_pool

    async with db_pool(size=2) as pool:
        assert len(pool.connections) == 2

        # 执行查询
        results = await pool.query("SELECT * FROM users")
        assert len(results) > 0
        assert "id" in results[0]


@pytest.mark.asyncio
async def test_timer(solutions) -> None:
    """测试计时器上下文"""
    import time

    example_02_context_managers = solutions.example_02_context_managers
    timer = example_02_context_managers.timer

    start = time.time()
    with timer("Test"):
        time.sleep(0.1)
    elapsed = time.time() - start

    assert elapsed >= 0.1


@pytest.mark.asyncio
async def test_transaction_success(solutions) -> None:
    """测试成功的事务"""
    example_02_context_managers = solutions.example_02_context_managers
    transaction = example_02_context_managers.transaction

    async with transaction() as tx:
        tx["operations"].append("INSERT")
        tx["operations"].append("UPDATE")

    # 事务应该成功提交（无异常）


@pytest.mark.asyncio
async def test_transaction_rollback(solutions) -> None:
    """测试失败的事务（回滚）"""
    example_02_context_managers = solutions.example_02_context_managers
    transaction = example_02_context_managers.transaction

    with pytest.raises(ValueError):
        async with transaction() as tx:
            tx["operations"].append("INSERT")
            raise ValueError("数据验证失败")


# ============================================================================
# 测试 Example 03: TaskGroup 和异常处理
# ============================================================================


@pytest.mark.asyncio
async def test_task_success(solutions) -> None:
    """测试成功的任务"""
    example_03_taskgroup_exceptions = solutions.example_03_taskgroup_exceptions
    task_success = example_03_taskgroup_exceptions.task_success

    result = await task_success(1)
    assert "Task-1" in result
    assert "成功" in result


@pytest.mark.asyncio
async def test_task_failure(solutions) -> None:
    """测试失败的任务"""
    example_03_taskgroup_exceptions = solutions.example_03_taskgroup_exceptions
    task_failure = example_03_taskgroup_exceptions.task_failure

    with pytest.raises(ValueError):
        await task_failure(2)


@pytest.mark.asyncio
async def test_gather_exception_handling(solutions) -> None:
    """测试 gather 的异常处理"""
    example_03_taskgroup_exceptions = solutions.example_03_taskgroup_exceptions
    task_failure = example_03_taskgroup_exceptions.task_failure
    task_success = example_03_taskgroup_exceptions.task_success

    # gather 只捕获第一个异常
    with pytest.raises(ValueError):
        await asyncio.gather(
            task_success(1),
            task_failure(2),
            task_failure(3),
        )


@pytest.mark.asyncio
async def test_taskgroup_exception_handling(solutions) -> None:
    """测试 TaskGroup 的异常组处理"""
    example_03_taskgroup_exceptions = solutions.example_03_taskgroup_exceptions
    task_failure = example_03_taskgroup_exceptions.task_failure
    task_success = example_03_taskgroup_exceptions.task_success

    # TaskGroup 捕获所有异常
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task_success(1))
            tg.create_task(task_failure(2))
            tg.create_task(task_failure(3))
    except* ValueError as eg:
        # 应该捕获 2 个 ValueError
        assert len(eg.exceptions) == 2


@pytest.mark.asyncio
async def test_risky_task(solutions) -> None:
    """测试有风险的任务"""
    example_03_taskgroup_exceptions = solutions.example_03_taskgroup_exceptions
    risky_task = example_03_taskgroup_exceptions.risky_task

    # task_id % 3 == 0 -> ValueError
    with pytest.raises(ValueError):
        await risky_task(3)

    # task_id % 5 == 0 -> TypeError
    with pytest.raises(TypeError):
        await risky_task(5)

    # task_id % 7 == 0 -> RuntimeError
    with pytest.raises(RuntimeError):
        await risky_task(7)

    # 其他情况成功
    result = await risky_task(1)
    assert "Task-1" in result
    assert "成功" in result


@pytest.mark.asyncio
async def test_fetch_url_with_semaphore(solutions) -> None:
    """测试限流的 URL 请求"""
    example_03_taskgroup_exceptions = solutions.example_03_taskgroup_exceptions
    fetch_url = example_03_taskgroup_exceptions.fetch_url

    semaphore = asyncio.Semaphore(2)
    result = await fetch_url("https://example.com", semaphore)

    assert result["url"] == "https://example.com"
    assert result["status"] == 200


@pytest.mark.asyncio
async def test_process_item(solutions) -> None:
    """测试单项处理"""
    example_03_taskgroup_exceptions = solutions.example_03_taskgroup_exceptions
    process_item = example_03_taskgroup_exceptions.process_item

    # 正常项
    result = await process_item(5)
    assert result == 10

    # item % 10 == 0 会失败
    with pytest.raises(ValueError):
        await process_item(10)


@pytest.mark.asyncio
async def test_batch_pipeline(solutions) -> None:
    """测试批量处理管道"""
    example_03_taskgroup_exceptions = solutions.example_03_taskgroup_exceptions
    batch_pipeline = example_03_taskgroup_exceptions.batch_pipeline

    items = list(range(1, 16))  # 1-15
    total_results = 0

    async for batch_results in batch_pipeline(items, batch_size=5):
        total_results += len(batch_results)

    # batch1: 1-5 (5个成功)
    # batch2: 6-10 (10失败，剩4个成功) = 4个
    # batch3: 11-15 (5个失败) = 不对...让我看看实际逻辑
    # 实际上 TaskGroup 遇到异常会导致整个批次失败
    # batch1: 1-5 (5个成功)
    # batch2: 6-10 (有10，整批失败，0个)
    # batch3: 11-15 (5个成功)
    # 总共: 5 + 0 + 5 = 10
    assert total_results == 10


# ============================================================================
# 性能测试
# ============================================================================


@pytest.mark.asyncio
async def test_async_vs_sync_performance(solutions) -> None:
    """测试异步 vs 同步性能差异"""
    import time

    # 同步版本（顺序执行）
    def sync_tasks(n: int) -> list[int]:
        results = []
        for i in range(n):
            time.sleep(0.01)
            results.append(i)
        return results

    # 异步版本（并发执行）
    async def async_task(i: int) -> int:
        await asyncio.sleep(0.01)
        return i

    async def async_tasks(n: int) -> list[int]:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(async_task(i)) for i in range(n)]
        return [t.result() for t in tasks]

    # 测试同步
    start = time.time()
    sync_results = sync_tasks(10)
    sync_time = time.time() - start

    # 测试异步
    start = time.time()
    async_results = await async_tasks(10)
    async_time = time.time() - start

    # 验证结果一致
    assert sync_results == async_results

    # 异步应该更快（至少 2x）
    assert async_time < sync_time / 2

    print(f"\n同步耗时: {sync_time:.2f}s")
    print(f"异步耗时: {async_time:.2f}s")
    print(f"性能提升: {sync_time / async_time:.2f}x")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
