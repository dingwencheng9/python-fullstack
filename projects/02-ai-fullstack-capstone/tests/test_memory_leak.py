"""内存泄露专项测试

from __future__ import annotations

验证 LRU 缓存和资源释放机制的正确性。
"""

import pytest

from app.routes.documents import LRUCache
from app.services.rag import RAGService


class TestLRUCacheEviction:
    """测试 LRU 缓存自动驱逐机制"""

    def test_basic_eviction(self):
        """测试 LRU 缓存自动驱逐最久未使用的项"""
        cache = LRUCache(maxsize=3)

        # 添加 3 个项
        svc1 = cache.get("workspace1")
        svc2 = cache.get("workspace2")
        svc3 = cache.get("workspace3")

        assert len(cache.cache) == 3
        assert not svc1._closed
        assert not svc2._closed
        assert not svc3._closed

        # 添加第 4 个项，应该驱逐 workspace1（最久未使用）
        svc4 = cache.get("workspace4")

        assert len(cache.cache) == 3
        assert "workspace1" not in cache.cache
        assert "workspace2" in cache.cache
        assert "workspace3" in cache.cache
        assert "workspace4" in cache.cache

        # 验证被驱逐的服务已关闭
        assert svc1._closed, "被驱逐的服务应该被关闭"
        assert not svc2._closed
        assert not svc3._closed
        assert not svc4._closed

    def test_access_order_update(self):
        """测试 LRU 缓存的访问顺序更新"""
        cache = LRUCache(maxsize=3)

        cache.get("workspace1")
        cache.get("workspace2")
        cache.get("workspace3")

        # 访问 workspace1，使其成为最近使用
        cache.get("workspace1")

        # 添加第 4 个项，应该驱逐 workspace2（现在是最久未使用）
        cache.get("workspace4")

        assert "workspace2" not in cache.cache
        assert "workspace1" in cache.cache
        assert "workspace3" in cache.cache
        assert "workspace4" in cache.cache

    def test_clear_all_services(self):
        """测试清空缓存时释放所有资源"""
        cache = LRUCache(maxsize=10)

        # 添加多个服务
        services = []
        for i in range(5):
            svc = cache.get(f"workspace{i}")
            services.append(svc)

        assert len(cache.cache) == 5

        # 清空缓存
        cache.clear()

        assert len(cache.cache) == 0

        # 验证所有服务都已关闭
        for svc in services:
            assert svc._closed, "清空缓存时所有服务都应该被关闭"

    def test_multiple_evictions(self):
        """测试连续多次驱逐"""
        cache = LRUCache(maxsize=2)

        # 添加 5 个项，应该只保留最后 2 个
        services = []
        for i in range(5):
            svc = cache.get(f"workspace{i}")
            services.append(svc)

        assert len(cache.cache) == 2
        assert "workspace3" in cache.cache
        assert "workspace4" in cache.cache

        # 验证前 3 个服务已关闭
        for i in range(3):
            assert services[i]._closed, f"服务 {i} 应该被关闭"

        # 验证后 2 个服务未关闭
        assert not services[3]._closed
        assert not services[4]._closed


class TestRAGServiceResourceManagement:
    """测试 RAGService 资源管理"""

    @pytest.mark.asyncio
    async def test_service_close(self):
        """测试服务关闭后无法使用"""
        service = RAGService()

        # 正常使用
        chunks = await service.ingest("标题", "内容")
        assert len(chunks) > 0

        # 关闭服务
        service.close()
        assert service._closed

        # 关闭后无法导入
        with pytest.raises(RuntimeError, match="RAGService 已关闭"):
            await service.ingest("新标题", "新内容")

        # 关闭后无法检索
        with pytest.raises(RuntimeError, match="RAGService 已关闭"):
            await service.retrieve("查询")

    @pytest.mark.asyncio
    async def test_service_context_manager(self):
        """测试服务作为上下文管理器使用"""
        with RAGService() as service:
            chunks = await service.ingest("标题", "内容")
            assert len(chunks) > 0
            assert not service._closed

        # 退出上下文后自动关闭
        assert service._closed

    def test_service_idempotent_close(self):
        """测试服务可以安全地多次关闭（幂等性）"""
        service = RAGService()

        # 第一次关闭
        service.close()
        assert service._closed

        # 第二次关闭不应该报错
        service.close()
        assert service._closed

        # 第三次关闭也不应该报错
        service.close()
        assert service._closed

    @pytest.mark.asyncio
    async def test_service_memory_cleanup(self):
        """测试服务关闭后内存被清理"""
        service = RAGService()

        # 添加多个文档
        for i in range(10):
            await service.ingest(f"标题{i}", f"内容{i}" * 100)

        assert len(service.store.documents) == 10
        assert len(service.store.chunks) > 0
        assert len(service.store.chunk_embeddings) > 0

        # 关闭服务
        service.close()

        # 验证所有数据被清空
        assert len(service.store.documents) == 0
        assert len(service.store.chunks) == 0
        assert len(service.store.chunk_embeddings) == 0


class TestMemoryLeakScenarios:
    """测试真实场景下的内存泄露防护"""

    @pytest.mark.asyncio
    async def test_rapid_workspace_switching(self):
        """测试快速切换工作空间不会导致内存泄露"""
        cache = LRUCache(maxsize=5)

        # 模拟用户快速切换工作空间
        for i in range(20):
            workspace_id = f"workspace{i % 10}"  # 循环使用 10 个工作空间
            service = cache.get(workspace_id)
            await service.ingest(f"文档{i}", f"内容{i}")

        # 缓存应该保持在限制内
        assert len(cache.cache) <= 5

    @pytest.mark.asyncio
    async def test_abandoned_workspaces(self):
        """测试废弃的工作空间会被自动清理"""
        cache = LRUCache(maxsize=3)

        # 创建 3 个工作空间
        for i in range(3):
            service = cache.get(f"workspace{i}")
            await service.ingest(f"文档{i}", f"内容{i}")

        # 记录第一个工作空间的服务实例
        first_service = cache.cache["workspace0"]

        # 创建 3 个新工作空间（不再访问旧工作空间）
        for i in range(3, 6):
            service = cache.get(f"workspace{i}")
            await service.ingest(f"文档{i}", f"内容{i}")

        # 旧工作空间应该被驱逐
        assert "workspace0" not in cache.cache
        assert "workspace1" not in cache.cache
        assert "workspace2" not in cache.cache

        # 被驱逐的服务应该已关闭
        assert first_service._closed

    def test_cache_size_limit(self):
        """测试缓存大小严格限制"""
        for maxsize in [1, 5, 10, 50, 100]:
            cache = LRUCache(maxsize=maxsize)

            # 添加 2x maxsize 个工作空间
            for i in range(maxsize * 2):
                cache.get(f"workspace{i}")

            # 缓存大小应该不超过 maxsize
            assert len(cache.cache) == maxsize
