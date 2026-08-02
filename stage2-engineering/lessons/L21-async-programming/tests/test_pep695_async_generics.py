"""

from __future__ import annotations

测试 L19 PEP 695 泛型异步编程特性

验证泛型异步函数、生成器、上下文管理器和对象池
"""

import asyncio
import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # AsyncPool 在动态加载的模块中定义，用于类型注解
    AsyncPool = None  # type: ignore[assignment,misc]

import pytest


@pytest.fixture
def ex():
    """加载 ex09_pep695_async_generics 模块"""
    file_path = (
        Path(__file__).parent.parent / "examples" / "ex09_pep695_async_generics.py"
    )
    spec = importlib.util.spec_from_file_location(
        "ex09_pep695_async_generics", file_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestGenericAsyncFunctions:
    """测试泛型异步函数"""

    @pytest.mark.asyncio
    async def test_fetch_data_with_dict_parser(self, ex):
        """测试泛型 fetch_data - dict 解析器"""

        def parse_dict(data: dict[str, Any]) -> dict[str, str | int]:
            return {"id": data["id"], "name": data["name"]}

        result = await ex.fetch_data("test_url", parse_dict)

        assert isinstance(result, dict)
        assert "id" in result
        assert "name" in result
        assert result["id"] == 1

    @pytest.mark.asyncio
    async def test_fetch_data_with_string_parser(self, ex):
        """测试泛型 fetch_data - str 解析器"""

        def parse_string(data: dict[str, Any]) -> str:
            return f"User: {data['name']}"

        result = await ex.fetch_data("test_url", parse_string)

        assert isinstance(result, str)
        assert "User:" in result
        assert "Alice" in result

    @pytest.mark.asyncio
    async def test_fetch_multiple(self, ex):
        """测试并发获取多个资源"""

        def parser(data: dict[str, Any]) -> int:
            return data["id"]

        urls = ["url1", "url2", "url3"]
        results = await ex.fetch_multiple(urls, parser)

        assert len(results) == 3
        assert all(isinstance(r, int) for r in results)
        assert all(r == 1 for r in results)


class TestGenericAsyncGenerators:
    """测试泛型异步生成器"""

    @pytest.mark.asyncio
    async def test_async_range_basic(self, ex):
        """测试异步范围生成器 - 基本功能"""
        results = []
        async for value in ex.async_range(1, 5, lambda x: x * 2):
            results.append(value)

        assert results == [2, 4, 6, 8]

    @pytest.mark.asyncio
    async def test_async_range_square(self, ex):
        """测试异步范围生成器 - 平方转换"""
        results = []
        async for square in ex.async_range(1, 4, lambda x: x**2):
            results.append(square)

        assert results == [1, 4, 9]

    @pytest.mark.asyncio
    async def test_async_range_string_transform(self, ex):
        """测试异步范围生成器 - 字符串转换"""
        results = []
        async for s in ex.async_range(0, 3, lambda x: f"item_{x}"):
            results.append(s)

        assert results == ["item_0", "item_1", "item_2"]

    @pytest.mark.asyncio
    async def test_paginate_basic(self, ex):
        """测试分页生成器 - 基本功能"""
        items = list(range(1, 11))
        pages = []

        async for page in ex.paginate(items, 3):
            pages.append(page)

        assert len(pages) == 4
        assert pages[0] == [1, 2, 3]
        assert pages[1] == [4, 5, 6]
        assert pages[2] == [7, 8, 9]
        assert pages[3] == [10]

    @pytest.mark.asyncio
    async def test_paginate_exact_division(self, ex):
        """测试分页生成器 - 整除情况"""
        items = list(range(1, 9))
        pages = []

        async for page in ex.paginate(items, 4):
            pages.append(page)

        assert len(pages) == 2
        assert pages[0] == [1, 2, 3, 4]
        assert pages[1] == [5, 6, 7, 8]

    @pytest.mark.asyncio
    async def test_paginate_empty_list(self, ex):
        """测试分页生成器 - 空列表"""
        pages = []
        async for page in ex.paginate([], 5):
            pages.append(page)

        assert len(pages) == 0


class TestGenericContextManagers:
    """测试泛型异步上下文管理器"""

    @pytest.mark.asyncio
    async def test_async_resource_basic(self, ex):
        """测试泛型资源管理器 - 基本功能"""
        resource_value = 42

        async with ex.async_resource(resource_value) as res:
            assert res == 42

    @pytest.mark.asyncio
    async def test_async_resource_with_setup_cleanup(self, ex):
        """测试泛型资源管理器 - 带初始化和清理"""
        setup_called = []
        cleanup_called = []

        class TestResource:
            def __init__(self, name: str):
                self.name = name

        def setup(res: TestResource) -> None:
            setup_called.append(res.name)

        def cleanup(res: TestResource) -> None:
            cleanup_called.append(res.name)

        test_res = TestResource("test")

        async with ex.async_resource(test_res, setup, cleanup) as res:
            assert res.name == "test"

        assert "test" in setup_called
        assert "test" in cleanup_called

    @pytest.mark.asyncio
    async def test_async_resource_exception_cleanup(self, ex):
        """测试资源管理器在异常时仍执行清理"""
        cleanup_called = []

        def cleanup(res: str) -> None:
            cleanup_called.append(res)

        with pytest.raises(ValueError, match="Test error"):
            async with ex.async_resource("resource", cleanup=cleanup):
                raise ValueError("Test error")

        assert "resource" in cleanup_called


class TestGenericAsyncPool:
    """测试泛型异步对象池"""

    @pytest.mark.asyncio
    async def test_pool_acquire_release(self, ex):
        """测试对象池的获取和释放"""
        counter = {"value": 0}

        def factory() -> int:
            counter["value"] += 1
            return counter["value"]

        pool: AsyncPool[int] = ex.AsyncPool(factory, size=3)

        # 获取对象
        obj1 = await pool.acquire()
        obj2 = await pool.acquire()

        assert obj1 in {1, 2, 3}
        assert obj2 in {1, 2, 3}
        assert obj1 != obj2

        # 释放对象
        await pool.release(obj1)
        await pool.release(obj2)

    @pytest.mark.asyncio
    async def test_pool_context_manager(self, ex):
        """测试对象池的上下文管理器用法"""
        pool: AsyncPool[str] = ex.AsyncPool(lambda: "connection", size=2)

        async with pool.get() as conn:
            assert conn == "connection"

    @pytest.mark.asyncio
    async def test_pool_concurrent_access(self, ex):
        """测试对象池的并发访问"""
        counter = {"value": 0}

        def factory() -> int:
            counter["value"] += 1
            return counter["value"]

        pool: AsyncPool[int] = ex.AsyncPool(factory, size=3)
        results = []

        async def worker(task_id: int) -> None:
            async with pool.get() as obj:
                results.append((task_id, obj))
                await asyncio.sleep(0.01)

        # 启动 5 个并发任务（池大小为 3）
        tasks = [worker(i) for i in range(5)]
        await asyncio.gather(*tasks)

        # 验证所有任务都完成
        assert len(results) == 5

        # 验证使用的对象都在池中
        used_objs = {obj for _, obj in results}
        assert used_objs.issubset({1, 2, 3})


class TestTypeAliasesAndSafeFetch:
    """测试类型别名和安全获取"""

    @pytest.mark.asyncio
    async def test_safe_fetch_success(self, ex):
        """测试安全获取 - 成功情况"""
        result = await ex.safe_fetch(lambda: 42)
        assert result == 42
        assert not isinstance(result, Exception)

    @pytest.mark.asyncio
    async def test_safe_fetch_exception(self, ex):
        """测试安全获取 - 异常情况"""

        def failing_fetcher() -> int:
            raise ValueError("Test error")

        result = await ex.safe_fetch(failing_fetcher)
        assert isinstance(result, Exception)
        assert isinstance(result, ValueError)
        assert str(result) == "Test error"

    @pytest.mark.asyncio
    async def test_safe_fetch_different_types(self, ex):
        """测试安全获取 - 不同返回类型"""
        # 字符串类型
        str_result = await ex.safe_fetch(lambda: "success")
        assert str_result == "success"

        # 字典类型
        dict_result = await ex.safe_fetch(lambda: {"key": "value"})
        assert dict_result == {"key": "value"}

        # 列表类型
        list_result = await ex.safe_fetch(lambda: [1, 2, 3])
        assert list_result == [1, 2, 3]


class TestIntegration:
    """集成测试"""

    @pytest.mark.asyncio
    async def test_pipeline_fetch_and_paginate(self, ex):
        """测试完整流程：获取数据 -> 分页处理"""

        # 模拟获取数据
        def parser(data: dict[str, Any]) -> list[int]:
            return list(range(1, 11))

        items = await ex.fetch_data("url", parser)

        # 分页处理
        pages = []
        async for page in ex.paginate(items, 3):
            pages.append(page)

        assert len(pages) == 4
        assert sum(len(p) for p in pages) == 10

    @pytest.mark.asyncio
    async def test_pool_with_resource_manager(self, ex):
        """测试对象池与资源管理器组合"""

        class Connection:
            def __init__(self, conn_id: int):
                self.id = conn_id
                self.closed = False

            def close(self) -> None:
                self.closed = True

        pool: AsyncPool[Connection] = ex.AsyncPool(lambda: Connection(1), size=2)

        async with pool.get() as conn:
            assert not conn.closed
            async with ex.async_resource(
                conn, cleanup=lambda c: c.close()
            ) as managed_conn:
                assert managed_conn.id == 1
                assert not managed_conn.closed

            # 资源管理器的清理已执行
            assert conn.closed


class TestThreadSafety:
    """测试 Free-threading 线程安全考量"""

    @pytest.mark.asyncio
    async def test_pool_lock_protection(self, ex):
        """验证对象池使用锁保护（Free-threading 安全）"""
        pool: AsyncPool[int] = ex.AsyncPool(lambda: 1, size=1)

        # 验证池有锁属性
        assert hasattr(pool, "_lock")
        assert pool._lock is not None

    @pytest.mark.asyncio
    async def test_concurrent_pool_access_safety(self, ex):
        """测试并发访问对象池的安全性"""
        counter = {"value": 0}

        def factory() -> int:
            # 返回可哈希的整数而不是字典
            counter["value"] += 1
            return counter["value"]

        pool: AsyncPool[int] = ex.AsyncPool(factory, size=2)
        access_log = []

        async def concurrent_worker(worker_id: int) -> None:
            for _ in range(3):
                async with pool.get() as obj:
                    access_log.append((worker_id, obj))
                    await asyncio.sleep(0.001)

        # 10 个 worker 并发访问
        tasks = [concurrent_worker(i) for i in range(10)]
        await asyncio.gather(*tasks)

        # 验证：所有访问都记录了
        assert len(access_log) == 30

        # 验证：使用的对象 ID 只有 1 和 2（池大小为 2）
        used_ids = {obj_id for _, obj_id in access_log}
        assert used_ids == {1, 2}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
